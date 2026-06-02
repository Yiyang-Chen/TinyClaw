# TinyClaw Memory Index

## Project Specifics

- Package name: `tinyclaw`, run with `py -m tinyclaw`
- `context_mgr/` used instead of `context/` to avoid Python builtin conflict
- All output uses `logging` (not `print`) to guarantee ordering
- Course reference: "从 0 开始构建 Agent Harness" (GeekBang, Tony Bai, 24 lectures)

## Current State

- Progress: Chapter 02 in progress (part 1 done: Schema)
- Latest commit: see chapter index

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

## Chapter Index

| Chapter | File | Topic |
|---|---|---|
| 01 | chapter_01.md | Architecture blueprint + project skeleton |

## Repo

- GitHub: https://github.com/Yiyang-Chen/TinyClaw
- Remote: origin
