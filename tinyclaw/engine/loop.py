import logging

from tinyclaw.provider.base import LLMProvider
from tinyclaw.schema import Message, Role
from tinyclaw.tools.base import Registry

log = logging.getLogger(__name__)


class AgentEngine:
    """微型 OS 的核心驱动。"""

    def __init__(self, provider: LLMProvider, registry: Registry, work_dir: str):
        self.provider = provider
        self.registry = registry
        self.work_dir = work_dir

    def run(self, user_prompt: str) -> None:
        log.info("[Engine] 引擎启动，锁定工作区: %s", self.work_dir)

        # 1. 初始化会话的 Context（上下文内存）
        # 真实场景中会由动态 Prompt 组装器加载 AGENTS.md，目前先硬编码
        context_history: list[Message] = [
            Message(
                role=Role.SYSTEM,
                content="You are TinyClaw, an expert coding assistant. "
                "You have full access to tools in the workspace.",
            ),
            Message(role=Role.USER, content=user_prompt),
        ]

        turn_count = 0

        # 2. The Main Loop: 心跳开始（标准的 ReAct 循环）
        while True:
            turn_count += 1
            log.info("========== [Turn %d] 开始 ==========", turn_count)

            available_tools = self.registry.get_available_tools()

            log.info("[Engine] 正在思考 (Reasoning)...")
            response_msg = self.provider.generate(context_history, available_tools)

            context_history.append(response_msg)

            if response_msg.content:
                log.info("模型: %s", response_msg.content)

            # 3. 退出条件：模型没有请求任何工具调用，任务完成
            if not response_msg.tool_calls:
                log.info("[Engine] 任务完成，退出循环。")
                break

            # 4. 执行行动 (Action) 与获取观察结果 (Observation)
            log.info(
                "[Engine] 模型请求调用 %d 个工具...", len(response_msg.tool_calls)
            )

            for tool_call in response_msg.tool_calls:
                log.info(
                    "  -> 执行工具: %s, 参数: %s", tool_call.name, tool_call.arguments
                )

                result = self.registry.execute(tool_call)

                if result.is_error:
                    log.error("  -> 工具执行报错: %s", result.output)
                else:
                    log.info(
                        "  -> 工具执行成功 (返回 %d 字节)", len(result.output)
                    )

                # 将 Observation 封装为 User Message 追加到上下文
                # ToolCallID 必须携带——维系大模型推理链条的关键
                observation_msg = Message(
                    role=Role.USER,
                    content=result.output,
                    tool_call_id=tool_call.id,
                )
                context_history.append(observation_msg)

            # 循环回到开头，模型将带着新的 Observation 继续下一轮思考...
