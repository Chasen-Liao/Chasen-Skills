---
name: grokbot-pi-dispatch
description: >-
  基于 pi-task 的 Grok Bot 队列派活与自动唤醒：超过两三步的执行活（写代码、改文件、扫目录、整理或生成内容）开干前读此 skill；
  Bot 写五要素任务书、用 pi-task 后台派给本机 Pi、被 webhook 叫醒后验收并 ack。还没装好先看 grokbot-pi-setup；
  无 pi-task 环境改用 cli-dispatch。触发：用 pi-task 派活 / 按 grokbot-pi-dispatch 派活。
license: MIT
compatibility: 需已完成 grokbot-pi-setup（本机已装 Pi、pi-task 及 webhook 唤醒）；Bot 需有可后台运行的 Shell 工具
metadata:
  author: Chasen-Liao
  version: "0.2.0"
  category: workflow
---

# grokbot-pi-dispatch：基于 pi-task 的队列派活与自动唤醒

Bot 只做三件事：写任务书、用 `pi-task` 后台派给 Pi、验收并 `ack`。一两步的小事 Bot 自己做，别派。
`pi-task` 来自 [robbin/grokbot-local-agent](https://github.com/robbin/grokbot-local-agent)，为每个任务维护独立 ID、状态目录与 `--owner` 归属，防止漏报或跨 Bot 串台。

> 下文涉及的 `~/tools/pi-call/pi-task`、`~/.pi/tasks/<ID>/`、`~/.pi/agent/auth.json` 及 `/home/box/agent-data/agents/<ID>/profile.json` 均为默认部署路径示例，实际按本机安装路径使用。

## 0. 确定 owner ID

以当前 Bot 的 agent ID 作为 `--owner <ID>`（标准 Grok Bot 部署中通常对应默认路径 `/home/box/agent-data/agents/<ID>/profile.json` 的目录名）。派活、`pending`、`ack` 均须携带 `--owner <ID>`。

## 1. 写任务书（越短越好）

只写五件事：
1. **要做什么**：一两句说清目标与必要背景（Pi 看不到聊天上下文）。
2. **产物路径**：产物写入哪个绝对路径。
3. **完成标准**：可检查的验收条件（存在性、内容要求、需跑的测试）。
4. **边界**：`只改 <目录>，遵守文末安全边界`。
5. **收尾**：`写完产物自查一次就结束，不要反复自查或重试`。

## 2. 后台派活

用 Bot 自己的 Shell 工具**后台**运行（不阻塞等待；不要用 `nohup`、`&`）：

```bash
PI_NOTIFY_URL="$<BOT>_PI_NOTIFY_URL" PI_NOTIFY_SECRET="$<BOT>_PI_NOTIFY_KEY" \
  ~/tools/pi-call/pi-task run <工作目录> '<任务书>' \
  --session <短名> --owner <ID> --model <provider/model> --thinking medium --timeout 1800
```

- **工作目录**：选最小范围（项目目录或 `/tmp/<名>`），不要传 `/` 或整个 home。
- **可选参数**：只读任务加 `--no-write`；无需联网加 `--no-web`；难活才开 `--thinking high`（默认 `medium`）；`--timeout 1800` 为单次执行超时上限（单位秒，按任务复杂度调整）。
- **追加说明**：用 `pi-task reply <ID> '<补充>'` 沿用同一会话与目录。
- **收尾回合**：派完告诉用户「已派出」，**立刻结束当前轮**，等待 webhook 单独叫醒。

## 3. 等结果

- **正常唤醒**：`pi-task` 结束时 POST `{source,id,owner,state,exit_code}`，由 webhook 例行任务把 Bot 叫醒。
- **醒来兜底**：每次醒来且此前派过活，先跑 `pi-task pending --owner <ID>` 确认待验收任务。
- **按需查看**：进度看 `pi-task status <ID>` / `pi-task log <ID> -n 20`；取消用 `pi-task cancel <ID>`。
- **事实真源**：硬盘上的默认状态目录 `~/.pi/tasks/<ID>/` 才是真相，漏收通知不要盲目重跑。

## 4. 验收并确认

1. 读 `~/.pi/tasks/<ID>/result.md`，并亲自检查产物、diff 或测试结果（Pi 的回复只是声称，不算证据）。
2. 向用户汇报：任务 ID、状态、结论、验收证据、产物路径。
3. 验收通过后执行 `pi-task ack <ID> --owner <ID>`；不过则不 `ack`，用 `pi-task reply` 补充说明重派（最多两次）。失败或超时先问用户是否重试。

## 边界与规矩

- **高危动作禁派**：删除、发送消息或邮件、付款、发帖、`git push` 永远不交给 Pi，由 Bot 在用户确认后自己做。
- **无沙箱限制**：Pi 可读写本机文件，任务书必须限定可改目录并禁止删除任何文件。
- **密钥隔离**：不读、不打印任何密钥或 `~/.pi/agent/auth.json`。
- **多 Bot 隔离**：永远带 `--owner <ID>` 过滤，不看、不报、不 `ack` 其他 Bot 的任务。
