# Reference

## Command Quick-Decision Guide

| I want to... | Command |
|-------------|---------|
| Set up a new research project | `/autoresearch:plan` |
| Run the optimization loop | `/autoresearch` |
| Run exactly N iterations | `/autoresearch` + `Iterations: N` inline |
| Investigate why something is broken | `/autoresearch:debug` |
| Fix all errors automatically | `/autoresearch:fix` |
| Debug then auto-fix | `/autoresearch:debug --fix` |
| Get expert opinions before acting | `/autoresearch:predict` |
| Converge on a decision without a metric | `/autoresearch:reason` |
| Audit for security vulnerabilities | `/autoresearch:security` |
| Explore edge cases and scenarios | `/autoresearch:scenario` |
| Generate documentation | `/autoresearch:learn` |
| Deploy or publish a finished artifact | `/autoresearch:ship` |

## Metric Cheat Sheet

| Domain | Metric | Direction | Evaluator snippet |
|--------|--------|-----------|------------------|
| Code performance | `median_time_s` | minimize | `timeit` 3 runs, median |
| ML accuracy | `accuracy` | maximize | `sklearn.metrics.accuracy_score` |
| Bundle size | `bundle_kb` | minimize | `du -sk dist/ \| cut -f1` |
| Prompt quality | `llm_judge_score` | maximize | LLM rates 1–10, average N=5 |
| Literature coverage | `papers_found` | maximize | Count matched papers |
| API latency | `p95_ms` | minimize | 100 requests, 95th percentile |
| Memory usage | `peak_mb` | minimize | `/usr/bin/time -v` |
| Test coverage | `coverage_pct` | maximize | `coverage run -m pytest` |
| RMSE | `rmse` | minimize | `sqrt(mean_squared_error)` |
| Security coverage | `fixed_pct` | maximize | Fixed / total findings |
| Query speed | `query_ms` | minimize | `EXPLAIN ANALYZE` execution time |
| LLM judge | `score_1_10` | maximize | Blind 1–10, N=5 samples |
| Compression | `ratio` | maximize | `original_bytes / compressed_bytes` |
| Translation | `bleu_score` | maximize | `sacrebleu` vs references |
| Simulation | `rmsd` | minimize | RMSD vs reference coordinates |

## Evaluator Contract

Every evaluator must output exactly:
```json
{"pass": true, "score": 0.94}
```

- `pass`: `true` if the target is met, `false` otherwise
- `score`: the metric value for this iteration (float)
- Exit code: `0` on success, non-zero on evaluation failure
- Timeout: wrap with `timeout 5m python evaluate.py`

## 8 Critical Rules

| # | Rule |
|---|------|
| 1 | **Loop until done** — unbounded: forever. Bounded: N times then summarize |
| 2 | **Read before write** — understand full context + git history before modifying |
| 3 | **One change per iteration** — atomic changes. If it breaks, you know why |
| 4 | **Mechanical verification only** — no subjective "looks good." Use metrics |
| 5 | **Automatic rollback** — failed changes revert instantly via git |
| 6 | **Simplicity wins** — equal results + less code = KEEP |
| 7 | **Git is memory** — read `git log` + `git diff` before each iteration |
| 8 | **When stuck, think harder** — L1/L2/L3 pivot strategy |

## Command Chaining Patterns

```
plan ──> autoresearch ──> ship           Core research pipeline
debug ──> fix ──> ship                   Bug fix pipeline
predict ──> debug / security / fix       Risk-aware pipeline
security ──> fix ──> security            Security hardening loop
reason ──> plan ──> autoresearch         Decision → validation
scenario ──> debug                       Edge case → bug hunt
scenario ──> security                    Threat scenario → audit
```

## Guard Patterns

| Goal | Guard command |
|------|--------------|
| Prevent test regressions | `python -m pytest` |
| Prevent type errors | `mypy src/` or `tsc --noEmit` |
| Prevent lint regressions | `flake8 src/` or `eslint src/` |
| Prevent correctness regression | `python -m pytest tests/correctness/` |
| Prevent API contract changes | `python tests/contract_test.py` |

## Crash Recovery Reference

| Failure | Response |
|---------|----------|
| Syntax error | Fix immediately, don't count as iteration |
| Runtime error | Attempt fix (max 3 tries), then move on |
| Timeout (exit 124) | Revert, log TIMEOUT, try smaller variant |
| Resource exhaustion | Revert, try smaller variant next iteration |
| External dependency | Skip, log, try different approach |
| Guard failure | Attempt fix-of-fix (max 2 tries), else revert |
