# AGENTS.md — Chasen-Skills

> 通用公开 Agent Skills 仓库，追求少而精、脱敏通用、开箱即用。项目规则优先于全局规则。

## 定位

- 本仓库 = **通用公开 skill 集散地**，不是产品、不是框架，也不存放个人私密配置
- 每个 skill 独立自治，互不依赖（除显式声明如 `parallel-agent → pi-subagents`）
- 重点维护对象是 **README**，`docs/` 仅本地草稿已忽略
- **公开 vs 私有边界**：个人人设/语料/账号实测数据、个人 IP 图片、内部 Bot UUID、具体云商/模型默认值、私有主机路径与任何凭证均属于独立私有覆写，禁止写入本公开仓库

## 目录结构

```text
<skill-name>/
├── SKILL.md # 给 Agent 看的执行契约（必须）
├── README.md # 给人看的介绍（必须，好看）
├── scripts/ # 可选，脚本
├── references/ # 可选，词表/手册/骨架
└── assets/ # 可选，中性占位或通用资源

根目录:
├── README.md # 总导航，Skills 一览 + 安装
├── AGENTS.md # 本文件，Agent 工作纪律
├── MAINTENANCE.md # 维护规则，新增/更新 skill 的 checklist
├── scripts/check-public-privacy.py # 轻量公开隐私/密钥自检
└── .gitignore # 已忽略 docs/、skills-lock.json、.agents/ 等
```

## 核心纪律

1. **README 优先** — `SKILL.md` 是执行契约不追求好看，`README.md` 必须好看、讲清做什么/怎么装/怎么用；根 `README.md` 只做导航
2. **公开脱敏与零冗余** — 所有公开技能正文、示例、参考文档与图片必须通用化（配置项走占位符）；不堆砌重复说明
3. **docs/ 不入库** — 已 `.gitignore`，研究笔记、草稿放 `docs/`，不提交
4. **单 skill 单原子任务** — 默认一次只新增或修改一个 skill，不顺手改其他 skill（全仓规范/隐私治理等明确要求除外）
5. **薄封装** — 不做投机功能，脚本/词表能解决的不写复杂逻辑
6. **标准结构** — 新 skill 必须有 `SKILL.md` + `README.md`，命名 `kebab-case`，frontmatter 须符合 `MAINTENANCE.md` 最小集（`name`、`description`、`license`、`compatibility`、`metadata.author/version/category`）

## SKILL.md vs README.md 分工

| 文件 | 受众 | 要求 |
| :--- | :--- | :--- |
| `SKILL.md` | Agent | frontmatter 完整、触发语明确、步骤可执行、边界清晰、通用无私密硬编码 |
| `README.md` | 人 | 首屏讲清价值、含 badges/特性表/安装/用法/输出示例 |
| `根 README.md` | 人 | 只做导航，不展开 skill 细节，表格链到各 `README.md` |

## 新增 / 修改 Skill 流程

1. 确认目标：这个 skill 解决什么具体问题，触发语是什么
2. 读现有 skill 的 `SKILL.md` + `README.md` 保持风格一致
3. 最小实现：先让 `SKILL.md` 可跑，再补 `README.md` 好看，参数走占位符不硬编码个人配置
4. 隐私与本地验证：运行 `python3 scripts/check-public-privacy.py`；按需用 `npx skills add . --skill <name> --global --yes` 验证
5. 更新根 `README.md` 导航表
6. 检查 `git status` / `git diff`，只提交本次任务相关文件

## 验证

- 公开隐私校验：每次提交前运行 `python3 scripts/check-public-privacy.py`
- 脚本类 skill：跑一遍真实数据/真实命令，贴输出
- 浏览器/只读类：说明前置依赖（登录态、子代理）
- 无测试时至少 `git diff` 自检，不编造“已验证”

## 禁止

- 不把真实邮箱/手机号、内部 Bot UUID、私钥/Token/Webhook URL、私有路径/个人语料或个人专属图片提交入库
- 不擅自 `git push` / `git commit`（用户确认或明确授权开 PR 后再提交，仍须人工合并）
- 不改无关 skill，不顺手重构
- 不把 `docs/`、`.agents/`、`skills-lock.json` 提交
- 不写客套话，结论先行
