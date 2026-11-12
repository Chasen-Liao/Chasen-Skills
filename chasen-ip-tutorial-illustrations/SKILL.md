---
name: chasen-ip-tutorial-illustrations
description: >-
  Generate Chasen IP visuals: default white hand-drawn tutorial
  illustrations; dense 信息图 when asked; vibrant X Article / 商单 covers when the
  ask is 封面/cover. Aspect ratio and pixels are chosen at generation time, not
  fixed in this skill. Use for tutorial, workflow, concept, comparison, or cover
  banners featuring Chasen.
license: MIT
compatibility: Needs local image viewer and built-in image_gen (or GenerateImage) with reference-image input.
metadata:
  author: Chasen-Liao
  version: "0.3.0"
  category: workflow
---
# Chasen IP 教程配图

## 定位与输入

将教程、工具、流程、概念或产品需求，转化为统一风格的 Chasen IP 视觉配图（默认解释型配图；按需切换信息图或封面模式）。

- **零门槛输入**：一句话、半截思路或画面描述即可出图，不强求先读完整文章；只要核心对象与动作明确就直接生成，仅在缺少核心对象或动作时追问一次。
- **画幅与像素**：本 skill 不写死比例（如 `5:2`、`3:1`、`16:9`）或像素尺寸，由用户或 Agent 在当次调用生图工具时指定（默认横版）。
- **多意图拆分**：单次请求包含多个核心意思且非信息图/封面单板时，按意思逐张生成，不拼多格图；本 skill 不出表情包贴纸包或 GIF。
- **工具约束**：默认直接调用环境内置 `image_gen`（或 `GenerateImage`），不静默切换到外部 CLI/API；若当前环境缺少支持参考图输入的生图工具，直接说明缺失依赖，不声称已生成。

## 参考资产与环境路径

角色素材随本 Skill 分发。以下路径均相对于本 `SKILL.md` 所在目录（非当前工作目录），调用工具前先解析为绝对路径；严禁修改或覆盖 `assets/` 原始素材：

- **主参考（必传）**：`assets/chasen-ip/01-角色设定/Chasen-个人IP-视觉规范板.png`
- **辅参考（按需）**：
  - `assets/chasen-ip/02-头像与立绘/Chasen-个人IP-全身立绘.png`
  - `assets/chasen-ip/02-头像与立绘/Chasen-个人IP-头像-微笑.png`
- **动作/场景补充（仅在相关动作或构图需要时查看）**：
  - `assets/chasen-ip/01-角色设定/Chasen-个人IP-角色设定板-v1.png`
  - `assets/chasen-ip/03-表情与动作/Chasen-个人IP-表情动作-六格.png`
  - `assets/chasen-ip/04-内容场景/Chasen-个人IP-横版主视觉.png`
  - `assets/chasen-ip/04-内容场景/Chasen-个人IP-内容场景-四格.png`
  - 不可直接把多格参考图作为交付构图。
- **传图方式**：当前对话尚未加载主参考图时，先用本地图片查看工具读取确认，再作为 `Image 1: character visual reference` 传入（标记为角色视觉参考，而非编辑目标）。
- **Grok Bot / `GenerateImage` 环境路径限制**：部分运行环境要求参考图位于工作区允许目录；此时先将所需参考图复制到 `/workspace/...` 或当前 agent 的 `attachments` / `assets` 目录后再传入 `reference_image_paths`，不要直接传入 Skill 安装目录原路径。

## Chasen Character Lock（角色硬约束）

### 固定外观特征

- **角色设定**：女性 Q 版动漫形象，约 3.5 头身。
- **发型与眼睛**：短浅棕发、不对称刘海、略微凌乱发尾；深棕大眼配青蓝高光。
- **服装与配饰**：粉色无袖上衣、浅灰白短外套、深色下装；银色科技头戴式耳机（青蓝灯带与少量粉色点缀）。
- **识别标识**：耳机或服装上的青蓝电路感 `C` 标识。
- **边界禁令**：严禁照搬小黑 IP 的角色、配色或已有案例构图；严禁自创第二个人设（封面仅可保留品牌方提供的官方小吉祥物，如黄星星）、第三方 Logo 或水印；AI 悬浮界面、代码、节点、报错符号仅在主题需要时加入，不强迫每张图塞满完整 UI。

### Character Lock 锁死块（直接拼入 Prompt）

```text
[Character Lock]
Chasen: female chibi anime character (~3.5 head-to-body ratio), short light-brown hair with asymmetrical bangs and slightly messy ends, large dark-brown eyes with cyan-blue highlights, wearing a pink sleeveless top under a light gray-white cropped jacket and dark bottoms, silver futuristic over-ear headphones with cyan-blue light strips and subtle pink accents, cyan circuit-style "C" emblem on the headphones or outfit. Keep character proportions, outfit, palette (pink, white, light gray, cyan-blue, dark gray), and facial traits strictly consistent with Image 1 (character visual reference). No other original characters, no third-party logos or watermarks.
角色锁死：女性 Q 版约 3.5 头身，短浅棕发与不对称微乱刘海，深棕大眼青蓝高光，粉色无袖上衣+浅灰白短外套+深色下装，银色科技耳机带青蓝灯带与少量粉色点缀，带青蓝电路感 C 标识，严格对齐图 1 视觉规范板。
```

## 三模式路由与硬规则

写 Prompt 前先确定唯一模式；未明确点名「信息图」或「封面」时，一律走**解释型配图（默认）**：

| 模式 | 何时启用 | 核心气质 |
|---|---|---|
| **解释型配图（默认）** | 教程步骤、工具演示、报错排查、流程/概念解释 | **纯白底**，深灰手绘线稿，清爽平涂，明显留白 |
| **信息图模式** | 用户明确要「信息图 / 对比图 / 信息密度要大」 | 手绘平涂高密度卡片，Chasen 缩至角落露头 |
| **封面模式** | 用户说「封面 / cover / X 长文封面 / 商单封面」或给海报改中文 | **禁纯白底与白 PPT 卡**，场景氛围 + 分层艺术字 + 角色互动 |

### 1. 解释型配图（默认）

- **何时启用**：教程步骤、工具操作、API/报错排查、工作流演示、概念或观点解释；未点名信息图或封面时的默认入口。
- **角色占比与动作**：Chasen 是画面核心动作主体，必须真正参与操作、演示、排查、连接、搬运或反应，不要站在旁边充当装饰。
- **背景与构图**：纯白背景，深灰手绘线稿，清爽平涂与少量柔和阴影，主色保持粉、白、浅灰、青蓝与深灰；单图只表达一个核心意思，保留明显留白，最多 1–2 个辅助物件或隐喻元素；不做 PPT、商业海报或密集写实背景。
- **文字规则**：默认不生成文字；用户明确要求文字时，只保留 1–5 个手写批注感短中文关键词或短句，不擅自加“教程”“流程图”“常见坑”等角标标题或长段落。
- **Prompt 必填项**：`Use case: illustration-story`（纯流程/结构图可用 `productivity-visual`）、`Asset type: Chinese tutorial illustration`、当次指定画幅、`Input images: Image 1: character visual reference`、`Character Lock` 块、纯白手绘平涂与单一核心动作描述、无字或逐字中文短词要求。

### 2. 信息图模式

- **何时启用**：用户明确要求「信息图」「对比信息图」「讲解图信息密度大」，或需要一图讲清左右对比与多步流程时启用。
- **角色占比与动作**：Chasen 极小且靠边，只占画面高度约 10%–15%，优先**左下角露头（头肩）**看向信息区；禁止居中大立绘抢版面。
- **背景与构图**：保持手绘平涂气质，但信息密度优先于留白，不用真实截图拼贴或无人物纯 PPT；常见骨架为「顶栏一句话结论 → 左『旧/问题』多步卡片（4–6 步）→ 中间切换箭头 → 右『新/方案』多步卡片 + 侧边短标签 → 底栏一句行动号召」，铺满中间与右侧。
- **文字规则**：标签从用户稿或已定原理稿提炼短句（每条尽量 ≤12 字），严禁编造实测数字；英文专有名词（如 `codemode`）必须逐字正确。
- **Prompt 必填项**：`Use case: productivity-visual`、`Asset type: Chinese tutorial illustration`、当次指定画幅、`Input images: Image 1: character visual reference`、`Character Lock` 块、`Chasen tiny head-and-shoulders bottom-left only`、`dense two-column hand-drawn comparison cards`、逐字指定的中文与英文标签清单。

### 3. 封面模式

- **何时启用**：用户明确要求「封面」「cover」「长文封面」「商单封面」，或丢来官方海报要求改中文/融入 Chasen IP 时启用；绝不把默认白底教程图当封面交付。
- **角色占比与动作**：Chasen 占画面一侧（通常右半）作清晰展示主体，带明确表情与互动动作（递卡、展示手机 App、比心、比耶等）；可按 brief 加入产品道具（卡面人名若用户说无所谓可保留示意名），若官方参考图自带品牌小吉祥物（如 Starryblu 黄星星）可保留。
- **背景与构图**：采用**左文右物**（或左右对调）的清晰分区；背景必须有场景与氛围（浅蓝天空/云、城市剪影、地球线框、柔和光斑、品牌色渐变等），**禁止整页纯白或用大块不透明白 PPT 卡片遮挡场景**，可读性用半透明浅色雾面或轻渐变托字；按当次指定画幅在 Prompt 写明安全构图带。
- **文字规则**：逐字使用用户定稿文案，支持「主标题 / 副标题 / 角标按钮」三层排版；主标题要有**艺术字感**（描边、双色、立体或强调色块），禁止整页同号纯黑黑体；品牌名拼写准确（如 `Starryblu`）；参考官方海报时只借构图、道具与氛围，**严禁抄原图英文文案**。
- **Prompt 必填项**：`Use case: illustration-story`（营销横幅质感）、`Asset type: Chinese cover banner`、当次指定画幅与安全构图带、`Input images: Image 1: character visual reference`、`Character Lock` 块、`no solid white poster panel`、`scenic or sky gradient background`、`artistic layered Chinese headline` 及逐字中文标题/品牌名。

## 交稿前自查

出图后逐项核验，任一项不通过不得作为最终资产交付：

- **通用一致性**
  - [ ] Chasen 发型/刘海、深棕大眼青蓝高光、粉无袖+浅灰白短外套+深色下装、银色科技耳机与青蓝 `C` 标识是否稳定。
  - [ ] 成图是否符合当次指定的画幅比例与模式气质，无意外裁切。
  - [ ] 是否未混入无关第二人设、小黑 IP 元素、已有案例构图、第三方 Logo 或水印。
  - [ ] 所有中文与英文专有名词是否清晰可读、无残字/叠字/乱码/错拼。
- **解释型配图专项**
  - [ ] Chasen 是否真正参与核心动作，而非站桩装饰。
  - [ ] 是否为纯白底手绘平涂、单图只表达一个核心意思且保留明显留白。
  - [ ] 是否按要求无字或仅保留 1–5 个准确短关键词，未擅自生成“教程/流程图/常见坑”角标。
- **信息图专项**
  - [ ] Chasen 是否已缩至角落露头（约 10%–15% 高度）不抢版面。
  - [ ] 是否保持手绘平涂气质（非无人物纯 PPT 或截图拼贴），卡片结构可读且未编造实测数字。
- **封面专项**
  - [ ] 缩略图下主标题是否仍醒目，具备分层艺术字感，且与用户定稿逐字一致（未抄参考海报英文）。
  - [ ] 背景是否有场景氛围，未退化成白底课本插图或大块不透明白卡片挡景。
  - [ ] 按目标画幅检查，人物脸部、耳机、`C` 标识、产品道具、Logo 与角标按钮是否完整。
- **失败单点迭代与本地修字**
  - 不满足检查项时，每次只针对**一个主要问题**做定向重生成，不要自动批量刷变体。
  - 封面或信息图若仅出现局部文字乱码/拼错，或封面边缘裁切轻微偏差，优先本地贴字修字或重裁，再考虑整图重做。

## 归档与交付口径

- **保存路径**：优先按用户指定目录保存；未指定时：
  - **Grok Bot**：`/workspace/chasen-ip/illustrations/YYYY-MM-DD-<主题>/`（选题配图可再复制一份到对应 `topics/<slug>/`）。
  - **其他项目**：`03-Assets/YYYY-MM-DD-<主题>-chasen-ip-illustrations/`。
  - 同批素材按顺序命名，不覆盖已有文件，修订用 `-v2`、`-v3`（封面可另存 `cover-final.png`）；严禁写回 Skill 安装目录或 `assets/` 目录。
- **交付口径（极简）**：完成后只需说明生成张数与所用模式、每张图的用途、最终保存路径，以及是否做过针对性迭代；除非用户主动要求，不输出冗长风格理论或完整提示词。
