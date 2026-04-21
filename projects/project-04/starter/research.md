# research.md — Project 04

## Goal
Score architectures; best weighted score >= 0.65.

## Metric
`weighted_score` — maximize — target `>= 0.65`

## History

| iter | commit | weighted_score | delta | status | description |
|------|--------|----------------|-------|--------|-------------|
| 0 | baseline | 0.71 | — | keep ✓ | microservices wins with default weights |

## Guard
```
python evaluate.py
```

## Max Iterations
10
