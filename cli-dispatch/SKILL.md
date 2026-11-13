---
name: cli-dispatch
description: >-
  无 pi-task 时的极简原生 pi -p 派活方案：Bot 额度贵且本机仅装了原生 Pi 时，Bot 只拆任务、写任务书、直接用 pi -p
  后台派活与验收（若已装 pi-task 多 Bot 队列，请改用 grokbot-pi-dispatch）。触发：用 pi -p 派活 / 按 cli-dispatch 派活。
license: MIT
compatibility: 需本机已安装原生 Pi（pi -p）并配好可用 provider/model；Bot 需有可后台运行的 Shell 工具
metadata:
  author: Chasen-Liao
  version: "0.6.0"
  category: workflow
---

# cli-dispatch

无 `pi-task` 依赖的原生 `pi -p` 极简派活方案。若本机已部署 `pi-task` 多 Bot 队列与 `pending/ack` 机制，请改用 `grokbot-pi-dispatch`。

## 原则

远端 Bot 额度稀缺。**Bot 只负责**：拆任务、写任务说明、用 `pi -p` 派活、验收产物。

- 超过两三步的执行（编码、改项目、扫文件、批量整理、写初稿）一律派 Pi；一两步能做完的小事或必须用 Bot 自有工具（连接器、发消息、浏览器、记忆）的活由 Bot 自己做。
- **删除、发送、付款、发帖、push** 永远不交给 Pi。
- ⚠️ 直接跑 `pi -p` 没有沙箱：Pi 能读写删本机任意文件、能联网。只在信任的机器上用，任务说明里写清边界。

## 前置

确认本机已装好 `pi` 且 `pi --list-models` 可见目标 provider/model，并准备好日志目录（如 `mkdir -p ~/.pi-dispatch/logs`）。

## 步骤

1. **拆解**：拆成单个可验收的小任务。
2. **写任务说明**（越短越好，直接按以下 5 项内联拼入 `-p`）：
   - **目标**：一句话写清要做什么（带上必要背景，Pi 看不到聊天）
   - **产物**：`/absolute/path/to/output`
   - **完成标准**：每个产物必须存在且非空，内容要满足什么，需要跑哪些测试
   - **边界**：只改 `<目录>`，其余只读；不要删除任何文件；不要 `git push`、发送、付款或发帖
   - **收尾**：写完产物自查一次就结束，不要反复自查或重试
3. **派活**：用 Bot 自己的 Shell 工具**后台**运行（`block_until_ms: 0`）：

   ```bash
   pi -p '<任务说明>' --provider <provider> --model <model> \
     --thinking medium --no-session --mode json > ~/.pi-dispatch/logs/<短名>.jsonl 2>&1
   ```

   - 例：`--provider magpie --model antigravity/gemini-3.8-flash`（按本机可用模型填写）。
   - Pi 一退出后台命令即结束，Bot 会被自动唤醒，**不要轮询或 sleep**；派完立刻结束当前轮（避免完成通知被并入未结束的同一轮）。
   - **不要前台阻塞等 Pi，也不要用 `nohup` 或 `&`**（否则 Bot 收不到完成通知）。
   - `--thinking` 默认 `medium`，只有难活才开 `high`（小活开 `high` 易乱翻文件、烧 token）；只读任务加 `--tools read,ls,grep,find`。
4. **跑完唤醒**：
   - 默认：Shell 后台命令退出即自动唤醒；此外**每轮开头检查未验收日志**，含 `agent_end` 就立刻验收。
   - 可选 webhook：若 Bot 已配好唤醒例行任务及环境变量 `PI_NOTIFY_URL`、`PI_NOTIFY_KEY`，在派活命令末尾接：

     ```bash
     ; curl -s -X POST "$PI_NOTIFY_URL" -H "Authorization: Bearer $PI_NOTIFY_KEY" \
         -H 'Content-Type: application/json' -d '{"name":"<短名>","log":"<日志路径>"}'
     ```

5. **看进度**（只在用户问起时看，别反复查）：
   - `rg -o '"toolName":"\w+"' <日志> | tail -5`：最近在用哪些工具
   - `rg -q '"type":"agent_end"' <日志>`：能匹配上就表示已跑完
6. **验收**（Bot 自己做，不能只看退出码）：看退出码，检查产物是否存在、非空、符合完成标准；必要时跑测试或看 `git diff`，确认未改出界。
7. **不合格**：补充说明后重派，**最多两次**；仍不行换更强模型或开 `--thinking high`，再不行由 Bot 接手或上报用户。
8. **回报**：只报结论和产物路径，不转贴日志。
