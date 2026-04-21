# Lecture 06 — Error-Crushing Pipeline

`L01 > L02 > L03 > L04 > L05 > [ L06 ] | L07 > L08 > L09 > L10 > L11 > L12`

> *"Fixing one error can reveal three more."* — Errors are not independent. Fix blockers first, verify after every change, guard against regressions.
>
> **Core idea**: How `/autoresearch:fix` eliminates a list of errors systematically — cascade-aware ordering, one fix per iteration, automatic regression detection.

Code examples: [code/](./code/)  
Practice project: [Project 03 — Debug a Real Failure](/en/projects/project-03-debug-real-failure/)


---

## The Problem

Debugging is investigation. Fixing is repair. They're different problems.

When a codebase has 23 errors after a large refactor, fixing them is not independent:
- Fix A can reveal error B that was hidden behind A
- Fix B can break test C that was previously green
- Fix C can re-introduce A

Naive approaches fail: fixing in random order wastes time, fixing multiple errors at once makes regressions unattributable, not running the full suite after each fix means you don't know the current state.

## The Solution

```
Run verify → get baseline error count and categorize:
  Build errors: 3   ← BLOCKER — fix these first
  Type errors:  8
  Test failures: 9
  Lint errors:  3

Each iteration:
  pick highest-priority unfixed error
        ↓
  ONE change to fix ONE error
        ↓
  git commit
        ↓
  run verify → did error count decrease?
        ↓
  run guard → did anything else break?
        ↓
  keep or revert
        ↓
  (loop until error count = 0)
```

The loop stops automatically at zero errors — even in unbounded mode.

## How It Works

**1. Priority order: blockers first.**

```
Build errors    → nothing else can run until these are fixed
Type errors     → may hide or cause test failures
Test failures   → the actual behavior regressions
Lint errors     → style issues, fix last
```

Fixing a build error often makes 3 type errors disappear as side effects. Cascade-aware ordering finds this automatically.

**2. One fix per iteration — always.**

This is the same rule as the core loop, applied to error fixing. One change means: if a regression appears, exactly one commit is responsible. You always know what to revert.

**3. The guard prevents regression accumulation.**

```markdown
Guard: npm test -- --testPathIgnorePatterns="auth.test"
```

You can narrow the guard to exclude known-broken tests. The guard protects the green tests while the fix loop repairs the red ones. If the guard fails and the fix-of-fix also fails (2 attempts max), the original fix is reverted automatically.

**4. Practical result: post-refactor cleanup.**

```
Baseline: 23 errors (2 build, 5 type, 12 test, 4 lint)

Iteration 1:  fix build error (import path in auth.ts) → 22 errors
Iteration 2:  fix build error (import path in user.ts) → 21 errors
Iteration 3:  fix type error (getUserById return type) → 18 errors  ← 3 disappeared as side effects
Iteration 4-6: fix remaining type errors → 12 errors
Iteration 7-15: fix test failures → 4 errors
Iteration 16:  fix lint errors → 4 errors
Iteration 17-20: fix remaining test failures → 0 errors
```

Zero errors in 20 iterations. The cascade management saved ~8 extra iterations compared to random order.

**5. Chain with debug: `--from-debug`.**

```bash
# Step 1: find all bugs
/autoresearch:debug
Scope: src/
Symptom: multiple test failures after refactor

# Step 2: fix them all
/autoresearch:fix --from-debug
```

`--from-debug` reads `findings.md` from the latest debug session and uses confirmed root causes to prioritize. Skips the discovery phase, goes straight to repair.

## What Changed

| Manual error fixing | `/autoresearch:fix` |
|---|---|
| Fix in random order | Blockers → types → tests → lint |
| Multiple changes at once | One fix per iteration |
| Regressions introduced silently | Guard catches regressions after every fix |
| Loop when done manually | Stops automatically at zero errors |
| Re-investigate same errors | `fix_log.md` records unfixable errors, prevents infinite loops |

## Try It

Run the error sorter and regression checker:

```sh
cd docs/en/lectures/lecture-06-error-crushing-pipeline/code
python error_sorter.py
python regression_checker.py
```

Questions to think about:

1. In `error_sorter.py`, which error category is first in the output? Why does this ordering matter?
2. What happens if you change the order so lint errors come before build errors — how many more iterations would the simulation take?
3. In the post-refactor example, 3 type errors disappeared as side effects of fixing one build error. Why does this happen?
4. Design a `Guard` command for a project you know — what test command would you run after every fix to catch regressions early?

---

**Next**: [Lecture 07 — Five-Expert Prediction](/en/lectures/lecture-07-five-expert-predict/)
