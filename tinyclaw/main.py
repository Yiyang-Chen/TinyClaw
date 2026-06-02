import logging
import os

from dotenv import load_dotenv

from tinyclaw.engine import AgentEngine
from tinyclaw.provider.openai_provider import OpenAIProvider
from tinyclaw.tools import BashTool, ReadFileTool, ToolRegistry, WriteFileTool

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    if not os.environ.get("ZHIPU_API_KEY"):
        raise SystemExit("请先设置 ZHIPU_API_KEY 环境变量")

    # 1. 获取工作区物理边界
    work_dir = os.getcwd()

    # 2. 初始化真实的大脑 (指向智谱 GLM-4.5，使用 OpenAI 适配器)
    pvd = OpenAIProvider.zhipu("glm-4.5-air")

    # 3. 初始化真实的 Tool Registry
    registry = ToolRegistry()

    # 4. 将工具挂载到注册表中
    registry.register(ReadFileTool(work_dir))
    registry.register(WriteFileTool(work_dir))
    registry.register(BashTool(work_dir))

    # 5. 实例化核心引擎
    eng = AgentEngine(pvd, registry, work_dir, enable_thinking=False)

    # 6. 发起一个需要连贯物理动作的任务
    eng.run(
        "请帮我执行以下操作：\n"
        "1. 用 bash 查看一下我当前电脑的 Python 版本。\n"
        "2. 帮我写一个简单的 hello_claw.py 文件，输出 \"Hello, TinyClaw!\"。\n"
        "3. 用 bash 运行这个 py 文件，确认它能正常工作。"
    )


if __name__ == "__main__":
    main()
