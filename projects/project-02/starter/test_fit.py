"""Correctness tests for fit.py — do not modify."""
import math
from fit import generate_data, fit_model, predict, rmse

def test_generates_500_points():
    xs, ys = generate_data(500)
    assert len(xs) == 500
    assert len(ys) == 500

def test_xs_in_range():
    xs, _ = generate_data(500)
    assert all(0 <= x <= 2 * math.pi for x in xs)

def test_model_returns_callable():
    xs, ys = generate_data(100)
    model = fit_model(xs, ys)
    assert callable(model)

def test_predict_length():
    xs, ys = generate_data(100)
    model = fit_model(xs, ys)
    preds = predict(model, xs)
    assert len(preds) == len(xs)

def test_rmse_perfect():
    ys = [1.0, 2.0, 3.0]
    assert rmse(ys, ys) == 0.0

def test_rmse_known():
    assert abs(rmse([0, 0], [1, 1]) - 1.0) < 1e-9
