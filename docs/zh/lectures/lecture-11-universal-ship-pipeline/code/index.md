# L11 代码 — 通用发布流水线

> 目标：运行机械可验证的发布前检查清单，观察"可验证的通过/失败"和"主观判断"的差别；再用回滚触发脚本验证每次发布都有可追溯的撤销路径。

运行方式：

```sh
python ship_checklist.py code-pr
python ship_checklist.py content
python rollback_trigger.py
```

---

## 工具一：发布前检查清单运行器

### 第一步：按发布类型定义检查命令

```python
import subprocess, sys, os
from datetime import datetime

# 每项检查 = (描述标签, 要运行的命令)
# 通过标准：命令退出码 == 0
CHECKLISTS = {
    "code-pr": [
        ("运行测试套件",
         ["python", "-m", "pytest", "--tb=short", "-q"]),
        ("检查语法错误",
         ["python", "-m", "py_compile"] +
         [f for f in os.listdir(".") if f.endswith(".py")]),
    ],
    "deployment": [
        ("运行测试套件",
         ["python", "-m", "pytest", "--tb=short", "-q"]),
        ("验证 evaluate.py 契约",
         ["python", "-c",
          "import json,subprocess,sys; "
          "r=subprocess.run([sys.executable,'evaluate.py'],capture_output=True); "
          "d=json.loads(r.stdout); "
          "assert 'pass' in d and 'score' in d, '契约格式错误'"]),
    ],
    "content": [
        ("验证 Markdown 文件存在",
         ["python", "-c",
          "import os; mds=[f for f in os.listdir('.') if f.endswith('.md')]; "
          "assert mds, '没有找到 .md 文件'"]),
    ],
}

LOG_FILE = "ship-log.md"
```

**关键行**：每项检查都是"运行命令，看退出码" — 没有"看起来没问题"这样的主观判断。

---

### 第二步：逐项运行并记录结果

```python
def run_checklist(ship_type: str) -> bool:
    items = CHECKLISTS.get(ship_type)
    if items is None:
        print(f"[error] 未知的发布类型 '{ship_type}'。")
        print(f"可用类型: {list(CHECKLISTS.keys())}")
        sys.exit(1)

    print(f"发布前检查: {ship_type}")
    print("=" * 50)
    passed, failed, results = 0, 0, []

    for label, cmd in items:
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            ok   = proc.returncode == 0
        except FileNotFoundError:
            ok = False   # 命令不存在
        except subprocess.TimeoutExpired:
            ok = False   # 超时

        status = "PASS" if ok else "FAIL"
        marker = "[✓]" if ok else "[✗]"
        print(f"  {marker} {label:<40} {status}")
        results.append((label, status))
        passed += ok
        failed += not ok
```

**关键行**：`proc.returncode == 0` — 唯一的判断标准。退出码 0 = 通过，非零 = 失败，没有例外。

---

### 第三步：输出汇总并写入发布日志

```python
    all_passed = failed == 0
    summary    = "可以发布" if all_passed else f"不可发布 — {failed} 项未通过"
    print(f"\n结果: {summary}  ({passed}/{passed+failed} 项通过)")

    # 追加到发布日志（`--rollback` 依赖这个文件）
    with open(LOG_FILE, "a") as f:
        f.write(f"\n## {datetime.utcnow().isoformat()}Z — {ship_type}\n")
        for label, status in results:
            f.write(f"- [{status}] {label}\n")
        f.write(f"- **{summary}**\n")

    return all_passed

def main():
    ship_type = sys.argv[1] if len(sys.argv) > 1 else "code-pr"
    ok = run_checklist(ship_type)
    sys.exit(0 if ok else 1)   # 退出码供 CI/CD 流水线使用

if __name__ == "__main__":
    main()
```

---

## 工具二：回滚触发脚本

### 第一步：从日志中找到最近一次发布记录

```python
import re

LOG_FILE = "ship-log.md"

# 每种发布类型对应的回滚命令
ROLLBACK_INSTRUCTIONS = {
    "code-pr":    "git push origin --delete <branch>   # 删除 PR 分支",
    "deployment": "kubectl rollout undo deployment/<name>",
    "content":    "通过 CMS 或 git revert 回滚到上一版本",
}

def find_last_ship(log_path: str) -> dict | None:
    if not os.path.exists(log_path):
        return None
    last = None
    with open(log_path) as f:
        for line in f:
            # 匹配格式: ## 2024-01-15T10:30:00Z — code-pr
            m = re.match(r"^## ([\dT:.Z-]+) — (\S+)", line)
            if m:
                last = {"timestamp": m.group(1), "type": m.group(2)}
    return last  # 遍历完整个文件，返回最后一个匹配
```

**关键行**：`last = {"timestamp": ..., "type": ...}` 在循环里不断覆盖 — 自然得到**最后一次**发布记录，而不是第一次。

---

### 第二步：打印回滚指令

```python
def main():
    entry = find_last_ship(LOG_FILE)
    if not entry:
        print(f"[error] 在 {LOG_FILE} 中没有找到发布记录。")
        sys.exit(1)

    ship_type   = entry["type"]
    ts          = entry["timestamp"]
    instruction = ROLLBACK_INSTRUCTIONS.get(ship_type, "需要手动回滚。")

    print(f"最近一次发布 : {ship_type}  时间: {ts}")
    print(f"回滚命令     : {instruction}")
    print()
    print("回滚后，重新运行检查清单再尝试发布：")
    print(f"  python ship_checklist.py {ship_type}")

if __name__ == "__main__":
    main()
```

---

## 动手改一改

1. 运行 `ship_checklist.py content`，检查通过了吗？如果没有，错误原因是什么？
2. 在 `CHECKLISTS["code-pr"]` 里添加一个新检查项：验证当前目录下没有 `.pyc` 文件。命令是什么？
3. 运行 `ship_checklist.py code-pr` 后再运行 `rollback_trigger.py`，回滚命令是什么？
4. 如果 `ship-log.md` 不存在，`rollback_trigger.py` 会输出什么？这说明回滚依赖什么前提？
