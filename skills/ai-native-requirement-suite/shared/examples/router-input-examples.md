# Router Input Examples

status: `mvp_v0.16`

## idea

输入：

> 我想做一个给项目团队用的知识检索助手，能帮成员更快找到决策记录和需求背景，但还没想清楚具体功能。

期望：

```yaml
input_stage: idea
recommended_subskill: idea-to-demand
confidence: high
reason: "输入是早期机会和痛点，没有明确目标用户细分、首期范围和验收口径。"
missing_context:
  - "目标用户是产品、研发、测试，还是项目负责人？"
  - "首期要解决搜索、问答、来源引用，还是过期内容识别？"
stop_condition: "在目标用户和首期痛点不明确前，不应直接生成 PRD。"
allowed_next_actions:
  - "进入 idea-to-demand 做澄清访谈"
```

## demand_brief

输入：

> 目标用户是项目成员。首期要解决需求背景和决策记录难查找的问题，减少重复沟通。已明确不做自动改写源文档。

期望：

```yaml
input_stage: demand_brief
recommended_subskill: demand-to-prd-spec
confidence: high
reason: "输入已有目标用户、首期目标、范围和非目标，但还不是完整 PRD/spec。"
missing_context:
  - "关键业务流程和异常场景还未展开。"
stop_condition: "如果核心流程仍不清楚，应先补充 demand brief。"
allowed_next_actions:
  - "进入 demand-to-prd-spec 生成可读 PRD/spec"
```

## prd_spec

输入：

> 这里是一份 PRD，包含背景、目标用户、功能范围、业务规则、验收标准和开放问题，请转换为 AI coding/testing 可用的资产包。

期望：

```yaml
input_stage: prd_spec
recommended_subskill: ai-ready-spec
confidence: high
reason: "输入已有 PRD/spec，并明确要求转换为 AI coding/testing 可用资产。"
missing_context: []
stop_condition: "如果 PRD 缺少 Story 或验收口径，应在转换中标记 need_revision。"
allowed_next_actions:
  - "进入 ai-ready-spec 生成 V3 requirement asset package"
```

## feature_story

输入：

> FEATURE-001 知识检索，下有 STORY-001 文档索引、STORY-002 带来源引用的问答，已有 GWT 验收条件。

期望：

```yaml
input_stage: feature_story
recommended_subskill: ai-ready-spec
confidence: high
reason: "输入已经是 Feature / Story / GWT 结构，需要整理成标准 V3 requirement asset package。"
missing_context: []
stop_condition: "如果 Story 缺少业务规则或测试入口，应在 asset package 中标记质量缺口。"
allowed_next_actions:
  - "进入 ai-ready-spec 标准化 Feature / Story 资产"
```

## requirement_asset

输入：

> 目录中已有 feature-map.md、story-map.md、stories/STORY-001.md、human-view.md、ai-coding-input.md、ai-testing-input.md，请做质量门禁。

期望：

```yaml
input_stage: requirement_asset
recommended_subskill: requirement-quality-review
confidence: high
reason: "输入已是 V3 requirement asset package，并明确要求质量门禁。"
missing_context: []
stop_condition: "如果用户只要求结构校验而非质量评审，应改用 shared validator。"
allowed_next_actions:
  - "进入 requirement-quality-review 做质量门禁"
  - "必要时先调用 shared/validators/requirement-asset-validator 做结构预检"
```

## low_confidence

输入：

> 帮我弄一下这个需求。

期望：

```yaml
input_stage: unknown
recommended_subskill: requirement-router
confidence: low
reason: "输入没有提供需求内容、阶段、目标用户或期望产物。"
missing_context:
  - "当前是早期想法、需求 brief、PRD/spec，还是已有 V3 资产包？"
  - "你希望下一步产出澄清问题、PRD、AI-ready asset package，还是质量评审？"
stop_condition: "在确认输入阶段和目标产物前，不应进入下游子 skill。"
allowed_next_actions:
  - "请求用户选择输入阶段"
  - "请求用户补充需求材料"
```
