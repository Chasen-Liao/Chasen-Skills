# personal-ip-builder

从照片或喜欢的角色参考图，做出可长期复用的**个人 IP 数字资产卡**，并默认打包成专属配图 Skill。

<p>

![Category](https://img.shields.io/badge/Category-workflow-7c3aed?style=flat-square)
![Output](https://img.shields.io/badge/Output-数字资产卡_+_配图_skill-f59e0b?style=flat-square)
![Style](https://img.shields.io/badge/Style-浅底_·_手绘线稿-0ea5e9?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-10b981?style=flat-square)
![Version](https://img.shields.io/badge/version-0.2.0-64748b?style=flat-square)

</p>

---

## 这是什么？

很多人做个人 IP 的第一反应是「帮我画一个好看的动漫头像」。头像只解决「我长什么样」。

本 Skill 的目标是把参考图或照片变成**可派生一切应用图的视觉真源**：定稿锁定后，产出角色设定卡、视觉规范卡、契约、透明头像与静态表情，并生成带内置 `assets/` 的专属配图 Skill。封面、背景图、场景图留在配图 Skill 里按需出，不在开场批量交齐。

---

## 特性

| 能力 | 说明 |
| :--- | :--- |
| **每轮 3～5 问** | 不再 11 轮一次一问；信息够了就停 |
| **最多 3 张定稿** | 用户锁定 master 后才出资产卡 |
| **核心资产卡** | 三视图设定卡 + 规范卡 + 契约 + 透明头像与 4～6 静态表情 |
| **配图 Skill** | 默认把参考图复制进 `<name>-ip-illustrations/assets/`，相对路径引用 |
| **GIF 外置** | 动态表情交给可选外部 GIF skill，本包不做 |

---

## 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill personal-ip-builder --global --yes
```

前置：当前环境能看参考图，并具备**带参考图输入**的图像生成（推荐 Codex image）。没有生图能力时，只交付契约与提示词。

---

## 怎么用

1. 准备一张照片或喜欢的角色图（只借气质与方向，不复刻原角色）
2. 对 Agent 说：`用 personal-ip-builder 帮我做个人 IP 数字资产卡`
3. 每轮回答 3～5 个打包问题，试最多 3 张定稿并锁定 master
4. Agent 按 master 出核心资产卡，并生成专属配图 Skill 文件夹

也可：`/personal-ip-builder`、`打造个人IP`、`做角色设定卡`、`数字资产卡`。

---

## 工作流

```text
读参考 → 每轮 3～5 问 → 最多 3 张定稿 → 锁定 master
    → 核心资产卡 → 专属配图 skill（assets/ 内置参考图）
```

| 阶段 | 做什么 |
| :--- | :--- |
| 0 工作区 | 素材路径、生图能力 |
| 1 参考图 | 提取可借视觉语言，标出必须原创化的部分 |
| 2 访谈 | 每轮 3～5 题，不问封面/场景制作清单 |
| 3 定稿 | 最多 3 张候选，锁定后才继续 |
| 4 资产卡 | 设定卡、规范卡、契约、头像、静态表情 |
| 5 配图 skill | 参考图进 `assets/`，不写死具体画幅比例 |

---

## 输出目录示例

```text
03-Assets/2026-11-09-my-ip-personal-ip/
├── character-contract.md
├── 01-数字资产卡/
│   ├── 角色设定卡.png
│   └── 视觉规范卡.png
└── 02-头像与表情/
    ├── 头像-透明.png
    └── 表情-01～06-透明.png

<name>-ip-illustrations/          # 默认可直接入库的配图 skill
├── SKILL.md
├── character-contract.md
└── assets/                       # 设定卡、规范卡、头像、表情
```

修订不覆盖旧版，用 `-v2`、`-v3`。

---

## 目录

```text
personal-ip-builder/
├── SKILL.md
├── README.md
└── references/
    ├── character-contract.md    # 契约模板
    ├── asset-checklist.md       # 核心资产验收
    └── design-interview.md      # 每轮 3～5 问问题包
```

---

## Changelog

- **0.2.0**：聚焦数字资产卡真源；每轮 3～5 问、最多 3 张定稿；核心产出缩为设定卡/规范卡/契约/透明头像与静态表情；默认生成 assets 内置的专属配图 skill；开场不做封面/场景/GIF。
- **0.1.0**：从动漫参考图做整套数字资产（含场景/贴纸/主视觉），可选 repo-only 教程配图 skill。

---

## 边界

- 参考图不是复刻模板
- 未锁定 master，不出资产卡
- 开场不制作封面、背景图、场景图
- 个人 PNG 留在你的项目目录；本仓库只放 skill 模板与参考文档

---

## License

MIT © Chasen-Liao
