import os
from typing import Any

from tinyclaw.schema import ToolDefinition
from tinyclaw.tools.base import BaseTool


class EditFileTool(BaseTool):
    """对现有文件进行局部字符串替换的工具。

    比 write_file 全量覆写更安全，适合小范围代码修改。
    内置四级容错降级替换算法（fuzzy_replace），
    从精确匹配逐级降级到逐行去缩进匹配，
    以应对大模型生成 old_text 时丢失缩进 / 换行符不一致等幻觉。
    """

    def __init__(self, work_dir: str) -> None:
        self._work_dir = work_dir

    def name(self) -> str:
        return "edit_file"

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name(),
            description=(
                "对现有文件进行局部的字符串替换。这比重写整个文件更安全、更快速。"
                "请提供足够的 old_text 上下文以确保匹配的唯一性。"
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "要修改的文件路径",
                    },
                    "old_text": {
                        "type": "string",
                        "description": (
                            "文件中原有的文本。必须包含足够的上下文"
                            "（建议上下各多包含几行），以确保在文件中的唯一性。"
                        ),
                    },
                    "new_text": {
                        "type": "string",
                        "description": "要替换成的新文本",
                    },
                },
                "required": ["path", "old_text", "new_text"],
            },
        )

    def execute(self, args: dict[str, Any]) -> str:
        path = args.get("path")
        if not path:
            raise ValueError("参数解析失败: 缺少必需的 'path' 字段")

        old_text = args.get("old_text")
        if old_text is None:
            raise ValueError("参数解析失败: 缺少必需的 'old_text' 字段")

        new_text = args.get("new_text")
        if new_text is None:
            raise ValueError("参数解析失败: 缺少必需的 'new_text' 字段")

        full_path = os.path.join(self._work_dir, path)

        try:
            with open(full_path, encoding="utf-8") as f:
                original_content = f.read()
        except FileNotFoundError:
            raise ValueError(f"读取文件失败，请确认路径是否正确: {path}") from None

        new_content = fuzzy_replace(original_content, old_text, new_text)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        return f"✅ 成功修改文件: {path}"


def fuzzy_replace(original_content: str, old_text: str, new_text: str) -> str:
    """四级容错降级替换算法。

    L1 精确匹配 → L2 换行符归一化 → L3 trim space → L4 逐行去缩进滑动窗口。
    每级在确认唯一匹配后立即执行替换并返回；
    匹配到多处则报错要求模型提供更多上下文。
    """
    # L1: 精确匹配
    count = original_content.count(old_text)
    if count == 1:
        return original_content.replace(old_text, new_text, 1)
    if count > 1:
        raise ValueError(
            f"old_text 匹配到了 {count} 处，请提供更多的上下文代码以确保唯一性"
        )

    # L2: 换行符归一化（统一 \r\n → \n）
    normalized_content = original_content.replace("\r\n", "\n")
    normalized_old = old_text.replace("\r\n", "\n")

    count = normalized_content.count(normalized_old)
    if count == 1:
        return normalized_content.replace(normalized_old, new_text, 1)

    # L3: Trim Space 匹配（忽略首尾空行和空格）
    trimmed_old = normalized_old.strip()
    if trimmed_old:
        count = normalized_content.count(trimmed_old)
        if count == 1:
            return normalized_content.replace(trimmed_old, new_text, 1)

    # L4: 逐行去缩进匹配（最强力的容错）
    return _line_by_line_replace(normalized_content, normalized_old, new_text)


def _line_by_line_replace(content: str, old_text: str, new_text: str) -> str:
    """将文本按行切割，去除每行首尾空白后进行滑动窗口匹配。"""
    content_lines = content.split("\n")
    old_lines = old_text.strip().split("\n")

    if not old_lines or len(content_lines) < len(old_lines):
        raise ValueError("找不到该代码片段")

    old_lines = [line.strip() for line in old_lines]

    match_count = 0
    match_start = -1
    match_end = -1

    for i in range(len(content_lines) - len(old_lines) + 1):
        is_match = all(
            content_lines[i + j].strip() == old_lines[j]
            for j in range(len(old_lines))
        )
        if is_match:
            match_count += 1
            match_start = i
            match_end = i + len(old_lines)

    if match_count == 0:
        raise ValueError(
            "在文件中未找到 old_text，请先调用 read_file 仔细确认文件内容和缩进"
        )
    if match_count > 1:
        raise ValueError(
            f"模糊匹配到了 {match_count} 处相似代码，请提供更多上下行代码以精确定位"
        )

    result_lines = content_lines[:match_start] + [new_text] + content_lines[match_end:]
    return "\n".join(result_lines)
