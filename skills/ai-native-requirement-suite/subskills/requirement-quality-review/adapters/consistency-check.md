# consistency-check Adapter

status: `mvp_v0.20`

## 职责

检查需求资产内部层级、术语、状态、规则和引用关系是否一致。

## 检查项

- Feature / Story / Rule / GWT 引用是否一致。
- PRD、feature-map、story-map、quality-review、human-view 中的 open questions 是否一致。
- Gate 状态和原因是否跨文件一致。
- shared glossary 和 templates 是否被正确使用。

## 输出判断

- `ready`：关键引用一致，Gate 状态和原因跨文件可追踪。
- `need_revision`：存在非阻塞引用缺口或问题清单不一致。
- `blocked`：核心引用断裂、Story 文件缺失、Gate 与原因冲突。
