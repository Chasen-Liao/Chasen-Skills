# 📡 x-ai-radar

> Antigravity 专用 · 自动刷 X 时间线 → 只取 **10 小时内**热帖 → 按 **流速/曝光/互动 + 大V权重**算热度分 → 输出 **中文 Top 8-10 热榜**。纯只读，不点赞不关注不发布。

<p>

![Platform](https://img.shields.io/badge/Platform-Antigravity-7c3aed?style=flat-square)
![Window](https://img.shields.io/badge/Window-10h_only-ef4444?style=flat-square)
![Mode](https://img.shields.io/badge/Mode-Read--only-10b981?style=flat-square)
![Requires](https://img.shields.io/badge/Requires-browser_·_logged--in_X-0ea5e9?style=flat-square)

</p>

---

## ✨ 特点

| 特性 | 说明 |
| :--- | :--- |
| **⏱️ 10h 硬窗口** | 超过 10 小时的一律丢弃，支持 Snowflake ID 精确兜底算时间 |
| **🌊 流速优先** | 用小时流速捕捉刚起势的新帖，不唯粉丝论 |
| **👑 多维加权** | 综合曝光、互动率、大V 认证、新帖爆发力与原贴/论文链接 |
| **🧠 AI 相关性** | `ai-keywords.json` 初筛 + LLM 语义复判，过滤泛娱乐噪音 |
| **🈶 中文摘要** | 每条 1 句中文核心事实，保留英文产品/模型名，不写口水总结 |
| **🔒 纯只读** | 会话内直出榜单，不写文件、不点赞、不关注、不自动发文 |

---

## 🚀 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill x-ai-radar --global --yes
```

前置：Antigravity 环境 + `browser` 子代理可用 + X 已登录（未登录会提示登录地址，不会伪造数据）。

---

## 🗣️ 怎么用

在 Antigravity 中：

```text
/x-ai-radar
```

或直接说：

> `刷一下 X AI 热榜` / `自动追踪X热点` / `看看X上AI今天火什么` / `X timeline hot posts`

选出值得聊的热点后，可直接把条目交给 `chasen-x-writing` 按你的口吻写成快评或长帖。

---

## 🧠 机制概览

```text
browser 刷 x.com/home (或 AI List) ──► 10h 窗口过滤（支持 Snowflake ID 兜底）
        │
        ▼
门槛筛选 + 刷量降权 ──► 关键词初筛 + LLM 相关性复判 ──► 0-100 热度分排序取 Top 8-10
```

详细门槛、公式权重与异常处理见 [`SKILL.md`](./SKILL.md)。

---

## 📋 输出示例

```markdown
## 𝕏 AI 雷达 · 10h 热榜（2026-09-01 22:00 CST）

> 窗口：近 10 小时 | 候选 18 → 入榜 9 | 按热度分排序

| # | 热度分 | 作者 | 曝光/互动 | 流速 | 一句话摘要 | AI标签 |
|---|--------|------|-----------|------|------------|--------|
| 1 | 88 | 花叔 @huashu | 128k / 1.2k♡ 180↻ 95💬 | 18k/h | Grok 4.1 泄露的上下文窗口实测细节，工程侧关注 KV 缓存改动 | LLM |
| 2 | 79 | ... | ... | ... | ... | Agent |

**今日脉搏**：Agent 框架的本地化与低成本推理成为主线

**候选透视**：共抓 18，剔除 低热 6 / 非AI 3 / 超 10h 2
```

---

## 📂 目录

```text
x-ai-radar/
├── SKILL.md                      # Agent 执行契约（完整算法、门槛与边界）
├── README.md                     # 本文件
└── references/
    └── ai-keywords.json          # AI 关键词初筛表
```

---

## 📄 License

MIT © Chasen-Liao
