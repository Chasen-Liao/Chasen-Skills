# 🚚 grokbot-pi-dispatch

Grok Bot 的通用派活方法：**Bot 写任务书 → `pi -p` 后台派给 Pi → Pi 跑完 webhook 叫醒 Bot → Bot 验收产物**。

**任务书只写五件事**：做什么、产物路径、完成标准、边界（限定目录、禁止删除）、自查一次就结束。

**适合谁**：已经按 [grokbot-pi-setup](../grokbot-pi-setup/README.md) 配好 Pi 和唤醒的 Grok Bot。

**安装**
```bash
npx skills add Chasen-Liao/Chasen-Skills --skill grokbot-pi-dispatch --global --yes
```

**触发**：Bot 遇到超过两三步的执行活时自动读；也可以说「派给 Pi」「用 pi -p 跑」。

删除、发送、付款、发帖永远不交给 Pi。
