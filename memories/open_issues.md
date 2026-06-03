# Open Issues

## 高危

- **路径穿越**：read_file / write_file 均未防御 `../` 和绝对路径逃逸 work_dir（write_file 更危险，可在任意位置创建目录+文件）
- **bash 超时残留**：`subprocess.run` 超时后子进程可能残留（应加 `process.kill()`）

## 中等（edit_file 原版设计问题，忠实保留）

- **edit_file L2/L3 换行符丢失**：L2/L3 匹配成功后返回 `normalized_content`（全文 `\r\n`→`\n`），导致只改一行却把整个文件的行尾都改了（Windows 下尤其严重）
- **edit_file L2/L3 多重匹配静默降级**：L1 在 `count>1` 时正确报错，但 L2/L3 的 `count>1` 会静默 fallthrough 到更宽松的级别；更宽松的级别只会匹配到更多，逻辑矛盾
- **edit_file 空/全空白 old_text**：`"".count("")` 返回 `len+1`，L1 报出误导性错误；`"\n\n"` 经 strip+split 变成 `[""]`，L4 会匹配任意空行

## 中等

- **read_file 编码脆弱**：`open(path, encoding="utf-8")` 硬编码 UTF-8，遇到 UTF-16 LE（如 PowerShell `echo > file` 产生的 BOM `0xFF 0xFE` 文件）直接抛 `UnicodeDecodeError`。应考虑 fallback 检测（如 `chardet` / BOM 嗅探）或至少在异常信息中提示编码问题
- **bash 跨平台**：Windows 上 `shell=True` 实际调用 cmd 而非 bash，工具名/描述有误导
- read_file `f.read()` 全量读入后再截断，大文件仍会 OOM（应改 `f.read(MAX_LEN+1)`）
- write_file 返回消息 "字节" 应为 "字符"（`len(content)` 计的是字符数）
- write_file / bash 缺少 `OSError` 捕获（磁盘满、权限不足等会抛未处理异常）

## 中等（并发执行，教程原版设计问题）

- **无 concurrency-safe 分批逻辑**：当前并发执行对同一 Turn 的所有 tool_calls 无差别并行。缺少 Claude Code 式的 `isConcurrencySafe` 声明机制——应由每个工具声明自身是否并发安全（read_file=safe, write_file/edit_file/bash=unsafe），Harness 将连续的 safe 工具并行、遇到 unsafe 则串行。当前实现在模型同时下发多个 write 到同一文件时可能产生竞态
- **`max_workers` 无上限**：Go 原版用 goroutine（极轻量）所以不设上限，Python 线程较重但沿用了同样策略。当模型返回大量 tool_calls 时可能创建过多线程

## 低等

- Claude 连续同 role 消息：多 tool_result 追加为 USER + thinking 模式连续 ASSISTANT → API 400
- OpenAI `json.loads(tc.function.arguments)` 无异常保护，畸形 JSON 报错缺上下文
- Claude `max_tokens` 硬编码 4096，应提为构造参数
- ToolRegistry `except Exception` 缺 `log.exception`，异常 traceback 丢失
