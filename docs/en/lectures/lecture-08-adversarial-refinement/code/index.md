# L08 Code — Adversarial Refinement

> **Goal**: Record a debate round (author proposal → critic objection → judge ruling), then aggregate judge scores across rounds to see if consensus is forming or disagreement is growing.

Run it:

```sh
cd docs/en/lectures/lecture-08-adversarial-refinement/code
python debate_tracker.py --demo
python judge_aggregator.py
```

---

## Tool 1: Debate Round Tracker

### Step 1: Load and save `handoff.json`

```python
import json, os, sys
from datetime import datetime

HANDOFF_FILE = "handoff.json"

def load_handoff() -> dict:
    if os.path.exists(HANDOFF_FILE):
        with open(HANDOFF_FILE) as f:
            return json.load(f)
    return {"rounds": []}

def save_handoff(data: dict) -> None:
    with open(HANDOFF_FILE, "w") as f:
        json.dump(data, f, indent=2)
```

**Key line**: `return {"rounds": []}` — if no file exists yet, start fresh with an empty rounds list. The file accumulates debate history across multiple sessions.

---

### Step 2: Use demo data to record a round

```python
DEMO_ROUND = {
    "author": (
        "I propose replacing the recursive Fibonacci with an iterative one. "
        "Benchmarks show 40x speedup and O(1) stack usage."
    ),
    "critic": (
        "The iterative version loses clarity for readers unfamiliar with "
        "dynamic programming. Is the complexity cost worth it?"
    ),
    "judge": (
        "Author's performance claim is valid for large n. Critic's readability "
        "concern is fair. Score: author 7/10, critic 6/10."
    ),
}

def main():
    demo = "--demo" in sys.argv
    data = load_handoff()
    new_round = DEMO_ROUND if demo else prompt_round()
    new_round["timestamp"]    = datetime.utcnow().isoformat() + "Z"
    new_round["round_number"] = len(data["rounds"]) + 1
    data["rounds"].append(new_round)
    save_handoff(data)
```

**Key line**: `new_round["round_number"] = len(data["rounds"]) + 1` — round numbers are assigned at save time, not input time. Running `--demo` three times creates rounds 1, 2, 3.

---

## Tool 2: Blind Judge Score Aggregator

### Step 3: Extract numeric scores with regex

```python
import re

SCORE_RE = re.compile(
    r"(author|critic)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*/\s*10",
    re.IGNORECASE
)

def extract_scores(judge_text: str) -> dict:
    scores = {}
    for match in SCORE_RE.finditer(judge_text):
        role  = match.group(1).lower()
        score = float(match.group(2))
        scores[role] = score
    return scores
```

**Key line**: `SCORE_RE` matches patterns like `author: 7/10`, `Author 8/10`, `critic - 6/10`. The flexible pattern handles natural language judge verdicts without requiring rigid formatting.

---

### Step 4: Compute agreement statistics

```python
def main():
    with open(HANDOFF_FILE) as f:
        data = json.load(f)

    for r in data["rounds"]:
        scores = extract_scores(r.get("judge", ""))
        a = scores.get("author")
        c = scores.get("critic")
        # print row...

    if all_author:
        avg_a     = sum(all_author) / len(all_author)
        avg_c     = sum(all_critic) / len(all_critic)
        agreement = abs(avg_a - avg_c)
        print(f"Author-critic gap: {agreement:.2f}  "
              f"({'low disagreement' if agreement < 1.5 else 'high disagreement — revisit'})")
```

**Key line**: `gap < 1.5` — a small gap means the judge found the author and critic roughly equally compelling. A large gap means the judge strongly favored one side. If the gap stays high across multiple rounds, the debate hasn't converged.

---

## Try Changing It

1. Run `debate_tracker.py --demo` three times, then `judge_aggregator.py` — what is the author-critic gap?
2. Manually edit `handoff.json` to add a round where the judge gives `author: 3/10, critic: 9/10` — how does the average change?
3. In the lecture, convergence requires N consecutive wins. What does "win" mean in terms of author and critic scores from this tool?
4. Take a technical decision you've made recently — write one round of the debate: what would the Author propose, what would the Critic attack, what would a fair Judge rule?
