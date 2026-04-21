"""
Optimized: Fourier basis fit (sin/cos terms up to degree 5).
Reaches RMSE < 0.05 on 500 noisy sine data points.
"""
import math

def generate_data(n=500, seed=42):
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

def _basis(x, degree=5):
    feats = [1.0]
    for k in range(1, degree + 1):
        feats.append(math.sin(k * x))
        feats.append(math.cos(k * x))
    return feats

def _lstsq(A, b):
    # Normal equations: (A^T A) w = A^T b
    n, p = len(A), len(A[0])
    AtA = [[sum(A[i][k] * A[i][j] for i in range(n)) for j in range(p)] for k in range(p)]
    Atb = [sum(A[i][k] * b[i] for i in range(n)) for k in range(p)]
    # Gaussian elimination
    for col in range(p):
        pivot = max(range(col, p), key=lambda r: abs(AtA[r][col]))
        AtA[col], AtA[pivot] = AtA[pivot], AtA[col]
        Atb[col], Atb[pivot] = Atb[pivot], Atb[col]
        for row in range(col + 1, p):
            if AtA[col][col] == 0:
                continue
            f = AtA[row][col] / AtA[col][col]
            for j in range(col, p):
                AtA[row][j] -= f * AtA[col][j]
            Atb[row] -= f * Atb[col]
    w = [0.0] * p
    for i in range(p - 1, -1, -1):
        w[i] = (Atb[i] - sum(AtA[i][j] * w[j] for j in range(i + 1, p))) / AtA[i][i]
    return w

def fit_model(xs, ys):
    A = [_basis(x) for x in xs]
    w = _lstsq(A, ys)
    return lambda x: sum(wi * fi for wi, fi in zip(w, _basis(x)))

def predict(model, xs):
    return [model(x) for x in xs]

def rmse(ys_true, ys_pred):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(ys_true, ys_pred)) / len(ys_true))
