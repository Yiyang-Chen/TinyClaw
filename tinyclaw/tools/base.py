import logging
from abc import ABC, abstractmethod
from typing import Any

from tinyclaw.schema import ToolCall, ToolDefinition, ToolResult

log = logging.getLogger(__name__)


class BaseTool(ABC):
    """所有具体工具必须实现的通用接口。

    对应 Go 版 BaseTool interface:
      Name()       → 工具的全局唯一名称（大模型通过这个名字调用它）
      Definition() → 提交给大模型的工具元信息和参数 JSON Schema
      Execute()    → 接收大模型吐出的参数，执行具体业务逻辑
    """

    @abstractmethod
    def name(self) -> str:
        """返回工具的全局唯一名称。"""
        ...

    @abstractmethod
    def definition(self) -> ToolDefinition:
        """返回用于提交给大模型的工具元信息和参数 JSON Schema。"""
        ...

    @abstractmethod
    def execute(self, args: dict[str, Any]) -> str:
        """接收大模型吐出的参数字典，执行具体业务逻辑并返回结果字符串。

        Go 版签名为 Execute(ctx, json.RawMessage) (string, error)。
        Python 侧：Provider 层已将 JSON 解析为 dict；异常代替 error 返回。
        """
        ...


class Registry(ABC):
    """工具的注册与分发执行接口。"""

    @abstractmethod
    def register(self, tool: BaseTool) -> None:
        """挂载一个新的工具到系统中。"""
        ...

    @abstractmethod
    def get_available_tools(self) -> list[ToolDefinition]:
        """返回当前系统挂载的所有可用工具的 Schema，供 Main Loop 交给 Provider。"""
        ...

    @abstractmethod
    def execute(self, call: ToolCall) -> ToolResult:
        """实际路由并执行模型请求的工具调用。"""
        ...


class ToolRegistry(Registry):
    """Registry 接口的默认实现。

    使用 dict 以工具的 name 作为 key 进行 O(1) 路由查找。
    对应 Go 版 registryImpl struct。
    """

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        name = tool.name()
        if name in self._tools:
            log.warning("[Registry] 工具 '%s' 已经被注册，将被覆盖。", name)
        self._tools[name] = tool
        log.info("[Registry] 成功挂载工具: %s", name)

    def get_available_tools(self) -> list[ToolDefinition]:
        return [tool.definition() for tool in self._tools.values()]

    def execute(self, call: ToolCall) -> ToolResult:
        # 1. 路由查找：找不到工具说明模型产生了幻觉，直接向模型抛出错误
        tool = self._tools.get(call.name)
        if tool is None:
            return ToolResult(
                tool_call_id=call.id,
                output=f"Error: 系统中不存在名为 '{call.name}' 的工具。",
                is_error=True,
            )

        # 2. 执行工具逻辑：将参数字典交给具体工具
        try:
            output = tool.execute(call.arguments)
        except Exception as e:
            return ToolResult(
                tool_call_id=call.id,
                output=f"Error executing {call.name}: {e}",
                is_error=True,
            )

        # 3. 封装结果返回给 Main Loop
        return ToolResult(
            tool_call_id=call.id,
            output=output,
            is_error=False,
        )
