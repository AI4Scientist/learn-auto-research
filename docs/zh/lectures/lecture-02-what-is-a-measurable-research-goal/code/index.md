# L02 代码 — 什么是可测量的研究目标

> 目标：生成一个合法的 `research.md`，并亲手运行一次评估器，看清 `{"pass": bool, "score": float}` 契约的全貌。

运行方式：

```sh
python gen_research_md.py    # 交互式生成 research.md
python evaluate.py           # 运行评估器，查看契约输出
```

---

## 工具一：`research.md` 生成器

### 第一步：定义模板结构

```python
from datetime import date

TEMPLATE = """\
# Research Goal

**Date**: {date}

## Goal
{goal}

## Metric
{metric}

## Target
{target}

## Baseline
{baseline}

## Notes
{notes}
"""
```

**关键行**：`{target}` 字段 — 这是 `check_target.py` 解析的字段，格式必须是 `< 0.5` 或 `> 0.90`。

---

### 第二步：交互式收集输入并写文件

```python
import sys, os

def prompt(label: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    raw = input(f"{label}{hint}: ").strip()
    return raw if raw else default   # 直接回车使用默认值

def main():
    print("=== research.md 生成器 ===")
    goal     = prompt("你想改进什么？",       "将排序中位数时间缩短 20%")
    metric   = prompt("如何测量？",           "median_ms（10k 元素列表）")
    target   = prompt("什么值算成功？",        "≤ 8.0 ms")
    baseline = prompt("当前基准值？",          "10.0 ms")
    notes    = prompt("约束条件或备注？",       "仅用标准库")

    content = TEMPLATE.format(
        date=date.today().isoformat(),
        goal=goal, metric=metric,
        target=target, baseline=baseline, notes=notes,
    )

    out_path = os.path.join(os.getcwd(), "research.md")
    with open(out_path, "w") as f:
        f.write(content)
    print(f"\n已写入 {out_path}")
    print(content)

if __name__ == "__main__":
    main()
```

**关键行**：`return raw if raw else default` — 直接回车就用括号里的示例值，方便快速生成示例文件。

---

## 工具二：评估器模板

评估器是 autoresearch 循环的核心接口。每次迭代，循环都会调用评估器，读取其输出来决定"保留还是回滚"。

### 第一步：配置目标和方向

```python
import json, sys, random

TARGET_SCORE     = 8.0    # 目标值：分数需达到这个数
HIGHER_IS_BETTER = False  # False = 越小越好（延迟）；True = 越大越好（准确率）
```

---

### 第二步：实现测量函数

```python
def measure() -> float:
    """用你的实际测量逻辑替换这里。必须返回一个浮点数。"""
    # 演示：用随机噪声模拟延迟测量
    random.seed(42)
    samples = [random.gauss(9.5, 1.0) for _ in range(100)]
    return sorted(samples)[len(samples) // 2]   # 返回中位数
```

**关键行**：`sorted(samples)[len(samples) // 2]` — 取中位数而不是平均数，对异常值更稳健。

---

### 第三步：输出契约格式

```python
def evaluate() -> dict:
    score = measure()
    passed = (score >= TARGET_SCORE) if HIGHER_IS_BETTER else (score <= TARGET_SCORE)
    return {"pass": passed, "score": round(score, 4)}

if __name__ == "__main__":
    result = evaluate()
    print(json.dumps(result))          # 循环读取这一行
    sys.exit(0 if result["pass"] else 1)  # 退出码也很重要
```

**关键行**：`sys.exit(0 if result["pass"] else 1)` — 退出码是循环判断"是否达到目标"的第二个信号，和 JSON 输出一起使用。

---

## 预期输出

```sh
$ python evaluate.py
{"pass": false, "score": 9.4762}
$ echo $?
1
```

`pass: false` + 退出码 `1` = 还没达到目标，循环继续。

---

## 动手改一改

1. 把 `TARGET_SCORE = 8.0` 改成 `TARGET_SCORE = 10.0`，输出变成 `pass: true` 了吗？退出码变了吗？
2. 把 `HIGHER_IS_BETTER = False` 改成 `True`，同样的分数，`pass` 会变成什么？
3. 把 `measure()` 里的 `random.gauss(9.5, 1.0)` 改成 `random.gauss(7.0, 0.1)`（更低的延迟），现在能通过了吗？
4. 用 `gen_research_md.py` 为你自己的项目生成一个真实的 `research.md`，不用示例值。
