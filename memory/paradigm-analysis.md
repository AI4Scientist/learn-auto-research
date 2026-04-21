---
name: learn-harness-engineering paradigm analysis
description: Complete structural and stylistic analysis of learn-harness-engineering tutorial course, used as the reference paradigm for Learn AutoResearch
type: project
---

# Learn Harness Engineering — Tutorial Paradigm

## Tech Stack

- **Framework**: VitePress 1.6+ (Vue 3-based SSG)
- **Diagrams**: vitepress-plugin-mermaid + mermaid (brand color: #D95C41)
- **Language**: TypeScript (strict mode throughout)
- **Build**: Vite
- **PDF export**: pdf-lib + tsx scripts
- **Screenshot automation**: Playwright
- **Deployment**: GitHub Pages via GitHub Actions
- **Package manager**: npm

## Directory Structure Pattern

```
learn-<course-name>/
├── package.json                   # VitePress + tooling
├── CLAUDE.md                      # Agent instructions
├── README.md / README-CN.md       # Bilingual course overview
├── .github/workflows/
│   ├── deploy-pages.yml           # GitHub Pages deploy
│   └── release-course-pdfs.yml   # PDF generation
├── .vitepress/
│   ├── config.mts                 # Bilingual nav + sidebar config
│   └── theme/
│       ├── index.js
│       └── style.css
├── docs/
│   ├── public/screenshots/
│   ├── en/
│   │   ├── index.md               # Home page
│   │   ├── lectures/              # NN lectures
│   │   │   └── lecture-NN-slug/
│   │   │       ├── index.md       # Main lecture content
│   │   │       └── code/          # Runnable examples
│   │   ├── projects/              # Hands-on projects
│   │   │   └── project-NN-slug/
│   │   │       └── index.md
│   │   └── resources/
│   │       ├── templates/
│   │       └── reference/
│   └── zh/                        # Parallel Chinese versions
└── projects/                      # Executable project code
    ├── shared/
    └── project-NN/
        ├── README.md
        ├── starter/               # Starting codebase
        └── solution/              # Reference solution
```

## Content Style — Lecture Format

Each lecture `index.md` follows this structure:

1. **Language switch link** at top: `[中文版本 →](...)`
2. **H1 heading** with lecture number + question form ("What is X?", "Why does Y fail?")
3. **Introduction** (3–5 paragraphs): real-world scenario or problem statement
4. **Core concepts** (5–8 key terms with definitions)
5. **Detailed breakdown** (subsections with H2/H3)
6. **Case study / experiment** with real data or controlled results
7. **Practical application** — industry example
8. **Key takeaways** — 4–5 bullet points
9. **Code examples** reference (link to `/code/` subfolder)

Code files in `/code/`:
- TypeScript examples executable with `npx tsx <file>.ts`
- Markdown checklists and machine-readable templates
- Named descriptively: `failure-pattern-demo.ts`, `minimal-harness-loop.ts`

## Content Style — Project Format

Each project `index.md` covers:
- Overview of what students build
- Learning objectives tied to lectures
- Starter vs solution comparison
- Implementation hints and gotchas
- Expected outcomes and verification criteria

Project code structure (`starter/` + `solution/`):
- `task-prompt.md` — one-sentence mission
- `AGENTS.md` — operating rules
- `CLAUDE.md` — Claude Code quick ref
- `feature_list.json` — features to implement (machine-readable)
- `init.sh` — build + verify + start
- `src/` — actual implementation code

## VitePress Config Pattern

```typescript
// config.mts key patterns:
base: '/learn-<course>/',
locales: {
  root: { label: 'English', lang: 'en-US' },
  zh: { label: '中文', lang: 'zh-CN' }
},
themeConfig: {
  nav: [...],     // top nav with active match patterns
  sidebar: {...}  // per-locale sidebar with lecture/project structure
}
```

## Curriculum Structure Pattern (12 lectures + 6 projects)

6 phases, each = 2 lectures + 1 project:
- Phase 1: See the Problem (L01-02 → P01)
- Phase 2: Structure the Repo (L03-04 → P02)
- Phase 3: Connect Sessions (L05-06 → P03)
- Phase 4: Feedback & Scope (L07-08 → P04)
- Phase 5: Verification (L09-10 → P05)
- Phase 6: Put It Together (L11-12 → P06)

## Key Design Principles

1. **Bilingual by default** — every piece of content in EN + ZH
2. **Progressive disclosure** — short entry files linking to focused docs
3. **Machine-readable state** — JSON/shell files as system of record
4. **Session continuity** — progress logs, feature tracking, handoff notes
5. **Hands-on projects** — real executable code, builds on itself across phases
6. **Evidence-first** — every claim backed by runnable verification
7. **Clear lifecycle** — Init → Execute → Verify → Document → Handoff

## Why:** This paradigm was proven in learn-harness-engineering as an effective format for AI-agent educational content. Replicating it ensures consistency and leverages the same deployment pipeline.

## How to apply:** Copy the VitePress config structure, maintain bilingual parallel structure under docs/en/ and docs/zh/, keep the 6-phase 12-lecture format for any new course.
