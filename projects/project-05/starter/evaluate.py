"""
Evaluator for Project 05.
Runs a static security checklist and scores fixes.
Contract: print {"pass": bool, "score": float} then exit 0.
"""
import json, sys, ast, pathlib

src = pathlib.Path("audit.py").read_text()

checks = {
    "no_md5":          "md5" not in src,
    "no_shell_true":   "shell=True" not in src,
    "has_authz_check": "caller" in src or "requester" in src or "authorized" in src,
    "no_password_log": "password" not in src.lower() or "log_event" not in src,
}

score = round(sum(checks.values()) / len(checks), 4)
passed = score >= 1.0

print(json.dumps({"pass": passed, "score": score, "checks": checks}))
sys.exit(0)
