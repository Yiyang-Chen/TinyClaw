# Chapter 06: write_file + bash 工具实现

## 实现内容

本章新增两个工具，补全 Agent 的物理动作能力：

### WriteFileTool (`tinyclaw/tools/write_file.py`)

- 参数：`path`（相对工作区）、`content`（文件内容）
- `os.makedirs` 自动递归创建父目录
- 写入后返回路径 + 字节数反馈

### BashTool (`tinyclaw/tools/bash.py`)

- 参数：`command`（shell 命令字符串）
- `subprocess.run(shell=True, cwd=work_dir)` 执行，捕获 stdout + stderr
- 30s 超时保护（`TIMEOUT_SECONDS`），8000 字符截断保护（`MAX_OUTPUT_LEN`）
- 返回格式：STDOUT / STDERR / EXIT_CODE

### 集成改动

- `tools/__init__.py`：导出 `BashTool`、`WriteFileTool`
- `main.py`：注册三工具（read_file + write_file + bash），prompt 改为三步连贯任务（查版本 → 写文件 → 运行验证）

## 当前工具清单

| Tool | File | 参数 |
|------|------|------|
| read_file | read_file.py | path |
| write_file | write_file.py | path, content |
| bash | bash.py | command |
