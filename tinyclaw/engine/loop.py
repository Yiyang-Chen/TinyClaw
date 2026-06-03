import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from tinyclaw.provider.base import LLMProvider
from tinyclaw.schema import Message, Role, ToolCall, ToolResult
from tinyclaw.tools.base import Registry

log = logging.getLogger(__name__)


class AgentEngine:
    """微型 OS 的核心驱动。"""

    def __init__(
        self,
        provider: LLMProvider,
        registry: Registry,
        work_dir: str,
        enable_thinking: bool = False,
    ):
        self.provider = provider
        self.registry = registry
        self.work_dir = work_dir
        self.enable_thinking = enable_thinking

    def _execute_single(self, index: int, tool_call: ToolCall) -> tuple[int, ToolResult]:
        """在线程池中执行单个工具调用，返回 (索引, 结果) 以便按序回填。"""
        log.info("  -> [Thread] 执行工具: %s, 参数: %s", tool_call.name, tool_call.arguments)
        result = self.registry.execute(tool_call)
        if result.is_error:
            log.error("  -> [Thread] 工具执行报错: %s", result.output)
        else:
            log.info("  -> [Thread] 工具执行成功 (返回 %d 字节)", len(result.output))
        return index, result

    def run(self, user_prompt: str) -> None:
        log.info("[Engine] 引擎启动，锁定工作区: %s", self.work_dir)
        log.info("[Engine] 慢思考模式 (Thinking Phase): %s", self.enable_thinking)

        context_history: list[Message] = [
            Message(
                role=Role.SYSTEM,
                content="You are TinyClaw, an expert coding assistant. "
                "You have full access to tools in the workspace.",
            ),
            Message(role=Role.USER, content=user_prompt),
        ]

        turn_count = 0

        while True:
            turn_count += 1
            log.info("========== [Turn %d] 开始 ==========", turn_count)

            available_tools = self.registry.get_available_tools()

            # ==============================================================
            # Phase 1: 慢思考阶段 (Thinking) — 剥夺工具，强制规划
            # ==============================================================
            if self.enable_thinking:
                log.info("[Engine][Phase 1] 剥夺工具访问权，强制进入慢思考与规划阶段...")

                think_resp = self.provider.generate(context_history, None)

                if think_resp.content:
                    log.info("[内部思考 Trace]: %s", think_resp.content)
                    context_history.append(think_resp)

            # ==============================================================
            # Phase 2: 行动阶段 (Action) — 恢复工具，顺着规划执行
            # ==============================================================
            log.info("[Engine][Phase 2] 恢复工具挂载，等待模型采取行动...")

            action_resp = self.provider.generate(context_history, available_tools)
            context_history.append(action_resp)

            if action_resp.content:
                log.info("[对外回复]: %s", action_resp.content)

            # ==============================================================
            # 退出与执行逻辑
            # ==============================================================
            if not action_resp.tool_calls:
                log.info("[Engine] 模型未请求调用工具，任务宣告完成。")
                break

            n = len(action_resp.tool_calls)
            log.info("[Engine] 模型请求并发调用 %d 个工具...", n)

            # 预分配固定长度切片，线程返回 (索引, 结果)，主线程按索引回填
            results: list[ToolResult | None] = [None] * n

            with ThreadPoolExecutor(max_workers=n) as pool:
                fut_to_ctx: dict[object, tuple[int, ToolCall]] = {}
                for i, tc in enumerate(action_resp.tool_calls):
                    f = pool.submit(self._execute_single, i, tc)
                    fut_to_ctx[f] = (i, tc)

                for fut in as_completed(fut_to_ctx):
                    try:
                        idx, res = fut.result()
                    except Exception:
                        idx, tc = fut_to_ctx[fut]
                        log.exception("工具 %s 线程发生未预期异常", tc.name)
                        res = ToolResult(
                            tool_call_id=tc.id,
                            output=f"Internal error executing {tc.name}",
                            is_error=True,
                        )
                    results[idx] = res

            for i, result in enumerate(results):
                if result is None:
                    raise RuntimeError(f"Tool call {i} 未返回结果（内部错误）")
                context_history.append(
                    Message(
                        role=Role.USER,
                        content=result.output,
                        tool_call_id=action_resp.tool_calls[i].id,
                    )
                )
