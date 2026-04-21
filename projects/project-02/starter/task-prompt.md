# Task — Project 02: Baseline to Optimal

## Goal
Reduce the RMSE of `fit_model()` on 500 noisy sine data points below **0.05**.

## Current State
`fit.py` uses a degree-1 linear fit. RMSE ≈ 0.32.

## Constraints
- Only modify `fit.py`
- Do not modify `test_fit.py` or `evaluate.py`
- Use Python stdlib only (no numpy, scipy, etc.)
- The function signatures must remain the same

## Metric
`rmse` — minimize — target `< 0.05`

## Suggested Directions
- Increase polynomial degree (Taylor / Chebyshev basis)
- Implement a cubic spline
- Use Fourier basis functions (sin/cos terms)
