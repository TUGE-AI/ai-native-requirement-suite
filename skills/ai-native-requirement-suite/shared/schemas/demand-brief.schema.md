# Demand Brief Schema

status: `mvp_v0.17`

## 用途

`idea-to-demand` 使用本契约，把模糊想法整理成可被 `demand-to-prd-spec` 消费的 demand brief。

本 schema 是人类可读契约，不是 JSON Schema。V0.17 不实现脚本校验。

## 字段

| Field | Required | Meaning |
|---|---|---|
| `target_users` | yes | 目标用户或主要使用角色 |
| `problem` | yes | 要解决的核心问题 |
| `business_goal` | yes | 业务目标或价值判断 |
| `scenarios` | yes | 关键用户场景或业务场景 |
| `first_scope` | yes | 首期建议范围 |
| `non_goals` | yes | 首期明确不做的内容 |
| `assumptions` | yes | 当前依赖但尚未验证的假设 |
| `open_questions` | yes | 需要用户或业务方继续回答的问题 |
| `risks` | yes | 需求风险、范围风险或假设风险 |
| `next_step` | yes | `demand-to-prd-spec` 或 `more_clarification` |

## 约束

- `target_users`、`problem`、`business_goal`、`scenarios` 或 `first_scope` 缺失时，`next_step` 必须是 `more_clarification`。
- `first_scope` 不得包含接口、数据库、技术架构或代码实现方案。
- `non_goals` 必须帮助控制首期范围。
- `open_questions` 必须是具体可回答的问题。
- Demand brief 不是 PRD/spec，不得包含完整 Story、GEARS/GWT 或测试用例。
