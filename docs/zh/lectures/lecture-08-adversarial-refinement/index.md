# 第八讲 — 对抗性精炼

`L01 > L02 > L03 > L04 > L05 > L06 | L07 > [ L08 ] L09 > L10 > L11 > L12`

> *"没有指标时，盲审裁判团就是指标。"* — 主观决策也可以有适应度函数。
>
> **本讲核心**：`/autoresearch:reason` 如何通过作者-批评者-裁判循环，把主观决策变成可迭代、可收敛的优化过程。

代码示例：[code/](./code/)  
配套项目：[项目四 — 架构决策辩论](/zh/projects/project-04-architecture-debate/)

---

## 问题

autoresearch 循环在有机械指标时运行良好。但架构选择、产品策略、内容质量、设计权衡呢？这些本质上是主观的——没有 `val_bpb`，没有 `median_time_s`。

主观决策通常靠"感觉"或"权威"来定拍。两者都不可靠，也都无法迭代。

## 解决方案

```
生成候选 A
     |
     v
批评者攻击 A              ← 冷启动，未看过生成过程
（尽可能猛烈）
     |
     v
作者 B 回应              ← 冷启动，只看 A 和批评
（生成改进候选 B）
     |
     v
合成 C = A 最强 + B 最强
     |
     v
盲审裁判团
（N 个裁判，不知道哪个是"新"的）
     |
  C 获胜？→ C 成为新的 A → 重复
  A 获胜？→ A 保留 → 重复
     |
连续 N 次获胜 → 收敛 → handoff.json
```

## 工作原理

**为什么必须冷启动？**

```
# 相关性偏差：agent 为了与之前说的保持一致，
# 会改变评估——即使内容本身没有变化。

# 解决方案：每个 agent 是全新调用，不看历史。
# 批评者只看候选 A，不知道它怎么生成的。
# 裁判只看 X 和 Y，不知道哪个是"新提案"。
```

**为什么盲审有效？**

```
有色眼镜评审（知道哪个是新提案）：
  → 锚定偏差：新的不一定更好，但感觉应该更好
  → 损失厌恶：放弃旧方案感觉是损失
  → 社会压力：作者在场时不好意思说"旧的更好"

盲审（只看内容）：
  → 纯内容胜出，没有元信息干扰
```

**收敛条件**

```markdown
# research.md 中配置
- Convergence: 3   # 候选连续3轮获胜则停止

# 输出：handoff.json
{
  "winning_position": "...",
  "judge_consensus": 0.8,
  "supporting_evidence": [...],
  "recommended_next": "plan"
}
```

**常用链式模式**

```bash
# 方案一：收敛后实证验证
/autoresearch:reason → /autoresearch:plan → /autoresearch

# 方案二：收敛后压力测试
/autoresearch:reason → /autoresearch:predict

# 方案三：完整决策到实施
/autoresearch:reason → /autoresearch:plan → /autoresearch → /autoresearch:ship
```

## 变更内容

| 方式 | 主观决策 | 对抗性精炼 |
|------|---------|-----------|
| 适应度函数 | "感觉好" | 盲审裁判团多数判断 |
| 迭代 | 无，一次拍板 | 作者-批评者-合成循环 |
| 偏差防护 | 无 | 冷启动 + 盲审 |
| 收敛信号 | 无，无限争论 | 连续 N 次获胜 |
| 产出 | 口头结论 | `handoff.json`，可链接下游命令 |

## 试一试

运行辩论追踪器和盲判分数聚合器：

```sh
cd docs/zh/lectures/lecture-08-adversarial-refinement/code
python debate_tracker.py --demo
python judge_aggregator.py
```

思考题：

1. 在 `judge_aggregator.py` 的输出里，作者分数和批评者分数谁更高？为什么批评者可能更难得到高分？
2. 如果批评者和作者都是同一个 agent 实例（共享历史），结果会有什么不同？
3. 在架构决策场景中，"候选 A"是什么？"批评者的攻击"可能是什么？
4. 你最近做的一个主观决策——如果用三轮对抗性精炼，第一轮批评者会攻击什么？

---

**下一讲**：[第九讲 — STRIDE+OWASP自动安全审计](/zh/lectures/lecture-09-stride-owasp-security/)
