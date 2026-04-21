# Lecture 01 — Why Manual Iteration Fails

[中文版本 →](/zh/lectures/lecture-01-why-manual-iteration-fails/)

Code examples: [code/](./code/)  
Practice project: [Project 01 — Your First Research Loop](/en/projects/project-01-first-research-loop/)

---

In 2025, Andrej Karpathy published a 630-line Python script that could run 100 ML experiments per night — unsupervised, automatically reverting failures, compounding every improvement. The result: models that took experienced researchers weeks to tune were surpassed in 48 hours of overnight runs.

What made this possible wasn't a smarter model. It was a smarter loop.

## The Problem with Manual Iteration

Most researchers iterate like this: run an experiment, wait, analyze results, form a hypothesis, make a change, repeat. On a good day, that's 3–5 experiments. On a typical day, it's 1–2. Each experiment requires human attention: reading outputs, deciding what to try next, manually reverting when something breaks.

This approach has three fatal flaws:

**Human attention is the bottleneck.** You can't run experiments while sleeping, while in meetings, or while working on something else. The research loop is gated by your availability.

**Manual reversion is slow and lossy.** When an experiment makes things worse, reverting it is manual work — and researchers often don't revert at all, letting bad state accumulate in the codebase.

**Subjective judgment creeps in.** "This looks promising" is not a metric. Without mechanical evaluation, researchers keep experiments that feel good but don't actually improve the target.

## Karpathy's Insight

Karpathy's autoresearch script embodied three principles that changed everything:

**One metric. One direction.** `val_bpb` (validation bits per byte). Lower is better. Not "model quality" or "training stability" — a single number that tells the agent exactly what to optimize. Every decision collapses to: did this change lower `val_bpb`?

**Constrained scope.** The agent could only modify `train.py`. It could not touch data preparation, the tokenizer, or evaluation code. This constraint meant every failure was isolatable: if the metric got worse, it was because of a change in `train.py`, nothing else.

**Mechanical verification + automatic rollback.** After every change, the script ran training for exactly 5 minutes and measured the metric. If it improved: `git commit` and keep. If it worsened: `git revert` and try something else. No human judgment required, no manual cleanup.

The result was a system where **every night compounded**. Each iteration built on the best previous state. Failures were automatically forgotten. Successes were permanently recorded in git history.

## Core Concepts

**Autonomous research loop**: A self-running cycle of modify → verify → keep/discard → repeat, requiring no human intervention between iterations.

**Mechanical metric**: A number that can be computed automatically from a defined procedure, with a clear direction (higher or lower is better). Examples: `val_bpb`, `median_time_s`, `test_coverage_pct`.

**Keep policy**: The rule that decides whether to keep or discard a change. The most common policy: `score_improvement` (keep if the new score is better than the previous best).

**Automatic rollback**: When a change worsens the metric, `git revert` automatically restores the previous state. The failed experiment is preserved in git history but doesn't affect the codebase.

**Bounded vs. unbounded mode**: A bounded loop runs exactly N iterations then stops. An unbounded loop runs until the target metric is achieved or the user interrupts.

**Search space**: The set of files and parameters the agent is allowed to modify. Constraining this is essential — a narrow search space means failures are isolatable and the agent doesn't break things it shouldn't touch.

## Why This Generalizes

The principles Karpathy used for ML training apply to any domain where you can:

1. Define a single number that measures progress
2. Constrain what can be changed
3. Verify mechanically whether a change was an improvement
4. Automatically revert changes that weren't

This covers an enormous range of problems:

- **Code performance**: `median_time_s` on a benchmark. Modify the algorithm. Verify by running it. Revert if slower.
- **Test coverage**: `coverage_pct`. Modify test files. Verify with `pytest --cov`. Revert if coverage drops.
- **Prompt quality**: `llm_judge_score` (1–10, averaged over 5 samples). Modify the prompt. Verify with an LLM call. Revert if score drops.
- **Literature coverage**: `papers_found`. Modify the search strategy. Verify by counting matched papers. Keep if more papers found.

The common pattern: **constraint + metric + loop = compounding gains**.

## The Case Study: 100 Experiments per Night

Here's what Karpathy's script actually achieved. Starting from a baseline model with `val_bpb = 1.85`:

| Night | Best val_bpb | Experiments Run | Key Discovery |
|-------|-------------|-----------------|---------------|
| 1 | 1.72 | 23 | Larger embedding layer |
| 2 | 1.61 | 31 | Attention head configuration |
| 3 | 1.54 | 28 | Learning rate schedule |
| 4 | 1.49 | 19 | Architecture depth |

In four nights of unattended runs, the agent achieved what would have taken weeks of manual experimentation. Each night's best result became the next night's baseline. The loop compounded.

## What You Need to Run Your Own Loop

Before starting `/autoresearch`, you need three things:

1. **A goal**: "Reduce sort function time to under 0.5s on 1M integers"
2. **A metric**: `median_time_s` (minimize, target `< 0.5`)
3. **An evaluator**: a script that outputs `{"pass": bool, "score": number}`

That's it. The `/autoresearch:plan` wizard walks you through defining all three in about 2 minutes.

## Key Takeaways

- Manual iteration is bottlenecked by human attention — agents remove that bottleneck entirely
- Three principles unlock autonomous research: one metric, constrained scope, mechanical verification
- Automatic rollback means failures are free — the agent tries boldly because bad changes cost nothing
- Any domain with a measurable metric can use the autoresearch loop
- The compound effect is the real power: each night builds on the previous night's best result

---

**Next**: [Lecture 02 — What Is a Measurable Research Goal](/en/lectures/lecture-02-what-is-a-measurable-research-goal/)
