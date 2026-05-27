# Story Granularity Gate

## Story 定义

Story / Requirement Work Unit 是一个可独立理解、可验收、可交给 AI coding / testing agent 消费的行为闭环。

V0.1 中，一个 Feature 通常先拆成 2-4 个 Story 形成可验证薄片。超过 4 个时优先检查 Feature 是否过大；如果真实 Feature 本身复杂，可以保留更多 Story，但必须保证每个 Story 都是可验收行为闭环。

## 合格 Story

一个 Story 通常满足：

- 有清楚用户或系统参与者。
- 有明确触发动作或业务事件。
- 有可观察结果。
- 有至少一条 GEARS 规则。
- 有至少一个 GWT 场景。
- 可以独立判断 ready / need_revision / blocked。
- 有 YAML front matter，包含稳定 ID、父 Feature、Gate、readiness 和 Rule/GWT 引用。
- 有 `Story Detail`，或 backend/API/job/data 类等价细节。

## 不合格 Story

以下内容通常不是需求 Story：

- “开发前端页面”
- “实现后端接口”
- “补充单元测试”
- “设计数据库表”
- “接入权限系统”

这些可以成为后续实现任务，但不能替代需求 Story。

## Gate 判断

- `ready`：Story 行为、规则、GWT、边界和开放问题已经足以让 coding/testing agent 进入下一步。
- `need_revision`：Story 方向明确，但还缺少字段、边界、状态、权限、错误处理或验收细节。
- `blocked`：关键事实缺失或冲突，继续生成会导致下游误实现。

如果 Story 太大，输出拆分建议，并标记 `need_revision` 或 `blocked`。

## 细节充分性

UI / 管理后台 / 工作流 / 表单 / 列表 / 详情 / 审批类 Story 应说明菜单路径、页面入口、布局摘要、字段规则、交互规则、权限规则、状态规则、校验规则和异常处理。

backend / API / job / data 类 Story 应说明 API path、事件或任务、数据对象、请求字段、输出规则、兼容规则、幂等规则和错误处理。

缺少这些细节时，Story 可以保留方向，但 `coding_readiness` 或 `testing_readiness` 应标记为 `need_revision`，不能让下游 agent 自行补造。
