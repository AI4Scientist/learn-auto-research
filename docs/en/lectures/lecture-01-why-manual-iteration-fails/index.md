# Lecture 01 — Why Manual Iteration Fails

`[ L01 ] L02 > L03 > L04 > L05 > L06 | L07 > L08 > L09 > L10 > L11 > L12`

> *"You sleep. The experiments don't have to."* — The bottleneck in manual research is you, not the model.
>
> **Core idea**: Why the loop beats the researcher, and the three principles that make it possible.

Code examples: [code/](./code/)  
Practice project: [Project 01 — Your First Research Loop](/en/projects/project-01-first-research-loop/)


---

## The Problem

The bottleneck in manual research is human attention. When you sleep, experiments stop. When you're in meetings, experiments stop. When an experiment breaks things, you often skip the rollback — and bad state accumulates.

On a good day: 3–5 experiments. Typical day: 1–2. Three fatal flaws:

**Attention is the bottleneck.** The research loop is gated by your calendar.

**Manual rollback is slow.** Bad experiments rarely get reverted. Broken state accumulates.

**Subjective judgment corrupts results.** "This looks promising" isn't a metric. Without mechanical evaluation, feel-good experiments get kept even when they don't improve the target.

## The Solution

```
+----------+      +------------+      +----------+
|  change  | ---> |  evaluate  | ---> |  better? |
|  one     |      |  python    |      |          |
|  thing   |      | evaluate.py|      +----+-----+
+----------+      +------------+           |
                                      yes → git commit (keep)
                                      no  → git revert (discard)
                                           |
                        (loop until target reached or budget exhausted)
```

One number. One direction. Automatic rollback. That's the entire secret of Karpathy's autoresearch script.

## How It Works

In 2025, Andrej Karpathy published a 630-line script that ran 100 ML experiments per night, unsupervised. It embodied three principles:

**1. One metric, one direction.**

```
Metric: val_bpb       # validation bits per byte
Direction: minimize   # lower is better
```

Not "model quality." Not "training stability." One number. Every decision collapses to: did this change lower `val_bpb`?

**2. Constrained scope.**

```
Scope: train.py only   # agent cannot touch anything else
```

If the metric worsens, the cause must be in `train.py`. Nothing else. Failures are isolatable.

**3. Mechanical verification + automatic rollback.**

```bash
python evaluate.py   # run for exactly 5 minutes
git commit           # commit first
# if score worsened:
git revert HEAD      # automatic, no manual cleanup
```

The result: a system where **every night compounds**. Failures are automatically forgotten. Successes are permanently recorded in git.

## Key Concepts

| Concept | Meaning |
|---------|---------|
| Autonomous research loop | modify → verify → keep/discard → repeat, no human between iterations |
| Mechanical metric | a number computed automatically, with a clear direction (higher/lower is better) |
| Keep policy | rule for deciding keep vs. discard; most common: `score_improvement` |
| Automatic rollback | `git revert` when score worsens — failed experiment stays in history but not in code |
| Bounded vs. unbounded | bounded: exactly N iterations; unbounded: run until target or user interrupt |

## Try It

Run the code example to see the efficiency gap between random guessing and systematic search:

```sh
cd docs/zh/lectures/lecture-01-why-manual-iteration-fails/code
python manual_vs_systematic.py
```

Questions to think about:

1. How much better is the grid strategy than the random strategy? Does the gap grow or shrink with a smaller budget?
2. Change `SEED = 42` to `SEED = 1` — the random strategy changes, but does the grid strategy?
3. In your own research project, what would "the metric" be? Can it be computed by one line of Python?
4. Try writing your first `research.md` — just three lines: goal, metric, direction.

---

**Next**: [Lecture 02 — What Is a Measurable Research Goal](/en/lectures/lecture-02-what-is-a-measurable-research-goal/)
