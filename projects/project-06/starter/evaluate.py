"""
Evaluator for Project 06.
Measures mean ROUGE-1 recall of summarize() across the test corpus.
Contract: print {"pass": bool, "score": float} then exit 0.
"""
import json, sys
from pipeline import summarize, rouge1_recall
from corpus import CORPUS

TARGET = 0.60

scores = [rouge1_recall(summarize(item["doc"]), item["ref"]) for item in CORPUS]
score = round(sum(scores) / len(scores), 4)
passed = score >= TARGET

print(json.dumps({"pass": passed, "score": score}))
sys.exit(0)
