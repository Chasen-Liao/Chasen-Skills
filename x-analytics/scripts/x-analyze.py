#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
x-analytics: 深度分析 X (Twitter) Content Analytics CSV
- 输入: account_analytics_content_*.csv (Post id, Post text, Impressions 等)
- 输出: <out>/YYYY-MM-DD_YYYY-MM-DD-{内容复盘|深度挖掘}.md + assets/*.png
- 自适应: <100条且跨度<=7天 lite(4图) / 否则 deep(6图)，可用 --deep/--lite 覆盖
- 小时还原: Snowflake (id>>22)+1288834974657 -> CST
"""
import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

TW_EPOCH = 1288834974657
CST = timezone(timedelta(hours=8))

ALIASES = {
    "post_id": ["post id", "post_id", "tweet id", "tweet_id"],
    "date": ["date", "日期"],
    "post_text": ["post text", "text", "tweet text", "内容", "post_text"],
    "post_link": ["post link", "permalink", "url", "link", "post_link"],
    "impressions": ["impressions", "views", "展示", "impression"],
    "likes": ["likes", "like", "点赞"],
    "engagements": ["engagements", "engagement", "互动"],
    "bookmarks": ["bookmarks", "bookmark", "收藏"],
    "shares": ["shares", "share", "分享"],
    "new_follows": ["new follows", "follows", "新关注", "new_follows"],
    "replies": ["replies", "reply", "回复"],
    "reposts": ["reposts", "repost", "转推"],
    "profile_visits": ["profile visits", "profile_visits", "主页访问"],
    "detail_expands": ["detail expands", "detail_expands", "详情展开"],
    "url_clicks": ["url clicks", "url_clicks", "link clicks", "链接点击"],
    "hashtag_clicks": ["hashtag clicks", "hashtag_clicks"],
    "permalink_clicks": ["permalink clicks", "permalink_clicks"],
}


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def _load_json_topics(path: Path):
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            return None
        # 过滤 _note / _comment 等元信息字段，只保留话题 -> 关键词列表映射
        cleaned = {
            k: v
            for k, v in raw.items()
            if not k.startswith("_") and isinstance(v, list)
        }
        return cleaned or None
    except Exception as e:
        print(f"[warn] 话题词表加载失败 {path}: {e}", file=sys.stderr)
        return None


def load_topics_cfg(args, niche: str):
    # 1. --topics 最高优先
    if args.topics and Path(args.topics).exists():
        cfg = _load_json_topics(Path(args.topics))
        if cfg:
            print(f"[x-analytics] 使用自定义 topics: {args.topics}")
            return cfg
    # 2. 按 niche 自动选预设（AI vs 通用）
    is_ai = False
    if niche:
        low = niche.lower()
        is_ai = any(k in low for k in ["ai", "agent", "vibe", "code", "模型", "编程", "大模型"])
    base = Path(__file__).parent.parent / "references"
    ai_path = base / "topics.json"
    generic_path = base / "topics.generic.json"
    chosen = ai_path if is_ai else generic_path
    if not chosen.exists():
        chosen = generic_path if chosen == ai_path else ai_path
    cfg = _load_json_topics(chosen) if chosen.exists() else None
    if cfg:
        print(f"[x-analytics] 话题预设: {chosen.name} (niche={niche} is_ai={is_ai})")
        return cfg
    # 3. 极简兜底
    print("[warn] 无可用 topics.json，使用极简兜底", file=sys.stderr)
    return {"其他": []}


def norm_key(k: str) -> str:
    return k.strip().lower().replace("_", " ").strip()


def build_alias_map(fieldnames):
    lower_map = {norm_key(k): k for k in fieldnames}
    resolved = {}
    for canon, alist in ALIASES.items():
        found = None
        for a in alist:
            if norm_key(a) in lower_map:
                found = lower_map[norm_key(a)]
                break
        if not found and norm_key(canon) in lower_map:
            found = lower_map[norm_key(canon)]
        resolved[canon] = found
    return resolved


def snowflake_to_cst(pid_str):
    try:
        pid = int(str(pid_str).strip())
        ts_ms = (pid >> 22) + TW_EPOCH
        dt_utc = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
        return dt_utc.astimezone(CST)
    except Exception:
        return None


def classify(text: str, topics_cfg: dict) -> str:
    if not text:
        return "其他"
    if text.lstrip().startswith("@"):
        return "纯回复"
    tt = text.lower()
    for topic, kws in topics_cfg.items():
        for kw in kws:
            if kw.lower() in tt or kw in text:
                return topic
    if "其他日常" in topics_cfg:
        return "其他日常"
    if "其他" in topics_cfg:
        return "其他"
    return list(topics_cfg.keys())[-1] if topics_cfg else "其他"


def ensure_mpl():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.ticker as mticker
        import numpy as np
        return plt, mticker, np
    except ImportError:
        req_path = Path(__file__).parent / "requirements.txt"
        print(
            "[error] 缺少绘图依赖 matplotlib（或 numpy）。请先安装后再运行：\n"
            f"  pip install -r \"{req_path}\"\n"
            "  # 或: uv pip install matplotlib numpy",
            file=sys.stderr,
        )
        sys.exit(1)


def load_csv(path: Path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV 无表头")
        alias = build_alias_map(reader.fieldnames)
        for need in ["post_id", "post_text", "impressions"]:
            if not alias.get(need):
                raise ValueError(f"缺必选列 [{need}]，实有 {reader.fieldnames}。期望别名: {ALIASES[need]}")
        rows = []
        for i, raw in enumerate(reader, start=2):
            try:
                pid = raw[alias["post_id"]].strip() if alias["post_id"] else ""
                text = raw[alias["post_text"]] if alias["post_text"] else ""
                imp_raw = raw[alias["impressions"]] if alias["impressions"] else "0"
                imp = int(str(imp_raw).replace(",", "").strip() or 0)

                def get(canon, default="0"):
                    col = alias.get(canon)
                    if not col:
                        return default
                    v = raw.get(col, default)
                    return v if v not in (None, "") else default

                likes = int(str(get("likes", "0")).replace(",", "").strip() or 0)
                eng = int(str(get("engagements", "0")).replace(",", "").strip() or 0)
                book = int(str(get("bookmarks", "0")).replace(",", "").strip() or 0)
                follows = int(str(get("new_follows", "0")).replace(",", "").strip() or 0)
                profiles = int(str(get("profile_visits", "0")).replace(",", "").strip() or 0)
                details = int(str(get("detail_expands", "0")).replace(",", "").strip() or 0)
                urls = int(str(get("url_clicks", "0")).replace(",", "").strip() or 0)
                link = raw[alias["post_link"]] if alias.get("post_link") else ""
                cst = snowflake_to_cst(pid) if pid else None

                if cst and alias.get("date"):
                    try:
                        date_raw_chk = raw[alias["date"]]
                        if date_raw_chk and date_raw_chk.strip():
                            dt_chk = datetime.strptime(date_raw_chk.strip().strip('"'), "%a, %b %d, %Y")
                            if abs((cst.date() - dt_chk.date()).days) > 1:
                                print(
                                    f"[warn] 第{i}行 Snowflake {cst.date()} 与 Date列 {dt_chk.date()} 偏差>1天",
                                    file=sys.stderr,
                                )
                    except Exception:
                        pass

                if not cst:
                    date_raw = raw[alias["date"]] if alias.get("date") else ""
                    try:
                        dt = datetime.strptime(date_raw.strip().strip('"'), "%a, %b %d, %Y")
                        cst = dt.replace(tzinfo=CST)
                    except Exception:
                        cst = datetime.now(CST)

                is_reply = text.lstrip().startswith("@")
                rows.append({
                    "post_id": pid,
                    "post_text": text,
                    "post_link": link,
                    "impressions": imp,
                    "likes": likes,
                    "engagements": eng,
                    "bookmarks": book,
                    "new_follows": follows,
                    "profile_visits": profiles,
                    "detail_expands": details,
                    "url_clicks": urls,
                    "cst": cst,
                    "is_reply": is_reply,
                    "raw": raw,
                })
            except Exception as e:
                print(f"[warn] 第{i}行跳过: {e}", file=sys.stderr)
        return rows


def decide_depth(rows, args):
    if args.deep:
        return "deep"
    if args.lite:
        return "lite"
    n = len(rows)
    span_days = 1
    if rows:
        dates = [r["cst"].date() for r in rows]
        span_days = (max(dates) - min(dates)).days + 1
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
    parser.add_argument("--niche", dest="niche", default=None, help="账号主方向，如 AI / Vibe Coding / 通用")
    args = parser.parse_args()

    # 1. 解析输入
    csv_path = Path(args.csv) if args.csv else None
    if not csv_path or not csv_path.exists():
        candidates = list(Path.cwd().glob("*.csv")) + list(Path.home().joinpath("Downloads").glob("account_analytics*.csv"))
        candidates = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)
        if candidates and not args.yes:
            print("[x-analytics] 未指定 CSV，探测到候选：")
            for i, p in enumerate(candidates[:5], 1):
                print(f"  {i}. {p} ({p.stat().st_size // 1024}KB)")
            try:
                sel = input("输入序号或直接输入路径 (回车选1): ").strip()
                if sel.isdigit() and 1 <= int(sel) <= len(candidates):
                    csv_path = candidates[int(sel) - 1]
                elif sel:
                    csv_path = Path(sel)
                else:
                    csv_path = candidates[0]
            except Exception:
                csv_path = candidates[0] if candidates else None
        elif candidates:
            csv_path = candidates[0]
        else:
            parser.error("未找到 CSV，请指定路径： python scripts/x-analyze.py <csv> --out ./x-reports")
    if not csv_path or not csv_path.exists():
        print(f"[error] CSV 不存在: {csv_path}", file=sys.stderr)
        sys.exit(1)
    print(f"[x-analytics] 输入: {csv_path}")

    # 2. 粉丝数与赛道
    followers = args.followers
    niche = args.niche
    if followers is None and not args.yes:
        try:
            ans = input("你现在多少粉？如 2800 (回车默认 0): ").strip()
            followers = int(ans) if ans else 0
        except Exception:
            followers = 0
    if followers is None:
        followers = 0
    if not niche and not args.yes:
        try:
            ans = input("账号主方向？如 AI / Vibe Coding / 通用 (回车默认 AI): ").strip()
            niche = ans if ans else "AI"
        except Exception:
            niche = "AI"
    if not niche:
        niche = "AI"
    print(f"[x-analytics] 粉丝数: {followers} | 方向: {niche} | 手册: references/handbook/")

    # 3. 输出目录
    out_base = Path(args.out) if args.out else None
    if not out_base and not args.yes:
        try:
            ans = input("报告输出到哪个文件夹？默认 ./x-reports/ (回车确认): ").strip()
            out_base = Path(ans) if ans else Path("./x-reports")
        except Exception:
            out_base = Path("./x-reports")
    if not out_base:
        out_base = Path("./x-reports")
    out_base = out_base.resolve()
    out_base.mkdir(parents=True, exist_ok=True)
    print(f"[x-analytics] 输出基目录: {out_base}")

    # 4. 加载与指标归一
    rows = load_csv(csv_path)
    if not rows:
        print("[error] 无有效数据", file=sys.stderr)
        sys.exit(1)
    topics_cfg = load_topics_cfg(args, niche)

    for r in rows:
        r["topic"] = classify(r["post_text"], topics_cfg)
        r["len"] = len(r["post_text"])
        r["has_link"] = 1 if ("http" in r["post_text"] or "t.co" in r["post_text"]) else 0
        r["er"] = safe_div(r["engagements"], r["impressions"])
        r["hr"] = r["cst"].hour

    orig = [r for r in rows if not r["is_reply"]]
    reply_rows = [r for r in rows if r["is_reply"]]
    depth = decide_depth(rows, args)
    print(f"[x-analytics] 共 {len(rows)} 条 (原创{len(orig)} 回复{len(reply_rows)}) -> 模式: {depth}")

    dates = [r["cst"].date() for r in rows]
    start, end = min(dates), max(dates)
    slug = f"{start}_{end}-内容复盘" if depth == "lite" else f"{start}_{end}-深度挖掘"
    out_dir = out_base / slug
    assets_dir = out_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    print(f"[x-analytics] 报告目录: {out_dir}")

    # 5. 可视化 (统一编号 01~06)
    plt, mticker, np = ensure_mpl()
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    generated_charts = []

    # 01-daily.png
    daily = defaultdict(list)
    for r in rows:
        daily[r["cst"].date()].append(r)
    sorted_days = sorted(daily.keys())
    labels = [d.strftime("%m/%d\n%a") for d in sorted_days]
    totals = [sum(x["impressions"] for x in daily[d]) for d in sorted_days]
    avgs = [safe_div(sum(x["impressions"] for x in daily[d]), len(daily[d])) for d in sorted_days]
    fig, ax1 = plt.subplots(figsize=(14 if len(sorted_days) > 14 else 11, 4.8))
    x = np.arange(len(sorted_days))
    ax1.bar(x, totals, color="#CBD5E1", edgecolor="white", width=0.6)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=7)
    ax1.set_ylabel("Total Impressions")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v / 1000)}k" if v >= 1000 else f"{int(v)}"))
    ax2 = ax1.twinx()
    ax2.plot(x, avgs, color="#EF4444", marker="o", markersize=4, linewidth=2)
    ax2.set_ylabel("Avg / post", color="#EF4444")
    if len(sorted_days) > 20:
        ax2.axvspan(len(sorted_days) - 7 - 0.5, len(sorted_days) - 0.5, color="#FEF2F2", alpha=0.6)
    plt.title(
        f"Daily Trend: {start} -> {end}  |  Total {sum(totals):,}  Avg {safe_div(sum(totals), len(rows)):.0f}",
        fontsize=11,
        fontweight="bold",
    )
    fig.tight_layout()
    plt.savefig(assets_dir / "01-daily.png", dpi=180, bbox_inches="tight")
    plt.close()
    generated_charts.append("01-daily.png")

    # 02-topic.png
    ts = defaultdict(list)
    for r in orig:
        if r["topic"] == "纯回复":
            continue
        ts[r["topic"]].append(r)
    topics_sorted = sorted(ts.keys(), key=lambda t: sum(x["impressions"] for x in ts[t]), reverse=True)
    if topics_sorted:
        avgs_t = [safe_div(sum(x["impressions"] for x in ts[t]), len(ts[t])) for t in topics_sorted]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        y = np.arange(len(topics_sorted))
        cols = ["#EF4444" if i == 0 else "#F59E0B" if i < 3 else "#94A3B8" for i in range(len(topics_sorted))]
        ax.barh(y, avgs_t, color=cols, edgecolor="white", height=0.55)
        ax.set_yticks(y)
        ax.set_yticklabels([f"{t} (n={len(ts[t])})" for t in topics_sorted], fontsize=9)
        ax.set_xlabel("Avg Impressions (原创)")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v / 1000)}k" if v >= 1000 else f"{int(v)}"))
        ax.invert_yaxis()
        offset_x = max(avgs_t) * 0.015 if max(avgs_t) > 0 else 10
        for i, avg in enumerate(avgs_t):
            ax.text(avg + offset_x, i, f"{int(avg):,}", va="center", fontsize=8, fontweight="bold")
        plt.title("Topic ROI: 均值 vs 总量", fontsize=11, fontweight="bold")
        plt.tight_layout()
        plt.savefig(assets_dir / "02-topic.png", dpi=180, bbox_inches="tight")
        plt.close()
        generated_charts.append("02-topic.png")

    # 03-hourly.png
    hr = defaultdict(list)
    for r in orig:
        hr[r["hr"]].append(r["impressions"])
    if hr:
        hours = sorted(hr.keys())
        avgs_h = [safe_div(sum(hr[h]), len(hr[h])) for h in hours]
        fig, ax = plt.subplots(figsize=(12, 4.2))
        cols_h = []
        for v in avgs_h:
            if v >= 5000:
                cols_h.append("#EF4444")
            elif v >= 3000:
                cols_h.append("#F59E0B")
            elif v >= 1500:
                cols_h.append("#38BDF8")
            else:
                cols_h.append("#E2E8F0")
        ax.bar(hours, avgs_h, color=cols_h, edgecolor="white", width=0.7)
        ax.set_xticks(hours)
        ax.set_xticklabels([f"{h:02d}" for h in hours], fontsize=8)
        ax.set_ylabel("Avg Impressions")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v / 1000)}k" if v >= 1000 else f"{int(v)}"))
        ax.set_xlabel("Beijing Hour (CST)")
        plt.title("Hourly Golden Windows (原创, CST)", fontsize=11, fontweight="bold")
        plt.tight_layout()
        plt.savefig(assets_dir / "03-hourly.png", dpi=180, bbox_inches="tight")
        plt.close()
        generated_charts.append("03-hourly.png")

    # 04-funnel.png
    tot_imp = sum(r["impressions"] for r in rows)
    tot_det = sum(r["detail_expands"] for r in rows)
    tot_url = sum(r["url_clicks"] for r in rows)
    tot_prof = sum(r["profile_visits"] for r in rows)
    tot_fol = sum(r["new_follows"] for r in rows)

    detail_rate = safe_div(tot_det, tot_imp) * 100
    url_rate = safe_div(tot_url, tot_imp) * 100
    prof_rate = safe_div(tot_prof, tot_imp) * 100
    fol_rate = safe_div(tot_fol, tot_imp) * 100
    home_to_fol = safe_div(tot_fol, tot_prof) * 100

    labels_f = [
        f"Impr\n{tot_imp // 1000}k" if tot_imp >= 1000 else f"Impr\n{tot_imp}",
        f"Detail\n{tot_det}",
        f"URL\n{tot_url}",
        f"Profile\n{tot_prof}",
        f"Follows\n{tot_fol}",
    ]
    vals_f = [max(1, v) for v in [tot_imp, tot_det, tot_url, tot_prof, tot_fol]]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    y = np.arange(len(labels_f))
    cols_f = ["#E2E8F0", "#38BDF8", "#0EA5E9", "#F59E0B", "#EF4444"]
    raw_vals = [tot_imp, tot_det, tot_url, tot_prof, tot_fol]
    pcts = [safe_div(v, tot_imp) * 100 for v in raw_vals]
    widths = [max(0.015, p) for p in pcts]
    ax.barh(y, widths, color=cols_f, edgecolor="white", height=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(labels_f, fontsize=8)
    ax.set_xlabel("占曝光比例 % (log)")
    ax.set_xscale("log")
    ax.set_xlim(0.01, 130)
    for i, (w, p) in enumerate(zip(widths, pcts)):
        ax.text(w * 1.08, i, f"{p:.2f}%", va="center", fontsize=7, fontweight="bold")
    ax.invert_yaxis()
    plt.title(
        f"Funnel: {detail_rate:.2f}% 详情 -> {prof_rate:.2f}% 主页 -> {fol_rate:.3f}% 关注",
        fontsize=10,
        fontweight="bold",
    )
    plt.tight_layout()
    plt.savefig(assets_dir / "04-funnel.png", dpi=180, bbox_inches="tight")
    plt.close()
    generated_charts.append("04-funnel.png")

    # Deep 追加: 05-length.png + 06-top10.png
    top10 = sorted(orig, key=lambda x: x["impressions"], reverse=True)[:10] if orig else []
    if depth == "deep" and orig:
        lens = [r["len"] for r in orig]
        imps = [max(1, r["impressions"]) for r in orig]
        fig, ax = plt.subplots(figsize=(10, 4.2))
        cols_l = ["#EF4444" if r["has_link"] else "#94A3B8" for r in orig]
        sizes = [40 if r["impressions"] < 1000 else 80 if r["impressions"] < 5000 else 120 for r in orig]
        ax.scatter(lens, imps, c=cols_l, s=sizes, alpha=0.65, edgecolors="white", linewidth=0.6)
        ax.set_xlabel("Post Length (chars)")
        ax.set_ylabel("Impressions")
        ax.set_yscale("log")
        low_y = max(1, min(200, min(imps) * 0.8))
        high_y = max(low_y * 2, max(imps) * 1.25)
        ax.set_ylim(low_y, high_y)
        plt.title("Length vs Impressions (red=with link, gray=no link)", fontsize=10, fontweight="bold")
        plt.tight_layout()
        plt.savefig(assets_dir / "05-length.png", dpi=180, bbox_inches="tight")
        plt.close()
        generated_charts.append("05-length.png")

        if top10:
            top10_rev = list(reversed(top10))
            labels_t = [
                (r["post_text"][:32] + "…" if len(r["post_text"]) > 32 else r["post_text"]).replace("\n", " ")
                for r in top10_rev
            ]
            vals_t = [r["impressions"] for r in top10_rev]
            fig, ax = plt.subplots(figsize=(11, 5))
            bars = ax.barh(range(len(vals_t)), vals_t, color="#94A3B8", edgecolor="white", height=0.6)
            for i in range(max(0, len(vals_t) - 3), len(vals_t)):
                bars[i].set_color("#F59E0B")
            if vals_t:
                bars[-1].set_color("#EF4444")
            ax.set_yticks(range(len(vals_t)))
            ax.set_yticklabels(labels_t, fontsize=7)
            ax.set_xlabel("Impressions")
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v / 1000)}k" if v >= 1000 else f"{int(v)}"))
            ax.invert_yaxis()
            offset_top = max(vals_t) * 0.015 if max(vals_t) > 0 else 10
            for i, r in enumerate(top10_rev):
                ax.text(
                    r["impressions"] + offset_top,
                    i,
                    f"{r['impressions']:,} · {r['cst'].strftime('%m/%d %H:%M')} · {r['topic']}",
                    va="center",
                    fontsize=6,
                    fontweight="bold",
                )
            plt.title("Top10 原创", fontsize=11, fontweight="bold", loc="left")
            plt.tight_layout()
            plt.savefig(assets_dir / "06-top10.png", dpi=180, bbox_inches="tight")
            plt.close()
            generated_charts.append("06-top10.png")

    # 动态计算小时黄金档与低谷档
    reliable_hours = {h: vals for h, vals in hr.items() if len(vals) >= 5}
    hours_for_rank = reliable_hours if reliable_hours else hr
    hour_note = "（已过滤样本 <5 条的时段）" if reliable_hours else "（样本较稀疏，未过滤 <5 条时段，仅供参考）"
    sorted_hours = sorted(
        hours_for_rank.items(),
        key=lambda kv: safe_div(sum(kv[1]), len(kv[1])),
        reverse=True,
    )
    if sorted_hours:
        golden_hours = [f"{h:02d}:00（均 {safe_div(sum(v), len(v)):.0f}, n={len(v)}）" for h, v in sorted_hours[:3]]
        golden_str = "、".join(golden_hours)
        low_slice = sorted_hours[3:][-3:]
        if low_slice:
            low_hours = [f"{h:02d}:00（均 {safe_div(sum(v), len(v)):.0f}, n={len(v)}）" for h, v in low_slice]
            low_str = "、".join(low_hours)
        else:
            low_str = "有效时段较少（≤3 个），暂未单列低谷时段"
    else:
        golden_str = "暂无原创样本"
        low_str = "暂无原创样本"

    # 章节动态编号（避免跳号）
    sec_num = 4
    top10_md = ""
    if depth == "deep" and top10:
        top10_rows = []
        for idx, r in enumerate(top10, 1):
            hook = (r["post_text"][:40] + "…" if len(r["post_text"]) > 40 else r["post_text"]).replace("\n", " ").replace("|", "\\|")
            top10_rows.append(
                f"| {idx} | {r['impressions']:,} | {r['cst'].strftime('%m-%d %H:%M')} | {r['topic']} | {hook} | {r['likes']}♡ / {r['bookmarks']}🔖 |"
            )
        top10_table = "\n".join(top10_rows)
        top10_md = f"""## {sec_num}. Top10 原创

| 排名 | 曝光 | 时间 (CST) | 话题 | 开头钩子 | 互动 |
|---:|---:|---|---|---|---|
{top10_table}

"""
        sec_num += 1

    handbook_sec_num = sec_num
    next_sec_num = sec_num + 1

    # 5.5 手册对标诊断（全部基于当前 CSV 动态计算）
    orig_pct = safe_div(len(orig), len(rows)) * 100
    reply_pct = safe_div(len(reply_rows), len(rows)) * 100
    reply_avg = safe_div(sum(r["impressions"] for r in reply_rows), len(reply_rows))

    if followers < 1000:
        stage, stage_en = "冷启动期（0-1000）", "以互动为主"
        stage_advice = (
            f"当前 {followers} 粉，处于冷启动。手册 `02-如何账号定位` / `04-如何和大V互动` 建议原创占比约 30%，"
            f"重心放在大V评论区互动（共鸣/配图/二创/接需求/AI辅助）。当前原创占比 {orig_pct:.1f}% "
            f"{'✅ 比例合理' if orig_pct < 50 else '⚠️ 原创偏高，建议增加高质量大V互动'}；"
            f"方向 `{niche}` 建议保持单语言赛道定位。"
        )
    elif followers < 3000:
        stage, stage_en = "成长期（1000-3000）", "以内容为主"
        stage_advice = (
            f"当前 {followers} 粉（{niche}），手册 `08-日常如何发帖` 建议 40% 原创 / 50% 互动 / 10% 生活感悟，"
            f"日更 20-25 条。当前原创 {orig_pct:.1f}% / 回复 {reply_pct:.1f}%，"
            f"{'✅ 结构健康' if 35 < orig_pct < 55 else '⚠️ 结构偏科，可向 40/50/10 调整'}。"
        )
    else:
        stage, stage_en = "变现期（3000+）", "可启动变现"
        stage_advice = (
            f"当前 {followers} 粉（手册 `05-怎么变现`：500 蓝V + 500 万展示可开创作者收益，2000 粉起可接商单）。"
            f"`{niche}` 赛道商单参考报价约为粉丝数的 10%-30%（约 {followers * 0.1:.0f}-{followers * 0.3:.0f} 元/条），"
            f"建议以干货实测自然带入产品，避免硬广。"
        )

    rows_sorted = sorted(rows, key=lambda x: x["cst"])
    intervals = [
        (rows_sorted[i]["cst"] - rows_sorted[i - 1]["cst"]).total_seconds() / 60
        for i in range(1, len(rows_sorted))
    ]
    avg_interval = safe_div(sum(intervals), len(intervals)) if intervals else 0.0
    burst = sum(1 for iv in intervals if iv < 60)

    has_link_ratio = safe_div(sum(r["has_link"] for r in orig), len(orig))
    orig_bm_rate = safe_div(sum(r["bookmarks"] for r in orig), sum(r["impressions"] for r in orig)) * 100
    life_cnt = sum(1 for r in orig if r["topic"] in ["个人思考", "其他日常", "日常与互动", "其他"])
    life_pct = safe_div(life_cnt, len(rows)) * 100

    if ts:
        top_vol_topic = max(ts.keys(), key=lambda t: len(ts[t]))
        top_vol_cnt = len(ts[top_vol_topic])
        top_vol_share = safe_div(top_vol_cnt, len(orig)) * 100
        source_msg = (
            f"本期第一大原创话题为 `{top_vol_topic}`（{top_vol_cnt} 条，占原创 {top_vol_share:.1f}%）。"
            f"{'⚠️ 单一话题占比 >40%，建议按手册第 07 章扩展多信息源（AI HOT / 社区 / X List / GitHub）' if top_vol_share > 40 else '✅ 选题分布较均衡，可继续沿用多源筛选'}。"
        )
    else:
        source_msg = "本期无原创话题样本，建议按手册第 07 章建立固定信息源选题池。"

    hourly_chart_file = "03-hourly.png" if "03-hourly.png" in generated_charts else "暂无"
    best_hours_hint = "、".join([f"{h:02d}:00" for h, _ in sorted_hours[:2]]) if sorted_hours else "数据样本时段"

    handbook_md = f"""## {handbook_sec_num}. 增长手册对标（{followers}粉 · {niche} · {stage}）

> 手册原文在 `references/handbook/`（8章）。当前分阶段：**{stage} — {stage_en}**

- **阶段诊断**：{stage_advice} 详见 `handbook/README.md` 与 `handbook/02-如何账号定位/`
- **算法对标（06章）**：回复权重 `回复 > 转发 > 收藏 > 点赞`，本期回复占比 {reply_pct:.1f}%；发帖后首小时决定权重，结合你本期的 `{hourly_chart_file}`，优先在 **{best_hours_hint}** 等高均值时段发布重点内容。
- **连发检测（06章第四点）**：{"平均发帖间隔 {:.1f} min，1h 内连发 {} 次。{}".format(avg_interval, burst, "✅ 间隔健康（>90min）" if avg_interval > 90 else "⚠️ 间隔偏密（手册建议同号连续发帖间隔 1-2h，避免时间线同质降权）") if intervals else "样本仅 1 条，无法计算发帖间隔。"} 参考 `handbook/06-X推荐算法讲解/`
- **内容配比（08章）**：手册建议 40% 原创 / 50% 互动 / 10% 生活，本期结构约 **{orig_pct:.0f}% / {reply_pct:.0f}% / ~{life_pct:.0f}%**。{'✅ 比例接近' if 35 < orig_pct < 55 else '⚠️ 可按阶段目标回调'} 见 `handbook/08-日常如何发帖/`
- **价值分（08章）**：原创带链接比例 {has_link_ratio * 100:.1f}%，原创整体收藏率 {orig_bm_rate:.2f}%。{'✅ 具备可收藏/可拿走价值' if (has_link_ratio > 0.3 or orig_bm_rate >= 0.5) else '⚠️ 收藏与可带走资料偏少，建议增加实操步骤/工具链接/配图'} 见 `handbook/08-日常如何发帖/`
- **互动质量（04章）**：本期共 {len(reply_rows)} 条回复（均曝光 {reply_avg:.0f}），避免低信息量水评，优先使用手册 5 法（深共鸣 / 配图 / 二创 / 接需求 / 润色）抢大V首评。见 `handbook/04-如何和大V互动/`
- **信息源（07章）**：{source_msg}"""

    # 6. 写 Markdown
    total_imp = sum(r["impressions"] for r in rows)
    total_likes = sum(r["likes"] for r in rows)
    total_eng = sum(r["engagements"] for r in rows)
    md_path = out_dir / f"{slug}.md"

    topic_lines = []
    if ts:
        for t in topics_sorted:
            lst = ts[t]
            tot = sum(x["impressions"] for x in lst)
            avg = safe_div(tot, len(lst))
            bm = sum(x["bookmarks"] for x in lst)
            bm_rate = safe_div(bm, tot) * 100
            topic_lines.append(f"| {t} | {len(lst)} | {tot:,} | {avg:.0f} | {bm} | {bm_rate:.2f}% |")
    topic_table = "\n".join(topic_lines) if topic_lines else "| - | 0 | 0 | 0 | 0 | 0.00% |"

    chart_md = "\n".join([f"![{p}](assets/{p})" for p in generated_charts])

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

> 由 `x-analytics` 自动生成。输入 {csv_path.name}，输出 {md_path.name}。Snowflake 还原 CST，自适应 {depth}（<100条且<=7天 lite / 否则 deep）。

## 0. 总览

- 总帖子 {len(rows)}（原创 {len(orig)} / 回复 {len(reply_rows)}）/ 总曝光 {total_imp:,} / 均 {safe_div(total_imp, len(rows)):.0f} / 总点赞 {total_likes:,} / 总互动 {total_eng:,}
- 周期 {start} -> {end}，跨 {(end - start).days + 1} 天；0 曝光 {sum(1 for r in rows if r['impressions'] == 0)} 条
- 模式 {depth}：{'4图 (日趋势 / 话题ROI / 小时档 / 转化漏斗)' if depth == 'lite' else '6图 (追加 字数散点 / Top10 原创)'}

{chart_md}

## 1. 话题 ROI（原创）

| 话题 | 条数 | 总曝光 | 均值 | 收藏 | 收藏率 |
|---|---:|---:|---:|---:|---:|
{topic_table}

> 均值与收藏率最高的 1-2 个话题通常是你的核心赛道；均值较低且条数较多的话题建议收敛或优化表达形式。

## 2. 转化漏斗

- 曝光 {tot_imp:,} -> 详情 {tot_det:,} ({detail_rate:.2f}%) -> URL {tot_url:,} ({url_rate:.2f}%) -> 主页 {tot_prof:,} ({prof_rate:.3f}%) -> 关注 {tot_fol:,} ({fol_rate:.3f}%) | 主页->关注 {home_to_fol:.1f}%

## 3. 小时黄金档（原创, CST）

见 `{hourly_chart_file}` {hour_note}：

- **高均值窗口**：{golden_str}
- **低均值窗口**：{low_str}

{top10_md}{handbook_md}

## {next_sec_num}. 下一步

- 需要调整话题词表：修改 `references/topics.json`（或传入 `--topics <自定义.json>`）后重跑
- 需要将本次数据洞察写成推文/长文：调用 `chasen-x-writing`，用真实复盘数字出稿（切勿编造未测数据）
- 推文参考模板（填入真实观测结论后使用）：`我用 x-analytics 复盘了 {len(rows)} 条推文（{start} -> {end}），总曝光 {total_imp:,}，高表现时段集中在 {best_hours_hint} ...`

---
*Generated by x-analytics {depth} on {datetime.now(CST).strftime('%Y-%m-%d %H:%M')} CST | CSV: {csv_path.name}*
"""
    md_path.write_text(md_content, encoding="utf-8")
    print(f"[x-analytics] 完成: {md_path}")
    print(f"[x-analytics] 图表: {assets_dir}")


if __name__ == "__main__":
    main()
