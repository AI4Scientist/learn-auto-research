---
name: Learn AutoResearch curriculum plan
description: Full curriculum plan for the Learn AutoResearch tutorial, organized by difficulty, covering all autoresearch commands and applications
type: project
---

# Learn AutoResearch — Curriculum Plan

## Course Goal

Teach students how to **automate specific research** using the autoresearch framework — from first principles (Karpathy's ML loop) to production-ready multi-domain autonomous research pipelines.

By the end, students can:
- Define any measurable research problem
- Set up and run an autonomous improvement loop overnight
- Debug, fix, and ship research artifacts autonomously
- Extend the framework to new domains
- Chain commands for complex multi-phase research

---

## Curriculum Overview (12 Lectures + 6 Projects)

### Phase 1 — 理解原理 (Why AutoResearch Works)
**L01 + L02 → P01**

**L01: 为什么手动迭代会失败 — Karpathy的顿悟**
- The original problem: ML researchers iterate slowly (1–3 experiments/day)
- Karpathy's insight: constraint + metric + loop = 100 experiments/night
- Key analogy: evolution vs. intelligent design — both need selection pressure
- Core loop anatomy: modify → verify → keep/discard → commit → repeat
- What makes autoresearch different from scripted hyperparameter search

**L02: 什么是可测量的研究目标**
- The "metric trap": when your metric doesn't capture what you care about
- How to decompose a vague goal into a mechanical metric
- The keep policy: score_improvement vs. always_keep vs. human_review
- Guard patterns: protecting invariants while optimizing metrics
- The `research.md` contract: goal, metric, constraints, history

**P01: 你的第一个研究循环**
- Task: Optimize a Python sort function from >2s to <0.5s on 1M integers
- Uses: `/autoresearch:plan` to scaffold, `/autoresearch` to run
- Learning: metric definition, evaluator writing, loop observation

---

### Phase 2 — 掌握核心循环 (Master the Core Loop)
**L03 + L04 → P02**

**L03: 5阶段循环的内部机制**
- Stage 1 (Understand): Why reading git history matters before every iteration
- Stage 2 (Hypothesize): One change per iteration — the atomic unit of research
- Stage 3 (Experiment): Timeouts, crash recovery, automatic rollback
- Stage 4 (Evaluate): The evaluator contract `{"pass": bool, "score": number}`
- Stage 5 (Log & Iterate): TSV format, progress.png, when to stop

**L04: 被卡住时怎么办 — 3级pivot策略**
- L1 pivot (3 consecutive non-improving): switch strategy within paradigm
- L2 pivot (5 consecutive non-improving): paradigm shift
- L3 pivot (max iterations reached): final_report.md + recommendations
- Anti-patterns: why "try everything" fails; why "one hypothesis per iteration" wins
- Noise handling: `noise_runs: 3`, `min_delta`, statistical significance

**P02: 从基线到最优 — 函数拟合实验**
- Task: Find the hidden mathematical function (RMSE 2.11 → <0.05)
- Uses: `/autoresearch` with custom evaluate.py
- Learning: evaluator design, pivot strategies, reading research logs

---

### Phase 3 — 调试与修复 (Debug & Fix)
**L05 + L06 → P03**

**L05: 科学方法调试 — 可证伪的假设**
- Why most debugging is slow: "try things until something works"
- The falsification loop: propose hypothesis → design test → disprove or confirm
- 7 investigation techniques: binary search, differential debugging, minimal reproduction, trace execution, pattern search, working backwards, rubber duck
- How `/autoresearch:debug` operationalizes this
- Reading the `hypotheses.md`, `eliminated.md`, `findings.md` outputs

**L06: 错误归零 — 自动修复流水线**
- The cascade problem: fixing one error creates three more
- How `/autoresearch:fix` handles error ordering (blockers first)
- Guard + fix: ensuring regressions don't occur during repair
- Chaining: `debug → fix → ship`
- When to use `--from-debug` flag

**P03: 调试一个真实的故障系统**
- Task: Debug a FastAPI service with intermittent 503 errors
- Uses: `/autoresearch:debug` → `/autoresearch:fix`
- Learning: hypothesis-driven investigation, evidence-based debugging

---

### Phase 4 — 多视角与预测 (Predict & Reason)
**L07 + L08 → P04**

**L07: 5专家视角 — 行动前的预判**
- Why single-perspective analysis misses critical issues
- The 5 personas: Architect, Security Analyst, Performance Engineer, Reliability Engineer, Devil's Advocate
- Anti-herd detection: why independent analysis matters
- Output structure: findings, consensus, dissent, recommended actions
- Chaining predict → debug/security/fix

**L08: 对抗性精炼 — 当没有客观指标时**
- The challenge of subjective domains (architecture decisions, content quality)
- The blind judge panel as fitness function (val_bpb for decisions)
- Iteration: Generate-A → Critic attacks → Author-B responds → Synthesize → Judge → Repeat
- Convergence criteria: N consecutive wins
- Use cases: architecture decisions, product strategy, content quality

**P04: 架构决策的自动化辩论**
- Task: Use reason to decide between two database architectures
- Uses: `/autoresearch:predict` + `/autoresearch:reason`
- Learning: subjective domains, adversarial refinement, convergence

---

### Phase 5 — 安全与场景探索 (Security & Scenarios)
**L09 + L10 → P05**

**L09: STRIDE + OWASP 自动安全审计**
- What STRIDE covers: Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation
- OWASP Top 10 sweep integration
- Red team personas (4 hostile actors)
- Evidence requirement: code evidence (file:line + attack scenario), no theoretical fluff
- Output: 7 structured report files in `security/{date}-{slug}/`
- Using `--fix` for auto-remediation of Critical/High findings

**L10: 12维场景探索**
- The 12 dimensions: happy paths, errors, edge cases, abuse, scale, concurrency, temporal, data variation, permissions, integrations, recovery, state transitions
- Domain-specific priorities (software vs. product vs. security)
- Output formats: use-cases, user-stories, test-scenarios, threat-scenarios
- Chaining scenario → debug (hunt bugs in discovered edge cases)
- Chaining scenario → security (audit discovered threat scenarios)

**P05: 完整的安全审计流水线**
- Task: Audit a web API for security vulnerabilities + generate edge case tests
- Uses: `/autoresearch:scenario` → `/autoresearch:security` → `/autoresearch:fix --from-debug`
- Learning: systematic security thinking, evidence-based findings

---

### Phase 6 — 发布与高级模式 (Ship & Advanced Patterns)
**L11 + L12 → P06**

**L11: 通用发布流水线**
- 8 phases: Identify → Inventory → Checklist → Prepare → Dry-run → Ship → Verify → Log
- 9 ship types: code-pr, code-release, deployment, content, marketing-email, marketing-campaign, sales, research, design
- The one mandatory confirm gate (before any irreversible action)
- Post-ship monitoring with `--monitor N`
- Rollback with `--rollback`

**L12: 高级模式 — 过夜运行、MCP集成、CI/CD**
- Overnight runs: `nohup`, `tmux`, progress monitoring
- MCP server integration (database queries, API calls during loop)
- CI/CD gating: `--fail-on <severity>` for security, coverage thresholds
- Multi-platform: Claude Code vs OpenCode vs Codex differences
- Building custom evaluators for new domains
- The research → skill → evaluator development cycle

**P06: 端到端自动化研究项目**
- Task: Full pipeline — plan → research (overnight simulation) → debug → fix → security → ship
- Uses: All 10 commands chained
- Learning: full pipeline orchestration, overnight runs, production patterns

---

## Resources Section

### Templates
- `research.md` template (blank)
- `evaluate.py` template (generic)
- `autoresearch-results.tsv` template
- `benchmark.py` template

### Reference
- Metric cheat sheet (15 domains)
- Command quick-decision guide
- Evaluator contract specification
- TSV format specification
- Guard pattern reference
- Crash recovery reference

### Domain Examples
- Code optimization (sort, bundle size, API latency)
- ML/Data Science (RMSE, accuracy, simulation)
- Content & Marketing (LLM judge score, conversion)
- Security (STRIDE + OWASP)
- Literature (papers_found, citation coverage)

---

## Key Pedagogical Choices

1. **Start with the canonical example** (sort optimization) — students see the full loop before abstraction
2. **Build from Karpathy's original** — intellectual lineage makes the principles memorable
3. **Each project uses real code** — not toy examples, actual measurable improvements
4. **Chaining taught progressively** — single commands first, chains in Phase 3+
5. **Chinese-first naming** for lecture themes — this is a Chinese-language primary audience
6. **Difficulty escalation**: mechanical metric (P01) → custom evaluator (P02) → stateful debugging (P03) → subjective domain (P04) → security (P05) → full pipeline (P06)

---

## Ultimate Purpose Context

**Why:** The course exists to teach "specific research automation." Every lecture builds toward a student being able to say: "I have a research question, I can define a metric, I can run 100 experiments overnight, and I wake up to results with full provenance in git."

**How to apply:** Design each lecture to answer ONE question that blocks the student from running their own research loop. Projects are the proof — if the student can complete P06, they can automate their research.
