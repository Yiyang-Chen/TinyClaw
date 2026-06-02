from abc import ABC, abstractmethod

from tinyclaw.schema import Message, ToolDefinition


class LLMProvider(ABC):
    """与大模型通信的统一契约。"""

    @abstractmethod
    def generate(
        self,
        messages: list[Message],
        available_tools: list[ToolDefinition] | None,
    ) -> Message:
        """接收当前的上下文历史、可用工具列表，发起一次大模型推理。

        available_tools 为 None 时表示 Thinking 阶段——剥夺工具，强制模型输出纯文本思考。
        """
        ...
