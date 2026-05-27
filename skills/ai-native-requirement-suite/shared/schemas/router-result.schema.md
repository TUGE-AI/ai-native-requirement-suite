# Router Result Schema

status: `mvp_v0.16`

## 用途

`requirement-router` 使用本契约输出阶段判断和下一步建议。

本 schema 是人类可读契约，不是 JSON Schema。V0.16 不实现脚本校验。

## 字段

| Field | Required | Values | Meaning |
|---|---|---|---|
| `input_stage` | yes | `idea` / `demand_brief` / `prd_spec` / `feature_story` / `requirement_asset` / `quality_review_request` / `unknown` | 输入所处需求阶段 |
| `recommended_subskill` | yes | `requirement-router` / `idea-to-demand` / `demand-to-prd-spec` / `ai-ready-spec` / `requirement-quality-review` / `shared/validators/requirement-asset-validator` | 推荐下一步入口 |
| `confidence` | yes | `high` / `medium` / `low` | 路由判断置信度 |
| `reason` | yes | free text | 阶段判断原因 |
| `missing_context` | yes | list | 继续推进前需要补充或确认的信息 |
| `stop_condition` | yes | free text | 不应继续推进的停止条件 |
| `allowed_next_actions` | yes | list | 当前允许的下一步动作 |

## 约束

- `confidence: low` 时，`input_stage` 必须是 `unknown`，`recommended_subskill` 必须是 `requirement-router`。
- `input_stage: unknown` 时，不得推荐生成型子 skill。
- `shared/validators/requirement-asset-validator` 只用于用户明确要求结构校验时。
- 路由结果不得宣称已执行任何下游子 skill。
