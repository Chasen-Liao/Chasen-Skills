---
name: chasen-skill-capture
description: 教完可复用的多步工作、用户要求记住流程或同类活重复出现时，把流程沉淀为技能并同步技能仓库。
license: MIT
compatibility: 需具备共享技能编辑能力（如 UpdateSkill）及 GitHub PR 同步条件；遵守平台仓库执行与审批边界
metadata:
  author: Chasen-Liao
  version: "0.1.0"
  category: workflow
---

# Chasen skill 沉淀规矩（2026-11-24 校正）

## 何时沉淀
教完或做完一件**可复用、多步骤**的活，当场沉淀，不要等下次。触发包括：用户说记住/写成 skill、同类活第二次出现、Bot 自己发现稳定流程。

## 怎么沉淀
1. 用 UpdateSkill 写共享 skill（kebab-case 名 + 何时用的 description + 通用步骤）；助手专属细节（哪个频道、哪个仓）放 routine/记忆，不写进 skill 正文。
2. **每次新增或更新 skill 后，必须同步进 GitHub `Chasen-Liao/Chasen-Skills`**（按该仓 AGENTS.md / MAINTENANCE.md：升 `metadata.version`、改 `SKILL.md` + `README.md`、必要时改根导航，开 PR；用户说「以后更新了要同步」即视为默认可提交，仍用 PR 让他点合并）。跨 Pi / Antigravity / Claude Code 的 skill 更是强制同步。遵守平台仓库执行与审批边界，不把 push 交给 Pi；未同步时如实标记待同步，不声称已完成仓库同步。
3. 回复里用 `[name](sand-workflow:<id>)` 提一嘴，PR 已建立才附实际 PR 链接。

## 不沉淀
一次性问答、纯事实备忘（用 memory）、商单 brief、密钥与私信内容。

## 新建 Bot
新 Bot 先找现行 Eggbot（4e21ed98-bde7-45d4-afb7-34cce27814d5）设计（少而精、单一职责）；能改现有描述就不新建。
