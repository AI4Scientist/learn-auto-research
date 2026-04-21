# L09 代码 — STRIDE + OWASP 安全审计

> 目标：用 STRIDE 矩阵对任意系统做威胁分类，再用 OWASP 检查清单找到代码中的具体危险模式。

运行方式：

```sh
python stride_matrix.py "订单管理 API"
python owasp_checklist.py
```

---

## 工具一：STRIDE 威胁矩阵生成器

### 第一步：定义六类威胁

```python
import textwrap, sys

STRIDE = [
    {
        "letter": "S",
        "threat": "欺骗（Spoofing）",
        "description": "攻击者冒充其他实体",
        "examples": ["未验证签名的 JWT", "缺少发送方身份验证"],
        "audit_question": "所有身份声明是否经过密码学验证？",
    },
    {
        "letter": "T",
        "threat": "篡改（Tampering）",
        "description": "攻击者在传输或存储中修改数据或代码",
        "examples": ["未签名的 API 响应", "状态变更端点上的 CSRF"],
        "audit_question": "所有写操作是否防止了未授权修改？",
    },
    {
        "letter": "R",
        "threat": "抵赖（Repudiation）",
        "description": "用户否认执行了敏感操作",
        "examples": ["管理员操作缺少审计日志", "写操作没有时间戳"],
        "audit_question": "敏感操作是否记录了用户身份和时间戳？",
    },
    {
        "letter": "I",
        "threat": "信息泄露（Information Disclosure）",
        "description": "敏感数据暴露给未授权方",
        "examples": ["500 响应中返回堆栈追踪", "API 响应过度获取"],
        "audit_question": "响应中是否包含了调用方不应看到的数据？",
    },
    {
        "letter": "D",
        "threat": "拒绝服务（Denial of Service）",
        "description": "攻击者使服务不可用",
        "examples": ["用户输入触发无限循环", "缺少速率限制"],
        "audit_question": "单个客户端能否压垮任何端点？",
    },
    {
        "letter": "E",
        "threat": "权限提升（Elevation of Privilege）",
        "description": "攻击者获得超出预期的权限",
        "examples": ["资源端点上的 IDOR", "缺少授权检查"],
        "audit_question": "每个敏感操作是否验证了调用者的角色？",
    },
]
```

**关键行**：每个威胁都有 `audit_question` — 这是审计时真正要在代码库里验证的问题，不是理论描述。

---

### 第二步：渲染威胁矩阵

```python
def render_matrix(system_name: str = "目标系统") -> None:
    print(f"STRIDE 威胁矩阵 — {system_name}")
    print("=" * 72)

    for item in STRIDE:
        print(f"\n[{item['letter']}] {item['threat']}")
        print(f"    威胁描述 : {item['description']}")
        print(f"    典型例子 : {', '.join(item['examples'])}")
        wrapped_q = textwrap.fill(
            item["audit_question"], width=60,
            subsequent_indent="             "
        )
        print(f"    审计问题 : {wrapped_q}")

    print()
    print("下一步：针对以上每类威胁，在代码库中搜索相关模式，")
    print("将发现映射到 OWASP Top 10 类别。")

def main():
    name = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "目标系统"
    render_matrix(name)

if __name__ == "__main__":
    main()
```

---

## 工具二：OWASP Top 10 检查清单

### 第一步：定义十类漏洞和对应代码模式

```python
OWASP_TOP_10 = [
    {
        "rank": 1,
        "name": "访问控制失效",
        "patterns": ["缺少 @login_required", "/api/ 上的 IDOR", "路径穿越 ../"],
        "severity": "Critical",
    },
    {
        "rank": 2,
        "name": "加密失败",
        "patterns": ["MD5(", "SHA1(", "配置中的 http://", "明文密码"],
        "severity": "High",
    },
    {
        "rank": 3,
        "name": "注入",
        "patterns": ['f"SELECT', "execute(query +", "shell=True", "eval("],
        "severity": "Critical",
    },
    {
        "rank": 4,
        "name": "不安全设计",
        "patterns": ["无速率限制", "直接对象引用", "缺少 CSRF token"],
        "severity": "High",
    },
    {
        "rank": 5,
        "name": "安全配置错误",
        "patterns": ["DEBUG=True", "默认密码", "详细错误信息", "CORS *"],
        "severity": "High",
    },
    {
        "rank": 6,
        "name": "易受攻击的组件",
        "patterns": ["requirements.txt", "package.json", "过期的固定版本"],
        "severity": "High",
    },
    {
        "rank": 7,
        "name": "身份验证失败",
        "patterns": ["无 MFA", "弱密码策略", "会话固定", "无注销"],
        "severity": "High",
    },
    {
        "rank": 8,
        "name": "软件完整性失败",
        "patterns": ["pickle.loads(", "yaml.load(", "deserialize(", "无校验和"],
        "severity": "High",
    },
    {
        "rank": 9,
        "name": "日志记录失败",
        "patterns": ["无审计日志", "日志中的敏感数据", "日志注入"],
        "severity": "Medium",
    },
    {
        "rank": 10,
        "name": "SSRF",
        "patterns": ["requests.get(url", "urllib.request", "未验证的重定向"],
        "severity": "High",
    },
]
```

**关键行**：`"patterns"` 字段 — 这些是可以直接在代码库里 `grep` 的字符串，把安全审计变成可执行的搜索任务。

---

### 第二步：打印检查清单

```python
def print_checklist() -> None:
    print("OWASP Top 10 — 审计检查清单")
    print("=" * 70)
    print(f"{'#':<4} {'类别':<22} {'严重级别':<10} 需搜索的代码模式")
    print("-" * 70)
    for item in OWASP_TOP_10:
        # 只显示前两个模式，避免一行太长
        patterns_str = " | ".join(item["patterns"][:2])
        print(f"{item['rank']:<4} {item['name']:<22} {item['severity']:<10} {patterns_str}")
    print()
    print("对每一行：在代码库中搜索模式，发现时记录：")
    print("  文件:行号 + 具体攻击场景 + 严重级别评估")

if __name__ == "__main__":
    print_checklist()
```

---

## 动手改一改

1. 运行 `stride_matrix.py "用户登录服务"`，哪个威胁类别和登录功能最相关？
2. 在 `OWASP_TOP_10` 里，找到 `"注入"` 条目。在你自己的代码里搜索 `f"SELECT` — 找到了吗？
3. 给 STRIDE 的 `"I"（信息泄露）`条目添加一个新的 `examples`：你的项目里最可能出现的信息泄露场景是什么？
4. 为什么"可能有 SQL 注入"不是有效发现，而"`users.py:147` 行的 f-string 查询"是？用一句话解释。
