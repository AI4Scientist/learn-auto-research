# Lecture 04 — What to Do When Stuck

[中文版本 →](/zh/lectures/lecture-04-what-to-do-when-stuck/)

Code examples: [code/](./code/)  
Practice project: [Project 02 — Baseline to Optimal](/en/projects/project-02-baseline-to-optimal/)

---

Every research loop eventually stalls. The metric stops improving. The agent tries variation after variation with no progress. If the loop has no strategy for this, it will waste the entire remaining budget on minor perturbations of a dead-end approach.

The autoresearch framework has a three-level pivot strategy for exactly this situation.

## What "Stuck" Means

The agent is stuck when it has made N consecutive iterations without improving the metric. This can happen for several reasons:

- **Local optimum**: The current approach has been optimized as far as it can go within its paradigm
- **Wrong abstraction**: The metric is improving in the wrong dimension (making the fast path faster while the slow path dominates)
- **Hypothesis exhaustion**: All reasonable variations of the current strategy have been tried
- **Noisy metric**: The metric variance is larger than the improvements being made

The stuck-detection thresholds in `research.md`:
```
Stuck detection:
  L1: 3 consecutive non-improving iterations → switch strategy
  L2: 5 consecutive non-improving iterations → paradigm shift
  L3: max_iterations exhausted → final_report.md
```

## Level 1 Pivot — Switch Strategy

After 3 non-improving iterations, the agent switches to a different strategy *within the same paradigm*.

If the paradigm is "optimize sort algorithm" and the agent has been trying radix sort variations, L1 pivot means: stop trying radix sort variants, try a completely different algorithm family (merge sort, timsort, counting sort).

The L1 pivot prompt the agent follows:
1. Re-read the full history — what paradigms have been tried?
2. What hasn't been tried in the current paradigm?
3. Pick the most promising untried approach
4. Form a new hypothesis with a clear mechanism

L1 pivot is conservative. It stays within the same problem framing but changes direction within it.

## Level 2 Pivot — Paradigm Shift

After 5 consecutive non-improving iterations, the agent escalates to a paradigm shift.

A paradigm shift means questioning the assumptions of the current approach. If you've been trying to optimize the sort algorithm itself, a paradigm shift might be: "What if the sort isn't the bottleneck? What if pre-processing the data before sorting is the bottleneck?"

Paradigm shifts are harder to specify mechanically, so the L2 pivot involves:
1. **Root cause analysis**: Why might the current approach be fundamentally limited?
2. **Constraint relaxation**: Which of the original constraints can be loosened?
3. **Cross-domain transfer**: What approaches from other domains might apply here?
4. **Combination strategies**: Can near-misses from the history be combined?

The agent re-reads the *entire* history, not just recent iterations, looking for near-misses — experiments that almost worked but didn't quite make it. These are often the seeds of breakthrough iterations.

## Level 3 — Max Iterations Exhausted

When `max_iterations` is reached, the loop stops. This isn't failure — it's the budget being spent. The agent writes `final_report.md` with:

1. **Best result achieved**: the highest (or lowest) metric value and the commit that achieved it
2. **What worked**: a summary of the successful approaches
3. **What didn't work**: a summary of failed approaches and why
4. **Recommended next steps**: 3–5 specific hypotheses to try in the next session
5. **Limitations**: what constraints might have prevented reaching the target

The `final_report.md` becomes the starting point for the next session. The new session reads it and picks up where the old one left off.

## Handling Noisy Metrics

A metric that varies by ±0.1 between runs will cause stuck detection to fire prematurely — the agent keeps making small improvements that look like non-improvements due to noise.

Fix this with `noise_runs: 3` in `research.md`. Instead of measuring the metric once, the agent runs the evaluator 3 times and takes the median. This reduces variance significantly.

For very noisy metrics (like LLM judge scores or network latency), use `noise_runs: 5` and a larger `min_delta`:
```
noise_runs: 5
min_delta: 0.05  # only keep changes that improve by at least 5%
```

## The "Think Harder" Rule

Rule 8 of the autoresearch framework: **When stuck, think harder.**

This sounds vague, but it has a specific implementation. When the agent detects it's stuck, before pivoting, it:

1. Re-reads the complete history looking for patterns
2. Identifies the best 3 experiments and asks: "What do these have in common?"
3. Identifies the worst 3 experiments and asks: "What did these all try?"
4. Generates 5 hypotheses it hasn't tried yet
5. Ranks them by expected impact
6. Picks the top-ranked one

This structured reflection often breaks stalls without needing a full paradigm shift.

## Practical Example: Stuck on Sort Optimization

Suppose after 8 iterations, the best result is `median_time_s = 0.52` (target: `< 0.5`), and the last 3 iterations have all been around 0.53–0.55.

**L1 pivot analysis**:
- Tried: radix sort (base 256, 512, 1024, 2048), timsort, numpy.sort
- Not tried: parallel sort (multiprocessing), SIMD-optimized sort (ctypes), partial sort (if only top-K needed)

New hypothesis: "Use Python's multiprocessing to sort chunks in parallel, then merge. This could halve the time on a 4-core machine."

Result: 0.49s — target met. The paradigm shift wasn't needed.

**If multiprocessing hadn't worked** (L2 pivot scenario):

- Root cause analysis: "Python's GIL limits parallel performance. Even with multiprocessing, the merge step is sequential."
- Paradigm shift: "Instead of optimizing the sort itself, can we avoid sorting altogether? Does the downstream code actually need a fully sorted array, or just the top-K elements?"
- New hypothesis: "Use `heapq.nsmallest(K, data)` instead of sorting the full array."

This is a complete paradigm shift — from "sort faster" to "don't sort." Often the best stuck-breaking move.

## Configuration Reference

```markdown
## Constraints
- Max iterations: 20
- Evaluator: python evaluate.py
- Keep policy: score_improvement
- Guard: python -m pytest test_sort.py
- Noise runs: 3
- Min delta: 0.01
- Stuck L1: 3  # trigger strategy switch after 3 non-improving
- Stuck L2: 5  # trigger paradigm shift after 5 non-improving
```

## Key Takeaways

- Stuck detection is proactive — don't wait for the budget to run out before changing strategy
- L1 pivot (3 iterations): change direction within the current paradigm
- L2 pivot (5 iterations): question the paradigm itself
- L3 (max iterations): write final_report.md, the next session reads it
- Noisy metrics cause false stuck detection — use `noise_runs` and `min_delta`
- "Think harder" means structured reflection on history patterns, not random exploration
- Near-misses in the history often contain the seeds of breakthrough approaches

---

**Next**: [Lecture 05 — Scientific Debugging](/en/lectures/lecture-05-scientific-debugging/)
