# 🧰 Chasen-Skills

> Chasen 的个人 Agent Skills 集合 — 为 **Pi / Antigravity / Claude Code** 打造，开箱即用，按 Git 版本维护。

<p>

![Skills](https://img.shields.io/badge/Skills-3-7c3aed?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-10b981?style=flat-square)
![npx skills](https://img.shields.io/badge/npx-skills-black?style=flat-square&logo=npm)
![Maintained](https://img.shields.io/badge/Maintained-by_Chasen-0ea5e9?style=flat-square)

</p>

---

## ✨ 这是什么？

把高频、好用的 Agent 能力沉淀为 **可复用 Skill**，一个命令安装到全局，Agent 自动发现、按需调用。

- **不造轮子** — 薄封装 + 强编排，核心逻辑落在脚本与参考文档
- **可版本化** — Git 管理，`npx skills` 一键安装/更新
- **即插即用** — 符合 `SKILL.md` 标准，Pi / Antigravity / Claude Code 通用

---

## 📦 Skills 导航

| Skill | 一句话介绍 | 适合谁 | 文档 |
| :--- | :--- | :--- | :--- |
| **🔀 [parallel-agent](./parallel-agent/README.md)** | Pi 并行编排的**策略层**：判断何时拆并行、如何安全调度 `pi-subagents` | 写复杂 Agent 工作流时 | [→ README](./parallel-agent/README.md) |
| **📊 [x-analytics](./x-analytics/README.md)** | 丢一个 X Content Analytics CSV → 自动出 **深度复盘报告 + 6张图 + 手册对标建议** | 运营 X / 做内容复盘 | [→ README](./x-analytics/README.md) |
| **📡 [x-ai-radar](./x-ai-radar/README.md)** | 只读刷 X 时间线 → **10小时内 AI 热帖雷达**，按热度分排 Top 8-10 中文榜 | 想快速追 AI 热点 | [→ README](./x-ai-radar/README.md) |

> 💡 每个 Skill 目录下都有独立 `README.md`，介绍**做什么、怎么装、怎么用**；`SKILL.md` 是给 Agent 看的执行契约。

---

## 🚀 快速开始

### 安装任意 Skill 到全局

```bash
# 通用
npx skills add Chasen-Liao/Chasen-Skills --skill <skill-name> --global --yes

# 举例
npx skills add Chasen-Liao/Chasen-Skills --skill x-analytics --global --yes
npx skills add Chasen-Liao/Chasen-Skills --skill x-ai-radar --global --yes
npx skills add Chasen-Liao/Chasen-Skills --skill parallel-agent --global --yes
```

安装后，Pi / Antigravity 会在全局 skills 目录自动发现该 Skill，无需额外配置。

### 更新

```bash
npx skills update <skill-name> --global
# 或重新 add 覆盖
npx skills add Chasen-Liao/Chasen-Skills --skill x-analytics --global --yes
```

### 在 Agent 中触发

| Skill | 触发方式 |
| :--- | :--- |
| `x-analytics` | 对 Agent 说：`分析一下这个 CSV` / `/x-analytics <csv> --out ./x-reports` |
| `x-ai-radar` | `/x-ai-radar` 或自然语言 `刷一下 X AI 热榜` |
| `parallel-agent` | Agent 自主判断：当任务可拆为 2+ 独立子域时自动启用 |

---

## 🗂️ 目录结构

```text
Chasen-Skills/
├── README.md                    # ← 你在这里（总导航）
├── AGENTS.md                    # Agent 工作纪律（给 Agent 看）
├── MAINTENANCE.md               # 维护规则（新增/更新 skill checklist）
├── .gitignore
├── skills-lock.json             # npx skills 本地锁
│
├── parallel-agent/              # 并行编排策略层
│   ├── SKILL.md                 # Agent 执行契约
│   └── README.md                # 人读的介绍
│
├── x-analytics/                 # X 内容深度复盘
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/x-analyze.py     # 核心分析脚本
│   ├── references/              # 报告骨架 / 手册 / 词表
│   └── assets/
│
├── x-ai-radar/                  # 10h AI 热点雷达
│   ├── SKILL.md
│   ├── README.md
│   └── references/ai-keywords.json
│
└── docs/                        # 本地研究草稿（已 .gitignore，不入库）
```

---

## 🛠️ 本地开发

```bash
git clone https://github.com/Chasen-Liao/Chasen-Skills.git
cd Chasen-Skills

# 改完某个 skill 后，本地验证
npx skills add . --skill x-analytics --global --yes
```

> `docs/` 仅本地沉淀研究笔记，已加入 `.gitignore`，不会提交到远端。重点维护对象是 **根 README + 各 Skill README**。
> 维护见 [AGENTS.md](./AGENTS.md) 与 [MAINTENANCE.md](./MAINTENANCE.md)。

---

## 📄 License

MIT © Chasen-Liao
