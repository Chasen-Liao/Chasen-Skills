---
name: x-ai-radar
description: Antigravity 专用：自动追踪 X 热点 — 自动刷 X AI 时间线、10小时内大V/高流速热帖雷达，按曝光/互动/流速算热度分并输出中文 Top 榜。用户说 自动追踪X热点/刷X热榜/AI热榜/追X时间线/看看X上AI今天火什么/X timeline hot posts 或调用 /x-ai-radar 时务必使用，即使未显式提 skill 名
license: MIT
compatibility: Requires browser subagent + logged-in X session (Antigravity on-demand, read-only)
metadata:
  author: Chasen-Liao
  version: "0.1.0"
  category: research
---

# X AI Radar — Antigravity 专用 X 热点雷达

> 自动刷 X AI 时间线 → 只取 **10 小时内**最新热帖 → 按 **流速/曝光/互动 + 大V 权重**算热度分 → 输出 **中文 Top 8-10 热榜**。纯只读，不写作、不发布。

## 何时使用

- 想要一份 **10h 内 AI 相关、真实高热**的清单，而不是冷门帖（触发语见 description）

## 核心工作流（Antigravity 只读闭环）

### 阶段一：刷时间线（必须走 browser 子代理）

1. **唯一入口**：收到触发后 **必须直接 `invoke_subagent` 唤起 `browser` 子代理**（`TypeName: "browser"`），严禁主 Agent 手写临时 CDP 脚本绕过。
2. **进入 AI 时间线**：让子代理打开 `x.com/home`（用户日常的 AI 调教流；若用户有 AI List，优先进 List），等待首屏加载完成。
3. **滚动抓候选**：向下滚动时间线，抓 **15-20 条候选**，每条记录：
   - `url / 作者 DisplayName + @handle / 是否认证/大V / 粉丝数`
   - `发布时间 / 距今小时数 h`
   - `Views / Likes / Reposts / Replies / Bookmarks`
   - `是否有媒体/链接/引用`
4. **10 小时硬窗口**：`now - 发布时间 > 10h` 的一律丢弃，不纳入候选（宁缺毋滥）。
5. **算流速与互动**（子代理回传后主 Agent 计算）：
   - `viewsPerHour = Views / max(h, 0.5)`
   - `likesPerHour = Likes / max(h, 0.5)`
   - `engagementRate = (Likes + Reposts*2 + Replies*2) / Views`

### 阶段二：过滤与热度分（大V/高流速优先）

1. **硬门槛 + 速度补偿（二选一即过）**：
   - **英文/大盘**：`Views ≥ 30,000 且 Likes ≥ 200`
   - **中文/AI 圈**：`Views ≥ 5,000 且 Likes ≥ 50`
   - **潜爆补偿**（尤其新帖）：`h ≤ 2 且 (viewsPerHour ≥ 5,000 或 likesPerHour ≥ 100) 且 Replies ≥ 15` → 视为 rising，直接过
   - 未过门槛的一律剔除，子代理需继续下滚直到凑够候选
2. **账号与流速加权**：
   - 大V（认证 / 粉丝 ≥ 10k）直接加权
   - 非大V但 `viewsPerHour` 爆高也保留（病毒式传播），不唯粉丝论
   - 刷量号/广告号（`engagementRate < 0.001 且 Replies < 5`）降权剔除
3. **AI 相关性**（关键词初筛 + LLM 复判）：
   - 读 `references/ai-keywords.json` 做初筛（命中即 `maybe`）
   - 再让 LLM 判 `AI-relevance: high/medium/low`，只保留 `high/medium`（`vibe coding / cursor / agent / gemma / deepseek` 等隐式 AI 靠 LLM 捞回）
4. **热度分**（用于排序，量级 0-100）：
   ```
   heatScore = (log10(Views+1)*10 + Likes*0.4 + Reposts*0.8 + Replies*1.0 + viewsPerHour*0.02) / 10
   # 示例：80k Views / 600 Likes / 120 Reposts / 90 Replies / 20k views/h → 49+240+96+90+400=875 → /10 ≈ 88 分
   ```
   - 大V +5 分，`h ≤ 2` 的 rising +8 分，含原贴链接/论文 +3 分（均在 /10 后叠加）
   - 按 `heatScore` 降序取 **Top 8-10**
5. **去重**：按 `tweet id/url` 去重，同一作者 10h 内多条爆帖只保留最高分那条

### 阶段三：汇总输出（仅会话内）

- **不写文件、不发布、不点赞、不关注**，只在当前会话输出 Markdown
- 每条用 1 句中文概括 **核心事实**（不是口号），保留必要英文产品/模型名，不加 `#标签`，不当口水总结
- 按 `heatScore` 排序输出，末尾给 1 句今日 AI 圈趋势脉搏

**输出模板（严格按此）：**

```markdown
## 𝕏 AI 雷达 · 10h 热榜（YYYY-MM-DD HH:mm CST）

> 窗口：近 10 小时 | 候选 18 → 入榜 9 | 按热度分排序

| # | 热度分 | 作者 | 曝光/互动 | 流速 | 一句话摘要 | AI标签 |
|---|--------|------|-----------|------|------------|--------|
| 1 | 88 | 花叔 @huashu | 128k / 1.2k♡ 180↻ 95💬 | 18k/h | Grok 4.1 泄露的上下文窗口实测细节，工程侧关注 KV 缓存改动 | LLM |
| 2 | 79 | ... | ... | ... | ... | Agent |

**今日脉搏**：一句话总结今日最强的 1-2 个信号（例：Agent 框架的本地化与低成本推理成为主线）

**候选透视**：共抓 18，剔除 低热 6 / 非AI 3 / 超 10h 2
```

字段说明：`曝光/互动 = Views / Likes Reposts Replies`；`流速 = viewsPerHour`

## 边界与禁止

- **10 小时硬约束**：超过 10h 的帖不入榜，即使热度高
- **只读**：严禁 `type_text / 点赞 / 转推 / 关注`，本 skill 不产生任何写入
- **不写作**：不生成 Quote/Reply 草稿；如需写作请另行调用写作类 skill（如 `x-browser-automation`，若已安装）
- **未登录**：若子代理发现未登录，立即报错并给 `https://x.com/login`，不伪造数据
- **候选不足**：不足 8 条就如实输出 N 条 + 标注原因，不凑数

## References

- `references/ai-keywords.json` — AI 关键词表（约 60 词，LLM 复判前初筛）
