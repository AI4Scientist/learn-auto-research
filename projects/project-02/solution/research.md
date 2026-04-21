# research.md — Project 02 Solution

## Goal
Reduce RMSE of `fit_model()` below 0.05 on 500 noisy sine data points.

## History

| iter | commit | rmse | delta | status | description |
|------|--------|------|-------|--------|-------------|
| 0 | baseline | 0.320 | — | keep | degree-1 linear fit |
| 1 | a1b2c3d | 0.198 | -0.122 | keep | degree-3 polynomial |
| 2 | e4f5g6h | 0.091 | -0.107 | keep | degree-6 polynomial |
| 3 | i7j8k9l | 0.047 | -0.044 | keep ✓ | Fourier basis degree-5, target met |

## Final Result
`rmse = 0.047` — target `< 0.05` ✓  
Iterations used: 3 / 20
