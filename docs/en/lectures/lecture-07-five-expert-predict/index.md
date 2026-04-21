# Lecture 07 — Five-Expert Prediction

`L01 > L02 > L03 > L04 > L05 > L06 | [ L07 ] L08 > L09 > L10 > L11 > L12`

> *"One person's blind spot is another person's obvious problem."* — Five independent cold-start analyses catch what any single perspective misses.
>
> **Core idea**: How `/autoresearch:predict` runs five expert personas independently before any action, detects minority views, and surfaces the risks that consensus would bury.

Code examples: [code/](./code/)  
Practice project: [Project 04 — Architecture Decision Debate](/en/projects/project-04-architecture-debate/)

[中文版本 →](/zh/lectures/lecture-07-five-expert-predict/)

---

## The Problem

Most pre-action analysis suffers from **perspective monoculture**: one person evaluates a change from their habitual angle. The security-focused engineer sees security risks. The performance engineer sees latency. But they rarely look at the same change at the same time.

The result: architectural decisions approved without asking the security question. Performance optimizations that introduce reliability regressions no one predicted. Debugging sessions that miss the infrastructure angle entirely.

## The Solution

```
Code change or decision
         |
    ─────┴─────────────────────────────────
    |         |         |         |        |
Architect  Security  Performance  Reliability  Devil's
           Analyst   Engineer     Engineer     Advocate
    |         |         |         |        |
    └─────┬──────────────────────────────────
         |
    (cold start — each analyzes without seeing others)
         |
    Synthesis: 4-5 agree = HIGH confidence
               1/5 raises = minority view ← most valuable
               A vs B contradict = human decision needed
         |
    Prioritized findings list
```

## How It Works

**1. Five independent cold-start analyses.**

Each persona analyzes the code without seeing any other persona's output. This prevents herding — the most dangerous failure mode in multi-agent analysis.

| Persona | Their core question |
|---|---|
| **Architect** | Does this fit the architecture? What coupling does it introduce? |
| **Security Analyst** | What new attack surfaces? What trust boundaries are crossed? |
| **Performance Engineer** | What's the complexity? What happens at 10× load? |
| **Reliability Engineer** | How does this fail under partial dependency failure? |
| **Devil's Advocate** | What assumption here is most likely to be wrong? |

**2. Anti-herd detection in synthesis.**

After all five complete their independent analyses, synthesis looks for:
- **4-5/5 agree** → high confidence finding
- **1/5 raises only** → minority view (highest value — the consensus is missing this)
- **A says X, B says ¬X** → unresolved tension → flag for human decision

Minority views are the most important output. The one Security Analyst who raises an injection risk while four others focus on performance has information the consensus is burying.

**3. Chain with action commands.**

```bash
/autoresearch:predict --chain debug
```
Output: pre-ranked hypotheses for the debug loop. Instead of guessing where to start, the loop begins with the Security Analyst's findings, then Reliability Engineer's.

```bash
/autoresearch:predict --chain security
/autoresearch:predict --chain scenario,debug,fix
```

**4. When to use predict.**

| Situation | What predict catches |
|---|---|
| Before a major refactor | Architectural risks before writing code |
| Before merging a large PR | Independent risk analysis from all angles |
| Before production deploy | Reliability and performance pre-flight |
| Debugging a mysterious failure | Pre-ranked hypotheses to start from |
| Before a security review | Pre-identify likely findings |

## What Changed

| Single-perspective review | Five-expert predict |
|---|---|
| Security question skipped | Security Analyst always asks it |
| Performance regressions missed | Performance Engineer always checks complexity |
| Consensus buries minority views | Synthesis explicitly surfaces dissent |
| Tension stays implicit | Unresolved tensions flagged for human decision |

## Try It

Run the five-expert predictor:

```sh
cd docs/en/lectures/lecture-07-five-expert-predict/code
python five_expert_predict.py
```

Questions to think about:

1. In the output, which finding had the highest agreement count? Which had the lowest?
2. Find a minority view (only 1/5 raised it) — why might this be the most important finding?
3. If the Security Analyst and Performance Engineer directly contradict each other, what does the synthesis output say? What should a human do with this?
4. Think of a recent architectural decision — which of the five personas would have raised the risk that turned out to matter most?

---

**Next**: [Lecture 08 — Adversarial Refinement](/en/lectures/lecture-08-adversarial-refinement/)
