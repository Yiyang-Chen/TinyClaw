# TinyClaw Memory Index

## Project Specifics

- Run: `py -m tinyclaw` | Repo: https://github.com/Yiyang-Chen/TinyClaw (origin)
- `context_mgr/` used instead of `context/` to avoid Python builtin conflict
- All output uses `logging` (not `print`) to guarantee ordering
- Course: "从 0 开始构建 Agent Harness" (GeekBang, Tony Bai, 24 lectures)
- API key via `.env` + `python-dotenv`，`.env` 已在 `.gitignore`

## Current State

- Progress: Chapter 04 completed

## Architecture

```
tinyclaw/
  main.py, schema/, engine/, provider/, context_mgr/, tools/, memory/, feishu/
  provider/: base.py (ABC), openai_provider.py, claude_provider.py
```

## Key Decisions

- Pydantic `BaseModel` for schema, `Role` as `StrEnum`
- Go `interface` → ABC, Go `json.RawMessage` → `dict[str, Any]`
- No `context.Context` (no timeout/cancel need yet), exceptions instead of error returns
- `enable_thinking`: 两阶段循环开关，`available_tools=None` 表示 Thinking 阶段（`[]` 不等价）
- Tool result: 内部 `Role.USER` + `tool_call_id`，Provider 层各自转换（OpenAI→`role:"tool"`, Claude→`tool_result` block）
- Provider 构造：通用 `__init__(model, api_key, base_url)` + `@classmethod zhipu()` 工厂方法

## Open Issues

- Claude 连续同 role 消息：多 tool_result 各自追加为 USER + thinking 模式连续 ASSISTANT，会导致 Anthropic API 400（接入真实 Claude 时需修）
- OpenAI `json.loads(tc.function.arguments)` 无异常保护，模型返回畸形 JSON 时报错缺上下文
- Claude `max_tokens` 硬编码 4096，应提为构造参数

## Chapter Index

| Ch | File | Topic |
|---|---|---|
| 01 | chapter_01.md | Architecture blueprint + project skeleton |
| 02 | chapter_02.md | 核心心脏：手写 Agent 的 Main Loop |
| 03 | chapter_03.md | 慢思考与自省：在 ReAct 循环中剥离独立的 Thinking 阶段 |
| 04 | chapter_04.md | 代码实战：实现双协议 Provider 适配器 |
