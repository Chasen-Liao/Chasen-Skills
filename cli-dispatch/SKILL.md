---
name: cli-dispatch
description: >-
  Bot 额度贵时：Bot 只拆任务、写任务书、派活与验收，具体执行交给本地 Pi（经 Magpie 网关用
  本机已登录的订阅/API 额度）。编码、批量改文件、扫盘、生成/整理内容等超过两轮工具调用的活，开干前先读此 skill。
license: MIT
compatibility: 需本地 Pi、Magpie 网关（至少一个 magpie accounts add 或 API provider）、bubblewrap、scripts/pi-run.sh；推荐 DISPATCH_HOME、PI_MODEL
metadata:
  author: Chasen-Liao
  version: "0.3.1"
  category: workflow
---

# cli-dispatch

## 前置条件 / 首次安装

按顺序完成（详情见 `README.md`）：

1. 安装 Pi：`curl -fsSL https://pi.dev/install.sh | sh`
2. 安装 Magpie：`curl -fsSL https://usemagpie.ai/install.sh | sh`
3. 添加 **Magpie 订阅账号**（任选其一，见 README 列表）：如 `magpie accounts add codex`、`magpie accounts add claude`、`magpie accounts add copilot`、`magpie accounts add gemini`、`magpie accounts add antigravity`（**风险**：用订阅经网关反代可能违反对应服务条款，有封号/停用风险，请用不怕丢的账号）
4. `magpie serve`（仅本机回环，**不要** `--lan` / `--web`）
5. `pi install npm:pi-magpie`
6. 安装 bubblewrap（如 `apt install bubblewrap` / `brew install bubblewrap`）
7. `npx skills add Chasen-Liao/Chasen-Skills --skill cli-dispatch --global --yes`
8. 设置 `export PI_MODEL='<provider>/<model>'`（与 Magpie 目录中一致，如 `codex/gpt-5.5-codex`），再跑冒烟：`scripts/pi-run.sh --profile write "$DISPATCH_HOME/out" -p '在本目录写 ok.txt，内容为 ok' --expect "$DISPATCH_HOME/out/ok.txt"`（应先 `export DISPATCH_HOME=~/.pi-dispatch` 并 `mkdir -p` 子目录）

`DISPATCH_HOME` 默认 `~/.pi-dispatch`，含 `tasks/`、`out/`、`logs/`、`status/`、`runs/`。

## 原则

远端 Agent 额度稀缺。**Bot 只负责**：拆任务、写任务书、派活、验收。执行走共用电脑上的 `scripts/pi-run.sh`（Pi + Magpie）。

- 默认派 **Pi**（经 Magpie，模型由 `PI_MODEL` / `--model` 指定）：编码、改项目、扫文件、批量整理、写初稿。
- 必须用 Bot 自有工具的活（连接器、发消息、浏览器、记忆）仍由 Bot 自己做。
- 一两步能自己做完的小事不用派。
- **删除、发送、付款、发帖** 永远不派给 CLI。
- **永远不用 `--no-sandbox`**。

## 步骤

1. **拆解**：拆成单个可验收的小任务，任务书尽量短。
2. **写任务书**：复制 `templates/TASK_TEMPLATE.md`（四段）到 `$DISPATCH_HOME/tasks/<日期>-<短名>.md`，产物写**绝对路径**。简单任务可直接 `-p`。
3. **选权限档**（每次运行自动生成沙箱）：
   - `scan`：只读 `$HOME` 与 `DISPATCH_RO_ROOTS`，只写 `--out`。
   - `code <项目目录>`：只读写该项目，可跑测试/构建。
   - `write <产物目录>`：只读写该目录。
   - 硬拦：`curl`、`wget`、`sudo`、`git push`、`rm -r`；沙箱断网，仅连 `MAGPIE_ADDR`。
4. **执行**：只走 `scripts/pi-run.sh`，不裸跑 `pi`：
   - `$R --profile scan --out <目录> --task tasks/<文件>.md`（`--task` 会把任务书里的产物当 `--expect`）
   - `$R --profile code <项目> -p '...' --expect <产物>`
   - `--model` 为 Magpie 的 `provider/model`（或设 `PI_MODEL`）；Pi 侧等价 `--provider magpie --model <该 id>`。`--thinking` 默认 **medium**；复杂任务或要求高质量完成时用 **`--thinking high`**。
   - 长任务 `--bg`：打印 `run_id`，读 `$DISPATCH_HOME/status/<run_id>.json`；勿反复轮询。
5. **验收**：
   - 前台：`OK` + 退出 0；`denied_actions` 非空即整次 FAIL。
   - 后台：看 status 的 `status`、`reason`、`artifacts`、`usage`。
   - 脚本通过后仍抽查产物与成功标准。
6. **不合格**：补任务书重派，最多两次；仍不行换 `--model` / 更大模型，再不行由 Bot 接手或上报用户。
7. **回报**：结论与产物路径；可附 status 中 token 用量。

## 注意

- 默认超时 20m（`--timeout`），排队上限 60m，Pi 最多并发 2，日志保留 14 天。
- 运行前 `magpie quota`：若当前订阅含 Gemini 5 小时窗口且 >90% → `FAIL: quota`。
- Magpie 无响应时在本机执行 `magpie serve`。
- 参数与环境变量见 `references/pi-run.md`。
