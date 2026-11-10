# 🚦 cli-dispatch

> Bot 只拆任务和验收，**重活交给本地 Pi（经 Magpie 用 Antigravity / Gemini 额度）** — 省 Grok Bot 额度；agy 作备用。

<p>

![Shell](https://img.shields.io/badge/Wrapper-bash-4b5563?style=flat-square&logo=gnu-bash&logoColor=white)
![Executor](https://img.shields.io/badge/Primary-Pi_via_Magpie-0ea5e9?style=flat-square)
![Model](https://img.shields.io/badge/Model-gemini--3.8--flash-4285f4?style=flat-square&logo=google&logoColor=white)
![Safety](https://img.shields.io/badge/Permissions-scan_·_code_·_write-10b981?style=flat-square)
![Version](https://img.shields.io/badge/version-0.2.1-7c3aed?style=flat-square)

</p>

---

## ✨ 能做什么

| 能力 | 说明 |
| :--- | :--- |
| **🧠 Bot 减负** | 远端 Agent 只做拆解、任务书、派活、验收；执行走本地 CLI |
| **⚡ Pi 为主** | 默认派 Pi（经 Magpie 网关），同样的代码修复 token 约为 agy 的 1/4；agy 兜底 |
| **🔒 三档权限** | `scan` / `code` / `write`，每次运行自动生成沙箱，Pi 断网只连本地 Magpie |
| **✅ 真验收** | 解析 headless JSON：`denied_actions`、产物、`--expect` 任一不过关即 `FAIL` |
| **⏱️ 排队与后台** | Pi 并发 2、agy 并发 1，`--bg` + `status/*.json`，适合长任务 |
| **📉 额度闸门** | 运行前查 `magpie quota`，5 小时窗口超 90% 直接 `FAIL: quota` |
| **🏠 可配置根目录** | `DISPATCH_HOME`（默认 `~/.agy-dispatch`），无写死个人路径 |

---

## 🚀 安装

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill cli-dispatch --global --yes
```

**前置**

1. 安装 **Pi**，本机启动 **Magpie** 网关并用 Antigravity 账号登录；准备 `pi-run.sh` 包装脚本（暂不在本仓库，参数与 `agy-run.sh` 一致）。
2. 备用：按 **Antigravity 官方文档** 安装 **agy** 并登录。
3. 可选：`export DISPATCH_HOME="$HOME/.agy-dispatch"`，`mkdir -p "$DISPATCH_HOME"/{tasks,out,logs,status,runs}`。
4. 无头环境：确保 dbus/keyring 可用，或设置 `AGY_XDG_RUNTIME_DIR` / `AGY_DBUS_SESSION_BUS_ADDRESS`。

---

## 🗣️ 怎么用

### 在 Agent 中（推荐）

对 Grok Bot / Pi 说：

> `这个大改动别你自己啃，按 cli-dispatch 派给 Pi` / `写任务书让本地 CLI 扫盘`

Agent 会读 `SKILL.md`，按四段模板写任务书并调用 `pi-run.sh`；Pi 不行时改用 `scripts/agy-run.sh`。

### 命令行示例

```bash
# 主力：Pi（经 Magpie）
pi-run.sh --profile code ~/my-repo -p 'npm test 并修失败' --expect ~/my-repo/.pi-ok
pi-run.sh --profile scan --model pro --task "$DISPATCH_HOME/tasks/2026-11-10-inventory.md"

# 备用：agy；SKILL_ROOT 指向本 skill 安装目录（由 npx skills 决定）
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
├── scripts/agy-run.sh       # agy 备用包装入口（固定模型、权限、验收）
├── templates/TASK_TEMPLATE.md
└── references/agy-run.md    # 脚本说明与示例
```

---

## Changelog

### 0.2.1

- Pi `--thinking` 默认从 low 改为 medium；难活单独加 `--thinking high`，小活别开 high（容易乱翻文件、烧 token）。

### 0.2.0

- 执行主力改为 **Pi（经 Magpie 网关用 Antigravity 额度，Gemini 3.8 Flash）**，agy 降为备用。
- 新增：Pi 模型档（flash / pro / claude）与完整 id 写法、额度闸门（`magpie quota`，>90% 直接 FAIL）、并发与超时默认值、越权一次即整次 FAIL。
- `pi-run.sh` 暂未入库（依赖本机沙箱环境），参数与 `agy-run.sh` 一致。

### 0.1.0

- 首版：从个人 dispatch 工作流通用化入库；`DISPATCH_HOME`、可配置 scan 可读目录、PATH 解析 `agy`。

---

## 📄 License

MIT © Chasen-Liao
