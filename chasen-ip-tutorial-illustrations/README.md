# 🎨 IP 教程配图（`chasen-ip-tutorial-illustrations`）

> 通用三模式角色 IP 配图 Skill — 接入你自己的角色参考图（或私有配置），生成风格统一的**解释型白底教程图**、**高密度对比信息图**与**有场景氛围的长文/商单封面**。

<p>

![Version](https://img.shields.io/badge/version-0.4.0-7c3aed?style=flat-square)
![Assets](https://img.shields.io/badge/Assets-Bring_Your_Own_IP-0ea5e9?style=flat-square)
![Modes](https://img.shields.io/badge/模式-教程_|_信息图_|_封面-f59e0b?style=flat-square)
![Image Gen](https://img.shields.io/badge/依赖-内置_image__gen-10b981?style=flat-square)

</p>

> 💡 目录名保留 `chasen-ip-tutorial-illustrations` 以兼容既有安装命令。本公开仓库**不内置任何个人角色素材**；请放置你自己的参考图，或先用 [`personal-ip-builder`](../personal-ip-builder/README.md) 生成角色资产包。

---

## 能做什么

| 特性 | 说明 |
| :--- | :--- |
| 三种模式 | **解释型**白底教程图（默认）· **信息图**高密度对比 · **封面**有场景 + 艺术字 |
| 动态画幅 | 比例与像素在出图时指定，不在 Skill 内写死 `5:2` / `16:9` 等 |
| 角色一致性 | 读取用户提供的参考图与 `Character Lock` 段落，严格防画风与特征漂移 |
| 解释型构图 | 角色参与操作、演示、排查或解释，一个核心意思一张图 |
| 封面不单调 | 禁止整页白底 / 白 PPT 卡片；要有氛围背景、分层标题与产品道具 |
| 控制文字 | 教程默认无字；封面用用户定稿主/副标题；信息图允许多短标签 |
| 项目内交付 | 结果保存到用户指定目录或当前项目的 `03-Assets/` |

---

## 安装与前置

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill chasen-ip-tutorial-illustrations --global --yes
```

**前置条件**：
- 运行环境提供本地看图工具以及支持参考图输入的 `image_gen` / `GenerateImage`（缺工具时会如实说明，不假装已生成）。
- 提供你自己的角色参考图（见 [`assets/README.md`](./assets/README.md)）及 `Character Lock` 文本（可在私有配置或会话中覆盖）。

---

## 用法

```text
用 $chasen-ip-tutorial-illustrations 和我的角色参考图，画一张排查 API 报错的教程配图。
```

也可以直接说：

- 用我的 IP 角色解释这个 AI Agent 工作流，白底无字。
- 画一张左右对比信息图，信息密度要大。
- 做一张长文封面 / 商单封面，融入我的角色，主标题……

出图时向生图工具说明本次画幅即可；多个核心意思分别出图（信息图 / 封面单板除外）。

---

## 输出示例

以下为文件命名示例：

```text
当前项目/
└── 03-Assets/YYYY-MM-DD-api调试-ip-illustrations/
    ├── 01-api-debugging.png
    ├── 02-error-fix.png
    └── cover-final.png
```

已有文件不覆盖，修订使用 `-v2`、`-v3` 后缀。

---

## 目录

```text
chasen-ip-tutorial-illustrations/
├── SKILL.md            # Agent 执行契约（三模式路由、Character Lock 模板与自查）
├── README.md           # 本文件
└── assets/
    └── README.md       # 用户自备角色参考图放置说明
```

---

## Changelog

- **0.4.0**：公开版脱敏通用化 — 移除个人专属角色图片资产与硬编码人设，改为由用户自备或私有配置挂载角色参考图与 `Character Lock`。
- **0.3.1**：清理未引用资产与重复规则，对齐仓库三模式母模板。
- **0.3.0**：重构 `SKILL.md` 为单点规则与统一交稿前自查。
- **0.2.1**：画幅与像素改由出图时指定；明确不出贴纸/GIF。
- **0.2.0**：新增封面模式与信息图模式。
- **0.1.0**：初版白底手绘教程配图。

---

## 📄 License

MIT © Chasen-Liao
