---
name: x-analytics
description: Use when 用户上传 X/Twitter CSV 或说“分析X数据 / 推文复盘 / x-analytics” — 丢数据给 AI，按规则脚本深度分析并给出做号建议。
license: MIT
compatibility: Requires Python 3.10+ with matplotlib. Writes report to ./x-reports/ by default.
metadata:
  author: Chasen-Liao
  version: "0.2.0"
  category: data-analysis
---

# X Analytics

> 把 `account_analytics_content_*.csv` 丢给 AI → 按写好的规则和脚本自动分析 → 给出黄金时段、发文节奏、话题等做号建议（建议来自 `references/handbook/` 8章）。

## When to use

- 用户说“分析X数据 / 复盘推文 / x-analytics”或直接给出 CSV 路径
- 想要黄金发布时间、日更节奏、话题 ROI、漏斗、藏在数据里的做号建议

## How to use (通用)

1. **丢数据**：把 CSV 路径给 AI（或拖入）。支持 `Post id` Snowflake 自动还原小时，无需手动填时间。
2. **AI 跑脚本**：`python scripts/x-analyze.py <csv> --out ./x-reports --followers <n> --niche <方向>`。未给 `followers/niche` 时先问一句（默认 0粉/AI），`--yes` 跳过。
3. **看报告**：`<out>/YYYY-MM-DD_YYYY-MM-DD-深度挖掘.md + assets/*.png`，含 4-6 张图与一节 `增长手册对标`，直接可发或入 Obsidian。

话题、指标、列名容错分别见 `references/topics.json` / `metrics.md` / `csv-aliases.md`，手册原文在 `references/handbook/` 可直接查询。

## Run

```bash
/x-analytics ./account_analytics_content_2026-08-21_2026-08-27.csv --out ./x-reports --followers 2800 --niche AI
python scripts/x-analyze.py "./xxx.csv" --out ./x-reports --yes
```

首次缺 `matplotlib` 会自动 `uv/pip install`。

## Output

- Markdown + 4图(lite<100条) / 6图(deep≥100条)：日趋势、话题、小时、漏斗，deep 加字数散点与 Top10
- 末尾按粉丝阶段（0-1000互动 / 1000-3000内容 / 3000+变现）与手册 06算法/08日常给出可执行清单，引 `handbook/` 原文路径

## References

- `handbook/` — 克隆自 `https://github.com/bozhouDev/x-growth-handbook`（8章，可直接查询，`git pull` 可更新）
- `topics.json` — 通用 8类（模型/Agent/Vibe Coding/产品/教程/行业/思考/其他）

## Guardrails

- 缺 `Post id/Post text/Impressions` 报错；小时必走 Snowflake，不走 `Date`
- 不自动 `git push`，只写本地
