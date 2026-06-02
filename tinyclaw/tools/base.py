from abc import ABC, abstractmethod

from tinyclaw.schema import ToolCall, ToolDefinition, ToolResult


class Registry(ABC):
    """工具的注册与分发执行接口。"""

    @abstractmethod
    def get_available_tools(self) -> list[ToolDefinition]:
        """返回当前系统挂载的所有可用工具的 Schema。"""
        ...

    @abstractmethod
    def execute(self, call: ToolCall) -> ToolResult:
        """实际执行模型请求的工具，并返回结果。"""
        ...
