---
name: demand-to-prd-spec
description: Use when turning confirmed demand brief into human-readable PRD/spec and structured requirement assets.
---

# demand-to-prd-spec

status: `hardened_v0.25`

## 职责

从已确认需求到人类可读 PRD/spec，并在信息缺口明显时触发局部 clarification-interview。

## V0.18 能力

- 消费 `demand brief`，输出人类可读 PRD/spec。
- 形成 Feature / Story 初始结构，但不生成完整 AI-ready asset package。
- 对局部缺口输出 clarification questions 和停止条件。
- 输出 `context-and-decision-updates.md` 建议产物，记录术语、歧义和 ADR 候选。
- 默认中文输出；文件名、ID、固定状态值可保留英文。

## V0.25 方法编排能力

用户可以自然语言使用本 skill，也可以手动指定 `grill-with-docs`、`grill-me`、`office-hours`、`plan-ceo-review`、`plan-eng-review` 或 `brainstorming` 等命令或风格。手动指定会被优先纳入方法组合，但不能让本阶段重新发散回 idea 阶段，也不能越界生成技术设计。

## 输入要求

输入必须至少包含：

- 目标用户或角色。
- 问题和业务目标。
- 主要场景。
- 首期范围或候选范围。
- 已知非目标、假设、开放问题或风险。

如果缺少目标用户、核心问题或首期范围，输出局部 clarification，不应补造 PRD。

## 输出结构

默认输出：

```text
prd-spec/
  prd.md
  feature-story-outline.md
  clarification-questions.md
  context-and-decision-updates.md
  handoff-to-ai-ready-spec.md
  methodology-trace.md
```

其中：

- `prd.md`：人类可读 PRD/spec，包含背景、目标用户、问题、目标、范围、非目标、核心流程、Feature / Story 初始结构、开放问题和风险。
- `feature-story-outline.md`：Feature / Story 初始拆分，只到需求粒度，不写接口、数据库或实现方案。
- `clarification-questions.md`：局部澄清问题、阻塞项和可继续推进的前提。
- `context-and-decision-updates.md`：术语、歧义、上下文建议和 ADR 候选。
- `handoff-to-ai-ready-spec.md`：给 `ai-ready-spec` 的输入摘要、可转换项和不得编造项。
- `methodology-trace.md`：说明本轮采用了哪些方法、为什么采用、用户指定命令是否被使用或降级、哪些方法被跳过、停止依据是什么。

## 第三方能力编排边界

- 按 `shared/methodology-orchestration.json` 通过运行时 skill registry / 相对路径提示解析可用方法；不得依赖本机绝对路径。
- 默认入口是自然语言：用户不需要知道第三方命令。
- 优先调用可用的 Matt Pocock `grill-with-docs` 进行术语澄清、上下文语言检查和决策记录候选识别；如果不可用，则降级为 Matt Pocock grill-with-docs-style domain terminology and decision documentation review。
- 其次调用可用的 Matt Pocock `grill-me` 挑战需求漏洞、隐含假设、边界缺口和反例；如果不可用，则降级为 Matt Pocock grill-me-style interview and challenge review。
- 优先调用可用的 gstack `office-hours` 复核价值、优先级、目标用户和首期范围；如果不可用，则降级为 gstack office-hours-style forcing questions。
- 需要高层业务判断时优先调用可用的 gstack `plan-ceo-review`；不可用时降级为 gstack plan-ceo-review-style strategic scope challenge。
- 需要工程可行性、实现边界或拆分风险判断时优先调用可用的 gstack `plan-eng-review`；不可用时降级为 gstack plan-eng-review-style feasibility and delivery review。
- 少量调用可用的 Superpowers `brainstorming`，仅用于补充备选流程、用户场景或方案可能性；不可用时降级为 Superpowers brainstorming-style divergent exploration，且不应重新发散到 idea 阶段。
- 不把外部 skill 作为硬运行时依赖。

## 用户手动指定命令

如果用户明确要求使用某个第三方命令或风格：

- `grill-with-docs`：优先用于术语澄清、上下文语言检查和决策记录候选识别。
- `grill-me`：用于挑战需求漏洞、隐含假设、边界缺口和反例。
- `office-hours`：用于复核价值、优先级、目标用户和首期范围。
- `plan-ceo-review`：用于战略价值、范围取舍和首期目标强度复核。
- `plan-eng-review`：用于工程可行性、实现边界、拆分风险和测试可用性复核。
- `brainstorming`：仅用于补充备选流程或用户场景，不得重新发散到 idea 阶段。

如果用户指定的方法不适合当前阶段，应说明原因，并改为轻量补充或建议回到 `idea-to-demand`。如果指定方法在当前运行环境不可用，应使用 `shared/methodology-orchestration.json` 中的 fallback style，并在 `methodology-trace.md` 中说明“使用同等风格策略”，不得声称已真实调用该第三方 skill。

## 足够停止的判断

满足以下条件时，可以输出 `handoff-to-ai-ready-spec.md` 并建议进入 `ai-ready-spec`：

- PRD/spec 已包含目标用户、问题、业务目标、范围、非目标和核心流程。
- Feature / Story 初始结构可被人类理解。
- 开放问题、风险和决策候选有稳定 ID 或清晰条目。
- handoff 明确哪些内容可转换、哪些不得编造。
- 不存在必须回到 idea 阶段重新定义需求的问题。

出现以下情况时，必须输出 `needs_more_clarification`，不得补造 PRD：

- 缺少目标用户、核心问题或首期范围。
- Feature / Story 无法形成可理解结构。
- 关键术语、边界或流程存在会影响 Story 拆分的歧义。
- 存在重大业务价值或工程可行性冲突，无法在 PRD/spec 中安全表达。

## 质量规则

- PRD/spec 必须区分事实、推断、待确认问题。
- Feature / Story 初始结构必须能被人类理解，不能用 Rule / GWT 替代 Story 描述。
- 开放问题必须有稳定 ID：`QUESTION-001`。
- 风险必须有稳定 ID：`RISK-001`。
- 不生成技术实现设计、接口设计、数据库设计、代码任务拆分或测试实现。
- 如果输出不足以进入 `ai-ready-spec`，必须在 handoff 中标记 `needs_more_clarification`。
- 必须输出 `methodology-trace.md` 或等价章节，记录 entry mode、用户指定方法、实际采用或降级的方法、跳过原因和停止依据。

## CONTEXT / ADR 边界

- V0.18 MVP 默认输出 `context-and-decision-updates.md` 建议产物。
- 不默认创建或修改用户项目的 `CONTEXT.md`、`CONTEXT-MAP.md` 或 `docs/adr/`。
- 只有用户明确要求真实写入，并且目标项目已有清晰文档边界时，后续迭代才允许实现写入流程。
- ADR 只在同时满足“难回退、没有上下文会令人困惑、确实存在取舍”时建议；否则只记录为 PRD note 或 open question。
