# Chapter 02: 核心心脏：手写 Agent 的 Main Loop

Course: "从 0 开始构建 Agent Harness" - 02｜核心心脏：手写 Agent 的 Main Loop

## What We Have

### 1. Schema 层 (`tinyclaw/schema/`)

最底层的统一数据结构，所有模块依赖它，它不依赖任何模块。

| Type | Purpose |
|---|---|
| `Role` (`StrEnum`) | Message roles: SYSTEM / USER / ASSISTANT |
| `ToolCall` | Model's request to invoke a tool (id, name, arguments) |
| `ToolResult` | Tool execution result (tool_call_id, output, is_error) |
| `ToolDefinition` | Tool metadata for model (name, description, input_schema) |
| `Message` | Single context message (role, content, tool_calls, tool_call_id) |

### 2. Provider 接口 (`tinyclaw/provider/base.py`)

`LLMProvider` ABC — 定义 `generate(messages, available_tools) -> Message`

### 3. Tools 接口 (`tinyclaw/tools/base.py`)

`Registry` ABC — 定义 `get_available_tools()` 和 `execute(call) -> ToolResult`

## Key Decisions

- Pydantic `BaseModel` 替代 Go struct + JSON tag
- `Role` 用 `StrEnum`（类型安全 + 序列化为纯字符串）
- Go `json.RawMessage` / `interface{}` → `dict[str, Any]`
- Go `interface` → Python `ABC`
- Go `context.Context` 暂不引入，当前无超时/取消需求

## Git Commits

- `e640c27` - add: schema layer
- `f4664f4` - mod: chapter title + chapter file + AGENTS.md rule
