# Research: Sort Optimization

## Goal
Reduce sort.py execution time to under 0.5 seconds on 1 million integers.

## Success Metric
- Metric: median_time_s
- Target: < 0.5
- Direction: minimize

## Constraints
- Max iterations: 20
- Evaluator: python benchmark.py
- Keep policy: score_improvement
- Guard: python -m pytest test_sort.py
- Noise runs: 3
- Min delta: 0

## Search Space
- Allowed to modify: sort.py (algorithm only)
- Forbidden: test_sort.py, benchmark.py, function signature

## History
| # | Change | Metric | Result | Timestamp |
|---|--------|--------|--------|-----------|
| 0 | Baseline (recursive quicksort) | 2.3991 | -- | 2026-04-20 |
