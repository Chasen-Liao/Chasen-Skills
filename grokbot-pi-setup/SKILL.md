---
name: grokbot-pi-setup
description: 第一次让 Grok Bot 把执行活派给电脑上的 Pi 之前用：在 Bot 的电脑上装 Pi、给 Pi 接一个模型（任意 API key、中转站或网关）、装 pi-task 并配好「Pi 跑完自动叫醒 Bot」的 webhook，并跑通一次验收。装好后日常派活看 grokbot-pi-dispatch。
---

# grokbot-pi-setup：让 Grok Bot 能派活给 Pi

目标：Grok Bot 额度贵，只用来「拆任务 + 验收」；真正干活交给 Bot 电脑上的 Pi（无头 coding agent），Pi 用什么模型都行（DeepSeek、中转站、Magpie 等），花的是你自己的额度。

做完应该满足三条：
1. Bot 的 Shell 里 `pi -p 'reply ok' --provider <provider> --model <model> --no-session` 回复 ok。
2. `~/tools/pi-call/pi-task` 能跑，有一个 webhook 例行任务能把 Bot 单独叫醒。
3. 两个密钥 `<BOT>_PI_NOTIFY_URL`、`<BOT>_PI_NOTIFY_KEY` 已存好，Bot 不在聊天里打印它们。

按下面顺序做，每步验收过再往下走。删除、付款、登录这类动作先问用户。

## 1. 装 Pi
- 在 Bot 的电脑上按 Pi 官方文档安装，确认 `pi --version` 能跑。
- 先用任意一个现成 provider 跑通 `pi -p 'reply ok' --no-session`，证明 Pi 本身没问题。

## 2. 给 Pi 接一个模型（来源随意）
Pi 能用的模型都行，挑你手上有的：
- 直接用 API key：DeepSeek、OpenRouter、各家中转站等，按 Pi 文档把 provider 写进 Pi 的配置（`~/.pi/agent/models.json` 或 `pi` 自带的登录）。
- 用网关统一管理（可选）：比如 Magpie，把订阅或各家 key（DeepSeek、中转站都行）统一接进去，再给 Pi 用。

不管哪种，最后只需要两样东西：一个 provider 名、一个模型名。验收：
```
pi -p 'reply ok' --provider <provider> --model <model> --no-session
```
回复 ok 就行。之后派活命令里都填这两个值。

### 网关放在另一台机器（可选）
如果用网关、又想多台电脑共用，可以把它放在 VPS 上：只监听内网地址（比如 Tailscale），**不要开公网端口**，并开启网关 key。

## 3. 装 pi-task 并配「跑完自动叫醒」
用 [robbin/grokbot-local-agent](https://github.com/robbin/grokbot-local-agent) 的脚本（Node 22+）：

```
git clone https://github.com/robbin/grokbot-local-agent /tmp/gla
mkdir -p ~/tools/pi-call && cp -a /tmp/gla/bin/. ~/tools/pi-call/ && chmod +x ~/tools/pi-call/*
```

它默认模型是 `deepseek/deepseek-flash`、thinking high；用别的模型就在派活时加 `--model <provider/model>`。
冒烟测试：`PI_NOTIFY_OFF=1 ~/tools/pi-call/pi-task run /tmp 'Reply with only OK' --session smoke --owner <ID>`，看到 `STATE done`，再 `pi-task ack <TASK> --owner <ID>`。

然后配唤醒：
1. Bot 自己建一个 webhook 触发的例行任务，比如「Pi 完成唤醒」。内容参考仓库里的 `routines/pi-task-notify.md`：醒来跑 `pi-task pending --owner <ID>`，按 grokbot-pi-dispatch 第 4 步验收、回报、ack；别的 Bot 的任务不碰。
2. 让用户用密钥输入卡，把 webhook 地址和 key 存成 `<BOT>_PI_NOTIFY_URL`、`<BOT>_PI_NOTIFY_KEY`（不要贴进聊天或文件）。共用一台电脑的多个 Bot 各用各的变量名，派活时再映射成 pi-task 读的 `PI_NOTIFY_URL`、`PI_NOTIFY_SECRET`。

## 4. 端到端验收
派一个最小任务（比如「在 /tmp/pi-test.txt 写一行 hello」），按 grokbot-pi-dispatch 的命令后台跑、结束当前轮。确认：Bot 被单独叫醒、`pi-task pending` 里有它、文件内容正确，ack 后 pending 变空。

## 风险，要跟用户说清楚
- Pi 默认没有沙箱，能改电脑上的任何文件。任务里必须限定目录、禁止删除。
- 如果把订阅反代给 agent 用，可能违反该订阅的服务条款，有封号风险，建议用小号。
- 密钥只存在密钥里，不写进文件、不打印。
