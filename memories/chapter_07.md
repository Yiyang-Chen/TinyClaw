# Chapter 07: edit_file 四级容错局部替换工具

## 本章目标

实现 `edit_file` 工具，支持对现有文件的局部字符串替换（对应 Go 版 `EditFileTool`）。核心亮点是内置四级容错降级替换算法 `fuzzy_replace`，容忍大模型生成 `old_text` 时丢失缩进、换行符不一致等幻觉。

## 新增文件

- `tinyclaw/tools/edit_file.py` — `EditFileTool` 类 + `fuzzy_replace` + `_line_by_line_replace`

## 修改文件

- `tinyclaw/tools/__init__.py` — 导出 `EditFileTool`
- `tinyclaw/main.py` — 挂载 `EditFileTool`，prompt 改为局部替换 `server.go` 的测试场景
- `server.go` — 项目根目录测试文件（有缩进的 Go 代码，用于验证 L4 模糊匹配）

## 核心实现：四级容错降级算法

`fuzzy_replace(original_content, old_text, new_text)` 的匹配策略：

| 级别 | 策略 | 处理的幻觉类型 |
|------|------|---------------|
| L1 | 精确匹配 `str.count` + `str.replace` | 无幻觉，理想情况 |
| L2 | `\r\n` → `\n` 归一化后重试 | Windows/Unix 换行符不一致 |
| L3 | `old_text.strip()` 后重试 | 模型在 old_text 首尾添加多余空行/空格 |
| L4 | 逐行 `.strip()` + 滑动窗口匹配 | 模型完全丢失缩进（最强容错） |

每级都检查唯一性：匹配 0 处 → 降级到下一级；匹配 1 处 → 执行替换；匹配多处 → 报错要求更多上下文。

## `new_text` 不做缩进修正

经调研 Claude Code 和 Cursor 的做法：两者都不对 `new_text` 做自动缩进对齐，依赖模型自行生成正确缩进。TinyClaw 沿用同样策略。L3/L4 触发时如果 `new_text` 缩进不对，替换后格式可能不美观，但优于匹配失败导致 Agent 死循环。

## 关键设计决策

- `fuzzy_replace` 和 `_line_by_line_replace` 作为模块级函数（非类方法），便于单独测试
- 错误信息直接返回给模型（如"匹配到 N 处"、"请先调用 read_file"），引导模型自行纠正
- L4 滑动窗口中 `new_text` 作为整体单行插入到 `result_lines`，而非按行拆分

## Git Commits

- 待提交
