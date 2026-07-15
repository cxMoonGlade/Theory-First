# 使用指南

[English](USAGE.md) | 简体中文

[返回项目说明](../README.zh-CN.md)

本指南说明如何把具体研究任务路由到这套七技能组合。请先安装完整套件。下面提供的是提示词
模板，并不声称某个特定来源一定存在，也不预设工作流必然通过门槛。使用前请替换所有尖括号
字段。

## 选择案例之前

除非现有输入已经满足某个子 skill 的前置条件，否则应使用编排器：

- 在开展新的承载主张的实验或实现之前，使用 `theory-first`；
- 在结果已经产生、但其解释尚未向下游传播之前，使用 `theory-fix`；
- 只有在需要宽范围定向时，才直接使用 `map-research-landscape`；
- 只有在主张已经冻结且承载证据的行已经明确时，才直接使用 `close-literature`；
- 只有在单一来源已经明确且被分配了一个问题时，才直接使用 `deep-read-paper`；
- 只有在完整的文献闭合包已经存在时，才直接使用 `preregister-claim`；
- 只有在闭合包、原始预注册和原始结果产物都已具备时，才直接使用
  `stress-test-claim`。

任何科学状态都不授权文件编辑、执行、网络访问、数据访问、付费，或用户请求和宿主权限之外
的其他行动。

## 案例 1 — 用 theory-first 为新实验打好基础

当实验、模型、机制、可观测量、指标或预测即将建立在尚未闭合的科学前提之上时，使用这条
路线。

### 可复制提示词

```text
Use theory-first for a new claim-bearing experiment.

Decision: <decision this experiment will support>
Draft claim: <exact claim to freeze>
Mechanism: <proposed mechanism or governing operation>
Observable: <measured or computed quantity>
Regime: <population, scale, assumptions, and boundary conditions>
Known sources: <source identifiers or "none">
Project profile: <profile path or "none">
Retrieval boundary: <local-only or authorized external sources>

Do not write or run claim-bearing code, and do not inspect results, until the workflow returns its scoped code gate.
```

### 为什么这样路由

结果尚未被查看，而任务将产生新的科学主张。因此，`theory-first` 会先冻结问题，按需梳理
不稳定术语，闭合承载主张的文献，并在决定是否可以开始承载主张的编码之前预注册预测。

### 预期产物

- 带版本的章程，包含主张、后果、适用范围、竞争解释、终止条件和非目标；
- 研究版图引用，或跳过这一步的明确理由；
- 文献闭合矩阵，以及所有承载主张的精读笔记引用；
- 未解决的矛盾记录和有范围限定的缺口记录；
- 预注册标识符及其通过或失败账本；
- 一条范围明确的 `CODE_BLOCKED` 或 `CODE_PERMITTED` 记录。

### 停止条件

- 缺少必需子 skill 时返回 `SUITE_INCOMPLETE`；继续之前应安装完整七技能套件。
- 任一承载证据的行处于缺失、歧义、仅推断、矛盾、不可访问或
  `search-exhausted-gap` 状态时，返回 `CODE_BLOCKED`。
- 预注册门槛失败同样返回 `CODE_BLOCKED`。
- `CODE_PERMITTED` 只适用于被冻结的主张版本、适用范围和实现边界；它不是真理证书，也
  不构成行动授权。

## 案例 2 — 先广扫研究版图，再闭合文献

当术语不稳定、多个形式体系互相竞争，或初始搜索很可能过窄时，使用这个两步流程。研究
版图负责选择阅读路径，不负责闭合证据。

### 可复制的研究版图提示词

```text
Use map-research-landscape before narrowing this research question.

Decision: <decision the map will inform>
Current draft claim: <claim or question>
Mechanism and observable: <current formulation>
Known synonyms or neighboring fields: <terms or "unknown">
Scope limits: <time, language, access, and confidentiality boundaries>
Project profile: <profile path or "none">

Return an orientation map, explicit no-go boundaries, and a minimal candidate reading set. Label every source as a discovery lead and do not claim literature closure.
```

当研究版图已经把证据行变得明确后，冻结主张并将其交给 `close-literature`：

```text
Use close-literature on the frozen claim below, using the landscape map only as routing input.

Charter ID: <frozen charter identifier>
Decision: <decision this claim will support>
Frozen claim: <exact claim>
Mechanism: <mechanism>
Observable: <observable and measurement procedure>
Regime: <assumptions, scale, and boundaries>
Landscape map: <artifact path or identifier>
Known sources: <source identifiers>
Project profile: <profile path or "none">

Build the coverage matrix first. Assign every load-bearing source to an evidence row and invoke deep-read-paper where equation, theorem, figure, data, or implementation fidelity is required. Do not preregister or write experiment code.
```

### 为什么这样路由

`map-research-landscape` 负责广扫：术语格、来源聚类、形式体系对照、基准、实现和禁区。
`close-literature` 则针对冻结主张做窄而严格的审计，只选择真正承载机制、可观测量、桥接、
有效范围、指标、数值、实现或反证行的来源。

### 预期产物

- 定向研究版图、候选阅读集合、搜索账本和待闭合证据行；
- 带有来源清单和逐行状态的闭合包；
- 对承载证据的公式、定理、图表、数据语义或实现细节给出精确的精读笔记引用；
- 矛盾账本和数值溯源账本；
- 文献闭合返回的 `CLOSED`、`OPEN`、`CONTRADICTED` 或
  `SEARCH_EXHAUSTED_GAP`。

### 停止条件

- 研究版图达到定向饱和时就应停止，不能滑向“已经全面覆盖整个领域”的主张。
- 如果无法发现 `deep-read-paper`，`close-literature` 返回 `SUITE_INCOMPLETE`。
- `OPEN`、`CONTRADICTED` 和 `SEARCH_EXHAUSTED_GAP` 会阻断 theory-first 的证据
  门槛，不能据此预注册正向前提。

## 案例 3 — 精读一篇承载证据的论文

当一个明确来源需要达到公式、定理、图表或实现级别的核验精度时，使用
`deep-read-paper`。不要用它调查整个领域，也不要用它在多个含糊引文之间做选择。

### 可复制提示词

```text
Use deep-read-paper for exactly one source.

Source: <local PDF, exact title plus DOI, or arXiv identifier and version>
Assigned evidence row or question: <one precise question>
Target claim: <claim that would use this source>
Consequence if wrong: <downstream consequence>
Required fidelity: <equation, theorem, figure, table, algorithm, or implementation>
Project mapping: <symbols, quantities, or operation to compare>

Do not survey the field or execute source code. Separate source claims, reconstruction, project inference, unknowns, and conflicts, and attach exact locators to every load-bearing use.
```

### 为什么这样路由

来源和任务已经明确。领域调查应交给 `map-research-landscape`；多来源发现与选择应交给
`close-literature`。

### 预期产物

- 固定的来源身份、版本、获取日期和摘要值；
- 来源结构图和符号账本；
- 对所分配公式、定理条件、图表、算法或实现细节的重建；
- 区分 `[source]`、`[reconstructed]`、`[project-inference]`、`[unknown]`
  和 `[conflict]` 的主张账本；
- 每个已分配证据行的 `CLOSED`、`INFERENCE_ONLY`、`MISSING`、`AMBIGUOUS`
  或 `CONTRADICTED` 状态。

### 停止条件

- 如果引文无法唯一确定来源和版本，应提供准确标题以及 DOI 或 arXiv 标识符，或直接提供
  来源文件；不能猜测。
- 无法目视检查的承载证据图表保持 `VISUALLY_UNVERIFIED`，不能闭合对应证据行。
- `CLOSED` 只对被分配的证据行有效，不代表整个领域已经闭合，不接受项目主张，也不授权
  编码。

## 案例 4 — 用 theory-fix 或直接压力测试审计结果

当结果令人意外、异常干净、符合期望、来自摘要、对形式体系敏感，或即将成为下游前提时，
默认使用 `theory-fix`。在改变代码、参数、排除规则、图表或措辞之前先冻结结果。

### 可复制的 theory-fix 提示词

```text
Use theory-fix before this result propagates.

Claim ID and exact wording: <identifier and frozen wording>
Statement type and intended confidence class: <registered values>
Code, configuration, data, environment, and result artifacts: <immutable identifiers>
Original charter and preregistration: <identifiers or recorded absence>
Observed metrics, uncertainty, exclusions, and stopping decision: <values and conventions>
Result-to-claim bridge: <why the result is said to support the claim>
Alternative explanations: <known rivals>
Downstream consumers: <definitions, designs, reports, or planned runs>

Freeze the artifacts and mark downstream consumers PROPAGATION_PAUSED. Reopen the load-bearing literature before stress testing. Do not edit code, rerun, or rewrite the claim during this audit.
```

只有在完整前置包已经存在时，才直接调用 `stress-test-claim`：

```text
Use stress-test-claim directly. The required refreshed closure packet, original preregistration, and raw result artifacts are already available.

Frozen claim: <exact wording and claim ID>
Consequence and downstream consumers: <decision and propagation sites>
Statement type and confidence class: <registered values>
Closed literature packet: <artifact identifier>
Original preregistration: <artifact identifier>
Raw artifacts and exact configuration: <immutable identifiers>
Alternative formulations and invariants: <registered alternatives>

Run every applicable trip-wire against the actual artifacts. Do not acquire literature, edit the preregistration, repair code, or launch a replacement experiment.
```

### 为什么这样路由

`theory-fix` 负责完整的结果后流程：冻结传播、重新打开证据、委派敌对检查，再对顶层结果
分类。只有在文献闭合已经刷新且所有必需产物均已存在时，才可以直接调用
`stress-test-claim`。

### 预期产物

- 冻结的主张和产物清单；
- 下游传播账本和证据变化账本；
- 逐条压力测试记录及预注册偏差；
- 反向证据、残余风险和禁止外推；
- `theory-fix` 给出的唯一顶层决策：`STOP`、`REPAIR`、`REOPEN_EVIDENCE` 或
  `ACCEPT_WITH_CLASS`。

### 停止条件

- 硬性检验触发、不可复现、溯源无效或直接矛盾时返回 `STOP`；只有当缺陷局部、有界且可在
  新产物上验证时，才可映射为 `REPAIR`。
- 缺失文献、可恢复的产物或可获得的独立检查会返回 `REOPEN_EVIDENCE`；直接压力测试也
  可能报告 `PENDING`。
- `REPAIR` 不验证修复后的结果；它要求新版本在不变的接受规则下接受全新测试。
- 只有 `ACCEPT_WITH_CLASS` 能在其准确类别和适用范围内恢复传播。“通过当前检验”不是
  证明。

## 案例 5 — 如实处理已知文献缺口

当一个冻结主张已经确定缺少足以承载其前提的证据时，使用这条路线。目标是审计搜索边界并
定义最小下一步，而不是把没有找到证据转化为正向证据。

### 可复制提示词

```text
Use close-literature to audit a known load-bearing literature gap without turning absence into evidence.

Charter ID: <frozen charter identifier>
Decision and frozen claim: <decision and exact claim>
Load-bearing row: <mechanism, observable, bridge, regime, metric, value, implementation, or disconfirmation>
Proposition not yet supported: <exact proposition>
Known sources and prior searches: <identifiers and query records>
Search boundary: <corpora, query families, date, languages, year filters, citation depth, and access limits>
External retrieval authority: <authorized services or local-only>

Search for supporting and contrary primary evidence. If no adequate source is found, record the scoped search-exhausted-gap and return the correct closure status. Do not use the gap as a positive premise, preregister the claim, or write claim-bearing code.
```

### 为什么这样路由

主张和缺失行已经冻结，所以问题是证据闭合，而不是研究版图定向。有范围限定的
`search-exhausted-gap` 记录搜索查过哪里，绝不表示整个领域都没有答案。

### 预期产物

- 更新后的覆盖矩阵和来源清单；
- 精确搜索账本、访问失败记录和反向证据搜索；
- 未找到的命题，以及已记录搜索的完整边界；
- 无法闭合时返回 `OPEN`、`CONTRADICTED` 或 `SEARCH_EXHAUSTED_GAP`；
- 最小下一步，例如获得访问权限、扩展获准的搜索范围，或对主张进行版本化收窄。

### 停止条件

- 未经授权不得外部搜索；流程停留在本地边界并保持该行开放。
- `search-exhausted-gap` 不闭合承载证据的行；theory-first 仍为 `CODE_BLOCKED`。
- 收窄或改变主张必须创建新的章程版本和变更账本，不能静默重写。

## 案例 6 — 不应触发这套 skills 的请求

以下任务本身不需要科学证据门槛：

```text
Rename this internal helper and update its existing unit tests without changing behavior.
```

```text
Translate this README while preserving its commands and links.
```

```text
Fix this deterministic CLI argument-parsing exception against the existing specification.
```

```text
Give me a short, non-claim-bearing summary of the abstract I supplied for personal orientation.
```

### 为什么不路由到这里

这些是普通工程、文档或轻量摘要任务，并不包含新的科学前提、承载主张的实验、承载证据的
来源核验，或从结果到下游主张的传播。

### 预期产物

返回与普通任务相匹配的产物：范围明确的代码改动与测试、翻译、错误修复，或边界清楚的
摘要。没有调用这套 skills 时，不应虚构 Theory First 状态。

### 升级条件

如果任务开始依赖尚未闭合的科学前提、询问一篇论文究竟证明了什么、设计承载主张的实验，
或把结果提升为下游主张，应停止普通路线并选择合适的 skill。

## 案例 7 — 在 Codex、Claude Code 或 OpenCode 调用同一工作流

请安装全部七个 skills 并开始一个新任务。先选择案例提示词，再在前面加上宿主的原生调用
方式。Skill 名称是宿主技能机制的标识符，不是 shell 命令。

### Codex

```text
Use $<skill-name>.
<paste the selected case prompt here>
```

对于主要的结果前与结果后工作流，请将 `<skill-name>` 替换为 `theory-first` 或
`theory-fix`。只有满足本指南前述前置条件时，才能直接使用子 skill 名称。

### Claude Code

```text
/theory-first:<skill-name>
<paste the selected case prompt here>
```

例如，带命名空间的入口为 `/theory-first:theory-first` 和
`/theory-first:theory-fix`。

### OpenCode

```text
Load and follow the <skill-name> skill before doing the task.
<paste the selected case prompt here>
```

OpenCode 通过原生 skill 工具解析指定的 skill。当安装后的宿主提供的是 skill 加载机制时，
不要虚构斜杠命令入口。

### 预期行为与停止条件

三个宿主加载相同的 canonical skill 目录，应产生相同的路由和状态语义。如果带依赖的
skill 无法发现某个指定子 skill，它会返回 `SUITE_INCOMPLETE`，而不是临时拼凑替代流程。
重新安装完整套件并开始一个新任务后再试。

## 如何理解最终状态

完整转换表见[状态模型](../plugins/theory-first/STATUS_MODEL.md)。实用规则很简短：

- 在结果产生前，只有范围明确的 `CODE_PERMITTED` 才能通过科学门槛；
- 在结果产生后，`STOP`、`REPAIR` 和 `REOPEN_EVIDENCE` 都会保持传播暂停；
- `ACCEPT_WITH_CLASS` 只记录主张在指定攻击面和准确适用范围内经受住了检验，并不代表
  普遍真理；
- 每个缺口、待完成检验、访问限制和项目推断都必须在输出包中保持可见。

完整的同题双跑请见[智能交通实例](../evals/examples/smart-traffic-management/README.zh-CN.md)：
其中包含冻结 rubric、公式级精读笔记、未通过的预注册闸门，以及与普通 deep research 的
illusion/drift 对比。
