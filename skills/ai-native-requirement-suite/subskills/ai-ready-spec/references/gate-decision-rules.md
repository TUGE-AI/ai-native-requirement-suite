# Gate Decision Rules

## Gate 状态

Feature Gate 和 Story Gate 的 `status` 只允许使用三个状态：

- `ready`
- `need_revision`
- `blocked`

不要使用分数制，也不要使用“基本可用”“风险较高”等不能触发行动的状态。

Story front matter 可以额外使用 readiness 字段，用来表达 coding/testing 的局部可用性：

- `granularity_readiness`: `ready | need_revision | blocked`
- `coding_readiness`: `ready | need_revision | blocked`
- `testing_readiness`: `ready | need_revision | blocked`
- `overall_decision`: `ready | ready_for_coding_only | ready_for_testing_only | need_revision | blocked`

`status` 仍是总 Gate；`overall_decision` 是给下游 agent 的执行口径。若 `status: ready` 但 `testing_readiness: need_revision`，则 `overall_decision` 不得写 `ready`，应写 `ready_for_coding_only` 并解释测试缺口。

## Feature Gate

Feature Gate 判断整个 Feature 是否能进入 AI coding / AI testing。

`ready` 条件：

- Feature 范围和非目标清楚。
- 至少 2 个 Story ready，或本 Feature 本身就是一个极小闭环。
- 关键 GEARS / GWT 可观察、可验收。
- 无关键事实冲突。

`need_revision` 条件：

- 目标明确，但仍有字段、状态、权限、边界或异常未定义。
- Story 粒度需要调整，但不影响方向判断。
- 部分 GWT 缺失，但可以通过补充上下文修复。

`blocked` 条件：

- 关键业务规则冲突。
- 缺少目标用户、核心流程或验收结果。
- 下游实现需要自行决定产品行为。

## Story Gate

Story Gate 判断单个 Story 是否可被下游 agent 消费。

必须输出：

- `status`
- `reason`
- `required_followup`
- `related_ids`

示例：

```text
Story Gate: STORY-001
status: need_revision
reason: RULE-002 缺少失败状态，GWT-003 无法判断 Then。
required_followup: 明确提交失败时用户可见反馈和数据保留策略。
related_ids: RULE-002, GWT-003, QUESTION-001
```
