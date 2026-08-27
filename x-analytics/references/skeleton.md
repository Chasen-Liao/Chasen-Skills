# 报告骨架 — X Analytics 标准6段（通用）

> 用途：给 AI 和脚本的**版式参考**，不锁死文案。数据段全由 CSV 算出，手册建议按 `followers` 分阶段。

## Frontmatter（必含）

```yaml
---
title: "{period}深度挖掘：{span_days}天{total_impressions}曝光复盘"
date: "{end}"
tags: [review, analytics, deep-dive, "{月度复盘|每周复盘}"]
type: deep-dive
period: "{start}_{end}"
posts: {n}            # 总条数
orig_posts: {orig}    # 原创
reply_posts: {reply}  # 回复
impressions: {total}
source: "{csv_path}"
assets: "assets/"     # 或 Clog 的 03-Assets/{slug}/
---
```

## 正文6段

### 0. Abstract（3句话，不瞎写）

> 1. {span_days}天{total}曝光，均{avg}，Top1 {top1}是均值{multiple}倍
> 2. {top_topic}均{top_avg}最印钞，末位{bottom_topic}仅{bottom_avg}
> 3. 漏斗{detail_rate}%→{profile_rate}%→{follow_rate}%，主页→关注{home_to_follow}%

### 1. 日历：周级拆解

- 图：`01-daily.png`（>14天加 `02-weekly.png` 周对比）
- 表：`周 | 周期 | 帖数(原创) | 总曝光 | 均值 | Top`
- 按 7天切 W1-W4，最后一周不足7天也单列

### 2. 话题ROI（自动识别赛道）

- 图：`03-topic.png`
- 表：`话题 | 条数 | 总曝光 | 均值 | 收藏 | 收藏率`
- 逻辑：不写死 AI 8类；按 `--niche` 或 CSV 高频词自动聚类，`--topics` 传入则优先

### 3. 黄金档

- 图：`04-hourly.png`
- 剔除样本<5的小时，标 S/A/坑三档

### 4. 漏斗

- 图：`05-funnel.png`
- 文：`曝光 → 详情 x% → URL x% → 主页 x% → 关注 x% | 主页→关注 x%`

### 5. Top10

- 图：`06-top10.png`
- 表：`排名 | 曝光 | 日期 | 话题 | 钩子 | 互动`

### 6. 手册对标（按粉丝阶段）

- `0-1000` 冷启动：重互动，30%原创，5种大V互动法，引用 `handbook/04-如何和大V互动/`
- `1000-3000` 成长期：重内容，40/50/10 配比，日更20-25，引用 `handbook/08-日常如何发帖/`
- `3000+` 变现期：可接商单/创作者收益，引用 `handbook/05-怎么变现/`
- 另含：算法权重（06章）、连发检测（间隔1-2h）、价值分（带链接/收藏率）

---

## 交付

- `slug/ + assets/*.png`（lite 4图 / deep 6图自动切换）
- 参考版式：`D:/Com-Sci-Tech/Obsidian/Clog/每周复盘/2026-07-31_2026-08-27-深度挖掘.md`
