# Project 04 — Architecture Decision Debate

[中文版本 →](/zh/projects/project-04-architecture-debate/)

**Paired with**: [Lecture 07](/en/lectures/lecture-07-five-expert-predict/) + [Lecture 08](/en/lectures/lecture-08-adversarial-refinement/)  
**Starter code**: [projects/project-04/starter/](https://github.com/zhimin-z/learn-auto-research/tree/main/projects/project-04/starter/)  
**Solution**: [projects/project-04/solution/](https://github.com/zhimin-z/learn-auto-research/tree/main/projects/project-04/solution/)

---

## What You'll Build

Use `/autoresearch:predict` and `/autoresearch:reason` to decide between two database architectures for an order management system. Then use the converged decision to scaffold a validation experiment with `/autoresearch:plan`.

## Learning Objectives

- Run a 5-expert prediction analysis and identify minority views
- Run an adversarial refinement loop until convergence
- Read `lineage.md` to understand how the debate evolved
- Chain `reason → plan` to validate the decision empirically

## The Decision

Your order management system processes 10,000 orders/day with complex queries and frequent updates. You need to choose between:

**Option A — CQRS with Event Sourcing**: Commands write events, queries read projections. Full audit trail. Complex implementation.

**Option B — Traditional CRUD with Audit Log**: Simple reads and writes. Audit log table appended on writes. Much simpler to implement.

## Step 1 — Five-Expert Analysis

```bash
/autoresearch:predict
Scope: projects/project-04/starter/
Task: Choose between CQRS+EventSourcing vs CRUD+AuditLog for order management
```

Read the output. Note: which persona raises the most concerns? Is there a minority view that the others dismiss?

## Step 2 — Adversarial Refinement

```bash
/autoresearch:reason
Task: Should we use event sourcing for our order management system?
Domain: software
Iterations: 8
Convergence: 3
```

Watch the debate evolve. After 8 iterations (or earlier if convergence is reached), read `lineage.md` to see how the position evolved round by round.

## Step 3 — Scaffold Validation

```bash
/autoresearch:plan
Goal: Validate the winning architecture with a performance benchmark
```

Use the converged decision from Step 2 as input. The plan wizard will help you define a metric that empirically validates which architecture performs better for your specific load pattern.

## Expected Output

```
reason/{date}-order-management/
├── lineage.md          ← round-by-round evolution
├── candidates.md       ← all candidate positions
├── judge-transcripts.md ← what each judge said
├── reason-results.tsv  ← machine-readable results
└── handoff.json        ← structured output for chaining
```

## Key Question to Answer

After completing the debate: did the adversarial process change your initial intuition? Which argument in `lineage.md` was the most decisive turning point?
