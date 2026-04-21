"""
Starter: fit a degree-1 polynomial to noisy sine data.
Goal: reduce RMSE below 0.05 by improving the model.
"""
import math

def generate_data(n=500, seed=42):
    # LCG pseudo-random for stdlib-only noise
    a, c, m = 1664525, 1013904223, 2**32
    state = seed
    xs, ys = [], []
    for i in range(n):
        x = i / n * 2 * math.pi
        state = (a * state + c) % m
        noise = (state / m - 0.5) * 0.1
        xs.append(x)
        ys.append(math.sin(x) + noise)
    return xs, ys

def fit_model(xs, ys):
    """Linear fit — intentionally underpowered."""
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxx = sum(x * x for x in xs)
    slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    intercept = (sy - slope * sx) / n
    return lambda x: slope * x + intercept

def predict(model, xs):
    return [model(x) for x in xs]

def rmse(ys_true, ys_pred):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(ys_true, ys_pred)) / len(ys_true))
