# Router Result Template

```yaml
input_stage: unknown
recommended_subskill: requirement-router
confidence: low
reason: ""
missing_context:
  - ""
stop_condition: ""
allowed_next_actions:
  - ""
```

## 填写规则

- `reason` 必须说明可观察到的输入信号。
- `missing_context` 必须是具体问题，不写泛泛的“信息不足”。
- `allowed_next_actions` 只能列当前阶段真实允许的动作。
- 不得在 router 结果中生成 PRD、Story、GEARS、GWT 或测试用例。
