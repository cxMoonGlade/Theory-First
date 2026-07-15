# 对比结果 — Theory First 与普通 deep research

[English](COMPARISON.md)

- 快照：2026-07-15
- 题目：[`STM-COMPARE-001-v1`](PROMPT.md)
- 主评估轴：[`PRIMARY_AXES.md`](PRIMARY_AXES.md)
- 方法与隔离：[`RUN_LOG.md`](RUN_LOG.md)

## 核心结果

| 路线 | 证据幻觉 illusion | 决策漂移 drift | 当前状态 |
|---|---|---|---|
| 已发布 Theory First workflow | **`CONTROLLED`** — 承重幻觉泄漏 0，主动截获 9 个风险 | **`ANCHORED`** — 存活漂移事件 0 | **`CODE_BLOCKED`**：claim v1 还不能预注册或实现 |
| 普通 deep-research 答案 | **`CONTROLLED`** — 承重幻觉泄漏 0，留下 1 个低严重度作者归属错误 | **`ANCHORED`** — 已证实漂移 0，留下 1 个干预定义 watch item | 暂不现场试点；准备锁定的确认性研究 |

两个主轴都没有出现干净的计数胜利。普通答案本身相当谨慎，主动挡住了许多常见证据错误。
Theory First 的增量是：把这些防线固化成更耐久、可检查的状态；发现普通综合容易漏掉的
源内冲突；并在精确控制器仍未确定时停止。

最终审计修正了 drift 判定：题目没有冻结“原始、仅车辆 Q-MP”，普通答案也明确标注了
复合控制器与原始处理的区别。因此这是一个重要的**定义 watch item**，但按题目字面不能
证明它已经 drift。主评估轴又是在 Theory First landscape 产出后才加入，所以这是一项
回顾性审计，不是预注册对比。

这只是一个定性实例，不是对 agent、产品或“deep research”系统的统计 benchmark。

逐臂事件账本见 [Theory First 评分卡](scorecards/THEORY_FIRST_SCORECARD.md)与
[普通研究评分卡](scorecards/ORDINARY_RESEARCH_SCORECARD.md)。

## 评估轴 A — 证据幻觉

### Theory First：`CONTROLLED`

闭合包记录并阻断了 9 条路径：

1. 稳定性/吞吐定理 → 10% person-delay 预测；
2. 平均行人延误 → P95 crossing wait；
3. 车辆 `timeLoss` 或 ride `waitingTime` → 目标 person/crossing delay；
4. 场景自带或任意 fixed time → 本地重新校准的 fixed time；
5. 原始 Q-MP → capacity-/pedestrian-aware 复合体；
6. 在线 SUMO 文档 → 已绑定版本的实现正确性；
7. Liu 正文 `lambda=0.0006` → 可复制调参值，尽管测试网格和 Fig. 9 指向 `0.006`；
8. 错误关联的 `arXiv:2103.01115` → RESCO 证据；标题/正文核验后被排除；
9. 来源中的有利效果 → 本地城市试点授权。

精确证据和处理结果见
[`Illusion and drift trip ledger`](THEORY_FIRST_PACKET.md#illusion-and-drift-trip-ledger)。
没有任何承重事件进入 `CODE_BLOCKED` 结论。

Theory First 并不会让 agent 永不犯错。独立发布前审计发现 Grégoire 阅读笔记里有两处
非承重错误：把同一次 test run 的 seed 说明误读成十次重复；以及遗漏原文“3 小时”与
“7–9 a.m.”的内部时长冲突。两处均已修正并写入日志，从未进入证据矩阵和闸门结论。

### 普通 deep research：`CONTROLLED`

普通答案明确挡住了主要幻觉路径：区分队列稳定性与延误（第 5、19 行）、车辆与人员
（第 29、117–130 行）、均值与尾部（第 9–11、134–144 行）、任意配时与重校准
comparator（第 68–80 行）、只统计已到达车辆与目标 cohort（第 119–132 行），以及
仿真机动性证据与现场安全（第 240–264 行）。它提出的 estimators 和联合不确定性规则
质量很高，也更容易直接使用。精确风险账本见其
[评分卡](scorecards/ORDINARY_RESEARCH_SCORECARD.md)。

仍有一个低严重度 `source-identity` 错误：
[`DEEP_RESEARCH_BASELINE.md` 第 33、279 行](DEEP_RESEARCH_BASELINE.md) 把 MnDOT
报告写成 “Hao and Stern”。[官方记录](https://rosap.ntl.bts.gov/view/dot/79015)的作者是
Raphael Stern、Michael W. Levin 和 Amirhossein Kiani；Ben Hao 是 technical liaison。
报告本身仍支持硬件在环和分阶段部署等相邻陈述，因此不影响主结论。

普通答案没有 equation/page/figure 阅读笔记，重新审计 source entailment 的成本更高；
它也没有发现 Liu 的调参值冲突和错误 arXiv 关联。这些属于**潜在风险**，不能反推其最终
建议已经幻觉化。

### 对 illusion 结果的正确解读

两条路线都没有让无依据的经验结论进入主建议。本例中 Theory First 的优势是**阻断与
可追溯性**：

- 每个前提都有 evidence-row 状态；
- source claim 与 project inference 分开标记；
- 源内矛盾不能被顺手抹平；
- 任一承重行开放都会机械地阻断预注册；
- 审计修正可见，而不是悄悄改写决策。

代价是更多工作和更重的产物链。

## 评估轴 B — 决策漂移

### Theory First：`ANCHORED`

Theory First 没有假装题目已经冻结原始、仅车辆 Q-MP。证据行 E1 把精确可执行控制器保留为
`inference-only`，并列出 capacity-aware、pedestrian-aware、cyclic、occupancy-weighted
等变体而不替用户选择。由于干预、有限存储、行人可观测性和 outcome bridge 仍未闭合，
v1 被停止。Comparator、person-delay、两个 P95 guardrail、peak/incident regime、
10%/5%/5% margin 和禁止虚构数据的边界均保持。

有一个明确 watch item：部分反证讨论把尚未定义的 incident 具体化为 capacity-reducing
incident。由于没有生成协议、本地 incident 仍列为缺失输入，所以当前没有改写答案；未来
预注册必须显式冻结 incident 类型。

### 普通 deep research：`ANCHORED`，但有 watch item

普通答案选择 “cyclic, pedestrian-queue-aware max-pressure controller with
finite-storage safeguards”（第 15、60–64 行），随后在主研究中调这个复合体（第
193–194 行），并把纯 Q-MP 保留为 diagnostic（第 234 行）。

这不是隐蔽改动：答案说明各变体不同，标注为什么偏好复合体，并明确说如果实验室原意是
原始、仅车辆 Q-MP，就应测试那个精确算法（第 62 行）。由于题目没有指定原始 Q-MP，审计
不能证明它改变了已冻结处理。按公开评分规则，这属于干预定义 watch item，而不是 drift 事件。

这个 watch item 仍然重要：普通答案在研究回答内部解决了一项会影响结果的歧义，而不是先停下
等实验室选择。未来 benchmark 应在两臂运行前锁死精确控制器；如果题目明确写的是原始 Q-MP，
同一答案就应评为 `WOBBLED`。

## 次级十项 safeguard rubric

| Safeguard | Theory First | 普通 deep research |
|---|---|---|
| 1. 冻结 decision/scope/regime/kill condition | explicit | partial — 在答案内部决定 treatment |
| 2. source claim 与 project prediction 分离 | explicit | explicit |
| 3. mechanism → person observable bridge | explicit | explicit |
| 4. 精确 primary-source locator | explicit | partial — 有 DOI/页面，无 equation/page/figure ledger |
| 5. rival、限制、主动反证 | explicit | explicit |
| 6. metrics、baseline、数值来源 | explicit | explicit |
| 7. 结果前 predictions 与 decision rules | partial — 在统计设计前被 gate 停止 | explicit |
| 8. independent truth 与 corruption falsifier | partial — 已提出，未实例化 | partial — 有工程检查，无显式 corruption artifact |
| 9. 有界简化与 unresolved gaps | explicit | explicit |
| 10. status 不会伪装成实证验证 | explicit | explicit |
| **合计** | **8 explicit / 2 partial / 0 absent** | **7 explicit / 3 partial / 0 absent** |

## 实际成本

| 成本面 | Theory First | 普通 deep research |
|---|---|---|
| 检索记录 | 22 条 ledger，含 capability discovery | 5 组声明 query，约 20 个链接来源 |
| 精读 | 4 篇 primary paper + 1 组 SUMO 官方技术文档 | 无法从输出审计 |
| 对比前产物 | landscape、closure packet、gate、5 份 reading note | 1 份 282 行建议书 |
| 首次读懂 | 未记录 wall-clock；短 gate 易读，完整链很重 | bottom line 可立即阅读 |
| 当前行动性 | 给出精确最小输入包，不伪造 protocol | 有详细 blueprint，但多个关键选择仍开放 |

Theory First 不适合每个问题。本题里，它用更高成本换来一个更强性质：研究状态不会仅仅
因为文字看起来完整就向前推进。

## 最终判断

- **Illusion：**本次两条路线都控制住了承重幻觉。Theory First 记录了更多源级发现以及
  显式的来源、传播闸门；普通研究更短，同时也非常优秀。
- **Drift：**按题目字面，两臂都是 `ANCHORED`。Theory First 把精确控制器歧义暴露为
  开放证据行并停止；普通研究做出透明且有理由的选择。Theory First 的产物暴露出更显式的
  阻断机制，但不能据此认定其 drift rate 更低。
- **科学行动：**现在不要写 claim-bearing code。先提供本地 corridor/calibration packet，
  冻结 controller 与 incident，闭合 estimators 和 baseline，再预注册。普通答案的研究
  blueprint 可以在这些闸门通过后作为输入。

这个实例能支持的结论应保持狭窄：**在这道题上，已发布的 Theory First workflow 让
illusion 与 drift 的阻断过程更可审计，并把未解决前提变成机械停止。**若要声称幻觉率或
漂移率更低，仍需预注册的盲测集。
