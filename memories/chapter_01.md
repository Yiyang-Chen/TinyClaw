# Chapter 01: Architecture Blueprint + Project Skeleton

Course: "从 0 开始构建 Agent Harness" - 01｜架构演进：从 Framework 到 Harness

## What We Did

1. Created project directory `202606_TinyClaw/` and initialized git repo.
2. Created GitHub repo: https://github.com/Yiyang-Chen/TinyClaw
3. Built the Python directory skeleton mapping from the Go tutorial structure:
   - `tinyclaw/main.py` — entry point with startup sequence and TODO placeholders
   - `tinyclaw/engine/` — for MainLoop core (empty)
   - `tinyclaw/provider/` — for LLM provider abstraction (empty)
   - `tinyclaw/context_mgr/` — for token monitoring and prompt composition (empty)
   - `tinyclaw/tools/` — for tool registry and built-in tools (empty)
   - `tinyclaw/memory/` — for file-based state management (empty)
   - `tinyclaw/feishu/` — for Feishu bot integration (empty)
4. Set up `requirements.txt` with initial dependencies: openai, pydantic, pyyaml.
5. Verified entry point works: `py -m tinyclaw`
6. Established memory system (`memories/` folder) for tracking progress.

## Key Decisions

- Chose Python over Go/C++/C# for better LLM SDK support and faster prototyping.
- Used `context_mgr` instead of `context` to avoid Python builtin conflicts.
- Used `logging` module instead of `print` for consistent output ordering.
- Used `origin` remote with personal GitHub account (not `personal` remote).

## Git Commit

Commit marking chapter completion: (see git log after this file is committed)
