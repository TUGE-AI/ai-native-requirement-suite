# GEARS / GWT Mapping

## GEARS 规则

GEARS 用来表达可验收的行为约束。iteration-1 使用以下句式：

```text
RULE-001
When <触发事件>
While <前置状态或持续状态>
Where <场景或边界>
If <条件>
The system shall <可观察行为>
```

不是每条规则都必须包含所有字段，但 `The system shall` 必须存在，并且必须是可观察行为。

## GWT 场景

每条关键 GEARS 规则至少映射一个 GWT：

```text
GWT-001
Given <已知前置条件>
When <用户或系统动作>
Then <可观察结果>
Related rule: RULE-001
```

## 映射要求

- GWT 必须引用至少一个 `RULE-*`。
- 一个 Rule 可映射多个 GWT。
- 一个 GWT 不应混合多个互斥行为。
- 如果 Rule 无法写出可观察 Then，标记 `testability_gap`。

## 常见错误

- 把实现动作写成需求行为，例如“调用接口保存数据”。
- 把模糊质量词写成 Then，例如“页面体验良好”。
- 把异常、权限、空状态漏掉，导致测试 agent 无法规划验收。
- 没有写清触发条件，导致 coding agent 自行猜测入口。
