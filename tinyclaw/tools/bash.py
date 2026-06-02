import subprocess
from typing import Any

from tinyclaw.schema import ToolDefinition
from tinyclaw.tools.base import BaseTool

TIMEOUT_SECONDS = 30
MAX_OUTPUT_LEN = 8000


class BashTool(BaseTool):
    """在工作区目录下执行任意 bash 命令的工具。

    这是 YOLO 哲学的核心原语：将大模型生成的命令原封不动地交给底层 OS 执行。
    使用 subprocess 模块，以 work_dir 作为 cwd 约束执行环境。
    """

    def __init__(self, work_dir: str) -> None:
        self._work_dir = work_dir

    def name(self) -> str:
        return "bash"

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name(),
            description=(
                "在当前工作区执行任意的 bash 命令。支持链式命令(如 &&)。"
                "返回标准输出(stdout)和标准错误(stderr)。"
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "要执行的 bash 命令，例如: ls -la 或 go test ./...",
                    },
                },
                "required": ["command"],
            },
        )

    def execute(self, args: dict[str, Any]) -> str:
        command = args.get("command")
        if not command:
            raise ValueError("参数解析失败: 缺少必需的 'command' 字段")

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self._work_dir,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return f"Error: 命令执行超时（{TIMEOUT_SECONDS}s 限制）: {command}"

        output_parts: list[str] = []

        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")

        if not output_parts:
            output_parts.append("(命令已执行，无输出)")

        output_parts.append(f"EXIT_CODE: {result.returncode}")

        combined = "\n".join(output_parts)

        if len(combined) > MAX_OUTPUT_LEN:
            return (
                f"{combined[:MAX_OUTPUT_LEN]}\n\n"
                f"...[由于输出过长，已被系统截断至前 {MAX_OUTPUT_LEN} 字符]..."
            )

        return combined
