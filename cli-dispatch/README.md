# 🚦 cli-dispatch

> **无 `pi-task` 时的原生 `pi -p` 极简派活方案** — 零包装脚本、零额外队列依赖，Bot 只拆任务和验收，重活直接后台跑本机 `pi -p`。

<p>

![Executor](https://img.shields.io/badge/Executor-pi_--p-0ea5e9?style=flat-square)
![Mode](https://img.shields.io/badge/Mode-Zero_Wrapper-10b981?style=flat-square)
![Version](https://img.shields.io/badge/version-0.6.0-7c3aed?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-64748b?style=flat-square)

</p>

> 💡 若你已按 [grokbot-pi-setup](../grokbot-pi-setup/README.md) 部署了 `pi-task`（需要 `--owner` 隔离、任务 ID 与 `pending/ack` 队列），请使用 [grokbot-pi-dispatch](../grokbot-pi-dispatch/README.md)。

---

## ✨ 能做什么

| 能力 | 说明 |
| :--- | :--- |
| **🧠 Bot 减负** | 远端 Bot 只负责拆解、写五要素任务书、派活与验收 |
| **⚡ 零脚本依赖** | 只需本机有原生 `pi`，直接调用 `pi -p` 无头模式，无需安装额外队列工具 |
| **🔔 退出即唤醒** | Bot 通过后台 Shell 调起 `pi -p`，进程退出自动唤醒（可选拼一句 `curl` webhook） |
| **👀 轻量查进度** | `--mode json` 输出结构化日志，需要时 `rg` 一行查最近工具与 `agent_end` |
| **✅ 安全与验收** | 禁删/禁发/禁付/禁 push，Bot 亲自查产物与 `git diff`，不合格最多重派两次 |

---

## 🚀 安装与前置

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill cli-dispatch --global --yes
```

**前置条件**：本机已安装 [Pi](https://pi.dev) 并配好至少一个可用模型（运行 `pi --list-models` 确认），且 Bot 具备后台执行 Shell 的能力。

冒烟验证：

```bash
mkdir -p ~/.pi-dispatch/logs
pi -p '在 /tmp/pi-smoke.txt 写入 ok' --provider <provider> --model <model> \
  --thinking medium --no-session --mode json > ~/.pi-dispatch/logs/smoke.jsonl 2>&1
```

---

## 🗣️ 怎么用

对 Bot 说：

> `用 pi -p 派活` / `按 cli-dispatch 派活：<任务描述>`

Bot 会按五要素（目标、产物绝对路径、完成标准、边界、单次自查收尾）内联拼出任务书，后台拉起 `pi -p` 后立即结束当前轮；被唤醒后检查产物与 `git diff` 再向你汇报。

| 常用参数 / 检查 | 用法 |
| :--- | :--- |
| 难活升级推理 | 加 `--thinking high`（默认 `medium`） |
| 只读侦察/扫盘 | 加 `--tools read,ls,grep,find` |
| 查看最近调用工具 | `rg -o '"toolName":"\w+"' <日志> \| tail -5` |
| 确认任务是否结束 | `rg -q '"type":"agent_end"' <日志>` |

---

## 📋 输出示例

Bot 被唤醒并验收通过后向用户汇报：

```text
已完成派活任务 `fix-auth-guard`：
- 结论：已修复空 token 校验边界并补齐 2 条单元测试（pytest 全部通过）。
- 验收：`git diff` 仅改动目标模块，无越界写入或删除。
- 产物：/workspace/project/src/auth.py、/workspace/project/tests/test_auth.py
```

---

## 📂 目录

```text
cli-dispatch/
├── SKILL.md    # Agent 执行契约（含内联五要素任务模板）
└── README.md   # 本文件
```

---

## 📄 License

MIT © Chasen-Liao
