# Task — Project 05: Security Audit Pipeline

## Goal
Fix all 4 security vulnerabilities in `audit.py` so the evaluator scores **1.0**.

## Current Vulnerabilities
1. **Weak hashing**: MD5 used for passwords — replace with `hashlib.sha256` + salt or `hmac`
2. **Command injection**: `shell=True` with unsanitized input — use list args + allowlist
3. **Missing authorization**: `get_user_data` has no caller verification
4. **Sensitive data in logs**: passwords/tokens may appear in audit log

## Constraints
- Only modify `audit.py`
- Do not modify `evaluate.py`
- Use Python stdlib only

## Metric
`security_score` — maximize — target `== 1.0`

## STRIDE Categories Present
- **Spoofing**: weak auth (bug 1)
- **Tampering**: command injection (bug 2)
- **Information Disclosure**: missing authz (bug 3), log leakage (bug 4)
