---
name: ai-ready-spec
description: Use when converting an existing V2 requirement spec, demand brief, or PRD draft into a minimal V3 requirement asset package for AI coding and AI testing. Also use when the user asks for GEARS, GWT, Story Map, Feature Gate, Story Gate, or AI-ready requirement assets.
---

# ai-ready-spec

`ai-ready-spec` 是 AI-native Requirement Suite 的正式一等子 skill。它把已有需求材料整理成最小 V3 requirement asset package，使 AI coding / AI testing agent 能引用稳定 ID、理解行为约束、识别开放问题，并判断哪些 Story 已经 ready。

当前 V0.24 已完成 suite shared 对齐和回归规则回流：它是一等 user-facing subskill，依赖 `shared/validators/requirement-asset-validator` 做结构校验，依赖 `shared/templates` / `shared/schemas` / `shared/glossary.md` 保持资产格式一致，依赖 `shared/tools/requirement-wiki-generator` 做后续 human-view 发布支持。它仍不包含代码实现或技术设计。

## 触发条件

使用本 skill 当用户要求：

- 把已有 V2 requirement spec / PRD 草稿 / demand brief 转成 V3 requirement asset package。
- 为一个 Feature 生成 GEARS、GWT、Story Map、Gate Decision。
- 生成适合 AI coding / AI testing 消费的需求输入。
- 判断一个需求资产是否 ready / need_revision / blocked。

不要使用本 skill 当用户：

- 只有模糊创意，需要先做 idea-to-demand。
- 只要求需求质量评审，应使用 review 类能力。
- 要求写代码、接口设计、数据库设计或测试实现。
- 要求把代码开发 PRD 直接转成 skill design spec。

## 工作流程

1. 判断输入是否适合转换。
   - 输入必须至少包含目标用户、业务目标、主要流程或期望行为。
   - 如果核心上下文缺失，输出 missing context，不补造事实。
2. 提取需求骨架。
   - 目标、用户、场景、范围、非目标、约束、开放问题。
   - 明确来源段落或来源文件，避免把推断写成事实。
3. 生成 Feature 结构。
   - iteration-1 默认只生成 1 个 Feature。
   - 使用稳定 ID：`FEATURE-001`。
   - Feature 是能力级资产，只写目标、业务价值、用户/角色、范围/非范围、高层规则、状态/权限/数据边界、共同约束、DFX 约束、影响/兼容摘要和 Story 引用。
   - Feature 不承载完整 Story 细节，不把 Rule/GWT 列表当成 Story 正文。
4. 拆分 2-4 个 Story / Requirement Work Unit。
   - Story 按可验收行为闭环拆分，不按前端、后端、测试等技术任务拆分。
   - 使用稳定 ID：`STORY-001`、`STORY-002`。
   - Story 是详细执行级资产，必须足够支撑 AI coding / AI testing。
   - UI / 管理后台 / 工作流 / 表单 / 列表 / 详情 / 审批类 Story 应优先补充 `story_detail`：菜单路径、页面入口、布局摘要、字段规则、交互规则、权限规则、状态规则、校验规则、异常处理。
   - backend / API / job / data 类 Story 可以用 API 路径、事件、任务、数据对象、错误响应、幂等和兼容规则替代 UI 字段。
5. 生成 GEARS 规则。
   - 使用 `When / While / Where / If / The system shall` 表达行为约束。
   - 每条规则使用稳定 ID：`RULE-001`。
6. 映射 GWT 验收场景。
   - 每条关键规则至少映射 1 个 `Given / When / Then` 场景。
   - 使用稳定 ID：`GWT-001`。
7. 执行 Story 粒度和门禁判断。
   - Gate 只能是 `ready`、`need_revision`、`blocked`。
   - 不使用分数制替代判断。
8. 生成 AI coding / AI testing 输入。
   - coding input 聚焦实现范围、稳定 ID、行为规则、非目标、依赖和开放问题。
   - testing input 聚焦 GWT、边界条件、回归风险、未决问题和验收门禁。
9. 生成 Story 一等资产。
   - 每个 Story 必须有独立 `stories/STORY-*.md` 文件。
   - Story 文件必须包含 YAML front matter、业务目标、用户与场景、范围、非目标、主要流程、`story_detail`、业务规则、验收场景、coding/testing notes、Gate 和 Open Questions。
   - Rule/GWT 是 Story 的内部结构，不能替代 Story narrative。
10. 生成或维护 YAML front matter。
   - 核心 Markdown 资产必须有轻量 front matter，至少包含 `asset_type`、稳定 ID、父级引用、状态、gate decision 和更新时间。
   - Story front matter 必须记录 `requirement_work_unit`、`estimated_effort`、`granularity_readiness`、`coding_readiness`、`testing_readiness`、`overall_decision`、相关 Rule/GWT/DFX 引用。
11. 生成建议版 human-view。
   - `human-view.md` 面向 PM、业务、开发、测试阅读。
   - human-view 是评审资料入口和未来 wiki/html 的前置内容，不替代 AI coding/testing 输入，也不承担完整 HTML/wiki 渲染。
   - human-view 应优先展示自然语言背景、目标、Story、规则摘要、Gate、风险和开放问题；GEARS/GWT/YAML 等机器友好内容只做摘要或折叠展示。
12. 输出缺口。
   - 对缺失字段、冲突、不可测试规则、过大 Story 单独列出。
   - 缺口不能静默消失，也不能被编造成确定需求。
13. 执行 review -> clarification -> revision loop。
   - 每轮生成后必须执行 quality review。
   - 对 `need_revision` / `blocked` 生成开放问题或结构化澄清项。
   - 修订后记录 Gate Decision 和 changelog。
14. 执行生成步骤 checklist。
   - 使用 `references/generation-checklist.md` 逐项检查资产包。
   - 未通过的检查项必须写入 `quality-review.md`，不能只在脑内判断。
15. 执行 shared 对齐检查。
   - 生成前检查输入是否来自 `demand-to-prd-spec` 的 `prd.md` / `feature-story-outline.md` / `handoff-to-ai-ready-spec.md`，或等价 PRD/spec。
   - 生成后用 `shared/validators/requirement-asset-validator` 做结构检查。
   - human-view 保持自然语言入口；AI coding/testing input 保持下游 agent 入口，二者不能混用。
   - 如果 Story 缺少用户场景、主要流程、story_detail、Rule/GWT 或 Gate 原因，标记 `need_revision`，不能补造。
16. 执行 V0.24 回归质量检查。
   - raw idea flow 和 V2 PRD/spec flow 必须在输出中可追踪，不得混淆。
   - `quality-review.md` 必须覆盖资产包内出现的所有 `QUESTION-*`，或明确写出豁免原因。
   - `human-view.md` 必须展示所有 `need_revision` / `blocked` 的 reason 或关联 `QUESTION-*`。
   - `feature-map.md`、`story-map.md` 和 Story 文件中的 Gate 必须一致。
   - validator warning 不应被删除或隐藏，应进入 quality review 或 release readiness。

## 输出结构

默认输出一个最小资产包：

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

若用户没有要求真实写入文件，可以按上述结构输出 Markdown 内容。若写入文件，不能修改原始 V2 spec，除非用户明确要求。

## 质量规则

- 默认中文输出；文件名、ID、固定术语可保留英文。
- 所有可被下游引用的需求、规则和验收场景必须有稳定 ID。
- Story 必须是一等资产；Rule/GWT 只能作为 Story 内部结构，不能替代 Story 正文。
- Feature / Story 边界必须清楚；Feature 不重复 Story 细节，Story 不把实现设计当成 PM 必填内容。
- 核心 Markdown 资产必须包含轻量 YAML front matter，以支持脚本、wiki 生成、AI 引用和质量门禁聚合。
- Story 必须包含 UI/API/job/data 等执行细节之一；缺失时标记 `need_revision`，不能伪造。
- GEARS 必须能映射到至少一个可观察 GWT；不能映射时标记 `testability_gap`。
- Story Gate 和 Feature Gate 必须解释原因，并引用对应 ID。
- 所有 Open Questions 必须在 `prd.md`、`feature-map.md`、`human-view.md` 和 `quality-review.md` 中保持可追踪；如果某个文件不适合展开，必须说明豁免。
- `human-view.md` 是人类消费入口，不得只列机器字段；但必须能让读者看到每个 Story 的 Gate、原因和下一步。
- AI coding / testing input 必须可直接被下游 agent 使用，不能只是摘要。
- 不生成接口、数据库或实现方案；复杂技术设计应交给后续 OpenSpec / technical design。

## 参考材料

- `references/asset-package-structure.md`
- `references/gears-gwt-mapping.md`
- `references/story-granularity-gate.md`
- `references/ai-coding-testing-input-guide.md`
- `references/gate-decision-rules.md`
- `references/generation-checklist.md`
