# 🧰 Chasen-Skills

> Chasen 的个人 Agent Skills 集合 — 为 **Pi / Antigravity / Claude Code** 打造，开箱即用，按 Git 版本维护。

<p>

![Skills](https://img.shields.io/badge/Skills-9-7c3aed?style=flat-square)
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
| **🎨 [personal-ip-builder](./personal-ip-builder/README.md)** | 照片或参考图 → **锁定定稿后出数字资产卡**，默认打包专属配图 skill | 做个人 IP 真源 / 配图 skill | [→ README](./personal-ip-builder/README.md) |
| **✍️ [chasen-x-writing](./chasen-x-writing/README.md)** | 把口播/思路写成 **Chasen 口吻的 𝕏 帖**；先说人话、读者一遍看懂，去 AI 味有数据支撑；口播观点默认不套爆款公式 | 写 𝕏 / 改稿 | [→ README](./chasen-x-writing/README.md) |
| **🖌️ [chasen-ip-tutorial-illustrations](./chasen-ip-tutorial-illustrations/README.md)** | 内置 Chasen 角色素材，**教程 / 信息图 / 封面** 三种模式；画幅由出图时指定 | 教程作者 / AI Builder | [→ README](./chasen-ip-tutorial-illustrations/README.md) |
| **🚦 [cli-dispatch](./cli-dispatch/README.md)** | Bot 只拆任务与验收，**重活直接派给本机 `pi -p`**，后台跑、自动唤醒、Bot 验收 | 省 Bot 额度 / 共用电脑执行 | [→ README](./cli-dispatch/README.md) |
| **🔧 [grokbot-pi-setup](./grokbot-pi-setup/README.md)** | 教 Grok Bot **装 Pi + 用 Magpie 接自己的订阅 + 配跑完自动唤醒**，端到端验收 | 第一次让 Bot 派活给 Pi | [→ README](./grokbot-pi-setup/README.md) |
| **🚚 [grokbot-pi-dispatch](./grokbot-pi-dispatch/README.md)** | 通用派活法：**任务书五件事 → `pi -p` 后台跑 → webhook 叫醒 → Bot 验收** | 已配好 Pi 的任何 Grok Bot | [→ README](./grokbot-pi-dispatch/README.md) |

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
npx skills add Chasen-Liao/Chasen-Skills --skill personal-ip-builder --global --yes
npx skills add Chasen-Liao/Chasen-Skills --skill chasen-x-writing --global --yes
npx skills add Chasen-Liao/Chasen-Skills --skill chasen-ip-tutorial-illustrations --global --yes
npx skills add Chasen-Liao/Chasen-Skills --skill cli-dispatch --global --yes
npx skills add Chasen-Liao/Chasen-Skills --skill grokbot-pi-setup --global --yes
npx skills add Chasen-Liao/Chasen-Skills --skill grokbot-pi-dispatch --global --yes
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
| `personal-ip-builder` | `打造个人IP` / `做角色设定卡` / `数字资产卡` / `/personal-ip-builder` |
| `chasen-x-writing` | `把这段口播写成帖` / `按我的口吻改这篇` / `$chasen-x-writing` |
| `chasen-ip-tutorial-illustrations` | `用 Chasen 解释这个工作流` / `信息图` / `做封面` / `$chasen-ip-tutorial-illustrations` |
| `cli-dispatch` | `派给 Pi` / `按 cli-dispatch 写任务书` / `用 pi -p 派活` |
| `grokbot-pi-setup` | `帮我配好 Pi 派活` / `按 grokbot-pi-setup 装一下` |
| `grokbot-pi-dispatch` | 超过两三步的执行活自动读 / `派给 Pi` |

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
├── personal-ip-builder/         # 个人 IP 数字资产卡 + 默认专属配图 skill
│   ├── SKILL.md
│   ├── README.md
│   └── references/              # 契约模板 / 验收清单 / 访谈问题包
│
├── chasen-x-writing/            # 𝕏 写稿：人味优先，口播观点默认不套公式
│   ├── SKILL.md
│   ├── README.md
│   ├── align.md / draft-types.md / traffic.md
│   ├── voice-and-craft.md / deliver.md
│   └── references/
│
├── chasen-ip-tutorial-illustrations/ # Chasen IP 教程配图，内置角色参考素材
│   ├── SKILL.md
│   ├── README.md
│   ├── agents/openai.yaml
│   └── assets/chasen-ip/
│
├── cli-dispatch/                # Bot 用 pi -p 派活给本机 Pi
│   ├── SKILL.md
│   ├── README.md
│   └── templates/TASK_TEMPLATE.md
│
├── grokbot-pi-setup/            # 教 Grok Bot 装 Pi + Magpie + 唤醒
│   ├── SKILL.md
│   └── README.md
│
├── grokbot-pi-dispatch/         # 通用派活：写任务 → pi -p → 唤醒 → 验收
│   ├── SKILL.md
│   └── README.md
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
