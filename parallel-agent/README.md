# 🔀 parallel-agent

> Pi 并行编排的**薄策略层** — `pi-subagents` 负责 API 与角色定义，本 Skill 负责「何时拆并行、如何防踩文件与越权」。

<p>

![Scope](https://img.shields.io/badge/Scope-Policy_Layer-7c3aed?style=flat-square)
![Depends](https://img.shields.io/badge/Depends-pi--subagents-0ea5e9?style=flat-square)
![Mode](https://img.shields.io/badge/Mode-Read--first_·_One_writer-f59e0b?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-64748b?style=flat-square)

</p>

---

## 这是做什么的？

给 Pi 主 Agent 提供一套简洁的本地调度边界：不重复官方 `pi-subagents` 文档，只在多子代理并行前把好四道关：

| 护栏 | 约束 |
| :--- | :--- |
| **真独立才拆** | 2+ 独立问题域、无共享可变状态才并行；耦合排查或同文件修改先找根因 |
| **父 Agent 兜底** | 编排、决策、`acceptedScope` 批准、验证与综合均归父 Agent；子代理不擅自扩 scope |
| **同区单 writer** | 同一 `repo/cwd` 同时只允许一个写入者；并发写必须做 `worktree` 隔离并记 lane board |
| **默认 `fresh` + 分层角色** | 独立 lane 默认 `fresh` 上下文，优先只读侦察/评审扇出，大报告走 artifact 不硬塞 prompt |

---

## 🚀 安装与触发

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill parallel-agent --global --yes
```

**前置**：仅用于 Pi 环境，且须已安装官方 `pi-subagents` Skill。当任务可安全拆为 2+ 独立子域时 Agent 自动触发，也可说「并行拆任务 / 多子代理并行」。

---

## 📋 并行拆解与 Handoff 示例

以**「多模块只读侦察 → 单 writer 修复」**（Staged implementation）为例：

```text
Stage 1（runs.all 并行只读，fresh 上下文）
  ├── lane-1 (scout): 分析 auth/ 鉴权边界（只读，不改文件）
  └── lane-2 (scout): 分析 billing/ 账单超时（只读，不改文件）
        ↓ 父 Agent 综合两份 handoff，批准 acceptedScope
Stage 2（runs.run 单 writer 实现）
  └── lane-3 (worker): 仅改 billing/retry.py，跑单测验证
```

子 Agent 返回的标准精简 Handoff：

```json
{
  "status": "done",
  "findings": ["billing/retry.py 缺少 429 指数退避，auth/ 无关"],
  "changedFiles": [],
  "validation": ["read-only check; inspected billing/retry.py L42-L88"],
  "remainingRisks": ["未实测生产网关并发限流阈值"]
}
```

---

## 📂 目录

```text
parallel-agent/
├── SKILL.md    # 给 Pi Agent 看的并行策略契约
└── README.md   # 本文件
```

---

## 📄 License

MIT © Chasen-Liao
