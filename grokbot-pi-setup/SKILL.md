---
name: grokbot-pi-setup
description: >-
  第一次让 Grok Bot 把执行活派给本机 Pi 之前的一次性初始化：装 Pi、接任意模型（API key / 中转站 / Magpie）、装 pi-task、
  配「Pi 跑完自动叫醒 Bot」的 webhook 并完成端到端验收。装好后日常派活看 grokbot-pi-dispatch。
  触发：帮我配好 Pi 派活 / 按 grokbot-pi-setup 装一下。
license: MIT
compatibility: 需 Linux/macOS Shell、Node 22+、可联网安装 Pi 与 robbin/grokbot-local-agent（pi-task）；Bot 需支持密钥输入与 webhook 例行任务
metadata:
  author: Chasen-Liao
  version: "0.2.0"
  category: workflow
---

# grokbot-pi-setup：让 Grok Bot 能派活给 Pi

目标：Grok Bot 额度贵，仅用于「拆任务 + 验收」；具体执行交给本机 Pi（可用 DeepSeek、中转站、Magpie 等任意额度）。
按下面 `1 → 4` 顺序推进，每步验收通过后再继续；涉及删除、付款、登录操作先问用户。

## 1. 装 Pi

- 在 Bot 所在主机按 Pi 官方文档完成安装，确认 `pi --version` 可运行。
- 用任意现成 provider 跑通一次 `pi -p 'reply ok' --no-session`，确认 Pi 本体正常。

## 2. 给 Pi 接一个模型（来源随意）

二选一，按用户手头资源配置：
- **直接用 API key**：DeepSeek、OpenRouter 或各家中转站，按 Pi 文档写入默认配置 `~/.pi/agent/models.json` 或使用 `pi` 自带登录。
- **用网关统一管理（可选）**：如 Magpie，把订阅或各家 key 接入后再配给 Pi；若网关放在另一台 VPS 上共用，只监听内网地址（如 Tailscale），**不要开公网端口**，并开启网关 key。

确定唯一 `provider` 名和 `model` 名后验收（以下两个值将用于后续派活）：

```bash
pi -p 'reply ok' --provider <provider> --model <model> --no-session
```

## 3. 装 pi-task 并配「跑完自动叫醒」

使用 [robbin/grokbot-local-agent](https://github.com/robbin/grokbot-local-agent) 脚本（需 Node 22+，下文 `~/tools/pi-call` 为默认安装路径示例）：

```bash
git clone https://github.com/robbin/grokbot-local-agent /tmp/gla
mkdir -p ~/tools/pi-call && cp -a /tmp/gla/bin/. ~/tools/pi-call/ && chmod +x ~/tools/pi-call/*
```

`pi-task` 默认使用 `deepseek/deepseek-flash`、`thinking high`，换模型在派活时传 `--model <provider/model>`。
冒烟验证：跑通 `PI_NOTIFY_OFF=1 ~/tools/pi-call/pi-task run /tmp 'Reply with only OK' --session smoke --owner <ID>`，确认输出 `STATE done` 后执行 `pi-task ack <TASK> --owner <ID>`。

配置自动唤醒：
1. Bot 创建 webhook 触发的例行任务（如「Pi 完成唤醒」），逻辑参考仓库 `routines/pi-task-notify.md`：唤醒后运行 `pi-task pending --owner <ID>`，按 `grokbot-pi-dispatch` 的验收与 `ack` 流程处理并回报，不碰其他 Bot 的任务。
2. 让用户通过密钥输入卡保存 webhook 地址与 key，命名为 `<BOT>_PI_NOTIFY_URL`、`<BOT>_PI_NOTIFY_KEY`（共用主机的多个 Bot 各用各的前缀，派活时再映射为 `pi-task` 读取的 `PI_NOTIFY_URL`、`PI_NOTIFY_SECRET`）。

## 4. 端到端验收

按 `grokbot-pi-dispatch` 的派活命令后台派发一个最小测试任务（如在 `/tmp/pi-test.txt` 写入 `hello`）并立刻结束当前轮。确认：Bot 被 webhook 单独唤醒、`pi-task pending --owner <ID>` 能查到任务、文件内容正确，且 `ack` 后 `pending` 清空。

## 风险提示

- Pi 默认无沙箱，可读写本机文件，日常任务书须限定目录并禁止删除。
- 将订阅反代给 Agent 可能违反对应服务条款并存在封号风险，建议用小号。
- 密钥只存入专用密钥管理，禁止写入普通文件或打印到聊天。
