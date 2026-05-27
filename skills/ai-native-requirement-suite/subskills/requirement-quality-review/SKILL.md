---
name: requirement-quality-review
description: Use when reviewing requirement completeness, testability, AI coding/testing readiness, and gate decision for AI-native requirement assets.
---

# requirement-quality-review

status: `hardened_v0.24`

## 职责

基于测试可用性、需求完整性、AI coding/testing 可消费性进行质量门禁。

## V0.20 能力

- 消费 V3 requirement asset package 和可选 validator report。
- 输出 `ready`、`need_revision` 或 `blocked`。
- 区分业务缺口、结构缺口、测试可用性缺口、AI coding/testing 消费缺口。
- 输出可回流给 `idea-to-demand`、`demand-to-prd-spec` 或 `ai-ready-spec` 的修订建议。
- 不复制 validator 脚本逻辑；结构检查结果来自 `shared/validators/requirement-asset-validator`。

## 输入

- `requirement-asset/` 目录。
- 可选 `validation-report.json` / `validation-report.md`。
- 可选人工 review 意见。

## 输出结构

```text
quality-gate/
  quality-review.md
  revision-actions.md
  downstream-consumer-check.md
```

## Gate 规则

- `ready`：无结构阻塞，Story 粒度、测试可用性、AI coding/testing 输入均可消费。
- `need_revision`：方向明确，但存在开放问题、测试缺口、Story 细节不足或下游消费风险；必须给出原因和回流目标。
- `blocked`：核心文件缺失、核心 ID 不一致、目标用户/范围/关键流程缺失，继续下游会导致误实现。

## 检查维度

- 业务完整性：目标用户、问题、业务目标、范围、非目标、场景和开放问题是否清楚。
- 结构一致性：使用 validator report 和 `adapters/consistency-check.md`。
- 测试可用性：使用 `adapters/testability-check.md`。
- AI 可消费性：使用 `adapters/ai-readiness-check.md`。

## 质量规则

- 每个 `need_revision` / `blocked` 必须有原因、证据路径、影响范围和回流目标。
- 每个 `need_revision` / `blocked` 必须引用至少一个 `QUESTION-*`、`QR-*`、Story ID 或具体证据路径；不能只写“待确认”“需补充”。
- `quality-review.md` 必须覆盖资产包内出现的所有 `QUESTION-*`，或明确写出“不阻塞本轮”的豁免理由。
- `human-view.md` 中出现的每个 `need_revision` / `blocked` 必须有 reason 或 QUESTION 引用，避免人类读者只看到状态看不到原因。
- 如果 validator report 中存在 `quality_review_missing_questions`、`missing_question_list` 或 `readiness_missing_reason`，quality review 不得标记为 `ready`。
- 对 V2 PRD/spec 输入，quality review 应区分“源需求真实缺口”和“转换过程缺口”；前者回流给 PM，后者回流给 `ai-ready-spec`。
- 对 raw idea 输入，quality review 应默认更保守；除非需求范围、目标用户、Story detail 和验收口径都足够明确，否则不应整体标记为 `ready`。
- 不把 `ready_for_coding_only` 解释为完整 ready。
- 不用分数代替 Gate。
- 不生成测试用例实现、接口设计或数据库设计。
