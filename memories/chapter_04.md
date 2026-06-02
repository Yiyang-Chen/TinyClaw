# Chapter 04: 代码实战：实现双协议 Provider 适配器

Course: "从 0 开始构建 Agent Harness" - 04｜代码实战：实现双协议 Provider 适配器

## What We Have

### 1. OpenAI 协议适配器 (`tinyclaw/provider/openai_provider.py`)

`OpenAIProvider(LLMProvider)` 基于 `openai` Python SDK，将内部 `Message` 双向翻译为 OpenAI Chat Completions 格式。核心翻译点：

- 内部 `Role.USER` + `tool_call_id` → OpenAI `role: "tool"` 消息
- `ToolCall.arguments` (`dict`) → `json.dumps()` 发送，`json.loads()` 接收
- `available_tools` 为 `None` 时不挂载 `tools` 字段（支撑慢思考）
- `@classmethod zhipu(model)` 工厂方法封装智谱 `base_url` 配置

### 2. Anthropic 协议适配器 (`tinyclaw/provider/claude_provider.py`)

`ClaudeProvider(LLMProvider)` 基于 `anthropic` Python SDK，翻译为 Anthropic Messages 格式。与 OpenAI 的关键差异：

- System prompt 抽离到 `system` 参数，不放在 messages 数组
- Tool result 是 `user` 消息内的 `tool_result` content block（而非独立 role）
- Assistant 回复以 content blocks 形式返回（`text` / `tool_use`）
- `ToolCall.arguments` (`dict`) 直接传递，无需 JSON 序列化

### 3. main.py 接入真实 Provider

- `MockProvider` 已移除，替换为 `OpenAIProvider.zhipu("glm-4.5-air")`
- `MockRegistry` 升级为 `get_weather` 工具（带完整 `input_schema`）
- 使用 `python-dotenv` + `.env` 文件管理 API key
- 已通过 `py -m tinyclaw` 验证真实 API 调用成功

### 4. 新增依赖

- `anthropic` — Anthropic 官方 Python SDK
- `python-dotenv` — 从 `.env` 加载环境变量

## Key Decisions

- Tool result role 问题已解决：采用 **Provider 层转换**方案，内部 schema 保持 `Role.USER` + `tool_call_id` 不变，各 Provider 自行映射为各自 API 格式
- 构造函数设计：类本身接受通用参数 `(model, api_key, base_url)`，`@classmethod zhipu()` 封装智谱特定配置（对应 Go 的 `NewZhipuXxxProvider` 构造函数）

## Git Commits

- (pending)
