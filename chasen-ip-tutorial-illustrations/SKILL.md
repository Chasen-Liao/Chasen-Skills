---
name: chasen-ip-tutorial-illustrations
description: Generate original 16:9 Chinese tutorial illustrations with Chasen's anime personal IP, consistent character design, white hand-drawn explanatory visuals, sparse short Chinese annotations, separate images for each core idea, and repository asset archiving. Use when users ask for tutorial, workflow, method, tool, process, concept, or system illustrations featuring Chasen; a full tutorial text is optional.
metadata:
  author: Chasen-Liao
  version: "0.1.0"
  category: workflow
  requires: Local image viewer and built-in image_gen with reference-image input support.
---

# Chasen IP 教程配图

## 定位

把一个教程、工具、流程、方法、概念或抽象观点，转化为一张清爽、可读、有动作感的 Chasen IP 解释型配图。

这个 skill 不要求先读取完整教程。用户可以只给一句画面需求；只要核心对象和动作明确，就直接生成。默认使用内置 `image_gen`，不切换到 CLI/API 路径。

## 参考资产

角色素材随 Skill 一起分发。以下路径均相对于本 `SKILL.md` 所在目录，不是当前工作目录；调用工具前先解析为绝对路径。生成前使用内置 IP 视觉规范板作为角色一致性参考：

```text
assets/chasen-ip/01-角色设定/Chasen-个人IP-视觉规范板.png
```

必要时再参考：

```text
assets/chasen-ip/02-头像与立绘/Chasen-个人IP-全身立绘.png
assets/chasen-ip/02-头像与立绘/Chasen-个人IP-头像-微笑.png
```

其余可选参考也在 `assets/chasen-ip/` 内：`01-角色设定/Chasen-个人IP-角色设定板-v1.png`、`03-表情与动作/Chasen-个人IP-表情动作-六格.png`、`04-内容场景/Chasen-个人IP-横版主视觉.png`、`04-内容场景/Chasen-个人IP-内容场景-四格.png` 和 `05-贴纸与装饰/Chasen-个人IP-贴纸表情-八格.png`。只在相关动作或构图需要时查看，不将多格参考图直接作为交付构图。

若当前对话尚未加载参考图，先用本地图片查看工具检查，再作为 `Image 1: character visual reference` 传给图像生成工具。不要修改或覆盖 Skill 内的原始素材。

## 适用请求

触发例子包括：

- “用 Chasen 演示一次 API 调试流程。”
- “给这个 Vibe Coding 方法画一张教程配图。”
- “画 Chasen 排查报错、找到问题并修复的过程。”
- “用 Chasen 解释这个 AI Agent 工作流。”

用户没有提供完整教程时，不要求补交正文。若主题、对象和动作仍然足够明确，直接补全构图并生成；只有缺少核心对象或动作时才追问。

## 视觉硬约束

### Chasen IP

每张图都让 Chasen 成为核心动作主体：操作、演示、排查、解释、连接、搬运、反应或展示，不要让她只是站在旁边装饰。

必须尽量保持：

- 女性 Q 版动漫形象，约 3.5 头身。
- 短浅棕发、不对称刘海、略微凌乱的发尾。
- 深棕大眼和青蓝高光。
- 粉色无袖上衣、浅灰白短外套、深色下装。
- 银色科技头戴式耳机，青蓝灯带和少量粉色点缀。
- 耳机或服装上的青蓝电路感 `C` 标识。

AI 悬浮界面、代码、节点或报错符号只在主题需要时加入，不强迫每张图都出现完整 UI。

### 画面风格

- 默认 16:9 横版；只有用户明确要求时才切换为 1:1 或 4:5。
- 纯白背景，深灰手绘线稿，清爽平涂，少量柔和阴影。
- 主色为粉色、白色、浅灰、青蓝和深灰；保持与 Chasen 设定板一致。
- 单图只表达一个核心意思，保留明显留白。
- 可以使用少量怪诞或隐喻元素，但隐喻必须服务于教程内容，不能照搬小黑技能的角色、颜色或已有构图。
- 不做 PPT、商业信息图、复杂架构图或满屏 UI。图要像一张有动作的手绘解释图。

### 文字

- 默认不生成文字。
- 用户明确提供文字时，只保留 1–5 个短中文关键词或短句，并要求逐字准确、手写批注感。
- 不擅自添加标题、段落、品牌名、长句或复杂 UI 文案。
- 避免左上角自动出现“教程”“流程图”“常见坑”等类型标题。

## 工作流

### 1. 解析请求

提炼四件事：

1. 核心对象：工具、代码、流程、问题或概念。
2. 核心动作：Chasen 正在做什么。
3. 认知结果：观众看完要理解什么。
4. 必要元素：最多加入 1–2 个辅助物件或符号。

如果用户一次提出多个核心意思，为每个意思单独生成一张图，不拼成多格图。

### 2. 组织提示词

每张图的提示词至少包含：

- `Use case: illustration-story`；如果用户明确要求流程图或结构图，再考虑 `productivity-visual`。
- `Asset type: 16:9 Chinese tutorial illustration`。
- `Input images: Image 1: Chasen visual reference`。
- 纯白背景、Chasen 核心动作、单一视觉隐喻或结构、留白和短文字约束。
- 明确要求保持发型、耳机、服装、C 标识和粉白青蓝配色一致。
- 明确禁止额外角色、可读性差的长文字、品牌 Logo、水印、密集背景和风格漂移。

不要把多个不同画面的 prompt 合并在一次生成里；每个核心意思调用一次图像生成。

### 3. 生成

用户已经明确要求“生成/画/做配图”时，直接调用内置 `image_gen`，不先等待额外确认。使用 Skill 内的参考图作为输入图，并把它标记为角色视觉参考，而不是编辑目标。若当前环境没有内置图像生成工具，说明缺少的依赖，不静默改用 CLI/API，也不声称已生成。

如果生成结果中的角色、动作、画幅、留白或文字不符合规范，先检查结果，再只修改一个主要问题进行针对性重生成。不要为了追求数量自动生成大量变体。

### 4. 检查

归档前检查：

- Chasen 是否真正参与核心动作。
- 发型、耳机、服装、C 标识和配色是否稳定。
- 是否只有一个核心意思，辅助元素是否过多。
- 是否为默认 16:9，背景是否干净留白。
- 中文标注是否仅来自用户提供的短文本，是否出现乱码或多余文字。
- 是否误用了小黑 IP、现有案例构图、第三方 Logo 或水印。

不满足时，优先单点迭代；未通过检查的版本不要作为最终资产交付。

### 5. 保存

优先按用户指定目录保存。未指定时，以当前项目根目录为基准，将最终图片保存到：

```text
03-Assets/YYYY-MM-DD-<主题>-chasen-ip-illustrations/
```

同一批素材按顺序命名，例如：

```text
01-api-debugging.png
02-agent-loop.png
```

不要覆盖已有文件；修订使用 `-v2`、`-v3` 等后缀。内置生成器的默认输出可以保留，但项目最终使用的图片必须复制到上述输出目录。生成结果不要写回 Skill 安装目录或 `assets/` 素材目录。

## 交付口径

完成后只需说明：

- 生成了几张。
- 每张图的用途。
- 最终保存路径。
- 是否做过针对性迭代。

不要输出冗长的风格理论或完整提示词解析，除非用户主动要求。
