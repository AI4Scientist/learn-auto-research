# Lecture 06 — Error-Crushing Pipeline

[中文版本 →](/zh/lectures/lecture-06-error-crushing-pipeline/)

Code examples: [code/](./code/)  
Practice project: [Project 03 — Debug a Real Failure](/en/projects/project-03-debug-real-failure/)

---

`/autoresearch:debug` finds bugs. `/autoresearch:fix` eliminates errors. These are different problems with different strategies.

Debugging is investigation: you don't know what's wrong. Fixing is repair: you have a list of errors and need to reduce it to zero. The fix loop is optimized for systematic, cascade-aware error elimination.

## The Cascade Problem

When a codebase has multiple errors, fixing them is not independent. Fixing error A can reveal error B that was previously hidden. Fixing error B can break error C that was previously passing. Fixing error C can re-introduce error A.

Naive approaches fail here:
- Fixing errors in arbitrary order wastes time on errors that will be fixed as side effects
- Fixing multiple errors at once makes regressions unattributable
- Not running the full error suite after each fix means you don't know the current state

`/autoresearch:fix` handles this with a cascade-aware strategy: fix ONE error per iteration, prioritize blockers first, verify after each fix, guard against regressions.

## How the Fix Loop Works

**Setup**: The agent runs the verify command to establish a baseline error count and categorize all errors:

```
Baseline: 23 errors
  - Build errors: 3 (BLOCKER — nothing else can run)
  - Type errors: 8
  - Test failures: 9
  - Lint errors: 3
```

**Priority order**: Build errors → type errors → test failures → lint errors. Blockers first because downstream errors may disappear when blockers are fixed.

**Each iteration**:
1. Run verify: get current error list
2. Pick the highest-priority unfixed error
3. Formulate a specific hypothesis: "This error is caused by X, fix is Y"
4. Make ONE change to fix ONE error
5. `git commit`
6. Run verify: count errors. Did the count decrease?
7. Run guard: did anything else break?
8. If both pass: keep. If guard fails: attempt fix-of-fix (max 2 tries), else revert.
9. Log: which error was fixed, what changed, new error count
10. **Automatically stop when error count reaches 0**

The loop terminates on zero errors even in unbounded mode. You never need to specify `max_iterations` for a fix run if you trust the error suite.

## The Guard in Fix Mode

The guard is especially important in fix mode. When fixing error A, you might accidentally break previously-passing test B. The guard catches this.

```
/autoresearch:fix
Guard: npm test -- --testPathIgnorePatterns="auth.test"
```

You can narrow the guard to avoid known-broken tests. The guard protects the green tests while the fix loop repairs the red ones.

## Error Categories

| Category | Verify command | Priority |
|----------|---------------|----------|
| Build errors | `tsc --noEmit` or `cargo build` | 1 (blocker) |
| Type errors | `tsc --strict` | 2 |
| Test failures | `pytest` or `npm test` | 3 |
| Lint errors | `eslint` or `flake8` | 4 |
| Security issues | `bandit` or `npm audit` | 2 (if severity >= High) |

The agent auto-detects which categories are present. You can filter with `--category`:

```
/autoresearch:fix --category test  # only fix test failures
/autoresearch:fix --category type  # only fix type errors
```

## Using `--from-debug`

The most powerful chain is debug → fix:

```bash
# Step 1: Find all bugs
/autoresearch:debug
Scope: src/
Symptom: multiple test failures after refactor
Iterations: 15

# Step 2: Fix them all
/autoresearch:fix --from-debug
```

`--from-debug` reads `findings.md` from the latest debug session and uses confirmed root causes to prioritize which errors to fix first. This skips the discovery phase and goes straight to repair.

## Practical Example: Post-Refactor Cleanup

After a large refactor, a codebase has:
- 2 build errors (import paths changed)
- 5 type errors (return types not updated)
- 12 test failures (test fixtures use old API)
- 4 lint errors (unused variables from removed code)

Without autoresearch: a developer spends 2–3 hours manually working through each error, often introducing new ones while fixing others.

With `/autoresearch:fix`:

```
Iteration 1: Fix build error — update import path in auth.ts → 22 errors
Iteration 2: Fix build error — update import path in user.ts → 21 errors
Iteration 3: Fix type error — update return type in getUserById → 18 errors
  (3 type errors disappeared as side effects)
Iteration 4-6: Fix remaining type errors → 12 errors
Iteration 7-15: Fix test failures (8/12 fixed, 4 interdependent)
Iteration 16: Fix lint errors → 4 errors
Iteration 17-20: Fix remaining test failures → 0 errors
```

Zero errors in 20 iterations. The cascade management (fixing in priority order, detecting side-effect fixes) saved approximately 8 extra iterations.

## Regression Prevention

The fix loop can introduce regressions. A type fix might break a test. A test fix might change behavior in a way that affects other tests.

Three mechanisms prevent this:

1. **Guard**: runs the full green test suite after every fix
2. **One change per iteration**: if a regression occurs, exactly one commit is responsible
3. **Automatic revert**: if the guard fails and the fix-of-fix also fails, the original fix is reverted. The regression is logged, not introduced.

## When Fix Loop Stops

The loop stops when:
- Error count reaches 0 (even in unbounded mode) ✓
- `max_iterations` is exhausted
- An error is unfixable (logged as SKIP, move on) — after 3 failed attempts per error

Unfixable errors are logged in `fix_log.md` with the reason. This prevents infinite loops on errors that require architectural changes or external dependency fixes.

## Key Takeaways

- Fix and debug are different problems — fix assumes you know what's broken, debug investigates
- Cascade-aware ordering (blockers first) prevents wasting iterations on dependent errors
- One fix per iteration keeps regressions attributable — you always know what to revert
- The guard prevents regression accumulation — every fix is verified against the green baseline
- `--from-debug` chains investigation findings directly into repair, skipping rediscovery
- The loop automatically stops at zero errors — you don't need to watch it

---

**Next**: [Lecture 07 — Five-Expert Prediction](/en/lectures/lecture-07-five-expert-predict/)
