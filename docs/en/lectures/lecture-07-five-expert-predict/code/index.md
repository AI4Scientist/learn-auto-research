# L07 Code — Five-Expert Prediction

> **Goal**: Generate five independent expert analysis prompts for a change you're about to make — one prompt per persona, ready to paste into separate Claude calls.

Run it:

```sh
cd docs/en/lectures/lecture-07-five-expert-predict/code
python five_expert_predict.py "Added LRU cache to the database query layer"
```

---

## Step 1: Define the five expert personas

```python
import sys, textwrap

EXPERTS = [
    {
        "name": "Performance Engineer",
        "focus": "latency, throughput, memory, CPU, cache behaviour",
        "question": (
            "What are the performance implications of this change? "
            "Will it reduce latency or throughput under high load? "
            "Are there hidden allocation or GC costs?"
        ),
    },
    {
        "name": "Correctness Reviewer",
        "focus": "edge cases, off-by-one errors, concurrency, data integrity",
        "question": "Where could this change introduce bugs? ...",
    },
    {
        "name": "Security Analyst",
        "focus": "injection, auth bypass, data leakage, supply-chain risk",
        "question": "Does this change open any attack surface? ...",
    },
    {
        "name": "Maintainability Advocate",
        "focus": "readability, coupling, testability, future change cost",
        "question": "How does this change affect long-term maintainability? ...",
    },
    {
        "name": "Research Validity Expert",
        "focus": "metric soundness, confounders, reproducibility",
        "question": "Does this change actually move the target metric? ...",
    },
]
```

**Key line**: Each expert has a distinct `focus` and `question` — no overlap. The five cover performance, correctness, security, maintainability, and research validity. A change that passes all five is genuinely low-risk.

---

## Step 2: Define the prompt template

```python
PROMPT_TEMPLATE = """\
=== Expert {n}: {name} ===
Focus area : {focus}

Change description:
  {change}

Your task:
  {question}

Respond with:
  PREDICTION : <one-sentence prediction of outcome>
  RISK LEVEL : low | medium | high
  TOP CONCERN: <the single most important thing to verify>
  SUGGESTED CHECK: <a concrete test or measurement to run>
"""
```

**Key line**: The structured response format (`PREDICTION`, `RISK LEVEL`, `TOP CONCERN`, `SUGGESTED CHECK`) makes the outputs comparable across personas and easy to synthesize.

---

## Step 3: Generate all five prompts for the given change

```python
def generate_prompts(change: str) -> None:
    wrapped = textwrap.fill(change, width=72, subsequent_indent="  ")
    print(f"Change: {change}\n")
    for i, expert in enumerate(EXPERTS, 1):
        print(PROMPT_TEMPLATE.format(
            n=i,
            name=expert["name"],
            focus=expert["focus"],
            change=wrapped,
            question=textwrap.fill(expert["question"], width=68,
                                   subsequent_indent="  "),
        ))

def main():
    if len(sys.argv) > 1:
        change = " ".join(sys.argv[1:])
    else:
        change = input("Describe the change you are about to make: ").strip()
        if not change:
            change = "Replaced linear scan with binary search in lookup function"
    generate_prompts(change)
```

**Key line**: Each prompt is independent — paste each one into a separate Claude call. If you paste them into the same session, the later personas will be influenced by the earlier ones (herding). Cold start matters.

---

## Try Changing It

1. Run the script for a change you're planning in your own project — which persona's `TOP CONCERN` surprised you most?
2. Find the "Research Validity Expert" prompt — why does this persona matter specifically for autoresearch loops?
3. In the lecture, "minority views" (1/5 experts) are described as the most valuable output. Which persona most often produces minority views, and why?
4. Add a sixth persona: "User Experience Advocate" — write their `focus` and `question` fields, and add them to `EXPERTS`.
