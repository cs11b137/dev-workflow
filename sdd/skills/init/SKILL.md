---
name: init
description: 在当前仓库初始化 sdd 规格驱动工作流：生成 AGENTS.md、docs/ 规格骨架、可选原型协议，并按真实技术栈填好验证矩阵。
disable-model-invocation: true
argument-hint: "[项目名] [--prototype <app>]"
---

# 初始化 sdd

插件根目录 = 本 skill 目录的上两级。脚本：`<插件根>/scripts/init.py`、`<插件根>/scripts/audit.py`。

## 1. 摸清仓库

1. 运行 `git rev-parse --show-toplevel` 与 `git status --short`。把已有改动记为用户所有，后续只暂存本 skill 生成或修改的文件。
2. 读根 README、`package.json` / `Cargo.toml` / `pyproject.toml` / `Makefile` 等清单，确定：项目名、一句话定位、是否有用户界面、有哪些产品表面（桌面 / Web / CLI / API）。
3. 参数里给了项目名或 `--prototype` 就直接用。推断不出来的项合并成一次 AskUserQuestion：项目名、是否建立原型目录（以及 app 名）。

完成标准：项目名、原型与否、产品表面三项都已确定。

## 2. 生成骨架

```bash
python3 <插件根>/scripts/init.py --target <仓库根> --name "<项目名>" [--prototype <app>] --dry-run
```

先 dry-run 看清单。`SKIPPED` 的文件（常见：已有 `AGENTS.md`、`CLAUDE.md`、`docs/README.md`）不用 `--force` 覆盖，改走第 3 步合并。然后去掉 `--dry-run` 正式执行，保留输出里的 `STACK` 与 `DIR` 行。

## 3. 合并已有文件

对每个 `SKIPPED` 文件：读现有内容与对应模板（`<插件根>/templates/project/...`），把模板的结构合并进去，保留用户原有规则。

- `AGENTS.md`：补上「按需阅读」路由表与「强制完成门」两节；原有细则若超过 80 行的限制，搬到 `docs/` 中所属文档，根文件留一行触发条件加链接。
- `CLAUDE.md`：确保含有一行 `@AGENTS.md`；原有内容保留。
- 其他文档：按「一事一处」把内容整合进模板对应章节。

## 4. 按真实环境填空

只填能从仓库查到的事实，命令必须来自 `STACK` 行列出的真实入口（scripts、Makefile 目标、cargo、pytest……）。填完一处就删掉对应的 `<!-- TODO(sdd) ... -->` 注释。

| 文件 | 填什么 |
| --- | --- |
| `docs/development-workflow.md` §2 | 每种语言 / 模块一行检查命令（类型检查、格式检查、受影响测试、全量测试、构建） |
| `docs/development-workflow.md` §3 | 产品表面一行一个；没有原型时删掉「原型」行与原型先行一条，并写明本项目无原型 |
| `docs/repo-conventions.md` §1 | `DIR` 行的每个顶层目录一行，写清放什么 |
| `docs/release.md` | 版本号所有者文件、CI 工作流（`STACK ci` 行）、仓库 owner/repo |
| `docs/README.md` | 一句话定位 |
| `docs/product/product-design.md` §1 | README 里已有的定位、用户、非目标 |
| `designs/<app>/` | 能从现有前端代码确认的设计系统、组件库、预览命令 |

产品需求、架构决定、验收条目保留 TODO，它们要用户来定。

完成标准：§2 验证矩阵每行命令都能在清单文件里找到出处。

## 5. 审计并提交

1. 运行 `python3 <插件根>/scripts/audit.py --root <仓库根>`，修到没有 ERROR（TODO 数量只作信息）。
2. 审阅 `git diff`，只暂存本 skill 生成或修改的文件，复核 `git diff --cached`。
3. 提交：`docs(sdd): bootstrap spec-driven workflow docs`。

## 6. 报告

- 新建、合并、跳过的文件各列一行。
- 已填好的部分，以及剩余 TODO 数量（按文件）。
- 推荐的下一步：补产品设计 §1、§9、§10，可以说「按 sdd 写新功能规格」触发 `change` skill 的 feature 场景。
- commit hash。
