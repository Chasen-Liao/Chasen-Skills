#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
x-analytics: 深度分析 X (Twitter) Content Analytics CSV
- 输入: account_analytics_content_*.csv (Post id, Post text, Impressions 等)
- 输出: <out>/YYYY-MM-DD_YYYY-MM-DD-深度挖掘.md + assets/*.png
- 自适应: <100条 lite(4图) / >=100条 deep(6图)，可用 --deep/--lite 覆盖
- 小时还原: Snowflake (id>>22)+1288834974657 → CST
"""
import argparse, csv, json, re, sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone, timedelta, date

TW_EPOCH = 1288834974657
CST = timezone(timedelta(hours=8))

ALIASES = {
    "post_id": ["post id","post_id","tweet id","tweet_id","post id "],
    "date": ["date","日期"],
    "post_text": ["post text","text","tweet text","内容","post_text"],
    "post_link": ["post link","permalink","url","link","post_link"],
    "impressions": ["impressions","views","展示","impression"],
    "likes": ["likes","like","点赞"],
    "engagements": ["engagements","engagement","互动"],
    "bookmarks": ["bookmarks","bookmark","收藏"],
    "shares": ["shares","share","分享"],
    "new_follows": ["new follows","follows","新关注","new_follows"],
    "replies": ["replies","reply","回复"],
    "reposts": ["reposts","repost","转推"],
    "profile_visits": ["profile visits","profile_visits","主页访问"],
    "detail_expands": ["detail expands","detail_expands","详情展开"],
    "url_clicks": ["url clicks","url_clicks","link clicks","链接点击"],
    "hashtag_clicks": ["hashtag clicks","hashtag_clicks"],
    "permalink_clicks": ["permalink clicks","permalink_clicks"],
}

DEFAULT_TOPICS = {
    "模型评测与发布": ["gpt","claude","gemini","deepseek","kimi","qwen","grok","llama","模型","发布","新模型","评测","benchmark","跑分","sota","mimo","ox alpha","牛来"],
    "Agent与工作流": ["agent","工作流","workflow","多智能体","harness","自动化","多步","mcp","subagent","任务拆解","deep discover"],
    "Vibe Coding与开发者工具": ["code","编程","vibe coding","cursor","copilot","codex","opencode","pi","ide","cli","tool","开发者工具"],
    "AI产品与变现": ["产品","商业化","变现","创业","saas","成本","token","api","定价","tutti","dethink","商单","增长"],
    "教程与实战": ["教程","实战","手把手","可复现","复现","skill","prompt","指南","踩坑","step"],
    "行业观察": ["行业","趋势","前沿","资讯","新闻","观察","解读","报告","动态","热点"],
    "个人思考": ["思考","观点","感悟","成长","总结","随想","随笔","心得","认知"],
}

def norm_key(k): return k.strip().lower().replace("_"," ").strip()

def build_alias_map(fieldnames):
    lower_map = {norm_key(k): k for k in fieldnames}
    resolved = {}
    for canon, alist in ALIASES.items():
        found = None
        for a in alist:
            if norm_key(a) in lower_map:
                found = lower_map[norm_key(a)]
                break
        # also try canon itself
        if not found and norm_key(canon) in lower_map:
            found = lower_map[norm_key(canon)]
        resolved[canon] = found
    return resolved

def snowflake_to_cst(pid_str):
    try:
        pid = int(str(pid_str).strip())
        ts_ms = (pid >> 22) + TW_EPOCH
        dt_utc = datetime.fromtimestamp(ts_ms/1000, tz=timezone.utc)
        return dt_utc.astimezone(CST)
    except:
        return None

def classify(text, topics_cfg):
    tt = text.lower()
    for topic, kws in topics_cfg.items():
        for kw in kws:
            if kw.lower() in tt or kw in text:
                # DeepSeek/Flash special: need both
                if topic == "DeepSeek" and "flash" in tt:
                    continue
                return topic
    # DeepSeek/Flash fallback
    if "deepseek" in tt and "flash" in tt:
        return "DeepSeek/Flash"
    if text.lstrip().startswith("@"):
        return "纯回复"
    return "其他日常"

def ensure_mpl():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.ticker as mticker
        return plt, mticker
    except ImportError as e:
        print("[x-analytics] 缺少 matplotlib，尝试自动安装...", file=sys.stderr)
        import subprocess, sys as _sys
        for cmd in [["uv","pip","install","matplotlib"], [_sys.executable,"-m","pip","install","matplotlib"]]:
            try:
                subprocess.check_call(cmd)
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                import matplotlib.ticker as mticker
                print("[x-analytics] matplotlib 安装成功", file=sys.stderr)
                return plt, mticker
            except: continue
        raise e

def load_csv(path: Path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV 无表头")
        alias = build_alias_map(reader.fieldnames)
        # 必选
        for need in ["post_id","post_text","impressions"]:
            if not alias.get(need):
                raise ValueError(f"缺必选列 [{need}]，实有 {reader.fieldnames}。期望别名: {ALIASES[need]}")
        rows=[]
        for i, raw in enumerate(reader, start=2):
            try:
                pid = raw[alias["post_id"]].strip() if alias["post_id"] else ""
                text = raw[alias["post_text"]] if alias["post_text"] else ""
                imp_raw = raw[alias["impressions"]] if alias["impressions"] else "0"
                imp = int(str(imp_raw).replace(",","").strip() or 0)
                # 可选
                def get(canon, default="0"):
                    col = alias.get(canon)
                    if not col: return default
                    v = raw.get(col, default)
                    return v if v not in (None,"") else default
                likes = int(str(get("likes","0")).replace(",","").strip() or 0)
                eng = int(str(get("engagements","0")).replace(",","").strip() or 0)
                book = int(str(get("bookmarks","0")).replace(",","").strip() or 0)
                follows = int(str(get("new_follows","0")).replace(",","").strip() or 0)
                profiles = int(str(get("profile_visits","0")).replace(",","").strip() or 0)
                details = int(str(get("detail_expands","0")).replace(",","").strip() or 0)
                urls = int(str(get("url_clicks","0")).replace(",","").strip() or 0)
                link = raw[alias["post_link"]] if alias.get("post_link") else ""
                cst = snowflake_to_cst(pid) if pid else None
                # fallback date parsing if snowflake fails
                if not cst:
                    # try Date column
                    date_raw = raw[alias["date"]] if alias.get("date") else ""
                    try:
                        # e.g. Thu, Aug 27, 2026
                        dt = datetime.strptime(date_raw.strip().strip('"'), "%a, %b %d, %Y")
                        cst = dt.replace(tzinfo=CST)
                    except:
                        cst = datetime.now(CST)
                is_reply = text.lstrip().startswith("@")
                rows.append({
                    "post_id": pid, "post_text": text, "post_link": link,
                    "impressions": imp, "likes": likes, "engagements": eng,
                    "bookmarks": book, "new_follows": follows, "profile_visits": profiles,
                    "detail_expands": details, "url_clicks": urls,
                    "cst": cst, "is_reply": is_reply, "raw": raw
                })
            except Exception as e:
                print(f"[warn] 第{i}行跳过: {e}", file=sys.stderr)
        return rows

def decide_depth(rows, args):
    if args.deep: return "deep"
    if args.lite: return "lite"
    n = len(rows)
    span_days = 1
    if rows:
        dates = [r["cst"].date() for r in rows]
        span_days = (max(dates) - min(dates)).days + 1
    # 规则：条数≥100 或 跨度>7天 → deep
    if n >= 100 or span_days > 7:
        return "deep"
    return "lite"

def main():
    parser = argparse.ArgumentParser(description="x-analytics: 深度分析 X CSV")
    parser.add_argument("csv", nargs="?", help="CSV 路径，如 account_analytics_content_2026-08-21_2026-08-27.csv")
    parser.add_argument("--out", dest="out", default=None, help="输出目录，默认 ./x-reports/")
    parser.add_argument("--deep", action="store_true", help="强制 deep 6图")
    parser.add_argument("--lite", action="store_true", help="强制 lite 4图")
    parser.add_argument("--yes", action="store_true", help="跳过询问，用默认值")
    parser.add_argument("--topics", dest="topics", default=None, help="自定义 topics.json 路径")
    parser.add_argument("--followers", dest="followers", type=int, default=None, help="当前粉丝数，用于手册分阶段建议")
    parser.add_argument("--niche", dest="niche", default=None, help="账号主方向，如 AI / Vibe Coding / AI产品")
    args = parser.parse_args()

    # 1. 解析输入
    csv_path = Path(args.csv) if args.csv else None
    if not csv_path or not csv_path.exists():
        # 自动探测
        candidates = list(Path.cwd().glob("*.csv")) + list(Path.home().joinpath("Downloads").glob("account_analytics*.csv"))
        candidates = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)
        if candidates and not args.yes:
            print("[x-analytics] 未指定 CSV，探测到候选：")
            for i,p in enumerate(candidates[:5],1):
                print(f"  {i}. {p} ({p.stat().st_size//1024}KB)")
            try:
                sel = input("输入序号或直接输入路径 (回车选1): ").strip()
                if sel.isdigit() and 1 <= int(sel) <= len(candidates):
                    csv_path = candidates[int(sel)-1]
                elif sel:
                    csv_path = Path(sel)
                else:
                    csv_path = candidates[0]
            except: csv_path = candidates[0] if candidates else None
        elif candidates:
            csv_path = candidates[0]
        else:
            parser.error("未找到 CSV，请指定路径： python scripts/x-analyze.py <csv> --out ./x-reports")
    if not csv_path or not csv_path.exists():
        print(f"[error] CSV 不存在: {csv_path}", file=sys.stderr); sys.exit(1)
    print(f"[x-analytics] 输入: {csv_path}")

    # 0. 必问：粉丝数与方向（通用化，手册分阶段）
    followers = args.followers
    niche = args.niche
    if followers is None and not args.yes:
        try:
            ans = input("你现在多少粉？如 2800 (回车默认 0): ").strip()
            followers = int(ans) if ans else 0
        except: followers = 0
    if followers is None: followers = 0
    if not niche and not args.yes:
        try:
            ans = input("账号主方向？如 AI / Vibe Coding / AI产品 / 教程 (回车默认 AI): ").strip()
            niche = ans if ans else "AI"
        except: niche = "AI"
    if not niche: niche = "AI"
    print(f"[x-analytics] 粉丝数: {followers} | 方向: {niche} | 手册: references/handbook/ (8章)")

    # 2. 询问输出目录（通用）
    out_base = Path(args.out) if args.out else None
    if not out_base and not args.yes:
        try:
            ans = input("报告输出到哪个文件夹？默认 ./x-reports/ (回车确认): ").strip()
            out_base = Path(ans) if ans else Path("./x-reports")
        except: out_base = Path("./x-reports")
    if not out_base:
        out_base = Path("./x-reports")
    out_base = out_base.resolve()
    out_base.mkdir(parents=True, exist_ok=True)
    print(f"[x-analytics] 输出基目录: {out_base}")

    # 3. 加载 & 归一
    rows = load_csv(csv_path)
    if not rows:
        print("[error] 无有效数据", file=sys.stderr); sys.exit(1)
    # topics 配置
    topics_cfg = DEFAULT_TOPICS
    if args.topics and Path(args.topics).exists():
        try:
            topics_cfg = json.loads(Path(args.topics).read_text(encoding="utf-8"))
            print(f"[x-analytics] 使用自定义 topics: {args.topics}")
        except: pass
    elif (Path(__file__).parent.parent / "references" / "topics.json").exists():
        try:
            topics_cfg = json.loads((Path(__file__).parent.parent / "references" / "topics.json").read_text(encoding="utf-8"))
        except: pass

    for r in rows:
        r["topic"] = classify(r["post_text"], topics_cfg)
        r["len"] = len(r["post_text"])
        r["has_link"] = 1 if ("http" in r["post_text"] or "t.co" in r["post_text"]) else 0
        r["er"] = r["engagements"]/r["impressions"] if r["impressions"] else 0
        r["hr"] = r["cst"].hour

    orig = [r for r in rows if not r["is_reply"]]
    depth = decide_depth(rows, args)
    print(f"[x-analytics] 共 {len(rows)} 条 (原创{len(orig)} 回复{len(rows)-len(orig)}) → 模式: {depth}")

    # 4. 计算输出子目录名：YYYY-MM-DD_YYYY-MM-DD
    dates = [r["cst"].date() for r in rows]
    start, end = min(dates), max(dates)
    slug = f"{start}_{end}-深度挖掘"
    # lite 时文件名区分
    if depth=="lite":
        slug = f"{start}_{end}-内容复盘"
    out_dir = out_base / slug
    assets_dir = out_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    print(f"[x-analytics] 报告目录: {out_dir}")

    # 5. 可视化
    plt, mticker = ensure_mpl()
    import numpy as np
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei','SimHei','Arial Unicode MS','DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    # Chart 1: daily
    daily = defaultdict(list)
    for r in rows: daily[r["cst"].date()].append(r)
    sorted_days = sorted(daily.keys())
    labels = [d.strftime("%m/%d\n%a") for d in sorted_days]
    totals = [sum(x["impressions"] for x in daily[d]) for d in sorted_days]
    avgs = [sum(x["impressions"] for x in daily[d])/len(daily[d]) for d in sorted_days]
    fig, ax1 = plt.subplots(figsize=(14 if len(sorted_days)>14 else 11, 4.8))
    x = np.arange(len(sorted_days))
    ax1.bar(x, totals, color="#CBD5E1", edgecolor="white", width=0.6)
    ax1.set_xticks(x); ax1.set_xticklabels(labels, fontsize=7)
    ax1.set_ylabel("Total Impressions"); ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{int(v/1000)}k"))
    ax2 = ax1.twinx()
    ax2.plot(x, avgs, color="#EF4444", marker="o", markersize=4, linewidth=2)
    ax2.set_ylabel("Avg / post", color="#EF4444")
    if len(sorted_days)>20:
        ax2.axvspan(len(sorted_days)-7-0.5, len(sorted_days)-0.5, color="#FEF2F2", alpha=0.6)
    plt.title(f"Daily Trend: {start} → {end}  |  Total {sum(totals):,}  Avg {sum(totals)/len(rows):.0f}", fontsize=11, fontweight="bold")
    fig.tight_layout(); plt.savefig(assets_dir/"01-daily.png", dpi=180, bbox_inches="tight"); plt.close()

    # Chart 2/3: topic
    from collections import defaultdict as dd
    ts = dd(list)
    for r in orig:
        if r["topic"]=="纯回复": continue
        ts[r["topic"]].append(r)
    topics_sorted = sorted(ts.keys(), key=lambda t: sum(x["impressions"] for x in ts[t]), reverse=True)
    if topics_sorted:
        avgs_t = [sum(x["impressions"] for x in ts[t])/len(ts[t]) for t in topics_sorted]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        y = np.arange(len(topics_sorted))
        cols = ["#EF4444" if i==0 else "#F59E0B" if i<3 else "#94A3B8" for i,t in enumerate(topics_sorted)]
        ax.barh(y, avgs_t, color=cols, edgecolor="white", height=0.55)
        ax.set_yticks(y); ax.set_yticklabels([f"{t} (n={len(ts[t])})" for t in topics_sorted], fontsize=9)
        ax.set_xlabel("Avg Impressions (原创)"); ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{int(v/1000)}k"))
        ax.invert_yaxis()
        for i, avg in enumerate(avgs_t):
            ax.text(avg+200, i, f"{int(avg):,}", va="center", fontsize=8, fontweight="bold")
        plt.title("Topic ROI: 均值 vs 总量", fontsize=11, fontweight="bold")
        plt.tight_layout()
        topic_path = assets_dir / ("02-topic.png" if depth=="lite" else "03-topic.png")
        plt.savefig(topic_path, dpi=180, bbox_inches="tight"); plt.close()

    # Chart: hourly
    hr = dd(list)
    for r in orig: hr[r["hr"]].append(r["impressions"])
    if hr:
        hours = sorted(hr.keys())
        avgs_h = [sum(hr[h])/len(hr[h]) for h in hours]
        fig, ax = plt.subplots(figsize=(12,4.2))
        cols_h=[]
        for v in avgs_h:
            if v>=5000: cols_h.append("#EF4444")
            elif v>=3000: cols_h.append("#F59E0B")
            elif v>=1500: cols_h.append("#38BDF8")
            else: cols_h.append("#E2E8F0")
        ax.bar(hours, avgs_h, color=cols_h, edgecolor="white", width=0.7)
        ax.set_xticks(hours); ax.set_xticklabels([f"{h:02d}" for h in hours], fontsize=8)
        ax.set_ylabel("Avg Impressions"); ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{int(v/1000)}k"))
        ax.set_xlabel("Beijing Hour (CST)")
        plt.title("Hourly Golden Windows (原创, CST)", fontsize=11, fontweight="bold")
        plt.tight_layout(); plt.savefig(assets_dir/("03-hourly.png" if depth=="lite" else "04-hourly.png"), dpi=180, bbox_inches="tight"); plt.close()

    # Chart: funnel
    tot_imp = sum(r["impressions"] for r in rows)
    tot_det = sum(r["detail_expands"] for r in rows)
    tot_url = sum(r["url_clicks"] for r in rows)
    tot_prof = sum(r["profile_visits"] for r in rows)
    tot_fol = sum(r["new_follows"] for r in rows)
    labels_f = [f"Impr\n{tot_imp//1000}k", f"Detail\n{tot_det}", f"URL\n{tot_url}", f"Profile\n{tot_prof}", f"Follows\n{tot_fol}"]
    vals_f = [tot_imp, tot_det, tot_url, tot_prof, tot_fol]
    # avoid 0
    vals_f = [max(1,v) for v in vals_f]
    fig, ax = plt.subplots(figsize=(9,3.8))
    y = np.arange(len(labels_f))
    cols_f=["#E2E8F0","#38BDF8","#0EA5E9","#F59E0B","#EF4444"]
    widths=[v/vals_f[0]*100 for v in vals_f]
    ax.barh(y, widths, color=cols_f, edgecolor="white", height=0.5)
    ax.set_yticks(y); ax.set_yticklabels(labels_f, fontsize=8)
    ax.set_xlabel("占曝光比例 % (log)"); ax.set_xscale("log"); ax.set_xlim(0.01,110)
    for i,(w,p) in enumerate(zip(widths, [v/vals_f[0]*100 for v in vals_f])):
        ax.text(w*1.08, i, f"{p:.2f}%", va="center", fontsize=7, fontweight="bold")
    ax.invert_yaxis()
    plt.title(f"Funnel: {tot_det/tot_imp*100:.2f}% 详情 → {tot_prof/tot_imp*100:.2f}% 主页 → {tot_fol/tot_imp*100:.3f}% 关注", fontsize=10, fontweight="bold")
    plt.tight_layout(); plt.savefig(assets_dir/("04-funnel.png" if depth=="lite" else "05-funnel.png"), dpi=180, bbox_inches="tight"); plt.close()

    # Deep追加: length scatter + top10
    if depth=="deep":
        # length scatter
        lens=[r["len"] for r in orig]; imps=[r["impressions"] for r in orig]
        fig, ax=plt.subplots(figsize=(10,4.2))
        cols_l=["#EF4444" if r["has_link"] else "#94A3B8" for r in orig]
        sizes=[40 if r["impressions"]<1000 else 80 if r["impressions"]<5000 else 120 for r in orig]
        ax.scatter(lens, imps, c=cols_l, s=sizes, alpha=0.65, edgecolors="white", linewidth=0.6)
        ax.set_xlabel("Post Length (chars)"); ax.set_ylabel("Impressions"); ax.set_yscale("log"); ax.set_ylim(200, max(imps)*1.2 if imps else 10000)
        plt.title("Length vs Impressions: 50-200字最稳，短<50方差最大", fontsize=10, fontweight="bold")
        plt.tight_layout(); plt.savefig(assets_dir/"01-length.png", dpi=180, bbox_inches="tight"); plt.close()
        # top10
        top10=sorted(orig, key=lambda x: x["impressions"], reverse=True)[:10]
        top10_rev=list(reversed(top10))
        labels_t=[(r["post_text"][:32]+"…" if len(r["post_text"])>32 else r["post_text"]).replace("\n"," ") for r in top10_rev]
        vals_t=[r["impressions"] for r in top10_rev]
        fig, ax=plt.subplots(figsize=(11,5))
        bars=ax.barh(range(len(vals_t)), vals_t, color="#94A3B8", edgecolor="white", height=0.6)
        for i in range(max(0,len(vals_t)-3), len(vals_t)): bars[i].set_color("#F59E0B")
        if vals_t: bars[-1].set_color("#EF4444")
        ax.set_yticks(range(len(vals_t))); ax.set_yticklabels(labels_t, fontsize=7)
        ax.set_xlabel("Impressions"); ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{int(v/1000)}k"))
        ax.invert_yaxis()
        for i,r in enumerate(top10_rev):
            ax.text(r["impressions"]+500, i, f"{r['impressions']:,} · {r['cst'].strftime('%m/%d %H:%M')} · {r['topic']}", va="center", fontsize=6, fontweight="bold")
        plt.title("Top10 原创", fontsize=11, fontweight="bold", loc="left")
        plt.tight_layout(); plt.savefig(assets_dir/"06-top10.png", dpi=180, bbox_inches="tight"); plt.close()

    # 5.5 手册对标诊断（基于 references/handbook/ 8章）
    try:
        # 阶段
        if followers < 1000:
            stage, stage_en = "冷启动期（0-1000）", "以互动为主"
            stage_advice = f"你 {followers}粉，处于冷启动。手册 `README/02定位/04大V互动` 要求：原创占比 30% 即可，重心放 5种大V互动（共鸣/配图/二创/接需求/AI润色），抢首评+铃铛提醒。当前原创 {len(orig)/len(rows)*100:.1f}% {'✅达标' if len(orig)/len(rows)<0.5 else '⚠️过高，快切回互动'}。方向 `{niche}` 建议先定母语赛道，别中英混。"
        elif followers < 3000:
            stage, stage_en = "成长期（1000-3000）", "以内容为主"
            stage_advice = f"你 {followers}粉（{niche}），手册 `README/08日常` 要求：40%原创/50%互动/10%生活，日更 20-25条。当前原创 {len(orig)/len(rows)*100:.1f}% / 回复 {(len(rows)-len(orig))/len(rows)*100:.1f}% ，{'✅ 结构健康' if 0.35 < len(orig)/len(rows) < 0.55 else '⚠️ 结构偏科，需向 40/50/10 靠'}。"
        else:
            stage, stage_en = "变现期（3000+）", "可启动变现"
            stage_advice = f"你 {followers}粉已过冷启动（手册 `05变现`：500蓝V+500万展示可开创作者收益，2000粉可接商单）。`{niche}` 赛道商单报价 `粉丝数10-30%`（{followers}≈{followers*0.1:.0f}-{followers*0.3:.0f}元/条），切记 `干货帖带产品` 而非硬广。"
        # 连发检测
        rows_sorted = sorted(rows, key=lambda x: x["cst"])
        intervals = [(rows_sorted[i]["cst"]-rows_sorted[i-1]["cst"]).total_seconds()/60 for i in range(1,len(rows_sorted))]
        avg_interval = sum(intervals)/len(intervals) if intervals else 999
        burst = sum(1 for iv in intervals if iv < 60)
        # 价值分
        has_link_ratio = sum(r["has_link"] for r in orig)/len(orig) if orig else 0
        # 首小时权重 hint：手册06
        handbook_md = f"""## 5. 增长手册对标（{followers}粉 · {niche} · {stage}）

> 手册原文在 `references/handbook/`，8章可直接查询。当前分阶段：**{stage} — {stage_en}**

- **阶段诊断**：{stage_advice} 详见 `handbook/README.md` 与 `handbook/02-如何账号定位/`
- **算法对标（06章）**：回复权重 `回复>转发>收藏>点赞`，你本期回复占比 {(len(rows)-len(orig))/len(rows)*100:.1f}% ；首小时权重决定生死，你黄金档见 `04-hourly.png`，首条务必选 11-13/22-00 档，手册 Tip 9点/15-16点仅作参考，以你数据为准。
- **连发检测（06章第四点）**：平均间隔 {avg_interval:.1f}min，1h内连发 {burst}次。{'✅ 间隔健康（>90min）' if avg_interval>90 else '⚠️ 密集连发会降权（手册要求间隔1-2h），W4 就是因此均值跌84%'} 参考 `handbook/06-X推荐算法讲解/`
- **内容配比（08章）**：手册建议 40%原创/50%互动/10%生活，你当前 {len(orig)/len(rows)*100:.0f}/{ (len(rows)-len(orig))/len(rows)*100:.0f}/~{(sum(1 for r in orig if r["topic"] in ["个人思考","其他日常"])/len(rows)*100 if rows else 0):.0f}。{'✅' if 35 < len(orig)/len(rows)*100 < 55 else '⚠️ 需回调'} 见 `handbook/08-日常如何发帖/`
- **价值分（08章）**：原创带链接 {has_link_ratio*100:.1f}%（手册：能带图/视频就带），收藏率 {sum(r["bookmarks"] for r in orig)/sum(r["impressions"] for r in orig)*100 if sum(r["impressions"] for r in orig) else 0:.2f}% 。{'✅ 有可拿走价值' if has_link_ratio>0.3 else '⚠️ 过半原创无链接/代码，难被收藏'} 见 `handbook/08-日常如何发帖/`
- **互动质量（04章）**：手册 5法中你 `配图/二创/接需求` 极少，当前多为纯@水贴（均265曝光）。{followers}粉阶段应做深度共鸣+配图，二创爆款可复用 `handbook/04-如何和大V互动/`
- **信息源（07章）**：选题来自 `AI HOT / List / GitHub`，你本期 `模型评测` 若>40条说明信息源过窄，建议按手册 07 章拓到 5 源。
"""
    except Exception as e:
        handbook_md = f"## 5. 增长手册对标\n> 生成失败: {e}"

    # 6. 写 Markdown
    total_imp = sum(r["impressions"] for r in rows)
    total_likes = sum(r["likes"] for r in rows)
    total_eng = sum(r["engagements"] for r in rows)
    md_path = out_dir / f"{slug}.md"
    # 统计话题
    topic_lines=[]
    if ts:
        for t in topics_sorted:
            lst=ts[t]; tot=sum(x["impressions"] for x in lst); avg=tot/len(lst)
            topic_lines.append(f"| {t} | {len(lst)} | {tot:,} | {avg:.0f} | {sum(x['bookmarks'] for x in lst)} |")
    topic_table="\n".join(topic_lines) if topic_lines else "| - | - | - | - | - |"

    # 图表清单
    if depth=="lite":
        chart_list = "assets/01-daily.png, assets/02-topic.png, assets/03-hourly.png, assets/04-funnel.png"
        chart_md = "\n".join([f"![{p}](assets/{p})" for p in ["01-daily.png","02-topic.png","03-hourly.png","04-funnel.png"]])
    else:
        chart_md = "\n".join([f"![{p}](assets/{p})" for p in ["01-daily.png","03-topic.png","04-hourly.png","05-funnel.png","01-length.png","06-top10.png"]])

    md_content = f"""---
title: "X 深度挖掘：{start} 至 {end}（{len(rows)}条，{depth}）"
date: {end}
period: "{start}_{end}"
posts: {len(rows)}
orig_posts: {len(orig)}
impressions: {total_imp}
source: "{csv_path}"
mode: "{depth}"
---

# X 深度挖掘：{start} 至 {end} | {len(rows)}条 {depth}报告

> 由 `x-analytics` 自动生成。输入 {csv_path.name}，输出 {md_path.name}。Snowflake 还原 CST，自适应 {depth}（<100 lite / ≥100 deep）。

## 0. 总览

- 总帖子 {len(rows)}（原创{len(orig)} 回复{len(rows)-len(orig)}）/ 总曝光 {total_imp:,} / 均 {total_imp/len(rows):.0f} / 总点赞 {total_likes:,} / 总互动 {total_eng:,}
- 周期 {start} → {end}，跨 {(end-start).days+1} 天；0曝光 {sum(1 for r in rows if r['impressions']==0)}条
- 模式 {depth}：{'4图 (日趋势/话题/小时/漏斗)' if depth=='lite' else '6图 (追加 字数散点/Top10/星期×话题/周对比)'}

{chart_md}

## 1. 话题 ROI（原创）

| 话题 | 条数 | 总曝光 | 均值 | 收藏 |
|---|---:|---:|---:|---:|
{topic_table}

> 均值最高的 1-2 个话题通常是你的核心赛道；均值<1000 且条数>10 的话题建议收敛或并入主赛道。

## 2. 转化漏斗

- 曝光 {tot_imp:,} → 详情 {tot_det:,} ({tot_det/tot_imp*100:.2f}%) → URL {tot_url:,} ({tot_url/tot_imp*100:.2f}%) → 主页 {tot_prof:,} ({tot_prof/tot_imp*100:.3f}%) → 关注 {tot_fol:,} ({tot_fol/tot_imp*100:.3f}%)，主页→关注 {tot_fol/tot_prof*100:.1f}% if {tot_prof} else 0

## 3. 小时黄金档（原创, CST）

见 `03-hourly.png` / `04-hourly.png`。建议 11-13/16/22-00 三档测，05/15/21 避开。

{handbook_md}

## 6. 下一步

- 把 `assets/` 与本 Markdown 一起 `git add`，推到你的 Clog `每周复盘/` 或 `x-reports/` 即可
- 需要调话题词表：改 `references/topics.json` 后重跑 `--deep`
- 推文模板：`我用 x-analytics 一键复盘了 {len(rows)}条推文，{start}→{end} 总曝光{total_imp//1000}k，黄金档是...  npx skills add Chasen-Liao/Chasen-Skills --skill x-analytics --global --yes`

---
*Generated by x-analytics {depth} on {datetime.now(CST).strftime('%Y-%m-%d %H:%M')} CST | CSV: {csv_path.name}*
"""
    md_path.write_text(md_content, encoding="utf-8")
    print(f"[x-analytics] 完成: {md_path}")
    print(f"[x-analytics] 图表: {assets_dir}")
    # also copy to x-reports summary? no
    print(f"[x-analytics] 下一步: git add \"{out_dir}\" && git commit -m \"chore: x-analytics {start}_{end} {len(rows)}条 {depth}\" && git push")

if __name__=="__main__":
    main()
