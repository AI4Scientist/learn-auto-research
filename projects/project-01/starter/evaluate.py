"""
Evaluator for Project 01.
Measures median execution time of sort_items() on 1M integers.
Contract: print {"pass": bool, "score": float} then exit 0.
"""
import json, sys, timeit, statistics
from sort import sort_items

N        = 1_000_000
RUNS     = 3
TARGET   = 0.5   # seconds

data = list(range(N - 1, -1, -1))  # worst-case reversed list

times = []
for _ in range(RUNS):
    t = timeit.timeit(lambda: sort_items(data[:]), number=1)
    times.append(t)

score  = round(statistics.median(times), 4)
passed = score < TARGET

print(json.dumps({"pass": passed, "score": score}))
sys.exit(0)
