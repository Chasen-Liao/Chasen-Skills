# 🔧 grokbot-pi-setup

让 Grok Bot 能把执行活派给电脑上的 **Pi**：装 Pi → 给 Pi 接一个模型（**DeepSeek / 中转站 / Magpie 等任意来源**）→ 装 [pi-task](https://github.com/robbin/grokbot-local-agent) → 配「Pi 跑完 webhook 叫醒 Bot」→ 端到端验收。

**适合谁**：Grok Bot 额度不够用，想让 Bot 只做「想」和「验收」，「干活」走自己订阅额度的人。

**安装**
```bash
npx skills add Chasen-Liao/Chasen-Skills --skill grokbot-pi-setup --global --yes
```

**触发**：对 Bot 说「帮我配好 Pi 派活」「按 grokbot-pi-setup 装一下」。

装好以后日常怎么用，看 [grokbot-pi-dispatch](../grokbot-pi-dispatch/README.md)。

⚠️ Pi 默认没有沙箱，任务里要限定目录、禁止删除。
