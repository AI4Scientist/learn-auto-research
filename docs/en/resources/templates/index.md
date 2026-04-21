# Templates

Copy these into your project to start a research loop immediately.

## research.md

The single source of truth for any autoresearch session. The agent reads this at the start of every iteration.

```markdown
# Research: [Goal Title]

## Goal
[Plain-language description of what you're trying to achieve]

## Success Metric
- Metric: [metric_name_with_units]
- Target: [< 0.5 | > 0.95 | == 0]
- Direction: [minimize | maximize]

## Constraints
- Max iterations: 20
- Evaluator: python evaluate.py
- Keep policy: score_improvement
- Guard: [command that must always pass, e.g. python -m pytest]
- Noise runs: 3
- Min delta: 0

## History
| # | Change | Metric | Result | Timestamp |
|---|--------|--------|--------|-----------|
| 0 | Baseline ([description]) | [value] | -- | [YYYY-MM-DD] |
```

## evaluate.py

Generic evaluator template. Replace the measurement logic with your domain.

```python
#!/usr/bin/env python3
"""
Evaluator contract: print {"pass": bool, "score": float} then exit 0.
Wrap the main command in: timeout 5m python evaluate.py
"""
import json, sys, statistics, time, subprocess

TARGET = 0.5       # change to your target
DIRECTION = "min"  # "min" or "max"
N_RUNS = 3         # set to 1 if not noisy

def measure() -> float:
    """Replace this with your actual measurement."""
    times = []
    for _ in range(N_RUNS):
        t0 = time.perf_counter()
        subprocess.run(["python", "main.py"], check=True, capture_output=True)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)

score = measure()
passed = (score < TARGET) if DIRECTION == "min" else (score > TARGET)
print(json.dumps({"pass": passed, "score": round(score, 4)}))
sys.exit(0)
```

## autoresearch-results.tsv

The machine-readable results log. Eight columns, tab-separated.

```
iteration	commit	metric	delta	status	description	timestamp	notes
0	a1b2c3d	2.3991	0.0	baseline	recursive quicksort	2026-04-20	
1	b2c3d4e	0.8709	-1.5282	keep	radix sort base 256	2026-04-20	
2	-	0.9122	+0.0413	discard	radix sort base 128	2026-04-20	worse
3	c3d4e5f	0.4979	-0.3730	keep	micro-optimized radix	2026-04-20	TARGET MET
```

## research_log.md

Detailed per-iteration notes. Append after every iteration.

```markdown
# Research Log: [Goal Title]

## Iteration 1
**Hypothesis**: [specific, testable hypothesis with mechanism]
**Change**: [what was changed, file:line]
**Result**: [score] — [KEEP | DISCARD]
**Notes**: [what was learned, what to try next]

## Iteration 2
...
```

## AGENTS.md (for research projects)

```markdown
# Research Agent Instructions

## Goal
[One-sentence goal from research.md]

## Workflow
1. Read research.md — understand goal, metric, full history
2. Read git log — what has been tried?
3. Propose ONE hypothesis
4. Make ONE change
5. Run evaluator: python evaluate.py
6. Keep or revert based on score
7. Log to research.md and research_log.md
8. Repeat

## Forbidden
- Do not modify evaluate.py or test files
- Do not make more than one change per iteration
- Do not ask "should I continue?" — keep going until target or max_iterations
```
