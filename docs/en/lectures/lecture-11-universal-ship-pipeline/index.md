# Lecture 11 — Universal Ship Pipeline

[中文版本 →](/zh/lectures/lecture-11-universal-ship-pipeline/)

Code examples: [code/](./code/)  
Practice project: [Project 06 — End-to-End Research Project](/en/projects/project-06-end-to-end-research/)

---

Research is only complete when the result is shipped. `/autoresearch:ship` is an 8-phase pipeline that takes any artifact from "ready" to "deployed" with one mandatory human confirmation gate before any irreversible action.

## The 8 Phases

```
Identify → Inventory → Checklist → Prepare → Dry-run → CONFIRM → Ship → Verify → Log
```

**Phase 1 — Identify**: Auto-detect what's being shipped. The agent reads the codebase, git status, and file types to determine the ship type. Overrideable with `--type`.

**Phase 2 — Inventory**: List everything that needs to ship. For a code PR: changed files, tests, documentation. For a blog post: content, images, metadata. For a deployment: build artifacts, environment configs, migration scripts.

**Phase 3 — Checklist**: Generate a domain-specific checklist. Every item is mechanically verifiable — no subjective judgments.

**Phase 4 — Prepare**: Run pre-ship preparation. Build artifacts, run tests, generate changelogs, update version numbers.

**Phase 5 — Dry-run**: Simulate the ship action without committing. For a PR: `git push --dry-run`. For a deployment: `kubectl apply --dry-run`.

**Phase 6 — CONFIRM** (mandatory human gate): Show the inventory, checklist results, and dry-run output. Ask for explicit confirmation before proceeding. This is the only phase that requires human input. If all checks pass and `--auto` is set, this gate auto-approves.

**Phase 7 — Ship**: Execute the actual ship action.

**Phase 8 — Verify + Log**: Confirm the ship succeeded. Run post-ship health checks. Log the result to `ship-log.md`.

## The 9 Ship Types

| Type | What it does |
|------|-------------|
| `code-pr` | Push branch, create PR with description, request reviewers |
| `code-release` | Bump version, generate changelog, tag, create GitHub release |
| `deployment` | Build, push container, deploy to environment, health check |
| `content` | Validate, publish to CMS or static host, verify URL live |
| `marketing-email` | Final review, schedule send, verify unsubscribe link |
| `marketing-campaign` | Multi-channel launch checklist (paid, social, email) |
| `sales` | CRM update, email send, follow-up scheduling |
| `research` | Package findings, upload to archive, notify stakeholders |
| `design` | Export assets, upload to shared drive, notify design system |

## Domain-Specific Checklists

Each ship type generates a different checklist. For `code-pr`:

```markdown
Pre-ship checklist:
- [ ] All tests passing (npm test)
- [ ] No TypeScript errors (tsc --noEmit)
- [ ] No lint errors (eslint src/)
- [ ] PR description written
- [ ] Breaking changes documented
- [ ] Migration notes included (if schema change)
```

For `deployment`:
```markdown
Pre-ship checklist:
- [ ] Build succeeds (docker build)
- [ ] All tests passing in CI
- [ ] Environment variables set
- [ ] Database migrations ready
- [ ] Rollback procedure documented
- [ ] Health check endpoint exists
- [ ] Monitoring alerts configured
```

## Key Flags

| Flag | Purpose |
|------|---------|
| `--dry-run` | Validate everything but don't ship |
| `--auto` | Auto-approve if all checks pass |
| `--force` | Skip non-critical items (blockers still enforced) |
| `--rollback` | Undo last ship action |
| `--monitor N` | Post-ship monitoring for N minutes |
| `--checklist-only` | Just check readiness, don't proceed |

## Rollback

Every ship action is logged with enough information to roll back:

```bash
/autoresearch:ship --rollback
```

For code-pr: deletes the branch. For deployment: runs `kubectl rollout undo`. For content: reverts to previous version.

The `ship-log.md` contains the complete record of every ship action for the session.

## Key Takeaways

- 8 phases from identification to logging provide complete coverage
- The mandatory human confirmation gate (Phase 6) is the only point that requires human input
- 9 ship types cover everything from code PRs to marketing campaigns
- Checklists are mechanically verifiable — no subjective "looks good"
- `--rollback` makes every ship action reversible
- Chain from the full research pipeline: plan → autoresearch → debug → fix → security → ship

---

**Next**: [Lecture 12 — Overnight Runs & Advanced Patterns](/en/lectures/lecture-12-overnight-runs-advanced/)
