# L11 Code — Universal Ship Pipeline

> **Goal**: Run the pre-ship checklist to see mechanical pass/fail verification, then run the rollback script to see how every ship action has a traceable undo path.

Run it:

```sh
cd docs/en/lectures/lecture-11-universal-ship-pipeline/code
python ship_checklist.py code-pr
python ship_checklist.py content
python rollback_trigger.py
```

---

## Tool 1: Pre-Ship Checklist Runner

### Step 1: Define checklists by ship type

```python
import subprocess, sys, os
from datetime import datetime

CHECKLISTS = {
    "code-pr": [
        ("Run test suite",
         ["python", "-m", "pytest", "--tb=short", "-q"]),
        ("Check syntax errors",
         ["python", "-m", "py_compile"] +
         [f for f in os.listdir(".") if f.endswith(".py")]),
    ],
    "deployment": [
        ("Run test suite",
         ["python", "-m", "pytest", "--tb=short", "-q"]),
        ("Validate evaluate.py contract",
         ["python", "-c",
          "import json,subprocess,sys; "
          "r=subprocess.run([sys.executable,'evaluate.py'],capture_output=True); "
          "d=json.loads(r.stdout); "
          "assert 'pass' in d and 'score' in d"]),
    ],
    "content": [
        ("Verify Markdown files exist",
         ["python", "-c",
          "import os; mds=[f for f in os.listdir('.') if f.endswith('.md')]; "
          "assert mds, 'No .md files found'"]),
    ],
}

LOG_FILE = "ship-log.md"
```

**Key line**: Every check is `(description, command)` — the check passes if and only if the command exits with code 0. No "looks good" judgments. A human cannot override a failing command item.

---

### Step 2: Run each item and record results

```python
def run_checklist(ship_type: str) -> bool:
    items = CHECKLISTS.get(ship_type)
    if items is None:
        print(f"[error] Unknown ship type '{ship_type}'.")
        sys.exit(1)

    passed, failed, results = 0, 0, []
    for label, cmd in items:
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            ok   = proc.returncode == 0
        except FileNotFoundError:
            ok = False
        except subprocess.TimeoutExpired:
            ok = False
```

**Key line**: `proc.returncode == 0` — the only criterion. Exit code 0 = pass, anything else = fail. Timeouts and missing commands also fail. There are no exceptions to this rule.

---

### Step 3: Write to ship log

```python
    all_passed = failed == 0
    summary    = "Ready to ship" if all_passed else f"Not ready — {failed} item(s) failed"
    print(f"\nResult: {summary}  ({passed}/{passed+failed} passed)")

    with open(LOG_FILE, "a") as f:
        f.write(f"\n## {datetime.utcnow().isoformat()}Z — {ship_type}\n")
        for label, status in results:
            f.write(f"- [{status}] {label}\n")
        f.write(f"- **{summary}**\n")

    return all_passed
```

**Key line**: `"a"` mode — the log is always appended, never overwritten. Every ship attempt is recorded, including failed ones. The rollback tool reads this log.

---

## Tool 2: Rollback Trigger

### Step 4: Find the last ship entry and print the rollback command

```python
import re

ROLLBACK_INSTRUCTIONS = {
    "code-pr":    "git push origin --delete <branch>",
    "deployment": "kubectl rollout undo deployment/<name>",
    "content":    "Revert via CMS or git revert to previous version",
}

def find_last_ship(log_path: str) -> dict | None:
    last = None
    with open(log_path) as f:
        for line in f:
            m = re.match(r"^## ([\dT:.Z-]+) — (\S+)", line)
            if m:
                last = {"timestamp": m.group(1), "type": m.group(2)}
    return last  # overwrite in loop → naturally gets the last one
```

**Key line**: `last = {...}` is overwritten in every loop iteration — naturally selecting the last match without any special handling. Walking the entire file and keeping the final match is simpler than reversing or indexing.

---

## Try Changing It

1. Run `ship_checklist.py content` — did the check pass? If not, what failed and why?
2. Add a new check to `CHECKLISTS["code-pr"]`: verify no `.pyc` files exist. What command does this use?
3. After running `ship_checklist.py code-pr`, run `rollback_trigger.py` — what rollback command is shown?
4. If `ship-log.md` doesn't exist when `rollback_trigger.py` runs, what happens? What precondition does rollback require?
