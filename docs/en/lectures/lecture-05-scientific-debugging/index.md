# Lecture 05 — Scientific Debugging

[中文版本 →](/zh/lectures/lecture-05-scientific-debugging/)

Code examples: [code/](./code/)  
Practice project: [Project 03 — Debug a Real Failure](/en/projects/project-03-debug-real-failure/)

---

Most debugging is not scientific. It is archaeological. The developer digs through logs, tries things, changes multiple variables at once, and eventually stumbles on the fix — without ever understanding why the fix worked.

`/autoresearch:debug` applies the scientific method to bugs: one falsifiable hypothesis per iteration, systematic evidence collection, and a permanent record of what was tested and what was learned.

## Why Most Debugging is Slow

The standard debugging session looks like this: observe a symptom, form a vague hypothesis ("it's probably the database connection"), make several changes at once, observe whether the symptom changes, make several more changes, repeat.

This approach has three problems:

**Multi-variable changes.** When you change three things and the bug goes away, you don't know which change fixed it. When the bug comes back, you don't know which change to make.

**Confirmation bias.** Developers tend to test hypotheses they believe are true and not test the ones that would falsify their belief. Evidence accumulates only on one side.

**Lost institutional knowledge.** When a debugging session ends, the failed hypotheses are forgotten. The next developer who encounters the same bug starts from scratch.

`/autoresearch:debug` solves all three: one hypothesis per iteration, systematic falsification, and every hypothesis — confirmed and disproven — logged to `hypotheses.md` and `eliminated.md`.

## The Debug Loop

```
1. Gather symptoms: what exactly is broken? Error message, stack trace, reproduction steps
2. Recon: map the error surface — which files, which paths, which conditions trigger the bug?
3. Hypothesize: ONE specific, testable hypothesis with a prediction
4. Test: design and run exactly ONE experiment to falsify or confirm
5. Classify: confirmed / disproven / inconclusive
6. Log: record the hypothesis, test, evidence, and conclusion
7. Repeat: move to next hypothesis (informed by what was eliminated)
```

The loop terminates when: all hypotheses are classified + a fix is applied, OR `max_iterations` is exhausted.

## The 7 Investigation Techniques

The agent selects from 7 techniques based on the type of bug:

**1. Binary search**: Divide the codebase or input space in half. Narrow down which half contains the bug. Repeat until the exact location is identified. Best for: regressions, "it worked before."

**2. Differential debugging**: Find a version that works, find a version that doesn't. What changed between them? `git bisect` automates this. Best for: "it used to work."

**3. Minimal reproduction**: Strip down the failing case to the smallest possible version that still reproduces the bug. This isolates the exact conditions. Best for: complex multi-component bugs.

**4. Trace execution**: Add logging or use a debugger to trace the exact execution path when the bug occurs. Best for: unexpected state, wrong control flow.

**5. Pattern search**: Search the codebase for similar code patterns. If the bug is in one place, a variant of it may exist elsewhere. Best for: systematic errors, copy-paste bugs.

**6. Working backwards**: Start from the symptom and trace backwards through the call stack. What state is wrong? What call produced that state? Repeat until you find the root cause. Best for: complex state bugs.

**7. Rubber duck**: Explain the bug out loud (to the agent's reasoning process). Articulating the problem in words often reveals the assumption that's wrong. Best for: subtle logic errors.

The agent automatically switches techniques based on progress. If binary search hasn't narrowed the search space after 3 iterations, it switches to trace execution.

## Output Files

Three files capture the debug session:

**`hypotheses.md`**: All hypotheses, their status, and evidence:
```markdown
## H-001 — Database connection pool exhausted
Status: DISPROVEN
Evidence: Pool size is 10, current connections is 3. Not exhausted.
Test: Added logging to connection acquisition — all connections released normally.
Eliminated: 2026-04-20 14:23

## H-002 — Request timeout shorter than database query
Status: CONFIRMED
Evidence: Timeout = 5s. Slow query log shows queries averaging 8.2s.
Test: SET statement_timeout = 30000 in test — all 503s disappeared.
Fix: Increase timeout to 30s, add query optimization for the slow query.
```

**`eliminated.md`**: A clean list of what's been ruled out (fast reference):
```
- Database connection pool exhaustion (H-001)
- Memory leak causing OOM (H-003)
- Load balancer misconfiguration (H-005)
```

**`findings.md`**: Confirmed bugs, reproduction steps, and recommended fixes.

## A Real Example: FastAPI 503 Errors

**Symptom**: POST /users returns 503 intermittently (~30% of the time), no pattern to which requests fail.

**Recon**: 503 means "Service Unavailable." In FastAPI with uvicorn, this can mean: worker crash, timeout, resource exhaustion, or upstream dependency failure.

**H-001**: Worker process crashing due to uncaught exception.
Test: Check uvicorn access logs for worker restart events.
Result: No worker restarts in the past hour. DISPROVEN.

**H-002**: Request timeout — the handler takes longer than the configured timeout.
Test: Add timing middleware. Log request duration for all POST /users calls.
Result: 503 requests all took >5s. Non-503 requests took <1s. CONFIRMED correlation.

**H-003**: Slow requests caused by database query in the hot path.
Test: Add query timing in the handler. Log SQL duration.
Result: `SELECT * FROM users WHERE email = ?` takes 4.8s on first call, 0.1s on subsequent calls.

**Root cause identified**: Missing index on `users.email`. Full table scan on first call (cold cache) takes 4.8s, exceeding the 5s timeout.

**Fix**: `CREATE INDEX idx_users_email ON users(email);`

**Verification**: 1000 POST /users requests after index creation — 0 timeouts, average 0.2s.

This investigation took 4 iterations. Without systematic logging of what was eliminated, it could have taken a day.

## Using `/autoresearch:debug`

```
/autoresearch:debug
Scope: src/api/**/*.ts
Symptom: POST /users returns 503 ~30% of requests
Iterations: 20
```

The agent asks 3 setup questions:
1. What is the symptom? (error message, frequency, reproduction steps)
2. What is the scope? (which files are in-scope for investigation)
3. What constitutes "found"? (when can the loop stop — confirmed root cause, or confirmed root cause + fix applied)

Then it runs the debug loop autonomously, producing `hypotheses.md`, `eliminated.md`, and `findings.md` as it goes.

Chain with fix: `/autoresearch:debug --fix` — after confirming root cause, automatically switches to `/autoresearch:fix` to repair it.

## Key Takeaways

- Scientific debugging requires one hypothesis per iteration, not multi-variable changes
- Falsification is as valuable as confirmation — knowing what *didn't* cause the bug is progress
- The 7 techniques are not sequential — the agent selects based on bug type and switches when stuck
- `eliminated.md` is the most valuable output — it prevents re-investigating dead ends
- Chain `/autoresearch:debug --fix` for a complete investigate-then-repair pipeline
- The permanent record in `hypotheses.md` is institutional knowledge — future developers start where you left off

---

**Next**: [Lecture 06 — Error-Crushing Pipeline](/en/lectures/lecture-06-error-crushing-pipeline/)
