import logging
import os

from dotenv import load_dotenv

from tinyclaw.engine import AgentEngine
from tinyclaw.provider.openai_provider import OpenAIProvider
from tinyclaw.tools import ReadFileTool, ToolRegistry

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

    # 4. 将真实的 ReadFile 工具挂载到注册表中
    registry.register(ReadFileTool(work_dir))

    # 5. 实例化核心引擎，任务简单关闭思考阶段以加快速度
    eng = AgentEngine(pvd, registry, work_dir, enable_thinking=False)

    # 6. 下发一个必须通过真实工具才能完成的任务
    eng.run("请调用工具读取一下当前工作区目录下 hello.txt 文件的内容，并用一句话向我总结它说了什么。")


if __name__ == "__main__":
    main()
