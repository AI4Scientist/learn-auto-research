"""
Evaluator for Project 03.
Runs pytest and counts passing tests.
Contract: print {"pass": bool, "score": float} then exit 0.
"""
import json, sys, subprocess

result = subprocess.run(
    [sys.executable, "-m", "pytest", "test_app.py", "-q", "--tb=no"],
    capture_output=True, text=True
)
output = result.stdout + result.stderr

# Parse "X passed" from pytest output
passed_count = 0
total_count = 6
for line in output.splitlines():
    if "passed" in line:
        try:
            passed_count = int(line.strip().split()[0])
        except (ValueError, IndexError):
            pass

score = round(passed_count / total_count, 4)
passed = passed_count == total_count

print(json.dumps({"pass": passed, "score": score}))
sys.exit(0)
