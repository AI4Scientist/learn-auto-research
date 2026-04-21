# Lecture 02 — What Is a Measurable Research Goal

[中文版本 →](/zh/lectures/lecture-02-what-is-a-measurable-research-goal/)

Code examples: [code/](./code/)  
Practice project: [Project 01 — Your First Research Loop](/en/projects/project-01-first-research-loop/)

---

The hardest part of autoresearch isn't running the loop. It's defining the goal correctly.

Most research goals are stated in natural language: "make the API faster," "improve model accuracy," "reduce bundle size." These are intentions, not metrics. An agent cannot optimize an intention — it can only optimize a number.

The `/autoresearch:plan` wizard exists precisely to convert intentions into mechanical metrics. But understanding *why* this matters, and what makes a metric good or bad, is the foundation of every successful autoresearch run.

## The Metric Trap

A bad metric is worse than no metric. It gives the agent a clear direction toward the wrong destination.

Consider "improve model accuracy." The agent increases accuracy on the training set by overfitting. Technically successful. Practically useless.

Or "reduce response time." The agent removes error handling to skip processing. Faster, yes. Also broken.

These failures happen because the metric didn't capture what the researcher actually cared about. A good metric has three properties:

**Measurable from code.** The metric must be computable by running a command or script. "User satisfaction" is not a metric. `p95_ms` from a load test is.

**Monotonically meaningful.** Higher (or lower) must always be better, with no diminishing returns that change the direction. A score that's good at 70% and bad at 100% will confuse the agent.

**Isolated from what you're not changing.** The metric should only measure the thing you're trying to improve, not side effects. If you're optimizing sort speed, the metric should measure sort speed — not total script time including file I/O.

## Core Concepts

**Mechanical metric**: A number computed by a deterministic procedure. Examples: `coverage_pct` from `pytest --cov`, `median_time_s` from `timeit`, `rmse` from `sklearn.metrics.mean_squared_error`.

**Direction**: Whether higher or lower is better. Always explicit — never leave this implicit. `median_time_s: minimize`. `accuracy: maximize`.

**Target**: The value at which the loop stops. `< 0.5`, `> 0.95`, `== 0`. Without a target, you need `max_iterations` to bound the run.

**Guard**: A secondary command that must pass for any change to be kept, regardless of the primary metric. Used to prevent regressions. Example: `Guard: python -m pytest test_sort.py` ensures the sort function still produces correct output after every speed optimization.

**Keep policy**: The rule for deciding whether to keep a change:
- `score_improvement`: keep if new score beats the current best
- `always_keep`: keep every change (useful for exploration)
- `human_review`: pause and ask the user (use sparingly — defeats the purpose of autonomy)

**Noise runs**: When a metric is noisy (varies between runs), take multiple measurements and use the median. Set `noise_runs: 3` in `research.md` to run the evaluator 3 times per iteration.

**Min delta**: The minimum improvement required to keep a change. Prevents keeping changes that improve the metric by noise-level amounts. Example: `min_delta: 0.01` means only keep changes that improve by at least 1%.

## The research.md Contract

`research.md` is the single source of truth for a research session. It contains everything the agent needs to run the loop:

```markdown
# Research: [Goal Title]

## Goal
[Plain-language description of what you're trying to achieve]

## Success Metric
- Metric: [metric_name]
- Target: [< 0.5 | > 0.95 | == 0]
- Direction: [minimize | maximize]

## Constraints
- Max iterations: [N]
- Evaluator: [command to run]
- Keep policy: [score_improvement | always_keep]
- Guard: [command that must always pass]
- Noise runs: [1-5]
- Min delta: [0 or a small number]

## History
| # | Change | Metric | Result | Timestamp |
|---|--------|--------|--------|-----------|
| 0 | Baseline ([description]) | [value] | -- | [date] |
```

The agent reads this file at the start of every iteration (Stage 1: Understand). The History table tells it what has been tried, what worked, and what was discarded. This is how the loop maintains memory across restarts.

## Designing a Good Evaluator

The evaluator is the script that computes the metric. It must output exactly:

```json
{"pass": true, "score": 0.94}
```

`pass` is true if the target is met. `score` is the metric value for this iteration.

A good evaluator is:
- **Deterministic** (or averaged over `noise_runs` to reduce variance)
- **Fast** (under 5 minutes — wrap with `timeout 5m`)
- **Isolated** (measures only what you're optimizing)
- **Self-contained** (no external dependencies that might fail)

```python
#!/usr/bin/env python3
import json, statistics, time, subprocess

TARGET = 0.5
N_RUNS = 3

times = []
for _ in range(N_RUNS):
    t0 = time.perf_counter()
    subprocess.run(["python", "sort.py"], check=True)
    times.append(time.perf_counter() - t0)

median = statistics.median(times)
print(json.dumps({"pass": median < TARGET, "score": round(median, 4)}))
```

## Metric Cheat Sheet

When you're not sure what metric to use, this table covers 15 common domains:

| Domain | Metric | Direction | Evaluator snippet |
|--------|--------|-----------|------------------|
| Code performance | `median_time_s` | minimize | `timeit` 3 runs, median |
| ML accuracy | `accuracy` | maximize | `sklearn.metrics.accuracy_score` |
| Bundle size | `bundle_kb` | minimize | `du -sk dist/ \| cut -f1` |
| Prompt quality | `llm_judge_score` | maximize | GPT-4o rates 1–10, average over 5 |
| Literature coverage | `papers_found` | maximize | Count matched papers |
| API latency | `p95_ms` | minimize | 100 requests, 95th percentile |
| Memory usage | `peak_mb` | minimize | `/usr/bin/time -v` |
| Test coverage | `coverage_pct` | maximize | `coverage run -m pytest` |
| RMSE | `rmse` | minimize | `sqrt(mean_squared_error)` |
| Security coverage | `coverage_pct` | maximize | Fixed / total findings |
| Query speed | `query_ms` | minimize | `EXPLAIN ANALYZE` |
| LLM judge | `score_1_10` | maximize | Blind 1–10, N=5 samples |

## Practical Example: From Intention to Metric

**Intention**: "Make the data pipeline faster."

Step 1 — What does "faster" mean in this context? End-to-end time? Throughput? Latency for the first result?

Step 2 — What can we actually measure? Let's say: time to process 10,000 records.

Step 3 — Write the evaluator: `python benchmark_pipeline.py` outputs `{"pass": elapsed < 30, "score": elapsed}`.

Step 4 — Define the scope: which files can the agent modify? Only `pipeline.py`. Not `schema.py` or test files.

Step 5 — Set the guard: `python -m pytest test_pipeline.py` must pass after every change.

**Result**: Goal = "Process 10,000 records in under 30 seconds." Metric = `elapsed_s`, minimize, target `< 30`. Guard = pytest. Scope = `pipeline.py` only.

This took 5 minutes to define. The agent can now run for hours without any human attention.

## Key Takeaways

- A goal is not a metric — convert every intention to a single measurable number
- Good metrics are computable from code, monotonically meaningful, and isolated
- The `research.md` file is the agent's memory — it reads it at the start of every iteration
- The Guard field prevents the agent from "cheating" — improving the metric by breaking something else
- Noise runs and min_delta prevent the agent from keeping changes that are noise-level improvements
- The `/autoresearch:plan` wizard converts a plain-language goal into a complete `research.md` in ~2 minutes

---

**Next**: [Lecture 03 — Five-Stage Loop Internals](/en/lectures/lecture-03-five-stage-loop-internals/)
