---
name: chasen-ip-tutorial-illustrations
description: >-
  Generate Chasen IP visuals: default white hand-drawn tutorial
  illustrations; dense 信息图 when asked; vibrant X Article / 商单 covers when the
  ask is 封面/cover. Aspect ratio and pixels are chosen at generation time, not
  fixed in this skill. Use for tutorial, workflow, concept, comparison, or cover
  banners featuring Chasen.
license: MIT
compatibility: >-
  Prioritizes built-in image_gen / GenerateImage with reference-image input;
  supports user-configured reference-capable generators and requires a local
  image viewer.
metadata:
  author: Chasen-Liao
  version: "0.3.1"
  category: workflow
---
# Chasen IP 教程配图

## 定位与输入

将教程、工具、流程、概念或产品需求，转化为统一风格的 Chasen IP 视觉配图（默认解释型配图；按需切换信息图或封面模式）。

- **零门槛输入**：一句话、半截思路或画面描述即可出图，不强求先读完整文章；只要核心对象与动作明确就直接生成，仅在缺少核心对象或动作时追问一次。
- **画幅与像素**：本 skill 不写死比例（如 `5:2`、`3:1`、`16:9`）或像素尺寸，由用户或 Agent 在当次调用生图工具时指定（默认横版）。
- **多意图拆分**：单次请求包含多个核心意思且非信息图/封面单板时，按意思逐张生成，不拼多格图；本 skill 不出表情包贴纸包或 GIF。
- **工具约束**：优先直接调用环境内置 `image_gen`（或 `GenerateImage`），不静默切换到未授权外部 CLI/API；若用户明确配置了其他支持参考图输入的生图工具可按需适配；若当前环境缺少支持参考图输入的生图工具，直接说明缺失依赖，不声称已生成。

## 参考资产与环境路径

角色素材随本 Skill 分发。以下路径均相对于本 `SKILL.md` 所在目录（非当前工作目录），调用工具前先解析为绝对路径；严禁修改或覆盖 `assets/` 原始素材：

- **主参考（必传）**：`assets/chasen-ip/01-角色设定/Chasen-个人IP-视觉规范板.png`
- **辅参考（按需）**：
  - `assets/chasen-ip/02-头像与立绘/Chasen-个人IP-全身立绘.png`
  - `assets/chasen-ip/02-头像与立绘/Chasen-个人IP-头像-微笑.png`
- **动作/场景补充（仅在相关动作或构图需要时查看，不可直接作交付构图）**：
  - `assets/chasen-ip/01-角色设定/Chasen-个人IP-角色设定板-v1.png`
  - `assets/chasen-ip/03-表情与动作/Chasen-个人IP-表情动作-六格.png`
  - `assets/chasen-ip/04-内容场景/Chasen-个人IP-横版主视觉.png`
  - `assets/chasen-ip/04-内容场景/Chasen-个人IP-内容场景-四格.png`
- **传图方式**：当前对话尚未加载主参考图时，先用本地图片查看工具读取确认，再作为 `Image 1: character visual reference` 传入（标记为角色视觉参考，而非编辑目标）。
- **沙箱/路径受限环境（如 Grok Bot）**：先将所需参考图复制到 `/workspace/...` 或当前 agent 允许的 `attachments` / `assets` 目录后再传参，不要直接传入 Skill 安装目录原路径。

## Chasen Character Lock（每次生图必带）

- **边界禁令**：严禁照搬无关 IP 的角色、配色或已有案例构图；严禁自创第二个人设（封面仅可保留品牌方提供的官方小吉祥物）、第三方 Logo 或水印；AI 悬浮界面、代码、节点、报错符号仅在主题需要时加入，不强迫每张图塞满完整 UI。

```text
[Character Lock]
Chasen: female chibi anime character (~3.5 head-to-body ratio), short light-brown hair with asymmetrical bangs and slightly messy ends, large dark-brown eyes with cyan-blue highlights, wearing a pink sleeveless top under a light gray-white cropped jacket and dark bottoms, silver futuristic over-ear headphones with cyan-blue light strips and subtle pink accents, cyan circuit-style "C" emblem on the headphones or outfit. Keep character proportions, outfit, palette (pink, white, light gray, cyan-blue, dark gray), and facial traits strictly consistent with Image 1 (character visual reference). No other original characters, no third-party logos or watermarks.
```

## 三模式路由与硬规则

写 Prompt 前先确定唯一模式；未明确点名「信息图」或「封面」时，一律走**解释型配图（默认）**：

| 模式 | 何时启用 | 角色占比与动作 | 背景与构图 | 文字规则 |
| :--- | :--- | :--- | :--- | :--- |
| **解释型配图（默认）** | 教程步骤、工具演示、API/报错排查、流程/概念或观点解释 | **核心动作主体**：真正参与操作、演示、排查、连接、搬运或反应，不站桩装饰 | **纯白背景**，深灰手绘线稿，清爽平涂与少量柔和阴影（粉/白/浅灰/青蓝/深灰）；单图只讲一个核心意思，明显留白，最多 1–2 个辅助物件；不做 PPT、海报或密集写实背景 | 默认不生成文字；用户要字时仅留 1–5 个手写批注感短关键词，禁擅自加「教程/流程图/常见坑」角标 |
| **信息图模式** | 用户明确要「信息图 / 对比信息图 / 信息密度大」 | **极小靠边**：仅占画面高度约 10%–15%，优先**左下角露头肩**看向信息区，禁居中大立绘抢版面 | 手绘平涂高密度卡片（不用真实截图拼贴或无人物纯 PPT）：顶栏一句话结论 → 左「旧/问题」4–6 步卡 → 中间切换箭头 → 右「新/方案」4–6 步卡 + 侧边短标签 → 底栏行动号召 | 从用户稿或已定原理稿提炼短句（尽量 ≤12 字），禁编造实测数字；英文专有名词（如 `codemode`）逐字准确 |
| **封面模式** | 用户说「封面 / cover / 长文封面 / 商单封面」或给海报改中文/融入 IP（绝不把白底教程图当封面） | **分侧展示主体**：占画面一侧（通常右半）递卡、展示 App、比心/比耶等；按需加产品道具或品牌小吉祥物 | **禁整页纯白与大块不透明白 PPT 卡片**；必须有场景/氛围背景（天空云朵、城市剪影、地球线框、光斑、品牌色渐变），采用左文右物（或对调）分区 + 半透明雾面/轻渐变托字；Prompt 标明当次画幅安全裁切带 | 逐字使用用户定稿「主标题 / 副标题 / 角标按钮」三层文案；主标题须有**分层艺术字感**（描边、双色、立体或强调色块），禁纯黑同号黑体；品牌名逐字准确；参考海报时禁抄原图英文 |

### 各模式 Prompt 必填项

- **解释型配图**：`Use case: illustration-story`（纯流程/结构图可用 `productivity-visual`）、`Asset type: Chinese tutorial illustration`、当次画幅、`Input images: Image 1: character visual reference`、`Character Lock` 块、纯白手绘平涂与单一核心动作描述、无字或逐字中文短词要求。
- **信息图模式**：`Use case: productivity-visual`、`Asset type: Chinese tutorial illustration`、当次画幅、`Input images: Image 1: character visual reference`、`Character Lock` 块、`Chasen tiny head-and-shoulders bottom-left only`、`dense two-column hand-drawn comparison cards`、逐字中英文标签清单。
- **封面模式**：`Use case: illustration-story`、`Asset type: Chinese cover banner`、当次画幅与安全构图带、`Input images: Image 1: character visual reference`、`Character Lock` 块、`no solid white poster panel`、`scenic or sky gradient background`、`artistic layered Chinese headline` 及逐字中文标题/品牌名。

## 交稿前自查

成图后逐项核验，任一项不通过不得直接交付：

1. **通用与文字**：发色/刘海、青蓝高光大眼、粉无袖+浅灰白外套+深色下装、银色耳机与青蓝 `C` 标识是否稳定；无无关第二人设、第三方 Logo 或水印；符合目标画幅且中英文无残字/叠字/错拼。
2. **模式核验**：
   - **解释型**：单图仅 1 个核心意思、角色在动作中、纯白底留白且无多余角标字。
   - **信息图**：Chasen 仅占角落约 10%–15% 高度、保持手绘卡片质感、无编造数字。
   - **封面**：缩略图下分层艺术字主标题醒目且逐字一致（未抄原海报英文）、具备氛围背景未退化成白卡片、人物核心特征与道具/角标在安全区完整。
3. **失败修正**：每次只针对**一个主要问题**单点重生成（回到 `Image 1` 参考，不自动批量刷变体）；仅局部错字或微偏裁切时优先本地贴字/重裁。

## 归档与交付口径

- **保存路径**：优先用户指定目录；未指定时 Grok Bot 存 `/workspace/chasen-ip/illustrations/YYYY-MM-DD-<主题>/`（选题配图可另拷一份到 `topics/<slug>/`），其他项目存 `03-Assets/YYYY-MM-DD-<主题>-chasen-ip-illustrations/`。同批按序命名，修订用 `-v2`、`-v3`（封面可另存 `cover-final.png`），严禁写回 Skill 目录或 `assets/`。
- **交付口径（极简）**：仅汇报生成张数与所用模式、每张用途、最终保存路径、是否做过单点迭代；除非用户要求，不输出冗长风格理论或完整提示词。
