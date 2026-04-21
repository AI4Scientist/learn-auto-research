# Lecture 12 — Overnight Runs & Advanced Patterns

`L01 > L02 > L03 > L04 > L05 > L06 | L07 > L08 > L09 > L10 > L11 > [ L12 ]`

> *"You sleep. The loop compounds."* — 100 experiments overnight, full git provenance in the morning. This is what Karpathy's original script demonstrated: the researcher's attention is the bottleneck, not the compute.
>
> **Core idea**: How to run autoresearch unattended overnight, monitor convergence from the terminal, integrate with CI/CD, and build custom evaluators for any domain.

Code examples: [code/](./code/)  
Practice project: [Project 06 — End-to-End Research Project](/en/projects/project-06-end-to-end-research/)

[中文版本 →](/zh/lectures/lecture-12-overnight-runs-advanced/)

---

## The Problem

The loop works in 20-iteration daytime sessions. But the real payoff is overnight: 100+ iterations while you sleep, wake up to `final_report.md` with the best result, full git history of every experiment. The challenge is keeping the loop alive, monitoring it without babysitting, and knowing when to stop.

## The Solution

```
Option 1: tmux (recommended)
  tmux new-session -d -s research
  claude -p '/autoresearch' --max-turns 200
  Ctrl+B D to detach → loop keeps running
  tmux attach -t research to check anytime

Option 2: bash loop (shell-level control)
  for i in $(seq 1 100); do
    claude -p "/autoresearch Iterations: 1"
    if python check_target.py research.md; then break; fi
  done

Option 3: CI/CD (nightly scheduled)
  cron: '0 2 * * *'
  claude -p "/autoresearch Iterations: 50" --cwd research/
```

## How It Works

**1. tmux is the best overnight runner.**

```bash
tmux new-session -d -s autoresearch
tmux send-keys -t autoresearch "claude -p '/autoresearch' --max-turns 200" Enter
# Detach: Ctrl+B D
# Check progress at any time:
tmux attach -t autoresearch
```

tmux survives disconnects. The loop keeps running even if your SSH session drops. You can check in and detach without interrupting the loop.

**2. Monitor convergence without babysitting.**

```bash
# Watch the results TSV grow
watch -n 30 "tail -20 autoresearch-results.tsv"
```

Run `progress_monitor.py` to read the TSV and print a convergence report:
- Total iterations, keep rate, best/worst/latest scores
- Convergence status: still improving / stabilizing / converged (std of last 5 kept < 0.005)

**3. `check_target.py` enables clean bash loop exits.**

```bash
python check_target.py research.md autoresearch-results.tsv
# Exit code 0 = target met, exit code 1 = not yet
```

Use it in the bash loop to stop as soon as the target is reached — even mid-budget.

**4. MCP servers extend what the evaluator can measure.**

Any MCP server configured in Claude Code is available during the loop:

```markdown
# research.md
Evaluator: Use MCP postgres tool to run EXPLAIN ANALYZE on the target query
Metric: query_ms
```

```markdown
Evaluator: Call MCP openai tool to judge prompt quality, average 5 samples
Metric: llm_judge_score
```

Any external system becomes a metric source.

**5. Custom evaluators follow one simple contract.**

```python
#!/usr/bin/env python3
import json, sys

score = measure_something()
TARGET = 0.95
passed = score >= TARGET

print(json.dumps({"pass": passed, "score": round(score, 4)}))
sys.exit(0)
```

Output `{"pass": bool, "score": float}` to stdout. Exit 0. That's the entire contract.

**6. The research → skill pipeline.**

A successful overnight run produces knowledge. Encode it as a reusable skill:

```
research.md → autoresearch runs → final_report.md → SKILL.md
```

Use `/autoresearch:learn --mode init` to scan the research output and generate documentation from it automatically.

## What Changed

| Daytime 20-iteration session | Overnight run |
|---|---|
| Stops when you stop | tmux survives disconnects, loop keeps running |
| Manual progress checks | `progress_monitor.py` prints convergence stats |
| Fixed iteration budget | `check_target.py` stops the loop when target is met |
| Standard evaluator only | MCP servers: any external system is a metric |
| Findings in your head | `final_report.md` + full git provenance waiting in the morning |

## Try It

Generate a TSV with the L03 simulator, then run the monitoring tools:

```sh
cd docs/en/lectures/lecture-12-overnight-runs-advanced/code
python progress_monitor.py autoresearch-results.tsv
python check_target.py research.md autoresearch-results.tsv
```

Questions to think about:

1. After running `progress_monitor.py`, what is the convergence status? What is `std_last5`?
2. Change the convergence threshold from `std < 0.005` to `std < 0.05` — does the same data show "converged" now?
3. In `check_target.py`, change `Target: < 0.5` to `Target: < 0.1` in `research.md` and re-run — what is the exit code?
4. Design a custom evaluator for something you'd actually want to optimize: what does `measure_something()` do, what is `TARGET`, and is the direction minimize or maximize?

---

**Course Complete.** You now have the full autoresearch toolkit. Start with [Project 06](/en/projects/project-06-end-to-end-research/) to build a complete research pipeline end to end.
