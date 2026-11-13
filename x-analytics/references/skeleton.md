# 报告骨架 — X Analytics 标准结构

> 用途：给 AI 和脚本的**版式参考**，不锁死文案。数据段全由 CSV 动态算出，手册建议按 `followers` 分阶段生成。

## Frontmatter（必含）

```yaml
---
title: "X 深度挖掘：{start} 至 {end}（{n}条，{depth}）"
date: {end}
period: "{start}_{end}"
posts: {n}
orig_posts: {orig}
impressions: {total}
source: "{csv_path}"
mode: "{depth}"
---
```

## 正文结构

### 0. 总览（Summary + 图表流）

- 关键指标：总帖数（原创 / 回复）、总曝光、均曝光、总点赞、总互动、0 曝光数
- 图表编号统一为 `01~06`（`lite` 生成 `01~04`，`deep` 追加 `05~06`）：
  - `01-daily.png`：日趋势（总量柱状 + 均值折线）
  - `02-topic.png`：话题 ROI
  - `03-hourly.png`：小时黄金档（CST）
  - `04-funnel.png`：转化漏斗
  - `05-length.png`：字数 vs 曝光散点（仅 `deep`）
  - `06-top10.png`：Top10 原创（仅 `deep`）

### 1. 话题 ROI（原创）

- 图：`02-topic.png`
- 表：`话题 | 条数 | 总曝光 | 均值 | 收藏 | 收藏率`
- 逻辑：不写死特定赛道；按 `--niche` 选 `topics.json`（AI）或 `topics.generic.json`（通用），传 `--topics` 时优先使用自定义词表

### 2. 转化漏斗

- 图：`04-funnel.png`
- 指标：`曝光 -> 详情 (x%) -> URL (x%) -> 主页 (x%) -> 关注 (x%) | 主页->关注 x%`

### 3. 小时黄金档（原创, CST）

- 图：`03-hourly.png`
- 逻辑：优先剔除样本 `<5` 的小时后按均值排序，动态输出高均值窗口与低均值窗口（全部由当前 CSV 实时计算，不硬编码固定时段）

### 4. Top10 原创（仅 `deep`）

- 图：`06-top10.png`
- 表：`排名 | 曝光 | 时间 (CST) | 话题 | 开头钩子 | 互动`

### 5. 增长手册对标（按粉丝阶段，`lite` 时为第 4 节）

- `0-1000` 冷启动：重互动，约 30% 原创，5 种大V互动法，引用 `handbook/04-如何和大V互动/`
- `1000-3000` 成长期：重内容，40/50/10 配比，日更 20-25，引用 `handbook/08-日常如何发帖/`
- `3000+` 变现期：可接商单/创作者收益，引用 `handbook/05-怎么变现/`
- 另含动态计算项：算法权重（06 章）、发帖间隔与连发检测（06 章）、带链/收藏率价值分（08 章）、话题集中度与信息源建议（07 章）

### 6. 下一步（`lite` 时为第 5 节）

- 若需调词表：改 `references/topics.json` 或传 `--topics` 重跑
- 若需将分析洞察写成推文/长文：调用 `chasen-x-writing`
