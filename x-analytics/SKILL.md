---
name: x-analytics
description: Use when 用户上传 X/Twitter CSV 或说“分析X数据 / 推文复盘 / x-analytics” — 深度分析 𝕏 账号数据，输出 Markdown 报告与可视化图表。
license: MIT
compatibility: Requires Python 3.10+ with matplotlib. Writes report to ./x-reports/ by default. Network not required.
metadata:
  author: Chasen-Liao
  version: "0.1.0"
  category: data-analysis
---

# X Analytics — 深度分析 𝕏 账号数据

> 用户上传 `account_analytics_content_*.csv` → 自动清洗 → 解码 Snowflake 还原发布时间 → 话题/漏斗/时段挖掘 → 生成带图表的 Markdown 报告。

## When to use

- 用户说“分析X数据”“推文复盘”“x-analytics”或直接拖入/给出 CSV 路径
- 有 `Post id, Date, Post text, Post Link, Impressions, Likes, Engagements...` 的 X Content Analytics 导出
- 想要日趋势、黄金发布时间、话题 ROI、转化漏斗、隐藏宝石等深度结论

## Inputs

- **必需**：CSV 路径（`Post id` + `Post text` + `Impressions` 至少3列）。列名大小写/中英兼容，`Post id` 用于 Snowflake 解小时。
- **可选**：`--out <dir>` 输出目录（不给则运行时询问，默认 `./x-reports/`）、`--deep/--lite` 强制深度、`--yes` 跳过询问

## Workflow

1. **Load & Normalize**：`utf-8-sig` 读、别名归一化（`Post id/Tweet id/帖子ID`）、数值清洗、Snowflake `(id>>22)+1288834974657` → CST、判 `is_reply`、`has_link`、`topic`
2. **Decide Depth**：无旗标时按条数自适应 — `<100条 → lite(4图)` / `≥100条 → deep(6图)`。`--deep/--lite` 可覆盖
3. **Analyze**：日/周趋势、小时均值与命中率、话题总/均/收藏、漏斗 `曝光→详情→主页→关注`、字数/链接相关性、星期×话题热力图（deep）
4. **Visualize**：`matplotlib Agg` 生成 `01-daily.png .. 06-top10.png` 到 `<out>/assets/`
5. **Report**：写 `<out>/YYYY-MM-DD_YYYY-MM-DD-深度挖掘.md`，含 frontmatter `period/posts/impressions` + 5-6章 + 图表相对路径

## Output

```
<out>/
  YYYY-MM-DD_YYYY-MM-DD-深度挖掘.md   # 主报告，frontmatter 可直接入 Obsidian 每周复盘
  assets/
    01-daily.png      # 日总量 vs 均值
    02-weekly.png     # 周总量 vs 均值（deep 且跨周时）
    03-topic.png      # 话题均值 vs 总量
    04-hourly.png     # 小时黄金档
    05-funnel.png     # 转化漏斗
    06-top10.png      # Top10 原创
    03-length.png / 05-weekday-topic.png  # deep 追加
```

图片用 `![...](assets/01-daily.png)` 相对路径，Obsidian 与 GitHub 均可渲染。

## Run

```bash
# 方式A：Pi Skill 触发（推荐）
/x-analytics C:/Users/Chasen/Downloads/account_analytics_content_2026-08-21_2026-08-27.csv --out ./x-reports --yes

# 方式B：直接跑脚本
python scripts/x-analyze.py "C:/path/to/csv" --out ./x-reports --deep
python scripts/x-analyze.py --help
```

首次运行若缺 `matplotlib`，脚本会提示并尝试 `uv pip install matplotlib` / `pip install matplotlib`。

## References

- `references/topics.json` — 话题分类词表（可改，不改即用内置 Pi/Harness 等8类）
- `references/metrics.md` — 指标定义（ER/BR/PR/漏斗）
- `references/csv-aliases.md` — 列名别名与容错

## Guardrails

- 列名做 `lower().strip()` 别名匹配，缺 `Post id/Impressions/Post text` 时报错提示期望列
- `Post text` 必须用 `csv` 模块解析（引号/逗号/emoji/t.co）
- 小时不走 `Date` 列，必须走 Snowflake，校验 `abs(解码日期 - Date) ≤1天`
- `0曝光` 标 `pending` 参与计数但单拎提示
- 不自动 `git push`，首版只写本地，用户自行 push
