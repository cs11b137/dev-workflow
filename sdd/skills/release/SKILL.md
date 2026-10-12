---
name: release
description: Release or publish a new version of a repo that has docs/release.md, including version bumps, platform continuation after a CI failure, and release notes/changelog. Defaults to tag release through CI.
---

# 发布

项目的发布事实（版本号所有者、tag 格式、CI 工作流、平台、读回命令）在 `docs/release.md`，先读它。其中还有 TODO 时，先和用户补齐再继续。

## 选择流程

| 用户意图 | 读 |
| --- | --- |
| 普通的发布请求，没有指定方式 | `tag-release.md`（**默认**） |
| 明确要求本地打包、手动发布、单平台补发或续发 | `manual-release.md` |
| 只改发布配置或凭据 | 改完配置按 `finish` 收尾；不打 tag、不发布 |

用户没指定方式时，直接用 tag 发布，不问用户选哪种。CI 失败时报告原因，不自动改用手动打包。用户明确指定的本地发布或单平台范围，优先于默认的全平台范围。

## 共享约束

- 先看 `git status`；冻结发布源码之前，先提交本任务的改动。
- 版本号只改 `docs/release.md` 登记的所有者文件，lockfile 用包管理器同步。
- 选版本前查询实际已有的 releases 和 tags；版本号与 build 号严格递增；已发布的 tag 和文件不可变。
- tag 和所有平台产物绑定同一个完整 SHA；产物只从干净的源码构建。
- 每个新版本都按 `release-notes.md` 写更新日志。
- push tag 需要用户为本任务授权；本任务里已经授权过的，不重复询问。

## 完成标准

推了 tag 不等于发布完成。全部满足才算完成：

1. 所选平台的 CI 任务全部成功；
2. `docs/release.md` §3 的每条读回检查都返回新版本；
3. 更新日志已写入并读回核对；
4. 最新稳定版已标记为 Latest 并读回（候选版、草稿、预发布版不标记；续发旧版本时保留更新的那个 Latest）：

   ```bash
   gh release edit "$tag" --repo "$repo" --latest
   gh api "repos/$repo/releases/latest" --jq '.tag_name'
   ```

最终报告：Release 链接、版本与 SHA、各平台结果、读回结果、更新日志的覆盖核对、跳过项。
