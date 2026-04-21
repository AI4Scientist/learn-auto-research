# Lecture 03 — Five-Stage Loop Internals

[中文版本 →](/zh/lectures/lecture-03-five-stage-loop-internals/)

Code examples: [code/](./code/)  
Practice project: [Project 02 — Baseline to Optimal](/en/projects/project-02-baseline-to-optimal/)

---

Every `/autoresearch` run follows the same five stages. Understanding what happens inside each stage — and why — is the key to designing research sessions that succeed rather than stall.

## Stage 1 — Understand

Before touching any code, the agent reads everything:

1. **`research.md`** — goal, metric, constraints, full history of every iteration
2. **`git log --oneline -20`** — recent experiment commits with their descriptions
3. **`git diff HEAD~1`** — what the last experiment actually changed
4. **All in-scope files** — the current state of every file the agent can modify

The critical insight here is **git as memory**. The agent doesn't maintain state between sessions — the git history is its memory. Every experiment is committed with an `experiment:` prefix and a description. When the agent reads `git log`, it reconstructs the full story of what's been tried:

```
experiment: try radix sort base 256 → 0.871s (kept)
experiment: try radix sort base 65536 → 0.573s (kept)  
experiment: try numpy sort → 0.612s (discarded, worse than base 65536)
experiment: micro-optimize radix with unrolled passes → 0.498s (kept, TARGET MET)
```

This log tells the agent: "radix sort is the winning family. Base 65536 is better than base 256. Numpy sort was tried and lost. The micro-optimization direction is promising." All of this from reading git history.

**Why read before write?** Agents that skip Stage 1 re-try experiments that already failed. They make changes that conflict with previous optimizations. They miss patterns in the history that would suggest the next hypothesis. Reading everything first is not optional — it's what separates systematic research from random search.

## Stage 2 — Hypothesize

One specific, testable change. Not "try different algorithms." Not "optimize performance." Exactly: "Change the sort implementation from recursive quicksort to radix sort with base 256, because radix sort has O(n·k) complexity vs O(n log n) for quicksort on integers, and this dataset has bounded key range."

The hypothesis has three parts:
- **What**: the specific change to make
- **Why**: the mechanism by which it should improve the metric
- **Expected magnitude**: roughly how much improvement is expected

Good hypotheses are *falsifiable*. If the hypothesis is "try something different," you can't tell when it's been tested. If the hypothesis is "radix sort with base 256 should reduce median time by 30-50% because of reduced comparisons," you know exactly when it's been confirmed or disproven.

**The one-change rule** is the most important constraint in the entire framework. One change per iteration means:
- If the metric improves, you know exactly why
- If the metric worsens, you know exactly what to revert
- The git history is clean and readable
- Each iteration is an atomic unit of knowledge

## Stage 3 — Experiment

Make the change, then commit it. The commit happens *before* verification — this is intentional. It means:
- The failed experiment is preserved in git history (valuable: you know not to try this again)
- Reverting is a clean `git revert`, not a manual undo
- The codebase is always in a committed state

All bash commands are wrapped with `timeout 5m`:

```bash
timeout 5m python evaluate.py
```

Exit code 124 means timeout. On timeout: `git revert HEAD`, log "TIMEOUT", move to next iteration.

**Crash recovery** is handled automatically:
- Syntax error: fix immediately, don't count as an iteration
- Runtime error: attempt fix up to 3 times, then revert and move on
- Resource exhaustion (OOM, disk full): revert, try a smaller variant next iteration
- External dependency failure: skip the evaluator call, log "EXTERNAL_FAILURE", try different approach

## Stage 4 — Evaluate

Run the evaluator: `timeout 5m python evaluate.py`. Parse the output: `{"pass": bool, "score": number}`.

Apply the keep policy:

```
score_improvement:
  if score < previous_best (minimize) or score > previous_best (maximize):
    keep (git commit stays)
    update previous_best
  else:
    discard (git revert HEAD)

always_keep:
  always keep (useful for exploration phases)

human_review:
  pause, show result, ask user
```

If `guard` is defined, run it after keeping: `timeout 5m python -m pytest test_sort.py`. If guard fails:
1. Attempt to fix the regression (up to 2 tries)
2. If fix succeeds: keep the original improvement with the fix
3. If fix fails: revert the original change

The Guard is a safety net. It lets the agent optimize aggressively while preventing it from breaking invariants that matter.

**Simplicity wins**: When two changes achieve equal scores, keep the simpler one. Less code is better than more code, all else equal. This prevents the agent from accumulating unnecessary complexity over many iterations.

## Stage 5 — Log & Iterate

After every iteration, the agent:

1. Appends a row to `research.md` History:
   ```
   | 3 | radix sort base 256 | 0.871 | keep | 2026-04-20 |
   ```

2. Appends a detailed entry to `research_log.md`:
   ```
   ## Iteration 3
   Hypothesis: radix sort base 256 should reduce time by ~60%
   Change: replaced quicksort with radix sort (base 256) in sort.py lines 12-34
   Result: 0.871s (was 2.399s baseline) — KEEP
   Notes: significant improvement. Try larger base next.
   ```

3. Appends a row to `autoresearch-results.tsv`:
   ```
   3  b2c3d4e  0.871  -1.528  keep  radix sort base 256
   ```

4. (Optional) Updates `progress.png` — a convergence plot showing metric vs. iteration number

Then checks termination conditions:
- Target met? → Write `final_report.md`, stop
- `max_iterations` exhausted? → Write `final_report.md`, stop
- Otherwise: **return to Stage 1 immediately**. No pausing, no asking permission, no summarizing. The loop continues.

## The Full Loop in Practice

```
Iteration 1: Understand → Hypothesize (radix 256) → Experiment → 0.871s → Keep → Log → back to Stage 1
Iteration 2: Understand → Hypothesize (radix 65536) → Experiment → 0.573s → Keep → Log → back to Stage 1
Iteration 3: Understand → Hypothesize (numpy sort) → Experiment → 0.612s → Discard → Log → back to Stage 1
Iteration 4: Understand → Hypothesize (micro-optimize radix) → Experiment → 0.498s → Keep (TARGET MET) → final_report.md
```

4 iterations. 4 commits in git history. A clear story of what was tried, what worked, and why.

## Output Files

| File | Contents | Updated |
|------|----------|---------|
| `research.md` | Goal, constraints, full history table | Every iteration |
| `research_log.md` | Detailed notes per iteration | Every iteration |
| `autoresearch-results.tsv` | Machine-readable (8 columns) | Every iteration |
| `progress.png` | Convergence plot: metric vs. iteration | Every iteration |
| `final_report.md` | Summary, best result, next steps | When done |

## Key Takeaways

- Stage 1 (Understand) is the most underrated stage — reading git history prevents re-trying failed experiments
- The one-change rule makes every iteration's result interpretable
- Commit before verify — this keeps git history clean and rollback simple
- The Guard runs after the metric check, not before — it prevents regressions without blocking exploration
- Stage 5 triggers Stage 1 immediately — no human intervention between iterations
- All output files together give a complete record of the research session

---

**Next**: [Lecture 04 — What to Do When Stuck](/en/lectures/lecture-04-what-to-do-when-stuck/)
