# Learn AutoResearch

> Set the GOAL → The agent runs the LOOP → You wake up to results.

**Learn AutoResearch** is a project-based course on automating research using the autoresearch framework — a generalization of Karpathy's autonomous ML training loop to any domain with a measurable metric.

[中文 →](README.md) | [Live Docs →](https://zhimin-z.github.io/learn-auto-research/)

---

## What You Will Learn

- **Define measurable research goals** — turn vague objectives into mechanical metrics any agent can optimize
- **Run autonomous improvement loops** — one change per iteration, automatic rollback, git as memory
- **Debug scientifically** — falsifiable hypotheses, evidence-based investigation, zero-error termination
- **Predict before acting** — five expert perspectives before committing to any major change
- **Audit security autonomously** — STRIDE + OWASP + red-team analysis with code-level evidence
- **Ship with confidence** — 8-phase pipeline covering code, content, and deployments

## Curriculum

| Phase | Topic | Lectures | Project |
|-------|-------|----------|---------|
| 1 Foundations | Why manual iteration fails, measurable goals | L01–L02 | P01 Sort optimization |
| 2 Core Loop | 5-stage loop internals, pivot strategies | L03–L04 | P02 Function fitting |
| 3 Debug & Fix | Scientific debugging, error cascade crushing | L05–L06 | P03 FastAPI debugging |
| 4 Predict & Reason | 5-expert prediction, adversarial refinement | L07–L08 | P04 Architecture debate |
| 5 Security & Scenarios | STRIDE/OWASP audit, 12-dimension exploration | L09–L10 | P05 Security audit |
| 6 Ship & Advanced | Universal ship pipeline, overnight runs | L11–L12 | P06 End-to-end pipeline |

## Quick Start

```bash
# Install dependencies
npm install

# Start local dev server
npm run dev

# Build static site
npm run build
```

## Tech Stack

- [VitePress](https://vitepress.dev/) 1.6+ static site generation
- [vitepress-plugin-mermaid](https://github.com/emersonbottero/vitepress-plugin-mermaid) for diagrams
- Bilingual: English (root) + Chinese (/zh/)
- Project code: Python (stdlib only, no pip required)

## Acknowledgements

The core loop concept is inspired by [Andrej Karpathy's autoresearch](https://github.com/karpathy/autoresearch).

## License

MIT
