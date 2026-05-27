# Generation Checklist

使用本 checklist 检查每次 V2 -> V3 requirement asset package 生成结果。未通过项必须写入 `quality-review.md`，不能静默忽略。

## 1. 输入适配

- [ ] 输入是已有 V2 requirement spec / demand brief / PRD draft，不是 raw idea。
- [ ] 已识别来源 Feature / Story / FR / AC。
- [ ] 已记录样本来源路径或来源文件名。
- [ ] 已区分事实、推断和开放问题。

## 2. 资产结构

- [ ] 生成根目录入口：`README.md`、`prd.md`、`feature-map.md`、`ai-coding-input.md`、`ai-testing-input.md`、`quality-review.md`、`human-view.md`。
- [ ] 至少生成一个 `features/FEATURE-001/`。
- [ ] Feature 目录包含 `feature-spec.md`、`story-map.md`、`ai-coding-input.md`、`ai-testing-input.md`、`quality-review.md`。
- [ ] Feature 目录包含 `stories/STORY-*.md`。
- [ ] 核心 Markdown 资产包含 YAML front matter，至少标识 `asset_type`、稳定 ID、状态、Gate 和更新时间。

## 3. 稳定 ID

- [ ] Feature 使用 `FEATURE-*`。
- [ ] Story 使用 `STORY-*`。
- [ ] Rule 使用 `RULE-*`。
- [ ] GWT 使用 `GWT-*`。
- [ ] Open Question 使用 `QUESTION-*`。
- [ ] `feature-map.md` 能把 Source ID 映射到新 ID。
- [ ] 每个 Story 都有独立 `stories/STORY-*.md`，且 Rule/GWT 只作为 Story 内部结构出现。

## 4. Story 粒度

- [ ] Story 按可验收行为闭环拆分，不按前端/后端/测试任务拆分。
- [ ] 每个 Story 有 Gate：`ready`、`need_revision` 或 `blocked`。
- [ ] Gate 有原因和关联 ID。
- [ ] 过大的 Story 已被拆分或标记为 `need_revision`。
- [ ] 每个 Story 文件有业务目标、用户与场景、范围、主要流程和非目标。
- [ ] 每个 Story front matter 包含 `requirement_work_unit`、`estimated_effort`、`granularity_readiness`、`coding_readiness`、`testing_readiness`、`overall_decision` 和相关 Rule/GWT 引用。
- [ ] 每个 Story 包含 `story_detail` 或等价的 API/job/data 细节字段。
- [ ] Rule/GWT 位于 Story 内部，不替代 Story narrative。

## 4.1 Feature / Story 边界

- [ ] Feature 只描述能力目标、业务价值、用户/角色、范围/非范围、高层规则、状态/权限/数据边界、共同约束、DFX 约束、影响/兼容摘要和 Story 引用。
- [ ] Feature 不重复 Story 的完整流程、字段、按钮、异常和 GWT 细节。
- [ ] Story 承载具体菜单路径、页面入口、布局摘要、字段规则、交互规则、权限规则、状态规则、校验规则和异常处理。
- [ ] backend/API/job/data 类 Story 用 API path、event/job、data object、错误响应、幂等、兼容规则等字段替代 UI 细节。

## 5. GEARS / GWT

- [ ] 每条关键业务规则有 `RULE-*`。
- [ ] Rule 使用可观察行为表达，而不是实现步骤。
- [ ] 每条关键 Rule 至少映射一个 GWT。
- [ ] GWT 的 Then 可验收。
- [ ] 无法映射的规则标记为 `testability_gap`。

## 6. AI Coding / Testing 输入

- [ ] `ai-coding-input.md` 明确 ready scope、non-goals、关键规则、依赖和开放问题。
- [ ] `ai-testing-input.md` 明确 GWT 入口、边界条件、回归风险和阻塞项。
- [ ] coding/testing 输入不凭空生成接口、数据库、架构或测试实现细节。

## 7. 缺口与门禁

- [ ] `quality-review.md` 明确 Feature Gate。
- [ ] Missing context 被写成 `QUESTION-*` 或 risk，不被补造。
- [ ] `need_revision` / `blocked` 项能说明谁需要补什么信息。
- [ ] 如果后续需要 OpenSpec / technical design，已明确触发原因。
- [ ] 已执行 `generate -> quality review -> open questions -> clarification / structured questions -> revision -> Gate Decision -> changelog` 循环，或明确本轮豁免原因。

## 8. 下游可消费性

- [ ] 下游 coding agent 可以引用 Story / Rule / GWT ID。
- [ ] 下游 testing agent 可以直接从 GWT 开始规划验收。
- [ ] 下游需要追问的问题被集中列出，而不是散落在正文。

## 9. Human View

- [ ] `human-view.md` 能让非执行 agent 的人类读者理解背景、目标、Story、规则摘要和开放问题。
- [ ] human-view 不暴露过多低层 GWT 细节，只保留关键验收摘要。
- [ ] human-view 明确当前 Gate 状态和不能直接开发的部分。
- [ ] human-view 可作为未来 wiki/html 的前置内容：有稳定标题、Feature/Story 导航、Gate 摘要、风险/开放问题摘要和引用 ID。
