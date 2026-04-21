# L10 代码 — 12维场景探索

> 目标：为任意领域计算12个场景维度的优先级得分，找出"最容易遗漏但最重要"的维度，作为下一批场景生成的起点。

运行方式：

```sh
python scenario_priority.py software
python scenario_priority.py security
python scenario_priority.py business
```

---

## 第一步：定义 12 个场景维度和基础分数

```python
import sys

DIMENSIONS = [
    {"id":  1, "name": "正常路径",    "base": 5},
    {"id":  2, "name": "错误条件",    "base": 8},
    {"id":  3, "name": "边界情况",    "base": 7},
    {"id":  4, "name": "滥用情况",    "base": 6},
    {"id":  5, "name": "规模压力",    "base": 6},
    {"id":  6, "name": "并发",        "base": 7},
    {"id":  7, "name": "时间性",      "base": 5},
    {"id":  8, "name": "数据变体",    "base": 6},
    {"id":  9, "name": "权限差异",    "base": 7},
    {"id": 10, "name": "第三方集成",  "base": 6},
    {"id": 11, "name": "恢复场景",    "base": 7},
    {"id": 12, "name": "状态转换",    "base": 6},
]
```

**关键行**：`"base"` 分数反映了每个维度在一般情况下的重要性 — 错误条件（8分）比正常路径（5分）更容易被忽视，所以基础优先级更高。

---

## 第二步：定义领域特定的权重倍数

```python
# 不同领域对不同维度有不同侧重
# 键是维度 ID，值是倍数（越高 = 该领域越重视这个维度）
DOMAIN_WEIGHTS = {
    "software": {2: 1.5, 6: 1.5, 5: 1.3, 11: 1.3},   # 错误、并发、规模、恢复
    "security": {4: 2.0, 9: 1.8, 8: 1.4, 10: 1.3},   # 滥用、权限、数据变体、集成
    "product":  {1: 1.8, 9: 1.4, 7: 1.3},             # 正常路径、权限、时间性
    "business": {5: 1.6, 10: 1.5, 11: 1.4, 12: 1.4},  # 规模、集成、恢复、状态
}
```

**关键行**：`"security": {4: 2.0, ...}` — 安全领域把"滥用情况"的优先级翻倍，因为恶意输入是安全测试的核心，而一般软件测试可能会忽视它。

---

## 第三步：计算加权得分并排序

```python
def compute_scores(domain: str) -> list[dict]:
    weights = DOMAIN_WEIGHTS.get(domain, {})
    scored  = []
    for dim in DIMENSIONS:
        multiplier = weights.get(dim["id"], 1.0)      # 没有权重的维度倍数为 1.0
        score      = round(dim["base"] * multiplier, 1)
        scored.append({**dim, "score": score, "multiplier": multiplier})
    # 按得分从高到低排序
    return sorted(scored, key=lambda d: d["score"], reverse=True)
```

**关键行**：`weights.get(dim["id"], 1.0)` — 未在权重表中指定的维度倍数默认为 1.0，基础分不变。

---

## 第四步：打印排名和建议

```python
def print_ranking(domain: str) -> None:
    ranked = compute_scores(domain)
    print(f"场景维度优先级 — 领域: {domain}")
    print("=" * 60)
    print(f"{'排名':<6} {'得分':<7} {'倍数':<6} 维度名称")
    print("-" * 60)

    for rank, dim in enumerate(ranked, 1):
        mult_str = f"x{dim['multiplier']}" if dim["multiplier"] != 1.0 else "    "
        print(f"{rank:<6} {dim['score']:<7} {mult_str:<6} {dim['name']}")

    print()
    print("建议迭代顺序：从排名 1-3 开始，依次向下。")
    print("每次迭代只覆盖一个维度的一个场景。")
    print()
    top3 = [d["name"] for d in ranked[:3]]
    print(f"'{domain}' 领域的 Top 3: {', '.join(top3)}")

def main():
    domain = sys.argv[1] if len(sys.argv) > 1 else "software"
    valid  = list(DOMAIN_WEIGHTS.keys())
    if domain not in valid:
        print(f"未知领域 '{domain}'。可选: {valid}")
        sys.exit(1)
    print_ranking(domain)

if __name__ == "__main__":
    main()
```

---

## 预期输出（`security` 领域）

```
场景维度优先级 — 领域: security
============================================================
排名   得分    倍数   维度名称
------------------------------------------------------------
1      12.6    x1.8   权限差异
2      12.0    x2.0   滥用情况
3      8.4     x1.4   数据变体
4      7.8     x1.3   第三方集成
5      7.0            并发
...

'security' 领域的 Top 3: 权限差异, 滥用情况, 数据变体
```

---

## 动手改一改

1. 对比 `software` 和 `security` 的 Top 3——哪些维度在两个领域都很重要？哪些只在一个领域突出？
2. 把 `"software"` 里的并发权重从 `1.5` 改成 `3.0`，并发会排到第几位？
3. 添加一个新领域 `"mobile"`，它应该重视哪些维度？写出 `DOMAIN_WEIGHTS["mobile"]`。
4. 选你上一个功能的 Top 1 维度，在那个维度下写出 3 个具体场景。
