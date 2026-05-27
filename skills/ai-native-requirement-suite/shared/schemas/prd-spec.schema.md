# PRD/spec Schema

status: `mvp_v0.18`

## 用途

本 schema 用于 `demand-to-prd-spec` 输出人类可读 PRD/spec。它不是技术设计 schema，也不是 AI-ready requirement asset package schema。

## 必需字段

- `title`：需求标题。
- `source_stage`：固定为 `demand_brief` 或 `confirmed_requirement_brief`。
- `target_users`：目标用户或角色。
- `problem`：要解决的问题。
- `business_goal`：业务目标。
- `scope`：首期范围。
- `non_goals`：非目标。
- `scenarios`：主要用户场景。
- `feature_story_outline`：Feature / Story 初始结构。
- `open_questions`：开放问题，使用 `QUESTION-*`。
- `risks`：风险，使用 `RISK-*`。
- `next_step`：通常为 `ai-ready-spec` 或 `more_clarification`。

## 禁止内容

- 不写接口设计。
- 不写数据库设计。
- 不写技术选型。
- 不把 Story 拆成前端、后端、测试等技术任务。
