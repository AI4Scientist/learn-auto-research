# L12 Code — Overnight Runs & Advanced Patterns

> **Goal**: Use the progress monitor to read a TSV and determine if the loop has converged, then use the target checker to get a bash-compatible exit code for automated loop termination.

Run it:

```sh
# Generate a results file first (requires L03 simulator)
python ../lecture-03-five-stage-loop-internals/code/loop_simulator.py
# Then run the monitoring tools
python progress_monitor.py autoresearch-results.tsv
python check_target.py research.md autoresearch-results.tsv
echo "Exit code: $?"   # 0 = target met, 1 = keep running
```

---

## Tool 1: Progress Monitor

### Step 1: Load the TSV results file

```python
import csv, os, sys, math

def load(path: str) -> list[dict]:
    if not os.path.exists(path):
        print(f"[error] {path} not found.")
        sys.exit(1)
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)
    return rows
```

---

### Step 2: Compute convergence statistics

```python
def convergence_rate(values: list[float], window: int = 10) -> float:
    """Improvement per iteration over the last window iterations."""
    if len(values) < 2:
        return 0.0
    tail = values[-window:]
    return (tail[-1] - tail[0]) / (len(tail) - 1)
```

**Key line**: `values[-window:]` — only the last 10 iterations matter for convergence detection. Early iterations are noisy and don't reflect the current trend.

---

### Step 3: Interpret and print the convergence status

```python
    rate = convergence_rate(scores, window=10)
    if abs(rate) < 0.001:
        print("  → Plateau detected. Consider a pivot or increasing exploration.")
    elif rate > 0:
        print("  → Still improving. Let it run.")
    else:
        print("  → Declining. Check for overfitting or bad pivot.")

    # ASCII sparkline of last 20 scores
    tail = scores[-20:]
    lo, hi = min(tail), max(tail)
    span   = hi - lo if hi != lo else 1.0
    bars   = " ▁▂▃▄▅▆▇█"
    line   = "".join(bars[min(8, int((v - lo) / span * 8))] for v in tail)
    print(f"\nLast {len(tail)} scores: {line}")
```

**Key line**: The ASCII sparkline `▁▂▃▄▅▆▇█` turns 20 numbers into a visual trend in one line — faster to read than a table when you check in on an overnight run from the terminal.

---

## Tool 2: Target Checker

### Step 4: Parse target from `research.md`

```python
import re

def read_target(path: str) -> float | None:
    in_target = False
    with open(path) as f:
        for line in f:
            stripped = line.strip()
            if re.match(r"^##\s+target", stripped, re.IGNORECASE):
                in_target = True
                continue
            if in_target:
                if stripped.startswith("#"):
                    break
                m = re.search(r"[-+]?\d*\.?\d+", stripped)
                if m:
                    return float(m.group())
    return None
```

**Key line**: `re.match(r"^##\s+target", ...)` — case-insensitive match on `## Target` or `## target`. The parser finds the section header, then reads the first number it finds after it.

---

### Step 5: Compare best score to target and exit with correct code

```python
HIGHER_IS_BETTER = True

def main():
    target = read_target(RESEARCH_MD)
    best   = read_best_score(RESULTS_TSV)

    met = (best >= target) if HIGHER_IS_BETTER else (best <= target)

    if met:
        print(f"[SUCCESS] Target met! best={best} target={target}")
        sys.exit(0)   # bash: if python check_target.py; then break; fi
    else:
        print(f"[NOT YET] Gap remaining: {abs(target - best):.4f}")
        sys.exit(1)
```

**Key line**: `sys.exit(0 if met else 1)` — the exit code is the signal for the outer bash loop. `if python check_target.py research.md; then break; fi` stops the loop automatically when the target is reached, without any manual intervention.

---

## Try Changing It

1. After running `progress_monitor.py`, what is the convergence status? Is the rate positive, negative, or near zero?
2. Change `window=10` in `convergence_rate()` to `window=3` — does the convergence verdict change? Why might a shorter window be misleading?
3. In `check_target.py`, set `HIGHER_IS_BETTER = False` and change the target to something your simulated scores can reach — what does the exit code become?
4. Design a complete overnight setup: write the bash loop command you would use, the `research.md` target you'd set, and the convergence threshold you'd watch for.
