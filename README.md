# Chasen-Skills

Chasen 使用的个人 Agent skills，按 Git 版本维护。

## 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill parallel-agent --global --yes
```

安装后，Pi 可以通过全局 skills 目录发现 `parallel-agent`。

## 更新

```bash
npx skills update parallel-agent --global
```

## 当前 skills

- `parallel-agent` — 使用 pi-subagents 编排并行侦察、研究、评审和实现任务。
- `x-analytics` — 深度分析 𝕏 (X/Twitter) 账号数据，一键生成带图表的 Markdown 报告（`npx skills add Chasen-Liao/Chasen-Skills --skill x-analytics --global --yes`，用法 `/x-analytics <csv> --out ./x-reports`）。

每个 skill 使用标准目录结构：

```text
<skill-name>/SKILL.md
```
