# ✍️ Chasen 𝕏 写作

把 Chasen 的口播、碎片思路或实操经历，写成像他本人写的 𝕏 帖子 / 长文。角度由他自己的话决定，链接只提供材料。开写前先对齐**这一条要传达的一个观点**，没对齐不交正文。

![Version](https://img.shields.io/badge/version-0.2.0-7c3aed?style=flat-square)
![Lang](https://img.shields.io/badge/中文写作-𝕏-0ea5e9?style=flat-square)
![Style](https://img.shields.io/badge/风格指南-内置-10b981?style=flat-square)

## 能做什么

| 特性 | 说明 |
| :--- | :--- |
| 观点对齐 | 写正文前先聊清「这一条要传达什么」，他确认后再出稿 |
| 口吻还原 | 按 `references/style_guide.md` 对齐语感与爆款样本 |
| 稿型分流 | 分享帖（默认）/ 实测 / 快评 / X 长文 |
| 流量层 | 数据目标三选一：浏览、收藏、回复；再从 8 种爆款帖型里选一个，服务已对齐的观点 |
| 通顺优先 | 讲透一个点，不硬塞情绪、不编测试数字 |
| 配图挂钩 | 需要图时走 `chasen-ip-tutorial-illustrations` |

## 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill chasen-x-writing --global --yes
```

## 用法

Agent 会先用几轮短对话对齐：要传达的那一句判断、数据目标（浏览 / 收藏 / 回复）、稿型和读者读完能拿走什么。对齐后再出稿。观点已经用一句话说清，并且明确说「按这个写 / 直接出稿」时，可以跳过长讨论。

```text
用 $chasen-x-writing 把下面这段口播写成一篇分享帖。先跟我对齐这一条要传达的观点。
```

也可以直接说：

- 我刚发现一个工具，帮我写成 𝕏 帖。
- 改一下这篇草稿，语气像我平时发的。
- 按实测帖写，我跑过这些步骤……
- 观点已经定了，按这个写，直接出稿。

## 目录

```text
chasen-x-writing/
├── SKILL.md
├── README.md
└── references/
    ├── style_guide.md
    ├── structure-variety.md
    └── writing_skill_fix_2026-10-31.md
```

## 边界

- 不替他发帖、回复、点赞或私信（除非他在当次对话明确说「你帮我发」）。
- 产品拆解长文栏目正文由他自己写，本 skill 不代写栏目正文。
- 分享帖不写「我实测」类编造。
