# L06 Code — Error-Crushing Pipeline

> **Goal**: Run the cascade-aware error sorter to see blockers-first ordering, then run the regression checker to see which metric changes count as regressions.

Run it:

```sh
cd docs/en/lectures/lecture-06-error-crushing-pipeline/code
python error_sorter.py
python regression_checker.py
```

---

## Tool 1: Cascade-Aware Error Sorter

### Step 1: Define errors with dependencies

```python
from collections import defaultdict, deque

ERRORS = [
    ("E01", "ImportError: module 'mylib' not found",           []),
    ("E02", "AttributeError: NoneType has no attribute 'run'", ["E01"]),
    ("E03", "TypeError: unsupported operand type in calc()",   ["E01"]),
    ("E04", "AssertionError in test_output_shape",             ["E02", "E03"]),
    ("E05", "FileNotFoundError: config.yaml missing",          []),
    ("E06", "KeyError: 'learning_rate' in config loader",      ["E05"]),
]
```

**Key line**: Each error declares what it *depends on* — `E02` depends on `E01`, meaning E01 must be fixed first. This dependency graph drives the sorting.

---

### Step 2: Topological sort — blockers first

```python
def topological_sort(errors: list) -> list:
    graph     = defaultdict(list)
    in_degree = defaultdict(int)
    nodes     = {e[0] for e in errors}

    for eid, _desc, deps in errors:
        in_degree[eid]          # ensure key exists even with no deps
        for dep in deps:
            if dep in nodes:
                graph[dep].append(eid)
                in_degree[eid] += 1
```

**Key line**: `in_degree[eid]` — accessing the key with no assignment ensures every error has an entry in the dict, even errors with no dependencies (in_degree = 0). These become the starting queue.

---

### Step 3: Process queue — zero in-degree means no blockers

```python
    queue = deque(eid for eid in nodes if in_degree[eid] == 0)
    order = []
    while queue:
        current = queue.popleft()
        order.append(lookup[current])
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
```

**Key line**: `if in_degree[neighbor] == 0: queue.append(neighbor)` — once a blocker is fixed (removed from queue), decrement its dependents. When a dependent reaches in_degree=0, all its blockers are fixed and it's ready to process.

---

## Tool 2: Regression Checker

### Step 4: Compare baseline vs. candidate with tolerance

```python
TOLERANCE = 0.01  # allow up to 1% degradation before flagging

LOWER_IS_BETTER = {"p50_latency_ms", "p99_latency_ms", "error_rate"}

def check(baseline: dict, candidate: dict) -> None:
    for key in sorted(set(baseline) | set(candidate)):
        b, c = baseline.get(key), candidate.get(key)
        change = (c - b) / abs(b) if b != 0 else 0.0

        if key in LOWER_IS_BETTER:
            regressed = change > TOLERANCE    # higher is worse
        else:
            regressed = change < -TOLERANCE   # lower is worse
```

**Key line**: `LOWER_IS_BETTER` set — the same formula works for both directions; only the comparison sign flips. `p99_latency_ms` going up is bad; `accuracy` going down is bad.

---

### Step 5: Print categorized results and fail loudly

```python
    if regressions:
        print(f"[FAIL] {len(regressions)} regression(s) detected. Do not ship.")
    else:
        print("[PASS] No regressions beyond tolerance.")
```

**Key line**: The report separates regressions, improvements, and neutral changes — so a fix that improves one metric but regresses another is immediately visible.

---

## Try Changing It

1. In `error_sorter.py` output, which error is #1 in priority? Why must E01 come before E02?
2. Add a new error `("E07", "ValueError in post-processing", ["E04"])` — where does E07 appear in the sorted output?
3. In `regression_checker.py`, change `TOLERANCE = 0.01` to `0.20` — does `p99_latency_ms` still show as a regression?
4. In the post-refactor example from the lecture, 3 type errors disappeared as side effects of fixing one build error. What does this tell you about the value of blockers-first ordering?
