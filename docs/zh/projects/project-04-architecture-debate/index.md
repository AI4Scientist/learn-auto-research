# 项目 04 — 架构决策辩论

[English Version →](/en/projects/project-04-architecture-debate/)

**配套讲座**：[第 07 讲](/zh/lectures/lecture-07-five-expert-predict/) + [第 08 讲](/zh/lectures/lecture-08-adversarial-refinement/)  
**起始代码**：[projects/project-04/starter/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-04/starter/)  
**参考答案**：[projects/project-04/solution/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-04/solution/)

---

## 你将构建什么

使用 `/autoresearch:predict` 和 `/autoresearch:reason` 为订单管理系统在两种数据库架构之间做出决策。然后用 `/autoresearch:plan` 将收敛的决策转化为验证实验。

## 学习目标

- 运行五专家预测分析并识别少数意见
- 运行对抗性精炼循环直至收敛
- 阅读 `lineage.md`，了解辩论是如何演进的
- 将 `reason → plan` 链接以实证验证决策

## 决策背景

你的订单管理系统每天处理 10,000 个订单，涉及复杂查询和频繁更新。你需要在以下两者之间选择：

**选项 A — CQRS + 事件溯源**：命令写入事件，查询读取投影。完整审计记录。实现复杂。

**选项 B — 传统 CRUD + 审计日志**：简单读写。写操作时追加审计日志表。实现简单得多。

## 第 1 步 — 五专家分析

```bash
/autoresearch:predict
Scope: projects/project-04/starter/
Task: Choose between CQRS+EventSourcing vs CRUD+AuditLog for order management
```

阅读输出。注意：哪个角色提出了最多顾虑？是否存在一个被其他人忽视的少数观点？

## 第 2 步 — 对抗性精炼

```bash
/autoresearch:reason
Task: Should we use event sourcing for our order management system?
Domain: software
Iterations: 8
Convergence: 3
```

观察辩论的演进。8 次迭代后（或更早达到收敛时），阅读 `lineage.md`，逐轮查看立场如何演变。

## 第 3 步 — 规划验证实验

```bash
/autoresearch:plan
Goal: Validate the winning architecture with a performance benchmark
```

将第 2 步的收敛决策作为输入。规划向导将帮助你定义一个指标，实证验证哪种架构在你的特定负载模式下表现更好。

## 预期输出

```
reason/{date}-order-management/
├── lineage.md           ← 逐轮演进记录
├── candidates.md        ← 所有候选立场
├── judge-transcripts.md ← 每位评判者的发言
├── reason-results.tsv   ← 机器可读结果
└── handoff.json         ← 用于链接的结构化输出
```

## 需要回答的关键问题

完成辩论后：对抗性过程是否改变了你的初始直觉？`lineage.md` 中哪个论点是最决定性的转折点？
