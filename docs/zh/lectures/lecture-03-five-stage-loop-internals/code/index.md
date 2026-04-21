# L03 代码 — 五阶段循环内部机制

> 目标：不依赖任何外部工具，用纯 Python 模拟完整的五阶段 autoresearch 循环，观察每个阶段如何衔接。

运行方式：

```sh
python loop_simulator.py
```

---

## 第一步：配置和初始化

```python
import csv, os, random, math
from datetime import datetime

RESEARCH_MD  = "research.md"
RESULTS_TSV  = "autoresearch-results.tsv"
MAX_ITERATIONS = 10
TARGET_SCORE   = 0.90   # 越高越好（模拟准确率）
RANDOM_SEED    = 7

random.seed(RANDOM_SEED)
```

**关键行**：`TARGET_SCORE = 0.90` — 这是循环提前停止的条件，对应 `research.md` 里的 `Target` 字段。

---

## 第二步：阶段 0 — 若 `research.md` 不存在则初始化

```python
if not os.path.exists(RESEARCH_MD):
    with open(RESEARCH_MD, "w") as f:
        f.write("# Research Goal\n\n## Target\n0.90\n\n## Metric\naccuracy\n")
    print(f"[bootstrap] 已写入 {RESEARCH_MD}")

def read_target(path: str) -> float:
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                try:
                    return float(line)
                except ValueError:
                    continue
    return TARGET_SCORE

target = read_target(RESEARCH_MD)
```

**关键行**：`read_target()` — 阶段 1（理解）的核心：每次迭代开始前先读目标，确保循环始终与 `research.md` 保持同步。

---

## 第三步：虚拟评估器（替代真实的 `evaluate.py`）

```python
best_score = 0.50

def fake_evaluate(iteration: int) -> float:
    """模拟带噪声的迭代改进——分数缓慢向 1.0 爬升。"""
    ideal = 0.50 + 0.05 * math.log1p(iteration)  # 对数增长
    noise = random.gauss(0, 0.02)                 # 加一点随机噪声
    return min(max(ideal + noise, 0.0), 1.0)
```

**关键行**：`math.log1p(iteration)` — 对数增长模拟真实研究的收益递减：早期进步快，后期越来越难。

---

## 第四步：初始化 TSV 结果文件

```python
tsv_exists = os.path.exists(RESULTS_TSV)
tsv_file   = open(RESULTS_TSV, "a", newline="")
writer     = csv.writer(tsv_file, delimiter="\t")

if not tsv_exists:
    writer.writerow(["iteration", "commit", "metric", "delta", "status", "description"])
```

**关键行**：`"a"` 模式（追加）— 重复运行不会覆盖之前的数据，这与真实循环一致：历史永远保留。

---

## 第五步：主循环 — 五个阶段

```python
prev_score = best_score

for i in range(1, MAX_ITERATIONS + 1):
    # 阶段 1: 理解 — 目标已在循环外加载（read_target）

    # 阶段 2: 生成 — 真实循环中 Claude 提出代码变更
    description = f"auto-change-{i:03d}"

    # 阶段 3: 评估
    score = fake_evaluate(i)
    delta = score - prev_score

    # 阶段 4: 保留 / 回滚
    if score >= prev_score:
        status = "keep"
        prev_score = score
        if score > best_score:
            best_score = score
    else:
        status = "revert"   # 分数变差：概念上回到 prev_score

    # 阶段 5: 记录
    fake_commit = f"abc{i:04d}"
    writer.writerow([i, fake_commit, round(score, 4), round(delta, 4), status, description])
    tsv_file.flush()

    print(f"{i:<6} {score:<8.4f} {delta:+8.4f} {status:<8} {description}")

    # 提前停止：达到目标
    if best_score >= target:
        print(f"\n[完成] 第 {i} 轮达到目标 {target}（best={best_score:.4f}）")
        break
else:
    print(f"\n[完成] 预算耗尽。best={best_score:.4f}  target={target}")

tsv_file.close()
```

**关键行**：`status = "revert"` 但 `prev_score` 不更新 — 这正是真实循环的行为：坏的实验被撤销，下次从上一个最佳状态继续。

---

## 五个阶段与真实循环的对应关系

| 阶段 | 模拟器中的代码 | 真实循环中发生的事 |
|------|--------------|-----------------|
| 阶段1 读取 | `read_target()` | 解析 `research.md`、`git log`、上次 diff |
| 阶段2 生成 | `description = f"..."` | Claude 提出并应用代码变更 |
| 阶段3 评估 | `fake_evaluate(i)` | 运行 `evaluate.py`，解析 JSON 输出 |
| 阶段4 保留/回滚 | `if score >= prev_score` | `git commit` 保留 或 `git revert` 撤销 |
| 阶段5 记录 | `writer.writerow(...)` | 更新 `.tsv`、`research.md`、`research_log.md` |

---

## 动手改一改

1. 把 `TARGET_SCORE = 0.90` 改成 `TARGET_SCORE = 0.60`，循环在第几轮停下来？
2. 把 `noise = random.gauss(0, 0.02)` 改成 `noise = random.gauss(0, 0.15)`（高噪声），`revert` 的比例变高了吗？
3. 把阶段4改成"只要新分数 > 0.7 就保留"（无论是否比上次好），循环行为有什么变化？这有什么问题？
4. 查看生成的 `autoresearch-results.tsv`，找到 delta 最大的一行，那一轮发生了什么？
