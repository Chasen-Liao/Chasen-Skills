---
name: cli-dispatch
description: >-
  Bot 额度贵时：Bot 只拆任务、写任务书、派活与验收，具体执行交给本地 Antigravity CLI（agy，走
  Google/Gemini 订阅）或备用 Pi。编码、批量改文件、扫盘、生成/整理内容等超过两轮工具调用的活，开干前先读此 skill。
license: MIT
compatibility: 需已安装并可登录 agy；推荐配置 DISPATCH_HOME；无头环境需 dbus/keyring；可选 Pi 作备用
metadata:
  author: Chasen-Liao
  version: "0.1.0"
  category: workflow
---

# cli-dispatch

## 前置条件 / 首次安装

1. **安装 agy（Antigravity CLI）**：按 Antigravity 官方文档安装，并用自己的 Google 账号完成登录。
2. **工作目录**：设置 `DISPATCH_HOME`（默认 `~/.agy-dispatch`）。首次使用前创建 `tasks/`、`out/` 等子目录（或由 Bot 按需 `mkdir -p`）。
3. **账号与模式**：部分 Google 账号不支持 `agy --mode auto`；包装脚本会自动忽略该参数。
4. **Keyring / dbus**：agy 登录态常放在系统 keyring，依赖 dbus 会话。无头或 SSH 环境若 agy 报未登录，让管电脑环境的人配置 `AGY_XDG_RUNTIME_DIR` / `AGY_DBUS_SESSION_BUS_ADDRESS`，或在本机会话里重新登录 agy。
5. **可选备用**：安装 Pi，在 agy 额度用尽或任务明显不适合 CLI 时改派 Pi。
6. **安装本 skill**：`npx skills add Chasen-Liao/Chasen-Skills --skill cli-dispatch --global --yes`

## 原则

Grok Bot（或其他远端 Agent）额度稀缺。**Bot 只负责**：拆任务、写任务书、派活、验收。具体执行交给共用电脑上的 CLI。

- 默认派给 **agy**（模型默认 `gemini-3.8-flash-high`，可用 `AGY_MODEL` 覆盖）：编码、改项目、扫文件、批量整理、写初稿素材。
- **Pi 仅备用**：agy 不可用、额度用尽或明显不适合时才用。
- 必须用 Bot 自有工具的活（连接器、发消息、浏览器、记忆、routine）仍由 Bot 自己做。
- **删除、发送、付款、发帖** 永远不派给 CLI。

## 步骤

1. **拆解**：把需求拆成单个可验收的小任务。任务书越短越好（agy 长思考也会耗大量 token）。
2. **写任务书**：复制 `templates/TASK_TEMPLATE.md`（四段）到 `$DISPATCH_HOME/tasks/<日期>-<短名>.md`，写明产物**绝对路径**（见「成功标准」）。
3. **选权限档**（每次运行自动生成会话级 settings，无需找人临时放行）：
   - `scan`：只读 `AGY_SCAN_READ_DIRS`（默认 `$HOME`，冒号分隔多目录），只写 `--out`（默认 `$DISPATCH_HOME/out`）；命令仅 `du`、`ls`、`stat`、`sha256sum`。
   - `code <项目目录>`：只读写该项目；放行测试/构建命令与只读 git。
   - `write <产物目录>`：只读写该目录；不放 shell 命令。
   - 三档都禁 `git push`、`rm -r`、`sudo`、`curl`、`wget`、`bash -c`。
4. **执行**：走 `scripts/agy-run.sh`，不直接裸跑 agy：
   - `R=<skill-root>/scripts/agy-run.sh`
   - `$R --profile scan --out <目录> --task tasks/<文件>.md`（`--task` 会从任务书提取默认 `--expect`）
   - `$R --profile code <项目目录> -p '<指令>' --expect <产物>`
   - 长任务加 `--bg`：立刻打印 `run_id`，结果在 `$DISPATCH_HOME/status/<run_id>.json`；后台跑完后读状态文件验收，勿 busy-poll。
5. **验收**：
   - 前台：`OK <产物>` 且退出码 0；`FAIL: 原因` 表示被拒、agy 失败或产物缺失/为空（headless 下 agy 有时仍报 SUCCESS，以脚本的 `denied_actions`、状态与产物为准）。
   - 后台：`--bg` 的退出码 0 只表示已转入后台；看状态文件里的 `status`、`reason`、`artifacts`、`usage`。
   - 脚本通过后仍应抽查产物是否符合成功标准（必要时跑测试或 diff）。日志在 `$DISPATCH_HOME/logs/`。
6. **不合格**：补任务书后重派，最多两次；仍不行由 Bot 接手或上报用户。
7. **回报**：只汇报结论与产物路径，不转贴日志；可附 token 用量。

## 注意

- 永远不要加 `--dangerously-skip-permissions`；需要档位外权限时，找**管电脑环境的人或 Bot** 改包装脚本/环境变量，不要自行放开全局。
- agy 通常查不到剩余订阅额度，只能看单次 `usage`；额度用尽时改派 Pi 或上报，勿硬重试。
- 机器重建或会话过期后 agy 可能需重新登录，找管环境的人处理。
- 包装脚本、环境变量与示例见 `references/agy-run.md`。
