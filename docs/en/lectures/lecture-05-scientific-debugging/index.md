# Lecture 05 — Scientific Debugging

`L01 > L02 > L03 > L04 > [ L05 ] L06 | L07 > L08 > L09 > L10 > L11 > L12`

> *"A disproven hypothesis is also progress."* — Knowing what did NOT cause the bug eliminates the search space, just as surely as knowing what did.
>
> **Core idea**: How `/autoresearch:debug` applies the scientific method to bugs — one falsifiable hypothesis per iteration, systematic evidence collection, and a permanent record that future developers can read.

Code examples: [code/](./code/)  
Practice project: [Project 03 — Debug a Real Failure](/en/projects/project-03-debug-real-failure/)


---

## The Problem

Most debugging is archaeological: dig through logs, try multiple things at once, stumble onto the fix without knowing why it worked. Three failure modes:

**Multi-variable changes**: Change three things, bug disappears — but which change fixed it? When the bug comes back, you don't know what to do.

**Confirmation bias**: Test only the hypotheses you believe are true. Evidence piles up on one side. Dead ends go unrecorded.

**Lost knowledge**: When the debugging session ends, failed hypotheses are forgotten. The next developer hits the same bug and starts over.

## The Solution

```
1. Gather symptoms  ← exact error message, reproduction steps, frequency
2. Recon            ← map the error surface: which files, conditions, paths
3. Hypothesize      ← ONE specific, testable hypothesis + prediction
4. Test             ← ONE experiment designed to falsify it
5. Classify         ← confirmed / disproven / inconclusive
6. Log              ← record hypothesis, test, evidence, conclusion
7. Repeat           ← informed by what was eliminated
            ↓
        Terminates when: root cause confirmed + fix applied
                     OR: max_iterations exhausted
```

Every hypothesis goes into `hypotheses.md`. Every eliminated hypothesis goes into `eliminated.md`. Nothing is forgotten.

## How It Works

**1. One hypothesis, one test.**

Good: *"H-002: Request timeout shorter than database query. Prediction: Adding timing middleware will show 503 requests all took >5s."*

Bad: *"Probably the database connection."* (Can't be tested. Can't be falsified.)

**2. Falsification is the goal.**

If H-001 (connection pool exhaustion) is disproven, the search space shrinks. You now know you're not looking for a connection pool problem. Disproven ≠ wasted — it's information.

**3. The 7 investigation techniques.**

The agent selects based on bug type:

| Technique | Best for |
|---|---|
| Binary search | Regressions: "it worked before" |
| Differential (git bisect) | "it used to work" — find the breaking commit |
| Minimal reproduction | Complex multi-component bugs |
| Trace execution | Unexpected state, wrong control flow |
| Pattern search | Systematic errors, copy-paste bugs |
| Working backwards | Complex state bugs: trace from symptom to cause |
| Rubber duck | Subtle logic errors: articulate to reveal the assumption |

If binary search hasn't narrowed the space after 3 iterations, the agent switches technique.

**4. Three output files capture everything.**

```
hypotheses.md   → all hypotheses, status, evidence, conclusion
eliminated.md   → clean list of ruled-out causes (fast reference)
findings.md     → confirmed root causes + reproduction steps + fix
```

**Real example — FastAPI 503 errors:**

```
Symptom: POST /users returns 503 ~30% of requests

H-001: Worker crash     → check uvicorn logs → no restarts → DISPROVEN
H-002: Request timeout  → add timing middleware → 503 requests all >5s → CONFIRMED
H-003: Slow DB query    → add SQL timing → SELECT * FROM users took 4.8s cold → CONFIRMED

Root cause: missing index on users.email
Fix: CREATE INDEX idx_users_email ON users(email)
Verification: 1000 requests after index → 0 timeouts, avg 0.2s
```

4 iterations. Without systematic hypothesis tracking, this was a day of work.

## What Changed

| Traditional debugging | Scientific debugging |
|---|---|
| Change multiple things at once | One hypothesis, one test per iteration |
| Failed approaches forgotten | Every disproven hypothesis in `eliminated.md` |
| Bug fix = mystery | Root cause documented in `findings.md` |
| Next developer starts over | Next developer reads `hypotheses.md` and continues |

## Try It

Run the hypothesis tracker and falsification loop:

```sh
cd docs/en/lectures/lecture-05-scientific-debugging/code
python hypothesis_tracker.py
python falsification_loop.py
```

Questions to think about:

1. After running `hypothesis_tracker.py`, how many hypotheses are in each status (confirmed / disproven / inconclusive)?
2. What's in `eliminated.md`? Why does this file exist separately from `hypotheses.md`?
3. In the FastAPI 503 example, why was H-001 worth testing first even though it turned out to be wrong?
4. Think of a bug you've encountered — write 3 hypotheses for it in the format: `H-00N: [cause]. Prediction: [observable evidence if true].`

---

**Next**: [Lecture 06 — Error-Crushing Pipeline](/en/lectures/lecture-06-error-crushing-pipeline/)
