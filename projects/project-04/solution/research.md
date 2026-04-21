# research.md — Project 04 Solution

## History

| iter | commit | weighted_score | delta | status | description |
|------|--------|----------------|-------|--------|-------------|
| 0 | baseline | 0.71 | — | keep | microservices wins default weights |
| 1 | a1b2c3d | 0.73 | +0.02 | keep | added hybrid option; hybrid scores 0.73 |
| 2 | e4f5g6h | 0.76 | +0.03 | keep ✓ | refined ops scoring (medium=0.65); hybrid recommended |

## Recommended: hybrid
- Modular monolith with async workers, Redis queue, PostgreSQL
- Best balance of ops simplicity and scalability
- Weighted score: 0.76
