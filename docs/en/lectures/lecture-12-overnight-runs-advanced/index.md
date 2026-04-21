# Lecture 12 — Overnight Runs & Advanced Patterns

[中文版本 →](/zh/lectures/lecture-12-overnight-runs-advanced/)

Code examples: [code/](./code/)  
Practice project: [Project 06 — End-to-End Research Project](/en/projects/project-06-end-to-end-research/)

---

The real power of autoresearch is what happens while you sleep. This lecture covers running loops unattended overnight, integrating with CI/CD pipelines, using MCP servers during loops, and building custom evaluators for novel domains.

## Overnight Runs

Three modes for long-running unattended loops:

**Foreground with tmux** (recommended):
```bash
tmux new-session -d -s autoresearch
tmux send-keys -t autoresearch "claude -p '/autoresearch' --max-turns 200" Enter
# Detach: Ctrl+B D
# Check progress anytime:
tmux attach -t autoresearch
```

**Background with nohup**:
```bash
nohup claude -p '/autoresearch' --max-turns 200 > autoresearch.log 2>&1 &
echo $! > autoresearch.pid

# Check progress
tail -f autoresearch.log
bash scripts/check_progress.sh ./my-research/
```

**Bash loop script** (when you want shell-level control):
```bash
#!/bin/bash
# autoresearch-loop.sh
RESEARCH_DIR="$1"
MAX_ITER="${2:-100}"

for i in $(seq 1 $MAX_ITER); do
  echo "=== Iteration $i / $MAX_ITER ==="
  claude -p "/autoresearch Iterations: 1" --cwd "$RESEARCH_DIR"
  
  # Check if target was met
  if python check_target.py "$RESEARCH_DIR/research.md"; then
    echo "Target achieved after $i iterations"
    exit 0
  fi
done
echo "Budget exhausted: $MAX_ITER iterations"
```

## Monitoring Progress

The `progress.png` file in the research directory is updated after every iteration. Open it in any image viewer to see the convergence curve.

For terminal monitoring:
```bash
# Watch the results TSV grow
watch -n 30 "tail -20 autoresearch-results.tsv"

# Check current best
python -c "
import csv
with open('autoresearch-results.tsv') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
    kept = [r for r in rows if r['status'] == 'keep']
    if kept:
        best = min(kept, key=lambda r: float(r['score']))  # for minimize
        print(f'Best: {best[\"score\"]} at iteration {best[\"iteration\"]}')
"
```

## MCP Server Integration

Any MCP server configured in Claude Code is available during the loop. This enables powerful research patterns:

**Database queries during evaluation**:
```markdown
# research.md
Evaluator: Use MCP postgres tool to run EXPLAIN ANALYZE on the target query
Metric: query_ms (execution time in milliseconds)
```

**API calls for scoring**:
```markdown
# research.md
Evaluator: Call MCP openai tool to judge prompt quality, average over 5 samples
Metric: llm_judge_score (1-10)
```

**External monitoring**:
```markdown
# research.md  
Guard: Use MCP grafana tool to check error rate < 0.1% for 5 minutes
```

## CI/CD Integration

Running autoresearch as part of CI ensures research quality is maintained automatically:

```yaml
# .github/workflows/research.yml
name: Automated Research

on:
  schedule:
    - cron: '0 2 * * *'  # Run nightly at 2am

jobs:
  research:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run research loop
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "/autoresearch Iterations: 50" --cwd research/
      
      - name: Security audit
        run: |
          claude -p "/autoresearch:security --fail-on High --diff"
      
      - name: Commit progress
        run: |
          git add research/
          git commit -m "chore: nightly research progress" || true
          git push
```

## Building Custom Evaluators

For novel domains, you need custom evaluators. The contract is simple:

```python
#!/usr/bin/env python3
"""
Custom evaluator template.
Must print: {"pass": bool, "score": float}
Must exit 0 on success, non-zero on evaluation failure.
"""
import json, sys

# 1. Run your measurement
score = measure_something()

# 2. Define target
TARGET = 0.95
passed = score >= TARGET  # or <= for minimize

# 3. Output contract
print(json.dumps({"pass": passed, "score": round(score, 4)}))
sys.exit(0)
```

**Example: LLM judge evaluator**:
```python
#!/usr/bin/env python3
import json, anthropic, statistics

client = anthropic.Anthropic()
TARGET = 8.0
N_SAMPLES = 5

with open("prompt.txt") as f:
    prompt = f.read()

scores = []
for _ in range(N_SAMPLES):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": f"Rate this prompt 1-10 for clarity and effectiveness. Reply with only a number.\n\nPrompt: {prompt}"
        }]
    )
    scores.append(float(response.content[0].text.strip()))

median = statistics.median(scores)
print(json.dumps({"pass": median >= TARGET, "score": round(median, 2)}))
```

## The Research → Skill Pipeline

A fully iterated research session produces knowledge that should be encoded as a reusable skill:

```
research.md → final_report.md → SKILL.md
```

The `final_report.md` from a successful autoresearch run contains the winning approach with evidence. This becomes the basis for a Claude Code skill that encodes the knowledge for future use.

Use `/autoresearch:learn` to automate this:
```
/autoresearch:learn --mode init
```
This scans the research output and generates documentation from it.

## Key Takeaways

- tmux is the best overnight runner — you can check progress and it survives disconnects
- `progress.png` gives visual confirmation the loop is working without reading logs
- MCP servers extend what the evaluator can measure — any external system is now a metric source
- CI/CD integration makes research a continuous process, not a one-time event
- Custom evaluators follow a simple contract: run measurement, output `{"pass": bool, "score": float}`
- The research → skill pipeline encodes successful research as reusable knowledge

---

**Course Complete.** You now have the full autoresearch toolkit. Start with [Project 06](/en/projects/project-06-end-to-end-research/) to build a complete pipeline.
