# research.md — Project 05

## Goal
Fix security vulnerabilities; security_score == 1.0

## Metric
`security_score` — maximize — target `== 1.0`

## History

| iter | commit | security_score | delta | status | description |
|------|--------|----------------|-------|--------|-------------|
| 0 | baseline | 0.00 | — | keep | all 4 vulnerabilities present |

## Guard
```
python evaluate.py
```

## Max Iterations
10
