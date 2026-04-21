# Project 01 — Your First Research Loop

[中文版本 →](/zh/projects/project-01-first-research-loop/)

**Paired with**: [Lecture 01](/en/lectures/lecture-01-why-manual-iteration-fails/) + [Lecture 02](/en/lectures/lecture-02-what-is-a-measurable-research-goal/)  
**Starter code**: [projects/project-01/starter/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-01/starter/)  
**Solution**: [projects/project-01/solution/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-01/solution/)

---

## What You'll Build

Run the canonical autoresearch example: optimize a Python sort function from ~2.4 seconds to under 0.5 seconds on 1 million integers. You'll use `/autoresearch:plan` to scaffold the project and `/autoresearch` to run the loop.

## Learning Objectives

By completing this project, you will:
- Convert a vague goal ("make it faster") into a mechanical metric (`median_time_s < 0.5`)
- Write an evaluator that outputs `{"pass": bool, "score": float}`
- Run the 5-stage loop and read the resulting `research.md` history
- Understand what gets committed and why

## Starting Point

```
projects/project-01/starter/
├── sort.py          ← the slow implementation (recursive quicksort)
├── test_sort.py     ← correctness tests (never modify)
└── task-prompt.md   ← your mission
```

`sort.py` contains a recursive quicksort on a list of 1 million integers. It takes ~2.4 seconds. Your goal: get it under 0.5 seconds without breaking the tests.

## Step 1 — Run the Plan Wizard

```bash
cd projects/project-01/starter/
/autoresearch:plan
```

Answer the wizard questions:
- **Goal**: Reduce sort.py execution time to under 0.5s on 1M integers
- **Metric**: `median_time_s`, direction: minimize, target: `< 0.5`
- **Noisy?** Yes — benchmarks vary. Set `noise_runs: 3`
- **Scope**: `sort.py` only. Forbidden: `test_sort.py`
- **Guard**: `python -m pytest test_sort.py`
- **Max iterations**: 20

The wizard generates `benchmark.py` and `research.md`.

## Step 2 — Run the Loop

```bash
/autoresearch
```

Watch the loop run. After 3–5 iterations you should see:
```
| 3 | radix sort base 256     | 0.871 | keep    |
| 4 | radix sort base 65536   | 0.573 | keep    |
| 5 | micro-optimized radix   | 0.498 | keep ✓  | ← target met
```

## Step 3 — Read the Results

Open `research.md` and `research_log.md`. Answer these questions:
1. How many iterations did it take to hit the target?
2. Which experiments were discarded? Why?
3. What does the git log look like? (`git log --oneline`)

## Expected Outcome

```
Final best: median_time_s = 0.498
Target: < 0.5 ✓
Iterations used: 5 of 20
```

## Verification

```bash
python benchmark.py
# Expected: {"pass": true, "score": 0.498}

python -m pytest test_sort.py
# Expected: all tests pass
```

## Hints

- If the loop is running slowly, it's because `noise_runs: 3` runs the benchmark 3 times per iteration. This is correct behavior — benchmarks are noisy.
- If you see `GUARD FAILED`, the sort is producing wrong results. Check which change broke correctness.
- The solution directory contains a completed `research.md` with a full 5-iteration history you can compare against.
