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

    # 5. 实例化核心引擎
    eng = AgentEngine(pvd, registry, work_dir, enable_thinking=False)

    # 6. 发起一个需要局部修改的指令
    eng.run(
        "我当前目录下有一个 server.go 文件。\n"
        '请帮我把里面 "TODO: 增加鉴权逻辑" 下面的那个 if 语句，整个替换为：\n'
        "    if user == nil {\n"
        '        fmt.Println("Forbidden!")\n'
        "        return\n"
        "    }"
    )


if __name__ == "__main__":
    main()
