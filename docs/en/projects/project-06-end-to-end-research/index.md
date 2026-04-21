# Project 06 — End-to-End Research Project

[中文版本 →](/zh/projects/project-06-end-to-end-research/)

**Paired with**: [Lecture 11](/en/lectures/lecture-11-universal-ship-pipeline/) + [Lecture 12](/en/lectures/lecture-12-overnight-runs-advanced/)  
**Starter code**: [projects/project-06/starter/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-06/starter/)  
**Solution**: [projects/project-06/solution/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-06/solution/)

---

## What You'll Build

A complete end-to-end automated research pipeline: choose your own optimization target, run an overnight simulation (50 iterations), debug any issues, run a security audit, and ship the result.

## Learning Objectives

- Design your own `research.md` from a blank slate
- Run a simulated overnight session (50 iterations with `max_iterations: 50`)
- Chain all 10 commands in a single cohesive workflow
- Write a `final_report.md` and use it to scaffold the next research session

## Your Mission

Choose ONE of the following optimization targets (or propose your own):

| Option | Target | Metric |
|--------|--------|--------|
| A | Optimize a text compression algorithm | `compression_ratio` (maximize) |
| B | Improve a recommendation system's precision | `precision_at_10` (maximize) |
| C | Reduce a graph traversal algorithm's memory | `peak_mb` (minimize) |
| D | Your own domain (requires writing evaluator) | Your choice |

## The Full Pipeline

```bash
# Phase 1: Plan
/autoresearch:plan

# Phase 2: Research (simulate overnight — 50 iterations)
/autoresearch
Iterations: 50

# Phase 3: Debug (if any issues arose during research)
/autoresearch:debug

# Phase 4: Fix
/autoresearch:fix

# Phase 5: Security (if the artifact is an API or service)
/autoresearch:security

# Phase 6: Ship
/autoresearch:ship --type research
```

## Deliverables

By the end of this project, you should have:

1. `research.md` — full experiment history (50 rows)
2. `research_log.md` — detailed notes on key iterations
3. `final_report.md` — best result + recommendations for next session
4. `autoresearch-results.tsv` — machine-readable results
5. `progress.png` — convergence plot

## Reflection Questions

After completing the pipeline, write a short `reflection.md` answering:
1. How many iterations did it take to reach the target? Did you need to pivot?
2. What was the most surprising discovery in the research history?
3. If you ran another 50 iterations tonight, what would you try?
4. What would you do differently in the `research.md` setup?

## Overnight Simulation Script

To simulate a real overnight run without actually waiting overnight:

```bash
# Run 50 iterations in tmux
tmux new-session -d -s overnight
tmux send-keys -t overnight \
  "claude -p '/autoresearch Iterations: 50'" Enter

# Monitor progress from another terminal
watch -n 60 "tail -5 autoresearch-results.tsv && echo '---' && cat research.md | grep 'Best:'"
```
