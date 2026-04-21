# 项目 01 — 你的第一个研究循环


**配套讲座**：[第 01 讲](/zh/lectures/lecture-01-why-manual-iteration-fails/) + [第 02 讲](/zh/lectures/lecture-02-what-is-a-measurable-research-goal/)  
**起始代码**：[projects/project-01/starter/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-01/starter/)  
**参考答案**：[projects/project-01/solution/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-01/solution/)

---

## 你将构建什么

运行经典 autoresearch 示例：将一个 Python 排序函数在 100 万个整数上的执行时间从约 2.4 秒优化到 0.5 秒以下。你将用 `/autoresearch:plan` 搭建项目，用 `/autoresearch` 运行循环。

## 学习目标

完成本项目后，你将能够：
- 将模糊目标（"让它更快"）转化为机械指标（`median_time_s < 0.5`）
- 编写输出 `{"pass": bool, "score": float}` 的评估器
- 运行 5 阶段循环并读懂 `research.md` 的历史记录
- 理解什么被提交、为什么提交

## 起始状态

```
projects/project-01/starter/
├── sort.py          ← 慢速实现（递归快速排序）
├── test_sort.py     ← 正确性测试（不要修改）
└── task-prompt.md   ← 你的任务说明
```

`sort.py` 包含对 100 万个整数的递归快速排序，耗时约 2.4 秒。目标：在不破坏测试的前提下使其低于 0.5 秒。

## 第一步 — 运行规划向导

```bash
cd projects/project-01/starter/
/autoresearch:plan
```

回答向导问题：
- **目标**：将 sort.py 在 100 万整数上的执行时间降到 0.5 秒以下
- **指标**：`median_time_s`，方向：最小化，目标值：`< 0.5`
- **有噪声？** 是——基准测试会有波动。设置 `noise_runs: 3`
- **范围**：仅限 `sort.py`，禁止修改 `test_sort.py`
- **守卫命令**：`python -m pytest test_sort.py`
- **最大迭代次数**：20

向导会生成 `benchmark.py` 和 `research.md`。

## 第二步 — 运行循环

```bash
/autoresearch
```

观察循环运行。3–5 次迭代后你应该看到：

```
| 3 | 基数排序 base 256     | 0.871 | keep    |
| 4 | 基数排序 base 65536   | 0.573 | keep    |
| 5 | 微优化基数排序         | 0.498 | keep ✓  | ← 目标达成
```

## 第三步 — 读取结果

打开 `research.md` 和 `research_log.md`，回答以下问题：
1. 达到目标花了几次迭代？
2. 哪些实验被丢弃了？为什么？
3. git 日志是什么样的？（`git log --oneline`）

## 预期结果

```
最终最优：median_time_s = 0.498
目标：< 0.5 ✓
使用迭代次数：5 / 20
```

## 验证

```bash
python benchmark.py
# 预期：{"pass": true, "score": 0.498}

python -m pytest test_sort.py
# 预期：所有测试通过
```

## 提示

- 如果循环运行很慢，是因为 `noise_runs: 3` 每次迭代运行 3 次基准测试。这是正确行为——基准测试本身有噪声。
- 如果看到 `GUARD FAILED`，说明排序结果不正确。检查是哪个改动破坏了正确性。
- 参考答案目录包含一份完整的 5 次迭代 `research.md` 历史，可以对照比较。
