# 第六讲 — 错误归零流水线

`L01 > L02 > L03 > L04 > L05 > [ L06 ] | L07 > L08 > L09 > L10 > L11 > L12`

> *"修复一个错误，可能暴露三个。"* — 级联感知排序让你先修阻塞者，而不是随机乱修。
>
> **本讲核心**：`/autoresearch:fix` 如何用优先级排序和 Guard 防止退化，系统性地把错误计数归零。

代码示例：[code/](./code/)  
配套项目：[项目三 — 调试真实故障](/zh/projects/project-03-debug-real-failure/)

---

## 问题

调试是调查——你不知道哪里出了问题。修复是修缮——你已有错误清单，目标是归零。

但修复有个陷阱：**级联问题**。修复错误 A 可能暴露原本被掩盖的错误 B，修复 B 可能破坏原本通过的错误 C。随机修复顺序会让你原地转圈。

## 解决方案

```
运行验证命令
    |
    v
获取当前错误列表
    |
    v
按优先级排序:
  1. 构建错误（其他一切都依赖它）
  2. 类型错误（阻塞运行时）
  3. 测试失败（功能退化）
  4. 代码风格（最低优先级）
    |
    v
选最高优先级错误 → 单一修改 → git commit
    |
    v
再次运行验证 → 运行 Guard
  通过 → 保留，处理下一个错误
  失败 → git revert，标记为 SKIP，继续
    |
    v
错误计数 == 0？→ 循环自动停止
```

## 工作原理

**1. 为什么"构建错误优先"？**

```
构建错误 → 类型错误 → 测试失败 → 代码风格
    ↑
  阻塞者

如果构建失败，测试根本无法运行。
先修构建错误，后面的错误可能自动消失。
```

**2. 每次只修一个错误**

```python
# ✓ 正确：每次迭代只修一个
fix_one_error(highest_priority_error)
git_commit()
run_validation()   # 验证这个修复没有引入新问题

# ✗ 错误：批量修复
fix_all_type_errors_at_once()   # 出了问题无法归因
```

**3. Guard 防止退化**

```bash
# research.md 中配置
Guard: python -m pytest tests/ -x    # 每次修复后运行完整测试套件

# 如果 Guard 失败：
git revert HEAD    # 撤销这次修复
# 标记为 SKIP，继续处理下一个错误
```

**4. `--from-debug` 链式命令**

```bash
/autoresearch:debug          # 找出所有 bug → findings.md
/autoresearch:fix --from-debug   # 读取 findings.md，跳过发现阶段，直接修复
```

跳过重新发现过程，直接从已确认的根因开始修复。

**5. 不可修复错误处理**

单个错误连续 3 次修复失败 → 记录为 SKIP → 继续处理下一个。防止无限循环，不让一个顽固错误阻塞整个流水线。

## 变更内容

| 方式 | 随机修复 | 级联感知修复 |
|------|---------|-------------|
| 修复顺序 | 随意 | 构建 → 类型 → 测试 → 风格 |
| 每次修改 | 可能多个 | 严格一个 |
| 退化防护 | 无 | Guard 在每次修复后运行 |
| 停止条件 | 人工判断 | 错误计数 == 0 自动停止 |

## 试一试

运行错误排序器和回归检查器，观察级联感知策略：

```sh
cd docs/zh/lectures/lecture-06-error-crushing-pipeline/code
python error_sorter.py
python regression_checker.py
```

思考题：

1. `error_sorter.py` 输出的顺序是什么？如果你随机修复，第一个修的可能是什么？
2. 找一个 Guard 触发 revert 的场景。这次 revert 防止了什么问题？
3. 为什么"每次只修一个"比"批量修复"更容易排查新出现的问题？
4. 你的项目里，Guard 命令应该是什么？写出那行命令。

---

**下一讲**：[第七讲 — 5专家视角预判](/zh/lectures/lecture-07-five-expert-predict/)
