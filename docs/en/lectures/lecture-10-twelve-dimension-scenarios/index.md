# Lecture 10 — 12-Dimension Scenario Exploration

[中文版本 →](/zh/lectures/lecture-10-twelve-dimension-scenarios/)

Code examples: [code/](./code/)  
Practice project: [Project 05 — Security Audit Pipeline](/en/projects/project-05-security-audit-pipeline/)

---

Features are usually designed for the happy path. `/autoresearch:scenario` explores the full scenario space — 12 dimensions of situation diversity — systematically and autonomously.

## The 12 Dimensions

Every feature or system can be analyzed across 12 dimensions. The scenario loop generates ONE situation per iteration across these dimensions, ensuring comprehensive coverage:

| # | Dimension | Examples |
|---|-----------|---------|
| 1 | **Happy path** | Normal user, normal data, expected behavior |
| 2 | **Error conditions** | Network failure, invalid input, service unavailable |
| 3 | **Edge cases** | Empty input, maximum values, boundary conditions |
| 4 | **Abuse cases** | Malicious input, injection attempts, enumeration attacks |
| 5 | **Scale** | 1000× normal load, large datasets, many concurrent users |
| 6 | **Concurrency** | Race conditions, simultaneous writes, lock contention |
| 7 | **Temporal** | Long-running operations, stale data, time zone issues |
| 8 | **Data variation** | Unicode, special characters, null values, large files |
| 9 | **Permissions** | Different roles, expired credentials, partial access |
| 10 | **Integrations** | Third-party API failures, version mismatches, rate limits |
| 11 | **Recovery** | Resume after crash, rollback after failure, retry logic |
| 12 | **State transitions** | Partial completion, interrupted workflows, state corruption |

## Output Formats

The scenario output is designed to feed directly into other tools:

```bash
/autoresearch:scenario --format test-scenarios    # pytest/jest test cases
/autoresearch:scenario --format user-stories      # Agile user stories
/autoresearch:scenario --format use-cases         # formal use case documents
/autoresearch:scenario --format threat-scenarios  # security threat scenarios
```

For `test-scenarios` format, each scenario becomes a test case with: preconditions, steps, expected outcome, and actual outcome (to be filled by running the test).

## Domain-Specific Priorities

Different domains prioritize different dimensions:

| Domain | Top dimensions |
|--------|---------------|
| `software` | error conditions, concurrency, scale, recovery |
| `security` | abuse cases, permissions, data variation, integrations |
| `product` | happy path, user stories, permissions, temporal |
| `business` | scale, integrations, recovery, state transitions |

## Chaining Scenarios

The scenario output chains directly to investigation and auditing:

```bash
# Find bugs in discovered edge cases
/autoresearch:scenario --chain debug

# Audit discovered threat scenarios for security vulnerabilities
/autoresearch:scenario --chain security
```

## Quick Example: Checkout Flow

```
/autoresearch:scenario
Scenario: User attempts to checkout with multiple payment methods
Iterations: 25
Domain: software
Format: test-scenarios
```

The agent generates 25 scenarios across all 12 dimensions. Sample output:

```markdown
## Scenario 003 — Concurrent Checkout (Dimension: Concurrency)
Precondition: Two users attempt to checkout the last item simultaneously
Steps: 
  1. User A begins checkout
  2. User B begins checkout of same item before A completes
  3. User A completes payment
  4. User B completes payment
Expected: Only one checkout succeeds; other receives "item no longer available"
Risk: Race condition may allow double-selling inventory
```

This scenario wouldn't be written manually — it requires thinking in the "concurrency" dimension. The systematic 12-dimension sweep catches what ad-hoc scenario writing misses.

## Key Takeaways

- 12 dimensions provide systematic coverage of the scenario space
- One scenario per iteration — methodical, not random
- Output format determines downstream use (tests, stories, threats)
- Domain-specific dimension priorities tune the coverage toward what matters most
- Chain with debug and security for a complete quality pipeline

---

**Next**: [Lecture 11 — Universal Ship Pipeline](/en/lectures/lecture-11-universal-ship-pipeline/)
