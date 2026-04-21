# Learn AutoResearch — Claude Code Instructions

## Project Purpose

Build the **Learn AutoResearch** tutorial course: a VitePress-based educational site teaching students how to automate specific research using the autoresearch framework (Karpathy-inspired autonomous improvement loops).

**Ultimate goal**: Students can define a measurable research problem, run 100 experiments overnight, wake up to results with full git provenance.

## Memory Index

All key context is stored in [memory/](memory/):

- [memory/paradigm-analysis.md](memory/paradigm-analysis.md) — The VitePress tutorial paradigm from learn-harness-engineering (tech stack, dir structure, content style, curriculum pattern). **Read this first** when building any part of the site.
- [memory/autoresearch-materials.md](memory/autoresearch-materials.md) — Summary of all three autoresearch source repos: commands, rules, examples, metric cheat sheet.
- [memory/curriculum-plan.md](memory/curriculum-plan.md) — Full 12-lecture 6-project curriculum plan, organized by difficulty across 6 phases.

## Source Material

Reference repos in this directory:
- `autoresearch/` — Karpathy's original ML training loop (the intellectual origin)
- `autoresearch_alt/` — Generalized multi-platform version (autoresearch_alt/README.md is the primary reference)
- `autoresearch-skill/` — Production-ready skill package (autoresearch-skill/SKILL.md + guide/ + examples/)

Tutorial structure reference:
- `learn-harness-engineering/` — The paradigm to clone (VitePress, bilingual, 12 lectures + 6 projects)

## Tech Stack (to implement)

- VitePress 1.6+ with vitepress-plugin-mermaid
- Bilingual: English (root) + Chinese (/zh/)
- GitHub Actions: deploy-pages + release-course-pdfs
- Project code: Python examples (not Electron — autoresearch uses Python)

## Curriculum Structure

6 phases × (2 lectures + 1 project):
1. **理解原理** — Why autoresearch works, measurable goals (L01-02, P01: sort optimization)
2. **掌握核心循环** — 5-stage loop, pivot strategies (L03-04, P02: function fitting)
3. **调试与修复** — Scientific debugging, error crushing (L05-06, P03: FastAPI debugging)
4. **多视角与预测** — Predict + Reason commands (L07-08, P04: architecture debate)
5. **安全与场景探索** — Security + Scenario commands (L09-10, P05: security audit)
6. **发布与高级模式** — Ship + advanced patterns (L11-12, P06: full pipeline)

## Key Conventions

- Follow the exact directory structure from `memory/paradigm-analysis.md`
- Every lecture has `index.md` + `code/` subfolder with runnable examples
- Every project has `starter/` + `solution/` with `research.md`, `evaluate.py`, `results.tsv`
- All content bilingual (docs/en/ and docs/zh/ in parallel)
- Code examples use Python (stdlib only, no pip) — matches autoresearch requirements
- Results always tracked in TSV format with columns: iteration, commit, metric, delta, status, description
