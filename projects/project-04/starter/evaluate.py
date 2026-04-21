"""
Evaluator for Project 04.
Scores both architectures and returns the weighted total of the recommended one.
Contract: print {"pass": bool, "score": float} then exit 0.
"""
import json, sys
from arch import score_architecture, weighted_total

WEIGHTS = {
    "throughput_score": 0.30,
    "latency_score":    0.25,
    "ops_score":        0.20,
    "scale_score":      0.15,
    "resilience_score": 0.10,
}
TARGET = 0.65

scores_a = score_architecture("monolith")
scores_b = score_architecture("microservices")
best = max([scores_a, scores_b], key=lambda s: weighted_total(s, WEIGHTS))
score = round(weighted_total(best, WEIGHTS), 4)
passed = score >= TARGET

print(json.dumps({"pass": passed, "score": score, "recommended": best["name"]}))
sys.exit(0)
