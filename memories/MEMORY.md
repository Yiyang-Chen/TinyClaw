# TinyClaw Memory Index

## Key Decisions

- Language: **Python** (not Go). Reason: LLM SDK support best in Python, faster prototyping, OpenClaw itself is TypeScript so scripting-to-scripting is natural.
- Project folder: `202606_TinyClaw/`, package name: `tinyclaw`
- `context_mgr/` used instead of `context/` to avoid conflict with Python builtins.
- All output uses `logging` (not `print`) to guarantee ordering.

## Current State

- Course: "从 0 开始构建 Agent Harness" (GeekBang, Tony Bai, 24 lectures)
- Progress: Chapter 01 completed
- Latest commit: see `chapter_01.md`

## Architecture

```
tinyclaw/
  main.py           # Entry point
  engine/           # Agent MainLoop
  provider/         # LLM adapters (Claude/Zhipu)
  context_mgr/      # Token monitor, prompt composer
  tools/            # Tool registry + built-in tools
  memory/           # File-based state (PLAN/TODO)
  feishu/           # Feishu integration
```

## Go -> Python Mapping

| Go | Python |
|---|---|
| struct | Pydantic BaseModel |
| interface | abc.ABC |
| goroutine/channel | asyncio/Queue |
| os/exec | subprocess |
| go run | py -m tinyclaw |

## Chapter Index

| Chapter | File | Topic |
|---|---|---|
| 01 | chapter_01.md | Architecture blueprint + project skeleton |

## Repo

- GitHub: https://github.com/Yiyang-Chen/TinyClaw
- Remote: origin
