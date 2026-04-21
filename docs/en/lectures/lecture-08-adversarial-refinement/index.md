# Lecture 08 — Adversarial Refinement

[中文版本 →](/zh/lectures/lecture-08-adversarial-refinement/)

Code examples: [code/](./code/)  
Practice project: [Project 04 — Architecture Decision Debate](/en/projects/project-04-architecture-debate/)

---

The autoresearch loop works when you have a mechanical metric. But what about decisions where no objective metric exists? Architecture choices, product strategy, content quality, design trade-offs — these are irreducibly subjective.

`/autoresearch:reason` extends the autoresearch loop to subjective domains by using a **blind judge panel** as the fitness function. The panel IS the metric: `val_bpb` for decisions.

## The Problem with Subjective Decisions

When there's no metric, three failure modes emerge:

**Premature convergence**: The first good-sounding argument wins. No one challenges it rigorously because challenging feels like being difficult.

**Authority bias**: The most senior person's opinion wins. Technical merit and evidence get crowded out by hierarchy.

**False consensus**: Everyone says they agree, but they haven't actually resolved the underlying tension. The decision gets made, the tension resurfaces in implementation.

The scientific method works for objective domains because experiments falsify hypotheses. For subjective domains, we need a different mechanism.

## The Adversarial Refinement Loop

The loop has six steps:

**1. Generate-A**: An agent generates candidate A — an answer, proposal, architecture design, or argument.

**2. Critic attacks**: A separate critic agent (cold start, hasn't seen the generation process) attacks candidate A as hard as possible. Strawman attacks, counterexamples, edge cases, alternative framings.

**3. Author-B responds**: A third agent (cold start, sees only A and the critique) generates candidate B — an improved version that addresses the critique.

**4. Synthesize**: A synthesizer agent merges the strongest elements of A and B into candidate C.

**5. Blind judge panel**: N judges (3–7, odd preferred) evaluate C without seeing labels. They don't know if they're judging A, B, or C — just two unmarked candidates X and Y. They pick the better one.

**6. Update and repeat**: The winning candidate becomes the new A. Loop until N consecutive wins (convergence) or `max_iterations` exhausted.

**Key invariant**: Every agent is a cold-start fresh invocation. No agent sees the history of the debate. No shared session. This prevents coherence bias — agents changing their assessment to match what they said before.

## Why Blind Judging Works

Sighted judging is unreliable. When judges know which option is "the new proposal" vs "the current approach," they bring in anchoring bias, loss aversion, and social pressure. The new proposal has to overcome not just its own weaknesses but also the psychological weight of disrupting the status quo.

Blind judging removes all of this. The judge sees only X and Y. They pick the better one based purely on the content. If Y wins 3 times in a row across different judges, it's genuinely better by the only measure that matters: human judgment.

## Domains and Use Cases

| Domain | Example task | Judge criteria |
|--------|-------------|----------------|
| `software` | "Event sourcing vs. CQRS for order management" | Scalability, maintainability, operational complexity |
| `product` | "Freemium vs. trial vs. open core pricing" | Market fit, conversion, competitive positioning |
| `business` | "Build vs. buy decision for auth system" | Cost, time-to-market, control, risk |
| `security` | "Defense-in-depth strategy for API" | Coverage, practicality, residual risk |
| `research` | "Hypothesis A vs. Hypothesis B for experiment" | Testability, expected information gain, cost |
| `content` | "Landing page copy variant A vs. B" | Clarity, persuasion, CTA effectiveness |

## Convergence and Handoff

The loop converges when one candidate wins `--convergence N` (default: 3) consecutive rounds. At convergence, the loop stops and generates `handoff.json` — a structured summary of the winning position with supporting evidence.

`handoff.json` is designed to be read by other commands:

```json
{
  "winning_candidate": "...",
  "convergence_round": 7,
  "judge_agreement": 0.85,
  "key_arguments": [...],
  "minority_dissent": "...",
  "recommended_next_step": "autoresearch:plan"
}
```

Chain: `reason → plan` — converge on the architecture decision, then scaffold a research project to validate the winning approach empirically.

## Chain Patterns

```
reason → predict    Converge on a position, then stress-test with 5-expert analysis
reason → plan       Converge, then scaffold an autoresearch project to validate empirically
reason → scenario   Converge, then explore edge cases of the winning decision
```

## Key Takeaways

- When no metric exists, the blind judge panel IS the metric
- Cold-start agents prevent coherence bias and herding
- Blind judging removes authority bias and anchoring — pure content wins
- Convergence (N consecutive wins) is the stopping condition
- `handoff.json` chains the output to any downstream command
- For architecture decisions specifically, chain `reason → plan → autoresearch` to validate empirically

---

**Next**: [Lecture 09 — STRIDE+OWASP Security Audit](/en/lectures/lecture-09-stride-owasp-security/)
