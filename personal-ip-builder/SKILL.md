---
name: personal-ip-builder
description: 从照片、角色/画风参考图或纯文字需求，打造可长期复用的个人 IP 数字资产卡并打包为专属三模式配图 Skill。用户说 打造个人IP/做个人IP形象/从参考图做角色资产/做角色设定卡/数字资产卡/personal IP / character IP pack 或调用 /personal-ip-builder 时使用
license: MIT
compatibility: >-
  Prioritizes built-in image_gen / GenerateImage with reference-image input;
  supports user-configured reference-capable generators (Codex image, GPT-4o,
  Nano Banana, Midjourney --cref, Flux Redux) and requires a local image
  viewer. Falls back to character contract + executable prompts when no image
  generator is available.
metadata:
  author: Chasen-Liao
  version: "0.3.1"
  category: workflow
---

# Personal IP Builder — 打造个人 IP 数字资产卡

> 先锁定单一视觉真源（`master-立绘参考.png`），派生跨工具可复用的数字资产卡，再打包成专属三模式配图 Skill。

## 何时使用

- 用户想做原创个人 IP（手里有**真人照片**、**角色/画风参考图**，或**纯文字想法 / 旧头像升级**），需要一套长期一致的角色真源资产而非单张一次性头像
- 触发词：`打造个人 IP` / `做个人 IP 形象` / `做角色设定卡` / `做数字资产卡` / `personal IP` / `/personal-ip-builder`

## 核心原则与边界

1. **三类输入全支持，严禁复刻受保护原图**：照片只提取用户点名的真人特征并转译为目标画风；参考图只借气质、比例或配色，严禁照抄原角色五官、服装组合、构图与第三方 Logo。
2. **画风随用户锁定**：无偏好时推荐「浅底、深灰手绘线稿、清爽平涂（3～3.5 头身）」；一旦在阶段 2 选定画风，阶段 3～5 严格沿用，不强行改回默认画风。
3. **单真源门禁，不重复出图**：未经用户明确锁定 `01-数字资产卡/master-立绘参考.png`，不生成设定卡与批量表情；阶段 4 以 `master` 为唯一 `Image 1` 参考真源，不再生成功能重叠的「视觉规范卡」。
4. **范围边界**：开场不制作封面、背景图、日常配图、场景图或 GIF（全部留给阶段 5 专属配图 Skill 或外部 GIF skill 按需派生）。
5. **生图工具与沙箱兼容**：优先直接调用环境内置 `image_gen`（或 `GenerateImage`），不静默切换未授权外部 CLI/API；若工具要求参考图位于特定目录（如 Grok Bot 的 `/workspace` 或 `attachments`），先复制再传参；无可用生图能力时不假装已出图，只交付 `character-contract.md`、Prompt 骨架与阶段 5 Skill 模板。

## 阶段总览

检查工作区 → 读取输入（照片/参考图/纯文字） → 每轮 3～5 问定需求 → 最多试 3 张候选锁定 `master-立绘参考.png` → 派生核心资产卡 → 打包专属三模式配图 Skill

---

## 阶段 0：检查工作区与能力

1. 确认归档根路径：优先用户指定目录，否则默认 `03-Assets/YYYY-MM-DD-<主题>-personal-ip/`。
2. 检查当前环境是否具备支持**参考图输入**的生图工具及本地看图工具，按「核心原则 5」执行或降级。

## 阶段 1–2：读取输入与访谈定稿

按 [design-interview.md](references/design-interview.md) 完成需求对齐，遵循以下规则：

1. 先询问用户走**照片转 IP**、**参考图借气质**还是**无图从零设定 / 旧头像升级**，按对应路径提炼「保留特征」与「必须原创替换项」。
2. 每轮打包 **3～5 个带推荐选项的问题**，已确认项跨轮锁定不重复问；先对齐「第一轮优先对齐 5 件事」，信息够生成 `master` 即停（缺口时按「补漏追问清单」追问 1 轮），不把用途展开成封面/场景制作清单。

## 阶段 3：试定稿并锁定 `master`（最多 3 张）

在生成设定卡和表情前，先试出最多 3 张干净单人物全身（推荐）或稳定半身候选图：

- **硬约束**：正面或微侧自然站姿，纯白/纯浅单色或透明底，画面内**禁止**三视图拼版、色卡条、文字标签、装饰边框或场景道具堆砌；画风与头身比严格按阶段 2 执行。
- **迭代规则**：每次重绘只改一个主要问题；参考图输入始终回到**原始照片/参考图 + 已确认契约**，禁止拿上一张失败候选图套娃。3 张未过关时交付当前最佳版本并说明单一差距。
- **拍板锁定**：用户明确确认后，保存为 `01-数字资产卡/master-立绘参考.png`，并写入 `character-contract.md`。

### 阶段 3 Prompt 骨架（`master-立绘参考.png`）

按所选生图工具适配输入方式，直接套用以下骨架并替换 `{{...}}`：

```text
[Use Case] Character design master reference sheet (single character only).
[Input Reference] {{若无参考图删除此行；有图则写：Image 1: user reference (borrow mood/color vibe or listed personal traits ONLY; keep face, outfit, pose, and accessories 100% original)}}.
[Subject] Single {{角色性别/年龄感/身份}} character, full-body standing neutral-friendly front pose (slight natural weight shift), centered with generous margins.
[Visual Style] {{锁定画风，例如：clean dark-gray hand-drawn lineart with crisp flat cel shading / 3D blind-box vinyl toy render / crisp flat vector illustration}}, {{头身比，如：3.5-head chibi proportion}}, consistent line weight and texture.
[Fixed Traits]
- Hair: {{发型与发色}}
- Face & Eyes: {{五官特征与瞳色/高光}}
- Outfit: {{固定服装组合}}
- Signature Accessory & Symbol: {{识别配件与品牌符号位置}}
- Color Palette: primary {{主色 + HEX}}, secondary {{辅色 + HEX}}, accent {{点缀色 + HEX}}.
[Background & Ban] Plain solid pure white (or clean transparent) background. NO turnaround grid, NO color swatches, NO text labels, NO UI cards, NO extra characters, NO watermark, NO third-party logos.
```

## 阶段 4：以 `master` 为真源出核心资产

阶段 4 所有生图必须将 `01-数字资产卡/master-立绘参考.png` 作为 `Image 1` 传入（**严禁拿派生图接力生图**），仅交付以下 4 类产物：

1. `01-数字资产卡/角色设定卡.png`（1 张）
2. `character-contract.md`（1 份，模板见 [character-contract.md](references/character-contract.md)）
3. `02-头像与表情/头像-透明.png`（1 张）
4. `02-头像与表情/表情-01～06-透明.png`（4～6 张）

### 阶段 4 Prompt 骨架 1：`角色设定卡.png`（三视图 + HEX 色条 + 配件标注）

```text
[Use Case] Orthographic character turnaround sheet based strictly on Image 1 (master-立绘参考.png).
[Input Reference] Image 1: master-立绘参考.png — keep 100% identical character face, hairstyle, outfit, accessories, proportions, and rendering style as Image 1.
[Layout] Clean light/white studio sheet with three full-body orthographic views arranged side-by-side at equal height:
1) Left: Front view (facing straight forward, arms relaxed at sides).
2) Center: True 90-degree side profile view (strictly perpendicular side silhouette; NOT a 3/4 angle).
3) Right: Back view (strictly back of head, hair, and outfit ONLY — ZERO facial features, eyes, or nose visible on the back).
[Callouts & Palette]
- Bottom bar: clean horizontal color palette swatches showing exact colors from Image 1 with crisp HEX codes ({{主色HEX}}, {{辅色HEX}}, {{点缀色HEX}}, {{线稿/辅助HEX}}).
- Side/corner inset: clear zoomed detail callout of signature accessory / brand symbol ({{识别配件与符号名称}}).
[Ban] Maintain exact rendering style of Image 1. NO extra characters, NO decorative posters, NO watermark, NO distorted text.
```

### 阶段 4 Prompt 骨架 2：`头像-透明.png`（圆框友好透明头像）

```text
[Use Case] Clean character avatar icon based strictly on Image 1 (master-立绘参考.png).
[Input Reference] Image 1: master-立绘参考.png — lock exact face, hair, expression, outfit collar, signature accessory, and rendering style of Image 1.
[Composition] Head-and-shoulders close-up portrait centered inside a safe circular crop zone (leave 15% breathing margin around head and accessories so nothing gets clipped in a circle avatar). Face and {{识别配件/品牌符号}} clearly visible inside the central circle.
[Background & Output] Isolated character bust on a 100% transparent PNG background (no background card, no circle frame drawn onto the image, no drop-shadow box).
[Ban] NO text, NO extra props, NO watermark, NO style drift from Image 1.
```

### 阶段 4 Prompt 骨架 3：`表情-01～06-透明.png`（静态透明表情包，逐张或分批生成后独立切分保存）

```text
[Use Case] Static expressive character sticker based strictly on Image 1 (master-立绘参考.png).
[Input Reference] Image 1: master-立绘参考.png — keep exact character identity, hairstyle, outfit, accessories, and rendering style of Image 1.
[Expression & Pose] Chest-up / half-body dynamic pose showing clear, exaggerated {{目标情绪，如：shocked discovery / deep focus / hilarious fail / cheerful thumbs-up}} — distinct facial expression + readable hand gesture or simple emotion cue (e.g. sweat drop, sparkle, question mark) so the mood is immediately recognizable WITHOUT any text labels.
[Background & Output] Isolated single character on a 100% transparent PNG background, clean silhouette edges.
[Ban] NO text captions, NO speech-bubble paragraphs, NO extra characters, NO background rectangle, NO style drift from Image 1.
```

> 若当前生图工具无法直接输出真透明通道 PNG，生成纯白/绿幕单色背景后，用本地脚本或抠图工具去背并验证边缘干净，再存为透明 PNG。

### 归档目录与阶段 4 交付验收清单

保存至指定路径（默认 `03-Assets/YYYY-MM-DD-<主题>-personal-ip/`，修订用 `-v2`、`-v3` 递增不覆盖旧版），交付前逐项核对（未通过项必须以 `master-立绘参考.png` 为参考单点重做）：

- [ ] **真源干净无重复**：`01-数字资产卡/master-立绘参考.png` 为纯白/浅单色或透明底单人物、无边框/色卡/文字干扰，路径已写入 `character-contract.md`，未重复生成「视觉规范卡」。
- [ ] **画风与特征零漂移**：设定卡、头像、表情的线条、上色、材质、头身比、发型、服装、识别配件与品牌符号严格跟随 `master`，无受保护抄袭、额外角色、第三方 Logo 或水印。
- [ ] **设定卡结构与 HEX**：`01-数字资产卡/角色设定卡.png` 侧面为真 90° 正侧面（非 3/4）、背面无五官，色条 HEX 清晰且与 `character-contract.md` 一致。
- [ ] **头像圆框安全**：`02-头像与表情/头像-透明.png` 为真透明 PNG，放入圆形裁切后面部与核心识别配件完整不被切边（留有约 15% 安全边距）。
- [ ] **表情无字可辨**：4～6 张 `02-头像与表情/表情-01～06-透明.png` 均为独立透明 PNG，遮住文件名或无文字时情绪与动作依然清晰可辨、彼此区分度高。

---

## 阶段 5：生成专属三模式配图 Skill

核心资产验收通过后，在用户项目或指定目录生成可独立分发、即装即用的专属配图 Skill：

```text
<name>-ip-illustrations/
├── SKILL.md                 # 基于 references/illustration-skill-template.md 填充生成
├── character-contract.md    # 从阶段 4 资产包完整复制
└── assets/
    ├── master-立绘参考.png
    ├── 角色设定卡.png
    ├── 头像-透明.png
    └── 表情-01～06-透明.png
```

生成与验收规则：

1. **基于母模板生成**：读取 [illustration-skill-template.md](references/illustration-skill-template.md)（仓库三模式配图规则唯一母模板），替换占位符为本次 `character-contract.md` 锁定的角色名、画风规则、HEX 色表、`Character Lock` 段落与 `assets/` 相对路径。
2. **完整保留契约**：生成的 `SKILL.md` 必须完整保留「解释型配图（默认）/ 信息图模式 / 封面模式」三条路由、动态画幅策略（不写死比例或像素）与合一交稿前自查清单；`assets/` 已拷入全部参考图且使用相对路径引用。
3. **版本同步提示**：告知用户日后角色资产改版时，需同步替换 `assets/` 与 `character-contract.md` 并在 `SKILL.md` 递增版本号。

## 动态表情与最终交付物

- **动态表情（可选扩展）**：若用户需要 GIF 或动态表情，引导其将已锁定的 `master-立绘参考.png`、`角色设定卡.png` 与静态透明表情包交给外部 GIF / 动效 skill 处理。
- **最终交付物**：① `character-contract.md`；② `01-数字资产卡/`（`master-立绘参考.png`、`角色设定卡.png`）；③ `02-头像与表情/`（`头像-透明.png` + 4～6 张表情）；④ `<name>-ip-illustrations/` 专属配图 Skill；⑤ 简短验收说明（补全了哪些部位、哪些细节需用户审美终审；无生图工具时如实说明仅交付契约与可执行 Prompt）。

## References

- [references/design-interview.md](references/design-interview.md) — 第一轮 5 问、三类输入路径预设、画风与头身比速选表、赛道表情推荐包、补漏清单
- [references/character-contract.md](references/character-contract.md) — 通用角色设计契约与 `Character Lock` 模板
- [references/illustration-skill-template.md](references/illustration-skill-template.md) — 阶段 5 专属三模式配图 Skill 仓库唯一母模板
