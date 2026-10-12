# 发布约定

{{PROJECT_NAME}} 的发布事实。发布步骤由 sdd 插件的 `release` skill 执行，本文只记录本项目特有的值。

## 目录

- [1. 版本](#1-版本)
- [2. 渠道与产物](#2-渠道与产物)
- [3. 读回检查](#3-读回检查)
- [4. 更新日志](#4-更新日志)

## 1. 版本

| 项 | 值 |
| --- | --- |
| 版本号的唯一所有者 | <!-- TODO(sdd): 如 `package.json` 的 `version` --> |
| 需要同步的文件 | <!-- TODO(sdd): 如根 lockfile；用包管理器同步 --> |
| tag 格式 | `v<version>` |
| build 号 | <!-- TODO(sdd): 有则写来源与递增规则；没有写「无」 --> |
| 默认发布方式 | tag 发布：推 tag 后由 CI 构建并发布 |

## 2. 渠道与产物

| 平台 / 渠道 | CI 工作流 | 产物 | 签名 / 公证 |
| --- | --- | --- | --- |
<!-- TODO(sdd): 每个平台或发布渠道一行（npm、PyPI、GitHub Release、应用安装包……）。 -->

## 3. 读回检查

发布完成需要以下每项都读回一致：

<!-- TODO(sdd): 列出读回命令，例如：
- `gh release view v<version> --json assets,body`
- `npm view <pkg>@<version> version`
- 下载页 / 更新源（appcast、feed）返回新版本
-->

## 4. 更新日志

- 仓库：<!-- TODO(sdd): owner/repo -->
- 基线：同一渠道上一个已公开发布的版本 tag。
- 语言：英文（用户另行指定时按要求）。
- 写入位置：GitHub Release 正文<!-- TODO(sdd): 另有 CHANGELOG.md 时写明 -->。
