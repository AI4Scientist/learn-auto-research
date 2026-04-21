# 项目 02 — 从基线到最优


**配套讲座**：[第 03 讲](/zh/lectures/lecture-03-five-stage-loop-internals/) + [第 04 讲](/zh/lectures/lecture-04-what-to-do-when-stuck/)  
**起始代码**：[projects/project-02/starter/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-02/starter/)  
**参考答案**：[projects/project-02/solution/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-02/solution/)

---

## 你将构建什么

一个函数拟合实验：发现生成某数据集的隐藏数学函数。目标 RMSE < 0.05。循环会在中间局部最优处卡住——你将亲身观察 L1 枢轴策略的实际运行。

## 学习目标

- 为非平凡指标（RMSE）编写自定义评估器
- 通过详细阅读 `research_log.md` 观察五阶段循环内部机制
- 体验 L1 枢轴（连续 3 次无改进迭代）
- 理解智能体如何读取 git 历史以避免重复尝试失败的方法

## 起始状态

```
projects/project-02/starter/
├── predict.py        ← 你的模型（从线性回归开始）
├── generate_data.py  ← 生成训练/测试数据（只读）
├── train_data.csv    ← 训练数据
├── test_data.csv     ← 测试数据
├── evaluate.py       ← RMSE 评估器（已写好）
└── research.md       ← 预配置了目标和约束
```

隐藏函数形式为 `y = f(x₁, x₂)`。起始 `predict.py` 使用线性回归——RMSE 约为 2.1。目标是 RMSE < 0.05。

## 第 1 步 — 确认基线

```bash
python evaluate.py
# {"pass": false, "score": 2.1147}
```

基线已确认。循环启动时智能体将从 `research.md` 读取这个值。

## 第 2 步 — 运行循环

```bash
/autoresearch
```

观察 L1 枢轴的出现。在优化多项式特征约 5 次迭代后，智能体会遇到连续 3 次无改进并切换策略。注意它枢轴到了什么方向。

## 关键观察点

在第 8 次迭代后读取 `research_log.md`，你应该看到类似以下内容：

```
## Iteration 7
Hypothesis: degree-6 polynomial should capture more curvature
Result: RMSE = 0.31 — DISCARD (worse than best: 0.28)

## Iteration 8 [L1 PIVOT]
History analysis: tried linear (2.1), quadratic (0.8), cubic (0.41), degree-4 (0.29),
degree-5 (0.28), degree-6 (0.31). Polynomial family appears saturated.
New direction: try interaction terms and non-polynomial features (log, sqrt, exp).
Hypothesis: log(x₁) * x₂ interaction may capture the hidden function structure.
Result: RMSE = 0.12 — KEEP
```

从多项式到交互项的枢轴正是 L1 策略：相同范式（特征工程），不同方向。

## 预期结果

```
Final best: rmse = 0.028
Target: < 0.05 ✓
Iterations used: ~12 of 20
```

## 验证

```bash
python evaluate.py
# {"pass": true, "score": 0.028}

git log --oneline | head -15
# Shows the full experiment history
```
