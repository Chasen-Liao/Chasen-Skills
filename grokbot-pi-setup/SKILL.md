---
name: grokbot-pi-setup
description: 第一次让 Grok Bot 把执行活派给电脑上的 Pi 之前用：在 Bot 的电脑上装 Pi、用 Magpie 把自己的模型订阅接成 Pi 的 provider、配好「Pi 跑完自动叫醒 Bot」的 webhook，并跑通一次验收。装好后日常派活看 grokbot-pi-dispatch。
---

# grokbot-pi-setup：让 Grok Bot 能派活给 Pi

目标：Grok Bot 额度贵，只用来「拆任务 + 验收」；真正干活交给 Bot 电脑上的 Pi（无头 coding agent），Pi 的模型走你自己的订阅（经 Magpie 反代）。

做完应该满足三条：
1. Bot 的 Shell 里 `pi -p 'reply ok' --provider magpie --model <模型> --no-session` 回复 ok。
2. 有一个 webhook 例行任务，curl 一下能把 Bot 单独叫醒。
3. 两个密钥 `<BOT>_PI_NOTIFY_URL`、`<BOT>_PI_NOTIFY_KEY` 已存好，Bot 不在聊天里打印它们。

按下面顺序做，每步验收过再往下走。删除、付款、登录这类动作先问用户。

## 1. 装 Pi
- 在 Bot 的电脑上按 Pi 官方文档安装，确认 `pi --version` 能跑。
- 先用任意一个现成 provider 跑通 `pi -p 'reply ok' --no-session`，证明 Pi 本身没问题。

## 2. 用 Magpie 把订阅接成 provider
Magpie 是一个本地模型网关：把你登录的订阅（Gemini / Antigravity、ChatGPT、Claude、Copilot 等）或 API key 变成一个 OpenAI 兼容的地址，Pi 等 agent 直接用。

1. 安装 Magpie，确认 `magpie --help` 能跑。
2. 登录订阅：`magpie accounts add <agent>`（例如 antigravity），或用 API key：`magpie provider add <preset> <key>`。登录需要用户本人在浏览器里完成。
3. 看能用的模型：`magpie models pi`。
4. 起网关：`magpie serve`（默认只监听 `127.0.0.1:3425`）。
5. 接到 Pi：`magpie pi <provider/model>` 会改 Pi 的设置；或者派活时显式写 `--provider magpie --model <provider/model>`。
6. 验收：`pi -p 'reply ok' --provider magpie --model <provider/model> --no-session` 回复 ok。

### 网关放在另一台机器（可选）
想让多台电脑、或 Bot 的电脑共用一份订阅时，把 Magpie 跑在一台 VPS 上：
- 只监听内网地址（推荐 Tailscale 的 100.x 地址），防火墙只放行内网网卡上的 3425，**不要开公网端口**。
- 网关不是只听回环时会强制要 gateway key，把 key 配进 Pi 的 magpie provider。
- Bot 的电脑如果只能跑 userspace Tailscale，就在本机起一个转发，把 `127.0.0.1:3425` 转到 VPS 的内网地址，Pi 的配置不用改。
- 验收：在 VPS 外的公网测试连不上 3425，在 Bot 电脑上 `pi -p 'reply ok'` 正常。

## 3. 配「跑完自动叫醒」
Pi 在后台跑，Bot 当前轮已经结束，需要一个 webhook 把 Bot 单独叫醒去验收。

1. Bot 自己建一个 webhook 触发的例行任务，名字比如「Pi 完成唤醒」。任务内容写：读 payload 里的 `name` 和 `log`，按 grokbot-pi-dispatch 第 4 步验收对应产物，然后把结果回报用户。
2. 让用户在例行任务面板里，把 webhook 地址和 key 分别存成 Bot 的密钥 `<BOT>_PI_NOTIFY_URL`、`<BOT>_PI_NOTIFY_KEY`（Bot 用密钥输入卡请求，不要让用户把值贴进聊天）。
3. 测试：
```
curl -s -X POST "$<BOT>_PI_NOTIFY_URL" -H "Authorization: Bearer $<BOT>_PI_NOTIFY_KEY" -H 'Content-Type: application/json' -d '{"name":"ping","log":"/tmp/none"}'
```
   Bot 被单独叫醒一次就算通过。

## 4. 端到端验收
派一个最小任务（比如「在 /tmp/pi-test.txt 写一行 hello」），按 grokbot-pi-dispatch 的命令后台跑、结束当前轮。确认：Bot 被叫醒、文件存在、内容正确。

## 风险，要跟用户说清楚
- Pi 默认没有沙箱，能改电脑上的任何文件。任务里必须限定目录、禁止删除。
- 用订阅反代给 agent 用，可能违反该订阅的服务条款，有封号风险，建议用小号。
- 密钥只存在密钥里，不写进文件、不打印。
