# 更新日志

每个新版本都根据实际包含的 commit 和 PR 生成。整理过程放在仓库外的临时目录（下称 `$WORK`）。

## 1. 确定范围

1. 固定完整的 `source` SHA。
2. 基线：同一渠道上一个**已公开发布**的版本 tag 及其完整 SHA。不要用仓库全局的 Latest、未发布的候选 tag、日期窗口或「最近 N 条」来代替。
3. 确认基线是 `source` 的祖先：`git merge-base --is-ancestor <base> <source>`。不是祖先或无法唯一确定时，停下来先解决范围问题。首次发布：明确起点；没有约定时用 `source` 可达的完整历史。
4. 浅克隆或缺 tag 时，先 `git fetch --unshallow --tags` 补齐。

## 2. 收集完整来源

```bash
git rev-list --count "$base..$source" > "$WORK/count.txt"
git log --reverse --topo-order --format='%H%x09%s' "$base..$source" > "$WORK/commits.tsv"
```

不要用 `--max-count`、`--first-parent` 或路径过滤来缩小范围。按 SHA 查找关联 PR（`gh api repos/<repo>/commits/<sha>/pulls`，或 `gh pr list --search <sha> --state merged`），列表接口要翻完所有分页。没有 PR 的提交，用 commit 正文和 diff 补齐。

## 3. 来源台账与分批总结

1. 建立台账 `$WORK/ledger.tsv`：`sha  source_group  pr  batch  disposition  note`。每个 SHA 恰好归入一个来源组；同一 PR 的多个 commit 归为一组。
2. 内容少时直接整理。多时按时间或模块分批，每批 30–50 个来源组；可以对每一批调用 `changelog-batcher` 子代理，给它这一批的 SHA 清单和仓库路径。
3. 每批的摘要记录：用户可见的功能、修复、兼容性与迁移、平台限制、相关工程变更，以及对应的 SHA／PR。内部改动也要登记，标为「内部，无用户可见变化」。没有证据的影响，不要推测。
4. 全部批次完成后，合并同类项：同一功能合成一条；已撤销、未出货的变化不写成新功能；不同的修复、限制、迁移事项分别保留。`docs`、`chore` 等类型也进入台账，再按实际影响决定是否进入正文。

## 4. 覆盖核对

- 所有批次的来源并集 = `commits.tsv`，数量等于 `count.txt`。
- 每个来源组都有最终条目，或明确的省略理由（内部 / 重复 / 已撤销）。

核对不通过，就不能宣称「完整整理」。

## 5. 写入与读回

1. 正文默认英文，面向用户描述结果，附 PR 或 commit 链接作为依据。保存为 `$WORK/release-notes.md`。
2. 等 CI 写完平台说明之后，读取现有正文，把更新日志和平台说明整合到一个新文件里，然后：

   ```bash
   gh release edit "$tag" --repo "$repo" --notes-file "$notes_file"
   gh release view "$tag" --repo "$repo" --json body,url,tagName
   ```

3. 读回核对：版本与范围正确、平台说明保留、没有重复段落。
4. 报告：Release 链接、比较范围（`base..source`）、commit 数与 PR 数、批次数、覆盖核对结果、缺失的来源。
