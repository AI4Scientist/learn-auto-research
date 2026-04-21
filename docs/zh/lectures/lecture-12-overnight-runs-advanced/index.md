# 第十二讲 — 过夜运行与高级模式

`L01 > L02 > L03 > L04 > L05 > L06 | L07 > L08 > L09 > L10 > L11 > [ L12 ]`

> *"你在睡觉，循环在复利。"* — 真正的力量不是一次迭代有多快，而是一夜能跑多少次。
>
> **本讲核心**：tmux 过夜运行、MCP 服务器作为指标来源、CI/CD 定时研究、自定义评估器契约，以及把成功研究编码成可复用技能。

代码示例：[code/](./code/)  
配套项目：[项目六 — 端到端研究项目](/zh/projects/project-06-end-to-end-research/)

---

## 问题

运行 20 次迭代很简单。运行 100 次、在你睡着的时候、出了问题能自己恢复、结果能被下周的你理解——这才是真正的挑战。

## 解决方案

```
本地过夜运行                CI/CD 定时研究
─────────────────           ─────────────────────────
tmux new -s research        GitHub Actions schedule:
  /autoresearch             cron: '0 2 * * *'  (每晚2点)
    迭代 1                    run: /autoresearch
    迭代 2                    自动提交进度到仓库
    ...
    迭代 100                MCP 服务器作为指标来源
[detach]  ← 断开，继续睡   ─────────────────────────
                            evaluate.py 可以调用:
第二天:                       MCP postgres → EXPLAIN ANALYZE
tmux attach -t research     MCP openai   → LLM 质量评分
  查看 progress.png         MCP grafana  → 生产错误率
```

## 工作原理

**1. tmux 过夜运行（推荐方式）**

```bash
# 开始
tmux new -s research
/autoresearch:plan      # 先定义目标
# 在 research.md 里设好 max_iterations: 100
/autoresearch           # 启动循环
# Ctrl+b d              # 分离会话，关掉终端，去睡觉

# 第二天
tmux attach -t research # 重新连接
# 或者直接看图
open progress.png       # 收敛曲线自动更新
```

`progress.png` 每次迭代后自动更新——无需看日志，一眼看出循环是否正常运行。

**2. MCP 服务器扩展评估器能力**

任何配置在 Claude Code 里的 MCP 服务器，在循环中都可以直接调用：

```python
# evaluate.py 示例：使用 MCP 评估数据库查询性能
import subprocess, json

result = subprocess.run(
    ["claude", "-p", "用 MCP postgres 对这个查询运行 EXPLAIN ANALYZE，返回 JSON: {score: 执行时间ms}"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
print(json.dumps({"pass": data["score"] < 100, "score": data["score"]}))
```

**3. 自定义评估器契约（唯一要求）**

```python
# 任何满足这个契约的程序都可以作为评估器
import json, sys

score = your_measurement_function()
print(json.dumps({
    "pass": score < TARGET,    # bool: 是否达到目标
    "score": score             # float: 具体数值
}))
sys.exit(0)                    # 始终以退出码 0 结束
```

**4. CI/CD 定时研究**

```yaml
# .github/workflows/nightly-research.yml
on:
  schedule:
    - cron: '0 2 * * *'   # 每晚2点
jobs:
  research:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: /autoresearch
      - run: git add autoresearch-results.tsv && git commit -m "nightly progress"
      - run: git push
```

**5. 研究→技能流水线**

```bash
# 成功的研究会话结束后
/autoresearch:learn --mode init
# 自动生成 SKILL.md：
# - 成功路径总结
# - 有效的假设类型
# - 失败模式清单
# - 下次可直接调用的技能
```

## 变更内容

| 方式 | 本地单次运行 | 高级模式 |
|------|------------|---------|
| 运行时长 | 受限于你的注意力 | tmux 无人值守，随时重连 |
| 指标来源 | 本地 Python 计算 | 任何 MCP 服务器：数据库、监控、LLM |
| 频率 | 手动触发 | CI/CD 定时，研究成为持续过程 |
| 知识积累 | 丢失 | `SKILL.md` 编码成可复用能力 |

## 试一试

运行进度监控器和目标检查器：

```sh
cd docs/zh/lectures/lecture-12-overnight-runs-advanced/code
python progress_monitor.py autoresearch-results.tsv
python check_target.py research.md autoresearch-results.tsv
```

思考题：

1. `progress_monitor.py` 的"收敛"判断标准是什么？`std < 0.005` 意味着什么？
2. 如果你的指标是 LLM 评分（天然有噪声），`std_last5` 会有多大？这对收敛判断意味着什么？
3. 你的项目里有什么外部系统（数据库、监控、API）可以成为 MCP 指标来源？
4. 把成功研究编码为 `SKILL.md` 的最大好处是什么？对你的团队意味着什么？

**用 `check_target.py` 在 bash 循环中提前停止：**

```bash
for i in $(seq 1 100); do
    claude -p "/autoresearch Iterations: 1"
    if python check_target.py research.md; then
        echo "第 $i 轮达到目标，停止"
        break
    fi
done
```

---

**课程完成。** 你现在掌握了完整的 autoresearch 工具集。从[项目六](/zh/projects/project-06-end-to-end-research/)开始，构建一个端到端的完整流水线。
