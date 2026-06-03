# Chapter 08: 并发工具执行

## 本章目标

将 AgentEngine 的工具执行从串行改为并发，当模型在单个 Turn 中下发多个 tool_call 时并行执行，显著降低延迟。

## 修改文件

- `tinyclaw/engine/loop.py` — 引入 `ThreadPoolExecutor` + 预分配 list 实现并发执行
- `tinyclaw/main.py` — prompt 改为多文件读取场景，促使模型一次性下发多个 read_file

## 核心实现

### 预分配 + 索引写入（无锁并发安全）

```python
results: list[ToolResult | None] = [None] * n

with ThreadPoolExecutor(max_workers=n) as pool:
    futures = [pool.submit(self._execute_single, i, tc) for i, tc in enumerate(tool_calls)]
    for fut in as_completed(futures):
        idx, res = fut.result()
        results[idx] = res
```

每个线程只写自己的索引位置，不需要锁。结果按原始顺序追加到 context_history，保证模型阅读上下文的一致性。

### `_execute_single` 方法

从 `run()` 内联逻辑中抽出为独立方法，接收 `(index, tool_call)` 返回 `(index, result)`，供线程池调度。

## 关键设计决策

- 使用 `ThreadPoolExecutor` 而非 `asyncio`：工具执行涉及文件 I/O 和子进程（bash），线程池更自然
- `max_workers=n`：与本轮 tool_call 数量一致，全部并行
- `as_completed` 而非 `map`：任意完成顺序收集，最终按索引回填保序

## Known Issues

- 当前对所有 tool_calls 无差别并行，缺少 `isConcurrencySafe` 声明式分批逻辑（详见 open_issues.md）

## Git Commits

- 待提交
