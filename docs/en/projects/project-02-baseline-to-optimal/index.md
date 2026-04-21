# Project 02 — Baseline to Optimal

[中文版本 →](/zh/projects/project-02-baseline-to-optimal/)

**Paired with**: [Lecture 03](/en/lectures/lecture-03-five-stage-loop-internals/) + [Lecture 04](/en/lectures/lecture-04-what-to-do-when-stuck/)  
**Starter code**: [projects/project-02/starter/](https://github.com/zhimin-z/learn-auto-research/tree/main/projects/project-02/starter/)  
**Solution**: [projects/project-02/solution/](https://github.com/zhimin-z/learn-auto-research/tree/main/projects/project-02/solution/)

---

## What You'll Build

A function fitting experiment: discover the hidden mathematical function that generated a dataset. The target RMSE is < 0.05. The loop will get stuck at an intermediate local optimum — you'll observe the L1 pivot strategy in action.

## Learning Objectives

- Write a custom evaluator for a non-trivial metric (RMSE)
- Observe the 5-stage loop internals by reading `research_log.md` in detail
- Experience the L1 pivot (3 consecutive non-improving iterations)
- Understand how the agent reads git history to avoid re-trying failed approaches

## Starting Point

```
projects/project-02/starter/
├── predict.py        ← your model (starts with linear regression)
├── generate_data.py  ← generates train/test data (read-only)
├── train_data.csv    ← training data
├── test_data.csv     ← test data  
├── evaluate.py       ← RMSE evaluator (already written)
└── research.md       ← pre-configured with goal and constraints
```

The hidden function has the form `y = f(x₁, x₂)`. The starter `predict.py` uses linear regression — RMSE ~2.1. The target is RMSE < 0.05.

## Step 1 — Establish Baseline

```bash
python evaluate.py
# {"pass": false, "score": 2.1147}
```

Baseline confirmed. The agent will read this from `research.md` when the loop starts.

## Step 2 — Run the Loop

```bash
/autoresearch
```

Watch for the L1 pivot. After ~5 iterations optimizing polynomial features, the agent will hit 3 non-improving iterations and switch strategy. Note what it pivots to.

## Key Observation

Read `research_log.md` after iteration 8. You should see something like:

```
## Iteration 7
Hypothesis: degree-6 polynomial should capture more curvature
Result: RMSE = 0.31 — DISCARD (worse than best: 0.28)

## Iteration 8 [L1 PIVOT]
History analysis: tried linear (2.1), quadratic (0.8), cubic (0.41), degree-4 (0.29), 
degree-5 (0.28), degree-6 (0.31). Polynomial family appears saturated.
New direction: try interaction terms and non-polynomial features (log, sqrt, exp).
Hypothesis: log(x₁) * x₂ interaction may capture the hidden function structure.
Result: RMSE = 0.12 — KEEP
```

The pivot from polynomial to interaction terms is the L1 strategy: same paradigm (feature engineering), different direction.

## Expected Outcome

```
Final best: rmse = 0.028
Target: < 0.05 ✓
Iterations used: ~12 of 20
```

## Verification

```bash
python evaluate.py
# {"pass": true, "score": 0.028}

git log --oneline | head -15
# Shows the full experiment history
```
