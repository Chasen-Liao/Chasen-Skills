# 🚚 grokbot-pi-dispatch

> **基于 `pi-task` 的 Grok Bot 队列派活与自动唤醒** — Bot 写五要素任务书 → `pi-task` 后台派给 Pi → webhook 叫醒 Bot → 验收并 `ack`，多 Bot 共享主机也不串台。

<p>

![Executor](https://img.shields.io/badge/Executor-pi--task-0ea5e9?style=flat-square)
![Isolation](https://img.shields.io/badge/Queue-owner_·_pending_·_ack-7c3aed?style=flat-square)
![Wake](https://img.shields.io/badge/Wake-Webhook-10b981?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-64748b?style=flat-square)

</p>

> 💡 若未使用 `pi-task`（仅需单 Bot 极简调用原生 `pi -p`），请看 [cli-dispatch](../cli-dispatch/README.md)。

---

## ✨ 核心能力

| 能力 | 说明 |
| :--- | :--- |
| **📝 五要素任务书** | 目标、产物路径、完成标准、安全边界、单次自查收尾，精炼不跑偏 |
| **🏷️ `--owner` 队列隔离** | 每个任务绑定 ID 与归属 Bot，支持同机多 Bot 并行派活不串台 |
| **🔔 Webhook 唤醒 + 兜底** | 跑完自动 POST 通知叫醒 Bot，配合 `pi-task pending` 防止漏报 |
| **💬 同会话续跑** | 验收不达标时用 `pi-task reply` 追加说明继续改，保留原上下文 |
| **✅ 强制验收闭环** | Bot 核对 `result.md`、产物与 `git diff` 后再 `ack` 销账 |

---

## 🚀 安装与前置

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill grokbot-pi-dispatch --global --yes
```

**前置条件**：须先按 [grokbot-pi-setup](../grokbot-pi-setup/README.md) 完成 Pi、[robbin/grokbot-local-agent](https://github.com/robbin/grokbot-local-agent)（`pi-task`）与 webhook 例行任务配置。

---

## 🗣️ 怎么用

对已配好的 Grok Bot 说：

> `用 pi-task 派活` / `按 grokbot-pi-dispatch 派活：<任务描述>`

Bot 在遇到超过两三步的执行活时也会自动启用该 Skill，后台启动 `pi-task run` 并结束当前轮，等 webhook 唤醒后汇报验收结果。

| 常用 `pi-task` 命令 | 用途 |
| :--- | :--- |
| `pi-task run <dir> '<任务书>' --owner <ID>` | 后台派发新任务（默认 `--thinking medium --timeout 1800`） |
| `pi-task pending --owner <ID>` | 查当前 Bot 待验收队列 |
| `pi-task status <ID>` / `log <ID> -n 20` | 按需查看状态或尾部日志 |
| `pi-task reply <ID> '<补充>'` | 验收未过时沿用原会话补充重派 |
| `pi-task ack <ID> --owner <ID>` | 验收通过后确认销账 |

---

## 📋 输出示例

Bot 被 webhook 唤醒并验收完成后向用户汇报：

```text
任务 `t-20261113-a1b2` 已完成（STATE: done）：
- 结论：已完成 scripts/parser.py 空行边界修复与回归测试。
- 验收证据：已核对 ~/.pi/tasks/t-20261113-a1b2/result.md，pytest 12/12 通过，git diff 无越界修改。
- 产物路径：/workspace/app/scripts/parser.py
- 状态确认：已执行 pi-task ack t-20261113-a1b2 --owner <ID>。
```

---

## 📂 目录

```text
grokbot-pi-dispatch/
├── SKILL.md    # Agent 执行契约（pi-task 队列派活与验收规范）
└── README.md   # 本文件
```

---

## 📄 License

MIT © Chasen-Liao
