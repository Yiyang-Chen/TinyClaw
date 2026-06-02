import logging
import os

from dotenv import load_dotenv

from tinyclaw.engine import AgentEngine
from tinyclaw.provider.openai_provider import OpenAIProvider
from tinyclaw.schema import ToolCall, ToolDefinition, ToolResult
from tinyclaw.tools.base import Registry

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


# ==========================================
# 伪造的工具注册表 (用于测试 Provider 的工具提取能力)
# ==========================================
class MockRegistry(Registry):
    def get_available_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="get_weather",
                description="获取指定城市的当前天气情况。",
                input_schema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                    },
                    "required": ["city"],
                },
            ),
        ]

    def execute(self, call: ToolCall) -> ToolResult:
        log.info("  -> [Mock 工具执行] 获取 %s 的天气中...", call.name)
        return ToolResult(
            tool_call_id=call.id,
            output="API 返回：今天是晴天，气温 25 度。",
            is_error=False,
        )


# ==========================================
# 组装运行
# ==========================================
def main():
    if not os.environ.get("ZHIPU_API_KEY"):
        raise SystemExit("请先设置 ZHIPU_API_KEY 环境变量")

    work_dir = os.getcwd()

    # 1. 初始化真实的 Provider 大脑 (指向智谱 GLM-4.5)
    #    可切换 ClaudeProvider.zhipu(...) 或 OpenAIProvider.zhipu(...)，效果一致
    pvd = OpenAIProvider.zhipu("glm-4.5-air")

    # 2. 注入伪造的工具注册表
    reg = MockRegistry()

    # 3. 实例化并运行引擎，开启慢思考阶段
    eng = AgentEngine(pvd, reg, work_dir, enable_thinking=True)

    eng.run("我想去北京跑步，帮我查查天气适合吗？")


if __name__ == "__main__":
    main()
