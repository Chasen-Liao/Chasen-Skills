# 🚦 cli-dispatch

> Bot 只拆任务和验收，**重活交给本地 Pi（经 Magpie 用 Antigravity / Gemini 额度）** — 省 Bot 额度；自带沙箱、`pi-run.sh` 开箱即用。

<p>

![Shell](https://img.shields.io/badge/Wrapper-bash-4b5563?style=flat-square&logo=gnu-bash&logoColor=white)
![Executor](https://img.shields.io/badge/Executor-Pi_+_Magpie-0ea5e9?style=flat-square)
![Model](https://img.shields.io/badge/Model-gemini--3.8--flash-4285f4?style=flat-square&logo=google&logoColor=white)
![Safety](https://img.shields.io/badge/Permissions-scan_·_code_·_write-10b981?style=flat-square)
![Version](https://img.shields.io/badge/version-0.3.0-7c3aed?style=flat-square)

</p>

---

## ✨ 能做什么

| 能力 | 说明 |
| :--- | :--- |
| **🧠 Bot 减负** | 远端 Agent 只做拆解、任务书、派活、验收 |
| **⚡ Pi + Magpie** | 经本机网关吃 Antigravity 额度；短模型名 flash / pro / claude |
| **🔒 三档权限** | `scan` / `code` / `write` + bwrap；断网后只连 Magpie |
| **✅ 真验收** | JSON 模式解析 `denied_actions`、`--expect`、quota 闸门 |
| **⏱️ 后台** | 最多 2 并发，`--bg` + `status/*.json` |
| **📉 额度闸门** | Gemini 5h 窗口 >90% 直接 `FAIL: quota` |
| **🏠 DISPATCH_HOME** | 默认 `~/.pi-dispatch`，无写死个人路径 |

---

## 🚀 安装

按顺序执行：

```bash
# 1. Pi
curl -fsSL https://pi.dev/install.sh | sh

# 2. Magpie
curl -fsSL https://usemagpie.ai/install.sh | sh

# 3. Antigravity 账号（经 Magpie 接入，非 agy CLI）
# ⚠️ Google 可能停用「在 Antigravity 产品外」使用的账号，请用备用 Google 账号
magpie accounts add antigravity

# 4. 网关（仅本机，不要 --lan / --web）
magpie serve

# 5. Pi 侧 Magpie 扩展
pi install npm:pi-magpie

# 6. 沙箱依赖
# Debian/Ubuntu: sudo apt install bubblewrap
# macOS: brew install bubblewrap

# 7. 本 skill
npx skills add Chasen-Liao/Chasen-Skills --skill cli-dispatch --global --yes

# 8. 工作目录
export DISPATCH_HOME="${DISPATCH_HOME:-$HOME/.pi-dispatch}"
mkdir -p "$DISPATCH_HOME"/{tasks,out,logs,status,runs}

# 9. 冒烟（将 SKILL_ROOT 换成你的 skill 安装路径，或在仓库根目录用 ./cli-dispatch/...）
SKILL_ROOT="$(pwd)"   # 示例：克隆仓库后
"$SKILL_ROOT/cli-dispatch/scripts/pi-run.sh" --profile write "$DISPATCH_HOME/out" \
  -p '在本目录写 ok.txt，内容为 ok' --expect "$DISPATCH_HOME/out/ok.txt"
# 期望最后一行含 OK，退出码 0
```

---

## 🗣️ 怎么用

### 在 Agent 中（推荐）

> `这个大改动按 cli-dispatch 派给 Pi` / `写任务书让本地 pi-run 扫盘`

Agent 读 `SKILL.md`，写四段任务书，调用 `scripts/pi-run.sh`。

### 命令行示例

```bash
export DISPATCH_HOME="${DISPATCH_HOME:-$HOME/.pi-dispatch}"
R="./scripts/pi-run.sh"

"$R" --profile code ~/my-repo -p 'npm test 并修失败' --expect ~/my-repo/.pi-ok
"$R" --profile scan --model pro --task "$DISPATCH_HOME/tasks/inventory.md"
"$R" --profile scan --bg --task ./task.md   # 输出 run_id → status/<run_id>.json
```

完整参数见 [references/pi-run.md](./references/pi-run.md)。

---

## 一键同款：发给你的 Bot

把下面整段复制给你的 Agent（Cursor / Pi / Claude 等），让它在本机端到端装好并跑通冒烟；**遇到 Google 登录时停下来请你操作**；只有冒烟打出 `OK` 才算完成。

```text
请在本机按 cli-dispatch skill 完成 Pi + Magpie 派活环境的一键安装与验收（仓库 Chasen-Liao/Chasen-Skills，skill 名 cli-dispatch）。严格按顺序：

1) curl -fsSL https://pi.dev/install.sh | sh
2) curl -fsSL https://usemagpie.ai/install.sh | sh
3) 运行 magpie accounts add antigravity；出现 Google 登录或浏览器授权时立即停止，提示我完成登录后再继续
4) 在后台或独立终端运行 magpie serve（仅本机，禁止 --lan 与 --web）
5) pi install npm:pi-magpie
6) 安装 bubblewrap（Linux: apt install bubblewrap；macOS: brew install bubblewrap）
7) npx skills add Chasen-Liao/Chasen-Skills --skill cli-dispatch --global --yes
8) export DISPATCH_HOME=$HOME/.pi-dispatch && mkdir -p $DISPATCH_HOME/{tasks,out,logs,status,runs}
9) 找到已安装的 cli-dispatch/scripts/pi-run.sh，执行：
   pi-run.sh --profile write "$DISPATCH_HOME/out" -p '在本目录写 ok.txt，内容为 ok' --expect "$DISPATCH_HOME/out/ok.txt"

验收标准：上一步退出码 0，标准输出含 OK，且 $DISPATCH_HOME/out/ok.txt 内容为 ok。把安装路径、magpie serve 是否在跑、以及冒烟完整输出回报给我。若任一步失败，说明原因并停，不要跳过沙箱或使用 --no-sandbox。
```

---

## 📦 目录

```text
cli-dispatch/
├── SKILL.md
├── README.md
├── scripts/
│   ├── pi-run.sh
│   └── lib/
│       ├── pi-netfwd.py
│       └── pi-wrappers/   # curl git rm sudo wget
├── templates/TASK_TEMPLATE.md
└── references/pi-run.md
```

---

## Changelog

### 0.3.0

- 入库通用 `scripts/pi-run.sh` + `lib/`（bwrap、Magpie 转发、wrapper、quota、status JSON）。
- 移除 agy / Antigravity CLI 备用路径；仅保留 `magpie accounts add antigravity`。
- `DISPATCH_HOME` 默认改为 `~/.pi-dispatch`；文档中文化与一键安装提示。

### 0.2.0

- 执行主力改为 Pi（经 Magpie）；agy 为备用（已在 0.3.0 移除）。

### 0.1.0

- 首版 dispatch 工作流通用化。

---

## 📄 License

MIT © Chasen-Liao
