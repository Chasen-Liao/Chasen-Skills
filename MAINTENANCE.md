# MAINTENANCE.md — 维护规则

> 本仓库只放 Chasen 自用 skills，维护目标：**少而精、README 好看、SKILL 可跑**。

## 一、Skill 标准

每个 skill 必须满足：

```text
<skill-name>/
├── SKILL.md    # 必须，含 frontmatter
└── README.md   # 必须，人读
```

`SKILL.md` frontmatter 最小集：

```yaml
---
name: kebab-case
description: 一句话讲清何时触发（含中文触发语，如有）
license: MIT
compatibility: 前置依赖说明
metadata:
  author: Chasen-Liao
  version: "0.1.0"   # semver，改动即升版本
  category: data-analysis | research | workflow
---
```

## 二、新增 Skill Checklist

- [ ] 1. 定名 `kebab-case`，确认不与现有 skill 重名
- [ ] 2. 写 `SKILL.md`：触发语、步骤、边界、References
- [ ] 3. 写 `README.md`：首屏价值 + badges + 特性表 + 安装 + 用法 + 输出示例 + 目录
- [ ] 4. 本地验证：`npx skills add . --skill <name> --global --yes` 并真实触发一次
- [ ] 5. 根 `README.md` 导航表加一行
- [ ] 6. `metadata.version` 设 `0.1.0`
- [ ] 7. `git status` 确认仅新增本 skill 目录 + 根 README

## 三、更新 Skill Checklist

- [ ] 只改一个 skill，不碰其他
- [ ] `SKILL.md` 改逻辑 → `metadata.version` 升 patch/minor
- [ ] `README.md` 同步更新（特性/用法/截图）
- [ ] 根 `README.md` 若有一句话介绍，同步改
- [ ] 本地重装验证：`npx skills add . --skill <name> --global --yes`

## 四、README 纪律

| 文件 | 职责 | 禁止 |
| :--- | :--- | :--- |
| 根 `README.md` | 导航：是什么 + Skills 表 + 快速开始 + 目录结构 | 不展开 skill 细节 |
| `<skill>/README.md` | 介绍：做什么 + 特性 + 安装 + 用法 + 输出 + 原理 | 不复制 SKILL.md 全文 |
| `<skill>/SKILL.md` | 契约：给 Agent 的可执行步骤 | 不追求好看，追求可跑 |

- 统一用中文，保留必要英文术语/命令
- 表格优先，少用长段落
- badges 用 `shields.io`，风格 `flat-square`

## 五、版本与提交

- 版本：`0.1.0 → 0.1.1(patch) → 0.2.0(minor) → 1.0.0(稳定)`
- 提交信息：`feat(<skill>): ...` / `docs(<skill>): ...` / `chore: ...`
- 提交前：`git diff` 自检，`git status` 确认无 `docs/`、`.agents/`、`skills-lock.json`

## 六、忽略规则

已在 `.gitignore`：

```text
docs/              # 研究草稿，不入库
.agents/ .claude/ .pi/
skills-lock.json
__pycache__/ .venv/
.DS_Store *.log
```

新增本地草稿一律放 `docs/`，不另建忽略。

## 七、废弃

- 不再用的 skill：删目录 + 删根 README 一行 + `git rm -r <skill>`，不留空目录
- 不写“已废弃”占位，直接删

---

> 维护本质：每次只动一个 skill，让 README 好看到愿意分享，让 SKILL 稳到敢一键安装。
