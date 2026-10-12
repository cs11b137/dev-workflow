---
name: change
description: Spec-driven procedure for implementation work in a repo with docs/development-workflow.md. Use before editing code or docs for a new feature, UI change, bug fix, protocol/format/public-behavior change, refactor or perf work, docs edit, or when spec and code disagree.
---

# 规格驱动的改动

插件根目录 = 本 skill 目录的上两级。场景细则在本 skill 的 `scenarios/` 下。

## 1. 定位（每个场景都做）

1. `git status --short`：已有改动记为用户所有，全程保持原样。
2. 读根 `AGENTS.md` 的路由表，从 `docs/` 选 1–3 个相关章节读；再读目标目录的 README、局部 `AGENTS.md` 和相邻测试。
3. 写下三件事：这个行为归属的规范章节（文档 § 号）、实现位置、相邻测试。规格里有定义只说明它是目标合同，是否已实现以代码为准。

完成标准：三件事都有具体路径或章节号；找不到规范章节时记为「规格缺失」，按 spec-conflict 场景处理。

## 2. 判定场景

| 场景 | 判定 | 读 |
| --- | --- | --- |
| feature | 新能力，规格里还没有 | `scenarios/feature.md` |
| ui | 用户可见的布局、视觉、交互、文案或状态变化 | `scenarios/ui.md` |
| bugfix | 实现偏离现有规格 | `scenarios/bugfix.md` |
| contract | 有意改变协议、格式或公开行为（参数、默认值、错误码、退出语义、JSON 输出） | `scenarios/contract.md` |
| refactor | 外部行为不变的重构或性能优化 | `scenarios/refactor.md` |
| docs | 只改文档、规范或代理指令 | `scenarios/docs.md` |
| spec-conflict | 规格缺漏、自相矛盾，或修复需要做产品决定 | `scenarios/spec-conflict.md` |

一个任务可以跨场景（如 feature 带 ui）：按表中顺序依次走，每个场景的步骤都做完。只读对应的场景文件。

## 3. 收尾

场景步骤做完后，调用 `finish` skill 完成验证、提交与交付说明。
