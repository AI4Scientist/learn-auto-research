# research.md — Project 03

## Goal
Fix all bugs in `app.py` so all 6 tests pass.

## Metric
`test_pass_rate` — maximize — target `== 1.0`

## History

| iter | commit | test_pass_rate | delta | status | description |
|------|--------|----------------|-------|--------|-------------|
| 0 | baseline | 0.333 | — | keep | 2/6 tests pass (3 bugs present) |

## Guard
```
python -m pytest test_app.py
```

## Max Iterations
10
