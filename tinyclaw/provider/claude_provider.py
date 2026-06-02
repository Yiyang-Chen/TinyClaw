import json
import logging
import os

from anthropic import Anthropic

from tinyclaw.provider.base import LLMProvider
from tinyclaw.schema import Message, Role, ToolCall, ToolDefinition

log = logging.getLogger(__name__)


class ClaudeProvider(LLMProvider):
    """基于 Anthropic SDK 的适配器，可通过 base_url 兼容智谱等兼容服务。"""

    def __init__(self, model: str, api_key: str, base_url: str | None = None):
        self.model = model
        self.client = Anthropic(api_key=api_key, base_url=base_url)

    @classmethod
    def zhipu(cls, model: str) -> "ClaudeProvider":
        """工厂方法：基于 Anthropic SDK，指向智谱底座。"""
        api_key = os.environ["ZHIPU_API_KEY"]
        base_url = "https://open.bigmodel.cn/api/paas/v4/"
        return cls(model=model, api_key=api_key, base_url=base_url)

    def generate(
        self,
        messages: list[Message],
        available_tools: list[ToolDefinition] | None,
    ) -> Message:
        anthropic_msgs: list[dict] = []
        system_prompt = ""

        # 1. 消息翻译
        for msg in messages:
            if msg.role == Role.SYSTEM:
                system_prompt = msg.content

            elif msg.role == Role.USER:
                if msg.tool_call_id:
                    anthropic_msgs.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": msg.tool_call_id,
                                "content": msg.content,
                            }
                        ],
                    })
                else:
                    anthropic_msgs.append({
                        "role": "user",
                        "content": [{"type": "text", "text": msg.content}],
                    })

            elif msg.role == Role.ASSISTANT:
                blocks: list[dict] = []
                if msg.content:
                    blocks.append({"type": "text", "text": msg.content})

                for tc in msg.tool_calls:
                    blocks.append({
                        "type": "tool_use",
                        "id": tc.id,
                        "name": tc.name,
                        "input": tc.arguments,
                    })

                if blocks:
                    anthropic_msgs.append({"role": "assistant", "content": blocks})

        # 2. 工具 Schema 翻译
        anthropic_tools = None
        if available_tools:
            anthropic_tools = []
            for td in available_tools:
                input_schema = td.input_schema
                if not input_schema:
                    input_schema = {"type": "object", "properties": {}}

                anthropic_tools.append({
                    "name": td.name,
                    "description": td.description,
                    "input_schema": input_schema,
                })

        # 3. 构建请求并发送
        kwargs: dict = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": anthropic_msgs,
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        if anthropic_tools:
            kwargs["tools"] = anthropic_tools

        resp = self.client.messages.create(**kwargs)

        # 4. 反向解析为内部 Message
        result = Message(role=Role.ASSISTANT)

        for block in resp.content:
            if block.type == "text":
                result.content += block.text
            elif block.type == "tool_use":
                result.tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        arguments=block.input if isinstance(block.input, dict)
                        else json.loads(block.input),
                    )
                )

        return result
