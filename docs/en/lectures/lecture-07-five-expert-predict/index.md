# Lecture 07 — Five-Expert Prediction

[中文版本 →](/zh/lectures/lecture-07-five-expert-predict/)

Code examples: [code/](./code/)  
Practice project: [Project 04 — Architecture Decision Debate](/en/projects/project-04-architecture-debate/)

---

Before you debug, fix, or ship — `/autoresearch:predict` gives you five expert perspectives in two minutes. This is pre-flight analysis: understand the risk landscape before committing to action.

## Why Single-Perspective Analysis Fails

Most pre-action analysis suffers from **perspective monoculture**: one person (or one AI persona) evaluates a change from their habitual angle. The security-focused engineer sees security risks. The performance engineer sees latency risks. The reliability engineer worries about edge cases. But they rarely all look at the same change at the same time.

The result: architectural decisions approved by developers who never asked the security question. Performance optimizations that introduce reliability regressions no one predicted. Debugging sessions that ignore the infrastructure angle and waste days on the application layer.

`/autoresearch:predict` runs five independent expert analyses simultaneously, then forces them to debate and converge on a prioritized finding list.

## The Five Personas

Each persona has a specific analytical lens and a set of questions they always ask:

**Architect** — system design perspective:
- Does this change fit the existing architecture?
- What coupling does it introduce?
- What does it make harder to change in the future?
- What are the scaling implications?

**Security Analyst** — threat modeling perspective:
- What new attack surfaces does this introduce?
- What data could be exposed or corrupted?
- What trust boundaries are being crossed?
- What's the blast radius if this is exploited?

**Performance Engineer** — runtime behavior perspective:
- What is the computational complexity?
- What are the memory allocation patterns?
- Where are the potential bottlenecks?
- What happens at 10× the current load?

**Reliability Engineer** — failure mode perspective:
- What can go wrong at runtime?
- How does this fail under partial failure of dependencies?
- Is there a graceful degradation path?
- What's the blast radius if this crashes?

**Devil's Advocate** — contrarian perspective:
- What assumption in this approach is most likely to be wrong?
- What simpler alternative hasn't been considered?
- What is the biggest risk that the other perspectives are downplaying?
- If this fails, what will the post-mortem say was the root cause?

## Anti-Herd Detection

The most dangerous failure mode in multi-agent analysis is convergence without genuine debate. If all five agents see the same code and read each other's analyses before forming their own, they will herd toward a consensus that reflects the first agent's framing.

`/autoresearch:predict` prevents this with **independent cold-start analysis**: each persona analyzes the code without seeing the other personas' output. Only after all five have completed their independent analysis does the synthesis phase begin.

The synthesis phase explicitly looks for dissent:
- Which findings do 4/5 agree on? (high confidence)
- Which findings does only 1/5 raise? (minority view — worth explicit investigation)
- Where do two personas directly contradict each other? (unresolved tension — flag for human decision)

Minority views are especially valuable. The one Security Analyst who raises an injection risk while four others focus on performance has information the consensus is missing.

## Output Structure

```markdown
# Predict Analysis: [scope]

## Consensus Findings (4-5/5 agree)
1. [finding] — confidence: HIGH
   Evidence: [specific file:line references]
   Recommendation: [specific action]

## Notable Dissent (1-2/5 raise)
- [Persona X only]: [finding]
  Reason to investigate: [why this minority view matters]

## Unresolved Tensions
- [Persona A] says X; [Persona B] says ¬X
  Decision required: [what needs a human call]

## Recommended Actions (prioritized)
1. [highest risk finding + action]
2. ...
```

## Chaining Predict with Other Commands

Predict is most powerful as a pre-flight step before action:

```
/autoresearch:predict --chain debug
```
Output: pre-ranked hypotheses for the debug loop. Instead of the agent guessing where to start, it begins with the Security Analyst's findings, then Reliability Engineer's, etc.

```
/autoresearch:predict --chain security
```
Output: multi-persona red team analysis fed directly into the security audit.

```
/autoresearch:predict --chain scenario,debug,fix
```
Output: full quality pipeline — explore scenarios, investigate bugs, fix errors.

## When to Use Predict

| Situation | Value |
|-----------|-------|
| Before a major refactor | Catch architectural risks before writing code |
| Before merging a large PR | Independent risk analysis from all angles |
| Before a production deployment | Reliability and performance pre-flight |
| When debugging a mysterious failure | Pre-ranked hypotheses save investigation time |
| Before a security review | Pre-identify likely findings before formal audit |

## Key Takeaways

- Five independent cold-start analyses prevent herding toward a flawed consensus
- Each persona has a specific analytical lens — no overlap, no gaps
- Minority views are the most valuable output — they catch what the consensus misses
- Unresolved tensions require human decisions — flag them explicitly
- Chain with `--chain debug/security/fix` to feed findings directly into action commands

---

**Next**: [Lecture 08 — Adversarial Refinement](/en/lectures/lecture-08-adversarial-refinement/)
