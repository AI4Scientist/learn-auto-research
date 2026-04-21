# research.md — Project 01 Solution

## Goal
Reduce `sort_items()` median execution time on 1M integers below 0.5 s.

## Metric
`median_time_s` — minimize — target `< 0.5`

## History

| iter | commit | median_time_s | delta | status | description |
|------|--------|---------------|-------|--------|-------------|
| 0 | baseline | 2.41 | — | keep | recursive quicksort (starter) |
| 1 | a1b2c3d | 1.83 | -0.58 | keep | iterative quicksort, no recursion |
| 2 | e4f5g6h | 1.12 | -0.71 | keep | Python built-in sorted() |
| 3 | i7j8k9l | 0.87 | -0.25 | keep | radix sort base 256 |
| 4 | m0n1o2p | 0.57 | -0.30 | keep | radix sort base 65536 |
| 5 | q3r4s5t | 0.49 | -0.08 | keep ✓ | micro-optimized radix, target met |

## Final Result
`median_time_s = 0.49` — target `< 0.5` ✓  
Iterations used: 5 / 20
