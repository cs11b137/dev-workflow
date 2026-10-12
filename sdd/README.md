# sdd：规格驱动开发插件

把「规格是唯一事实源、原型先行、按影响验证、强制完成门、可追溯发布」这套方法论打包成 Claude Code 插件。方法论原文见 [`../ai-dev-workflow-methodology.md`](../ai-dev-workflow-methodology.md)，提炼自 [BaoCut](https://github.com/JimLiu/baocut)。

## 安装

```bash
claude plugin marketplace add cs11b137/dev-workflow
claude plugin install sdd@dev-workflow
```

开发调试时可直接加载：`claude --plugin-dir /path/to/dev-workflow/sdd`。

依赖：`git`、`python3`；发布流程需要 `gh`。

## 快速开始

1. 在目标仓库运行 `/sdd:init`，生成 `AGENTS.md`、`CLAUDE.md`、`docs/` 规格骨架，并按真实技术栈填好验证矩阵。
2. 补全产品设计 §1、§9、§10（直接说「按 sdd 写 <功能> 的规格」）。
3. 之后正常提需求即可：`change` skill 判定场景，`finish` skill 收尾。

## 组件

| 组件 | 调用 | 作用 |
| --- | --- | --- |
| `init` | `/sdd:init [项目名] [--prototype <app>]` | 复制模板，合并已有 AGENTS.md / CLAUDE.md，按 `package.json`、Cargo、pyproject 等填写验证矩阵、目录约定、发布约定，审计后提交 |
| `change` | 自动（实现任务开始前） | 定位规格章节、实现与测试，判定场景：feature / ui / bugfix / contract / refactor / docs / spec-conflict，按场景细则执行 |
| `finish` | 自动（实现完成、合并分支时） | 按验证矩阵验证，构建 / 测试 / 视觉分栏报告，只暂存本任务文件，`type(scope)` 提交，整理分支与 worktree，写交付说明 |
| `release` | 自动（「发布」「出新版本」） | 默认 tag 发布；手动发布与单平台续发；完整 commit 台账、分批总结、覆盖核对的更新日志；读回检查并标记 Latest |
| `acceptance` | `/sdd:acceptance [条目]` | 隔离环境执行端到端验收，写带证据的执行记录 |
| `audit` | `/sdd:audit [--fix]` | 检查 AGENTS.md 行数、断链与锚点、ID 重复与悬空引用、剩余 TODO |
| `changelog-batcher` | 子代理（由 release 调用） | 把一批 commit 整理成台账行，输出覆盖计数 |
| 推送守卫 | 钩子（PreToolUse / Bash） | 在 sdd 仓库里执行 `git push` 前请求确认；force push 会单独标注 |

推送守卫只在当前目录或上级目录存在 `docs/development-workflow.md` 时生效，其他仓库不受影响。

## 生成的项目结构

```text
AGENTS.md                         # 全局约束 + 按需阅读路由（≤80 行）+ 强制完成门
CLAUDE.md                         # @AGENTS.md
docs/
├── README.md                     # 文档目录、阅读路线、文档约定（用语、范围标记、ID 体系、写作规则）
├── glossary.md                   # 术语表
├── repo-conventions.md           # 目录、放置、命名、文案
├── development-workflow.md       # 规范与实现、提交分类、验证矩阵、多端同步、语言与平台、工作区
├── release.md                    # 版本号所有者、CI、平台、读回检查
├── product/product-design.md     # 定位、界面、工作流 Snn、需求 XX-nn、发布路线
├── architecture/architecture-design.md  # 模块、状态所有权、决定 Dnn
├── spec/README.md                # 格式与协议规范索引
└── acceptance/acceptance-spec.md # 口径、测试策略、发布门槛、验收矩阵 AT-nn
designs/<app>/                    # 可选：原型 README + 局部协议
```

未填的位置用 `<!-- TODO(sdd): ... -->` 标记，`/sdd:audit` 会统计剩余数量。

## 插件目录

```text
sdd/
├── .claude-plugin/plugin.json
├── skills/{init,change,finish,release,acceptance,audit}/
├── agents/changelog-batcher.md
├── hooks/{hooks.json,guard-push.py}
├── scripts/{init.py,audit.py}
└── templates/
    ├── project/      # init 复制到仓库根
    ├── prototype/    # --prototype 时复制为 designs/<app>/
    └── extra/        # 按需使用：spec.md、acceptance-record.md、delivery-note.md
```

## 定制

- 模板是中文的。要改用其他语言，替换 `templates/` 下的文件；`audit.py` 的锚点规则与语言无关。
- 验证矩阵、发布平台等项目事实写在生成的 `docs/` 里，插件 skill 运行时读取，不需要修改插件。
- 根 AGENTS.md 的行数上限：`audit.py --max-agents-lines <n>`。
