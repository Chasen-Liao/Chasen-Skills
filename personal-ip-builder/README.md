# personal-ip-builder

从照片、角色/画风参考图或纯文字想法出发，打造可长期复用的**个人 IP 数字资产卡**，并默认打包为开箱即用的**三模式专属配图 Skill**。

<p>

![Category](https://img.shields.io/badge/Category-workflow-7c3aed?style=flat-square)
![Output](https://img.shields.io/badge/Output-数字资产卡_+_配图_skill-f59e0b?style=flat-square)
![Style](https://img.shields.io/badge/Style-多画风通用-0ea5e9?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-10b981?style=flat-square)
![Version](https://img.shields.io/badge/version-0.3.1-64748b?style=flat-square)

</p>

---

## 这是什么？

很多人做个人 IP 的第一反应是「帮我画一个好看的头像」，但单张头像只能解决一时，换个场景就走形。

本 Skill 帮你把个人特征或灵感收束成**单一视觉真源**（`master-立绘参考.png`），再由它派生三视图设定卡、设计契约、透明头像与 4～6 个无字可辨静态表情，最后自动打包成带内置 `assets/` 的 `<name>-ip-illustrations` 专属配图 Skill——开箱支持**解释型配图 / 信息图 / 封面**三种出图模式。

---

## 特性

| 能力 | 说明 |
| :--- | :--- |
| **三类输入全支持** | 照片转 IP、参考图借气质转原创 IP、无图纯文字从零设定 / 旧头像升级 |
| **多画风通用** | 不强绑单一画风；支持 Q 版手绘平涂（默认推荐）、日系赛璐璐、扁平矢量、像素、3D 盲盒/粘土、半写实等 |
| **零重复单真源** | Stage 3 锁定的 `master-立绘参考.png` 直接作为 Stage 4 唯一参考真源，去掉冗余规范卡 |
| **可执行 Prompt 骨架** | 内置 Stage 3 `master`、Stage 4 正/侧/背三视图（含 HEX 色条）及透明头像/表情 Prompt 骨架 |
| **Stage 5 三模式 Skill** | 基于 `illustration-skill-template.md` 打包专属配图 Skill，自带解释型/信息图/封面三模式与自查清单 |
| **跨工具与跨 Agent** | 兼容 `image_gen` / `GenerateImage`、Codex image、GPT-4o、Nano Banana、Midjourney、Flux Redux 等 |

---

## 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill personal-ip-builder --global --yes
```

前置：具备参考图输入能力的图像生成工具与本地看图工具；若当前环境无生图工具，将交付完整的 `character-contract.md`、Prompt 骨架与 Stage 5 Skill 模板。

---

## 怎么用

1. 准备好**个人照片**、**喜欢的角色/画风参考图**，或直接想好一句**角色定位**
2. 对 Agent 说：`用 personal-ip-builder 帮我做个人 IP 数字资产卡`
3. 每轮回答 3～5 个带推荐预设的问题，最多试 3 张候选并锁定 `master-立绘参考.png`
4. Agent 以 `master` 为真源产出设定卡、契约、透明头像与静态表情，并生成 `<name>-ip-illustrations/` 配图 Skill

也可触发：`/personal-ip-builder`、`打造个人IP`、`做角色设定卡`、`数字资产卡`、`character IP pack`。

---

## 工作流

```text
工作区检查 → 三选一输入（照片 / 参考图 / 纯文字） → 每轮 3～5 问定画风与记忆点
    → 最多 3 张候选锁定 master-立绘参考.png → 派生核心资产卡 → 打包三模式配图 Skill
```

| 阶段 | 做什么 | 核心产出 |
| :--- | :--- | :--- |
| 0 工作区 | 确认归档路径与参考图生图能力 | 路径与工具适配策略 |
| 1 输入解析 | 提炼真人保留项或参考图可借视觉语言 | 原创化边界清单 |
| 2 访谈定稿 | 每轮 3～5 问，用速选表定画风、比例与表情包 | 锁定需求（不展开封面清单） |
| 3 试定稿 | 最多 3 张干净单人物候选，用户拍板锁定 | `01-数字资产卡/master-立绘参考.png` |
| 4 核心资产 | 以 `master` 为真源派生三视图、契约与透明表情 | `角色设定卡.png`、`character-contract.md`、头像与表情 |
| 5 配图 Skill | 用模板打包内置 `assets/` 的专属配图 Skill | `<name>-ip-illustrations/`（三模式 + 自查） |

---

## 输出目录示例

```text
03-Assets/2026-11-12-my-ip-personal-ip/
├── character-contract.md
├── 01-数字资产卡/
│   ├── master-立绘参考.png           # Stage 3 锁定的唯一单人物真源
│   └── 角色设定卡.png                # 正/真90°侧/背三视图 + HEX 色条 + 配件标注
└── 02-头像与表情/
    ├── 头像-透明.png                 # 圆框安全裁切透明头像
    └── 表情-01～06-透明.png          # 4～6 个无字可辨静态透明表情

<name>-ip-illustrations/              # Stage 5 可直接分发安装的专属配图 Skill
├── SKILL.md                          # 三模式路由 + Character Lock + 合一自查
├── character-contract.md             # 从资产包复制
└── assets/
    ├── master-立绘参考.png
    ├── 角色设定卡.png
    ├── 头像-透明.png
    └── 表情-01～06-透明.png
```

修订不覆盖旧版，用 `-v2`、`-v3` 递增。

---

## 目录

```text
personal-ip-builder/
├── SKILL.md
├── README.md
└── references/
    ├── design-interview.md            # 第一轮 5 问、三类输入预设、画风速选表、赛道表情包
    ├── character-contract.md          # 通用角色契约与 Character Lock 模板
    └── illustration-skill-template.md # 阶段 5 三模式配图 Skill 仓库唯一母模板
```

---

## Changelog

- **0.3.1**：将 `asset-checklist.md` 独有验收项并入 `SKILL.md` 阶段 4 验收清单并删除冗余文件；合并 `SKILL.md` 重复禁令，将阶段 1–2 细则下沉 `design-interview.md`；标注 `illustration-skill-template.md` 为三模式配图 Skill 唯一母模板并对齐内置生图工具兼容表述。
- **0.3.0**：通用化升级（支持照片 / 参考图 / 无图纯文字三路径、多画风自由锁定、多生图工具与多 Agent 适配）；消除 `master` 与旧「视觉规范卡」重复产物，统一为 `master-立绘参考.png` + `角色设定卡.png`；补充 Stage 3/4 可执行 Prompt 骨架；重写 `design-interview.md` 预设包，并新增 `illustration-skill-template.md` 固化 Stage 5 三模式配图模板。
- **0.2.0**：聚焦数字资产卡真源；每轮 3～5 问、最多 3 张定稿；核心产出缩为设定卡/规范卡/契约/透明头像与静态表情；默认生成 assets 内置的专属配图 skill；开场不做封面/场景/GIF。
- **0.1.0**：从动漫参考图做整套数字资产（含场景/贴纸/主视觉），可选 repo-only 教程配图 skill。

---

## 边界

- 参考图与照片都不是一比一复刻模板
- 未锁定 `master-立绘参考.png`，不出核心资产卡
- 开场不直接批量做封面、背景图或场景图（交由 Stage 5 专属配图 Skill 按需派生）
- 本仓库只保留 Skill 模板与参考文档，个人生成图留在你自己的项目目录

---

## License

MIT © Chasen-Liao
