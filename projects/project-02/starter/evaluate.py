"""
Evaluator for Project 02.
Measures RMSE of fit_model() on sine data.
Contract: print {"pass": bool, "score": float} then exit 0.
"""
import json, sys
from fit import generate_data, fit_model, predict, rmse

TARGET = 0.05

xs, ys = generate_data(n=500)
model = fit_model(xs, ys)
ys_pred = predict(model, xs)
score = round(rmse(ys, ys_pred), 4)
passed = score < TARGET

print(json.dumps({"pass": passed, "score": score}))
sys.exit(0)
