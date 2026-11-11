# 🔧 grokbot-pi-setup

让 Grok Bot 能把执行活派给电脑上的 **Pi**：装 Pi → 用 **Magpie** 把你自己的模型订阅接成 Pi 的 provider →（可选）网关放 VPS、只走 Tailscale 内网 → 配「Pi 跑完 webhook 叫醒 Bot」→ 端到端验收。

**适合谁**：Grok Bot 额度不够用，想让 Bot 只做「想」和「验收」，「干活」走自己订阅额度的人。

**安装**
```bash
npx skills add Chasen-Liao/Chasen-Skills --skill grokbot-pi-setup --global --yes
```

**触发**：对 Bot 说「帮我配好 Pi 派活」「按 grokbot-pi-setup 装一下」。

装好以后日常怎么用，看 [grokbot-pi-dispatch](../grokbot-pi-dispatch/README.md)。

⚠️ Pi 默认没有沙箱；订阅反代可能违反服务条款，建议用小号。
