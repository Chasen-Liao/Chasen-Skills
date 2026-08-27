---
name: x-analytics
description: Use when 用户想复盘任意 X/Twitter 账号 — 丢 Content Analytics CSV，按 Snowflake 还原时间做话题/时段/漏斗分析，并结合《X增长手册》给做号建议
license: MIT
compatibility: Requires Python 3.10+ with matplotlib
metadata:
  author: Chasen-Liao
  version: "0.3.1"
  category: data-analysis
---

# X Analytics

> 丢个 `account_analytics_content_*.csv` 给 AI → 自动出报告 `YYYY-MM-DD_YYYY-MM-DD-深度挖掘.md + assets/*.png`，含数据分析 + 手册对标的做号建议。

## When to use

- 用户说 `分析X数据 / 复盘推文 / 看看账号 / 黄金时段 / 话题ROI` 或直接丢 CSV 路径
- 想要一份**数据分析 + 账号建议**的报告（不对口瞎写，只基于 CSV 和 `handbook/`）

## How to use

1. **拿数据**：用用户给的 CSV 路径；没给就找最新的 `*.csv`
2. **跑脚本**：`python scripts/x-analyze.py <csv> --out <目录> --followers <粉> --niche <赛道> --yes`
   - `--followers` 不给就问一句（默认 0），`--niche` 不给就自动识别赛道
   - `--topics` 可传自定义词表，`--lite/--deep` 可强制模式
3. **看报告**：检查 `<out>/YYYY-MM-DD_YYYY-MM-DD-*/.md` 和 `assets/*.png` 是否生成，用报告里的总览/话题/漏斗/手册对标四段做总结

```bash
python scripts/x-analyze.py "./account_analytics_content_2026-08-21_2026-08-27.csv" --out ./x-reports --followers 2800 --niche AI --yes
python scripts/x-analyze.py "./xxx.csv" --out ./x-reports --yes
```

## Output

- Markdown + 图表：周期、总量/均值、话题 ROI、黄金时段、漏斗、Top10（数据量大时自动加周对比/字数等）
- 末尾有《X增长手册》对标建议，按粉丝阶段给可执行清单，并标注引用的 `handbook/` 章节

想改输出样式？直接参考 `D:/Com-Sci-Tech/Obsidian/Clog/每周复盘/2026-07-31_2026-08-27-深度挖掘.md` 的版式，脚本生成的 Markdown 可在此基础上微调。

## References

- `references/skeleton.md` — 报告骨架（标准6段，自动识别赛道，按粉分阶段）
- `references/handbook/` — 8章手册原文，可 `git pull` 更新
- `references/topics.json` / `topics.generic.json` — 词表，可自定义或自动识别
- `references/metrics.md` / `csv-aliases.md` — 指标与列名容错说明

## Guardrails

- 缺 `Post id / Post text / Impressions` 直接报错
- 小时用 Snowflake `(id>>22)+1288834974657 → CST` 还原
- 只写本地，不自动 `git push`
