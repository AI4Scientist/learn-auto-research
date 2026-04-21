# L10 Code — 12-Dimension Scenario Exploration

> **Goal**: Score and rank the 12 scenario dimensions for your domain — so you know which dimension to explore first before you start writing scenarios.

Run it:

```sh
cd docs/en/lectures/lecture-10-twelve-dimension-scenarios/code
python scenario_priority.py api
python scenario_priority.py ml
python scenario_priority.py security
```

---

## Step 1: Define the 12 dimensions

```python
import sys

DIMENSIONS = [
    {"id": "D01", "name": "Happy Path",
     "desc": "Normal usage with valid inputs and expected conditions.",
     "tags": ["all"]},
    {"id": "D02", "name": "Edge Cases",
     "desc": "Boundary values, empty inputs, maximum sizes.",
     "tags": ["all"]},
    {"id": "D03", "name": "Adversarial Input",
     "desc": "Malformed, malicious, or unexpected data from untrusted sources.",
     "tags": ["api", "web", "security"]},
    {"id": "D04", "name": "Concurrency / Race Conditions",
     "desc": "Multiple simultaneous users or threads accessing shared state.",
     "tags": ["api", "database", "distributed"]},
    # D05-D12 follow same structure...
]
```

**Key line**: `"tags": ["all"]` — dimensions tagged `"all"` apply to every domain. Dimensions tagged with specific domains (like `"api"` or `"ml"`) get a bonus score only for those domains.

---

## Step 2: Define domain-specific boosts

```python
DOMAIN_BOOSTS: dict[str, dict[str, int]] = {
    "api":        {"D03": 3, "D04": 2, "D05": 2, "D06": 2, "D10": 1},
    "ml":         {"D07": 4, "D08": 3, "D05": 2, "D10": 2},
    "security":   {"D03": 4, "D11": 3, "D04": 2},
    "web":        {"D12": 3, "D03": 2, "D05": 2},
    "database":   {"D04": 3, "D05": 3, "D06": 3},
    "distributed":{"D04": 4, "D06": 4, "D08": 2},
}

BASE_SCORE    = 5
TAG_MATCH_BONUS = 2
```

**Key line**: `"ml": {"D07": 4, ...}` — ML gets a +4 boost for D07 (Data Distribution Shift) because production data differing from training data is the most common and most dangerous ML failure. Domain expertise is encoded as numbers.

---

## Step 3: Score and sort dimensions

```python
def score_dimensions(domain: str) -> list[tuple[int, dict]]:
    domain  = domain.lower().strip()
    boosts  = DOMAIN_BOOSTS.get(domain, {})
    scored  = []
    for dim in DIMENSIONS:
        score = BASE_SCORE
        if domain in dim["tags"] or "all" in dim["tags"]:
            score += TAG_MATCH_BONUS
        score += boosts.get(dim["id"], 0)
        scored.append((score, dim))
    scored.sort(key=lambda x: -x[0])
    return scored
```

**Key line**: `boosts.get(dim["id"], 0)` — dimensions not in the boost table get 0 added. Only explicitly prioritized dimensions get the bonus. Unknown dimensions still get the base score.

---

## Step 4: Print ranked output with recommendations

```python
def main():
    domain  = sys.argv[1] if len(sys.argv) > 1 else "api"
    results = score_dimensions(domain)

    print(f"\nScenario Priority for domain: '{domain}'")
    for rank, (score, dim) in enumerate(results, 1):
        print(f"{rank:<10} {score:<7} {dim['id']:<5} {dim['name']:<35} {dim['desc']}")

    top3 = [d["name"] for _, d in results[:3]]
    print(f"\nRecommended first three: {', '.join(top3)}")
    print("Run these scenarios before moving to lower-priority dimensions.")
```

**Key line**: The recommendation is to start with the top 3 and work down — not to generate all 12 at once. One scenario per dimension per iteration keeps the loop systematic.

---

## Try Changing It

1. Compare `api` and `security` outputs — which dimensions appear in both Top 3s? Which appear in only one?
2. Change the `"ml"` boost for D07 from `4` to `1` — does Data Distribution Shift drop out of the Top 3?
3. Add a new domain `"mobile"` to `DOMAIN_BOOSTS` — which 3-4 dimensions matter most for mobile apps? Write the dict.
4. Pick a feature you built recently, choose its domain, and write one concrete scenario for each of the Top 3 dimensions.
