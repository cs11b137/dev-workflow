# 合并前提交整理与 worktree 清理

## 整理提交

1. 确定合入基线：`git merge-base HEAD main`。
2. 看全部改动：`git log --reverse <base>..HEAD` 和 `git diff <base>..HEAD --stat`。
3. 按独立事项分组：同一功能或修复（及其文档、测试）归为一组；互不相关的事项各自一组。已撤销的尝试不单独成组。
4. 记下整理前的树：`git rev-parse HEAD^{tree}`。
5. 在本任务独占的分支上重建提交（如 `git reset --soft <base>` 后按组 `git add` + `git commit`）。每条提交按 §1.1 命名，摘要写最终交付的结果，正文列出具体修复、限制、迁移要求与 PR／issue。
6. 核对 `git rev-parse HEAD^{tree}` 与第 4 步一致（净改动等价）。不一致就停下来排查。
7. 重新跑受影响的验证。

适用范围：只整理本任务尚未合入的提交。`main`、已发布 tag、共享分支和他人的提交保持原历史；共享分支在合入时用 squash 达到同样效果，PR 标题与 squash 正文遵守同样的命名要求。

## 合入

用户要求合入时，在主检出执行 `git merge --ff-only <分支>`（或用户指定的方式）。有冲突时停下来报告，不要自行改写对方的提交。

## 清理 worktree

任务完成时，二选一：

- **已合并**：`git worktree remove <路径>`，`git branch -d <分支>`。
- **不合并**：先把未提交的改动提交到该分支，`git tag archive/<worktree 名> <分支>`，再 `git worktree remove <路径>`，`git branch -D <分支>`。

同时删除这个 worktree 专用的构建目录，并停掉本任务启动的预览服务。

确实需要保留的（等用户裁决、有冲突待解决），在交付说明里点名路径与原因。

完成标准：`git worktree list` 里不再有本任务的 worktree，除非交付说明点名保留。
