# `parallel-agent` 瘦身研究

## 结论

可以明显拆薄。当前 `parallel-agent/SKILL.md` 约 226 行，其中大量内容重复已安装的 `pi-subagents` skill 和 references。建议将它改成 **本地调度策略层**，不再复制 API 文档和完整 `workflowScript` 示例。

## 应保留

1. **触发条件**：只有存在两个以上真正独立的任务域时才并行。
2. **父 Agent 责任**：父 Agent 编排、综合结果、批准修改并最终验收。
3. **写入安全**：默认只读并行；同一 `repo/cwd` 只能有一个 writer；并发写入必须 worktree 隔离。
4. **批准边界**：规划结果不是批准；worker 只能执行父 Agent 明确给出的 accepted scope。
5. **上下文边界**：独立 lane 默认 fresh；跨仓库任务明确 repository 和 cwd；普通子 agent 不再嵌套派发。
6. **最小角色提示**：`scout` 做本地侦察，`researcher` 做外部研究，`reviewer` 做只读评审，`worker` 做已批准实现，`oracle` 做继承决策咨询。
7. **文档路由**：执行前读取已安装的 `pi-subagents` skill，并按任务读取对应 reference；它是 API、参数和执行控制的唯一事实来源。

## 可以删除或改成引用

- 完整 builtin agent 表：`pi-subagents` 已维护。
- `workflowScript`、`runs.all`、`runs.run` 的长代码示例：执行 API 已在 `pi-subagents` 文档中定义。
- fork 的详细语义、async 行为、artifact、outputMode、acceptance、gate：直接引用 `execution-controls.md` 和 `constraints-and-recipes.md`。
- 详细 child prompt contract：保留一句“使用角色化、最小、自包含的任务契约”，其余由 `prompting-and-roles.md` 负责。
- 三套完整工作流代码：压缩成三行模式说明：并行只读分析、分析→父级批准→单 writer→验证、scout + researcher。

## 推荐目标结构

目标约 60–90 行、3–4 KB：

```text
frontmatter
本地职责与 pi-subagents 文档路由
何时并行 / 何时不并行
本地不可违反的 6 条策略
最小角色路由
三种工作流的文字版
失败、验收与停止规则
```

## 主要依据

- `C:\Users\Chasen\Desktop\Chasen-Skills\parallel-agent\SKILL.md`：当前本地实现，226 行。
- `C:\Users\Chasen\.pi\agent\npm\node_modules\pi-subagents\skills\pi-subagents\SKILL.md`：父 Agent 编排职责、角色、workflowScript 和安全边界。
- `...\pi-subagents\skills\pi-subagents\references\prompting-and-roles.md`：角色路由、prompt contract、review/research/staged-fix 模式。
- `...\pi-subagents\skills\pi-subagents\references\execution-controls.md`：`runs.run`、`runs.all`、fresh/fork、async、cwd、worktree 和输出控制。
- `...\pi-subagents\skills\pi-subagents\references\multi-lane-orchestration.md`：lane、repo/cwd、单 writer、worktree 隔离和父级验收。
- `...\pi-subagents\skills\pi-subagents\references\constraints-and-recipes.md`：父级权威、并行只读、实现与验证流程。

## 风险

过度瘦身会让 Agent 不知道何时使用哪个角色，或忘记“父级批准后才能写入”。这两类本地策略不能删除；应删除的是 API 解释和长示例，而不是安全不变量。
