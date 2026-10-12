# dev-workflow

Claude Code 插件市场，收录 **sdd**：一个规格驱动开发（spec-driven development）插件，适用于编码代理。

它的核心做法：规格是唯一事实源；UI 先在原型里定稿；验证按改动影响选择范围并如实报告；每个任务以本地 commit 收尾；发布可以追溯、可以读回核对。方法论提炼自 [BaoCut](https://github.com/JimLiu/baocut) 的实际做法。

## 安装

```bash
claude plugin marketplace add cs11b137/dev-workflow
claude plugin install sdd@dev-workflow
```

依赖：`git`、`python3`；发布流程还需要 `gh`。

## 快速开始

1. 在目标仓库运行 `/sdd:init`。它会生成 `AGENTS.md`、`CLAUDE.md` 和 `docs/` 规格骨架，并按真实技术栈填好验证命令。
2. 补全产品设计：说「按 sdd 补全产品设计 §1、§9、§10」。
3. 之后正常提需求即可。新功能、UI 改动、修 bug、改协议、重构、改文档、规格冲突都会自动走对应流程，完成后自动验证、提交，并给出交付说明。

| 场景 | 你这样说 | 需要你确认的地方 |
| --- | --- | --- |
| 新功能 | 「加一个导出 CSV 的功能」 | 审阅规格后，才开始写代码 |
| 改 UI | 「把侧栏改成可折叠」 | 确认原型后，才改真实应用 |
| 修 bug | 「导出时中文文件名乱码」 | 看交付说明 |
| 发布 | 「发布 0.4.0」 | 确认版本号、tag、SHA 后，才推 tag |
| 文档体检 | `/sdd:audit` | 选择要修复的问题 |

## 目录

| 路径 | 内容 |
| --- | --- |
| [`sdd/`](sdd/README.md) | 插件：6 个 skill、1 个子代理、push 守卫钩子、初始化与审计脚本、项目模板 |
| [`ai-dev-workflow-methodology.md`](ai-dev-workflow-methodology.md) | 方法论全文与通用模板 |

## 许可

[MIT](LICENSE)
