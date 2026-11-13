# 📊 x-analytics

> 丢一个 `account_analytics_content_*.csv` → 自动出 **Markdown 深度报告 + 4~6 张图**，含话题 ROI、黄金时段、转化漏斗，并按《X增长手册》给分阶段做号建议。

<p>

![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python&logoColor=white)
![Charts](https://img.shields.io/badge/Charts-matplotlib-ef4444?style=flat-square)
![Mode](https://img.shields.io/badge/Mode-lite_4_charts_·_deep_6_charts-f59e0b?style=flat-square)
![Output](https://img.shields.io/badge/Output-Markdown_+_PNG-10b981?style=flat-square)

</p>

---

## ✨ 能做什么

| 能力 | 说明 |
| :--- | :--- |
| **🕰️ 时间还原** | 用 Snowflake `id>>22` 还原发帖时间 → CST 小时分布，不依赖 CSV 的 `Date` 列 |
| **🏷️ 话题 ROI** | 按 `topics.json` 自动分类，算条数 / 总曝光 / 均值 / 收藏 / 收藏率，一眼看出高价值话题 |
| **⏰ 黄金时段** | 按小时聚合原创均值（优先过滤样本 `<5` 的时段），动态标出高均值与低均值窗口 |
| **🔻 转化漏斗** | `曝光 → 详情 → 链接 → 主页 → 关注` 全链路转化率与主页关注转化 |
| **📈 自适应深度** | `<100条且<=7天 lite（4图）/ 否则 deep（6图，追加 字数散点 + Top10 原创表与图）` |
| **📖 手册对标** | 结合 `references/handbook/` 8 章，按粉丝阶段（0-1k / 1k-3k / 3k+）动态生成可执行清单 |

---

## 🚀 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill x-analytics --global --yes
```

依赖：`Python 3.10+`，运行前需安装绘图依赖：

```bash
pip install -r x-analytics/scripts/requirements.txt
# 或使用 uv:
uv pip install matplotlib numpy
```

---

## 🗣️ 怎么用

### 在 Agent 中（推荐）

直接把 CSV 丢给 Agent，说：

> `分析一下这个 CSV` / `复盘一下 X 数据` / `看看黄金时段`

Agent 会自动调用 `scripts/x-analyze.py` 并把报告总结给你；若想把复盘洞察写成推文，可继续配合 `chasen-x-writing`。

### 命令行直接跑

```bash
# 最简 — 自动识别赛道、自动选输出目录
python x-analytics/scripts/x-analyze.py "./account_analytics_content_2026-08-21_2026-08-27.csv" --out ./x-reports --yes

# 指定粉丝数与赛道，手册建议更准
python x-analytics/scripts/x-analyze.py "./xxx.csv" --out ./x-reports --followers 2800 --niche AI --yes

# 强制深度/轻量
python x-analytics/scripts/x-analyze.py "./xxx.csv" --out ./x-reports --deep --yes
python x-analytics/scripts/x-analyze.py "./xxx.csv" --out ./x-reports --lite --yes

# 自定义话题词表
python x-analytics/scripts/x-analyze.py "./xxx.csv" --out ./x-reports --topics ./my-topics.json --yes
```

**参数**

| 参数 | 说明 |
| :--- | :--- |
| `csv` | CSV 路径，不传则自动探测当前目录或 `Downloads/` 最新 CSV |
| `--out` | 输出基目录，默认 `./x-reports/` |
| `--followers` | 当前粉丝数，影响手册分阶段建议 |
| `--niche` | 账号主方向，如 `AI` / `Vibe Coding` / `通用`，影响预设词表选择 |
| `--topics` | 自定义 `topics.json` 路径，优先级最高 |
| `--deep` / `--lite` | 强制 6 图 / 4 图 |
| `--yes` | 跳过交互询问，用默认值直接跑 |

---

## 📦 输出

```text
x-reports/
└── 2026-08-21_2026-08-27-深度挖掘/   # deep 含 6图，lite 为 "内容复盘" 4图
    ├── 2026-08-21_2026-08-27-深度挖掘.md
    └── assets/
        ├── 01-daily.png      # 日趋势（总量+均值）
        ├── 02-topic.png      # 话题 ROI
        ├── 03-hourly.png     # 小时黄金档（CST）
        ├── 04-funnel.png     # 转化漏斗
        ├── 05-length.png     # 字数 vs 曝光（仅 deep）
        └── 06-top10.png      # Top10 原创（仅 deep）
```

Markdown 结构：`总览 → 话题ROI → 转化漏斗 → 小时黄金档 → (Top10 原创) → 手册对标 → 下一步`

---

## 🧠 工作原理

```text
CSV ──► 列名容错(alias) ──► Snowflake还原CST ──► 话题分类(topics.json)
                                │
                                ▼
                    动态统计(日/话题/小时/漏斗) ──► 绘图(matplotlib) ──► Markdown 组装
                                │
                                ▼
                    按粉丝阶段对标 handbook/8章 → 可执行建议
```

- **列名容错**：`Post id / Post text / Impressions` 等大小写/别名自动归一，缺必选列直接报错
- **时间**：`(id >> 22) + 1288834974657 → UTC → CST`，与 `Date` 列偏差 `>1` 天会告警
- **话题**：`--topics` > 按 `niche` 选 `topics.json`（AI） / `topics.generic.json`（通用） > 兜底
- **手册**：`references/handbook/` 8 章原文随仓库分发，报告末尾按当前数据动态引用对应章节

---

## 📂 目录

```text
x-analytics/
├── SKILL.md                 # Agent 执行契约
├── README.md                # 本文件
├── scripts/
│   ├── x-analyze.py         # 主脚本
│   └── requirements.txt
└── references/
    ├── skeleton.md          # 报告骨架（版式与图表编号规范）
    ├── metrics.md           # 指标说明
    ├── csv-aliases.md       # 列名容错表
    ├── topics.json          # AI 赛道词表（含定制示例）
    ├── topics.generic.json  # 通用词表
    └── handbook/            # 《X增长手册》8章原文
```

---

## 💡 小技巧

- 想调话题分类？直接复制修改 `references/topics.json`（支持 `_note` 注释键），通过 `--topics` 传入即可
- 多账号？用 `--niche` 区分，报告会自动切换词表与手册话术
- 建议复盘后把高曝光写作规律同步到日常发帖，配合 `chasen-x-writing` 使用

---

## 📄 License

MIT © Chasen-Liao
