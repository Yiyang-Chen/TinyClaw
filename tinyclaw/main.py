import logging
import os

from tinyclaw.engine import AgentEngine
from tinyclaw.provider.base import LLMProvider
from tinyclaw.schema import Message, Role, ToolCall, ToolDefinition, ToolResult
from tinyclaw.tools.base import Registry

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


# ==========================================
# 1. 升级版 Mock Provider
# ==========================================
class MockProvider(LLMProvider):
    def __init__(self):
        self._action_turn = 0

    def generate(
        self, messages: list[Message], available_tools: list[ToolDefinition] | None
    ) -> Message:
        # Phase 1: Thinking — 工具列表为空，模型被迫输出纯文本思考
        if available_tools is None:
            return Message(
                role=Role.ASSISTANT,
                content="【推理中】目标是检查文件。我不能直接盲猜，"
                "我需要先调用 bash 工具执行 ls 命令，看看当前目录下有什么，然后再做定夺。",
            )

        # Phase 2: Action — 工具列表恢复，顺着 Thinking 执行
        self._action_turn += 1
        if self._action_turn == 1:
            return Message(
                role=Role.ASSISTANT,
                content="我要执行我刚才计划的步骤了。",
                tool_calls=[
                    ToolCall(
                        id="call_123",
                        name="bash",
                        arguments={"command": "ls -la"},
                    )
                ],
            )

        return Message(
            role=Role.ASSISTANT,
            content="根据工具返回的结果，我看到了 main.py，任务圆满完成！",
        )


# ==========================================
# 2. 伪造的 Tool Registry
# ==========================================
class MockRegistry(Registry):
    def get_available_tools(self) -> list[ToolDefinition]:
        return [ToolDefinition(name="bash", description="Execute bash commands")]

    def execute(self, call: ToolCall) -> ToolResult:
        return ToolResult(
            tool_call_id=call.id,
            output="-rw-r--r--  1 user group  234 Oct 24 10:00 main.py\n",
            is_error=False,
        )


# ==========================================
# 3. 组装运行
# ==========================================
def main():
    work_dir = os.getcwd()

    pvd = MockProvider()
    reg = MockRegistry()

    eng = AgentEngine(pvd, reg, work_dir, enable_thinking=True)

    eng.run("帮我检查当前目录的文件")


if __name__ == "__main__":
    main()
