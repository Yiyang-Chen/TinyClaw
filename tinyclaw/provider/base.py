from abc import ABC, abstractmethod

from tinyclaw.schema import Message, ToolDefinition


class LLMProvider(ABC):
    """与大模型通信的统一契约。"""

    @abstractmethod
    def generate(
        self,
        messages: list[Message],
        available_tools: list[ToolDefinition],
    ) -> Message:
        """接收当前的上下文历史、可用工具列表，发起一次大模型推理。"""
        ...
