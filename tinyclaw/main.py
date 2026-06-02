import logging
import os

from tinyclaw.engine import AgentEngine
from tinyclaw.provider.base import LLMProvider
from tinyclaw.schema import Message, Role, ToolCall, ToolDefinition, ToolResult
from tinyclaw.tools.base import Registry

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


# ==========================================
# 1. 伪造的大模型 Provider
# ==========================================
class MockProvider(LLMProvider):
    def __init__(self):
        self._turn = 0

    def generate(
        self, messages: list[Message], available_tools: list[ToolDefinition]
    ) -> Message:
        self._turn += 1
        if self._turn == 1:
            return Message(
                role=Role.ASSISTANT,
                content="让我来看看当前目录下有什么文件。",
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
            content="我看到了文件列表，里面包含 main.py，任务完成！",
        )


# ==========================================
# 2. 伪造的 Tool Registry
# ==========================================
class MockRegistry(Registry):
    def get_available_tools(self) -> list[ToolDefinition]:
        return []

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

    eng = AgentEngine(pvd, reg, work_dir)

    eng.run("帮我检查当前目录的文件")


if __name__ == "__main__":
    main()
