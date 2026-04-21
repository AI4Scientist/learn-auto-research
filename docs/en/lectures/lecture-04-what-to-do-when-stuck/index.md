# Lecture 04 — What to Do When Stuck

`L01 > L02 > L03 > [ L04 ] L05 > L06 | L07 > L08 > L09 > L10 > L11 > L12`

> *"Consecutive failures are not bad luck — they are a signal."* — Three non-improving iterations means change direction, not try harder in the same direction.
>
> **Core idea**: How the autoresearch loop detects stalls and automatically escalates through three pivot levels — so your budget doesn't get wasted on a dead end.

Code examples: [code/](./code/)  
Practice project: [Project 02 — Baseline to Optimal](/en/projects/project-02-baseline-to-optimal/)

[中文版本 →](/zh/lectures/lecture-04-what-to-do-when-stuck/)

---

## The Problem

Every research loop eventually stalls. The metric plateaus at 0.52 when the target is 0.50. The agent tries variation after variation — radix base 512, radix base 1024, radix base 2048 — and none of them improve.

Without a pivot strategy, the loop burns the entire remaining budget on minor perturbations of a dead-end approach.

## The Solution

```
Consecutive non-improving iterations:

  0 ──────────────────────────────  normal, keep trying
  |
  3 ──── L1 Pivot ─────────────────  switch strategy (same paradigm)
  |         ↓
  |   "All radix variants tried.
  |    Try parallel sort instead."
  |
  5 ──── L2 Pivot ─────────────────  paradigm shift
  |         ↓
  |   "Sort isn't the bottleneck.
  |    Try heapq.nsmallest() instead
  |    of sorting the full array."
  |
  N ──── L3 Stop ──────────────────  max_iterations exhausted
            ↓
        Write final_report.md
        (next session reads it and picks up)
```

## How It Works

**1. Configure stuck detection in `research.md`.**

```markdown
## Constraints
- Stuck L1: 3   # switch strategy after 3 non-improving iterations
- Stuck L2: 5   # paradigm shift after 5 non-improving iterations
- Noise runs: 3
- Min delta: 0.01
```

**2. L1 Pivot — change direction within the same paradigm.**

After 3 non-improving iterations, the agent:
1. Re-reads the full history — what has been tried?
2. Lists what hasn't been tried within the current paradigm
3. Picks the most promising untried approach
4. Forms a new hypothesis

If the paradigm is "optimize sort algorithm" and all radix variants have been tried, L1 means: stop radix variations, try a different algorithm family (merge sort, timsort, counting sort).

**3. L2 Pivot — question the paradigm itself.**

After 5 non-improving iterations, the agent escalates to a paradigm shift:
1. **Root cause analysis**: Why might the current approach be fundamentally limited?
2. **Constraint relaxation**: Which original assumptions can be loosened?
3. **Near-miss combination**: Which almost-worked experiments can be combined?

Example: *"Python's GIL limits parallel performance. Even with multiprocessing, the merge step is sequential. Instead of optimizing the sort itself — does the downstream code actually need a fully sorted array, or just the top-K elements? `heapq.nsmallest(K, data)` instead of sorting."*

This is a complete paradigm shift: from "sort faster" to "don't sort."

**4. L3 — write `final_report.md` and stop.**

When `max_iterations` is reached, the loop stops and writes:
- Best result achieved (commit hash + metric value)
- What worked and why
- What didn't work and why
- 3–5 specific next hypotheses for the next session

The next session reads `final_report.md` and picks up exactly where the old one left off. Budget exhaustion is not failure — it's the budget being spent.

**5. Handle noisy metrics with `noise_runs`.**

A metric that varies ±0.1 between runs will trigger false stuck detection — small improvements look like non-improvements due to noise.

```markdown
## Constraints
- Noise runs: 5    # run evaluator 5 times, take median
- Min delta: 0.05  # only keep changes that improve by ≥ 5%
```

## What Changed

| Without pivot strategy | With three-level pivot |
|---|---|
| Loop spends 20 iterations on one dead end | L1 fires at iteration 3, changes direction |
| No record of what was tried | Full pivot history in `research_log.md` |
| Budget exhaustion = failure | Budget exhaustion = `final_report.md` for next session |
| Noisy metrics cause premature stalls | `noise_runs` + `min_delta` filter out noise |

## Try It

Run the pivot detector on a simulated results file:

```sh
cd docs/en/lectures/lecture-04-what-to-do-when-stuck/code
python pivot_detector.py
```

Questions to think about:

1. In the output, what was the streak count when L1 triggered? What was the last metric value?
2. Change `L1_THRESHOLD = 3` to `L1_THRESHOLD = 1` — how does the pivot behavior change? Is this better or worse?
3. In the sort optimization example, why did the L2 pivot succeed where L1 didn't?
4. Write a `research.md` for a project you care about — set `Stuck L1` and `Stuck L2` thresholds you'd actually use.

---

**Next**: [Lecture 05 — Scientific Debugging](/en/lectures/lecture-05-scientific-debugging/)
