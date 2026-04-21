# 第三讲 — 5阶段循环的内部机制

`L01 > L02 > [ L03 ] L04 > L05 > L06 | L07 > L08 > L09 > L10 > L11 > L12`

> *"git 是 agent 的记忆。"* — 它不需要记住过去，它只需要读 `git log`。
>
> **本讲核心**：逐阶段拆解每次 `/autoresearch` 迭代发生的事，以及每个设计决策背后的原因。

代码示例：[code/](./code/)  
配套项目：[项目二 — 从基准到最优](/zh/projects/project-02-baseline-to-optimal/)

---

## 问题

当你运行 `/autoresearch` 时，agent 在做什么？如果你不了解内部机制，遇到问题时就无从诊断——不知道为什么循环停滞，不知道为什么某次迭代没被保留，不知道如何调整参数来改变行为。

## 解决方案

每次迭代都是同一个五阶段序列：

```
阶段1: 理解       阶段2: 假设       阶段3: 实验
research.md  -->  提出一个具体 --> git commit
git log           可证伪的改变      (先提交)
上次 diff                              |
                                       v
阶段5: 记录 <----- 阶段4: 评估
更新 .tsv          运行 evaluate.py
更新 .md           分数更好? → 保留
立即进阶段1        分数变差? → revert
```

五个阶段，没有人工干预，立即循环。

## 工作原理

**阶段 1 — 理解（Understand）**

```python
# agent 在修改任何代码之前，先读取：
# - research.md（目标、约束、历史）
# - git log（哪些实验已经尝试过）
# - 上次实验的 diff（上次改了什么）
# - 所有作用域内的文件（当前代码状态）
```

关键洞见：**git 即记忆**。agent 没有跨会话的状态，但 git 历史有。每次提交以 `experiment:` 前缀记录尝试过的改变。

**阶段 2 — 形成假设（Hypothesize）**

```
✓ 好的假设（具体、可证伪）：
  "将 QuickSort 的 pivot 从固定第一元素改为随机元素，
   预期对已排序输入的 median_time_s 降低约 40%"

✗ 坏的假设（模糊、不可证伪）：
  "尝试优化排序算法"
```

**单一改变原则**：每次迭代只做一个改变。这是整个框架最重要的约束——成功的原因可追溯，失败时回滚干净。

**阶段 3 — 实验（Experiment）**

```bash
# 注意顺序：先提交，后验证
git add -A
git commit -m "experiment: 随机 pivot 替换固定 pivot"
# 然后才运行 evaluate.py
```

为什么先提交？确保失败的实验也被保存在历史中。回滚只需一条 `git revert`。

**阶段 4 — 评估（Evaluate）**

```python
# 运行评估器，应用保留策略
new_score = run_evaluator()   # python evaluate.py
if new_score < best_score:    # score_improvement 策略
    keep()                    # 提交留在历史
    run_guard()               # Guard 在保留后运行
else:
    revert()                  # git revert HEAD
```

Guard 在保留**之后**运行，不是之前——不阻碍探索，但防止退化。

**阶段 5 — 记录并迭代（Log & Iterate）**

```
更新 research.md        → 追加新的历史行
更新 autoresearch-results.tsv → 记录 iteration/metric/delta/status
更新 research_log.md    → 人类可读的实验日志
→ 立即返回阶段 1（无需人工干预）
```

## 变更内容

| 组件 | 手动研究 | autoresearch 循环 |
|------|----------|------------------|
| 记忆 | 研究员的大脑 | `git log` + `research.md` |
| 假设 | 随意 | 单一、具体、可证伪 |
| 提交时机 | 验证后 | **验证前**（先提交）|
| 回滚 | 手动、常被跳过 | 自动、可靠 |
| 循环间隔 | 人的注意力 | 零间隔，立即迭代 |

## 试一试

运行循环模拟器，观察五个阶段实际发生的事：

```sh
cd docs/zh/lectures/lecture-03-five-stage-loop-internals/code
python loop_simulator.py
```

观察输出并思考：

1. 哪个阶段消耗了最多"时间"（模拟步骤）？为什么阶段1看起来最重要？
2. 找到一次被 revert 的迭代。它的 `delta` 是多少？Guard 有没有触发？
3. 把 `MAX_SCORE = 0.99` 改成 `MAX_SCORE = 0.85`，循环在第几轮停下来？
4. 在输出的 TSV 数据里，`status=keep` 和 `status=revert` 的比例大约是多少？

---

**下一讲**：[第四讲 — 被卡住时怎么办](/zh/lectures/lecture-04-what-to-do-when-stuck/)
