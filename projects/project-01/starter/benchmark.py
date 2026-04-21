#!/usr/bin/env python3
"""
Evaluator for sort optimization.
Outputs: {"pass": bool, "score": float}
score = median_time_s (lower is better)
"""
import json, statistics, time, random, sys
from sort import sort_numbers

TARGET = 0.5
N_RUNS = 3
N_ELEMENTS = 1_000_000

times = []
for run in range(N_RUNS):
    data = [random.randint(0, 10_000_000) for _ in range(N_ELEMENTS)]
    t0 = time.perf_counter()
    sort_numbers(data)
    elapsed = time.perf_counter() - t0
    times.append(elapsed)

median = statistics.median(times)
passed = median < TARGET

print(json.dumps({"pass": passed, "score": round(median, 4)}))
sys.exit(0)
