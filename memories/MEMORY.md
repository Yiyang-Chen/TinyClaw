# TinyClaw Memory Index

## Project Specifics

- Run: `py -m tinyclaw` | Repo: https://github.com/Yiyang-Chen/TinyClaw (origin)
- `context_mgr/` used instead of `context/` to avoid Python builtin conflict
- All output uses `logging` (not `print`) to guarantee ordering
- Course: "从 0 开始构建 Agent Harness" (GeekBang, Tony Bai, 24 lectures)

## Current State

- Progress: Chapter 03 completed

## Architecture

```
tinyclaw/
  main.py, schema/, engine/, provider/, context_mgr/, tools/, memory/, feishu/
```

## Key Decisions

- Pydantic `BaseModel` for schema, `Role` as `StrEnum`
- Go `interface` → ABC, Go `json.RawMessage` → `dict[str, Any]`
- No `context.Context` (no timeout/cancel need yet), exceptions instead of error returns
- `enable_thinking`: 两阶段循环开关，`available_tools=None` 表示 Thinking 阶段（`[]` 不等价）

## Open Issues

- Tool result role: 当前用 `Role.USER` + `tool_call_id`，接入真实 Provider 时需决定加 `TOOL` role 还是 Provider 层转换

## Chapter Index

| Ch | File | Topic |
|---|---|---|
| 01 | chapter_01.md | Architecture blueprint + project skeleton |
| 02 | chapter_02.md | 核心心脏：手写 Agent 的 Main Loop |
| 03 | chapter_03.md | 慢思考与自省：在 ReAct 循环中剥离独立的 Thinking 阶段 |
