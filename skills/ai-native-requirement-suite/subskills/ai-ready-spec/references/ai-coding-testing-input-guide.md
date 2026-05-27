# AI Coding / Testing Input Guide

## AI Coding Input

`ai-coding-input.md` 面向实现 agent，应包含：

- 入口说明：要实现哪个 Feature / Story。
- 稳定引用：Feature、Story、Rule、GWT ID。
- 实现范围：必须做什么、明确不做什么。
- 行为规则：GEARS 摘要和关键 GWT。
- 依赖上下文：已有系统、权限、数据、外部服务。
- 开放问题：会影响实现决策的问题。
- Gate 状态：哪些 Story ready，哪些不能进入实现。

不要在 coding input 中凭空生成接口、数据库、框架选型或内部架构。

## AI Testing Input

`ai-testing-input.md` 面向测试 agent，应包含：

- 验收目标：要验证的 Feature / Story。
- GWT 场景列表：每个场景引用对应 Rule。
- 边界条件：权限、空状态、异常、兼容、回归风险。
- 非目标：本轮不测试什么。
- 阻塞项：哪些缺口会导致测试计划不可靠。
- 判定标准：ready / need_revision / blocked 的原因。

## 下游消费检查

后续 downstream consumer check 应记录：

- 下游 agent 是否能引用稳定 ID。
- 下游 agent 需要追问多少问题。
- 下游 agent 是否误解范围或自行补造需求。
- 下游 agent 是否能形成下一步 coding/testing 行动。
