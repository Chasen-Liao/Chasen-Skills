# chasen-x-writing

把 Chasen 的口播、碎片想法写成他本人会发的 𝕏 帖，**人味优先于爆款公式**

![Version](https://img.shields.io/badge/version-0.7.1-7c3aed?style=flat-square)
![Voice](https://img.shields.io/badge/人味-优先-f59e0b?style=flat-square)
![Draft](https://img.shields.io/badge/默认稿型-口播观点-0ea5e9?style=flat-square)

## 2026-11-10 (v0.7.1)

| 变化 | 说明 |
| :--- | :--- |
| **去重与单点原则** | 核心规矩只在 SKILL.md 核心铁律写一次，子文件一律引用条款编号；删 style_guide.md 第 8 节；align.md 第 6 步改为一行引用 plain-talk.md；第 12 节开头与读者价值挪入 structure-variety.md 第 B 节 |
| **合并自查清单** | deliver.md 三问与 structure-variety.md 反模板清单并入 SKILL.md「交稿前自查」，全仓库保留一套自查（共 12 条），其余文件只作引用 |
| **解决 4 处冲突** | emoji 不当编号并删推荐 1️⃣2️⃣3️⃣；统一情绪帖表情规范；干货长帖收尾改观点或行动号召不写总结腔；段落长短不齐注明是段落层面（句长不刻意制造）；设问可用但不用反问收尾 |
| **二次精简** | 删掉只剩跳转的小节（voice-and-craft 规则引用、structure-variety 表情与自查、deliver 里重复的代发和格式条），style_guide 与 structure-variety 重复的曝光统计只留一处 |

## 2026-11-10 (v0.7.0)

| 变化 | 说明 |
| :--- | :--- |
| 新增 plain-talk.md | 说人话 6 条（先场景后概念、术语用熟悉的东西解释、功能写成省了哪一步、用真实数字、教程每步写怎么算过、翻车照实写），例句都来自高曝光帖原文 |
| 去 AI 味改成看数据 | 按 @Zhiyu333 对 283 万字语料的对照统计，重点查空转冒号、拟人化比喻、段首没头没尾的评价句、提示语冒号、翻译腔；设问句人用得更多，不再当 AI 味删 |
| 教程长文骨架 | draft-types.md 新增，每一步写要做什么、现成 prompt、看到什么算过了，技术细节放附录 |
| 素材少先问再写 | align.md 新增：一次问一个问题，问 3～5 个再写，正文只写他说过的经历 |
| 自查清单 | SKILL.md 新增「看不看得懂」7 问，deliver.md 改为引用它；交付统一为一版一个代码块、长文发文件 |

## 2026-11-10 (v0.5.0)

| 变化 | 说明 |
| :--- | :--- |
| **清理过时机制** | 清理已下线的独立写帖助手配置、历史选题跟踪表、外部账号监控逻辑及旧版代发流程；发帖规则统一为：默认 Chasen 自己发，只有他说「你帮我发」才用 X 连接器 create_posts 原样代发；长文只存草稿 |
| **合并重复规则** | 各子文件与 references 之间说同一件事的合并保留单点，其余改为引用跳转，消除冗余表述 |
| **精简 SKILL.md** | 路由总入口大幅精简，只留一句定位、先对齐观点、核心铁律清单（每条一行）与场景路由表 |
| **整合修复记录** | 将 references/writing_skill_fix_2026-10-31.md 有效规则并入 draft-types、voice-and-craft 和 deliver，移除该记录文件；精简 style_guide.md 与 structure-variety.md |
| **排版与视觉规范** | 手机排版三条（短段多换行、正文不用句号「。」、不用「踩坑」）；emoji 只放首行末或高潮句且同一表情重复 3～5 次；生图只推荐 Codex image，封面比例 5:2 |

## 2026-11-05 (v0.4.0)

| 变化 | 说明 |
| :--- | :--- |
| **人味优先** | 读起来像跟群友说话，不像调研报告，也不像填空爆款模板 |
| **口播观点** | 新稿型；他口述判断，或讲完「好奇 → 以为 → 发现」时优先用，约 80～250 字、2～3 段口语 |
| **Chris 公式改为可选** | 8 型 / 硬钩子只在明确要冲浏览或收藏时再用；口播观点、随手判断默认不套 |

## 路由

`SKILL.md` 是总入口，按顺序读子文件，不要把所有风格挤进一个文档

| 文件 | 何时读 |
| :--- | :--- |
| `plain-talk.md` | 说人话、去 AI 味，改稿必读 |
| `align.md` | 开写前对齐观点；他说「随便写写」时，数据目标默认无冲量 |
| `draft-types.md` | 口播观点 / 分享帖 / 实测 / 快评 / X 长文；口播观点优先于硬拉分享长帖 |
| `traffic.md` | 浏览 / 收藏 / 回复 / 无冲量；8 型仅冲量帖选用 |
| `voice-and-craft.md` | 他的语气口癖、口播正反例、事实分层与语感样本指针，规则见 SKILL |
| `deliver.md` | 稿下标注、调研放稿外、配图时加载哪个 skill |
| `references/structure-variety.md` | 结构轮换 6 种形状、编号与表情细则 |
| `references/style_guide.md` | 风格指南、Chasen 真实高赞发帖样本与经典范例 |

账号运营习惯（热点连发、收藏夹拆解）不在本 skill

## 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill chasen-x-writing --global --yes
```

## 用法

丢一段口播、思路或草稿，并加载本 skill；Agent 先对齐「要传达哪一句」，确认稿型和是否冲量，再出正文

他已经用口语讲清观点时，篇幅跟着口播走，不扩成带百分比的调研长文；调研数字默认放稿外，除非他明确要写进正文
