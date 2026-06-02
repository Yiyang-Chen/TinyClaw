from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class Role(StrEnum):
    """消息角色，与大模型沟通的基石。"""

    SYSTEM = "system"       # 系统提示词：确立 Agent 的性格与红线
    USER = "user"           # 用户输入 / 工具执行的返回结果 (Observation)
    ASSISTANT = "assistant"  # 模型的输出：包含推理(Reasoning)或工具调用(ToolCall)


class ToolCall(BaseModel):
    """模型请求调用某个具体的工具。"""

    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    """工具在本地执行完毕后返回的结果。"""

    tool_call_id: str
    output: str
    is_error: bool = False


class ToolDefinition(BaseModel):
    """大模型可以调用的工具元信息（供模型理解工具有什么用）。"""

    name: str
    description: str
    input_schema: dict[str, Any] = Field(default_factory=dict)


class Message(BaseModel):
    """上下文中传递的单条消息。"""

    role: Role
    content: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)
    tool_call_id: str | None = None
