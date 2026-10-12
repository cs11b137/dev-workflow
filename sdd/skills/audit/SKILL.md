---
name: audit
description: 审计 sdd 文档健康度：根 AGENTS.md 行数、相对链接与锚点、需求/验收 ID 的重复与悬空引用、剩余 TODO(sdd)，并给出修复。
disable-model-invocation: true
argument-hint: "[--fix]"
---

# 文档审计

插件根目录 = 本 skill 目录的上两级。

1. 运行 `python3 <插件根>/scripts/audit.py --root <仓库根>`。
2. 按类别汇总结果，每类先列数量，再列前 5 条：
   - **ERROR 断链 / 缺锚点**：目标文件或标题不存在。
   - **ERROR ID 重复定义**：同一个 ID 出现在两张表的第一列。
   - **ERROR AGENTS.md 超长**。
   - **WARN 悬空引用**：引用了不存在的 ID。
   - **INFO TODO(sdd)**：按文件统计。
3. 每个问题给出修复建议：
   - 断链 → 找出目标改名或移动后的路径（`git log --follow --diff-filter=R`），或者删除这个引用；
   - 缺锚点 → 列出目标文件现有的标题，选出最接近的一个；
   - ID 重复 → 保留最早发布的定义，另一处改用新编号或改为引用；
   - AGENTS.md 超长 → 指出可以搬进 `docs/` 的段落和目标文档。
4. 参数带 `--fix` 时：只自动修复那些只有一种合理改法的问题（目标被改名、锚点只有一个候选）；其余列出来交给用户。修复后重跑审计，用 `finish` skill 提交（`docs(<scope>): fix doc links and ids`）。

完成标准：报告里的每个 ERROR 都有修复建议，或者已经修复；`--fix` 运行后 ERROR 数量不增加。
