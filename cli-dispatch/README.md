# 🚦 cli-dispatch

> Bot 只拆任务和验收，**重活直接交给本机 Pi 的无头模式（`pi -p`）** — 省 Bot 额度，不用任何包装脚本。

<p>

![Executor](https://img.shields.io/badge/Executor-pi_--p-0ea5e9?style=flat-square)
![Thinking](https://img.shields.io/badge/thinking-medium-64748b?style=flat-square)
![Version](https://img.shields.io/badge/version-0.4.0-7c3aed?style=flat-square)

</p>

---

## ✨ 能做什么

| 能力 | 说明 |
| :--- | :--- |
| **🧠 Bot 减负** | 远端 Bot 只做拆解、任务说明、派活、验收 |
| **⚡ 直接 `pi -p`** | 一条命令派活，provider / model 随本机配置（可经 Magpie 网关） |
| **🔔 自动唤醒** | Bot 用自己的 Shell 后台跑，Pi 一退出 Bot 就被唤醒，不用轮询 |
| **👀 按需看进度** | `--mode json` 写日志，`rg` 一行看最近工具和是否 `agent_end` |
| **✅ Bot 自己验收** | 看产物和 diff，不合格最多重派两次 |

> ⚠️ 没有沙箱：Pi 能读写删本机任意文件、能联网。只在信任的机器上用，任务说明里写清边界；删除、发送、付款、发帖永远不交给 Pi。

---

## 🚀 安装

```bash
# 1. Pi
curl -fsSL https://pi.dev/install.sh | sh

# 2. 配一个 provider（示例：Magpie 网关，仅本机，不要 --lan / --web）
curl -fsSL https://usemagpie.ai/install.sh | sh
magpie accounts add <codex|claude|copilot|gemini|antigravity>   # ⚠️ 订阅经反代可能违反服务条款
magpie serve
pi install npm:pi-magpie

# 3. 本 skill
npx skills add Chasen-Liao/Chasen-Skills --skill cli-dispatch --global --yes

# 4. 冒烟
mkdir -p ~/.pi-dispatch/logs ~/.pi-dispatch/out
pi -p '在 ~/.pi-dispatch/out/ok.txt 写入 ok' --provider magpie --model <model> \
  --thinking medium --no-session --mode json > ~/.pi-dispatch/logs/smoke.jsonl 2>&1
cat ~/.pi-dispatch/out/ok.txt   # 期望输出 ok
```

---

## 🗣️ 怎么用

对你的 Bot 说：

> `这个改动按 cli-dispatch 派给 Pi`

Bot 会：写一段短的任务说明（目标、产物绝对路径、完成标准、边界）→ 用自己的 Shell 后台跑下面这条 → 被唤醒后验收。

```bash
pi -p '<任务说明>' --provider <provider> --model <model> \
  --thinking medium --no-session --mode json > ~/.pi-dispatch/logs/<短名>.jsonl 2>&1
```

| 场景 | 加什么 |
| :--- | :--- |
| 难活 | `--thinking high`（小活别开） |
| 只读扫描 | `--tools read,ls,grep,find` |
| 看进度 | `rg -o '"toolName":"\w+"' <日志> \| tail -5` |
| 是否跑完 | `rg -q '"type":"agent_end"' <日志>` |

---

## 📦 目录

```text
cli-dispatch/
├── SKILL.md
├── README.md
└── templates/TASK_TEMPLATE.md
```

---

## Changelog

### 0.4.0

- 去掉 `scripts/pi-run.sh`、`lib/` 和 `references/pi-run.md`，不再用包装脚本。
- SKILL 改为教 Bot 直接用 `pi -p` 无头模式派活：Shell 后台运行、Pi 退出自动唤醒、`--mode json` 日志按需看进度、`agent_end` 表示完成。
- 保留任务说明模板、Bot 自己验收、最多重派两次、删/发/付/发帖不交给 Pi，加上无沙箱风险提示。

### 0.3.1

- 判定 heredoc 改用 `transport_fail_texts(events, err)`，仅提取 Pi 自身错误事件与 stderr，避免工具输出或模型正文误触发认证/网络失败判定。
- `resolve_model()` 优先读取环境变量 `PI_MODEL_ALIASES`（逗号分隔 `短名=完整id`）进行短名映射，命中后走现有补全逻辑。
- `--task` 自动提取产物路径的正则支持通过环境变量 `DISPATCH_EXPECT_ROOTS`（逗号分隔）配置前缀，默认 `workspace,tmp,home,Users,var`。
- 文档补充 `PI_MODEL_ALIASES`、`DISPATCH_EXPECT_ROOTS` 说明，强调调用方 PATH 原样传进沙箱需包含 node/npm 等运行时，以及工作区不在 `$HOME` 下时必须设 `DISPATCH_RO_ROOTS`。

### 0.3.0

- 改为纯 **Pi + Magpie**：入库 `scripts/pi-run.sh` + `lib/`，`DISPATCH_HOME` 默认 `~/.pi-dispatch`，文档与一键安装提示。
- Pi `--thinking` 默认 **medium**；复杂或高质量任务使用 **`--thinking high`**。
- Magpie **不限定 Antigravity**：文档与 `PI_MODEL` 通用化，支持 CLI 确认的多种 `magpie accounts add` 订阅。

### 0.2.0

- 执行主力改为 Pi（经 Magpie）。

### 0.1.0

- 首版 dispatch 工作流通用化。

---

## 📄 License

MIT © Chasen-Liao
