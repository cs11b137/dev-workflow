# AGENTS.md

{{PROJECT_NAME}} 编码代理的通用规则。本文只保留全局约束和阅读入口；细则按任务加载，目录内的 `AGENTS.md` 补充局部约束。

## 阅读与语言

- 默认跟随用户输入的语言回复；代码标识符、命令与已有术语保持原样。
- 先按下表定位，再从相关文档选 1–3 个章节读，随后看目标目录的 README、局部 `AGENTS.md` 与相邻测试；不要通读 `docs/`。
- 根文件保持精简，不超过 80 行；新增细则放到所属文档，在这里写触发条件与链接，不复制正文。

## 按需阅读

| 何时 | 读什么 |
| --- | --- |
| 定位模块、运行项目 | [根 README](README.md)；目录边界见[仓库约定](docs/repo-conventions.md) |
| 新建文件、包或模块 | [仓库约定](docs/repo-conventions.md) |
| 产品、架构、格式、协议行为 | [文档阅读路线](docs/README.md#阅读路线) |
| 修改规范或其他文档 | [文档约定](docs/README.md#文档约定)；[开发流程 §1](docs/development-workflow.md#1-规范与实现) |
| 准备验证改动 | [开发流程 §2](docs/development-workflow.md#2-验证)；标准见[验收与测试](docs/acceptance/acceptance-spec.md) |
| 修改用户可见 UI（原型先行） | [开发流程 §3](docs/development-workflow.md#3-多端同步) |
| 修改语言处理或平台专属实现 | [开发流程 §4](docs/development-workflow.md#4-语言与平台) |
| 修改依赖、生成物，或使用 worktree | [开发流程 §5](docs/development-workflow.md#5-工作区与产物) |
| 发布 | [发布约定](docs/release.md) |

## 通用约束

- 协议、格式或公开行为有意变化时，在同一任务同步实现、规范与测试；发现冲突明确说明，不为迁就实现擅改规格。
- UI 变化先只改原型并交用户确认，确认后才改真实实现；届时审计各表面的对应功能，无对应功能说明原因。
- 验证按影响选择最小但充分的范围；视觉改动检查实际页面；只把实际执行过的检查报告为通过。
- 产品能力不假定某种语言或平台为缺省；语言分支有明确兜底，平台专属代码条件化。
- 依赖变化同步 lockfile；生成物遵守所属目录规则；临时产物放仓库外的临时目录。

## 强制完成门

凡是修改文件的实现任务，都必须在最终回复前创建 git commit。

- 开始编辑前检查 `git status`，任务前已有或并发出现的改动视为用户所有。
- 提交前审阅最终 diff，按风险运行适量验证；报告实际执行的检查和已知跳过项。
- 只暂存本任务的文件或 hunk；`git add` 后复核 `git diff --cached`。
- 提交信息用 `type(scope): summary`（见[提交分类](docs/development-workflow.md#11-提交分类)），默认英文，最终回复报告 commit hash。
- 只创建本地 commit；push 由用户针对当前任务另行明确要求，之前任务的授权不沿用。
- 分支合回 `main` 前按[合并前提交整理](docs/development-workflow.md#12-合并前提交整理)归并；此外不 amend、不改写历史。只读任务不创建空提交。
- worktree 用完即清：完成时删除 worktree、分支与专用构建目录（先合并，或提交并打 `archive/<worktree 名>` tag）；确需保留的在最终回复里点名路径与原因。
