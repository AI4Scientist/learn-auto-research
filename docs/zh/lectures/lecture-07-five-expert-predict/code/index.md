# L07 代码 — 5专家视角预判

> 目标：为任意变更生成五个专家角色的分析提示词，体验"冷启动独立分析"如何发现单视角遗漏的问题。

运行方式：

```sh
python five_expert_predict.py "为查询层新增了 LRU 缓存"
# 或交互式
python five_expert_predict.py
```

---

## 第一步：定义五个专家角色

```python
import sys, textwrap

EXPERTS = [
    {
        "name": "性能工程师",
        "icon": "⚡",
        "focus": "延迟、吞吐量、内存、CPU、缓存行为",
        "question": (
            "这个改变对性能有什么影响？"
            "在高负载下会降低延迟还是吞吐量？"
            "有没有隐藏的内存分配或 GC 开销？"
        ),
    },
    {
        "name": "正确性审查员",
        "icon": "🔍",
        "focus": "边界情况、差一错误、并发、数据完整性",
        "question": (
            "这个改变可能在哪里引入 bug？"
            "哪些边界情况没有被处理？"
            "竞态条件或状态变更可能导致无声失败吗？"
        ),
    },
    {
        "name": "安全分析师",
        "icon": "🛡️",
        "focus": "注入、认证绕过、数据泄露、供应链风险",
        "question": (
            "这个改变是否扩大了攻击面？"
            "不可信输入能触达敏感代码路径吗？"
            "存在权限提升或信息泄露风险吗？"
        ),
    },
    {
        "name": "可维护性倡导者",
        "icon": "🧹",
        "focus": "可读性、耦合度、可测试性、未来改动成本",
        "question": (
            "这个改变如何影响长期可维护性？"
            "是否引入了紧耦合或隐式依赖？"
            "未来的工程师能理解并扩展它吗？"
        ),
    },
    {
        "name": "研究有效性专家",
        "icon": "📊",
        "focus": "指标合理性、混杂因素、可复现性、统计有效性",
        "question": (
            "这个改变真的以有意义的方式改善了目标指标吗？"
            "测量到的改进可能是混杂因素或测量误差吗？"
            "评估方法足够可靠吗？"
        ),
    },
]
```

**关键行**：每个专家有独立的 `focus` 和 `question`，互不重叠 — 确保五个视角加起来覆盖完整的风险空间。

---

## 第二步：生成提示词模板

```python
PROMPT_TEMPLATE = """\
=== 专家 {n}: {icon} {name} ===
关注领域: {focus}

变更描述:
  {change}

你的任务:
  {question}

请回答:
  预测结果  : <一句话预测结果>
  风险等级  : 低 | 中 | 高
  最大关注点: <最重要的一件需要验证的事>
  建议检查  : <一个具体的测试或测量方法>
"""
```

---

## 第三步：为每个角色生成独立提示词

```python
def generate_prompts(change: str) -> None:
    print(f"变更描述: {change}\n")
    print("=" * 72)
    print("以下每个代码块是一个独立的 Claude 调用提示词。")
    print("关键：每个角色单独调用，不看其他角色的输出（冷启动）。\n")

    for i, expert in enumerate(EXPERTS, 1):
        wrapped_change   = textwrap.fill(change, width=68, subsequent_indent="  ")
        wrapped_question = textwrap.fill(expert["question"], width=68, subsequent_indent="  ")
        print(PROMPT_TEMPLATE.format(
            n=i,
            icon=expert["icon"],
            name=expert["name"],
            focus=expert["focus"],
            change=wrapped_change,
            question=wrapped_question,
        ))

def main():
    if len(sys.argv) > 1:
        change = " ".join(sys.argv[1:])
    else:
        change = input("描述你即将做的改变: ").strip()
        if not change:
            change = "将线性扫描替换为二分搜索"
    generate_prompts(change)

if __name__ == "__main__":
    main()
```

**关键行**：注释"每个角色单独调用，不看其他角色的输出" — 这不只是注释，是冷启动原则的操作说明。

---

## 预期输出（节选）

```
变更描述: 为查询层新增了 LRU 缓存

=== 专家 1: ⚡ 性能工程师 ===
关注领域: 延迟、吞吐量、内存、CPU、缓存行为

变更描述:
  为查询层新增了 LRU 缓存

你的任务:
  这个改变对性能有什么影响？在高负载下会降低延迟还是吞吐量？
  有没有隐藏的内存分配或 GC 开销？

请回答:
  预测结果  : <一句话预测结果>
  ...
```

---

## 动手改一改

1. 用你最近做的一个真实改动替换 `change` 变量，哪个角色提出了你没想到的问题？
2. 把五个提示词分别粘贴到五个独立的 Claude 对话里，对比合并后的发现与你单独分析时的差异。
3. 找到"研究有效性专家"的问题：如果测量到的改进是测量误差，你怎么验证？
4. 在 `EXPERTS` 里添加一个新角色"用户体验设计师"，它的 `focus` 和 `question` 应该是什么？
