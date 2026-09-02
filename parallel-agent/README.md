# 🔀 parallel-agent

> Pi 并行编排的**薄策略层** — 只决定「要不要拆、怎么拆才安全」，具体 API 以 `pi-subagents` 为准。

<p>

![Scope](https://img.shields.io/badge/Scope-Policy_Layer-7c3aed?style=flat-square)
![Depends](https://img.shields.io/badge/Depends-pi--subagents-0ea5e9?style=flat-square)
![Mode](https://img.shields.io/badge/Mode-Read--first_·_One_writer-f59e0b?style=flat-square)

</p>

---

## 这是做什么的？

`parallel-agent` **不是**执行引擎，而是给 Pi 主 Agent 的一套**本地调度纪律**：

- 什么时候该并行，什么时候不该
- 并行时如何保证**不踩文件、不丢结果、不越权**
- 如何用 `workflowScript + runs.all / runs.run` 与官方 `pi-subagents` 协作

> 一句话：`pi-subagents` 告诉你**怎么调 API**，`parallel-agent` 告诉你**什么时候调、怎么调才不翻车**。

---

## ✨ 核心规则

| 原则 | 说明 |
| :--- | :--- |
| **可拆才拆** | 仅当 2+ 任务域真正独立、无共享可变状态时才并行 |
| **父 Agent 负责** | 编排、综合、批准、验收都在父 Agent；子 Agent 只做被分配的事 |
| **默认只读** | 侦察/研究/评审并行 → 父 Agent 批准 `acceptedScope` → 单 writer 写入 → 再并行验证 |
| **单 writer** | 同一 `repo/cwd` 同时只能有一个写入者；并发写必须 `worktree` 隔离 |
| **上下文隔离** | 独立 lane 默认 `fresh`，仅继承决策咨询时用 `fork` |
| **批准才写** | 规划输出 ≠ 批准，worker 只能执行父 Agent 明确给的 scope |

---

## 🚀 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill parallel-agent --global --yes
```

安装后 Pi 会自动发现该 Skill。Agent 在合适时机自主启用，无需手动 `/parallel-agent`。

---

## 🧭 何时并行 / 何时不并行

**适合并行 ✅**

- 无关的多个 bug / 需求，改不同模块
- 独立子系统的侦察（scout）/ 外部研究（researcher）
- 多视角只读评审（reviewer）
- 本地上下文 + 外部研究的对比决策

**不要并行 ❌**

- 耦合调查、需串行依赖的链路
- 会改同一批文件的任务
- 共享可变状态、需先找到根因的场景 → 先搞清楚再拆

---

## 🔧 三种标准形态

```text
1. 只读扇出          scout/researcher/reviewer 并行 → 父 Agent 综合

2. 研究扇出          本地侦察 + 外部研究 并行 → 父 Agent 对比证据再决策

3. 分阶段实现        并行只读规划 → 父 Agent 定 acceptedScope → 单 writer 实现 → 并行只读验证
```

> 每种形态的子 Agent 都需返回精简 handoff：`status / findings / changedFiles / validation / remainingRisks`

---

## 📂 目录

```text
parallel-agent/
├── SKILL.md    # 给 Agent 看的执行契约（策略 + 路由）
└── README.md   # 给人看的介绍（本文件）
```

执行前 Agent 会：

1. 完整读取已安装的 `pi-subagents` Skill
2. 按任务路由到对应 reference（roles / execution-controls / orchestration）
3. `subagent({ action: "list" })` 确认可用 agents 后再调度

---

## 🔗 依赖

- **必需**：已安装 `pi-subagents`（Pi 官方子代理编排 Skill）
- 本 Skill 不复制其 API 文档，一切以 `pi-subagents` 为事实来源

---

## 📄 License

MIT © Chasen-Liao
