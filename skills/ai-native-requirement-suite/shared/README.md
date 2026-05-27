# Shared Assets

`shared/` 承载 AI-native Requirement Suite 内部复用资产，不作为默认 user-facing subskill 列表。

## 当前资产

- `schemas/`：共享 schema 承载位置。
- `templates/`：共享模板承载位置。
- `glossary.md`：共享术语表。
- `examples/`：共享示例承载位置。
- `install.md`：suite-level 安装说明承载位置。
- `methodology-orchestration.json`：外部/相邻 skill 与方法论风格的默认编排配置。
- `validators/requirement-asset-validator`：V3 requirement asset package 结构校验器。
- `tools/requirement-wiki-generator`：HTML human-view / review cockpit 生成工具。

## 使用边界

- shared asset 可以被一等子 skill 调用。
- shared asset 可以保留独立验证历史。
- shared asset 不应被误列为 PRD V3.0 首期一等子 skill。
- 外部/相邻 skill 应按 `methodology-orchestration.json` 优先解析；对应 skill 不可用时，降级为同等风格的问题策略或评审视角。
