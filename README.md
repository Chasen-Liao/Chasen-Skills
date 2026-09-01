# Chasen-Skills

Chasen 使用的个人 Agent skills，按 Git 版本维护。

## 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill <skill-name> --global --yes
# 例如
npx skills add Chasen-Liao/Chasen-Skills --skill x-ai-radar --global --yes
```

安装后，Pi / Antigravity 可通过全局 skills 目录发现对应 skill。

## 更新

```bash
npx skills update <skill-name> --global
```

## 当前 skills

- `parallel-agent` — 使用 pi-subagents 编排并行侦察、研究、评审和实现任务。
- `x-analytics` — 深度分析 𝕏 (X/Twitter) 账号数据，一键生成带图表的 Markdown 报告（`npx skills add Chasen-Liao/Chasen-Skills --skill x-analytics --global --yes`，用法 `/x-analytics <csv> --out ./x-reports`）。
- `x-ai-radar` — Antigravity 专用：自动追踪 X 热点，10 小时内 AI 热帖雷达（大V/高流速/热度分排序，Top 8-10 中文热榜，会话内直出）（`npx skills add Chasen-Liao/Chasen-Skills --skill x-ai-radar --global --yes`，用法 `/x-ai-radar` 或“刷一下 X AI 热榜”）。

### x-ai-radar 适配（Antigravity 专用）

- 触发：`/x-ai-radar` 或自然语言“自动追踪X热点/刷X热榜”
- 依赖：需已登录 X 且支持 `browser` 子代理；on-demand，会话内直出，不写文件

每个 skill 使用标准目录结构：

```text
<skill-name>/SKILL.md
```
