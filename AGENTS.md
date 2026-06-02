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

### Chapter Files

At the end of each chapter, a new file `memories/chapter_XX.md` is created summarizing:
- What was implemented in that chapter
- Which git commit marks the chapter's completion
- Key technical decisions made

The agent can use these files to resume context at any point.

## Run Command

```
py -m tinyclaw
```

## Project Structure

```
tinyclaw/            # Main package
  main.py            # Entry point (corresponds to cmd/claw/main.go)
  engine/            # MainLoop core
  provider/          # LLM provider abstraction (Claude/Zhipu)
  context_mgr/       # Token monitoring, prompt composition
  tools/             # Tool registry, built-in tools (bash/edit)
  memory/            # File-based memory state
  feishu/            # Feishu bot integration
```

## Go -> Python Mapping

| Go | Python |
|---|---|
| `struct` + json tag | Pydantic `BaseModel` |
| `interface` | `abc.ABC` |
| `goroutine` / `channel` | `asyncio` / `Queue` |
| `os/exec` | `subprocess` |
| `go run cmd/claw/main.go` | `py -m tinyclaw` |
