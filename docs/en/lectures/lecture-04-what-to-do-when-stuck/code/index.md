# L04 Code — What to Do When Stuck

> **Goal**: Run the pivot detector on a results file and see which pivot level (L1/L2/L3) has been triggered — and what action is recommended.

Run it:

```sh
cd docs/en/lectures/lecture-04-what-to-do-when-stuck/code
# Generate a results file first (requires L03 simulator)
python ../lecture-03-five-stage-loop-internals/code/loop_simulator.py
python pivot_detector.py autoresearch-results.tsv
```

---

## Step 1: Define pivot thresholds and advice

```python
import csv, sys, os

L1_THRESHOLD = 3
L2_THRESHOLD = 5
L3_THRESHOLD = 10

PIVOT_ADVICE = {
    1: "L1 pivot: try a different parameter value or small code tweak.",
    2: "L2 pivot: change your approach — try a different algorithm or architecture.",
    3: "L3 pivot: fundamental rethink needed — revisit the research goal itself.",
}
```

**Key line**: Three distinct thresholds, three distinct responses. L1 is cheap (try a small variation); L2 is expensive (paradigm shift); L3 means the goal itself may need revisiting.

---

## Step 2: Load the results TSV

```python
def load_tsv(path: str) -> list[dict]:
    if not os.path.exists(path):
        print(f"[error] file not found: {path}")
        sys.exit(1)
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)
    return rows
```

---

## Step 3: Count the trailing revert streak

```python
def analyse(rows: list[dict]) -> None:
    streak = 0
    for row in reversed(rows):
        status = row.get("status", "").strip().lower()
        if status == "revert":
            streak += 1
        else:
            break
```

**Key line**: `for row in reversed(rows)` — only the *trailing* streak matters. Ten reverts in the middle of a run don't matter if the last 5 iterations all kept. Walking backwards finds the current streak without scanning the whole history.

---

## Step 4: Determine pivot level and print recommendation

```python
    pivot_level = 0
    if streak >= L3_THRESHOLD:
        pivot_level = 3
    elif streak >= L2_THRESHOLD:
        pivot_level = 2
    elif streak >= L1_THRESHOLD:
        pivot_level = 1

    if pivot_level == 0:
        print(f"[ok] No pivot needed yet (streak={streak}).")
    else:
        print(f"[!] {PIVOT_ADVICE[pivot_level]}")
        print(f"    Streak of {streak} consecutive reverts.")
```

**Key line**: Checking L3 before L2 before L1 — if `streak >= 10`, it's also `>= 5` and `>= 3`. Check the most severe condition first to avoid multiple triggers.

---

## Try Changing It

1. In the output, what is the current revert streak? Which pivot level was triggered?
2. Change `L1_THRESHOLD = 3` to `L1_THRESHOLD = 1` — how does the pivot behavior change? Is this better or worse?
3. Manually edit `autoresearch-results.tsv` to add 6 consecutive "revert" rows at the end — what does the detector output now?
4. In the sort optimization example from the lecture, which pivot level broke the stall? Why didn't L1 work?
