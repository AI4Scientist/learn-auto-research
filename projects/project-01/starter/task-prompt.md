# Project 01 — Task Prompt

## Mission

Optimize the sort function in `sort.py` to run in under 0.5 seconds on 1 million integers.

## Rules

1. Only modify `sort.py` — specifically the `sort_numbers` function implementation
2. Never modify `test_sort.py` or `benchmark.py`
3. The function signature must remain: `def sort_numbers(numbers: list[int]) -> list[int]:`
4. All tests in `test_sort.py` must pass after every change

## How to Start

```bash
# Run the evaluator to see baseline
python benchmark.py
# Expected: {"pass": false, "score": ~2.4}

# Run correctness tests
python -m pytest test_sort.py

# Start the research loop
/autoresearch:plan
# Then: /autoresearch
```

## Done When

```bash
python benchmark.py
# {"pass": true, "score": <0.5}

python -m pytest test_sort.py
# All 8 tests pass
```
