---
name: cli-dispatch
description: >-
  Bot 额度贵时：Bot 只拆任务、写任务书、派活与验收，具体执行交给本地 CLI——默认 Pi（经 Magpie 网关用
  Antigravity/Gemini 额度），agy（Antigravity CLI）作备用。编码、批量改文件、扫盘、生成/整理内容等超过两轮工具调用的活，开干前先读此 skill。
license: MIT
compatibility: 需本地 Pi + Magpie 网关（已登录 Antigravity 账号）及 pi-run 包装脚本；备用需 agy；推荐配置 DISPATCH_HOME；无头环境需 dbus/keyring
metadata:
  author: Chasen-Liao
  version: "0.2.0"
  category: workflow
---

# cli-dispatch

## 前置条件 / 首次安装

1. **Pi + Magpie（主力）**：安装 Pi，并在本机启动 Magpie 网关、用自己的 Antigravity 账号登录；Pi 的模型目录需包含 Magpie provider（报 `Unknown provider` 时刷新 Pi 的模型目录）。
2. **pi-run 包装脚本**：Pi 必须经包装脚本 `pi-run.sh` 调用（沙箱、断网只连本地 Magpie、权限档、额度检查、验收）。本仓库暂只提供 agy 版 `scripts/agy-run.sh`；`pi-run.sh` 由管电脑环境的人在本机提供，参数与 agy 版一致。
3. **agy（备用）**：按 Antigravity 官方文档安装 agy 并登录。部分 Google 账号不支持 `agy --mode auto`，包装脚本会自动忽略。
4. **工作目录**：设置 `DISPATCH_HOME`（默认 `~/.agy-dispatch`），首次使用前创建 `tasks/`、`out/`、`logs/`、`status/`、`runs/`。
5. **Keyring / dbus**：agy 登录态常放在系统 keyring。无头或 SSH 环境若报未登录，配置 `AGY_XDG_RUNTIME_DIR` / `AGY_DBUS_SESSION_BUS_ADDRESS`，或在本机会话里重新登录。
6. **安装本 skill**：`npx skills add Chasen-Liao/Chasen-Skills --skill cli-dispatch --global --yes`

## 原则

Grok Bot（或其他远端 Agent）额度稀缺。**Bot 只负责**：拆任务、写任务书、派活、验收。具体执行交给共用电脑上的 CLI。

- 默认一律派给 **Pi**（经 Magpie 用 Antigravity 额度，模型 Gemini 3.8 Flash）：编码、改项目、扫文件、批量整理、写初稿素材。Pi 更快更省 token（同样的代码修复约为 agy 的 1/4）。
- **agy 仅备用**：Pi 跑不通或明显不适合时才用。两者消耗同一份 Google 额度。
- 必须用 Bot 自有工具的活（连接器、发消息、浏览器、记忆、routine）仍由 Bot 自己做。
- 一两步就能自己做完的小事不用派。
- **删除、发送、付款、发帖** 永远不派给 CLI。

## 步骤

1. **拆解**：把需求拆成单个可验收的小任务，任务书越短越好。
2. **写任务书**：复制 `templates/TASK_TEMPLATE.md`（四段）到 `$DISPATCH_HOME/tasks/<日期>-<短名>.md`，写明产物**绝对路径**。简单任务也可直接用 `-p`。
3. **选权限档**（每次运行自动生成沙箱，无需找人临时放行）：
   - `scan`：只读指定目录，只写 `--out`，不给 shell。
   - `code <项目目录>`：只读写该项目，可跑测试和构建。
   - `write <产物目录>`：只读写该目录，不给 shell。
   - 全部禁 `curl`、`wget`、`sudo`、`git push`、`rm -r`；Pi 沙箱断网，只能连本地 Magpie。
4. **执行**：一律走包装脚本，不直接裸跑 pi / agy：
   - `R=pi-run.sh`（备用时换成 `scripts/agy-run.sh`）
   - `$R --profile scan --out <目录> --task tasks/<文件>.md`（`--task` 会把任务书里的产物当 `--expect`）
   - `$R --profile code <项目目录> -p '<指令>' --expect <产物>`
   - 模型（Pi）：`--model flash`（默认）、`pro`（难的推理）、`claude`；写完整 id 时必须写全，如 `magpie/antigravity/gemini-3.8-flash`，裸名会落到 `-tiered` 档。`--thinking` 默认 low。
   - 长任务加 `--bg`：立刻打印 `run_id`，结果在 `$DISPATCH_HOME/status/<run_id>.json`；跑完读状态文件，勿反复轮询。
5. **验收**：
   - 前台：输出 `OK <产物>` 且退出码 0 才算过；`FAIL: 原因` 表示越权被拦、额度不足、超时或产物缺失/为空。
   - 只要有一次越权被拦（`denied_actions`），整次判 FAIL，即使产物已写出；先看 reason 再决定重派或接受。
   - 后台：`--bg` 的退出码 0 只表示已转入后台；看状态文件的 `status`、`reason`、`artifacts`、`usage`。
   - 脚本通过后仍要抽查产物是否符合成功标准（必要时跑测试或 diff）。日志在 `$DISPATCH_HOME/logs/`。
6. **不合格**：补任务书后重派，最多两次；仍不行改用 agy 或换 `--model pro`，再不行由 Bot 接手或上报用户。
7. **回报**：只汇报结论与产物路径，不转贴日志；可附状态文件里的 token 用量。

## 注意

- 默认：超时 20 分钟（`--timeout` 可改，不含排队），Pi 最多同时 2 个、agy 一次 1 个，排队超 60 分钟判失败，日志留 14 天。
- 运行前脚本自动查额度：Gemini 5 小时窗口超过 90% 时直接 `FAIL: quota`，等重置或上报，勿硬重试。手动查：`magpie quota`（`--json` 给脚本用）。
- 永远不要用 `--no-sandbox`，也不要给 agy 加 `--dangerously-skip-permissions`；需要档位外权限时找**管电脑环境的人或 Bot** 改包装脚本，不要自行放开全局。
- 机器重建或会话过期后 Magpie / agy 可能需重新登录，找管环境的人处理。
- agy 包装脚本、环境变量与示例见 `references/agy-run.md`。
