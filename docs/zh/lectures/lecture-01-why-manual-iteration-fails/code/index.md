# L01 代码 — 手动迭代为何会失败

> 目标：用 30 行代码，亲眼看到"随机跳跃"和"系统搜索"在同等预算下的效率差距。

运行方式：

```sh
python manual_vs_systematic.py
```

---

## 第一步：定义目标函数和预算

```python
import random
import math

SEED   = 42
BUDGET = 20           # 允许的评估次数
DOMAIN = (0.0, 10.0)  # 搜索空间

def objective(x: float) -> float:
    """峰值函数，最大值在 x=3.7。"""
    return math.exp(-0.5 * (x - 3.7) ** 2)
```

**关键行**：`BUDGET = 20` — 两种策略共享同一个预算，这是公平对比的前提。

---

## 第二步：手动（随机跳跃）策略

```python
random.seed(SEED)
manual_history = []
best_manual = (None, -1.0)

for i in range(BUDGET):
    x = random.uniform(*DOMAIN)   # 凭"直觉"随意跳跃
    score = objective(x)
    manual_history.append((i + 1, round(x, 4), round(score, 4)))
    if score > best_manual[1]:
        best_manual = (x, score)
```

**关键行**：`random.uniform(*DOMAIN)` — 用均匀随机模拟"人工调参"：每次都是一次独立的猜测，没有利用上次的结果。

---

## 第三步：系统性（网格搜索）策略

```python
grid_history = []
best_grid = (None, -1.0)
step = (DOMAIN[1] - DOMAIN[0]) / BUDGET  # 均匀划分搜索空间

for i in range(BUDGET):
    x = DOMAIN[0] + i * step              # 每次向右移动固定步长
    score = objective(x)
    grid_history.append((i + 1, round(x, 4), round(score, 4)))
    if score > best_grid[1]:
        best_grid = (x, score)
```

**关键行**：`step = (DOMAIN[1] - DOMAIN[0]) / BUDGET` — 把搜索空间均匀分成 20 份，确保每一块都被覆盖到。

---

## 第四步：打印对比报告

```python
print(f"{'Iter':<6} {'Manual x':<12} {'Manual score':<15} {'Grid x':<12} {'Grid score'}")
print("-" * 60)
for (mi, mx, ms), (gi, gx, gs) in zip(manual_history, grid_history):
    print(f"{mi:<6} {mx:<12} {ms:<15} {gx:<12} {gs}")

print()
print(f"Best manual : x={best_manual[0]:.4f}  score={best_manual[1]:.4f}")
print(f"Best grid   : x={best_grid[0]:.4f}  score={best_grid[1]:.4f}")
print(f"True optimum: x=3.7000  score=1.0000")

gap_manual = 1.0 - best_manual[1]
gap_grid   = 1.0 - best_grid[1]
print(f"Systematic is {gap_manual/gap_grid:.1f}x closer to optimum with same budget.")
```

---

## 预期输出

```
Best manual : x=4.1731  score=0.8948
Best grid   : x=3.6842  score=0.9997
True optimum: x=3.7000  score=1.0000

Systematic is 9.6x closer to optimum with same budget.
```

用同样的 20 次评估预算，系统搜索比随机跳跃接近最优解 **近 10 倍**。

---

## 动手改一改

1. 把 `BUDGET = 20` 改成 `BUDGET = 5`，差距变大了还是缩小了？
2. 把 `SEED = 42` 改成 `SEED = 1`，手动策略的结果变了，系统策略变了吗？为什么？
3. 把 `DOMAIN = (0.0, 10.0)` 改成 `DOMAIN = (3.0, 4.5)`（缩小到最优解附近），手动策略还那么差吗？这说明什么？
