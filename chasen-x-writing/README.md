# ✍️ chasen-x-writing

> 把 Chasen 的口播、碎片想法与实操过程写成他本人会发的 **𝕏 帖 / 长文** — **说人话、去 AI 味、人味优先于爆款公式**。

<p>

![Version](https://img.shields.io/badge/Version-0.8.0-7c3aed?style=flat-square)
![Voice](https://img.shields.io/badge/Voice-人味优先-f59e0b?style=flat-square)
![Draft](https://img.shields.io/badge/Default-口播观点-0ea5e9?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-10b981?style=flat-square)

</p>

---

## ✨ 能做什么

| 能力 | 说明 |
| :--- | :--- |
| **🎯 先对齐观点** | 出稿前先确认「最想让读者带走哪一句」与数据目标，素材少时先问 3～5 个问题再写 |
| **🗣️ 说人话去 AI 味** | 具象场景先于概念，基于对照语料剔除空转冒号、提示语冒号、拟人比喻与报告腔 |
| **🎙️ 口播观点优先** | 默认保持 80～250 字口语节奏，不擅自拉长成带百分比墙的调研报告 |
| **📐 多稿型与结构轮换** | 覆盖口播观点 / 分享 / 实测 / 快评 / 教程长文，6 种结构形状轮换避免模板化 |
| **🚀 按需冲量加权** | 仅在明确要冲浏览或收藏时启用 Chris 8 型，不为了套公式牺牲人味 |
| **🔗 联动配图与代发** | 默认仅产出文稿；需配图/封面时路由 `chasen-ip-tutorial-illustrations`，明确授权才代发 |

---

## 🚀 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill chasen-x-writing --global --yes
```

可选联动：

- 配图或封面：搭配 [`chasen-ip-tutorial-illustrations`](../chasen-ip-tutorial-illustrations/README.md)（封面默认建议 `5:2`）
- 热点选题 / 数据复盘：配合 [`x-ai-radar`](../x-ai-radar/README.md) 抓热点、[`x-analytics`](../x-analytics/README.md) 做发帖后复盘

---

## 🗣️ 怎么用

把口播语音转文字、碎片想法、实操笔记或草稿直接丢给 Agent：

> `把这段口播写成帖` / `按我的口吻改这篇草稿` / `帮我写篇教程长文` / `$chasen-x-writing`

Agent 会按以下顺序工作：

1. **对齐**：确认核心观点、稿型与是否需要冲量
2. **成稿**：按需加载 `references/` 中的口吻、说人话与结构规则出稿
3. **自查交付**：过完自查清单后，用代码块输出正文并在稿外附策略标注

---

## 📦 输出示例

交付时**正文放独立代码块**（方便手机/网页直接复制），策略标注与调研材料放代码块外：

````markdown
```text
好久没在推上看到有人聊 LangChain 了，这玩意25年年初到 Codex 问世之前都属于是 Agent 框架里的大哥大了

Codex 火起来了之后感觉这玩意就一夜销声匿迹了一样，想到这里的时候，我还觉得可能现在很多企业会用，但去查了一波才知道，大家现在都是用 SDK，或者说是 Pi 这类比较轻量级的 Agent 框架
```

- **本稿观点**：Agent 生态正从重型框架转向原生 SDK 与轻量 Harness
- **数据目标**：无冲量（自然观点表达）
- **稿型 / 爆款型**：口播观点 / 未套
- **建议发帖时段**：工作日 10:00–11:00 或 21:00–23:00 CST
````

---

## 📂 目录

```text
chasen-x-writing/
├── SKILL.md                          # Agent 总入口（对齐流程、核心铁律、自查与交付）
├── README.md                         # 本文件
└── references/
    ├── plain-talk.md                 # 说人话 6 条 + 数据化去 AI 味对照表
    ├── draft-types.md                # 5 种稿型与教程长文骨架
    ├── traffic.md                    # 流量目标、三要素与 Chris 8 型（仅冲量选用）
    ├── voice-and-craft.md            # Chasen 语气口癖、正反例与事实分层
    ├── structure-variety.md          # 6 种结构形状轮换与编号细则
    └── style_guide.md                # 风格画像、发帖时段分布与高赞历史样本
```

---

## 📄 License

MIT © Chasen-Liao
