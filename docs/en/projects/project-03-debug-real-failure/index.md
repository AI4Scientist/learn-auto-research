# Project 03 — Debug a Real Failure


**Paired with**: [Lecture 05](/en/lectures/lecture-05-scientific-debugging/) + [Lecture 06](/en/lectures/lecture-06-error-crushing-pipeline/)  
**Starter code**: [projects/project-03/starter/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-03/starter/)  
**Solution**: [projects/project-03/solution/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-03/solution/)

---

## What You'll Build

Debug a FastAPI service that returns intermittent 503 errors on POST /users. Use `/autoresearch:debug` to investigate, then `/autoresearch:fix` to repair.

## Learning Objectives

- Run a scientific debugging session with falsifiable hypotheses
- Read `hypotheses.md` and `eliminated.md` to understand what was ruled out
- Chain debug → fix with `--from-debug`
- Verify the fix eliminates the symptom

## Starting Point

```
projects/project-03/starter/
├── app/
│   ├── main.py          ← FastAPI app
│   ├── models.py        ← SQLAlchemy models
│   ├── database.py      ← DB connection (has the bug)
│   └── routers/
│       └── users.py     ← User endpoints
├── tests/
│   └── test_users.py    ← integration tests
├── requirements.txt
└── README.md
```

The service works correctly for most requests but ~30% of POST /users requests return 503. The bug is intentionally seeded.

## Step 1 — Reproduce the Bug

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload &

# Run load test
python tests/load_test.py
# Expected: ~30% 503 errors
```

## Step 2 — Debug

```bash
/autoresearch:debug
Scope: app/
Symptom: POST /users returns 503 ~30% of requests
Iterations: 15
```

The agent will investigate the FastAPI app, form hypotheses, and test them one by one.

## Step 3 — Fix

```bash
/autoresearch:fix --from-debug
```

The fix loop reads the confirmed findings from the debug session and repairs the root cause.

## Expected Debug Output

After the debug session, `hypotheses.md` should contain 3–5 hypotheses with evidence. `eliminated.md` should list what was ruled out. `findings.md` should identify the root cause.

## Verification

```bash
python tests/load_test.py
# Expected: 0 503 errors

python -m pytest tests/
# Expected: all tests pass
```

## What the Bug Is (don't read until after debugging)

<details>
<summary>Reveal the bug</summary>

The database connection pool size is set to 2 in `database.py`. Under moderate load, all connections are exhausted, causing new requests to fail with 503. Fix: increase pool size to 10 and add connection timeout handling.

</details>
