# 项目 05 — 安全审计流水线


**配套讲座**：[第 09 讲](/zh/lectures/lecture-09-stride-owasp-security/) + [第 10 讲](/zh/lectures/lecture-10-twelve-dimension-scenarios/)  
**起始代码**：[projects/project-05/starter/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-05/starter/)  
**参考答案**：[projects/project-05/solution/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-05/solution/)

---

## 你将构建什么

对一个存在漏洞的 Web API 运行完整的安全审计流水线：场景探索发现边缘案例，安全审计识别漏洞，修复循环修复发现的问题。

## 学习目标

- 在 12 个维度上生成全面的测试场景
- 运行带有代码级证据的 STRIDE + OWASP 安全审计
- 链接 scenario → security → fix
- 解读严重性评级并确定修复优先级

## 起始状态

```
projects/project-05/starter/
├── api/
│   ├── main.py          ← FastAPI 应用（故意植入漏洞）
│   ├── auth.py          ← 认证（存在问题）
│   ├── users.py         ← 用户管理（存在问题）
│   └── items.py         ← 条目 CRUD（存在问题）
├── tests/
└── requirements.txt
```

该 API 在代码库中植入了 3-5 个故意的漏洞。

## 第 1 步 — 场景探索

```bash
/autoresearch:scenario
Scenario: User authenticates and manages their items
Domain: security
Format: threat-scenarios
Iterations: 20
```

这将在所有 12 个维度上生成 20 个威胁场景。输出将作为安全审计的输入。

## 第 2 步 — 安全审计

```bash
/autoresearch:security
Iterations: 15
```

审计运行 STRIDE 建模、OWASP 扫描和 4 个红队角色。每个发现都包含文件:行号的证据。

## 第 3 步 — 修复严重/高危发现

```bash
/autoresearch:fix
Guard: python -m pytest tests/
```

修复审计中识别的严重和高危漏洞。

## 预期审计发现

起始 API 包含：
- 用户搜索中的 SQL 注入（严重）
- 条目删除缺少授权检查（高危）
- 错误响应中的敏感数据泄露（中危）

（根据分析深度可能发现更多。）

## 验证

```bash
# Re-run security audit on fixed code
/autoresearch:security --diff

# Should show: no Critical findings, no High findings
```
