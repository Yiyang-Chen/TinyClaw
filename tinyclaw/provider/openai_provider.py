import json
import logging
import os

from openai import OpenAI

from tinyclaw.provider.base import LLMProvider
from tinyclaw.schema import Message, Role, ToolCall, ToolDefinition

log = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """基于 OpenAI SDK 的适配器，可通过 base_url 兼容智谱等 OpenAI 协议服务。"""

    def __init__(self, model: str, api_key: str, base_url: str | None = None):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    @classmethod
    def zhipu(cls, model: str) -> "OpenAIProvider":
        """工厂方法：基于 OpenAI SDK，指向智谱底座。"""
        api_key = os.environ["ZHIPU_API_KEY"]
        base_url = "https://open.bigmodel.cn/api/paas/v4/"
        return cls(model=model, api_key=api_key, base_url=base_url)

    def generate(
        self,
        messages: list[Message],
        available_tools: list[ToolDefinition] | None,
    ) -> Message:
        openai_msgs: list[dict] = []

        # 1. 翻译上下文消息
        for msg in messages:
            if msg.role == Role.SYSTEM:
                openai_msgs.append({"role": "system", "content": msg.content})

            elif msg.role == Role.USER:
                if msg.tool_call_id:
                    openai_msgs.append({
                        "role": "tool",
                        "content": msg.content,
                        "tool_call_id": msg.tool_call_id,
                    })
                else:
                    openai_msgs.append({"role": "user", "content": msg.content})

            elif msg.role == Role.ASSISTANT:
                ast_msg: dict = {"role": "assistant"}
                if msg.content:
                    ast_msg["content"] = msg.content

                if msg.tool_calls:
                    ast_msg["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.name,
                                "arguments": json.dumps(tc.arguments, ensure_ascii=False),
                            },
                        }
                        for tc in msg.tool_calls
                    ]

                openai_msgs.append(ast_msg)

        # 2. 翻译工具定义
        openai_tools = None
        if available_tools:
            openai_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": td.name,
                        "description": td.description,
                        "parameters": td.input_schema,
                    },
                }
                for td in available_tools
            ]

        # 3. 构建请求并发送
        kwargs: dict = {
            "model": self.model,
            "messages": openai_msgs,
        }
        if openai_tools:
            kwargs["tools"] = openai_tools

        resp = self.client.chat.completions.create(**kwargs)

        if not resp.choices:
            raise RuntimeError("API 返回了空的 Choices")

        # 4. 将 API Response 反向翻译为内部 Message
        choice = resp.choices[0].message

        result = Message(
            role=Role.ASSISTANT,
            content=choice.content or "",
        )

        if choice.tool_calls:
            for tc in choice.tool_calls:
                if tc.type == "function":
                    result.tool_calls.append(
                        ToolCall(
                            id=tc.id,
                            name=tc.function.name,
                            arguments=json.loads(tc.function.arguments),
                        )
                    )

        return result
