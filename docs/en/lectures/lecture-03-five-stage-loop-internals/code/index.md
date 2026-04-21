# L03 Code — Five-Stage Loop Internals

> **Goal**: Run the 5-stage loop simulator and watch each stage execute — READ goal, GENERATE change, EVALUATE, KEEP/REVERT, LOG to TSV — the same sequence as a real `/autoresearch` run.

Run it:

```sh
cd docs/en/lectures/lecture-03-five-stage-loop-internals/code
python loop_simulator.py
```

---

## Step 1: Bootstrap and configure

```python
import csv, os, random, math
from datetime import datetime

MAX_ITERATIONS = 10
TARGET_SCORE   = 0.90
RANDOM_SEED    = 7

random.seed(RANDOM_SEED)

if not os.path.exists("research.md"):
    with open("research.md", "w") as f:
        f.write("# Research Goal\n\n## Target\n0.90\n\n## Metric\naccuracy\n")
```

**Key line**: Writing `research.md` if it doesn't exist mirrors Stage 1 — the loop always reads from a file, never from memory.

---

## Step 2 (Stage 1+2): Read goal and generate hypothesis

```python
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

target = read_target("research.md")
```

**Key line**: `read_target()` runs at the start of every iteration — not once at startup. In a real loop the agent re-reads the entire git history here, learning from every prior experiment.

---

## Step 3 (Stage 3): Evaluate the change

```python
def fake_evaluate(iteration: int) -> float:
    """Simulate noisy improvement over iterations."""
    ideal = 0.50 + 0.05 * math.log1p(iteration)
    noise = random.gauss(0, 0.02)
    return min(max(ideal + noise, 0.0), 1.0)
```

**Key line**: `math.log1p(iteration)` — diminishing returns over time. Early iterations improve fast; later iterations improve slowly. This mirrors real research loops.

---

## Step 4 (Stage 4): Keep or revert

```python
for i in range(1, MAX_ITERATIONS + 1):
    score = fake_evaluate(i)
    delta = score - prev_score

    if score >= prev_score:
        status = "keep"
        prev_score = score
        if score > best_score:
            best_score = score
    else:
        status = "revert"
        # prev_score unchanged — revert means previous state is restored
```

**Key line**: `status = "revert"` but `prev_score` is not updated — a reverted change leaves the codebase exactly as it was. The score goes back to the previous best.

---

## Step 5 (Stage 5): Log every iteration

```python
    writer.writerow([i, f"abc{i:04d}", round(score, 4),
                     round(delta, 4), status, f"auto-change-{i:03d}"])
    tsv_file.flush()

    if best_score >= target:
        print(f"[done] target {target} reached at iteration {i}")
        break
else:
    print(f"[done] budget exhausted. best={best_score:.4f}")
```

**Key line**: `tsv_file.flush()` after every row — if the loop crashes or is interrupted, the TSV already has all completed iterations. No data is lost.

---

## Try Changing It

1. After running, open `autoresearch-results.tsv` — what columns does it have? Find the first "revert" row.
2. Change `MAX_ITERATIONS = 10` to `MAX_ITERATIONS = 3` — does the loop reach `TARGET_SCORE = 0.90`? What does it print at the end?
3. Change `TARGET_SCORE = 0.90` to `TARGET_SCORE = 0.55` — how many iterations does it take to reach the target?
4. In Stage 4, why is `prev_score` NOT updated when `status = "revert"`? What would happen if it were updated?
