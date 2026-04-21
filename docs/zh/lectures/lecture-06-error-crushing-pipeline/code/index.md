# L06 代码 — 错误归零流水线

> 目标：用拓扑排序把错误按"谁阻塞谁"的依赖关系排序，再用回归检查器验证修复没有引入新退化。

运行方式：

```sh
python error_sorter.py
python regression_checker.py
```

---

## 工具一：级联感知错误排序器

### 第一步：定义错误和依赖关系

```python
from collections import defaultdict, deque

# 格式：(错误ID, 描述, [此错误依赖的其他错误ID列表])
# 含义：如果 E02 依赖 E01，说明 E01 必须先修复才能解除 E02 的阻塞
ERRORS = [
    ("E01", "ImportError: module 'mylib' not found",           []),
    ("E02", "AttributeError: NoneType has no attribute 'run'", ["E01"]),
    ("E03", "TypeError: unsupported operand type in calc()",   ["E01"]),
    ("E04", "AssertionError in test_output_shape",             ["E02", "E03"]),
    ("E05", "FileNotFoundError: config.yaml missing",          []),
    ("E06", "KeyError: 'learning_rate' in config loader",      ["E05"]),
]
```

**关键行**：`["E01"]` — E02 依赖 E01，意思是"修好 E01 才能看清 E02 是否真的是问题"。先修根因，再看症状。

---

### 第二步：拓扑排序（Kahn 算法）

```python
def topological_sort(errors: list) -> list:
    """按依赖顺序排列错误：被依赖者（阻塞者）优先。"""
    # 构建有向图：dep → eid（dep 必须在 eid 之前修复）
    graph     = defaultdict(list)   # dep_id → [依赖它的 error_id]
    in_degree = defaultdict(int)    # 每个错误有多少个未解决的依赖
    nodes     = {e[0] for e in errors}

    for eid, _desc, deps in errors:
        in_degree[eid]   # 确保 key 存在，即使入度为 0
        for dep in deps:
            if dep in nodes:
                graph[dep].append(eid)   # dep 解决后，eid 的入度 -1
                in_degree[eid] += 1
```

**关键行**：`in_degree[eid]` — 入度表示"还有多少个阻塞我的错误没解决"，入度为 0 的错误可以立即修复。

---

### 第三步：BFS 输出修复顺序

```python
    # 所有入度为 0 的错误可以立即处理
    queue  = deque(eid for eid in nodes if in_degree[eid] == 0)
    order  = []
    lookup = {e[0]: e for e in errors}

    while queue:
        current = queue.popleft()
        order.append(lookup[current])
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1        # 当前错误修好了，邻居的依赖减少
            if in_degree[neighbor] == 0:    # 所有阻塞都解除了
                queue.append(neighbor)      # 可以处理了

    if len(order) != len(errors):
        raise ValueError("错误依赖图中存在循环！")
    return order

def main():
    sorted_errors = topological_sort(ERRORS)
    print(f"{'优先级':<8} {'ID':<6} {'依赖':<20} 描述")
    print("-" * 75)
    for priority, (eid, desc, deps) in enumerate(sorted_errors, 1):
        dep_str = ", ".join(deps) if deps else "—"
        print(f"{priority:<8} {eid:<6} {dep_str:<20} {desc}")
    print("\n从上到下依次修复。修好阻塞者，后续错误可能自动消失。")

if __name__ == "__main__":
    main()
```

---

## 工具二：回归检查器

### 第一步：定义基准和候选结果

```python
TOLERANCE = 0.01   # 允许最多 1% 劣化；超过则标记为 REGRESSION

# 修复前的基准测量
BASELINE = {
    "throughput_rps": 1200.0,
    "p50_latency_ms":    8.3,
    "p99_latency_ms":   45.1,
    "error_rate":        0.002,
    "accuracy":          0.913,
}

# 修复后的新测量
CANDIDATE = {
    "throughput_rps": 1185.0,   # 轻微下降
    "p50_latency_ms":    8.1,   # 改进
    "p99_latency_ms":   52.4,   # 退化！
    "error_rate":        0.002,
    "accuracy":          0.911, # 轻微下降
}

# 越小越好的指标（上升 = 退化）
LOWER_IS_BETTER = {"p50_latency_ms", "p99_latency_ms", "error_rate"}
```

**关键行**：`LOWER_IS_BETTER` 集合 — 不同指标方向不同，必须分类处理，否则"延迟上升"会被误判为"改进"。

---

### 第二步：逐指标比对并分类

```python
def check(baseline: dict, candidate: dict) -> None:
    regressions, improvements, neutral = [], [], []

    for key in sorted(set(baseline) | set(candidate)):
        b = baseline.get(key)
        c = candidate.get(key)
        if b is None or c is None:
            neutral.append((key, b, c, "—", "缺失"))
            continue

        change   = (c - b) / abs(b) if b != 0 else 0.0
        regressed = (change > TOLERANCE) if key in LOWER_IS_BETTER else (change < -TOLERANCE)
        improved  = not regressed and abs(change) > TOLERANCE

        tag = "REGRESSION" if regressed else ("improvement" if improved else "ok")
        row = (key, b, c, f"{change:+.2%}", tag)
        (regressions if regressed else (improvements if improved else neutral)).append(row)

    print(f"{'指标':<25} {'基准':>12} {'候选':>12} {'变化':>10}  状态")
    print("-" * 75)
    for group in (regressions, improvements, neutral):
        for key, b, c, chg, tag in group:
            marker = "  <-- !" if tag == "REGRESSION" else ""
            print(f"{key:<25} {str(b):>12} {str(c):>12} {chg:>10}  {tag}{marker}")

    print()
    if regressions:
        print(f"[FAIL] 发现 {len(regressions)} 个退化。不要发布。")
    else:
        print("[PASS] 没有超出容差的退化。")

if __name__ == "__main__":
    check(BASELINE, CANDIDATE)
```

**关键行**：`(regressions if regressed else (improvements if improved else neutral)).append(row)` — 三路分类，输出时先打印退化（红色警告），再打印改进，最后打印中性。

---

## 动手改一改

1. 运行 `error_sorter.py`，确认 E01 和 E05 排在最前面。如果删掉 E01（假设已修复），E02 和 E03 的优先级会怎么变？
2. 在 `ERRORS` 里添加一个新错误 `("E07", "测试超时", ["E04"])`，它会排在第几位？
3. 把 `TOLERANCE = 0.01` 改成 `0.05`（更宽松的容差），`p99_latency_ms` 的退化还会被报告吗？
4. 在 `CANDIDATE` 里把 `p99_latency_ms` 改回 `45.0`（不再退化），重新运行，输出变成 PASS 了吗？
