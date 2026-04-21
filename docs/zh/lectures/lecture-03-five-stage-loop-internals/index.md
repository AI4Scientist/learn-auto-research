# 第三讲 — 5阶段循环的内部机制

[English Version →](/en/lectures/lecture-03-five-stage-loop-internals/)

代码示例：[code/](./code/)  
配套项目：[项目二 — 从基准到最优](/zh/projects/project-02-baseline-to-optimal/)

---

每一次 `/autoresearch` 运行都遵循相同的五个阶段。理解每个阶段的内部运作——以及背后的原因——是设计出成功而非停滞的研究会话的关键。

五个阶段依次为：**理解（Understand）→ 形成假设（Hypothesize）→ 实验（Experiment）→ 评估（Evaluate）→ 记录并迭代（Log & Iterate）**。第一阶段要求 agent 在修改任何代码之前，先完整读取 `research.md`、`git log`、上一次实验的 diff 以及所有在作用域内的文件。这里的核心洞见是"**git 即记忆**"——agent 不在会话之间保存状态，git 历史就是它的记忆，每次提交都以 `experiment:` 前缀记录下尝试过的改变。

第二阶段要求 agent 提出一个具体、可证伪的单一假设，包含"改什么、为什么改、预期改进幅度"三个部分。**单一改变原则**是整个框架中最重要的约束：每次迭代只做一个改变，使得成功的原因可追溯，失败时回滚干净。第三阶段在验证之前先 `git commit`——这是有意为之，确保失败的实验也被保存在历史中，回滚只需一条 `git revert`。第四阶段运行评估器并应用保留策略，决定提交是否保留；Guard 在保留后运行，防止引入退化。第五阶段更新 `research.md`、`research_log.md` 和 `autoresearch-results.tsv`，然后立即返回第一阶段——无需人工干预。

## 核心概念

**git 即记忆**：agent 通过读取 `git log` 和 `git diff` 重建研究历史，所有实验提交均以 `experiment:` 前缀标注。

**单一改变原则**：每次迭代只做一个修改，使成功/失败原因完全可归因。

**先提交后验证**：实验变更在运行评估器之前就 `git commit`，确保历史干净且回滚简单。

**保留策略（keep policy）**：决定是否保留当前提交的规则，最常用的是 `score_improvement`（新分数优于前最佳则保留）。

**Guard**：在保留改变后运行的安全检查命令，防止 agent 在优化主指标时破坏其他不变量。

## 关键要点

- 阶段1（理解）是最容易被低估的阶段——读取 git 历史能防止重复尝试已失败的实验
- 单一改变原则让每次迭代的结果都可解释
- 先提交后验证保持 git 历史干净，使回滚变得简单
- Guard 在指标检查之后运行，而非之前——在不阻碍探索的前提下防止退化
- 阶段5触发后立即进入阶段1——循环在迭代之间不需要人工介入
- 五个输出文件（`research.md`、`research_log.md`、`autoresearch-results.tsv`、`progress.png`、`final_report.md`）共同构成完整的研究会话记录

---

**下一讲**：[第四讲 — 被卡住时怎么办](/zh/lectures/lecture-04-what-to-do-when-stuck/)
