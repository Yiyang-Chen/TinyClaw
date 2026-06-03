import logging
import os

from dotenv import load_dotenv

from tinyclaw.engine import AgentEngine
from tinyclaw.provider.openai_provider import OpenAIProvider
from tinyclaw.tools import BashTool, EditFileTool, ReadFileTool, ToolRegistry, WriteFileTool

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
    registry.register(EditFileTool(work_dir))

    # 5. 实例化核心引擎，开启慢思考促使模型一次性统筹规划
    eng = AgentEngine(pvd, registry, work_dir, enable_thinking=True)

    # 6. 下发一个需要收集多源信息的任务
    eng.run(
        "我当前目录下有 a.txt, b.txt, c.txt 三个文件。\n"
        "为了节省时间，请你同时一次性读取这三个文件，"
        "并将它们的内容综合起来，告诉我它们分别记录了什么领域的信息。"
    )


if __name__ == "__main__":
    main()
