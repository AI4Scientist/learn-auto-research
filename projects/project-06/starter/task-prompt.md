# Task — Project 06: End-to-End Research Project

## Goal
Improve the `summarize()` function in `pipeline.py` so that mean ROUGE-1 recall
across all 5 corpus entries reaches **≥ 0.60**.

## Current State
Baseline: first-N-sentences summary. Mean ROUGE-1 ≈ 0.28.

## Constraints
- Only modify `pipeline.py`
- Do not modify `corpus.py` or `evaluate.py`
- Use Python stdlib only

## Metric
`mean_rouge1_recall` — maximize — target `>= 0.60`

## Suggested Directions
- Extractive summarization: rank sentences by keyword overlap with document
- TF-IDF style scoring: weight words by frequency
- Lead + keyword hybrid: combine position bias with content relevance
- Query-focused: extract sentences most relevant to the reference keywords

## This is the Full Pipeline
In this project you will run the complete autoresearch workflow:
1. `/autoresearch:plan` — set up research.md
2. `/autoresearch` — run the improvement loop
3. `/autoresearch:ship` — generate final report and tag release
