---
name: autoresearch source materials summary
description: Summary of all three autoresearch reference repos used as teaching material for Learn AutoResearch
type: project
---

# AutoResearch Source Materials

## Three Repos Overview

### 1. `autoresearch/` — Karpathy's Original Concept
Minimal ML training loop. The intellectual origin of the entire approach.

Key files:
- `prepare.py` (read-only): Data prep, tokenizer, constants, eval utils
- `train.py` (agent modifies): Model arch, optimizer, training loop
- `program.md`: Agent directives, rules, output format
- `results.tsv`: Tab-separated results log

Core mechanic:
1. Modify `train.py`
2. Commit changes
3. Run training (exactly 5 min budget)
4. Log results (commit hash, metric `val_bpb`, memory, status, description)
5. Keep if improved, revert if not
6. Iterate

**Metric**: `val_bpb` (validation bits per byte, lower = better)

---

### 2. `autoresearch_alt/` — Generalized Multi-Platform Version
Extends Karpathy's concept beyond ML to ANY domain. Authored by uditgoenka.

**Multi-platform support:**
- `.claude/` — Claude Code (canonical source)
- `.agents/` — OpenAI Codex
- `.opencode/` — OpenCode
- `claude-plugin/` — Plugin marketplace package

**10 commands:**
| Command | Purpose |
|---------|---------|
| `/autoresearch` | Core 5-stage loop (modify → verify → keep/discard → repeat) |
| `/autoresearch:plan` | 7-step interactive wizard → writes `research.md` |
| `/autoresearch:debug` | Scientific bug hunting with falsifiable hypotheses |
| `/autoresearch:fix` | Cascade-aware error crusher, stops at 0 errors |
| `/autoresearch:security` | STRIDE + OWASP iterative audit |
| `/autoresearch:scenario` | 12-dimension scenario exploration |
| `/autoresearch:predict` | Multi-persona deliberation (5 experts, anti-herd) |
| `/autoresearch:learn` | Autonomous documentation engine |
| `/autoresearch:reason` | Adversarial refinement with blind-judge panel |
| `/autoresearch:ship` | 8-phase universal shipping workflow |

**8 Critical Rules:**
1. Loop until done (unbounded: forever; bounded: N times)
2. Read before write
3. One change per iteration
4. Mechanical verification only (no subjective judgment)
5. Automatic rollback on failure
6. Simplicity wins (equal result + less code = KEEP)
7. Git is memory (experiments committed with `experiment:` prefix)
8. When stuck, think harder (3-level pivot: 3 non-improving → switch, 5 → paradigm shift)

**Results TSV format:**
```
iteration  commit   metric  delta   status    description
0          a1b2c3d  85.2    0.0     baseline  initial state
1          b2c3d4e  87.1    +1.9    keep      add tests for auth edge cases
```

**Command chaining patterns:**
```
plan ──> autoresearch ──> ship
debug ──> fix ──> ship
predict ──> debug / security / fix
security ──> fix ──> security (re-audit)
reason ──> plan ──> autoresearch
```

---

### 3. `autoresearch-skill/` — Production-Ready Skill Package
Same functionality as autoresearch_alt, packaged as installable skill.

**Installation:**
```bash
git clone https://github.com/wjgoarxiv/autoresearch-skill ~/.claude/plugins/autoresearch-skill
ln -s ~/.claude/plugins/autoresearch-skill/SKILL.md ~/.claude/skills/autoresearch.md
```

**Guide directory (14 files):**
- `getting-started.md` — 60-second quickstart
- `autoresearch.md` — core loop reference
- `plan.md` — setup wizard
- `predict.md` — multi-persona prediction
- `debug.md` — scientific bug hunting
- `fix.md` — iterative error repair
- `scenario.md` — 12-dimension exploration
- `reason.md` — adversarial refinement
- `security.md` — STRIDE + OWASP audit
- `ship.md` — universal shipping workflow
- `chains-and-combinations.md`
- `advanced-patterns.md`

**Examples directory (4 worked examples):**
1. `code-optimization/` — sort 2.12s → 0.15s (−93%)
2. `function-fitting/` — RMSE 2.11 → 0.030 (−99%)
3. `skill-elaboration/` — composite score 0.28 → 0.98 (+255%)
4. `literature-review/` — 8 categories, 19 papers

**5-Stage Core Loop:**
1. **Understand**: Read `research.md`, load goal/metric/constraints/history
2. **Hypothesize**: Propose ONE specific, testable change
3. **Experiment**: Execute the change (wrap in `timeout 5m`)
4. **Evaluate**: Run evaluator → `{"pass": bool, "score": number}` → apply keep policy
5. **Log & Iterate**: Append to `research.md`, `research_log.md`, `autoresearch-results.tsv`, update `progress.png` → loop

**Evaluator contract:** `{"pass": true, "score": 0.94}`

**Output files per research session:**
- `research.md` — full history with metric values
- `research_log.md` — detailed experiment notes
- `progress.png` — convergence plot
- `autoresearch-results.tsv` — machine-readable (8 columns)
- `final_report.md` — summary + next steps

---

## Metric Cheat Sheet (Key Domains for Tutorial)

| Domain | Metric | Direction |
|--------|--------|-----------|
| Code performance | `median_time_s` | minimize |
| ML accuracy | `accuracy` | maximize |
| Bundle size | `bundle_kb` | minimize |
| Prompt quality | `llm_judge_score` | maximize |
| Literature coverage | `papers_found` | maximize |
| API latency | `p95_ms` | minimize |
| Test coverage | `coverage_pct` | maximize |
| RMSE | `rmse` | minimize |
| LLM judge score | `score_1_10` | maximize |

---

## Ultimate Purpose

The goal is to make **specific research automated** — autoresearch is the mechanism. The tutorial teaches:
1. How to define a measurable research goal
2. How to set up the autonomous loop
3. How to interpret and act on results
4. How to extend the loop to new domains and scenarios
5. How to chain commands for complex research pipelines

**Why:** Automated research = compounding gains overnight. One agent, one metric, one loop = 100 experiments per night.
