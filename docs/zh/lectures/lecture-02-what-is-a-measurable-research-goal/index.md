# 第二讲 — 什么是可测量的研究目标

[English Version →](/en/lectures/lecture-02-what-is-a-measurable-research-goal/)

代码示例：[code/](./code/)  
配套项目：[项目一 — 你的第一个研究循环](/zh/projects/project-01-first-research-loop/)

---

autoresearch 最难的部分不是运行循环，而是正确定义目标。

大多数研究目标用自然语言表述："让 API 更快"、"提高模型准确率"、"减小包体积"。这些是意图，不是指标。agent 无法优化意图——它只能优化一个数字。

`/autoresearch:plan` 向导的存在正是为了把意图转化为机械指标。理解*为什么*这很重要，以及什么让指标好或坏，是每次成功 autoresearch 运行的基础。

## 指标陷阱

坏的指标比没有指标更糟。它给 agent 一个清晰的方向——朝向错误的目的地。

考虑"提高模型准确率"。agent 通过过拟合提高训练集准确率。技术上成功，实际上无用。

或"减少响应时间"。agent 删除错误处理来跳过计算。确实更快，也确实坏了。

## 核心概念

**机械指标**：由确定性程序计算的数字。例如：`pytest --cov` 的 `coverage_pct`、`timeit` 的 `median_time_s`。

**方向**：高还是低更好。始终显式声明——绝不留作隐含。`median_time_s: minimize`，`accuracy: maximize`。

**目标值（Target）**：循环停止的值。`< 0.5`、`> 0.95`、`== 0`。没有目标则用 `max_iterations` 来限制运行。

**Guard**：无论主指标如何，改变被保留前必须通过的次要命令。用于防止退化。例如：`Guard: python -m pytest test_sort.py` 确保每次速度优化后排序函数仍产生正确输出。

**噪声运行（noise_runs）**：当指标有噪声时，多次测量取中位数。设置 `noise_runs: 3` 让评估器运行 3 次。

## research.md 契约

`research.md` 是研究会话的唯一事实来源：

```markdown
# Research: [目标标题]

## Goal
[目标的自然语言描述]

## Success Metric
- Metric: [指标名称]
- Target: [< 0.5 | > 0.95 | == 0]
- Direction: [minimize | maximize]

## Constraints
- Max iterations: 20
- Evaluator: python evaluate.py
- Keep policy: score_improvement
- Guard: [必须始终通过的命令]
- Noise runs: 3
- Min delta: 0

## History
| # | Change | Metric | Result | Timestamp |
|---|--------|--------|--------|-----------|
| 0 | Baseline ([描述]) | [值] | -- | [日期] |
```

## 指标速查表

| 领域 | 指标 | 方向 | 评估器片段 |
|------|------|------|----------|
| 代码性能 | `median_time_s` | minimize | `timeit` 3次取中位数 |
| ML准确率 | `accuracy` | maximize | `sklearn.metrics.accuracy_score` |
| 包体积 | `bundle_kb` | minimize | `du -sk dist/ \| cut -f1` |
| 提示词质量 | `llm_judge_score` | maximize | LLM评分1–10，平均5次 |
| 文献覆盖 | `papers_found` | maximize | 计数匹配论文 |
| API延迟 | `p95_ms` | minimize | 100次请求的第95百分位 |
| 测试覆盖 | `coverage_pct` | maximize | `coverage run -m pytest` |
| RMSE | `rmse` | minimize | `sqrt(mean_squared_error)` |

## 关键要点

- 目标不是指标——把每个意图转化为单一可测量数字
- 好的指标可从代码计算、单调有意义、与未改变部分隔离
- `research.md` 文件是 agent 的记忆——它在每次迭代开始时读取
- Guard 字段防止 agent "作弊"——通过破坏其他东西来改善指标
- `/autoresearch:plan` 向导在约2分钟内将自然语言目标转化为完整的 `research.md`

---

**下一讲**：[第三讲 — 5阶段循环的内部机制](/zh/lectures/lecture-03-five-stage-loop-internals/)
