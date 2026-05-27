# testability-check Adapter

status: `mvp_v0.20`

## 职责

检查需求是否足以支持测试人员设计测试用例。

## 检查项

- Story 是否有可观察验收结果。
- Rule 是否能映射到 GWT。
- Open Questions 是否阻塞测试设计。
- `need_revision` / `blocked` 是否有可见原因。

## 输出判断

- `ready`：关键 Story 均有 GWT 或等价验收场景，边界条件可推导。
- `need_revision`：存在可补充的验收缺口，例如异常流程、状态边界或开放问题未覆盖。
- `blocked`：关键行为不可观察，或缺少足以设计测试的用户流程。
