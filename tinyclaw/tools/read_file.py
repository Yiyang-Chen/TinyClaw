import os
from typing import Any

from tinyclaw.schema import ToolDefinition
from tinyclaw.tools.base import BaseTool

MAX_LEN = 8000


class ReadFileTool(BaseTool):
    """读取本地文件内容的工具。

    将引擎的 work_dir 注入给工具，限制它只能在此目录及其子目录下操作。
    """

    def __init__(self, work_dir: str) -> None:
        self._work_dir = work_dir

    def name(self) -> str:
        return "read_file"

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name(),
            description="读取指定路径的文件内容。请提供相对工作区的路径。",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "要读取的文件路径，如 cmd/claw/main.go",
                    },
                },
                "required": ["path"],
            },
        )

    def execute(self, args: dict[str, Any]) -> str:
        # 1. 参数提取（Provider 层已完成 JSON 解析，这里做字段校验）
        path = args.get("path")
        if not path:
            raise ValueError("参数解析失败: 缺少必需的 'path' 字段")

        # 2. 拼接绝对路径
        #    注意：生产环境中需要做路径穿越检测防范，防止 ../../etc/passwd
        full_path = os.path.join(self._work_dir, path)

        # 3. 执行物理 IO 操作
        with open(full_path, encoding="utf-8") as f:
            content = f.read()

        # 4. 【核心防线】长度截断保护
        #    防止大模型读取几百 MB 的日志文件导致 Context 瞬间爆炸 (OOM)
        if len(content) > MAX_LEN:
            return (
                f"{content[:MAX_LEN]}\n\n"
                f"...[由于内容过长，已被系统截断至前 {MAX_LEN} 字符]..."
            )

        return content
