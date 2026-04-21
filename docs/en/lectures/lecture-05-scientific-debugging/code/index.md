# L05 Code — Scientific Debugging

> **Goal**: Use the hypothesis tracker to add and update hypotheses, then run the falsification loop to automatically test and classify each active hypothesis.

Run it:

```sh
cd docs/en/lectures/lecture-05-scientific-debugging/code
python hypothesis_tracker.py add "Caching the DB query reduces latency"
python hypothesis_tracker.py add "Switching to binary search improves throughput"
python hypothesis_tracker.py list
python falsification_loop.py
python hypothesis_tracker.py list
```

---

## Tool 1: Hypothesis Tracker

### Step 1: Parse and write the Markdown table

```python
import re, os
from datetime import date

FILE   = "hypotheses.md"
HEADER = "# Hypotheses\n\n| # | Status | Date | Hypothesis |\n|---|--------|------|------------|\n"

def load() -> list[dict]:
    if not os.path.exists(FILE):
        return []
    rows = []
    with open(FILE) as f:
        for line in f:
            m = re.match(
                r"\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*([\d-]+)\s*\|\s*(.+?)\s*\|", line
            )
            if m:
                rows.append({"id": int(m.group(1)), "status": m.group(2),
                              "date": m.group(3), "text": m.group(4)})
    return rows
```

**Key line**: The regex `\|\s*(\d+)\s*\|...` parses the Markdown table format — a format humans can also edit directly in their editor. The file is always human-readable.

---

### Step 2: Add a new hypothesis

```python
def cmd_add(rows, text):
    new_id = max((r["id"] for r in rows), default=0) + 1
    rows.append({"id": new_id, "status": "active",
                 "date": date.today().isoformat(), "text": text})
    save(rows)
    print(f"Added hypothesis #{new_id}: {text}")
```

**Key line**: `default=0` in `max()` — handles the case where the file is empty. The first hypothesis gets id=1.

---

### Step 3: Update hypothesis status

```python
def cmd_update(rows, hyp_id, new_status):
    for r in rows:
        if r["id"] == hyp_id:
            r["status"] = new_status
            save(rows)
            print(f"Hypothesis #{hyp_id} → {new_status}")
            return
    print(f"Hypothesis #{hyp_id} not found.")
```

Valid statuses: `active`, `confirmed`, `eliminated`. Only `active` hypotheses are tested by the falsification loop.

---

## Tool 2: Falsification Loop

### Step 4: Load only active hypotheses

```python
def load_active() -> list[dict]:
    rows = []
    with open(FILE) as f:
        for line in f:
            m = re.match(
                r"\|\s*(\d+)\s*\|\s*active\s*\|\s*([\d-]+)\s*\|\s*(.+?)\s*\|", line
            )
            if m:
                rows.append({"id": int(m.group(1)), "text": m.group(3)})
    return rows
```

**Key line**: The regex matches only rows with `active` status — confirmed and eliminated hypotheses are skipped. The loop only tests what hasn't been resolved yet.

---

### Step 5: Test and auto-classify each hypothesis

```python
def test_hypothesis(hyp: dict) -> bool:
    """Return True = CONFIRMED, False = ELIMINATED."""
    text = hyp["text"].lower()
    return "cache" in text or "index" in text  # demo heuristic

def main():
    active = load_active()
    for hyp in active:
        result     = test_hypothesis(hyp)
        new_status = "confirmed" if result else "eliminated"
        print(f"  #{hyp['id']} [{'CONFIRMED' if result else 'ELIMINATED'}] — {hyp['text']}")
        subprocess.run([sys.executable, "hypothesis_tracker.py",
                        "update", str(hyp["id"]), new_status], check=False)
```

**Key line**: `subprocess.run(["hypothesis_tracker.py", "update", ...])` — the falsification loop calls the tracker as a subprocess, so both tools can be used independently or together.

---

## Try Changing It

1. After running both tools, how many hypotheses are in each status? What does `hypotheses.md` look like?
2. Add a hypothesis that does NOT contain "cache" or "index" — what status does the falsification loop assign it?
3. Replace `test_hypothesis()` with a real check for your project — what command would you run, and what would a `True` result mean?
4. In the FastAPI 503 example from the lecture, write 3 hypotheses in the `hypothesis_tracker.py add` format — one for each stage of investigation.
