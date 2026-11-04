# chasen-x-writing

把 Chasen 的口播、碎片想法写成他本人会发的 𝕏 帖。**人味优先于爆款公式。**

![Version](https://img.shields.io/badge/version-0.4.0-7c3aed?style=flat-square)
![Voice](https://img.shields.io/badge/人味-优先-f59e0b?style=flat-square)
![Draft](https://img.shields.io/badge/默认稿型-口播观点-0ea5e9?style=flat-square)

## 2026-11-05

| 变化 | 说明 |
| :--- | :--- |
| **人味优先** | 读起来像跟群友说话，不像调研报告，也不像填空爆款模板 |
| **口播观点** | 新稿型。他口述判断，或讲完「好奇 → 以为 → 发现」时优先用，约 80～250 字、2～3 段口语 |
| **Chris 公式改为可选** | 8 型 / 硬钩子只在明确要冲浏览或收藏时再用；口播观点、随手判断默认不套 |

## 路由

`SKILL.md` 是总入口。按顺序读子文件，不要把所有风格挤进一个文档。

| 文件 | 何时读 |
| :--- | :--- |
| `align.md` | 开写前对齐观点。他说「随便写写」时，数据目标默认无冲量 |
| `draft-types.md` | 口播观点 / 分享 / 实测 / 快评 / 长文。口播观点优先于硬拉分享长帖 |
| `traffic.md` | 浏览 / 收藏 / 回复 / 无冲量。8 型仅冲量帖选用 |
| `voice-and-craft.md` | 声音、口播正反例、去 AI 味、短叙事硬卡 |
| `deliver.md` | 交稿三问。标注是否套爆款型，多数口播写「未套」 |
| `references/` | 语感样本。口播观点以 `voice-and-craft.md` 正例为准，不硬套分享长帖骨架 |

账号运营习惯（热点连发、收藏夹拆解）不在本 skill。

## 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill chasen-x-writing --global --yes
```

## 用法

丢一段口播、思路或草稿，并加载本 skill。Agent 先对齐「要传达哪一句」，确认稿型和是否冲量，再出正文。

他已经用口语讲清观点时，篇幅跟着口播走，不扩成带百分比的调研长文。调研数字默认放稿外，除非他明确要写进正文。
