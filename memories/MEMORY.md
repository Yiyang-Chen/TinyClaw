# TinyClaw Memory Index

## Project Specifics

- Package name: `tinyclaw`, run with `py -m tinyclaw`
- `context_mgr/` used instead of `context/` to avoid Python builtin conflict
- All output uses `logging` (not `print`) to guarantee ordering
- Course reference: "从 0 开始构建 Agent Harness" (GeekBang, Tony Bai, 24 lectures)

## Current State

- Progress: Chapter 02 completed
- Latest commit: `b4cbb46`

## Architecture

```
tinyclaw/
  main.py           # Entry point
  schema/           # Unified data types (Message, ToolCall, etc.)
  engine/           # Agent MainLoop
  provider/         # LLM adapters (Claude/Zhipu)
  context_mgr/      # Token monitor, prompt composer
  tools/            # Tool registry + built-in tools
  memory/           # File-based state (PLAN/TODO)
  feishu/           # Feishu integration
```

## Key Decisions

- Schema uses Pydantic `BaseModel` (Go struct + JSON tag equivalent)
- `Role` uses `StrEnum` (type-safe + serializes as plain string)
- Go `json.RawMessage` / `interface{}` → Python `dict[str, Any]`
- Go `interface` → Python `ABC` (abstract base class)
- Go `context.Context` 暂不引入，当前无超时/取消需求，后续按需补充
- Go `fmt.Errorf` 错误返回 → Python 异常自然传播

## Open Issues

- Tool result 的 role：当前用 `Role.USER` + `tool_call_id` 承载（跟随 Go 课程原版），但 OpenAI API 要求 `role: "tool"`。接入真实 Provider 时需决定是在 Schema 层加 `TOOL` role 还是在 Provider 层做转换。

## Chapter Index

| Chapter | File | Topic |
|---|---|---|
| 01 | chapter_01.md | Architecture blueprint + project skeleton |
| 02 | chapter_02.md | 核心心脏：手写 Agent 的 Main Loop |

## Repo

- GitHub: https://github.com/Yiyang-Chen/TinyClaw
- Remote: origin
