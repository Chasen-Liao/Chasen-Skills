---
name: chasen-skill-capture
description: 教完可复用的多步工作、用户要求记住流程或同类活重复出现时，把流程沉淀为通用共享技能并按规范通过 PR 同步技能仓库。
license: MIT
compatibility: 需具备共享技能编辑能力（如 UpdateSkill）及 GitHub PR 同步条件；遵守平台仓库执行与审批边界
metadata:
  author: Chasen-Liao
  version: "0.2.0"
  category: workflow
---

# 可复用技能沉淀与仓库同步规矩

## 何时沉淀

教完或做完一件**可复用、多步骤**的活，当场沉淀，不要等下次。触发包括：用户说「记住 / 写成 skill」、同类活第二次出现、Bot 自己发现稳定流程。

## 怎么沉淀

1. **编写通用共享 Skill**：用平台技能更新工具（如 `UpdateSkill`）写入 `kebab-case` 名称、明确的触发 `description` 与通用可执行步骤。助手或个人专属细节（频道、特定仓库、内部 ID、个人环境默认值）放入 routine / memory 或独立私有覆写，**不写入公开技能正文**。
2. **同步技能仓库（仅走 PR）**：每次新增或更新可复用技能后，同步至目标技能仓库（`<skills-repo>`，默认按仓库 `AGENTS.md` / `MAINTENANCE.md` 升 `metadata.version`、更新 `SKILL.md` + `README.md` 与必要根导航，提交前执行公开隐私自检，开 PR 等待人工审阅合并）。跨 Pi / Antigravity / Claude Code 复用的技能更应及时同步。
3. **执行与诚实边界**：
   - 遵守平台仓库执行与审批边界，**不把 `git push` 交给 Pi**。
   - 若当前环境尚未完成仓库同步，如实标记「待同步」，绝不声称已完成仓库同步。
   - 回复中按当前平台方式提及已沉淀技能（如技能名或平台内链接），**仅在 PR 实际建立后附真实 PR 链接**。

## 不沉淀

一次性问答、纯事实备忘（用 memory）、商单 brief、密钥与凭证、私信内容，以及个人联系方式或内部实例 ID。

## 新建 Bot 原则

新建 Bot 前，先联系平台内指定的现行 Bot 设计助手（具体名称与 ID 由私有配置或平台列表提供，不硬编码进公开技能）评审设计，坚持少而精、单一职责；能改现有描述就不新建。
