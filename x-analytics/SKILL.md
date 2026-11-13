---
name: x-analytics
description: 用户想复盘任意 X/Twitter 账号时使用 — 传入 Content Analytics CSV，按 Snowflake 还原 CST 时间做话题 ROI、黄金时段与转化漏斗分析，并结合《X增长手册》按粉丝阶段给出做号建议
license: MIT
compatibility: Requires Python 3.10+ with matplotlib and numpy (pip install -r scripts/requirements.txt)
metadata:
  author: Chasen-Liao
  version: "0.4.0"
  category: data-analysis
---

# X Analytics

> 丢个 `account_analytics_content_*.csv` 给 AI → 自动出报告 `YYYY-MM-DD_YYYY-MM-DD-{内容复盘|深度挖掘}.md + assets/*.png`，含动态数据分析 + 手册对标的做号建议。

## When to use

- 用户说 `分析X数据 / 复盘推文 / 看看账号 / 黄金时段 / 话题ROI` 或直接给出 CSV 路径
- 想要一份**数据分析 + 账号建议**的报告（只基于 CSV 实时计算与 `references/handbook/`，不编造指标）

## How to use

1. **拿数据**：使用用户提供的 CSV 路径；未提供则按修改时间寻找最新的 `*.csv`
2. **跑脚本**：`python scripts/x-analyze.py <csv> --out <目录> --followers <粉> --niche <赛道> --yes`
   - `--followers` 未提供则询问一次（默认 `0`），`--niche` 未提供可自动选通用或 AI 赛道
   - `--topics` 可传自定义词表，`--lite/--deep` 可强制模式（默认 `<100` 条且跨度 `<=7` 天为 `lite` 4 图，否则 `deep` 6 图）
   - 若缺 `matplotlib` / `numpy`，提示用户运行 `pip install -r scripts/requirements.txt`（不要静默改系统环境）
3. **看报告**：检查 `<out>/YYYY-MM-DD_YYYY-MM-DD-*/` 下的 Markdown 与 `assets/01~06*.png` 是否生成，总结总览、话题 ROI、黄金时段、漏斗与手册对标建议

```bash
python scripts/x-analyze.py "./account_analytics_content_2026-08-21_2026-08-27.csv" --out ./x-reports --followers 2800 --niche AI --yes
python scripts/x-analyze.py "./xxx.csv" --out ./x-reports --yes
```

## Output

- Markdown + 图表（`01-daily.png`、`02-topic.png`、`03-hourly.png`、`04-funnel.png`，`deep` 追加 `05-length.png`、`06-top10.png`）
- 末尾附《X增长手册》动态对标诊断，按粉丝阶段给可执行清单，并标注引用的 `handbook/` 章节；若用户希望将复盘洞察转成推文，可引导调用 `chasen-x-writing`
- 若需调整输出版式，可参考 `references/skeleton.md`

## References

- `references/skeleton.md` — 报告骨架（标准段落与图表编号规范）
- `references/handbook/` — 《X增长手册》8 章原文
- `references/topics.json` / `topics.generic.json` — AI / 通用词表，支持 `--topics` 自定义覆盖
- `references/metrics.md` / `csv-aliases.md` — 指标定义与列名容错说明

## Guardrails

- 缺 `Post id / Post text / Impressions` 直接报错
- 小时必须用 Snowflake `(id>>22)+1288834974657 -> CST` 还原
- 报告内所有结论、时段、均值必须来自当次 CSV 实算，禁止套用历史硬编码数字
- 只写本地，不自动 `git push`
