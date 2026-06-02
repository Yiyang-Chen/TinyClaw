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

`LLMProvider` ABC — `generate(messages, available_tools) -> Message`

### 3. Tools 接口 (`tinyclaw/tools/base.py`)

`Registry` ABC — `get_available_tools()` and `execute(call) -> ToolResult`

### 4. Engine 核心循环 (`tinyclaw/engine/loop.py`)

`AgentEngine` — ReAct Main Loop 实现：
- 初始化上下文（System prompt + User prompt）
- 循环：调用 Provider → 检查 ToolCalls → 执行工具 → Observation 回填 → 下一轮
- 退出条件：模型不再请求工具调用

### 5. Mock 验证 (`tinyclaw/main.py`)

`MockProvider` + `MockRegistry` 验证 Main Loop：
- Turn 1: 模型请求调用 bash → 工具返回伪造输出
- Turn 2: 模型输出最终结果 → 循环退出

已通过 `py -m tinyclaw` 验证运行正常。

## Key Decisions

- Pydantic `BaseModel` 替代 Go struct + JSON tag
- `Role` 用 `StrEnum`（类型安全 + 序列化为纯字符串）
- Go `json.RawMessage` / `interface{}` → `dict[str, Any]`
- Go `interface` → Python `ABC`
- Go `context.Context` 暂不引入，当前无超时/取消需求
- Go `fmt.Errorf` 错误返回 → Python 异常自然传播

## Git Commits

- `e640c27` - add: schema layer
- `f4664f4` - mod: chapter title + chapter file + AGENTS.md rule
- `6d33d2b` - add: provider and tools interfaces
