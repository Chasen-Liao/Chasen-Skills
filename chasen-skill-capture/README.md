# 📝 chasen-skill-capture

> **技能沉淀与公私分流规矩** — 经过验证的可复用多步工作流优先迭代既有 Skill、单真源不重复；通用模板走公开仓 PR，个人非密钥配置验明 `PRIVATE` 后入已配置私有仓；任何仓禁入密钥/凭证库/原始记忆与聊天记录，不把 `git push` 交给本地执行器。

<p>

![Scope](https://img.shields.io/badge/Scope-Skill_Capture-7c3aed?style=flat-square)
![Routing](https://img.shields.io/badge/Routing-Public_vs_Private-0ea5e9?style=flat-square)
![Version](https://img.shields.io/badge/version-0.2.0-10b981?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-64748b?style=flat-square)

</p>

> 💡 目录名保留 `chasen-skill-capture` 以兼容既有安装命令；正文与示例均为通用规则，实际仓库名、私有配置地址与当前设计助手 ID 均从使用侧/私有配置加载，不硬编码进公开模板。

---

## ✨ 核心规则

| 维度 | 规范 |
| :--- | :--- |
| **⚡ 验证后沉淀 + 去重** | 针对已验证的可复用多步流程优先迭代既有 Skill；规则单真源引用、正文精炼不重复 |
| **🔀 公私分流（不整份照搬）** | 绝不把完整本地 Skill / Profile 复制到公开仓；个人身份、实例 ID、路径、设备、模型默认值、语料与角色资产仅入已配置的私有仓库或本地私有配置 |
| **🔒 私有先验 + 公开全检** | 写私有仓前必验可见性为 `PRIVATE`（未配置不猜测）；提公开 PR 前检查正文、`references/`、图片、示例、commit 元数据与 PR 正文并保留合法署名 |
| **🚫 任何仓均禁入** | 密钥、凭证库（vault）、原始 memory 导出、私信/聊天记录、一次性问答与商单 brief 均不写入任何仓库 |
| **🛡️ 审批与状态诚实** | 平台执行与审批优先、不把 `git push` 委托给本地执行器、不重复开 PR；严格区分 `local live` / `branch saved` / `PR pending` / `main updated` / `runtime loaded` |
| **🧩 新建助手边界** | 使用当前已配置的设计助手，优先改进既有描述；不隐式转交任务、不扩权、不擅自新增 routine |

---

## 🚀 安装与前置

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill chasen-skill-capture --global --yes
```

**前置条件**：具备共享技能写入能力（如 `UpdateSkill`）与合规的 Git/PR 同步路径；所有仓库与权限操作遵守平台安全边界。

---

## 🗣️ 怎么用

经过验证的可复用多步工作流完成时自动触发，或直接说：

> `记住这个流程` / `把这个写成 skill` / `按 chasen-skill-capture 沉淀`

| 阶段 | 动作 |
| :--- | :--- |
| **1. 去重与判界** | 优先更新既有 Skill；排除密钥/凭证库、原始记忆、聊天记录、一次性问答与商单 brief |
| **2. 分流与验私** | 通用步骤去硬编码走公开仓；个人非密钥配置核验目标仓为 `PRIVATE` 后入已配置的私有仓库（未配置不猜测） |
| **3. 公开前全检** | 检查正文、参考、图片、示例、commit 元数据与 PR 正文并运行隐私自检；走 PR 等人工合并（已有 PR 则同分支迭代，不把 `push` 交本地执行器） |
| **4. 精确报状态** | 如实区分 `local live` / `branch saved` / `PR pending` / `main updated` 与 `runtime loaded`，归档不等于运行态已加载 |

---

## 📋 输出示例

已创建 PR 待人工合并时：

```text
已迭代共享技能 `weekly-review`：
- 状态：local live（本机技能已更新）；PR pending（公开仓待人工合并）；runtime loaded（待合并并重装后生效）。
- 公开同步：通用模板与文档已通过隐私检查，未包含个人配置。
- PR 链接：https://github.com/<owner>/<public-skills-repo>/pull/99
```

仅本地生效、尚未完成仓库同步时（如实标注，不谎称已同步）：

```text
已迭代共享技能 `weekly-review`：
- 状态：local live（仅本地已更新）；仓库同步待执行（未推送分支、未建 PR）。
```

---

## 📂 目录

```text
chasen-skill-capture/
├── SKILL.md    # Agent 执行契约（去重、公私分流、安全检查与状态口径）
└── README.md   # 本文件
```

---

## 📄 License

MIT © Chasen-Liao
