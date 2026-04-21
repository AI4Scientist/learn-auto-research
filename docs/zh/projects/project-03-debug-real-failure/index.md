# 项目 03 — 调试真实故障


**配套讲座**：[第 05 讲](/zh/lectures/lecture-05-scientific-debugging/) + [第 06 讲](/zh/lectures/lecture-06-error-crushing-pipeline/)  
**起始代码**：[projects/project-03/starter/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-03/starter/)  
**参考答案**：[projects/project-03/solution/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-03/solution/)

---

## 你将构建什么

调试一个在 POST /users 上间歇性返回 503 错误的 FastAPI 服务。使用 `/autoresearch:debug` 进行调查，然后用 `/autoresearch:fix` 修复。

## 学习目标

- 使用可证伪的假设运行科学调试会话
- 阅读 `hypotheses.md` 和 `eliminated.md`，了解哪些被排除
- 使用 `--from-debug` 链接调试→修复
- 验证修复消除了症状

## 起始状态

```
projects/project-03/starter/
├── app/
│   ├── main.py          ← FastAPI 应用
│   ├── models.py        ← SQLAlchemy 模型
│   ├── database.py      ← 数据库连接（包含 bug）
│   └── routers/
│       └── users.py     ← 用户端点
├── tests/
│   └── test_users.py    ← 集成测试
├── requirements.txt
└── README.md
```

该服务对大多数请求正常工作，但约 30% 的 POST /users 请求返回 503。bug 是故意植入的。

## 第 1 步 — 复现 bug

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload &

# Run load test
python tests/load_test.py
# Expected: ~30% 503 errors
```

## 第 2 步 — 调试

```bash
/autoresearch:debug
Scope: app/
Symptom: POST /users returns 503 ~30% of requests
Iterations: 15
```

智能体将调查 FastAPI 应用，逐一形成并测试假设。

## 第 3 步 — 修复

```bash
/autoresearch:fix --from-debug
```

修复循环读取调试会话中已确认的发现，并修复根本原因。

## 预期调试输出

调试会话结束后，`hypotheses.md` 应包含 3-5 条带证据的假设。`eliminated.md` 应列出被排除的内容。`findings.md` 应标识根本原因。

## 验证

```bash
python tests/load_test.py
# Expected: 0 503 errors

python -m pytest tests/
# Expected: all tests pass
```

## bug 是什么（调试前请勿阅读）

<details>
<summary>揭示 bug</summary>

`database.py` 中数据库连接池大小设置为 2。在中等负载下，所有连接耗尽，导致新请求以 503 失败。修复方案：将连接池大小增加到 10，并添加连接超时处理。

</details>
