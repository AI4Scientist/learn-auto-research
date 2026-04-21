# research.md — Project 05 Solution

## History

| iter | commit | security_score | delta | status | description |
|------|--------|----------------|-------|--------|-------------|
| 0 | baseline | 0.00 | — | keep | all 4 vulns present |
| 1 | a1b2c3d | 0.25 | +0.25 | keep | replace MD5 → HMAC-SHA256 |
| 2 | e4f5g6h | 0.50 | +0.25 | keep | fix command injection (allowlist) |
| 3 | i7j8k9l | 0.75 | +0.25 | keep | add authorized_caller param |
| 4 | m0n1o2p | 1.00 | +0.25 | keep ✓ | document log_event redaction policy |

## Final Result
`security_score = 1.0` — all 4 checks pass ✓
