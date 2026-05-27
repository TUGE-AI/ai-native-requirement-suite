---
name: requirement-router
description: Use as the AI-native Requirement Suite entrypoint to classify requirement input stage and route to the proper subskill.
---

# requirement-router

status: `hardened_v0.24`

## 职责

统一入口，判断输入处于想法、demand brief、PRD/spec、Feature/Story、V3 requirement asset package 或质量评审阶段，并路由到对应子 skill。

## V0.16 边界

本文件实现规则型 MVP：只判断输入阶段并输出结构化路由建议，不执行完整子 skill，不做需求生成，不做脚本分类。

## 输入阶段

| input_stage | 典型信号 | 默认路由 |
|---|---|---|
| `idea` | 模糊想法、机会、痛点、方向，还没有明确目标用户、范围或验收口径 | `idea-to-demand` |
| `demand_brief` | 已有目标用户、业务目标、场景、初步范围或需求 brief，但还不是完整 PRD/spec | `demand-to-prd-spec` |
| `prd_spec` | 已有人类可读 PRD/spec、功能说明、业务规则或验收口径，需要转成 AI 可消费资产 | `ai-ready-spec` |
| `feature_story` | 已有 Feature / Story / Acceptance Criteria / GWT / GEARS 片段，需要整理成 V3 requirement asset package | `ai-ready-spec` |
| `requirement_asset` | 已有 V3 requirement asset package 目录、feature-map、story-map、human-view、ai-coding/testing input | `requirement-quality-review` |
| `quality_review_request` | 用户明确要求评审需求质量、测试可用性、AI coding/testing 可用性或门禁状态 | `requirement-quality-review` |
| `unknown` | 输入过短、缺少上下文、阶段冲突或无法判断 | `requirement-router` |

## 结构校验例外

当用户明确要求“结构校验、ID 一致性检查、open question 数量检查、asset package validator”时，允许推荐 `shared/validators/requirement-asset-validator`。

这不是一等 user-facing subskill 的默认路由，只是 shared validator 的工具型入口。

## V0.16 输出契约

每次只输出一个结构化路由结果：

```yaml
input_stage: idea | demand_brief | prd_spec | feature_story | requirement_asset | quality_review_request | unknown
recommended_subskill: requirement-router | idea-to-demand | demand-to-prd-spec | ai-ready-spec | requirement-quality-review | shared/validators/requirement-asset-validator
confidence: high | medium | low
reason: ""
missing_context: []
stop_condition: ""
allowed_next_actions: []
```

规则：

- `confidence: high` 只用于阶段信号明确且下一步无明显歧义的输入。
- `confidence: medium` 可推荐下一步，但必须列出仍需确认的上下文。
- `confidence: low` 时不得直接推进生成，应输出缺失上下文。
- `input_stage: unknown` 时只能建议澄清，不得猜测进入后续子 skill。
- 路由器只输出决策，不执行完整子 skill。

## 判定顺序

1. 先识别用户是否明确要求质量评审或结构校验。
2. 再识别是否已经是 V3 requirement asset package。
3. 再识别是否已有 Feature / Story / PRD/spec。
4. 再识别是否是 demand brief。
5. 最后才判断为 early idea。
6. 如果多个阶段信号冲突，选择最保守的下一步，并在 `missing_context` 中列出需要用户确认的冲突点。

## V0.24 分流规则

V0.22 / V0.23 验证后，路由必须显式区分 raw idea 与 V2 PRD/spec：

- 输入只有一句想法、问题、机会、目标方向，且缺少目标用户、范围或验收口径时，必须路由到 `idea-to-demand`。
- 输入已有目标用户、业务目标、场景、首期范围和开放问题，但还不是 PRD/spec 时，必须路由到 `demand-to-prd-spec`。
- 输入是历史 V2 PRD/spec、Feature spec、Story spec、已有验收标准或业务规则时，必须路由到 `ai-ready-spec`，不应重新走 `idea-to-demand`。
- 输入是已生成的 V3 requirement asset package 时，必须路由到 `requirement-quality-review`；只有用户明确要求结构校验时，才推荐 shared validator。
- 如果用户要求“从想法开始重新生成”，即使上下文里存在历史 PRD，也应优先询问是否使用 raw idea flow 或 V2 regression flow，不能静默选择。

## 低置信度处理

低置信度时输出：

- `input_stage: unknown`
- `recommended_subskill: requirement-router`
- `confidence: low`
- `missing_context` 至少包含 2 个具体问题
- `allowed_next_actions` 只能包含澄清、补充材料或让用户选择输入阶段

## 输出示例

```yaml
input_stage: prd_spec
recommended_subskill: ai-ready-spec
confidence: high
reason: "输入已经包含 PRD、业务规则和验收口径，下一步应转换为 V3 requirement asset package。"
missing_context: []
stop_condition: "如果 PRD 中缺少目标用户、关键业务规则或验收口径，应先返回 demand-to-prd-spec 补齐。"
allowed_next_actions:
  - "进入 ai-ready-spec，生成 V3 requirement asset package"
  - "先进行 requirement-quality-review 的轻量预审"
```
