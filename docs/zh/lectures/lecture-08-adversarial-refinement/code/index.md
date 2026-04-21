# L08 代码 — 对抗性精炼

> 目标：用辩论追踪器记录作者/批评者/裁判三轮，再用分数聚合器验证盲审是否真的减少了偏差。

运行方式：

```sh
python debate_tracker.py --demo   # 用演示数据记录一轮辩论
python judge_aggregator.py        # 聚合裁判分数，计算一致性
```

---

## 工具一：辩论轮次追踪器

### 第一步：演示数据（一轮完整辩论）

```python
import json, os, sys
from datetime import datetime

HANDOFF_FILE = "handoff.json"

# 演示：一轮真实的技术决策辩论
DEMO_ROUND = {
    "author": (
        "我建议将递归 Fibonacci 实现替换为迭代版本。"
        "基准测试显示 40 倍加速，栈使用降为 O(1)。"
    ),
    "critic": (
        "迭代版本对不熟悉动态规划的读者来说失去了清晰度。"
        "另外，基准测试用的是 n=35；在 n=10 时差距可以忽略不计。"
        "复杂度代价值得吗？"
    ),
    "judge": (
        "作者的性能主张对大 n 有效。批评者的可读性担忧合理。"
        "裁决：接受改变，但添加解释 DP 模式的注释。"
        "评分：author 7/10, critic 6/10。"
    ),
}
```

**关键行**：`DEMO_ROUND` 展示了完整的辩论结构 — author 提案、critic 攻击、judge 裁决加评分。

---

### 第二步：加载和保存 handoff.json

```python
def load_handoff() -> dict:
    if os.path.exists(HANDOFF_FILE):
        with open(HANDOFF_FILE) as f:
            return json.load(f)
    return {"rounds": []}   # 首次运行：空结构

def save_handoff(data: dict) -> None:
    with open(HANDOFF_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```

**关键行**：`{"rounds": []}` — 文件不存在时自动初始化，每次追加不覆盖历史。

---

### 第三步：记录新一轮并写入文件

```python
def main():
    demo = "--demo" in sys.argv
    data = load_handoff()

    # 使用演示数据或交互式输入
    new_round = DEMO_ROUND if demo else prompt_round()

    # 添加元数据
    new_round["timestamp"]    = datetime.utcnow().isoformat() + "Z"
    new_round["round_number"] = len(data["rounds"]) + 1

    data["rounds"].append(new_round)
    save_handoff(data)

    print(f"\n第 {new_round['round_number']} 轮已保存到 {HANDOFF_FILE}")
    print(json.dumps(new_round, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

---

## 工具二：盲判分数聚合器

### 第一步：用正则从裁判文本中提取分数

```python
import re

HANDOFF_FILE = "handoff.json"

# 匹配 "author 7/10" 或 "critic: 6/10" 等格式
SCORE_RE = re.compile(
    r"(author|critic)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*/\s*10",
    re.IGNORECASE
)

def extract_scores(judge_text: str) -> dict:
    scores = {}
    for match in SCORE_RE.finditer(judge_text):
        role  = match.group(1).lower()   # "author" 或 "critic"
        score = float(match.group(2))    # 数字评分
        scores[role] = score
    return scores
```

**关键行**：`re.IGNORECASE` — 匹配 "Author 7/10"、"AUTHOR: 7/10"、"author 7 / 10" 等各种写法。

---

### 第二步：按轮次打印评分表，计算一致性

```python
def main():
    if not os.path.exists(HANDOFF_FILE):
        print(f"[error] 找不到 {HANDOFF_FILE}。请先运行 debate_tracker.py --demo。")
        sys.exit(1)

    with open(HANDOFF_FILE) as f:
        data = json.load(f)

    rounds = data.get("rounds", [])
    if not rounds:
        print("还没有记录任何轮次。")
        return

    all_author, all_critic = [], []

    print(f"{'轮次':<8} {'作者':>8} {'批评者':>8}  裁判摘要")
    print("-" * 75)

    for r in rounds:
        rn     = r.get("round_number", "?")
        judge  = r.get("judge", "")
        scores = extract_scores(judge)
        a = scores.get("author")
        c = scores.get("critic")
        excerpt = judge[:55] + "..." if len(judge) > 55 else judge
        a_str = f"{a:>8.1f}" if a is not None else "       —"
        c_str = f"{c:>8.1f}" if c is not None else "       —"
        print(f"{rn!s:<8} {a_str} {c_str}  {excerpt}")
        if a is not None: all_author.append(a)
        if c is not None: all_critic.append(c)

    # 计算平均分和一致性
    print()
    if all_author:
        avg_a = sum(all_author) / len(all_author)
        avg_c = sum(all_critic) / len(all_critic) if all_critic else float("nan")
        gap   = abs(avg_a - avg_c)
        print(f"作者平均分   : {avg_a:.2f}/10")
        print(f"批评者平均分 : {avg_c:.2f}/10")
        print(f"分歧程度     : {gap:.2f}  "
              f"({'分歧较小' if gap < 1.5 else '分歧较大——建议重新审视'})")
    else:
        print("裁判文本中未找到数字评分。")

if __name__ == "__main__":
    main()
```

**关键行**：`gap < 1.5` — 作者和批评者分数差距小于 1.5 分说明裁判认为双方都有道理；差距大说明有一方明显更有说服力。

---

## 动手改一改

1. 运行 `debate_tracker.py --demo` 三次，再运行 `judge_aggregator.py`，三轮的评分一样吗？
2. 修改 `DEMO_ROUND["judge"]` 里的评分为 "author 9/10, critic 3/10"，`gap` 变成多少？这意味着什么？
3. 把 `SCORE_RE` 里的 `re.IGNORECASE` 去掉，再运行——什么情况下会提取失败？
4. 在你自己的一个技术决策上写出三个角色的内容（author/critic/judge），然后运行工具记录下来。
