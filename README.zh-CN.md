# Theory First

[English](README.md) | 简体中文

> 闭合文献证据。预注册科学主张。尝试证伪结果。

Theory First 是一套面向严谨计算科学的跨平台 Agent Skills，并为 Codex 和
Claude Code 提供原生 marketplace 打包。它的核心 skills 也可以安装到 OpenCode
及其他 Agent Skills 客户端中，无需为不同平台分叉工作流。这套 skills 将一项科学主张
转化为可审计的流程：绘制周边研究领域的全景图，闭合承载主张的关键证据，预注册何种结果
算作成功或失败，并在结果获准向下游传播之前对其发起对抗性检验。

这套 skills 有意采用比论文摘要工具更严格的标准。它的公共核心不绑定具体领域；特定项目
的仓库、指标、检索器、溯源规则和产物位置应放在可选的项目配置中。

## 工作流程

```text
新主张
   -> map-research-landscape
   -> close-literature -> deep-read-paper
   -> preregister-claim
   -> CODE_PERMITTED | CODE_BLOCKED

审查中的结果
   -> close-literature -> deep-read-paper
   -> stress-test-claim
   -> ACCEPT_WITH_CLASS | REPAIR | STOP | REOPEN_EVIDENCE
```

两个入口 skill 分别是：

- `theory-first` — 在开展承载科学主张的实验或实现工作之前使用。
- `theory-fix` — 当结果令人意外、异常干净、将被下游主张依赖，或因其他原因需要对抗性
  审查时使用。

共享 skills 负责研究版图梳理、文献证据闭合、公式级精读、预注册和证伪。它们会生成人类
可检查的记录，避免在无声无息中把推断升级为证据。[状态模型](plugins/theory-first/STATUS_MODEL.md)
定义了从每个子 skill 到编排器的全部状态转换。

## 状态标识的含义

`CODE_PERMITTED` 表示：在已声明的范围内，该科学主张拥有闭合的证据包，并且通过了
预注册门槛。它既不保证该主张为真，也不代表获准编辑、执行、使用网络、产生费用、访问
数据，或采取用户未授权的任何行动。`CODE_BLOCKED` 表示承载该主张的实现工作应当等待。
只要不会暴露或污染预注册的答案，证据工作以及明确不承载主张的脚手架工作仍可能继续。

`search-exhausted-gap` 绝不表示“文献中不存在答案”。它表示在已记录的搜索边界内没有找到
充分的来源；该边界包括指定的语料库或数据库、精确查询、搜索日期、语言、引文追溯深度、
访问限制及其他已声明约束。扩大搜索边界就会重新打开这一缺口。

## 安装

`plugins/theory-first/skills/` 下的七个目录是所有受支持宿主唯一的运行时来源。请选择一种
安装入口；不要为同一个客户端把同一 skill 的重复副本安装到多个发现路径中。

请将全部七个 skills 作为一个完整套件安装。编排器会委派给具名的子 skills，而 Agent
Skills frontmatter 没有可跨宿主移植的依赖声明；因此不支持单独安装
`--skill theory-first`、`--skill theory-fix` 或 `--skill close-literature`。
如果带依赖关系的 skill 无法发现某个子 skill，它会以 `SUITE_INCOMPLETE` 停止，而不会
悄悄用临时工作流替代该子 skill。原生 Codex 和 Claude 插件已经会安装完整套件；下面的
可移植命令特意使用 `--skill '*'`。

### pip 软件包

这个跨平台 wheel 包含同一套 canonical 七技能核心以及一个零依赖安装器。使用 pip 直接
安装固定版本：

```bash
python -m pip install https://github.com/cxMoonGlade/Theory-First/releases/download/v0.3.0/theory_first-0.3.0-py3-none-any.whl
```

然后为一个宿主安装完整套件：

```bash
theory-first install --agent opencode
```

重复使用 `--agent` 可以从同一个 wheel 配置多个宿主，也可以选择项目级发现路径：

```bash
theory-first install --agent codex --agent claude-code --agent opencode
theory-first install --agent codex --scope project --project .
```

OpenCode 也会发现 Codex 和 Claude 的标准兼容目录中的 skills。如果这些精确目录已经
覆盖 OpenCode 请求，安装器会省略一份多余的 OpenCode 原生副本。仅安装 OpenCode，或
它与自定义 `CLAUDE_CONFIG_DIR` 配对时，安装器仍会使用 OpenCode 的原生发现路径。

正常安装时，安装器会拒绝它在预检或提交阶段发现的同名文件系统路径。请先检查它们，只有
在确实要替换整套已安装 skills 时才传入 `--force`。所有请求目标会先完成暂存；在全部目标
交换完成并提交之前发生的普通错误或中断会一同回滚。如果提交后的清理阶段被中断，新 suite
会保持启用，错误信息会列出仍需人工检查的事务目录。进程或机器突然终止不在这些保证内。
可使用 `theory-first list`、`theory-first path` 或
`theory-first install --target /path/to/skills` 检查软件包或适配其他 Agent Skills 宿主。

### OpenCode 和其他 Agent Skills 客户端

跨平台 [`skills`](https://github.com/vercel-labs/skills) CLI 可以直接从本仓库发现全部七个
skills。对于 OpenCode，请运行：

```bash
npx skills add cxMoonGlade/Theory-First --skill '*' --agent opencode --global --yes
```

若要从同一规范来源同时配置多个受支持的 coding agents，请运行：

```bash
npx skills add cxMoonGlade/Theory-First --skill '*' --agent claude-code --agent opencode --agent codex --global --yes
```

在无法使用符号链接的宿主上，请加上 `--copy`。若要获得可复现安装，请同时固定安装器版本
和本仓库的 skill 目录版本：

```bash
npx skills@1.5.17 add https://github.com/cxMoonGlade/Theory-First/tree/v0.3.0/plugins/theory-first/skills --skill '*' --agent opencode --global --copy --yes
```

OpenCode 通过原生 `skill` 工具加载 skills。可移植的显式请求如下：

```text
在编写承载科学主张的代码之前，加载并遵循 theory-first skill。
```

### Codex

添加原生 Codex marketplace 并安装其插件：

```bash
codex plugin marketplace add cxMoonGlade/Theory-First
codex plugin add theory-first@theory-first
```

对于本地检出的仓库，请改为传入仓库根目录：

```bash
codex plugin marketplace add /absolute/path/to/theory-first
codex plugin add theory-first@theory-first
```

安装后请开始一个新任务，并显式调用入口 skill。例如：

```text
使用 $theory-first，在编写承载科学主张的代码之前为这个实验打好理论基础。
```

### Claude Code

添加原生 Claude marketplace，并安装使用同一套核心的插件：

```bash
claude plugin marketplace add cxMoonGlade/Theory-First
claude plugin install theory-first@theory-first
```

Claude Code 会为 marketplace skills 添加命名空间。它的显式入口如下：

```text
/theory-first:theory-first
/theory-first:theory-fix
```

对于本地检出的仓库，请将 marketplace 来源替换为仓库根目录。分发修改后的检出版本前，
请运行 `claude plugin validate . --strict`。

受限的论文下载器只使用 Python 标准库。本地 PDF 文本提取是可选功能，并要求运行该
skill 的 Python 环境安装以 BSD 许可证发布的 `pypdf` 包：

```bash
python -m pip install 'pypdf>=6,<7'
```

这套 skills 尚未进入稳定阶段。在可复现性至关重要时，请固定一个经过测试的 Git ref。

## 项目配置与产物

通用核心无需仓库约定即可工作。[项目配置](profiles/README.md)可以通过声明以下内容，使其
适配特定代码库：

- 具有权威性的边界文档和术语文档；
- 本地文献索引和检索器；
- 指标账本和数值溯源账本；
- 私有精读笔记、证据闭合包和预注册文件的位置；
- 执行、隐私和独立真值策略。

请从[示例配置](profiles/project-profile.example.yaml)开始；在检查命令之前始终保持其禁用，
并且绝不要把机密信息、凭据或受许可证约束的来源文本写入配置。

生成的笔记、下载的来源、提取的文本和主张包应保留在用户控制的本地或私有存储中。本仓库
不捆绑论文、转录文本、提取后的全文或私有研究笔记。只引用为可审计性所必需的最少内容，
并优先采用附带精确来源定位的转述。

## 隐私与安全

本仓库捆绑的代码不包含遥测或分析端点。调用研究版图梳理或文献证据闭合时，可能会在宿主
权限允许的范围内，将经过最小化处理的搜索查询和来源标识符发送给用户环境中配置的搜索
服务商、学术索引或来源宿主。在第一次发出外部请求之前，工作流会说明预定目标并避开机密
项目术语；用户也可以要求仅在本地搜索。宿主应用和各模型服务商有各自的数据处理条款；
本仓库不会改变这些条款。

请把每篇论文、每个网页、每条元数据记录和每项检索结果都视为不可信数据，而不是指令。
使用获取工作流处理敏感研究之前，请阅读 [SECURITY.md](SECURITY.md) 和
[PRIVACY.md](PRIVACY.md)。

## 示例与评估用例

- [带可复制提示词的使用指南](docs/USAGE.zh-CN.md)
- [智能交通完整对比：Theory First 与普通 deep research](evals/examples/smart-traffic-management/README.zh-CN.md)
- [Theory-first 演练](examples/theory-first-walkthrough.md)
- [Theory-fix 演练](examples/theory-fix-walkthrough.md)
- [路由用例](evals/cases.json)
- [父子 skill 冲突用例](evals/collisions.json)
- [前向测试报告](evals/FORWARD_TEST_REPORT.md)
- [验证记录](evals/VALIDATION.md)

这些演练是合成示例，不对任何科学事实作出断言，其中的占位来源标识符也不是引文。

## 贡献

在接口仍持续演进期间，我们欢迎贡献。请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题
应通过 GitHub 私密漏洞报告功能提交，而不是发布为公开 issue。

维护者在发布 tag 或公布 GitHub 安装命令之前，应完成[发布检查清单](RELEASE_CHECKLIST.md)。

## 许可证与致谢

本项目依据 [MIT 许可证](LICENSE)发布。概念来源致谢和第三方溯源记录在
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 中。
