# Chapter 03: 慢思考与自省：在 ReAct 循环中剥离独立的 Thinking 阶段

Course: "从 0 开始构建 Agent Harness" - 03｜慢思考与自省：在 ReAct 循环中剥离独立的 Thinking 阶段

## What We Have

### 1. Provider 接口变更 (`tinyclaw/provider/base.py`)

`LLMProvider.generate()` 的 `available_tools` 参数类型从 `list[ToolDefinition]` 改为 `list[ToolDefinition] | None`。`None` 表达 Thinking 阶段的"剥夺工具"语义（对应 Go 的 `nil`）。

### 2. 两阶段 Main Loop (`tinyclaw/engine/loop.py`)

`AgentEngine` 新增 `enable_thinking: bool` 配置项，`run()` 内每个 Turn 拆为两阶段：

- **Phase 1 (Thinking)**：`enable_thinking=True` 时，传 `None` 给 provider，模型被迫输出纯文本思考 trace
- **Phase 2 (Action)**：恢复工具列表，模型顺着 Phase 1 的思考链精准发起工具调用

核心机制：利用 LLM 自回归特性——Phase 1 的 thinking trace 存入 context_history 后，Phase 2 模型看到自己的思考，会顺理成章地执行计划，大幅降低幻觉和瞎调工具的概率。

### 3. 升级版 Mock 验证 (`tinyclaw/main.py`)

- `MockProvider`：按 `available_tools is None` 区分 Thinking/Action 阶段
- `MockRegistry.get_available_tools()` 返回伪工具定义（使 Phase 2 能感知工具）
- `AgentEngine` 构造时传入 `enable_thinking=True`

已通过 `py -m tinyclaw` 验证两阶段流转正常。

## Key Decisions

- `available_tools=None` 表示 Thinking 阶段（对应 Go `nil`），空列表 `[]` 不等价
- `enable_thinking` 默认 `False`，简单任务可关闭以节省 Token

## Git Commits

- `0f82b81` - add: chapter 03 memory file + MEMORY.md line limit and chapter lazy-read rules
- (this commit) - add: two-phase Thinking/Action loop with enable_thinking config
