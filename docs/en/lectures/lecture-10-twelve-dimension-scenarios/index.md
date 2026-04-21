# Lecture 10 — 12-Dimension Scenario Exploration

`L01 > L02 > L03 > L04 > L05 > L06 | L07 > L08 > L09 > [ L10 ] L11 > L12`

> *"The happy path is just one of twelve dimensions."* — Systematic scenario coverage catches every class of failure that ad-hoc scenario writing misses.
>
> **Core idea**: How `/autoresearch:scenario` explores the full scenario space across 12 dimensions — one scenario per iteration, domain-aware prioritization, and output formats that chain directly into tests, stories, or security audits.

Code examples: [code/](./code/)  
Practice project: [Project 05 — Security Audit Pipeline](/en/projects/project-05-security-audit-pipeline/)

[中文版本 →](/zh/lectures/lecture-10-twelve-dimension-scenarios/)

---

## The Problem

Features are usually designed for the happy path. When someone asks "what could go wrong?", they write a few obvious cases — invalid input, network failure, unauthorized access — and stop. The entire class of concurrency bugs, temporal failures, and state transition corruptions never gets written.

You can't catch what you don't think to ask about.

## The Solution

```
Feature or system under analysis
         |
    ─────┴──────────────────────────────────
    D1    D2    D3    D4    D5    D6
    Happy  Error  Edge  Abuse  Scale  Concurrency
    path   cond.  case  case
    ─────┬──────────────────────────────────
    D7    D8    D9    D10   D11   D12
    Temporal  Data  Permissions  Integrations  Recovery  State
              variation         (3rd party)             transitions
         |
    One scenario per iteration, cycling through dimensions
         |
    Output: test cases / user stories / threat scenarios
```

## How It Works

**1. The 12 dimensions.**

| # | Dimension | What it catches |
|---|---|---|
| 1 | Happy path | Normal user, expected data, baseline behavior |
| 2 | Error conditions | Network failure, invalid input, service unavailable |
| 3 | Edge cases | Empty input, maximum values, boundary conditions |
| 4 | Abuse cases | Malicious input, injection attempts, enumeration |
| 5 | Scale | 1000× normal load, large datasets, many concurrent users |
| 6 | Concurrency | Race conditions, simultaneous writes, lock contention |
| 7 | Temporal | Long-running ops, stale data, time zone issues |
| 8 | Data variation | Unicode, special characters, nulls, large files |
| 9 | Permissions | Different roles, expired credentials, partial access |
| 10 | Integrations | 3rd-party failures, version mismatches, rate limits |
| 11 | Recovery | Resume after crash, rollback after failure, retry logic |
| 12 | State transitions | Partial completion, interrupted workflows, corruption |

**2. One scenario per iteration — systematic, not random.**

The agent cycles through dimensions in priority order, generating one concrete scenario per iteration. After 25 iterations you have coverage across all 12 dimensions, not 25 variations of the happy path.

**3. Output format determines downstream use.**

```bash
/autoresearch:scenario --format test-scenarios    # pytest / jest test cases
/autoresearch:scenario --format user-stories      # Agile user stories
/autoresearch:scenario --format threat-scenarios  # security threat scenarios
```

Example output (dimension: Concurrency):
```markdown
## Scenario 003 — Concurrent Checkout
Precondition: Two users attempt to checkout the last item simultaneously
Steps:
  1. User A begins checkout
  2. User B begins checkout of same item before A completes
  3. User A completes payment → item marked sold
  4. User B completes payment
Expected: Only one succeeds; other receives "item no longer available"
Risk: Race condition may allow double-selling inventory
```

This scenario wouldn't be written manually — it requires thinking in the "concurrency" dimension.

**4. Domain-specific priorities.**

| Domain | Top dimensions |
|---|---|
| `software` | Error conditions, concurrency, scale, recovery |
| `security` | Abuse cases, permissions, data variation, integrations |
| `product` | Happy path, permissions, temporal |
| `business` | Scale, integrations, recovery, state transitions |

**5. Chain with other commands.**

```bash
/autoresearch:scenario --chain debug     # find bugs in discovered edge cases
/autoresearch:scenario --chain security  # audit discovered threat scenarios
```

## What Changed

| Ad-hoc scenario writing | 12-dimension sweep |
|---|---|
| Same tester, same blind spots, every time | 12 forced dimensions, no dimension skipped |
| Happy path and obvious error cases | Concurrency, temporal, recovery scenarios generated |
| Scenarios live in a notebook | Structured output feeds directly into tests or audits |
| Stop when you run out of ideas | Loop generates until `max_iterations` or all dimensions covered |

## Try It

Run the scenario priority calculator:

```sh
cd docs/en/lectures/lecture-10-twelve-dimension-scenarios/code
python scenario_priority.py software
python scenario_priority.py security
```

Questions to think about:

1. Compare the Top 3 for `software` and `security` — which dimensions appear in both? Which appear in only one?
2. Change the concurrency weight in `software` from `1.5` to `3.0` — how does the ranking change?
3. Add a new domain `"mobile"` to `DOMAIN_WEIGHTS` — which 3-4 dimensions matter most for mobile apps?
4. Pick a feature you built recently. Go through all 12 dimensions and write one concrete scenario for each — which dimension produced the scenario you'd never have written otherwise?

---

**Next**: [Lecture 11 — Universal Ship Pipeline](/en/lectures/lecture-11-universal-ship-pipeline/)
