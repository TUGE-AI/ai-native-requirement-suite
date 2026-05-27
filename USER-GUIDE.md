# AI-native Requirement Suite 使用手册

status: `v0.25-public-preview`

本手册面向两类人：

- 需求负责人、产品经理、业务负责人：用它把想法、需求草稿、PRD 或 Story 整理成可被研发和测试消费的需求资产。
- Skill 维护者、研发负责人：安装、验证、升级和评估这个 skill suite。

当前版本已经完成从想法到质量评审的最小闭环，并整理为公开预览版。V0.25 进一步明确了第三方 skill / 命令的复用方式：用户默认自然语言使用 suite，也可以手动指定命令。它适合试点和评估，但仍不是稳定公开发行版。

## 一句话理解

`AI-native Requirement Suite` 是一套需求技能集，用来把需求从“人能讨论的材料”逐步加工成“AI 编码、AI 测试、人类评审都能消费的结构化资产”。

典型流程：

```text
模糊想法
  -> idea-to-demand
  -> demand brief
  -> demand-to-prd-spec
  -> PRD/spec
  -> ai-ready-spec
  -> V3 requirement asset package
  -> requirement-quality-review
  -> ready / need_revision / blocked
```

如果你不知道当前材料属于哪一阶段，先用 `requirement-router`。

## 什么时候用哪个子 Skill

| 你的输入 | 使用入口 | 输出 |
|---|---|---|
| 只有一个模糊想法，例如“想做一个团队知识检索助手” | `idea-to-demand` | `demand brief`、首期范围、假设、开放问题、停止条件 |
| 已经有比较确认的需求 brief | `demand-to-prd-spec` | 人类可读 PRD/spec、Feature/Story 初始结构、局部澄清问题 |
| 已经有 PRD、Story、Feature spec 或 V2 需求文档 | `ai-ready-spec` | V3 requirement asset package、human-view、AI coding/testing input |
| 已经有 V3 requirement asset package，需要判断能不能交给研发/测试 | `requirement-quality-review` | `ready` / `need_revision` / `blocked`、原因、证据、回流建议 |
| 不确定该走哪一步 | `requirement-router` | 阶段判断、推荐子 skill、缺失上下文、允许的下一步 |
| 只想校验资产包结构、ID、引用、开放问题一致性 | shared validator | validation report |
| 想把资产包生成人类可浏览 HTML | shared wiki generator | 静态 HTML wiki / review cockpit |

注意：`requirement-asset-validator` 和 `requirement-wiki-generator` 是 shared 内部能力，不是一等用户入口。日常优先从 suite 或上表的一等子 skill 进入。

## 第三方技能命令如何复用

这个 suite 复用了多个第三方 skill / 命令的方法能力，包括：

| 命令 | 来源 | 主要用途 |
|---|---|---|
| `brainstorming` | Superpowers | 发散机会、场景、备选方向 |
| `office-hours` | gstack | 价值、目标用户、痛点强度、首期范围和优先级判断 |
| `grill-me` | Matt Pocock agent skills | 反例、漏洞、隐含假设、边界缺口和风险挑战 |
| `grill-with-docs` | Matt Pocock agent skills | 术语澄清、上下文语言检查和决策记录候选 |
| `plan-ceo-review` | gstack | 战略价值、范围取舍和首期目标强度复核 |
| `plan-eng-review` | gstack | 工程可行性、实现边界、拆分风险和测试可用性复核 |

### 推荐方式：自然语言使用

大多数时候你不需要知道这些命令。直接说你的目标即可：

```text
使用 ai-native-requirement-suite，从下面这个想法开始澄清需求。
```

suite 会根据当前阶段自动选择方法：

- `idea-to-demand` 默认融合 `brainstorming`、`office-hours`，少量使用 `grill-me`。
- `demand-to-prd-spec` 默认融合 `grill-with-docs`、`grill-me`、`office-hours`、`plan-ceo-review`、`plan-eng-review`，少量使用 `brainstorming`。

如果对应第三方 skill 在当前环境不可用，suite 会降级为同等风格的问题策略，不应声称已经真实调用了不可用命令。

### 高级方式：手动指定命令

你也可以明确要求使用某些命令或风格：

```text
使用 idea-to-demand，并显式加入 office-hours 和 grill-me 风格的问题。
```

```text
使用 demand-to-prd-spec，优先使用 grill-with-docs 和 plan-eng-review，不要重新发散到 idea 阶段。
```

手动指定命令时，suite 会按以下规则处理：

- 适合当前阶段：纳入方法组合。
- 只适合作为补充：说明边界后轻量使用。
- 不适合当前阶段：说明原因，并建议改用更合适阶段或降级为问题策略。
- 当前环境不可用：使用 fallback style，并说明是降级策略。

手动指定不能跳过阶段边界。例如在 `idea-to-demand` 阶段指定 `plan-eng-review`，只会用于轻量暴露工程风险，不会进入技术设计。

### 如何知道是否已经足够

`idea-to-demand` 足够停止的标准：

- 目标用户清楚。
- 痛点和业务目标可以区分。
- 首期范围和非目标已经有可讨论边界。
- 关键场景、假设、开放问题和风险已经列出。

`demand-to-prd-spec` 足够停止的标准：

- PRD/spec 已包含目标用户、问题、业务目标、范围、非目标和核心流程。
- Feature / Story 初始结构可被人类理解。
- 开放问题、风险和决策候选有稳定 ID 或清晰条目。
- handoff 明确哪些内容可进入 `ai-ready-spec`，哪些不得编造。

两个阶段都应该输出 `methodology_trace` 或 `methodology-trace.md`，说明本轮采用了哪些方法、用户指定命令是否被使用或降级、以及为什么可以停止或必须继续澄清。

## 推荐使用方式

### 方式 A：从模糊想法开始

适合早期产品想法、业务机会、内部工具设想。

你可以这样对 Codex 说：

```text
使用 ai-native-requirement-suite，从下面这个想法开始做需求澄清：
我想做一个给项目团队用的知识检索助手，帮助成员更快找到决策记录和需求背景，但功能还没明确。
```

期望输出：

- 目标用户
- 问题和业务目标
- 典型场景
- 首期范围
- 非目标
- 关键假设
- 开放问题
- 风险
- 下一步建议

如果信息太少，skill 应该停下来问澄清问题，而不是编造完整需求。

### 方式 B：从需求 brief 生成 PRD/spec

适合你已经完成初步澄清，需要形成产品/研发可读文档。

示例：

```text
使用 demand-to-prd-spec，把这个 demand brief 转成 PRD/spec。
要求保留开放问题，不要生成接口设计、数据库设计或技术方案。
```

期望输出：

- PRD/spec
- Feature/Story 初始结构
- 局部 clarification questions
- 首期范围和非目标
- 风险与决策候选
- `context-and-decision-updates.md` 建议产物

`demand-to-prd-spec` 可以利用 `grill-with-docs`、`grill-me`、`office-hours`、`plan-ceo-review`、`plan-eng-review` 等外部技能的方法。如果外部 skill 不可用，会降级为同等风格的问题策略。

### 方式 C：从已有 PRD/V2 spec 生成 AI-ready 需求资产

适合已有文档要交给 AI 编码或 AI 测试。

示例：

```text
使用 ai-ready-spec，把这个 PRD 转成 V3 requirement asset package。
要求 Story 作为一等资产，Rule/GWT 只能作为 Story 内部结构，并生成 human-view、AI coding input、AI testing input。
```

期望资产包通常包括：

```text
feature-map.md
story-map.md
prd.md
quality-review.md
human-view.md
ai-coding-input.md
ai-testing-input.md
stories/
  STORY-001.md
  STORY-002.md
```

质量要求：

- Story 是一等资产。
- Rule/GWT 不能替代 Story。
- 每个 `need_revision` / `blocked` 都必须有原因、证据或 `QUESTION-*` 引用。
- `human-view.md` 必须让人能快速看懂状态、问题和下一步。
- validator warning 不能被静默忽略，必须进入质量评审或 release readiness。

### 方式 D：做质量门禁

适合资产包生成后，判断是否能进入研发/测试。

示例：

```text
使用 requirement-quality-review，评审这个 V3 requirement asset package。
重点从 PM、研发、测试和 AI coding/testing consumer 角度判断是否 ready。
```

输出结论：

- `ready`：可以进入下游开发/测试。
- `need_revision`：可以继续推进部分工作，但仍有必须修订的问题。
- `blocked`：不能交给下游，必须先补齐关键信息。

不要把 `need_revision` 当成失败。对于真实需求，能清楚暴露缺口比假装 ready 更有价值。

## 安装

### 前置条件

- 已有 Codex skill 目录：`$env:CODEX_HOME\skills`
- 使用可用 Python。Windows 下不要使用 Windows Store alias 的 `python.exe`。如果不确定，先确认 `python --version` 有正常输出。

```powershell
$py = '<你的可用 Python 路径>'
```

在 Codex 桌面环境中，可以使用 Codex bundled Python；在其他机器上，请替换为那台机器的可用 Python 路径。不要把本机绝对路径写入可安装 skill source。

### 推荐安装入口

只推荐安装 suite：

```text
ai-native-requirement-suite
```

不推荐单独安装 `requirement-asset-validator` 或 `requirement-wiki-generator`。它们由 suite 的 `shared/` 提供。

### 安装命令

在仓库根目录执行：

```powershell
$env:CODEX_HOME = '<你的 CODEX_HOME>'
$py = '<你的可用 Python 路径>'
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --dry-run
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --install
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --verify
```

如果已经安装过，使用升级：

```powershell
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --upgrade
```

升级会先备份旧版本，再替换，并自动 verify。

## 安装后怎么确认可用

安装后应存在：

```text
$CODEX_HOME/skills/ai-native-requirement-suite/SKILL.md
$CODEX_HOME/skills/ai-native-requirement-suite/subskills/requirement-router/SKILL.md
$CODEX_HOME/skills/ai-native-requirement-suite/subskills/idea-to-demand/SKILL.md
$CODEX_HOME/skills/ai-native-requirement-suite/subskills/demand-to-prd-spec/SKILL.md
$CODEX_HOME/skills/ai-native-requirement-suite/subskills/ai-ready-spec/SKILL.md
$CODEX_HOME/skills/ai-native-requirement-suite/subskills/requirement-quality-review/SKILL.md
```

`--verify` 还会检查 shared validator 和 wiki generator 的脚本帮助命令是否可运行。

## 使用时的建议 Prompt

### 先让 suite 判断阶段

```text
使用 ai-native-requirement-suite 的 requirement-router，判断下面材料处于哪个需求阶段，并告诉我下一步应该用哪个子 skill。
材料如下：
...
```

### 让它不要越界

```text
只做当前阶段，不要提前进入技术设计、接口设计、数据库设计或代码实现。
如果信息不足，请输出澄清问题和停止条件。
```

### 要求输出中文

```text
所有输出默认使用中文。英文术语可以保留，但必须给出中文解释。
```

### 要求保留问题

```text
不要为了让结果看起来完整而隐藏开放问题。所有 QUESTION、need_revision 和 blocked 都要给出原因、证据或下一步处理建议。
```

## 人类用户怎么看产物

优先阅读顺序：

1. `human-view.md`：先看人类视图，快速理解需求、Story、Gate 状态和开放问题。
2. `quality-review.md`：看是否 `ready`、`need_revision` 或 `blocked`，以及原因。
3. `feature-map.md` / `story-map.md`：看范围和拆分结构。
4. `stories/STORY-*.md`：看具体 Story、规则和 GWT。
5. `ai-coding-input.md` / `ai-testing-input.md`：给编码和测试 agent 使用。
6. validator report：排查结构、ID、引用和问题覆盖是否一致。

如果生成了 HTML wiki，先打开 `index.html` 和 `review-cockpit.html`。

## 研发和测试怎么消费

研发重点看：

- `ai-coding-input.md`
- `feature-map.md`
- 对应 `stories/STORY-*.md`
- `quality-review.md` 中与 AI coding readiness 相关的问题

测试重点看：

- `ai-testing-input.md`
- Story 内部 GWT
- `quality-review.md` 中 testability 问题
- Open Questions 和 `need_revision` 原因

如果 Story 是 `need_revision`，研发可以做无争议的准备工作，但不能把该 Story 当成完整可交付范围。

## 常见误用

- 不要把 `requirement-router` 当作执行器。它只给路由建议。
- 不要让 `idea-to-demand` 直接生成 PRD、Story 或技术方案。
- 不要让 `demand-to-prd-spec` 生成接口、数据库或实现设计。
- 不要把 `ai-ready-spec` 的输出直接当作 ready，必须再做质量评审。
- 不要把 validator report 当作业务质量评审。validator 主要检查结构和一致性。
- 不要把 `need_revision` 当作失败。它是把真实风险暴露出来。

## 当前限制

- 当前状态是 `v0.25-public-preview`，不是稳定公开发行版。
- 外部工具如 `grill-with-docs`、`grill-me`、`office-hours`、`plan-ceo-review`、`plan-eng-review` 可用时优先使用；不可用时降级为同等风格问题策略。
- suite 已有最小闭环和公开预览版结构，但仍需要更多公开样本、跨工具安装验证和真实项目人工复核。
- 生成质量仍依赖输入材料质量和人类 review。skill 不替代产品负责人、研发负责人和测试负责人判断。

## 最小上手路径

如果你只想快速试用，按这个顺序：

1. 安装 suite 并运行 `--verify`。
2. 准备一个真实想法、demand brief 或 PRD。
3. 先用 `requirement-router` 判断阶段。
4. 按推荐子 skill 进入下一步。
5. 生成资产后运行 `requirement-quality-review`。
6. 人工重点看 `human-view.md` 和 `quality-review.md`。
7. 只有 Gate 为 `ready` 的 Story 才交给 AI coding/testing。
