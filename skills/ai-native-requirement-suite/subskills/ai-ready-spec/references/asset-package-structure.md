# Asset Package Structure

## 最小目录

```text
requirement-asset/
  README.md
  prd.md
  feature-map.md
  ai-coding-input.md
  ai-testing-input.md
  quality-review.md
  human-view.md
  features/
    FEATURE-001/
      feature-spec.md
      story-map.md
      ai-coding-input.md
      ai-testing-input.md
      quality-review.md
      stories/
        STORY-001.md
        STORY-002.md
```

## 根目录文件职责

- `README.md`：说明资产包来源、范围、状态、如何消费。
- `prd.md`：保留人类可读的产品需求摘要，必须区分事实、推断、开放问题。
- `feature-map.md`：列出 Feature、Story、Rule、GWT 的稳定 ID 和关系。
- `ai-coding-input.md`：给 AI coding agent 的入口文件。
- `ai-testing-input.md`：给 AI testing agent 的入口文件。
- `quality-review.md`：门禁结论、缺口、风险、待确认问题。
- `human-view.md`：面向 PM、业务、开发、测试的人类阅读视图，用于后续 wiki/html 生成前的 Markdown 中间层。

## Feature 目录文件职责

- `feature-spec.md`：Feature 目标、用户、范围、非目标、高层规则、共同约束和 Story 引用。Feature 不重复完整 Story 细节。
- `story-map.md`：Story 列表、Story Gate、GEARS -> GWT 映射。
- `ai-coding-input.md`：Feature 级实现输入。
- `ai-testing-input.md`：Feature 级验收输入。
- `quality-review.md`：Feature 级质量门禁和缺口。
- `stories/STORY-*.md`：Story 一等资产，包含 front matter、narrative、范围、流程、`story_detail` 或 API/job/data 等价细节、规则、GWT、Gate、Open Questions。

## Story 文件职责

Story 文件必须让人先理解需求，再查看规则和验收。推荐结构：

```text
---
asset_type: story_spec
feature_id: FEATURE-001
story_id: STORY-001
title: <标题>
status: ready | need_revision | blocked
requirement_work_unit: true
estimated_effort: 1-2d
granularity_readiness: ready | need_revision | blocked
coding_readiness: ready | need_revision | blocked
testing_readiness: ready | need_revision | blocked
overall_decision: ready | ready_for_coding_only | ready_for_testing_only | need_revision | blocked
related_rule_refs: []
related_gwt_refs: []
updated_at: "YYYY-MM-DD"
---

# STORY-001: <标题>
## 业务目标
## 用户与场景
## 范围
## 非目标
## 主要流程
## Story Detail
## 业务规则 / GEARS
## 验收场景 / GWT
## AI Coding Notes
## AI Testing Notes
## Gate Decision
## Open Questions
```

Rule/GWT 是 Story 的内部结构，不应替代 Story 描述。

`Story Detail` 推荐使用 YAML 代码块。UI / 管理后台 / 工作流类 Story 使用：

```yaml
story_detail:
  menu_path: ""
  page_or_entry: ""
  layout_summary: ""
  field_rules: []
  interaction_rules: []
  permission_rules: []
  status_rules: []
  validation_rules: []
  error_handling: []
```

backend / API / job / data 类 Story 可使用等价字段：

```yaml
story_detail:
  api_path: ""
  event_or_job: ""
  data_object: ""
  request_fields: []
  response_or_output_rules: []
  compatibility_rules: []
  idempotency_rules: []
  error_handling: []
```

## 稳定 ID

- Feature：`FEATURE-001`
- Story：`STORY-001`
- Rule：`RULE-001`
- GWT：`GWT-001`
- Open Question：`QUESTION-001`
- Risk：`RISK-001`

ID 在同一资产包内必须稳定，不随段落移动变化。下游引用优先使用 ID，而不是自然语言标题。

## 状态字段

每个 Feature 和 Story 必须有 gate status：

- `ready`
- `need_revision`
- `blocked`

不允许只写“基本完成”“较好”“高风险”等不可执行描述。

Story front matter 可额外使用 readiness 字段：

- `granularity_readiness`
- `coding_readiness`
- `testing_readiness`
- `overall_decision`

`overall_decision` 允许值：

- `ready`：可进入 coding 和 testing。
- `ready_for_coding_only`：可进入局部 coding / 技术探查，但 testing 仍有需求缺口。
- `ready_for_testing_only`：可进入测试补充或测试设计，但 coding 仍有实现前缺口。
- `need_revision`：方向明确但需补充需求信息。
- `blocked`：关键事实缺失或冲突，继续执行会导致误实现。
