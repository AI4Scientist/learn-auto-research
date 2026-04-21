# 第九讲 — STRIDE+OWASP 自动安全审计

`L01 > L02 > L03 > L04 > L05 > L06 | L07 > L08 > [ L09 ] L10 > L11 > L12`

> *"每项发现必须有代码级证据。"* — 没有文件名和行号的安全发现不是发现，是猜测。
>
> **本讲核心**：`/autoresearch:security` 如何用 STRIDE 威胁建模 + OWASP Top 10 + 四种红队角色，把主观安全审计变成基于证据的可重复过程。

代码示例：[code/](./code/)  
配套项目：[项目五 — 安全审计流水线](/zh/projects/project-05-security-audit-pipeline/)

---

## 问题

传统安全审计昂贵、缓慢且主观。审计质量取决于审计员的经验和当天的注意力——同一个代码库，两次审计结果可能大相径庭。更糟糕的是，"这里可能有问题"这样的发现毫无可操作性。

## 解决方案

```
代码库
  |
  v
阶段1: STRIDE 威胁建模
  6类威胁系统性扫描
  → 资产清单 + 信任边界图
  |
  v
阶段2: OWASP Top 10 扫描
  10类漏洞逐一搜索代码模式
  → 带代码位置的发现列表
  |
  v
阶段3: 四种红队角色
  机会主义攻击者 | 内部威胁
  国家级攻击者   | 脚本小子
  → 多元攻击视角验证
  |
  v
7个结构化输出文件
  每项发现: 文件:行号 + 攻击场景 + 严重级别 + 修复代码
```

## 工作原理

**阶段 1：STRIDE 威胁建模**

| 字母 | 威胁类型 | 典型问题 |
|------|---------|---------|
| S | 欺骗（Spoofing） | JWT 未验证签名？ |
| T | 篡改（Tampering） | API 响应未签名？ |
| R | 抵赖（Repudiation） | 管理员操作有审计日志吗？ |
| I | 信息泄露（Information Disclosure） | 500 响应返回了堆栈追踪吗？ |
| D | 拒绝服务（Denial of Service） | 用户输入能触发无限循环吗？ |
| E | 权限提升（Elevation of Privilege） | 每个敏感操作都验证了角色吗？ |

**阶段 2：OWASP Top 10 代码模式搜索**

```python
# agent 在代码库中搜索这些模式
危险模式 = [
    "f\"SELECT",           # SQL 注入
    "shell=True",          # 命令注入
    "DEBUG=True",          # 安全配置错误
    "requests.get(url",    # 未验证的 SSRF
    "pickle.loads(",       # 不安全反序列化
]
```

**证据要求（强制）**

```markdown
## 发现 #1
- 文件: src/api/users.py:147
- 代码: cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
- 攻击场景: 攻击者传入 `1 OR 1=1` 获取所有用户数据
- 严重级别: Critical
- 修复: cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
```

没有文件:行号，发现无效。

**CI/CD 集成**

```bash
# 在 CI 中作为质量门禁
/autoresearch:security --fail-on High   # 发现 High/Critical 时退出码 1

# 增量扫描（只审计变更的文件）
/autoresearch:security --diff           # 比完整扫描快 10 倍
```

## 变更内容

| 方式 | 传统审计 | `/autoresearch:security` |
|------|---------|------------------------|
| 覆盖一致性 | 取决于审计员 | STRIDE + OWASP 100% 系统覆盖 |
| 证据要求 | 无 | 文件:行号 + 攻击场景（强制） |
| 可重复性 | 不同审计员结果不同 | 相同代码库结果可复现 |
| CI 集成 | 手动 | `--fail-on` + `--diff` 自动化 |

## 试一试

运行 STRIDE 矩阵生成器和 OWASP 检查清单：

```sh
cd docs/zh/lectures/lecture-09-stride-owasp-security/code
python stride_matrix.py "我的 API 服务"
python owasp_checklist.py
```

思考题：

1. 在 `stride_matrix.py` 的输出里，哪个威胁类别和你的项目最相关？
2. `owasp_checklist.py` 列出的代码模式中，哪些你在自己的代码里见过？
3. 为什么"理论上可能有 SQL 注入"不是有效发现，而"users.py:147 行的 f-string 查询"是？
4. 如果你要把安全审计加入 CI，`--fail-on` 应该设置为什么级别？为什么？

---

**下一讲**：[第十讲 — 12维场景探索](/zh/lectures/lecture-10-twelve-dimension-scenarios/)
