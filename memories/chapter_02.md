# Chapter 02: 核心心脏：手写 Agent 的 Main Loop

Course: "从 0 开始构建 Agent Harness" - 02｜核心心脏：手写 Agent 的 Main Loop

## What We Have

Created `tinyclaw/schema/` module — the lowest layer that all other modules depend on, but depends on nothing itself.

### Types Defined (`schema/message.py`)

| Type | Purpose |
|---|---|
| `Role` (`StrEnum`) | Message roles: SYSTEM / USER / ASSISTANT |
| `ToolCall` | Model's request to invoke a tool (id, name, arguments) |
| `ToolResult` | Tool execution result returned to model (tool_call_id, output, is_error) |
| `ToolDefinition` | Tool metadata for model understanding (name, description, input_schema) |
| `Message` | Single context message carrying role, content, tool_calls, tool_call_id |

### Key Decisions

- All types use Pydantic `BaseModel` (Go struct + JSON tag equivalent)
- `Role` uses `StrEnum` — type-safe and serializes as plain string
- Go `json.RawMessage` → `dict[str, Any]` (ToolCall.arguments)
- Go `interface{}` → `dict[str, Any]` (ToolDefinition.input_schema)

## Git Commits

- `e640c27` - add: chapter 02 part 1 - schema layer
