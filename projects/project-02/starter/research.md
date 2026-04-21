# research.md — Project 02

## Goal
Reduce RMSE of `fit_model()` below 0.05 on 500 noisy sine data points.

## Metric
`rmse` — minimize — target `< 0.05`

## History

| iter | commit | rmse | delta | status | description |
|------|--------|------|-------|--------|-------------|
| 0 | baseline | 0.320 | — | keep | degree-1 linear fit |

## Guard
```
python -m pytest test_fit.py
```

## Max Iterations
20
