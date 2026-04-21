# 第十二讲 — 过夜运行与高级模式

[English Version →](/en/lectures/lecture-12-overnight-runs-advanced/)

代码示例：[code/](./code/)  
配套项目：[项目六 — 端到端研究项目](/zh/projects/project-06-end-to-end-research/)

---

autoresearch 的真正威力在于你睡觉时发生的事情。本讲涵盖无人值守过夜运行、CI/CD 流水线集成、循环中使用 MCP 服务器，以及为新领域构建自定义评估器。

**过夜运行**推荐使用 tmux：在 tmux 会话中启动循环后分离，随时可以重新连接查看进度。备选方案是 `nohup` 后台运行并将输出重定向到日志文件。每次迭代后 `progress.png` 自动更新，直接用图像查看器打开即可看到收敛曲线，无需阅读日志。**MCP 服务器集成**极大地扩展了评估器的能力：在 `research.md` 的 Evaluator 字段中指定使用 MCP postgres 工具执行 `EXPLAIN ANALYZE`，或调用 MCP openai 工具对提示词质量打分，或用 MCP grafana 工具检查错误率作为 Guard。任何配置在 Claude Code 中的 MCP 服务器在循环中都可直接使用，使任何外部系统都能成为指标来源。**CI/CD 集成**通过 GitHub Actions 定时任务（例如每晚2点）自动运行研究循环、安全审计，并将进度提交回仓库，让研究成为持续性过程而非一次性事件。

**自定义评估器**遵循简单契约：运行测量 → 输出 `{"pass": bool, "score": float}` → 以退出码0退出。任何能产生数字的程序都可以成为评估器。研究完成后，可通过 `/autoresearch:learn --mode init` 将 `research.md` 和 `final_report.md` 转化为可复用的技能文档，将成功研究所积累的知识编码为未来可调用的能力。

## 核心概念

**tmux 过夜运行**：在持久化的 tmux 会话中运行循环，支持断开连接后重新附加查看进度，是长时间无人值守运行的推荐方式。

**`progress.png` 收敛可视化**：每次迭代后自动更新的指标vs迭代次数收敛图，提供循环运行状态的直觉性确认。

**MCP 服务器作为指标来源**：在 `research.md` 的 Evaluator 或 Guard 字段中使用 MCP 工具，使数据库查询时间、LLM 评分、监控指标等任何外部系统测量值都能成为优化目标。

**自定义评估器契约**：输出 `{"pass": bool, "score": float}` 并以退出码0退出的任何程序，都可作为评估器接入循环。

**研究→技能流水线**：`research.md → final_report.md → SKILL.md`，将成功研究会话的知识编码为可复用技能，通过 `/autoresearch:learn` 自动化完成。

## 关键要点

- tmux 是最佳过夜运行工具——支持重新连接且能在断开后存活
- `progress.png` 提供循环正常运行的可视化确认，无需阅读日志
- MCP 服务器扩展了评估器可测量的范围——任何外部系统都可成为指标来源
- CI/CD 集成使研究成为持续过程，而非一次性事件
- 自定义评估器遵循简单契约：运行测量，输出 `{"pass": bool, "score": float}`
- 研究→技能流水线将成功研究编码为可复用知识

---

**课程完成。** 你现在掌握了完整的 autoresearch 工具集。从[项目六](/zh/projects/project-06-end-to-end-research/)开始，构建一个端到端的完整流水线。
