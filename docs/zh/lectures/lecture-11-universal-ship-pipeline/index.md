# 第十一讲 — 通用发布流水线

`L01 > L02 > L03 > L04 > L05 > L06 | L07 > L08 > L09 > L10 > [ L11 ] L12`

> *"人工确认只需要一次，在所有不可逆操作之前。"* — 8个阶段，7个自动，1个等你点头。
>
> **本讲核心**：`/autoresearch:ship` 如何用机械可验证的检查清单和强制确认关卡，让任何制品从"就绪"到"已部署"都有完整记录和可回滚路径。

代码示例：[code/](./code/)  
配套项目：[项目六 — 端到端研究项目](/zh/projects/project-06-end-to-end-research/)

---

## 问题

研究只有在结果被发布后才算完成。但发布步骤容易出错：遗漏检查项、跳过验证、没有记录——出了问题无法回滚，也不知道哪一步出了问题。

更糟糕的是，"检查清单"往往是主观的："看起来没问题"不是一个可验证的条件。

## 解决方案

```
阶段1: 识别   → 自动检测发布类型
阶段2: 清单   → 列出所有制品和依赖
阶段3: 检查   → 运行机械可验证的检查命令
阶段4: 准备   → 生成变更日志、标签、描述
阶段5: 演习   → dry-run，预览实际操作
         |
         v
  ┌──────────────┐
  │  阶段6: 确认  │  ← 唯一需要人工输入的阶段
  │  展示所有信息 │    "输入 YES 继续"
  │  等待确认    │
  └──────┬───────┘
         |
阶段7: 发布   → 执行实际操作
阶段8: 验证   → 健康检查 + 写入 ship-log.md
```

## 工作原理

**9 种发布类型，同一框架**

| 发布类型 | 自动操作 |
|---------|---------|
| 代码 PR | 推送分支、创建 PR、请求审阅者 |
| 代码发布 | 升级版本、生成变更日志、打 tag、GitHub Release |
| 部署 | 构建容器、推送、部署、健康检查 |
| 内容发布 | 验证 Markdown、推送到 CMS |
| 研究成果 | 生成报告、存档数据、发布摘要 |

**机械可验证的检查清单**

```bash
# ✓ 可验证的检查（有明确退出码）
python -m pytest tests/ -q           # 测试通过？
python -c "import evaluate; evaluate.run()"  # 契约满足？
git diff --name-only HEAD~1          # 变更范围确认

# ✗ 不可验证的检查（主观判断）
# "代码看起来没问题"
# "文档应该够用了"
```

**`--rollback` 可逆性**

```bash
# 每次发布都记录足够的回滚信息
/autoresearch:ship --rollback

# 自动执行对应操作：
# 代码 PR   → git push origin --delete <branch>
# 部署      → kubectl rollout undo deployment/<name>
# 内容发布  → git revert + 重新发布
```

**完整研究流水线**

```bash
/autoresearch:plan       # 定义目标
/autoresearch            # 运行优化循环
/autoresearch:debug      # 发现 bug
/autoresearch:fix        # 修复错误
/autoresearch:security   # 安全审计
/autoresearch:ship       # 发布结果
```

## 变更内容

| 方式 | 手动发布 | `/autoresearch:ship` |
|------|---------|---------------------|
| 检查清单 | 主观，"看起来好" | 机械可验证，每项有退出码 |
| 确认时机 | 随意 | 固定在阶段6，不可跳过 |
| 记录 | 无或不完整 | `ship-log.md` 完整记录 |
| 回滚 | 手动、依赖记忆 | `--rollback` 自动执行 |
| 适用范围 | 仅代码 | 9种制品类型统一框架 |

## 试一试

运行发布检查清单和回滚触发脚本：

```sh
cd docs/zh/lectures/lecture-11-universal-ship-pipeline/code
python ship_checklist.py code-pr
python rollback_trigger.py
```

思考题：

1. `ship_checklist.py` 的输出里，哪些检查通过了，哪些失败了？失败的原因是什么？
2. 为什么第6阶段（人工确认）被设计为唯一的人工干预点，而不是分散在各阶段？
3. 你上次发布代码时，有没有一个步骤是"主观判断"而不是"可验证条件"？那个步骤应该怎么改成可验证的？
4. 如果 `ship-log.md` 不存在，`rollback_trigger.py` 会怎样？这说明什么？

---

**下一讲**：[第十二讲 — 过夜运行与高级模式](/zh/lectures/lecture-12-overnight-runs-advanced/)
