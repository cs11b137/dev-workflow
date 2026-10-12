---
name: finish
description: Completion gate for repos with docs/development-workflow.md. Use when implementation is done and before the final reply (verify, commit, delivery note), or when merging a task branch or worktree back to main.
---

# 完成门

插件根目录 = 本 skill 目录的上两级。

## 1. 验证

1. 列出本任务改动覆盖的范围（`git diff --stat` 加上未跟踪的新文件），对照 `docs/development-workflow.md` §2 的验证矩阵，为每个范围选出检查命令。
2. 逐条执行。失败就修复后重跑这一条；修复改动了别的范围时，把那个范围加进来。
3. UI 变化：打开实际页面，检查目标状态、交互和控制台，按影响覆盖主题、尺寸、弹层、键盘焦点。
4. 分三栏记录结果：构建、自动测试、视觉验收。无法执行的检查（缺工具链、凭据、平台）记为「未测 + 原因」。

完成标准：每个改动范围都有「通过」或「未测 + 原因」，没有空白项；报告为通过的检查都在本次会话里实际执行过。

## 2. 同步核对

- 公开行为变了：规格、实现、测试是否都在本次改动里？
- 用户可见 UI 变了：原型是否已确认，§3 表里每个表面是否都有「已同步」或「不适用 + 依据」？
- 规格与实现的差异：是否都已记录下来，准备写进交付说明？

## 3. 提交

1. `git status --short`，和任务开始时的状态对比，分出本任务的文件。
2. 审阅最终 `git diff`。
3. 只暂存本任务的文件或 hunk（必要时用 `git add -p`），然后复核 `git diff --cached`。
4. 提交：`type(scope): summary`，默认英文，按 `docs/development-workflow.md` §1.1 选择 type 和 scope，同类修复沿用已有 scope；正文写原因、影响，破坏兼容时写 `BREAKING CHANGE:`。
5. 只读任务、没有文件改动的任务不提交。

push 只在用户为**本任务**明确要求时执行（插件的钩子会在 push 前请求确认）。

## 4. 分支与 worktree

工作在任务分支或 worktree 上，或者用户要求合并时，读 `merge.md` 并执行。

## 5. 交付说明

按 `<插件根>/templates/extra/delivery-note.md` 的结构写最终回复：结果、改动、验证（三栏加未测项）、多端同步、与规格的差异、commit hash（注明「本地，未 push」）。原型阶段要写明「真实页面尚未改动，等待确认」。
