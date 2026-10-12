# Tag 发布（默认）

## 准备源码与 tag

1. 查看 `git status`，查询实际的 releases、tags 和各平台的更新源：`gh release list --limit 20`，`git tag --sort=-v:refname | head`。
2. 确定新版本号（以及 build 号）。只在需要时修改版本号所有者文件，再用包管理器同步 lockfile。tag 严格等于 `docs/release.md` 的格式。
3. 按改动跑相应检查，审阅 diff，只提交本任务的文件（`chore(release): <version>`）。
4. 确认冻结的源码已在远端 `main` 上，并且包含发布工作流。需要 push `main` 时，先取得本任务的授权。
5. 推 tag 之前，向用户展示：版本号、build 号、tag、完整源码 SHA、要发布的平台。
6. `git tag <tag> <sha>`，`git push origin <tag>`。

## 跟进 CI 直到完成

1. 列出这个 tag 触发的工作流运行：`gh run list --commit <sha>`。用 `gh run watch <id>` 跟进每个平台。
2. 任一任务失败：读日志（`gh run view <id> --log-failed`），报告原因和建议。没有用户指示时，不改用手动打包。
3. 全部成功后，执行 `docs/release.md` §3 的每条读回检查。
4. 按 `release-notes.md` 写更新日志并读回核对。
5. 标记 Latest 并读回（见 SKILL.md 的完成标准）。
