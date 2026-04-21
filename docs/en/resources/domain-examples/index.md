# Domain Examples

Worked examples showing autoresearch applied across different domains. Each example shows the `research.md` setup and the key results.

## Code Optimization

**Goal**: Reduce sort function execution time to under 0.5s on 1M integers  
**Result**: 2.12s → 0.15s (−93%) in 5 iterations

```markdown
# research.md excerpt
Metric: median_time_s, minimize, target: < 0.5
Evaluator: python benchmark.py
Guard: python -m pytest test_sort.py
Noise runs: 3

History highlights:
| 1 | radix sort base 256     | 0.871 | keep |
| 2 | radix sort base 65536   | 0.573 | keep |
| 3 | numpy sort              | 0.612 | discard |
| 4 | micro-optimized radix   | 0.498 | keep ✓ |
```

## Function Fitting (ML)

**Goal**: Find hidden function with RMSE < 0.05  
**Result**: RMSE 2.11 → 0.030 (−99%) in 12 iterations

```markdown
# research.md excerpt
Metric: rmse, minimize, target: < 0.05
Evaluator: python evaluate.py
Noise runs: 1 (deterministic)

Key pivot: After 3 non-improving polynomial iterations (L1 pivot),
switched to interaction terms. log(x₁) * x₂ term reduced RMSE from 0.28 → 0.12.
```

## Test Coverage

**Goal**: Increase test coverage from 62% to 85%  
**Result**: 62% → 87% in 18 iterations

```markdown
# research.md excerpt
Metric: coverage_pct, maximize, target: > 85
Evaluator: coverage run -m pytest && coverage report --format=total
Guard: python -m pytest (all existing tests must keep passing)
```

## API Performance

**Goal**: Reduce p95 latency from 340ms to under 100ms  
**Result**: 340ms → 88ms (−74%) in 9 iterations

```markdown
# research.md excerpt
Metric: p95_ms, minimize, target: < 100
Evaluator: python load_test.py --requests 100 --output p95
Guard: python -m pytest tests/functional/
```

## Prompt Engineering

**Goal**: Improve LLM judge score for a summarization prompt from 5.2 to 8.0  
**Result**: 5.2 → 8.4 (+62%) in 11 iterations

```markdown
# research.md excerpt
Metric: llm_judge_score, maximize, target: > 8.0
Evaluator: python judge.py  # calls claude-haiku-4-5-20251001, averages 5 samples
Noise runs: 5  # LLM scores are noisy
Min delta: 0.2  # only keep improvements of 0.2+ points
Scope: prompt.txt only
```

## Literature Review

**Goal**: Find all papers on "autonomous agent evaluation" — target 20 papers  
**Result**: 3 → 19 papers in 8 iterations

```markdown
# research.md excerpt
Metric: papers_found, maximize, target: >= 20
Evaluator: python count_papers.py  # counts unique papers in papers.md
Scope: search_strategy.md (modify search queries, not the papers file)

Key insight: Switching from keyword search to citation graph traversal
(L1 pivot at iteration 5) found 8 more papers.
```

## Security Hardening

**Goal**: Fix all Critical and High security findings  
**Result**: 3 Critical + 5 High → 0 Critical + 0 High in 12 iterations

```markdown
# Command chain used:
/autoresearch:security  # identify all findings
/autoresearch:fix --category security --guard "pytest tests/"

# research.md for the fix loop
Metric: open_critical_high_count, minimize, target: == 0
Evaluator: python count_findings.py security/latest/findings.md
```
