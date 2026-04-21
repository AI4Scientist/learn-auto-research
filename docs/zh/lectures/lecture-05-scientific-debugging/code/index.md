# L05 代码 — 科学方法调试

> 目标：用两个小工具模拟假设驱动的调试循环——追踪假设状态，并自动对每个假设执行"证伪测试"。

运行方式：

```sh
# 完整工作流
python hypothesis_tracker.py add "缓存数据库查询可降低延迟"
python hypothesis_tracker.py add "切换到二分搜索可提升吞吐量"
python hypothesis_tracker.py list
python falsification_loop.py
python hypothesis_tracker.py list   # 查看状态更新
```

---

## 工具一：假设追踪器

### 第一步：文件格式和加载

```python
import sys, os, re
from datetime import date

FILE = "hypotheses.md"
VALID_STATUSES = {"active", "confirmed", "eliminated"}

# 表格表头（写入文件时用）
HEADER = "# Hypotheses\n\n| # | Status | Date | Hypothesis |\n|---|--------|------|------------|\n"

def load() -> list[dict]:
    if not os.path.exists(FILE):
        return []
    rows = []
    with open(FILE) as f:
        for line in f:
            # 用正则解析 Markdown 表格的每一行
            m = re.match(r"\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*([\d-]+)\s*\|\s*(.+?)\s*\|", line)
            if m:
                rows.append({"id": int(m.group(1)), "status": m.group(2),
                              "date": m.group(3), "text": m.group(4)})
    return rows
```

**关键行**：`re.match(r"\|\s*(\d+)..."` — 直接解析 Markdown 表格，`hypotheses.md` 既是人类可读的文档，也是机器可解析的数据。

---

### 第二步：三个命令（list / add / update）

```python
def save(rows: list[dict]) -> None:
    with open(FILE, "w") as f:
        f.write(HEADER)
        for r in rows:
            f.write(f"| {r['id']} | {r['status']} | {r['date']} | {r['text']} |\n")

def cmd_list(rows):
    if not rows:
        print("还没有假设。")
        return
    print(f"{'#':<4} {'状态':<12} {'日期':<12} 假设内容")
    print("-" * 70)
    for r in rows:
        print(f"{r['id']:<4} {r['status']:<12} {r['date']:<12} {r['text']}")

def cmd_add(rows, text):
    new_id = max((r["id"] for r in rows), default=0) + 1
    rows.append({"id": new_id, "status": "active",
                 "date": date.today().isoformat(), "text": text})
    save(rows)
    print(f"已添加假设 #{new_id}: {text}")

def cmd_update(rows, hyp_id, new_status):
    if new_status not in VALID_STATUSES:
        print(f"无效状态 '{new_status}'。可选: {VALID_STATUSES}")
        sys.exit(1)
    for r in rows:
        if r["id"] == hyp_id:
            r["status"] = new_status
            save(rows)
            print(f"假设 #{hyp_id} → {new_status}")
            return
    print(f"找不到假设 #{hyp_id}。")
```

**关键行**：`new_id = max(..., default=0) + 1` — 自增 ID，`default=0` 处理列表为空的情况，不会崩溃。

---

### 第三步：命令行入口

```python
def main():
    args = sys.argv[1:]
    rows = load()
    if not args or args[0] == "list":
        cmd_list(rows)
    elif args[0] == "add" and len(args) >= 2:
        cmd_add(rows, " ".join(args[1:]))   # 支持带空格的假设文本
    elif args[0] == "update" and len(args) == 3:
        cmd_update(rows, int(args[1]), args[2])
    else:
        print("用法: hypothesis_tracker.py list | add <文本> | update <id> <状态>")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 工具二：证伪循环运行器

### 第一步：加载所有 active 假设

```python
import subprocess

def load_active() -> list[dict]:
    if not os.path.exists(FILE):
        print(f"[error] 找不到 {FILE}。请先运行 hypothesis_tracker.py add。")
        sys.exit(1)
    rows = []
    with open(FILE) as f:
        for line in f:
            # 只加载状态为 active 的行
            m = re.match(r"\|\s*(\d+)\s*\|\s*active\s*\|\s*([\d-]+)\s*\|\s*(.+?)\s*\|", line)
            if m:
                rows.append({"id": int(m.group(1)), "date": m.group(2), "text": m.group(3)})
    return rows
```

---

### 第二步：测试函数（替换为真实逻辑）

```python
def test_hypothesis(hyp: dict) -> bool:
    """
    返回 True  → 假设已确认（找到证据）。
    返回 False → 假设已排除（没有证据）。
    在真实调试中，这里应该是：运行单一实验，读取结果，判断假设是否成立。
    """
    text = hyp["text"].lower()
    # 演示：含"cache"或"index"的假设在这里倾向于被确认
    return "cache" in text or "index" in text
```

**关键行**：整个函数只做一件事——测试**单一**假设。这是科学调试的核心约束。

---

### 第三步：循环测试并更新状态

```python
def main():
    active = load_active()
    if not active:
        print("没有 active 状态的假设可测试。")
        return

    print(f"测试 {len(active)} 个假设...\n")
    for hyp in active:
        result     = test_hypothesis(hyp)
        new_status = "confirmed" if result else "eliminated"
        verdict    = "已确认" if result else "已排除"
        print(f"  #{hyp['id']} [{verdict}] — {hyp['text']}")

        # 通过追踪器更新状态（保持单一数据源）
        subprocess.run(
            [sys.executable, "hypothesis_tracker.py", "update",
             str(hyp["id"]), new_status],
            check=False,
        )

    print("\n已更新 hypotheses.md。运行 `python hypothesis_tracker.py list` 查看结果。")

if __name__ == "__main__":
    main()
```

**关键行**：`subprocess.run([sys.executable, "hypothesis_tracker.py", "update", ...])` — 通过命令行调用追踪器，保持 `hypotheses.md` 作为唯一数据源。

---

## 动手改一改

1. 添加一个假设："binary search improves throughput"，运行 `falsification_loop.py`，它被确认了吗？为什么？
2. 修改 `test_hypothesis()` 里的判断逻辑，让它测试假设文本里是否含有"排序"，观察结果。
3. 把一个 `eliminated` 假设手动改回 `active`（用 `update` 命令），再运行证伪循环，会发生什么？
4. `eliminated.md` 为什么比 `findings.md` 更有长期价值？用你自己的话解释。
