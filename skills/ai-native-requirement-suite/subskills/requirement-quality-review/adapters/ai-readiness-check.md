# ai-readiness-check Adapter

status: `mvp_v0.20`

## 职责

检查需求资产是否足以被 AI coding / AI testing workflow 消费。

## 检查项

- AI coding input 是否明确范围、非目标、依赖和开放问题。
- AI testing input 是否包含 GWT、边界条件和回归风险。
- Story、Rule、GWT、Question 是否有稳定 ID。
- `ready_for_coding_only` 不得被误判为完整 ready。

## 输出判断

- `ready`：AI coding/testing 入口均可直接消费，并保留稳定 ID。
- `need_revision`：AI coding 或 testing 入口缺少上下文、边界或问题说明。
- `blocked`：缺少 AI coding/testing 入口，或入口与 Story/Gate 冲突。
