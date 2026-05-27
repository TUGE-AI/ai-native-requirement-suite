---
name: ai-native-requirement-suite
description: Use when routing, clarifying, drafting, converting, reviewing, validating, or preparing AI-native requirement assets for AI coding, AI testing, and human review.
---

# AI-native Requirement Suite

本 suite 是 AI-native 需求分析与规约技能套件的统一入口。当前 V0.25 已完成 raw idea 端到端验证、V2 PRD/spec 回归验证、质量规则回流，以及第三方方法编排与用户使用体验固化。它仍是 validated with revision items 版本，不是正式公开发行版。

## 一等子 Skill

| Subskill | 状态 | 职责 |
|---|---|---|
| `subskills/requirement-router` | hardened | 统一入口，判断输入阶段并输出路由建议 |
| `subskills/idea-to-demand` | hardened | 从模糊想法到 demand brief / 首期需求计划 |
| `subskills/demand-to-prd-spec` | hardened | 从已确认需求到人类可读 PRD/spec |
| `subskills/ai-ready-spec` | hardened | 将 PRD/Story 转换为 GEARS + GWT + AI coding/testing 输入包 |
| `subskills/requirement-quality-review` | hardened | 基于测试可用性、需求完整性和 validator report 进行质量门禁 |

## Shared 内部资产

| Shared Asset | 职责 |
|---|---|
| `shared/validators/requirement-asset-validator` | 校验 V3 requirement asset package 结构、ID、Gate、开放问题和下游消费入口 |
| `shared/tools/requirement-wiki-generator` | 生成 HTML human-view / review cockpit，作为后续发布和人工阅读工具 |

## 默认编排

```text
input idea / demand / PRD / Story
  -> requirement-router
  -> idea-to-demand 或 demand-to-prd-spec
  -> ai-ready-spec
  -> requirement-quality-review
  -> shared validators / tools as needed
```

## V0.25 使用边界

- 可以用于解释 suite 结构、映射已有资产、规划后续子 skill 迭代。
- 可以使用 `requirement-router` 判断输入阶段，并输出结构化路由结果。
- 可以使用 `idea-to-demand` 把模糊想法整理为 demand brief 和首期范围建议。
- 可以使用 `demand-to-prd-spec` 把已确认 demand brief 转成人类可读 PRD/spec。
- 可以使用 `ai-ready-spec` 处理已有 PRD/spec，并生成 V3 requirement asset package。
- 可以使用 `requirement-quality-review` 消费资产包和 validator report，输出 `ready` / `need_revision` / `blocked`。
- `requirement-router` 只输出决策，不执行完整子 skill。
- `idea-to-demand` 只输出 demand brief，不生成 PRD/spec、Story、GEARS/GWT 或技术设计。
- `demand-to-prd-spec` 不生成接口、数据库、技术设计或 AI coding/testing 输入包。
- `ai-ready-spec` 不替代质量门禁；生成后仍需 `requirement-quality-review`。
- `requirement-quality-review` 不复制 validator 脚本逻辑，也不替代人工业务判断。
- 不应把 `requirement-asset-validator` 当作一等 user-facing subskill 推荐安装；它是 shared validator。
- 不应把 `requirement-wiki-generator` 当作 V3.0 PRD 首期一等子 skill；它是 shared publishing/tooling asset。
- raw idea 与历史 V2 PRD/spec 必须先由 `requirement-router` 分流：raw idea 走 `idea-to-demand`，已有 PRD/spec 走 `ai-ready-spec`。
- quality review 必须覆盖所有 `QUESTION-*`，并让 `human-view` 中的 `need_revision` 原因可见。
- validator warning 不等于失败，但必须进入 quality review 或 release readiness，不得静默忽略。
- 用户默认可以自然语言使用本 suite，不需要知道第三方 skill 命令。
- 用户也可以手动指定 `brainstorming`、`office-hours`、`grill-me`、`grill-with-docs`、`plan-ceo-review` 或 `plan-eng-review` 等命令或风格；suite 应优先纳入方法组合，但不能越过阶段边界。
- 第三方 skill 可用时优先调用；不可用时降级为 `shared/methodology-orchestration.json` 定义的同等风格策略，不得声称已真实调用不可用 skill。
- `idea-to-demand` 和 `demand-to-prd-spec` 必须输出或包含 `methodology_trace` / `methodology-trace.md`，说明入口模式、采用方法、用户指定方法、降级情况、跳过原因和停止依据。
