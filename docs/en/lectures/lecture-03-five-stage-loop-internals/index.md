# Lecture 03 — Five-Stage Loop Internals

`L01 > L02 > [ L03 ] L04 > L05 > L06 | L07 > L08 > L09 > L10 > L11 > L12`

> *"git is the agent's memory."* — Every experiment is a commit. Every commit can be reverted. Nothing is ever truly lost.
>
> **Core idea**: What actually happens inside each `/autoresearch` iteration — and why Stage 1 (reading history) is the most important stage.

Code examples: [code/](./code/)  
Practice project: [Project 02 — Baseline to Optimal](/en/projects/project-02-baseline-to-optimal/)

[中文版本 →](/zh/lectures/lecture-03-five-stage-loop-internals/)

---

## The Problem

Most automated agents keep trying the same thing in different ways — because they don't remember what they already tried. Without memory, every iteration starts from scratch.

The autoresearch loop solves this with git: every experiment is committed before it's evaluated, so the entire history of what was tried, what worked, and what didn't is readable at the start of every iteration.

## The Solution

```
Stage 1: Understand    ← read research.md + git log + all in-scope files
         |
Stage 2: Hypothesize   ← ONE specific, falsifiable change + expected magnitude
         |
Stage 3: Experiment    ← make the change → git commit (before verify!)
         |
Stage 4: Evaluate      ← run evaluate.py → compare to previous_best
         |              → keep or revert
Stage 5: Log & Iterate ← append to research.md, results.tsv, research_log.md
         |
         └──────────────────────────────────── back to Stage 1
```

The loop only stops when: target met, or `max_iterations` exhausted.

## How It Works

**1. Stage 1 — Understand (don't skip this).**

The agent reads everything before touching any code:

```
research.md          → goal, metric, constraints, full history
git log --oneline    → what was tried and what the result was
git diff HEAD~1      → what the last experiment actually changed
all in-scope files   → current state of everything the agent can modify
```

Reading git history is what prevents wasted iterations:
```
experiment: try radix sort base 256 → 0.871s (kept)
experiment: try radix sort base 65536 → 0.573s (kept)
experiment: try numpy sort → 0.612s (discarded, worse)
```
From this log the agent learns: radix wins, numpy lost, base 65536 beats base 256. All from reading.

**2. Stage 2 — Hypothesize (one change, one mechanism).**

Not "try something different." Exactly: *"Change recursive quicksort to radix sort base 256, because radix has O(n·k) vs O(n log n) on bounded-key integers. Expected improvement: 30-50%."*

A good hypothesis has: what, why, and expected magnitude. Vague hypotheses can't be falsified.

**3. Stage 3 — Experiment (commit before verify).**

Make the change, then `git commit` *before* running the evaluator. Why?

```
commit first  →  failed experiment preserved in git history
              →  rollback is clean: git revert HEAD
              →  codebase always in committed state
```

All commands are wrapped: `timeout 5m python evaluate.py`. Exit code 124 = timeout → auto-revert.

**4. Stage 4 — Evaluate (the keep policy decides).**

```
score_improvement:
  new_score < previous_best (minimize)?  → keep
  new_score >= previous_best?            → git revert HEAD

always_keep:   keep regardless (for exploration phases)
human_review:  pause and ask
```

If a `Guard` is defined, run it *after* keeping: `timeout 5m python -m pytest test_sort.py`. Guard fails → attempt fix (max 2 tries) → if still failing, revert.

**5. Stage 5 — Log (every iteration writes three places).**

```
research.md          → append row to History table
research_log.md      → detailed per-iteration notes
autoresearch-results.tsv → machine-readable: iteration, commit, metric, delta, status
```

Then immediately return to Stage 1. No pausing, no summarizing, no asking permission.

## What Changed

| Manual research | Autoresearch loop |
|---|---|
| Experiments live in your head | Every experiment is a git commit |
| Failed approaches forgotten | Failed approaches in git log forever |
| Re-tries same dead ends | Stage 1 reads history before every iteration |
| Results scattered in notebooks | Three structured output files, always current |
| Stops when you stop | Loops until target or budget exhausted |

## Try It

Simulate the 5 stages with the loop simulator:

```sh
cd docs/en/lectures/lecture-03-five-stage-loop-internals/code
python loop_simulator.py
```

Questions to think about:

1. After the simulation, what does the `autoresearch-results.tsv` look like? What columns does it have?
2. Find the first "revert" row — what was the hypothesis, and why did it fail?
3. In Stage 3, why does the commit happen *before* `evaluate.py` runs, not after?
4. Change `MAX_ITERATIONS = 10` to `MAX_ITERATIONS = 3` — does the loop reach the target? What does it write to `final_report.md`?

---

**Next**: [Lecture 04 — What to Do When Stuck](/en/lectures/lecture-04-what-to-do-when-stuck/)
