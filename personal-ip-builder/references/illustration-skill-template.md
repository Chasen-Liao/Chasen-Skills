# 阶段 5 专属配图 Skill 模板（`illustration-skill-template.md`）

> **三模式配图 Skill 仓库唯一母模板**：本仓库内所有三模式配图规则（包括阶段 5 生成的 `<name>-ip-illustrations` 及 `chasen-ip-tutorial-illustrations`）均以本模板为单真源同步。
> 使用方式：在阶段 5 为用户生成 `<name>-ip-illustrations/SKILL.md` 时，把下方虚线框内的完整模板复制过去，将所有 `{{...}}` 占位符替换为本次 `character-contract.md` 锁定的真实内容，并删掉模板说明。所有参考图路径均指向同目录下的 `assets/`。

---

````markdown
---
name: {{SKILL_SLUG}}
description: >-
  Generate {{IP_NAME}} IP visuals: default {{STYLE_SHORT}} explanatory
  illustrations; dense 信息图 when asked; vibrant covers/banners when the ask
  is 封面/cover. Aspect ratio and pixels are chosen at generation time, not
  fixed in this skill. Use for tutorial, workflow, concept, comparison, or
  cover banners featuring {{IP_NAME}}.
license: MIT
compatibility: >-
  Prioritizes built-in image_gen / GenerateImage with reference-image input;
  supports user-configured reference-capable generators (Codex image, GPT-4o,
  Nano Banana, Midjourney --cref, Flux Redux) and requires a local image
  viewer.
metadata:
  author: {{AUTHOR_NAME}}
  version: "0.1.0"
  category: workflow
---

# {{IP_NAME}} IP 配图生成器

## 定位与输入

将教程、工具、流程、方法、概念、产品体验或观点，转化为角色风格统一的 **{{IP_NAME}}** 专属配图；或在用户要「封面 / cover / 长文封面 / 商单封面」时，生成高点击率视觉封面。

- **轻量触发**：不需要先交完整长文；只要用户给出一句画面需求，且核心对象与动作明确，即可直接组织提示词出图。只有缺少核心对象或动作时才追问。
- **动态画幅**：本 skill 不写死比例（如 16:9、5:2、3:1、4:3）或像素尺寸；每次出图时按用户指定或当次场景需要传入生图参数，并在 Prompt 中标明安全构图区。
- **独立多意**：若用户一次给出多个核心意思且不是信息图/封面，为每个意思单独生成一张图，不拼多格图。

## 参考资产与环境路径

以下路径均相对于本 `SKILL.md` 所在目录（不是当前工作目录）；调用工具前先解析为绝对路径，并用本地看图工具确认后作为视觉参考传入，禁止修改或覆盖 `assets/` 原始素材：

- **主参考真源（必传 `Image 1`）**：`assets/master-立绘参考.png`
- **多视角与配件/色卡补充**：`assets/角色设定卡.png`（涉及侧面、背面或配件细节时一并参考）
- **头像与情绪动作参考（按需）**：`assets/头像-透明.png`、`assets/表情-01～06-透明.png`（不把透明表情图直接原封贴成整张配图构图）

**多工具与沙箱环境适配**：
- 优先直接调用当前环境内置 `image_gen`（或 `GenerateImage`），不静默切换到未授权外部 CLI/API；若用户明确配置了 Codex image、GPT-4o、Nano Banana、Midjourney（`--cref`）或 Flux Redux 等带参考图能力的工具，可按其接口适配传参。若当前环境没有可用生图能力，如实说明缺口，只输出完整 Prompt 而不假装已生成。
- 若运行在路径受限环境（如 Grok Bot），调用 `GenerateImage` 前先将 `assets/` 下需要传入的参考图复制到 `/workspace/...` 或当前 agent 允许的 `attachments` / `assets` 目录再传路径。

## {{IP_NAME}} Character Lock（每次生图必带）

将以下锁定段落原样写入每次生图 Prompt，确保角色、画风、配色跨图零漂移：

```text
{{CHARACTER_LOCK_BLOCK}}
```

## 三模式路由与硬规则（写 Prompt 前先定模式）

| 模式 | 何时启用 | 角色占比与动作 | 背景与构图 | 文字规则 |
| :--- | :--- | :--- | :--- | :--- |
| **解释型配图（默认）** | 教程步骤、概念拆解、工具演示、观点配图 | **核心动作主体**：操作、演示、排查、连接、搬运、反应，不站在角落干看 | 严格遵循 `master` 锁定画风（{{STYLE_SUMMARY}}），搭配 {{DEFAULT_BG_DESC}} 与明显留白；单图只讲一个核心意思 | 默认不生成文字；用户给字时仅留 1–5 个短关键词，逐字准确，禁擅自加「教程/流程图」标题 |
| **信息图模式** | 用户明确要「信息图 / 对比图 / 讲解图信息密度大」 | **极小靠边**：仅占画面高度 10%–15%，优先**左下角露头肩**看向信息区，禁居中大立绘抢版面 | 信息密度优先于留白：顶栏一句话结论 → 左「旧/问题」多步卡片 → 中「换成」箭头 → 右「新/方案」多步卡片 + 侧边短标签 → 底栏行动号召（4–6 步左右对称） | 从用户稿提炼短标签（每条尽量 ≤12 字），不编造实测数字；专有英文名逐字核对 |
| **封面模式** | 用户说「封面 / cover / 长文封面 / 商单封面」或丢来参考海报要改标题/融入 IP | **分侧展示主体**：占画面一侧展示产品、递卡、比心或做出夸张情绪动作，配件与品牌符号清晰 | **禁止整页纯白底与大块不透明白 PPT 卡片**；必须有场景/光影/品牌色渐变氛围；左文右物（或右文左物）分侧，可读性用半透明雾面/轻渐变托字 | 允许「主标题 / 副标题 / 角标按钮」三层；主标题须有**分层艺术字感**（描边、双色、立体或强调色块），逐字使用用户定稿文案；禁止抄官方参考图原英文 |

### 各模式 Prompt 组织要点

- **解释型配图**：标注 `Use case: illustration-story`，写明 `Image 1: master character reference`、保持 {{STYLE_SUMMARY}} 与固定 HEX 配色（{{PALETTE_HEX}}）、{{DEFAULT_BG_DESC}} 背景与核心动作；辅助物件最多 1–2 个，不硬塞满屏 UI。
- **信息图模式**：标注 `Use case: productivity-visual`，写明 `{{IP_NAME}} tiny head-and-shoulders bottom-left only (10%-15% height)`、`dense structured two-column comparison cards`、以及逐字准确的中文短标签与英文专有名词；仍保持 {{STYLE_SUMMARY}} 视觉气质，不用真实截图硬拼贴。
- **封面模式**：标注 `Use case: illustration-story / cover banner`，明确写 `scenic or atmospheric gradient background, NO solid white poster background, NO opaque white PPT card`、`split composition: layered artistic Chinese headline on one side, {{IP_NAME}} interacting with product/prop on the other`、以及当次指定的画幅安全裁切带；可按需保留官方小吉祥物，不另造无关新角色。

## 交稿前自查（合一清单）

成图后必须逐项检查，任一项不通过不要直接交付：

1. **通用角色一致性（对比 `assets/master-立绘参考.png`）**：
   - 发型、发色、五官、服装、识别配件与品牌符号是否零漂移？
   - 画风质感与主/辅/点缀色（{{PALETTE_HEX}}）是否与 `master` 保持同一视觉体系？
   - 是否误混入无关角色、第三方 Logo 或水印？
2. **模式分项检查**：
   - **解释型**：是否真的只有 1 个核心意思？角色是否正在参与动作而不是呆立？是否有多余乱字？
   - **信息图**：角色是否足够小且靠边不抢版面？卡片结构是否对齐？中文短句与英文专有名词拼写是否 100% 准确？
   - **封面**：缩略图下主标题是否清晰吸睛？有没有退化成「白底课本插图」或大白块 PPT？按目标画幅裁切后脸部、配件、主标题与角标是否完整？中文是否残字、叠字或漏字？
3. **失败修正策略**：
   - 发现问题时**只改一个主要问题**做单点迭代（回到 `assets/master-立绘参考.png` 重新生成，不要拿残图连续套娃）。
   - 若仅个别中文字符写错或位置微偏，优先使用本地贴字/局部重绘修正，不要整图糊弄或推翻满意构图。

## 归档与交付口径

- **保存路径**：优先按用户指定路径；未指定时默认保存至 `03-Assets/YYYY-MM-DD-<主题>-{{SKILL_SLUG}}/`（Grok Bot 默认 `/workspace/{{IP_SLUG}}/illustrations/YYYY-MM-DD-<主题>/`）。同批按序命名，修订使用 `-v2`、`-v3`，不覆盖已有文件，不写回本 Skill 的 `assets/` 目录。
- **交付说明**：只汇报 4 件事——生成了几张与所用模式、每张图用途、最终保存路径、是否做过单点迭代（除非用户要求，不输出冗长 Prompt 解析）。
````
