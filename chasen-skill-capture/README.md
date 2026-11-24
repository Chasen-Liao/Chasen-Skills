# 📝 chasen-skill-capture

> **Chasen 团队技能沉淀与仓库同步规矩** — 可复用的多步流程当场用 `UpdateSkill` 沉淀为共享 Skill，并按仓库规范开 PR 同步至 `Chasen-Liao/Chasen-Skills`；未同步不谎称已完成，不把 `git push` 交给 Pi。

<p>

![Scope](https://img.shields.io/badge/Scope-Skill_Capture-7c3aed?style=flat-square)
![Sync](https://img.shields.io/badge/Sync-GitHub_PR-0ea5e9?style=flat-square)
![Version](https://img.shields.io/badge/version-0.1.0-10b981?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-64748b?style=flat-square)

</p>

---

## ✨ 核心规则

| 维度 | 规范 |
| :--- | :--- |
| **⚡ 当场沉淀** | 教完或做完可复用、多步骤工作，或用户要求「记住 / 写成 skill」、同类活第二次出现时当场沉淀 |
| **🧩 通用与专属分离** | `UpdateSkill` 写通用步骤（`kebab-case` 命名 + 清晰触发 `description`）；频道、仓库等助手专属细节放 routine / 记忆 |
| **🔁 仓库同步 via PR** | 每次新增或更新后同步到 `Chasen-Liao/Chasen-Skills`（升 `metadata.version`、同步 `SKILL.md` + `README.md` 与必要导航、开 PR 等人工合并） |
| **🛡️ 诚实与安全边界** | 遵守平台仓库执行与审批边界，**不把 `git push` 交给 Pi**；尚未完成同步时如实标记「待同步」，PR 建立后才附真实链接 |
| **🚫 不沉淀范围** | 一次性问答、纯事实备忘（走 memory）、商单 brief、密钥与私信内容 |
| **🥚 新建 Bot 原则** | 新建 Bot 先找现行 Eggbot（`4e21ed98-bde7-45d4-afb7-34cce27814d5`）设计，少而精、单一职责；能改现有描述就不新建 |

---

## 🚀 安装与前置

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill chasen-skill-capture --global --yes
```

**前置条件**：Bot 具备共享技能写入能力（如 `UpdateSkill`）以及合规的 GitHub PR 同步路径；所有仓库提交与推送遵守平台安全与审批边界。

---

## 🗣️ 怎么用

以下场景自动触发，或直接对 Bot 说：

> `记住这个流程` / `把这个写成 skill` / `按 chasen-skill-capture 沉淀`

| 阶段 | 动作 |
| :--- | :--- |
| **1. 判边界** | 确认是可复用多步流程，而非一次性问答、纯事实备忘、商单 brief、密钥或私信 |
| **2. 写共享 Skill** | 用 `UpdateSkill` 写入通用步骤与触发语，剥离单助手专属细节 |
| **3. 同步技能仓** | 按 `AGENTS.md` / `MAINTENANCE.md` 更新 `SKILL.md`、`README.md`、版本与导航并开 PR（不把 `push` 交 Pi） |
| **4. 诚实汇报** | 用 `[name](sand-workflow:<id>)` 提及已沉淀技能；PR 已建则附实际链接，未同步则明确标注「待同步」 |

---

## 📋 输出示例

已完成仓库同步并开 PR 时：

```text
已将复盘流程沉淀为共享技能 [weekly-review](sand-workflow:example-id)，并已同步至 Chasen-Skills 仓库：
- 同步内容：新增 weekly-review/SKILL.md（v0.1.0）、README.md 及根导航入口。
- 审阅链接：https://github.com/Chasen-Liao/Chasen-Skills/pull/99（待合并）
```

若当前环境尚未完成仓库同步，则如实说明（不谎称已同步）：

```text
已将复盘流程沉淀为共享技能 [weekly-review](sand-workflow:example-id)。
- 仓库同步状态：待同步（当前未向 GitHub 提交 PR，后续按 Chasen-Skills 规范补提 PR）。
```

---

## 📂 目录

```text
chasen-skill-capture/
├── SKILL.md    # Agent 执行契约（沉淀、仓库同步与新建 Bot 规矩）
└── README.md   # 本文件
```

---

## 📄 License

MIT © Chasen-Liao
