---
name: personal-ip-builder
description: 从照片、角色/画风参考图或纯文字需求，打造可长期复用的个人 IP 数字资产卡并打包为专属三模式配图 Skill。用户说 打造个人IP/做个人IP形象/从参考图做角色资产/做角色设定卡/数字资产卡/personal IP / character IP pack 或调用 /personal-ip-builder 时使用
license: MIT
compatibility: Compatible with any reference-capable image generator (built-in image_gen / GenerateImage, Codex image, GPT-4o, Nano Banana, Midjourney --cref, Flux Redux, etc.) and local image viewer. Falls back to character contract + executable prompts when no image generator is available.
metadata:
  author: Chasen-Liao
  version: "0.3.0"
  category: workflow
---

# Personal IP Builder — 打造个人 IP 数字资产卡

> 目标不是一次交齐封面、背景图和场景图，而是先锁定单一视觉真源（`master-立绘参考.png`），派生一套跨工具可复用的数字资产卡，并打包成专属三模式配图 Skill。

## 何时使用

- 用户想做原创个人 IP：无论手里有**真人照片**、**喜欢的角色/画风参考图**，还是**只有文字想法 / 想升级旧头像**
- 需要一套长期一致的角色真源资产，而不是单张一次性头像
- 用户说「打造个人 IP」「做个人 IP 形象」「做角色设定卡」「做数字资产卡」「personal IP」或调用 `/personal-ip-builder`

## 核心原则

1. **三类输入全支持，绝不复刻受保护原图。**
   - 照片路径：只提取用户点名的真人特征（发型、眼镜、常戴配饰等），转译为目标画风。
   - 参考图路径：只借情绪、比例、配色或笔触气质，严禁照抄原角色的脸部细节、服装组合、构图与 Logo。
   - 无图 / 旧头像升级路径：优先询问是否有照片或参考图；若用户希望从零纯文字设计，直接按文字访谈启动。
2. **画风随用户锁定，不强绑单一画风。** 只有当用户没有画风偏好时，才推荐「浅底、深灰手绘线稿、清爽平涂」作为默认起手；一旦用户在阶段 2 选定画风（如日系赛璐璐、Q版手绘平涂、扁平矢量、像素风、3D 盲盒/粘土、半写实等），阶段 3～5 全部严格沿用该锁定画风。
3. **单真源不重复出图。** 阶段 3 锁定的干净单人物参考图直接归档为 `01-数字资产卡/master-立绘参考.png`；阶段 4 以它为唯一参考真源生成设定卡、头像与表情，不再重复生成一张功能重叠的「视觉规范卡」。
4. **先锁定 master，再出核心资产。** 未经用户明确锁定 `master-立绘参考.png`，不生成设定卡与批量表情；开场不做封面、背景图、场景图与 GIF。
5. **跨工具与跨 Agent 兼容。** 兼容 `image_gen` / `GenerateImage`、Codex image、GPT-4o、Nano Banana、Midjourney（`--cref`）、Flux Redux 等；适配 Pi、Antigravity、Claude Code、Cursor、Grok Bot。若当前生图工具要求参考图位于特定目录（如 Grok Bot 的 `/workspace` 或 `attachments`），先复制再传参。

## 阶段总览

检查工作区 → 读取输入（照片/参考图/纯文字） → 每轮 3～5 问定需求 → 最多试 3 张候选锁定 `master-立绘参考.png` → 派生核心资产卡 → 打包专属三模式配图 Skill

---

## 阶段 0：检查工作区与能力

1. 确认归档根路径：优先使用用户指定目录，否则默认 `03-Assets/YYYY-MM-DD-<主题>-personal-ip/`。
2. 检查当前环境图像能力：
   - 是否有支持**参考图输入**的图像生成工具（内置 `image_gen` / `GenerateImage`、Codex image 或外部工作流）。
   - 若无生图能力：如实说明缺少生图依赖，继续完成访谈并交付完整 `character-contract.md`、可直接粘贴的 Prompt 骨架与 Stage 5 Skill 模板，不假装已出图。

## 阶段 1：读取输入并确定路径

先礼貌询问用户是否有**个人照片**、**喜欢的角色/画风参考图**或**想升级的旧头像**；若用户明确没有图或想纯文字从零设定，直接进入纯文字路径。

按输入类型提炼（详见 [design-interview.md](references/design-interview.md)）：

- **照片转 IP**：列出用户希望保留的真人辨识点（发型、眼镜、耳饰、肤色倾向、神态），其余按目标画风简化提纯。
- **参考图借气质转原创 IP**：拆解「可借视觉语言（情绪、头身比、配色关系、笔触氛围）」与「必须原创替换项（五官细节、服装结构、职业道具、品牌符号）」。
- **无图从零设定 / 旧头像升级**：提炼核心人设关键词、视觉记忆点与需要保留/淘汰的旧特征。

## 阶段 2：每轮 3～5 问（给推荐选项）

每轮打包 3～5 个问题并附推荐答案，已确认项跨轮保留，信息够了就停，不要走 11 轮一次一问，也不要把用途展开成封面/场景制作清单。

第一轮优先对齐 5 件事（细节选项与赛道预设见 [design-interview.md](references/design-interview.md)）：

1. **输入与原创边界**：用哪条输入路径？哪些特征保留，哪些必须原创化？
2. **画风与头身比**：从速选表选定（无偏好时默认推荐「Q 版手绘平涂 / 3～3.5 头身 / 浅底」；也可自选赛璐璐、扁平矢量、像素、3D 盲盒/粘土、半写实等）。
3. **第一眼记忆点**：发型发色、固定服装、1 个识别配件、主色/辅色/点缀色、品牌符号（如有）。
4. **身份与性格**：本人分身还是虚构角色？一句话内容定位与 2～3 个能驱动动作的性格词。
5. **首批 4～6 个静态表情**：直接匹配创作者内容里最常出现的情绪（可从赛道推荐包勾选）。

## 阶段 3：试定稿并锁定 `master`（最多 3 张）

在生成设定卡和表情前，先试出最多 3 张单人物候选图，让用户看清「这个角色长什么样」。

### 候选图硬约束

- 干净单人物全身或稳定半身（推荐全身，便于后续三视图推导），正面或微侧自然站姿。
- **纯白或纯浅单色/透明背景**，画面内禁止出现三视图拼版、色卡条、文字标签、装饰边框或场景道具堆砌。
- 画风、渲染质感、头身比严格按阶段 2 确认执行。

### 迭代与锁定规则

- 每次重绘**只改一个主要问题**（如调整发型、更换配色或修正头身比）。
- 参考图输入始终回到**用户原始照片/参考图 + 已确认契约**，禁止拿上一张失败的候选图继续套娃。
- 3 张仍未过关时，交付当前最佳版本并说明待调整的单一差距，等待用户方向。
- **用户明确拍板（「就这版 / 定稿 / 锁定」）后**，将最终选定图直接归档为：
  `01-数字资产卡/master-立绘参考.png`
  并将其路径写入 `character-contract.md`。

### 阶段 3 Prompt 骨架（`master-立绘参考.png`）

按所选生图工具适配输入方式（多模态 `Input images` / Midjourney `--cref` / Flux Redux），直接套用以下骨架并替换 `{{...}}`：

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

只交付以下核心资产，禁止自行加出封面、背景图、场景图或 GIF。

1. `01-数字资产卡/角色设定卡.png`（1 张）
2. `character-contract.md`（1 份，模板见 [character-contract.md](references/character-contract.md)）
3. `02-头像与表情/头像-透明.png`（1 张）
4. `02-头像与表情/表情-01～06-透明.png`（4～6 张）

### 一致性铁律

- **唯一真源**：阶段 4 所有生成图都必须把 `01-数字资产卡/master-立绘参考.png` 作为 `Image 1` 传入；**禁止用上一张派生图接力生图**。
- **画风继承**：线条、上色、光影与材质必须严格跟随 `master-立绘参考.png`，不强行改成未选定的其他画风。
- **结构硬约束**：侧面必须是真 90° 正侧面（不能画成 3/4 侧脸）；背面后脑勺不得长出正面五官；头像在圆形裁切下脸与识别配件清晰；表情遮住文件名/文字后仍可一眼分辨情绪。
- **默认无字**：除设定卡色条上的 HEX 色值外，默认不生成多余文字、装饰排版、第三方 Logo 或水印。

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

### 归档目录

保存到用户指定路径，默认：

```text
03-Assets/YYYY-MM-DD-<主题>-personal-ip/
├── character-contract.md
├── 01-数字资产卡/
│   ├── master-立绘参考.png
│   └── 角色设定卡.png
└── 02-头像与表情/
    ├── 头像-透明.png
    └── 表情-01～06-透明.png
```

修订不覆盖旧版，用 `-v2`、`-v3` 递增。交付前按 [asset-checklist.md](references/asset-checklist.md) 逐项验收。

---

## 阶段 5：生成专属三模式配图 Skill

核心资产验收通过后，默认在用户项目或指定目录生成可独立分发、即装即用的专属配图 Skill 文件夹：

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

生成规则：

1. **直接基于模板生成**：读取 [illustration-skill-template.md](references/illustration-skill-template.md)，将占位符替换为本次锁定的角色名、画风规则、HEX 色表、`Character Lock` 段落与本地素材相对路径。
2. **三模式开箱内置**：生成的 `SKILL.md` 必须完整保留「解释型配图（默认）/ 信息图模式 / 封面模式」三条路由、动态画幅策略与合一交稿前自查清单。
3. **资产自包含**：所有参考图拷入 `<name>-ip-illustrations/assets/`，使用相对路径引用，不依赖外部目录。
4. **不写死固定画幅**：不在配图 Skill 中锁死具体比例或像素，由用户在每次出图时指定。
5. **版本同步提示**：告知用户日后角色资产改版时，需同步替换 `assets/` 与 `character-contract.md` 并在 `SKILL.md` 递增版本号；该文件夹可直接放入个人 GitHub Skill 仓库供任意 Bot / Agent 安装。

## 动态表情（可选扩展）

本 skill 不直接制作 GIF 或动态表情。若用户需要会动的表情，引导其将已锁定的 `master-立绘参考.png`、`角色设定卡.png` 与静态透明表情包交给外部 GIF / 动效 skill 处理。

## 最终交付物清单

1. `character-contract.md`（含锁定路径、画风 HEX 规范与 `Character Lock`）
2. `01-数字资产卡/master-立绘参考.png` 与 `01-数字资产卡/角色设定卡.png`
3. `02-头像与表情/头像-透明.png` 与 4～6 张 `表情-01～06-透明.png`
4. `<name>-ip-illustrations/` 专属三模式配图 Skill 文件夹（内置 `assets/` 与 `character-contract.md`）
5. 简短验收说明：补全了原图未展示的哪些部位、哪些细节仍需用户审美终审（无生图工具时如实说明仅交付契约与可执行 Prompt）

## 边界与禁止

- 未锁定 `master-立绘参考.png` 之前，不出设定卡、头像与表情包
- 不在阶段 4 重复生成功能重叠的「视觉规范卡」
- 不把参考图或真人照片当成一比一复刻模板
- 不强迫偏好其他画风的用户套用「浅底手绘线稿」
- 开场不制作封面、背景图、日常配图、场景图或 GIF（全部留给阶段 5 专属配图 Skill 按需派生）
- 无生图能力时不假装已出图

## References

- [references/design-interview.md](references/design-interview.md) — 三类输入路径预设、画风与头身比速选表、赛道表情推荐包
- [references/character-contract.md](references/character-contract.md) — 通用角色设计契约与 Character Lock 模板
- [references/asset-checklist.md](references/asset-checklist.md) — 核心资产与衍生 Skill 验收清单
- [references/illustration-skill-template.md](references/illustration-skill-template.md) — 阶段 5 专属三模式配图 Skill 模板
