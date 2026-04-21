# Learn AutoResearch

> 设定目标 → Agent 运行循环 → 你醒来看结果

**Learn AutoResearch** 是一门基于项目的课程，教你用 autoresearch 框架实现研究自动化——它是 Karpathy 自主 ML 训练循环的泛化版本，适用于任何有可测量指标的领域。

[English →](README_EN.md) | [在线文档 →](https://zhimin-z.github.io/learn-auto-research/)

---

## 你将学到什么

- **定义可测量的研究目标** — 把模糊的目标转化为 agent 能自动优化的机械指标
- **运行自主改进循环** — 每次迭代只做一个改变，自动回滚，git 作为实验记忆
- **科学调试** — 可证伪的假设，基于证据的调查，错误归零自动停止
- **行动前预判** — 5 位专家视角在提交任何重大改变前进行分析
- **自主安全审计** — STRIDE + OWASP + 红队分析，带代码级证据
- **自信地发布** — 覆盖代码、内容、部署的 8 阶段发布流水线

## 课程结构

| 阶段 | 主题 | 讲义 | 项目 |
|------|------|------|------|
| 1 理解原理 | 为什么手动迭代失败，可测量目标 | L01–L02 | P01 排序优化 |
| 2 核心循环 | 五阶段循环内部机制，遇到瓶颈的策略 | L03–L04 | P02 函数拟合 |
| 3 调试修复 | 科学调试，错误瀑布解决 | L05–L06 | P03 FastAPI 调试 |
| 4 多视角预测 | 5 专家预判，对抗性精化 | L07–L08 | P04 架构辩论 |
| 5 安全场景 | STRIDE/OWASP 安全审计，12 维场景探索 | L09–L10 | P05 安全审计 |
| 6 发布高级 | 通用发布流水线，过夜运行 | L11–L12 | P06 端到端流水线 |

## 快速开始

```bash
# 安装依赖
npm install

# 启动本地预览
npm run dev

# 构建静态站点
npm run build
```

## 技术栈

- [VitePress](https://vitepress.dev/) 1.6+ 静态站点生成
- [vitepress-plugin-mermaid](https://github.com/emersonbottero/vitepress-plugin-mermaid) 流程图渲染
- 双语：英文（默认）+ 中文（/zh/）
- 项目示例代码：Python（仅标准库）

## 致谢

本课程的核心循环理念来源于 [Andrej Karpathy 的 autoresearch](https://github.com/karpathy/autoresearch)。

## 许可证

MIT
