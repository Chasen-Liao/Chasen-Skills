# 🔧 grokbot-pi-setup

> **Grok Bot 一次性派活初始化** — 装 Pi → 接任意模型（DeepSeek / 中转站 / Magpie）→ 装 `pi-task` → 配 webhook 自动唤醒 → 端到端验收。

<p>

![Phase](https://img.shields.io/badge/Phase-One--time_Setup-7c3aed?style=flat-square)
![Runtime](https://img.shields.io/badge/Runtime-Pi_+_pi--task-0ea5e9?style=flat-square)
![Node](https://img.shields.io/badge/Node-22+-10b981?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-64748b?style=flat-square)

</p>

> 💡 配置完成后的日常派活与验收，请使用 [grokbot-pi-dispatch](../grokbot-pi-dispatch/README.md)。

---

## ✨ 四步初始化流程

| 阶段 | 核心动作 | 验收指标 |
| :--- | :--- | :--- |
| **1. 装 Pi** | 在 Bot 主机安装 Pi | `pi --version` 正常，基础命令有响应 |
| **2. 接模型** | 接入 API key、中转站或 Magpie 网关 | `pi -p 'reply ok' --provider <p> --model <m>` 返回 `ok` |
| **3. 装 `pi-task` + 唤醒** | 部署 `robbin/grokbot-local-agent` 并建 webhook 例行任务 | 冒烟任务 `STATE done`，`<BOT>_PI_NOTIFY_URL/KEY` 就位 |
| **4. 端到端验收** | 后台派发最小写文件任务并结束当前轮 | Bot 被 webhook 单独叫醒，检查产物并 `ack` 后 `pending` 清空 |

---

## 🚀 安装与前置

```bash
npx skills add Chasen-Liao/Chasen-Skills --skill grokbot-pi-setup --global --yes
```

**前置条件**：Linux/macOS Shell、Node 22+、可联网拉取 Pi 与 [robbin/grokbot-local-agent](https://github.com/robbin/grokbot-local-agent)，且 Bot 支持密钥输入卡与 webhook 例行任务。

---

## 🗣️ 怎么用

对 Bot 说：

> `帮我配好 Pi 派活` / `按 grokbot-pi-setup 装一下`

Bot 会按 `1 → 4` 顺序逐步执行并验收（涉及登录、付款、删除或密钥录入时会停下请你操作）。

---

## 📋 验收结果示例

全部四步跑通后，Bot 返回环境就绪摘要：

```text
Pi 派活环境已就绪：
- Pi & 模型：`pi --version` 正常；`--provider <provider> --model <model>` 冒烟返回 ok。
- pi-task：`~/tools/pi-call/pi-task` 冒烟 STATE done；多 Bot 密钥 `<BOT>_PI_NOTIFY_URL/KEY` 已安全保存。
- 端到端测试：测试任务已触发 webhook 唤醒，/tmp/pi-test.txt 内容核对无误，ack 后 pending 已清空。
```

---

## 📂 目录

```text
grokbot-pi-setup/
├── SKILL.md    # Agent 初始化契约（四步安装与验收流程）
└── README.md   # 本文件
```

---

## 📄 License

MIT © Chasen-Liao
