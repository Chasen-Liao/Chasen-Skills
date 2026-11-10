---
name: cli-dispatch
description: >-
  Bot 额度贵时：Bot 只拆任务、写任务书、派活与验收，具体执行交给本机 Pi 的无头模式（pi -p）。编码、批量改文件、扫盘、
  生成/整理内容等超过两三步的活，开干前先读此 skill。
license: MIT
compatibility: 需本机已安装 Pi 并配好至少一个可用 provider（例如经 Magpie 网关）；Bot 需有可后台运行的 Shell 工具
metadata:
  author: Chasen-Liao
  version: "0.5.0"
  category: workflow
---

# cli-dispatch

## 原则

远端 Bot 额度稀缺。**Bot 只负责**：拆任务、写任务说明、派给 Pi、验收产物。

- 超过两三步的执行（编码、改项目、扫文件、批量整理、写初稿）一律派 Pi；一两步能做完的小事自己做。
- 必须用 Bot 自有工具的活（连接器、发消息、浏览器、记忆）仍由 Bot 自己做。
- **删除、发送、付款、发帖** 永远不交给 Pi。
- ⚠️ 直接跑 `pi -p` 没有沙箱：Pi 能读写删本机任意文件、能联网。只在你信任的机器上用，任务说明里写清边界。

## 前置

1. 安装 Pi：`curl -fsSL https://pi.dev/install.sh | sh`
2. 配好一个 provider，并确认 `pi --list-models` 能看到要用的模型。例如用 Magpie 网关：`magpie serve` + `pi install npm:pi-magpie`，provider 写 `magpie`。
3. 准备日志目录，例如 `mkdir -p ~/.pi-dispatch/logs`。

## 步骤

1. **拆解**：拆成单个可验收的小任务。
2. **写任务说明**（越短越好，可用 `templates/TASK_TEMPLATE.md`）：
   - 目标（一句话）
   - 产物绝对路径
   - 怎么算完成
   - 只改哪个目录；不要删除任何文件；不要 git push
   - 写完产物自查一次就结束，不要反复自查或重试
3. **派活**：用 Bot 自己的 Shell 工具**后台**运行（`block_until_ms: 0`）：

   ```bash
   pi -p '<任务说明>' --provider <provider> --model <model> \
     --thinking medium --no-session --mode json > <日志目录>/<短名>.jsonl 2>&1
   ```

   - 例：`--provider magpie --model antigravity/gemini-3.8-flash`（按你本机可用的模型填写）。
   - Pi 一退出，后台命令就结束，Bot 会被自动唤醒，**不要轮询或 sleep**。
   - 派完立刻结束当前轮。Pi 跑完时 Bot 如果还在一个没结束的轮里，完成通知会被并进那一轮，不会再单独叫醒。
   - **不要前台阻塞等 Pi，也不要用 `nohup` 或 `&`**（那样 Bot 收不到完成通知）。
   - `--thinking` 默认 `medium`；只有难活才开 `high`（小活开 high 容易乱翻文件、烧 token）。
   - 只读类任务加 `--tools read,ls,grep,find`，更省也更安全。
4. **跑完自动叫醒（推荐）**：给 Bot 建一个 webhook 触发的例行任务（内容：按本 skill 验收请求里日志对应的产物并回报用户），让用户把面板里的 POST to 地址和 key 存成 Bot 的两个密钥，例如 `PI_NOTIFY_URL`、`PI_NOTIFY_KEY`。派活命令末尾接一句：

   ```bash
   ; curl -s -X POST "$PI_NOTIFY_URL" -H "Authorization: Bearer $PI_NOTIFY_KEY" \
       -H 'Content-Type: application/json' -d '{"name":"<短名>","log":"<日志路径>"}'
   ```

   Pi 一退出就会单独开一轮去验收，不管 Bot 当时忙不忙；只在完成时触发，平时不花额度。没配的话，**每轮开头先查自己还没验收的日志**，有 `agent_end` 就立刻验收回报。
5. **看进度**（只在用户问起时看，别反复查）：
   - `rg -o '"toolName":"\w+"' <日志> | tail -5`：最近在用哪些工具
   - `rg -q '"type":"agent_end"' <日志>`：能匹配上就表示已跑完
6. **验收**（Bot 自己做，不能只看退出码）：看退出码，检查产物是否存在、非空、符合完成标准；必要时跑测试或看 `git diff`，确认 Pi 没有改出界。
7. **不合格**：补充说明后重派，**最多两次**；仍不行换更强的模型或开 `--thinking high`，再不行由 Bot 接手或上报用户。
8. **回报**：只报结论和产物路径，不转贴日志。
