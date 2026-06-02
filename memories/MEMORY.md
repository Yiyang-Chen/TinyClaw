# TinyClaw Memory Index

## Project Specifics

- Run: `py -m tinyclaw` | Repo: https://github.com/Yiyang-Chen/TinyClaw (origin)
- Course: GeekBang "从 0 开始构建 Agent Harness" (Tony Bai, 24 lectures)
- `context_mgr/` avoids Python builtin conflict; all output via `logging`
- API key via `.env` + `python-dotenv`（`.env` in `.gitignore`）

## Current State

- Progress: Chapter 07 completed

## Architecture

```
tinyclaw/
  main.py, schema/, engine/, provider/, tools/
  provider/: base.py (ABC), openai_provider.py, claude_provider.py
  tools/: base.py (BaseTool ABC + Registry ABC + ToolRegistry impl)
          read_file.py, write_file.py, bash.py, edit_file.py
```

## Key Decisions

- Pydantic `BaseModel` for schema, `Role` as `StrEnum`
- Go `interface` → ABC, Go `json.RawMessage` → `dict[str, Any]`, exceptions instead of error returns
- `enable_thinking`: 两阶段循环开关，`available_tools=None` 表示 Thinking 阶段（`[]` 不等价）
- Tool result: 内部 `Role.USER` + `tool_call_id`，Provider 层各自转换
- Provider: `__init__(model, api_key, base_url)` + `@classmethod zhipu()` 工厂方法
- Tool 层：`BaseTool` ABC → `ToolRegistry` dict O(1) 路由，所有工具注入 `work_dir`
- 截断保护：read_file/bash MAX_LEN=8000；bash TIMEOUT=30s
- edit_file：四级容错降级（L1 精确→L2 \r\n 归一→L3 trim→L4 逐行去缩进滑窗）

## Open Issues

- 详见 `memories/open_issues.md`（13 条，含路径穿越、edit_file 原版设计问题等）

## Chapter Index

| Ch | File | Topic |
|---|---|---|
| 01 | chapter_01.md | Architecture blueprint + project skeleton |
| 02 | chapter_02.md | 核心心脏：手写 Agent 的 Main Loop |
| 03 | chapter_03.md | 慢思考与自省：在 ReAct 循环中剥离独立的 Thinking 阶段 |
| 04 | chapter_04.md | 代码实战：实现双协议 Provider 适配器 |
| 05 | chapter_05.md | 工具与执行层：BaseTool + ToolRegistry + read_file |
| 06 | chapter_06.md | write_file + bash 工具实现 |
| 07 | chapter_07.md | edit_file 四级容错局部替换工具 |
