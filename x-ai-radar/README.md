# 📡 x-ai-radar

> Antigravity 专用 · 自动刷 X 时间线 → 只取 **10小时内**热帖 → 按 **流速/曝光/互动 + 大V权重**算热度分 → 输出 **中文 Top 8-10 热榜**。纯只读，不点赞不关注不发布。

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
| **⏱️ 10h 硬窗口** | 超过 10小时的一律丢弃，只追最新热度 |
| **🌊 流速优先** | `viewsPerHour / likesPerHour` 捕捉潜爆帖，不唯粉丝论 |
| **👑 大V加权** | 认证/≥10k 粉 +5分，`h≤2` 的 rising +8分，含论文/链接 +3分 |
| **🧠 AI 相关性** | `ai-keywords.json` 初筛 + LLM 复判 `high/medium/low`，只留 high/medium |
| **📊 热度分排序** | `log(Views)+Likes+Reposts+Replies+流速` 综合 0-100分 |
| **🈶 中文摘要** | 每条 1句中文核心事实，保留英文产品/模型名，不口水 |

---

## 🚀 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill x-ai-radar --global --yes
```

前置：Antigravity 环境 + `browser` 子代理可用 + X 已登录。未登录会直接报错并给 `https://x.com/login`。

---

## 🗣️ 怎么用

在 Antigravity 中：

```text
/x-ai-radar
```

或自然语言：

> `刷一下 X AI 热榜` / `自动追踪X热点` / `看看X上AI今天火什么` / `X timeline hot posts`

Skill 会自动唤起 `browser` 子代理刷时间线，会话内直出热榜，**不写文件、不发布**。

---

## 🔄 工作流

```text
阶段一：刷时间线（browser 子代理）
  x.com/home → 滚动抓 15-20条候选 → 记录 Views/Likes/Reposts/Replies/时间/作者 → 10h过滤

阶段二：过滤与打分
  硬门槛(二选一) → 大V/流速加权 → AI相关性复判 → heatScore排序 → 去重 → 取Top 8-10

阶段三：会话内输出
  Markdown 表格 + 今日脉搏一句话 + 候选透视
```

**硬门槛（二选一即过）**

| 类型 | 条件 |
| :--- | :--- |
| 英文/大盘 | `Views ≥ 30,000 且 Likes ≥ 200` |
| 中文/AI圈 | `Views ≥ 5,000 且 Likes ≥ 50` |
| 潜爆补偿 | `h≤2 且 (viewsPerHour≥5k 或 likesPerHour≥100) 且 Replies≥15` |

**热度分**

```text
heatScore = (log10(Views+1)*10 + Likes*0.4 + Reposts*0.8 + Replies*1.0 + viewsPerHour*0.02) / 10
# + 大V +5 / rising +8 / 含链接 +3
```

---

## 📋 输出示例

```markdown
## 𝕏 AI 雷达 · 10h 热榜（2026-09-01 22:00 CST）

> 窗口：近 10 小时 | 候选 18 → 入榜 9 | 按热度分排序

| # | 热度分 | 作者 | 曝光/互动 | 流速 | 一句话摘要 | AI标签 |
|---|--------|------|-----------|------|------------|--------|
| 1 | 88 | 花叔 @huashu | 128k / 1.2k♡ 180↻ 95💬 | 18k/h | Grok 4.1 泄露的上下文窗口实测细节... | LLM |
| 2 | 79 | ... | ... | ... | ... | Agent |

**今日脉搏**：Agent 框架的本地化与低成本推理成为主线

**候选透视**：共抓 18，剔除 低热 6 / 非AI 3 / 超 10h 2
```

---

## 📂 目录

```text
x-ai-radar/
├── SKILL.md                      # Agent 执行契约（含完整算法与边界）
├── README.md                     # 本文件
└── references/
    └── ai-keywords.json          # AI 关键词表（~60词，初筛用）
```

---

## 🚧 边界

- **只读**：严禁 `type_text / 点赞 / 转推 / 关注`，不产生任何写入
- **不凑数**：不足 8条就如实输出 N条 + 标注原因
- **去重**：按 `tweet id/url` 去重，同一作者多条爆帖只留最高分

---

## 📄 License

MIT © Chasen-Liao
