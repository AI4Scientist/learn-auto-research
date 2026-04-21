# Lecture 11 — Universal Ship Pipeline

`L01 > L02 > L03 > L04 > L05 > L06 | L07 > L08 > L09 > L10 > [ L11 ] L12`

> *"Human confirmation is required exactly once — before every irreversible action."* — Everything before Phase 6 is automated. Everything after is logged.
>
> **Core idea**: How `/autoresearch:ship` takes any artifact from "ready" to "deployed" through an 8-phase pipeline with one mandatory human gate and automatic rollback.

Code examples: [code/](./code/)  
Practice project: [Project 06 — End-to-End Research Project](/en/projects/project-06-end-to-end-research/)


---

## The Problem

Shipping without a checklist means something always gets skipped: tests weren't run, the PR description is empty, the database migration isn't ready, no one documented the rollback procedure. The more confident you feel about a change, the more likely you are to skip the checks.

And when something goes wrong after shipping, there's no record of what was shipped or how to undo it.

## The Solution

```
Phase 1: Identify    ← auto-detect what's being shipped (or --type to override)
Phase 2: Inventory   ← list everything that needs to ship
Phase 3: Checklist   ← generate domain-specific, mechanically verifiable checks
Phase 4: Prepare     ← build, test, changelog, version bump
Phase 5: Dry-run     ← simulate ship action without committing
Phase 6: ─── CONFIRM ───  ← MANDATORY HUMAN GATE (only human input in the pipeline)
Phase 7: Ship        ← execute the actual ship action
Phase 8: Verify+Log  ← post-ship health check → write ship-log.md
```

If all checks pass and `--auto` is set, Phase 6 auto-approves. Otherwise it always asks.

## How It Works

**1. Checklists are mechanically verifiable — no subjective items.**

For `code-pr`:
```markdown
- [ ] All tests passing (npm test)          ← exit code 0 = pass
- [ ] No TypeScript errors (tsc --noEmit)   ← exit code 0 = pass
- [ ] No lint errors (eslint src/)          ← exit code 0 = pass
- [ ] PR description written
- [ ] Breaking changes documented
```

No "looks good to me." Every item either passes its command or doesn't.

**2. Nine ship types cover everything.**

| Type | What it does |
|---|---|
| `code-pr` | Push branch, create PR, request reviewers |
| `code-release` | Bump version, generate changelog, tag, GitHub release |
| `deployment` | Build, push container, deploy, health check |
| `content` | Validate, publish to CMS or static host, verify URL live |
| `marketing-email` | Final review, schedule send, verify unsubscribe link |
| `marketing-campaign` | Multi-channel launch checklist |
| `sales` | CRM update, email send, follow-up scheduling |
| `research` | Package findings, upload to archive, notify stakeholders |
| `design` | Export assets, upload to shared drive, notify design system |

**3. Rollback is always available.**

Every ship action is logged in `ship-log.md` with enough information to undo it:

```bash
/autoresearch:ship --rollback
```

For `code-pr`: deletes the branch. For `deployment`: runs `kubectl rollout undo`. For `content`: reverts to previous version.

**4. Key flags.**

| Flag | Purpose |
|---|---|
| `--dry-run` | Validate everything, don't actually ship |
| `--auto` | Auto-approve Phase 6 if all checks pass |
| `--rollback` | Undo the last ship action |
| `--checklist-only` | Check readiness only, don't proceed |

## What Changed

| Manual shipping | Ship pipeline |
|---|---|
| Checklist exists in someone's head | Domain-specific checklist generated automatically |
| "Subjective: looks good" | Every check is exit code 0 or not |
| Rollback procedure: "figure it out" | `--rollback` always available, logged in ship-log.md |
| No record of what was shipped | `ship-log.md` records every ship action with timestamp |

## Try It

Run the ship checklist and rollback trigger:

```sh
cd docs/en/lectures/lecture-11-universal-ship-pipeline/code
python ship_checklist.py code-pr
python ship_checklist.py content
python rollback_trigger.py
```

Questions to think about:

1. After running `ship_checklist.py content`, did all checks pass? If not, what failed and why?
2. Add a new check to `CHECKLISTS["code-pr"]`: verify no `.pyc` files exist in the current directory. What command does this check run?
3. After running `ship_checklist.py code-pr` and then `rollback_trigger.py` — what rollback command is shown? Does it match the ship type?
4. If `ship-log.md` doesn't exist when `rollback_trigger.py` runs, what happens? What does this tell you about the precondition for rollback?

---

**Next**: [Lecture 12 — Overnight Runs & Advanced Patterns](/en/lectures/lecture-12-overnight-runs-advanced/)
