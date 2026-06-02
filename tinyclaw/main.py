import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


def main():
    log.info("Welcome to TinyClaw Engine startup sequence")

    # TODO: 1. 初始化模型 Provider (大脑)
    # pvd = ClaudeProvider(...)

    # TODO: 2. 初始化 Tool Registry (手脚)
    # registry = ToolRegistry()
    # registry.register(BashTool())

    # TODO: 3. 初始化上下文管理器 (内存管理器)
    # ctx_manager = ContextManager(...)

    # TODO: 4. 组装并启动核心 Engine (操作系统心脏)
    # engine = AgentEngine(pvd, registry, ctx_manager)

    # log.info("开始执行任务...")
    # engine.run("帮我检查一下当前目录下的文件并输出一个 README.md 大纲")

    log.info("架构蓝图搭建完毕，等待各核心模块注入！")


if __name__ == "__main__":
    main()
