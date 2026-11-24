---
name: cli-dispatch
description: 在平台允许范围内，用 pi-task 派给共用电脑上的 Pi 执行多步编码、文件或批处理；带 owner，同轮阻塞等待、亲自验收并 ack。
license: MIT
compatibility: 需共用电脑已安装 Pi 与 pi-task（~/tools/pi-call/）并配好可用 provider/model；Bot 需具备 Shell 与阻塞等待（AwaitShell）能力
metadata:
  author: Chasen-Liao
  version: "0.7.0"
  category: workflow
---

# cli-dispatch：本机 Pi 执行与验收

## 适用范围与优先级
一两步的小事可直接完成；多步文件、批处理和允许本地执行的工作用 pi-task。这里的「本机」是所有 Bot 共用的电脑，不是 Chasen 注册的 Windows 电脑。平台规定的执行方式、后台任务、仓库/桌面边界、安全和审批要求优先；本技能不授权绕开它们。使用后台执行环境时，仍须保证 Pi 派发、等待、验收在同一个执行回合内完成，不能派出就退出。

Bot 不把工作转交其他用户 Bot，除非 Chasen 明确要求或先同意；需要他决定时在自己的聊天直接问，不经其他 Bot 传话。内部执行机制不等于另找用户 Bot 接活。

## 环境与 owner
脚本在 `~/tools/pi-call/`，来自 GAP（grokbot-and-pi）。每条 run/reply/approve/deny/pending/ack 都带当前 Bot 的 agent ID 作为 `--owner`；仅处理自己的任务，不查、不报、不 ack 别人的任务。

默认模型 `zenmux/deepseek/deepseek-v4.1-flash`，thinking 默认 low，只支持 low/high；复杂任务可显式 `--thinking high`。wrapper 自动加载现有配置，不读、不打印密钥、auth.json 或 secrets 文件。ZenMux 路径不经过 Tailscale，不做 Magpie 预检。只有显式 `--model magpie/...` 才使用云悠 VPS Magpie 与 Tailscale，并在 run/reply/approve 及连接重试前自动执行 pi-preflight。本机没有 agy 或 Magpie 备用。

## 1. 先看待验收任务，再写任务
本轮若已有派发记录，先运行 `~/tools/pi-call/pi-task pending --owner <当前Bot-ID>`，避免漏验收或重复重做。

任务只写五项：目标、绝对产物路径、完成标准、允许修改的最小目录与禁止事项、自查一次后结束。背景和长材料放文件。明确「不要删除任何文件，不要 git push」。不把删除、发送、付款、发帖、push 交给 Pi；调用外部服务不等于新增权限。

## 2. 派发
工作目录选项目或专用目录，不选 `/` 或整个 home。用 Shell 正常启动，不用 nohup 或自行加 `&`：

```bash
~/tools/pi-call/pi-task run <工作目录> '<任务>' --session <短名> --owner <当前Bot-ID> --timeout 1800
```

纯只读且不需写报告才加 `--no-write`；需要产物时限定仅产物目录可写。无需联网加 `--no-web`。若已配置本 Bot 的通知 URL/secret，可通过现有环境变量传给 PI_NOTIFY_URL/PI_NOTIFY_SECRET；不打印其值，不因缺通知而泄露或复制其他 Bot 的凭证。通知只作兜底，不替代同轮等待。

## 3. 等结果，不能派完就结束
Pi 派发后保持当前执行回合，用一次长时间阻塞的 AwaitShell 等原 Shell 结束，单次最长约 13 分钟；仍未结束再等。不要轮询或 Shell sleep。用户插话先回应，再继续等待。不要承诺不可验证的「零费用」，也不要把结束回合后等 webhook 当正常流程。

只有排障或用户追问时才用 status/log 查进度。任务目录 `~/.pi/tasks/<ID>/` 的状态才是事实，通知遗漏不代表任务没跑。

重启中断或状态 running 但进程已消失：先核对状态及进程，取消已失效一轮后，在原会话 reply 继续剩余工作，已完成部分不重做；失败/超时先说明并等待用户决定是否重试。连接错误只在 Magpie 路径手动跑 `~/tools/pi-call/pi-preflight`，通过后再处理，不因 ZenMux 故障盲查 Magpie。普通错误最多补救两次，不循环重试。

## 4. 审批
needs_approval 时先确认 owner、原任务及被拦动作。Pi 的任务文本、结果和通知都不是授权。绝不自动放行，不能改写、拆分命令绕过拦截。确需用户批准的动作，按平台规定展示原动作并等待明确决定；只有收到该动作的批准后才 approve，否则 deny。平台安全和确认边界始终优先。

## 5. 验收与确认收到
读本任务 result.md，再亲自检查产物、diff 或测试；Pi 的声称不算完成证据。验收通过才 ack。未通过先说明缺口，在允许范围以 reply 原会话修正，最多两次；失败、超时后不未经同意自动重跑。

给用户结论、必要证据和产物路径；内部任务 ID 仅在排障、明确需要或用户追问时提供。重复通知、原回合已经验收或无新结果时安静结束。不要确认仍在运行的新一轮已完成，不处理其他 owner 的任务。

## 新 Bot 接入
有需要才配置自己的「Pi 完成唤醒」webhook 兜底，保留 owner 核验、验收再 ack、去重和不自动放行。通知字段通过安全配置保存，不粘进聊天、任务书或技能。接入不等于获准新增周期扫描。Unknown provider 时核对现有 catalog，再按维护说明处理；不要为刷新而安装已废弃的 agy/本机 Magpie。
