# Lecture 08 — Adversarial Refinement

`L01 > L02 > L03 > L04 > L05 > L06 | L07 > [ L08 ] L09 > L10 > L11 > L12`

> *"When there's no metric, the blind judge panel is the metric."* — Blind judging removes authority bias and anchoring. Pure content wins.
>
> **Core idea**: How `/autoresearch:reason` extends the loop to subjective decisions — adversarial critique, cold-start agents, and a blind judge panel as the fitness function.

Code examples: [code/](./code/)  
Practice project: [Project 04 — Architecture Decision Debate](/en/projects/project-04-architecture-debate/)


---

## The Problem

The autoresearch loop works when you have a mechanical metric. But architecture choices, product strategy, content quality, and design trade-offs are irreducibly subjective — there's no `evaluate.py` to run.

Without a mechanism, three failure modes appear:

**Premature convergence**: The first good-sounding argument wins. No one challenges it rigorously because challenging feels difficult.

**Authority bias**: The most senior person's opinion wins. Technical merit gets crowded out by hierarchy.

**False consensus**: Everyone says they agree, but the underlying tension resurfaces in implementation.

## The Solution

```
Author-A generates candidate A
        |
Critic attacks A (cold start — hasn't seen the generation)
        |
Author-B responds (cold start — sees A + critique only)
  generates improved candidate B
        |
Synthesizer merges strongest elements → candidate C
        |
Blind judge panel (3-7 judges, odd number preferred):
  "Which is better, X or Y?" ← no labels, no history
        |
  C wins? → C becomes new A → loop
  A wins? → A becomes new A → loop
        |
  N consecutive wins = convergence → write handoff.json
```

**Key invariant**: Every agent is a fresh cold-start invocation. No shared session. No agent sees the history of the debate. This prevents coherence bias — agents changing their assessment to match what they said earlier.

## How It Works

**1. Cold-start agents prevent herding.**

If agents read each other's outputs before forming their own, they herd toward a consensus that reflects the first agent's framing. Cold start means each agent forms an independent position before any synthesis happens.

**2. Blind judging removes authority bias.**

Sighted judging is unreliable. When judges know which option is "the new proposal" vs "the current approach," they bring in loss aversion and social pressure. Blind judges see only X and Y. If Y wins 3 times in a row across different judges, it's genuinely better by the only measure that matters: human judgment.

**3. Convergence stops the loop.**

```bash
/autoresearch:reason --convergence 3  # default: 3 consecutive wins
```

At convergence, the loop writes `handoff.json`:

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

**4. Where to use it.**

| Domain | Example task |
|---|---|
| `software` | Event sourcing vs. CQRS for order management |
| `product` | Freemium vs. trial vs. open core pricing |
| `business` | Build vs. buy decision for auth system |
| `security` | Defense-in-depth strategy for API |
| `research` | Hypothesis A vs. B — which to run first |
| `content` | Landing page copy variant A vs. B |

**5. Chain patterns.**

```
reason → predict    Converge on position → stress-test with 5-expert analysis
reason → plan       Converge → scaffold autoresearch project to validate empirically
reason → scenario   Converge → explore edge cases of the winning decision
```

The most powerful chain for architecture decisions: `reason → plan → autoresearch` — converge on the decision, then validate it empirically with a research loop.

## What Changed

| Subjective decision without structure | Adversarial refinement |
|---|---|
| First good argument wins | Critic attacks every candidate before it advances |
| Authority bias decides | Blind judges see only content, not labels |
| Consensus is false | Convergence requires N consecutive wins, not one vote |
| Decision is not documented | `handoff.json` captures winning arguments + dissent |

## Try It

Run the debate tracker and judge aggregator:

```sh
cd docs/en/lectures/lecture-08-adversarial-refinement/code
python debate_tracker.py
python judge_aggregator.py
```

Questions to think about:

1. After running `judge_aggregator.py`, what was the `judge_agreement` score? What does a score below 0.6 mean?
2. In the loop, the critic's job is to attack the candidate "as hard as possible." Why is a weak critic worse than no critic?
3. Why does the loop use a blind judge panel instead of having the same agents vote?
4. Think of a technical decision you've made recently — write three rounds of the adversarial loop: what would Critic say about your original choice?

---

**Next**: [Lecture 09 — STRIDE+OWASP Security Audit](/en/lectures/lecture-09-stride-owasp-security/)
