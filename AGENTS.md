# TinyClaw Agent Rules

## Project Overview

TinyClaw is a Python reimplementation of the `go-tiny-claw` Agent Harness from the GeekBang course "从 0 开始构建 Agent Harness". The course uses Go; this project translates it to Python.

## Memory System

The `memories/` folder tracks project progress and key decisions.

### MEMORY.md (Required Reading)

`memories/MEMORY.md` is the **core memory file** — a compact index of key decisions, architecture choices, and current project state. It must never exceed 50 lines.

**Rules:**
- Before making any modification to the project, **always read `memories/MEMORY.md` first** to understand current architecture and decisions.
- At the end of each chapter or modification round, update `MEMORY.md` to reflect the latest state.
- Only keep the most important content in `MEMORY.md`; use references to chapter files for details.

**What to record:** Only record **project-specific knowledge** that an agent would not know by default. For example:
- YES: how to run this project (`py -m tinyclaw`), `context_mgr` was used instead of `context`, project-specific naming conventions
- NO: general language differences (Go vs Python syntax), how `logging` works in Python, what Pydantic is

### Chapter Files

Each chapter has a file `memories/chapter_XX.md` that is **created or updated** when:
1. The user says "记录一下" or similar
2. The chapter ends

**Content rules:**
- Always show the **current latest state** of the chapter — what has been implemented so far, key decisions, and git commits
- Do NOT record modification history or change logs — only the final accumulated result
- Each update **overwrites** the previous content with the latest snapshot

Do NOT auto-create or auto-update chapter files without the user's instruction.

The agent can use these files to resume context at any point.
