# 智能交通管理完整实例

[English](README.md) | 简体中文

这是一次真实的同题双跑：一边使用仓库中已发布的 Theory First suite，另一边使用普通
deep research。题目要求判断：一个四路口 SUMO 研究能否支持 10% 的 person-delay 收益，
同时守住两个 5% 的 P95 guardrail。整个过程没有运行仿真，也没有虚构本地校准数据。

## 结果

| 路线 | Illusion | Drift | 状态 |
|---|---|---|---|
| Theory First | `CONTROLLED` | `ANCHORED` | `CODE_BLOCKED` |
| 普通 deep research | `CONTROLLED` | `ANCHORED` + 1 个定义 watch item | 不做现场试点；准备研究 |

普通答案本身很强：两条路线都没有让承重幻觉进入建议。Theory First 截获了更多源级风险，
并在前提开放时机械停止。普通路线选择了 cyclic、pedestrian-aware、finite-storage 的
复合控制器，但题目没有冻结原始、仅车辆 Q-MP；最终审计因此将其记为定义 watch item，
而不是已证实的 drift 事件。

请阅读[完整对比](COMPARISON.zh-CN.md)和逐臂[评分卡](scorecards/)，其中包含事件账本、
实际成本、审计局限，以及这个单实例结论的边界。

## 复现这条路线

安装锁定版本的 wheel，并配置完整 suite：

```bash
python -m pip install https://github.com/cxMoonGlade/Theory-First/releases/download/v0.3.0/theory_first-0.3.0-py3-none-any.whl
theory-first install --agent codex
```

新开一个 agent 任务，粘贴 [`PROMPT.md`](PROMPT.md)，然后显式调用：

```text
Use $theory-first to analyze this claim before any claim-bearing code.
```

预期路由是：研究版图 → 文献闭合 → 定向精读 → 预注册闸门。仅有公开题目时，诚实状态应为
`CODE_BLOCKED`，而不是一个虚构的协议。只有补齐本地输入包并闭合所有记录行，未来运行
才可能改变状态。

## 审计链

- [冻结题目](PROMPT.md)
- [Illusion/drift 主评估轴](PRIMARY_AXES.md)
- [原始十项 safeguard rubric](RUBRIC.md)
- [运行与隔离日志](RUN_LOG.md)
- [运行清单与产物 hash](RUN_MANIFEST.json)
- [逐臂评分卡](scorecards/)
- [普通 deep-research 答案](DEEP_RESEARCH_BASELINE.md)
- [Theory First 研究版图](THEORY_FIRST_LANDSCAPE.md)
- [Theory First 闭合包](THEORY_FIRST_PACKET.md)
- [预注册闸门](THEORY_FIRST_PREREGISTRATION_GATE.md)
- [精读来源审计](source-audits/)

私下检查的论文全文不会随仓库分发。
