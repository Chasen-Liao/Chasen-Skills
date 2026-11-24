# 🚦 cli-dispatch

> **共用主机 `pi-task` 派活与同轮验收** — Bot 写五要素任务，用 `<pi-task-dir>/pi-task run <work-dir> '<任务>' --owner <agent-id>` 派给共用主机上的 Pi；派完保持同一执行回合阻塞等待，亲自验收产物后才 `ack`，通知只作兜底。不要自行 `nohup` 或后台化。

<p>

![Executor](https://img.shields.io/badge/Executor-pi--task-0ea5e9?style=flat-square)
![Isolation](https://img.shields.io/badge/Isolation-owner_·_same--turn_ack-10b981?style=flat-square)
![Version](https://img.shields.io/badge/version-0.8.0-7c3aed?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-64748b?style=flat-square)

</p>

> 💡 **范围说明**：这里的「本机」指多个 Bot 共用的执行主机，**不是**用户注册的个人电脑。平台规定的执行方式、后台任务、仓库/桌面边界、安全与审批要求始终优先。具体的 `<pi-task-dir>`、默认 `<provider/model>` 与通知配置由部署环境或私有配置提供。

---

## ✨ 核心约束

| 维度 | 规范 |
| :--- | :--- |
| **🛡️ 平台要求优先** | 平台执行方式、仓库/桌面边界、安全与审批优先；不绕过、不自动放行 `needs_approval` |
| **🏷️ `--owner` 隔离** | `run / reply / approve / deny / pending / ack` 均带当前 Bot 的 agent ID，只处理自己的任务 |
| **⏳ 同回合阻塞等待** | Shell 正常启动（不自行 `nohup` / `&`），用长时间 `AwaitShell` 等到结束并验收后才 `ack` |
| **🔔 Webhook 仅兜底** | 通知只作兜底，不替代同轮等待；任务状态目录才是事实 |
| **🚫 高危禁派与保密** | 删除、发送、付款、发帖、`git push` 不交给 Pi；不读不打印密钥、`auth.json` 或 secrets |
| **🧾 诚实与精简回报** | 亲自验收产物/diff/测试后回报结论、证据与产物路径；默认不报内部任务 ID，不作零费用承诺 |

---

## 🚀 安装与前置

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill cli-dispatch --global --yes
```

**前置条件**：
- 共用主机已安装 Pi 与 `pi-task` 脚本，并配好至少一个可用 `<provider/model>`。
- Bot 具备 Shell 与阻塞等待（`AwaitShell`）工具。
- 若使用异步 webhook 唤醒方案而非同回合阻塞等待，可另见 [`grokbot-pi-dispatch`](../grokbot-pi-dispatch/README.md)。

---

## 🗣️ 怎么用

遇到平台允许本地执行的多步编码、文件或批处理任务时触发（或直接说 `按 cli-dispatch 派活`）。

标准执行闭环：查待验收队列 → 写五要素任务书（目标、绝对产物路径、完成标准、最小可改目录与禁令、单次自查收尾）→ 同回合启动并等待 → 亲自验收 → `ack`。

```bash
# 1. 若本轮已有派发记录，先看待验收队列
<pi-task-dir>/pi-task pending --owner <agent-id>

# 2. 派发任务（不加 nohup / &，随后用 AwaitShell 同回合等待）
<pi-task-dir>/pi-task run <work-dir> '<任务书>' --session <short-name> --owner <agent-id> --timeout 1800
```

| 常用参数 / 场景 | 用法 |
| :--- | :--- |
| 指定模型与思考强度 | `--model <provider/model> --thinking <low\|medium\|high>` |
| 纯只读且不写报告 | 加 `--no-write` |
| 无需联网 | 加 `--no-web` |
| 验收未过原会话修正 | `pi-task reply <ID> '<缺口说明>' --owner <agent-id>`（最多两次） |
| 验收通过确认销账 | `pi-task ack <ID> --owner <agent-id>` |

---

## 📋 输出示例

同回合验收通过并完成 `ack` 后向用户汇报（默认不附内部任务 ID，仅在排障或用户追问时提供）：

```text
已完成权限校验修复并验收通过：
- 结论：已修复空 token 边界判断并补齐 2 条回归用例。
- 验收证据：已核对 result.md 与 git diff，仅改动目标目录；pytest 12/12 全部通过。
- 产物路径：/workspace/project/src/auth.py、/workspace/project/tests/test_auth.py
```

---

## 📂 目录

```text
cli-dispatch/
├── SKILL.md    # Agent 执行契约（完整规则与排障/审批流程）
└── README.md   # 本文件
```

---

## 📄 License

MIT © Chasen-Liao
