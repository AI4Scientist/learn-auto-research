# 第二讲 — 什么是可测量的研究目标

`L01 > [ L02 ] L03 > L04 > L05 > L06 | L07 > L08 > L09 > L10 > L11 > L12`

> *"意图不是指标。"* — agent 只能优化一个数字，不能优化一个愿望。
>
> **本讲核心**：把自然语言目标转化为 agent 可以优化的机械指标，以及 `research.md` 契约的完整结构。

代码示例：[code/](./code/)  
配套项目：[项目一 — 你的第一个研究循环](/zh/projects/project-01-first-research-loop/)

---

## 问题

大多数研究目标用自然语言表述："让 API 更快"、"提高模型准确率"、"减小包体积"。这些是意图，不是指标。

坏的指标比没有指标更糟——它给 agent 一个清晰的方向，朝向错误的目的地：

- "提高准确率" → agent 过拟合训练集。技术上成功，实际上无用。
- "减少响应时间" → agent 删除错误处理来跳过计算。确实更快，也确实坏了。

## 解决方案

```
自然语言目标
     |
     v
+----+----+
| 问三个  |
| 问题：  |
| 1.能用  |  →  Metric: median_time_s
| Python  |  →  Direction: minimize
| 算吗？  |  →  Target: < 0.5
| 2.方向？|
| 3.目标值|
+----+----+
     |
     v
  research.md  ← agent 每次迭代读取的唯一事实来源
```

`/autoresearch:plan` 向导在约两分钟内完成这个转化。

## 工作原理

**1. 判断指标是否合格。**

好的指标满足三个条件：

```python
# ✓ 可从代码计算
score = timeit.timeit(lambda: sort(data), number=100) / 100

# ✓ 单调有意义（越低/越高始终更好）
direction = "minimize"   # 不会"低了又不行"

# ✓ 与未改变部分隔离
# 指标只测排序速度，不测数据加载时间
```

**2. 写出 `research.md`。**

```markdown
# Research: 加速排序函数

## Goal
将 sort_items() 的中位数执行时间降低到 0.5 秒以下。

## Success Metric
- Metric: median_time_s
- Target: < 0.5
- Direction: minimize

## Constraints
- Max iterations: 20
- Evaluator: python evaluate.py
- Keep policy: score_improvement
- Guard: python -m pytest test_sort.py
- Noise runs: 3
- Min delta: 0
```

**3. 理解每个字段的作用。**

```
Guard   → 防止 agent "作弊"——优化速度时不能破坏正确性
Noise runs → 测量 3 次取中位数，消除计时抖动
Min delta  → 只有真实进步（>0）才算改进，防止噪声触发保留
Target  → 达到后循环自动停止
```

## 指标速查表

| 领域 | 指标 | 方向 | 评估器核心代码 |
|------|------|------|--------------|
| 代码性能 | `median_time_s` | minimize | `timeit` 取中位数 |
| ML 准确率 | `accuracy` | maximize | `accuracy_score` |
| 包体积 | `bundle_kb` | minimize | `du -sk dist/` |
| 提示词质量 | `llm_judge_score` | maximize | LLM 评 1–10，平均5次 |
| API 延迟 | `p95_ms` | minimize | 100 次请求的 P95 |
| 测试覆盖 | `coverage_pct` | maximize | `coverage run -m pytest` |

## 试一试

生成一个完整的 `research.md`，并亲手跑一次评估器：

```sh
cd docs/zh/lectures/lecture-02-what-is-a-measurable-research-goal/code
python gen_research_md.py       # 生成示例 research.md
python evaluate.py              # 查看评估器输出格式
```

思考题：

1. 运行 `evaluate.py` 后，输出的 `score` 是什么？`pass` 字段什么时候为 `true`？
2. 如果去掉 `Guard` 字段会发生什么？agent 可能会怎么"作弊"？
3. 把 `noise_runs` 从 1 改成 5，再跑 `evaluate.py` — 分数有变化吗？为什么？
4. 为你自己的项目写一个 `research.md`，只需要填 Goal、Metric、Direction、Target 四个字段。

---

**下一讲**：[第三讲 — 5阶段循环的内部机制](/zh/lectures/lecture-03-five-stage-loop-internals/)
