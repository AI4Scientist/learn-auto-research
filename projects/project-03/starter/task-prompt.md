# Task — Project 03: Debug a Real Failure

## Goal
Fix all 3 bugs in `app.py` so that all 6 tests in `test_app.py` pass.

## Current State
`app.py` has 3 intentional bugs:
1. `parse_request` raises `KeyError` when `user_id` is missing (should default to `"anonymous"`)
2. `parse_request` accepts negative amounts (should raise `ValueError`)
3. `parse_request` returns `None` for missing `items` (should return `[]`)

## Constraints
- Only modify `app.py`
- Do not modify `test_app.py` or `evaluate.py`
- Use Python stdlib only

## Metric
`test_pass_rate` — maximize — target `== 1.0` (all 6 tests pass)

## Scientific Debugging Approach
Use the 5-stage loop's debugging mode:
1. Identify which test fails first
2. Form a hypothesis about the root cause
3. Make the minimal fix
4. Re-run and verify
5. Repeat until all tests pass
