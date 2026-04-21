# L04 代码 — 被卡住时怎么办

> 目标：读取一份 TSV 结果文件，判断当前是否已触发 L1/L2/L3 转向阈值，并输出具体建议。

运行方式：

```sh
# 先用 L03 的模拟器生成结果文件，再运行检测器
python ../lecture-03-five-stage-loop-internals/code/loop_simulator.py
python pivot_detector.py autoresearch-results.tsv
```

---

## 第一步：定义三个转向阈值

```python
import csv, sys, os

# 三个级别的转向阈值（连续 revert 次数）
L1_THRESHOLD = 3   # 策略切换：换个方向，别换方法
L2_THRESHOLD = 5   # 范式转移：质疑根本假设
L3_THRESHOLD = 10  # 根本性反思：重新审视研究目标本身

PIVOT_ADVICE = {
    1: "L1 转向：在当前范式内切换策略——换一种算法变体或参数方向。",
    2: "L2 转向：更换思路——尝试完全不同的算法族或架构。",
    3: "L3 转向：根本性反思——重新审视研究目标本身是否正确。",
}
```

**关键行**：`L1_THRESHOLD = 3` — 3 次连续失败是信号，不是坏运气。框架主动识别这个信号。

---

## 第二步：加载 TSV 文件

```python
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

## 第三步：统计连续 revert 次数（从末尾往前数）

```python
def analyse(rows: list[dict]) -> None:
    if not rows:
        print("TSV 中没有数据。")
        return

    # 从最后一行向前数，遇到非 revert 就停
    streak = 0
    for row in reversed(rows):
        if row.get("status", "").strip().lower() == "revert":
            streak += 1
        else:
            break   # 只统计末尾连续的 revert，中间的不算
```

**关键行**：`for row in reversed(rows)` — 只统计**末尾**连续的 revert 次数，中间某轮成功了就重置计数。

---

## 第四步：计算统计摘要并输出转向建议

```python
    total     = len(rows)
    kept      = sum(1 for r in rows if r.get("status","").strip().lower() == "keep")
    keep_rate = kept / total if total else 0.0

    scores = []
    for r in rows:
        try:
            scores.append(float(r["metric"]))
        except (KeyError, ValueError):
            pass

    best  = max(scores) if scores else float("nan")
    worst = min(scores) if scores else float("nan")

    print("=== 转向分析 ===")
    print(f"总迭代次数     : {total}")
    print(f"保留 / 回滚   : {kept} / {total - kept}  (保留率 {keep_rate:.0%})")
    print(f"历史最佳分数   : {best:.4f}")
    print(f"末尾连续回滚   : {streak} 次")
    print()

    # 判断转向级别
    if streak >= L3_THRESHOLD:
        level = 3
    elif streak >= L2_THRESHOLD:
        level = 2
    elif streak >= L1_THRESHOLD:
        level = 1
    else:
        level = 0

    if level == 0:
        print(f"[ok] 暂不需要转向（streak={streak}，L1 阈值={L1_THRESHOLD}）。")
    else:
        print(f"[!] {PIVOT_ADVICE[level]}")
        print(f"    末尾 {streak} 次连续回滚超过了"
              f" {'L3' if level==3 else 'L2' if level==2 else 'L1'} 阈值。")

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "autoresearch-results.tsv"
    rows = load_tsv(path)
    analyse(rows)

if __name__ == "__main__":
    main()
```

---

## 预期输出（触发 L2 的示例）

```
=== 转向分析 ===
总迭代次数     : 18
保留 / 回滚   : 6 / 12  (保留率 33%)
历史最佳分数   : 0.7310
末尾连续回滚   : 6 次

[!] L2 转向：更换思路——尝试完全不同的算法族或架构。
    末尾 6 次连续回滚超过了 L2 阈值。
```

---

## 动手改一改

1. 把 `L1_THRESHOLD = 3` 改成 `1`，用 L03 生成的 TSV 跑一遍，第一个转向在第几轮触发？
2. 在 TSV 里手动添加一行 `status=keep`（在末尾的 revert 之后），再运行，`streak` 是否归零？
3. 如果 `scores` 列表为空（TSV 里没有 `metric` 列），程序会崩溃吗？`float("nan")` 的作用是什么？
4. 为你自己的研究场景写出 L1 和 L2 转向的具体内容：L1 会换什么？L2 会质疑什么假设？
