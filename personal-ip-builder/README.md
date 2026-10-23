# 🎨 personal-ip-builder

> 从一张喜欢的动漫参考图，打造**一整套**可长期复用的个人 IP 数字资产，并可选沉淀成教程配图 Skill。

<p>

![Category](https://img.shields.io/badge/Category-workflow-7c3aed?style=flat-square)
![Output](https://img.shields.io/badge/Output-IP_pack_+_optional_skill-f59e0b?style=flat-square)
![Style](https://img.shields.io/badge/Style-white_bg_·_ink_line-0ea5e9?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-10b981?style=flat-square)
![Version](https://img.shields.io/badge/version-0.1.0-64748b?style=flat-square)

</p>

---

## ✨ 这是什么？

很多人做个人 IP 的第一反应是：「帮我画一个好看的动漫头像。」

头像只解决「我长什么样」。这个 Skill 解决的是：**参考图只给情绪与方向，产出一套能反复调用的原创数字资产。**

| 问题 | 交付 |
| :--- | :--- |
| 我代表什么内容？ | 角色设计契约 `character-contract.md` |
| 观众第一眼记住什么？ | 固定配件 + 品牌符号 |
| 教程/文章里怎么行动？ | 表情动作 + 内容场景（角色必须在做事） |
| 换场景还能不能一致？ | 角色设定板 + 视觉规范板 |
| 以后能不能只给一句话出图？ | 可选：repo-only 教程配图 Skill |

方法来自 Chasen 的实操长文：[用 Codex 打造自媒体 IP 形象全流程](https://x.com/chasen_liao/status/2079467790252294636)。

---

## 📦 两层交付

| 层 | 你得到什么 | 何时停 |
| :--- | :--- | :--- |
| **第一层 · 数字资产** | 设定板、视觉规范板、头像、全身立绘、表情与动作、内容场景、贴纸、横版主视觉，外加 `character-contract.md` | 只要资产就可以停 |
| **第二层 · 教程配图 Skill** | 放在项目 `.agents/skills/` 的 repo-only skill，**引用**资产路径，不复制 PNG | 资产稳定，且你明确要求之后 |

---

## ✨ 特性

| 能力 | 说明 |
| :--- | :--- |
| **🎙️ 一次一问** | 优先 `grill-me`，每题给推荐答案和理由，先定位再外观 |
| **🖼️ 整套资产** | 设定板 → 规范板 → 头像 → 立绘 → 表情动作 → 场景 → 贴纸 → 横版主视觉 |
| **✏️ 白底线稿** | 纯白背景、深灰手绘线稿、清爽平涂；单图只讲一个核心意思 |
| **🎭 角色在做事** | 角色是动作主体，不站成证件照，也不把多场景拼成多格大图 |
| **🔧 定向修复** | 出问题只改一个变量，不全盘重抽 |
| **📚 教程配图** | 第二层 skill 引用契约与资产，避免 PNG 双份版本 |

---

## 🚀 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill personal-ip-builder --global --yes
```

推荐同时安装访谈技能（仅当前仓库，不要 `-g`）：

```bash
npx skills@latest add mattpocock/skills
# 交互只选 grill-me + 当前 Project
```

前置：当前环境能看参考图，并具备**带参考图输入**的图像生成。没有生图能力时，只交付契约和提示词。

---

## 🗣️ 怎么用

1. 准备一张你喜欢的参考图（只借情绪和方向，不复刻原角色）
2. 对 Agent 说：`用 personal-ip-builder 帮我从这张参考图打造个人 IP 数字资产`
3. 一次回答一个设计问题，确认「角色设计契约」
4. Agent 先出设定板，过关后再扩展整套资产并归档
5. 需要教程配图时再说：`基于这套资产创建教程配图 skill`

也可直接：`/personal-ip-builder`、`打造个人IP`、`从参考图做角色资产`。

---

## 🔄 工作流

```text
检查工作区 → 读参考图 → grill-me 设计访谈
    → 输出契约并等人确认
    → 先设定板，再扩展整套资产
    → 检查与定向修复
    → （可选）repo-only 教程配图 skill
```

| 阶段 | 做什么 |
| :--- | :--- |
| 0 工作区 | 看 skills 目录、素材路径、`grill-me`、生图能力 |
| 1 参考图 | 只提取情绪、比例、配色记忆、动作感 |
| 2 访谈 | 一次一问，临时契约跨轮不丢 |
| 3 契约 | 写清身份、外观、配件、色彩、动作；**确认前不生图** |
| 4 资产 | 设定板不过关，不批量头像/表情/贴纸 |
| 5 修复 | 每次只改一个主因 |
| 6 配图 skill | 引用 `character-contract.md` 与资产路径 |

---

## 📦 输出目录示例

```text
03-Assets/2026-10-23-my-ip-personal-ip/
├── character-contract.md
├── 01-角色设定/          # 设定板、视觉规范板、横版主视觉
├── 02-头像与立绘/
├── 03-表情与动作/        # 4–6 个状态
├── 04-内容场景/
└── 05-贴纸与装饰/
```

修订不覆盖旧版，用 `-v2`、`-v3`。个人 PNG 留在你的素材目录，不进入本 skill 仓库。

---

## 📂 目录

```text
personal-ip-builder/
├── SKILL.md                         # Agent 执行契约
├── README.md                        # 本文件
└── references/
    ├── asset-checklist.md           # 整套资产验收清单
    └── design-interview.md          # 设计访谈问题顺序
```

---

## 🚧 边界

- 参考图不是复刻模板：禁止照搬原角色的脸、服装、构图、Logo
- 契约未确认，不批量生图
- 单图单核心；白底、深灰线稿；角色必须在做事
- 第二层 skill 只引用资产，不复制 PNG，也不拷贝他人 IP 的案例构图

---

## 📄 License

MIT © Chasen-Liao
