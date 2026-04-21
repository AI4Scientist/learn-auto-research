# Lecture 02 — What Is a Measurable Research Goal

`L01 > [ L02 ] L03 > L04 > L05 > L06 | L07 > L08 > L09 > L10 > L11 > L12`

> *"An intention is not a metric."* — The agent can only optimize a number, not a wish.
>
> **Core idea**: How to convert a natural-language goal into a mechanical metric the agent can actually optimize, and the complete structure of the `research.md` contract.

Code examples: [code/](./code/)  
Practice project: [Project 01 — Your First Research Loop](/en/projects/project-01-first-research-loop/)


---

## The Problem

Most research goals are stated in natural language: "make the API faster," "improve model accuracy," "reduce bundle size." These are intentions, not metrics.

A bad metric is worse than no metric — it gives the agent a clear direction toward the wrong destination:

- "Improve accuracy" → agent overfits the training set. Technically successful. Practically useless.
- "Reduce response time" → agent removes error handling to skip processing. Faster, yes. Also broken.

## The Solution

```
Natural-language goal
        |
        v
+-------+-------+
| Ask 3          |  →  Metric: median_time_s
| questions:     |  →  Direction: minimize
| 1. Computable  |  →  Target: < 0.5
|    from code?  |
| 2. Direction?  |
| 3. Target?     |
+-------+-------+
        |
        v
  research.md  ← the agent's single source of truth, read every iteration
```

The `/autoresearch:plan` wizard completes this conversion in about two minutes.

## How It Works

**1. Check if the metric qualifies.**

A good metric satisfies three conditions:

```python
# ✓ Computable from code
score = timeit.timeit(lambda: sort(data), number=100) / 100

# ✓ Monotonically meaningful (lower/higher always better — no inversion)
direction = "minimize"   # never "lower is sometimes bad"

# ✓ Isolated from what you're not changing
# metric only measures sort speed, not file I/O time
```

**2. Write `research.md`.**

```markdown
# Research: Speed Up the Sort Function

## Goal
Reduce sort_items() median execution time below 0.5 seconds.

## Success Metric
- Metric: median_time_s
- Target: < 0.5
- Direction: minimize

## Constraints
- Max iterations: 20
- Evaluator: python evaluate.py
- Keep policy: score_improvement
- Guard: python -m pytest test_sort.py
- Noise runs: 3
- Min delta: 0
```

**3. Understand each field.**

```
Guard      → prevents "cheating" — speed improvements can't break correctness
Noise runs → measure 3 times, take median — eliminates timing jitter
Min delta  → only real progress (> 0) counts as improvement, not noise
Target     → when reached, loop stops automatically
```

## Metric Cheat Sheet

| Domain | Metric | Direction | Evaluator core |
|--------|--------|-----------|----------------|
| Code performance | `median_time_s` | minimize | `timeit`, median of N runs |
| ML accuracy | `accuracy` | maximize | `accuracy_score` |
| Bundle size | `bundle_kb` | minimize | `du -sk dist/` |
| Prompt quality | `llm_judge_score` | maximize | LLM rates 1–10, average 5 |
| API latency | `p95_ms` | minimize | 100 requests, P95 |
| Test coverage | `coverage_pct` | maximize | `coverage run -m pytest` |

## Try It

Generate a complete `research.md` and run the evaluator once to see the contract:

```sh
cd docs/zh/lectures/lecture-02-what-is-a-measurable-research-goal/code
python gen_research_md.py       # generate example research.md
python evaluate.py              # see the evaluator output format
```

Questions to think about:

1. After running `evaluate.py`, what is the output `score`? When is `pass` true?
2. What happens if you remove the `Guard` field? How might the agent "cheat"?
3. Change `noise_runs` from 1 to 5 and re-run `evaluate.py` — does the score change? Why?
4. Write a `research.md` for your own project — just fill in Goal, Metric, Direction, Target.

---

**Next**: [Lecture 03 — Five-Stage Loop Internals](/en/lectures/lecture-03-five-stage-loop-internals/)
