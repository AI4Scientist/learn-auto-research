# 项目 06 — 端到端研究项目


**配套讲座**：[第 11 讲](/zh/lectures/lecture-11-universal-ship-pipeline/) + [第 12 讲](/zh/lectures/lecture-12-overnight-runs-advanced/)  
**起始代码**：[projects/project-06/starter/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-06/starter/)  
**参考答案**：[projects/project-06/solution/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-06/solution/)

---

## 你将构建什么

一个完整的端到端自动化研究流水线：选择你自己的优化目标，运行过夜模拟（50 次迭代），调试任何问题，运行安全审计，并发布结果。

## 学习目标

- 从空白开始设计你自己的 `research.md`
- 运行模拟过夜会话（使用 `max_iterations: 50` 进行 50 次迭代）
- 在单一连贯工作流中链接全部 10 个命令
- 编写 `final_report.md` 并用它为下一次研究会话做铺垫

## 你的任务

从以下优化目标中选择一个（或提出你自己的）：

| 选项 | 目标 | 指标 |
|------|------|------|
| A | 优化文本压缩算法 | `compression_ratio`（最大化） |
| B | 提升推荐系统精度 | `precision_at_10`（最大化） |
| C | 减少图遍历算法内存占用 | `peak_mb`（最小化） |
| D | 你自己的领域（需要编写评估器） | 你的选择 |

## 完整流水线

```bash
# 阶段 1：规划
/autoresearch:plan

# 阶段 2：研究（模拟过夜——50 次迭代）
/autoresearch
Iterations: 50

# 阶段 3：调试（如果研究过程中出现问题）
/autoresearch:debug

# 阶段 4：修复
/autoresearch:fix

# 阶段 5：安全审计（如果产物是 API 或服务）
/autoresearch:security

# 阶段 6：发布
/autoresearch:ship --type research
```

## 交付成果

完成本项目后，你应该拥有：

1. `research.md` — 完整实验历史（50 行）
2. `research_log.md` — 关键迭代的详细注释
3. `final_report.md` — 最佳结果及下次会话的建议
4. `autoresearch-results.tsv` — 机器可读结果
5. `progress.png` — 收敛曲线图

## 反思问题

完成流水线后，写一份简短的 `reflection.md` 回答以下问题：
1. 达到目标花了多少次迭代？你需要进行枢轴吗？
2. 研究历史中最令人惊讶的发现是什么？
3. 如果今晚再运行 50 次迭代，你会尝试什么？
4. 在 `research.md` 设置上，你会做什么不同的事？

## 过夜模拟脚本

在不真正等待一夜的情况下模拟真实过夜运行：

```bash
# Run 50 iterations in tmux
tmux new-session -d -s overnight
tmux send-keys -t overnight \
  "claude -p '/autoresearch Iterations: 50'" Enter

# Monitor progress from another terminal
watch -n 60 "tail -5 autoresearch-results.tsv && echo '---' && cat research.md | grep 'Best:'"
```
