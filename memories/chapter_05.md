# Chapter 05: 工具与执行层：BaseTool + ToolRegistry + read_file

Course: "从 0 开始构建 Agent Harness" - 05｜驾驭工程：工具注册与执行

## What We Have

### 1. BaseTool ABC (`tinyclaw/tools/base.py`)

所有具体工具必须实现的通用接口，三方法：
- `name() -> str` — 工具的全局唯一名称
- `definition() -> ToolDefinition` — 提交给大模型的元信息 + JSON Schema
- `execute(args: dict[str, Any]) -> str` — 执行业务逻辑，异常代替 error 返回

### 2. ToolRegistry (`tinyclaw/tools/base.py`)

`Registry` ABC 的默认实现：
- `dict[str, BaseTool]` 做 O(1) 路由查找
- `register(tool)` 挂载工具（重复注册时 warning 并覆盖）
- `execute(call)` 三步：路由查找 → try/except 执行 → 包装为 ToolResult
- 找不到工具时返回 `is_error=True`（模型幻觉检测），不抛异常保引擎不崩

### 3. ReadFileTool (`tinyclaw/tools/read_file.py`)

第一个真实物理工具：
- 构造注入 `work_dir`，限制操作范围
- `execute` 拼接路径 → 读文件 → MAX_LEN=8000 截断保护
- 参数校验：缺少 `path` 字段时 raise ValueError

### 4. main.py 接入真实工具

- `MockRegistry` 完全移除
- 组装：`ToolRegistry()` → `register(ReadFileTool(work_dir))` → `AgentEngine`
- 测试 prompt 要求模型读取 `hello.txt` 并总结
- `enable_thinking=False`（任务简单，加快速度）

## Key Decisions

- `Registry` ABC 新增 `register()` 抽象方法（之前只有 get_available_tools + execute）
- Go `json.RawMessage` 由各工具内部反序列化 → Python 侧 Provider 已完成解析，工具直接收 `dict`
- 错误处理：工具 raise 异常 → Registry 统一捕获包装为 ToolResult(is_error=True)
- 截断用字符数（非字节数），与 Go 版 `len(content)` 按字节略有差异

## Git Commits

- (this commit)
