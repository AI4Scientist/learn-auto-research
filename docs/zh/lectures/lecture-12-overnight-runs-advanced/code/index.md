# L12 代码 — 过夜运行与高级模式

> 目标：用进度监控器读取 TSV 判断循环是否收敛，用目标检查器在 bash 循环里实现"达标自动停止"。

运行方式：

```sh
# 先用 L03 生成结果文件
python ../lecture-03-five-stage-loop-internals/code/loop_simulator.py
# 然后运行这两个工具
python progress_monitor.py autoresearch-results.tsv
python check_target.py research.md autoresearch-results.tsv
```

---

## 工具一：进度监控器

### 第一步：加载 TSV 结果文件

```python
import csv, os, sys, math

def load_tsv(path: str) -> list[dict]:
    if not os.path.exists(path):
        print(f"[error] 找不到文件: {path}")
        sys.exit(1)
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)
    return rows
```

---

### 第二步：计算收敛统计

```python
def compute_stats(rows: list[dict]) -> dict:
    # 提取所有有效分数
    scores = []
    for r in rows:
        try:
            scores.append(float(r["metric"]))
        except (KeyError, ValueError):
            pass   # 跳过无效行，不崩溃

    if not scores:
        return {}

    # 区分保留和回滚的行
    kept     = [r for r in rows if r.get("status", "").strip().lower() == "keep"]
    reverted = len(rows) - len(kept)

    best      = min(scores)   # 最小化指标；若最大化请改为 max()
    keep_rate = len(kept) / len(rows) if rows else 0.0
```

**关键行**：`best = min(scores)` — 假设指标越小越好（如延迟、损失）。如果是准确率等越大越好的指标，改为 `max(scores)`。

---

### 第三步：计算最近 5 次保留的标准差（收敛信号）

```python
    # 只看 keep 状态的分数
    kept_scores = []
    for r in kept:
        try:
            kept_scores.append(float(r["metric"]))
        except (KeyError, ValueError):
            pass

    # 取最近 5 个保留分数的窗口
    window = kept_scores[-5:] if len(kept_scores) >= 5 else kept_scores

    if len(window) >= 2:
        mean_w     = sum(window) / len(window)
        variance   = sum((x - mean_w) ** 2 for x in window) / len(window)
        std_window = math.sqrt(variance)
    else:
        std_window = float("nan")   # 数据不足，无法判断

    return {
        "total": len(rows), "kept": len(kept), "reverted": reverted,
        "keep_rate": keep_rate, "best": best,
        "worst": max(scores), "last": scores[-1], "std_last5": std_window,
    }
```

**关键行**：`kept_scores[-5:]` — 只看最近 5 次**保留**（非回滚）的分数，因为只有保留的迭代才代表真实进步。

---

### 第四步：打印收敛报告

```python
def print_report(stats: dict, path: str) -> None:
    if not stats:
        print("没有找到有效的数值指标数据。")
        return

    print(f"=== 收敛报告: {os.path.basename(path)} ===")
    print(f"  总迭代次数  : {stats['total']}")
    print(f"  保留 / 回滚 : {stats['kept']} / {stats['reverted']}"
          f"  (保留率: {stats['keep_rate']:.0%})")
    print(f"  最佳分数    : {stats['best']:.4f}")
    print(f"  最差分数    : {stats['worst']:.4f}")
    print(f"  最新分数    : {stats['last']:.4f}")
    print()

    std = stats["std_last5"]
    if math.isnan(std):
        print("  收敛状态    : 数据不足（保留迭代 < 2 次）")
    elif std < 0.005:
        print(f"  收敛状态    : 已收敛  (最近5次保留的标准差 = {std:.4f})")
    elif std < 0.02:
        print(f"  收敛状态    : 趋于稳定 (std = {std:.4f})")
    else:
        print(f"  收敛状态    : 仍在改进 (std = {std:.4f})")

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "autoresearch-results.tsv"
    rows = load_tsv(path)
    stats = compute_stats(rows)
    print_report(stats, path)

if __name__ == "__main__":
    main()
```

---

## 工具二：目标检查器

### 第一步：从 `research.md` 解析目标值和方向

```python
import re

def parse_target(md_path: str) -> tuple[float, str]:
    """
    从 research.md 中提取目标。
    支持格式：Target: < 0.05  或  Target: > 0.90
    返回 (目标值, 方向)，方向为 'min' 或 'max'。
    """
    if not os.path.exists(md_path):
        print(f"[error] 找不到 {md_path}。")
        sys.exit(1)

    with open(md_path) as f:
        content = f.read()

    # 匹配 < 0.05 或 >= 0.90 等格式
    m = re.search(r"[Tt]arget\s*[:=]\s*([<>]=?)\s*([\d.]+)", content)
    if not m:
        print("[error] 无法从 research.md 中解析 Target。")
        print("期望格式: Target: < 0.05  或  Target: > 0.90")
        sys.exit(1)

    op        = m.group(1)              # "<", "<=", ">", ">="
    value     = float(m.group(2))
    direction = "min" if "<" in op else "max"
    return value, direction
```

**关键行**：`direction = "min" if "<" in op else "max"` — `<` 表示"越小越好"（最小化），`>` 表示"越大越好"（最大化）。

---

### 第二步：从 TSV 提取最佳已保留分数

```python
def best_score(tsv_path: str, direction: str) -> float | None:
    if not os.path.exists(tsv_path):
        return None
    scores = []
    with open(tsv_path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row.get("status", "").strip().lower() == "keep":  # 只看保留的
                try:
                    scores.append(float(row["metric"]))
                except (KeyError, ValueError):
                    pass
    if not scores:
        return None
    return min(scores) if direction == "min" else max(scores)
```

---

### 第三步：判断目标是否达成并返回退出码

```python
def main():
    md_path  = sys.argv[1] if len(sys.argv) > 1 else "research.md"
    tsv_path = sys.argv[2] if len(sys.argv) > 2 else "autoresearch-results.tsv"

    target, direction = parse_target(md_path)
    best = best_score(tsv_path, direction)

    if best is None:
        print(f"[check_target] 还没有保留的分数。目标: {direction} {target}")
        sys.exit(1)

    met    = (best <= target) if direction == "min" else (best >= target)
    symbol = "<=" if direction == "min" else ">="
    status = "已达成" if met else "未达成"

    print(f"[check_target] best={best:.4f}  目标 {symbol} {target}  → {status}")
    sys.exit(0 if met else 1)   # 退出码 0 = 已达成，供 bash 循环判断

if __name__ == "__main__":
    main()
```

**关键行**：`sys.exit(0 if met else 1)` — 退出码是给 bash 循环用的信号：`if python check_target.py research.md; then break; fi`。

---

## 在 bash 循环中使用 check_target.py

```bash
for i in $(seq 1 100); do
    claude -p "/autoresearch Iterations: 1"
    if python check_target.py research.md; then
        echo "第 $i 轮达到目标，停止"
        break
    fi
done
```

---

## 动手改一改

1. 用 L03 的模拟器生成 TSV 后运行 `progress_monitor.py`，收敛状态是什么？`std_last5` 是多少？
2. 把 `std < 0.005` 改成 `std < 0.05`（更宽松的收敛标准），同样的数据会变成"已收敛"吗？
3. 在 `research.md` 里把 `Target: 0.90` 改成 `Target: > 0.95`，重新运行 `check_target.py`，结果变了吗？
4. 如果你的指标是网络延迟（天然高噪声），`std_last5` 会很大，这对"收敛"判断意味着什么？你会怎么处理？
