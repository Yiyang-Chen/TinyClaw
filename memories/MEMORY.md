# TinyClaw Memory Index

## Project Specifics

- Package name: `tinyclaw`, run with `py -m tinyclaw`
- `context_mgr/` used instead of `context/` to avoid Python builtin conflict
- All output uses `logging` (not `print`) to guarantee ordering
- Course reference: "从 0 开始构建 Agent Harness" (GeekBang, Tony Bai, 24 lectures)

## Current State

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

## Chapter Index

| Chapter | File | Topic |
|---|---|---|
| 01 | chapter_01.md | Architecture blueprint + project skeleton |

## Repo

- GitHub: https://github.com/Yiyang-Chen/TinyClaw
- Remote: origin
