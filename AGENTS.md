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

Chapter boundaries are **determined by the user** — the user will explicitly tell the agent when a chapter ends and when to create the summary. Do NOT auto-create chapter files without the user's instruction.

At the end of each chapter, a new file `memories/chapter_XX.md` is created summarizing:
- What was implemented in that chapter
- Which git commit marks the chapter's completion
- Key technical decisions made

The agent can use these files to resume context at any point.
