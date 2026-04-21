# L02 Code — What Is a Measurable Research Goal

> **Goal**: Generate a `research.md` contract and run the evaluator once to see the `{"pass": bool, "score": float}` output format that every autoresearch loop depends on.

Run it:

```sh
cd docs/en/lectures/lecture-02-what-is-a-measurable-research-goal/code
python gen_research_md.py
python evaluate.py
```

---

## Tool 1: research.md Generator

### Step 1: Define the template

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

**Key line**: The `## Target` section is what `check_target.py` parses later — it must contain a bare number the loop can compare against.

---

### Step 2: Prompt for each field with defaults

```python
def prompt(label: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    raw = input(f"{label}{hint}: ").strip()
    return raw if raw else default
```

**Key line**: `return raw if raw else default` — pressing Enter accepts the default. This makes it fast to generate a working `research.md` in under 30 seconds.

---

### Step 3: Write the file

```python
def main():
    goal     = prompt("What are you trying to improve?",
                      "Reduce median sort time by 20%")
    metric   = prompt("How will you measure it?",
                      "median_ms on 10k-element list")
    target   = prompt("What value counts as success?", "≤ 8.0 ms")
    baseline = prompt("Current baseline value?",        "10.0 ms")
    notes    = prompt("Any constraints or notes?",
                      "Python stdlib only, no C extensions")

    content = TEMPLATE.format(date=date.today().isoformat(),
                              goal=goal, metric=metric,
                              target=target, baseline=baseline, notes=notes)
    with open("research.md", "w") as f:
        f.write(content)
    print(content)
```

---

## Tool 2: Evaluator Template

### Step 1: Define target and direction

```python
import json, sys, random

TARGET_SCORE    = 8.0   # lower is better for latency
HIGHER_IS_BETTER = False
```

**Key line**: `HIGHER_IS_BETTER = False` — this single flag determines the comparison direction. For accuracy-style metrics, set it to `True`.

---

### Step 2: Measure and compare

```python
def measure() -> float:
    random.seed(42)
    samples = [random.gauss(9.5, 1.0) for _ in range(100)]
    return sorted(samples)[len(samples) // 2]  # median

def evaluate() -> dict:
    score = measure()
    passed = score <= TARGET_SCORE if not HIGHER_IS_BETTER else score >= TARGET_SCORE
    return {"pass": passed, "score": round(score, 4)}
```

**Key line**: `{"pass": passed, "score": round(score, 4)}` — this dict is the entire contract. The loop reads `pass` to decide keep/revert and `score` to track progress.

---

### Step 3: Print and exit with the right code

```python
if __name__ == "__main__":
    result = evaluate()
    print(json.dumps(result))
    sys.exit(0 if result["pass"] else 1)
```

**Key line**: `sys.exit(0 if result["pass"] else 1)` — exit code 0 means "target met, stop the loop." Exit code 1 means "keep iterating." This is how the bash loop knows when to stop.

---

## Try Changing It

1. Run `evaluate.py` — what is the output `score`? Is `pass` true or false?
2. Change `TARGET_SCORE = 8.0` to `TARGET_SCORE = 10.0` — does `pass` change? Why?
3. Change `HIGHER_IS_BETTER = False` to `True` — what happens to the comparison logic?
4. Write a `research.md` for a project you care about — just fill in Goal, Metric, Target, and Baseline.
