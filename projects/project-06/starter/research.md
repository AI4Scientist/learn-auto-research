# research.md — Project 06

## Goal
Improve summarize() so mean ROUGE-1 recall >= 0.60.

## Metric
`mean_rouge1_recall` — maximize — target `>= 0.60`

## History

| iter | commit | mean_rouge1 | delta | status | description |
|------|--------|-------------|-------|--------|-------------|
| 0 | baseline | 0.28 | — | keep | first-N-sentences baseline |

## Guard
```
python evaluate.py
```

## Max Iterations
20
