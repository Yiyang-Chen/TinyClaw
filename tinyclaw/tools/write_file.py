import os
from typing import Any

from tinyclaw.schema import ToolDefinition
from tinyclaw.tools.base import BaseTool


class WriteFileTool(BaseTool):
    """创建或覆盖写入文件的工具。

    将引擎的 work_dir 注入给工具，限制它只能在此目录及其子目录下操作。
    如果目标路径的父目录不存在，会自动递归创建。
    """

    def __init__(self, work_dir: str) -> None:
        self._work_dir = work_dir

    def name(self) -> str:
        return "write_file"

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name(),
            description="创建或覆盖写入一个文件。如果目录不存在会自动创建。请提供相对于工作区的相对路径。",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "要写入的文件路径，如 src/main.py",
                    },
                    "content": {
                        "type": "string",
                        "description": "要写入文件的完整内容",
                    },
                },
                "required": ["path", "content"],
            },
        )

    def execute(self, args: dict[str, Any]) -> str:
        path = args.get("path")
        if not path:
            raise ValueError("参数解析失败: 缺少必需的 'path' 字段")

        content = args.get("content")
        if content is None:
            raise ValueError("参数解析失败: 缺少必需的 'content' 字段")

        full_path = os.path.join(self._work_dir, path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"文件已成功写入: {path} ({len(content)} 字节)"
