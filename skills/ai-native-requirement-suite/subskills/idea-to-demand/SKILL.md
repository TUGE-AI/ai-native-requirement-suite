---
name: idea-to-demand
description: Use when turning vague ideas, early opportunities, or unclear directions into demand brief and first-scope requirement plan.
---

# idea-to-demand

status: `hardened_v0.25`

## 职责

从模糊想法、早期机会或不清晰方向，产出结构化 `demand brief` 和首期需求计划。

本 skill 主要承载 clarification-interview mode。它帮助用户把“想做什么”澄清为“为谁解决什么问题、首期做什么、不做什么、还有哪些假设和问题”。

## V0.25 边界

本 MVP 只产出 demand brief，不生成 PRD/spec、Feature/Story、GEARS/GWT、接口设计、数据库设计或技术实现方案。

如果信息不足，应输出具体澄清问题、缺失上下文和停止条件，不得伪造确定需求。

用户可以自然语言使用本 skill，也可以手动指定 `brainstorming`、`office-hours`、`grill-me`、`plan-ceo-review` 或 `plan-eng-review` 等命令或风格。手动指定会被优先纳入方法组合，但不能越过本阶段边界。

## 默认流程

1. 判断输入是否确实处于 `idea` / early opportunity 阶段；如果输入已经是 demand brief 或 PRD/spec，应建议回到 `requirement-router` 或进入对应下游。
2. 使用发散问题澄清机会、目标用户、痛点、场景和备选方向。
3. 使用聚焦问题收敛首期目标、首期范围、非目标和成功判断。
4. 使用轻量挑战暴露明显反例、边界漏洞、高风险假设和不应推进的停止条件。
5. 输出结构化 demand brief。

## 输出契约

输出必须包含：

```yaml
target_users: []
problem: ""
business_goal: ""
scenarios: []
first_scope: []
non_goals: []
assumptions: []
open_questions: []
risks: []
next_step: demand-to-prd-spec | more_clarification
methodology_trace:
  entry_mode: suite_auto | subskill_direct | manual_method_override
  selected_methods: []
  manual_methods_requested: []
  methods_used_or_fallback: []
  methods_skipped: []
  stop_basis: ""
```

规则：

- `target_users`、`problem`、`business_goal`、`scenarios` 和 `first_scope` 缺失时，`next_step` 必须是 `more_clarification`。
- `open_questions` 必须是可回答的问题，不写泛泛的“继续调研”。
- `first_scope` 只描述需求范围，不写实现方案。
- `non_goals` 必须明确首期不做什么，避免早期范围膨胀。
- `risks` 至少包含需求风险或假设风险，不把技术实现风险作为默认重点。
- `methodology_trace` 必须简要说明本轮采用了哪些方法、为什么采用、用户指定命令是否被使用或降级、以及为何可以进入下一阶段或必须继续澄清。

## 第三方能力编排

按 `shared/methodology-orchestration.json` 通过运行时 skill registry / 相对路径提示解析可用方法；不得依赖本机绝对路径。

- 默认入口是自然语言：用户不需要知道第三方命令。
- 优先调用可用的 Superpowers `brainstorming`，用于发散、用户场景探索和备选流程补充；不可用时降级为 Superpowers brainstorming-style divergent exploration。
- 优先调用可用的 gstack `office-hours`，用于价值、目标用户、痛点强度、首期范围和优先级判断；不可用时降级为 gstack office-hours-style forcing questions。
- 少量调用可用的 Matt Pocock `grill-me`，仅用于暴露明显反例、边界漏洞和高风险假设；不可用时降级为 Matt Pocock grill-me-style interview and challenge review。
- 本阶段不默认调用 gstack `plan-ceo-review` / `plan-eng-review`。只有用户明确要求高层商业判断或工程可行性挑战时才使用。
- 不把外部 skill 作为硬运行时依赖。

## 用户手动指定命令

如果用户明确要求使用某个第三方命令或风格：

- `brainstorming`：优先用于发散机会、场景、备选方向。
- `office-hours`：优先用于目标用户、痛点强度、首期范围和优先级判断。
- `grill-me`：作为轻量挑战，用于反例、边界漏洞和高风险假设。
- `plan-ceo-review`：只作为可选补充，用于高层商业判断；不得因此直接生成 PRD 或路线图。
- `plan-eng-review`：只作为可选补充，用于暴露工程可行性风险；不得因此进入技术设计。
- `grill-with-docs`：通常更适合 `demand-to-prd-spec`；本阶段只可降级为术语和上下文澄清问题。

如果用户指定的命令在当前运行环境不可用，应使用 `shared/methodology-orchestration.json` 中的 fallback style，并在 `methodology_trace` 中说明“使用同等风格策略”，不得声称已真实调用该第三方 skill。

## 足够停止的判断

满足以下条件时，可以输出 `next_step: demand-to-prd-spec`：

- 目标用户清楚。
- 痛点和业务目标可以区分。
- 至少有 2 个关键场景，或 1 个高置信核心场景。
- 首期范围和非目标已形成可讨论边界。
- 关键假设、开放问题和风险已列出。
- 不存在阻止理解需求本质的缺失信息。

## 停止条件

出现以下情况时，不得输出“可进入 PRD”的结论：

- 目标用户不清楚。
- 痛点和业务目标无法区分。
- 首期范围无法从备选方向中收敛。
- 关键场景缺失。
- 用户只给出一句泛泛请求，例如“帮我弄一下这个需求”。

此时应输出 `next_step: more_clarification`，并给出 3-5 个具体澄清问题。
