# 🚦 cli-dispatch

> Bot 只拆任务和验收，**重活交给本地 agy（Gemini 订阅）** — 省 Grok Bot 额度；Pi 作备用。

<p>

![Shell](https://img.shields.io/badge/Wrapper-bash-4b5563?style=flat-square&logo=gnu-bash&logoColor=white)
![Model](https://img.shields.io/badge/Default-gemini--3.8--flash--high-4285f4?style=flat-square&logo=google&logoColor=white)
![Safety](https://img.shields.io/badge/Permissions-scan_·_code_·_write-10b981?style=flat-square)
![Version](https://img.shields.io/badge/version-0.1.0-7c3aed?style=flat-square)

</p>

---

## ✨ 能做什么

| 能力 | 说明 |
| :--- | :--- |
| **🧠 Bot 减负** | 远端 Agent 只做拆解、任务书、派活、验收；执行走本地 CLI |
| **🔒 三档权限** | `scan` / `code` / `write` + 会话级 `--settings`，不改全局配置 |
| **✅ 真验收** | 解析 headless JSON：`denied_actions`、产物、`--expect` 任一不过关即 `FAIL` |
| **⏱️ 排队与后台** | 并发 1、`--bg` + `status/*.json`，适合长任务 |
| **🏠 可配置根目录** | `DISPATCH_HOME`（默认 `~/.agy-dispatch`），无写死个人路径 |

---

## 🚀 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill cli-dispatch --global --yes
```

**前置**

1. 按 **Antigravity 官方文档** 安装 **agy**，并用 Google 账号登录。
2. 可选：`export DISPATCH_HOME="$HOME/.agy-dispatch"`，`mkdir -p "$DISPATCH_HOME"/{tasks,out,logs,status,runs}`。
3. 无头环境：确保 dbus/keyring 可用，或设置 `AGY_XDG_RUNTIME_DIR` / `AGY_DBUS_SESSION_BUS_ADDRESS`。
4. 可选：安装 **Pi** 作 agy 不可用时的备用。

---

## 🗣️ 怎么用

### 在 Agent 中（推荐）

对 Grok Bot / Pi 说：

> `这个大改动别你自己啃，按 cli-dispatch 派给 agy` / `写任务书让本地 CLI 扫盘`

Agent 会读 `SKILL.md`，按四段模板写任务书并调用 `scripts/agy-run.sh`。

### 命令行示例

```bash
# SKILL_ROOT 指向本 skill 安装目录（由 npx skills 决定）
R="./scripts/agy-run.sh"   # 在 skill 根目录下执行时
export DISPATCH_HOME="${DISPATCH_HOME:-$HOME/.agy-dispatch}"

"$R" --profile scan --task "$DISPATCH_HOME/tasks/2026-11-10-inventory.md"
"$R" --profile code ~/my-repo -p 'npm test 并修失败' --expect ~/my-repo/.agy-ok
"$R" --profile scan --bg --task ./task.md   # 输出 run_id，查 $DISPATCH_HOME/status/<run_id>.json
```

详细参数与档位说明见 [references/agy-run.md](./references/agy-run.md)。

---

## 📦 目录

```text
cli-dispatch/
├── SKILL.md                 # Agent 执行契约
├── README.md                # 本文件
├── scripts/agy-run.sh       # 包装入口（固定模型、权限、验收）
├── templates/TASK_TEMPLATE.md
└── references/agy-run.md    # 脚本说明与示例
```

---

## Changelog

### 0.1.0

- 首版：从个人 dispatch 工作流通用化入库；`DISPATCH_HOME`、可配置 scan 可读目录、PATH 解析 `agy`。

---

## 📄 License

MIT © Chasen-Liao
