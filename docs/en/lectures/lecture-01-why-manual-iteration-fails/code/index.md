# L01 Code — Why Manual Iteration Fails

> **Goal**: See the efficiency gap between random human-style search and systematic grid search on a 1-D objective — with the same budget.

Run it:

```sh
cd docs/en/lectures/lecture-01-why-manual-iteration-fails/code
python manual_vs_systematic.py
```

---

## Step 1: Define the objective and search space

```python
import random
import math

SEED   = 42
BUDGET = 20           # number of evaluations allowed
DOMAIN = (0.0, 10.0)  # search space

def objective(x: float) -> float:
    """A simple peaked function. Maximum near x=3.7."""
    return math.exp(-0.5 * (x - 3.7) ** 2)
```

**Key line**: `BUDGET = 20` — both strategies get exactly 20 evaluations. The only difference is how they spend them.

---

## Step 2: Manual strategy — random jumps

```python
random.seed(SEED)
manual_history = []
best_manual = (None, -1.0)

for i in range(BUDGET):
    x = random.uniform(*DOMAIN)   # "gut feel" = uniform random
    score = objective(x)
    manual_history.append((i + 1, round(x, 4), round(score, 4)))
    if score > best_manual[1]:
        best_manual = (x, score)
```

**Key line**: `x = random.uniform(*DOMAIN)` — models human tendency to jump around intuitively. With 20 evaluations over a range of 10, large regions go unexplored.

---

## Step 3: Systematic strategy — evenly spaced grid

```python
grid_history = []
best_grid = (None, -1.0)
step = (DOMAIN[1] - DOMAIN[0]) / BUDGET

for i in range(BUDGET):
    x = DOMAIN[0] + i * step      # evenly spaced: 0.0, 0.5, 1.0, ...
    score = objective(x)
    grid_history.append((i + 1, round(x, 4), round(score, 4)))
    if score > best_grid[1]:
        best_grid = (x, score)
```

**Key line**: `step = (DOMAIN[1] - DOMAIN[0]) / BUDGET` — divides the entire search space evenly. No gaps larger than one step.

---

## Step 4: Report the gap

```python
print(f"Best manual : x={best_manual[0]:.4f}  score={best_manual[1]:.4f}")
print(f"Best grid   : x={best_grid[0]:.4f}  score={best_grid[1]:.4f}")
print(f"True optimum: x=3.7000  score=1.0000")

gap_manual = 1.0 - best_manual[1]
gap_grid   = 1.0 - best_grid[1]
print(f"Systematic search is {gap_manual/gap_grid:.1f}x closer to optimum.")
```

**Key line**: `gap_manual/gap_grid` — the multiplier tells you how much more of the budget the manual strategy "wasted" on unexplored regions.

---

## Try Changing It

1. Change `BUDGET = 20` to `BUDGET = 5` — does the gap between strategies grow or shrink with a tighter budget?
2. Change `SEED = 42` to `SEED = 1` — does the manual strategy change? Does the grid strategy change? Why?
3. Move the optimum by changing `x - 3.7` to `x - 9.5` — does the grid strategy still find it? What about manual?
4. For your own research: what is your "domain" (the thing you're tuning), and what is your "objective" (the metric you're measuring)?
