---
name: grokbot-pi-dispatch
description: Grok Bot 要做超过两三步的执行活（写代码、改文件、扫目录、整理或生成内容）时，开干前读这个：Bot 只写任务书、用 pi -p 后台派给电脑上的 Pi、等自动唤醒后验收。还没装好 Pi 和唤醒先看 grokbot-pi-setup。
---

# grokbot-pi-dispatch：Bot 写任务，Pi 干活，Bot 验收

Bot 只做三件事：写任务、派给 Pi、验收。一两步的小事 Bot 自己做，别派。

## 1. 写任务书（越短越好）
只写五件事：
1. 要做什么（一两句）。
2. 产物写到哪个绝对路径。
3. 怎么算做完（可检查的标准）。
4. 边界：「只改 <目录>，不要删除任何文件，不要 git push」。
5. 收尾：「写完产物自查一次就结束，不要反复自查或重试」。

## 2. 后台派活
用 Bot 自己的 Shell 工具**后台**运行（不阻塞等待），不要用 `nohup` 或 `&`：

```
pi -p '<任务书>' --provider magpie --model <provider/model> --thinking medium --no-session --mode json > <日志目录>/<短名>.jsonl 2>&1 ; curl -s -X POST "$<BOT>_PI_NOTIFY_URL" -H "Authorization: Bearer $<BOT>_PI_NOTIFY_KEY" -H 'Content-Type: application/json' -d '{"name":"<短名>","log":"<日志目录>/<短名>.jsonl"}'
```

- 小活用 `--thinking medium`；难活才换更强的模型或加 `--thinking high`（小活开 high 会乱翻文件、烧 token）。
- 只读的活加 `--tools read,ls,grep,find`。
- 用到 MCP 的活，用 `--exclude-tools` 关掉删除、移动类工具。
- 派完告诉用户「已派出」，然后**立刻结束当前轮**。如果 Pi 跑完时 Bot 还在一个没结束的轮里，完成通知会并进当轮，不会再单独叫醒。

## 3. 等结果
- 正常情况：Pi 退出后 curl 触发 webhook，Bot 被单独叫醒，不用轮询。
- 兜底：每轮开头（包括用户问进度时），先查自己派出去、还没验收的日志：`rg -q '"type":"agent_end"' <日志>` 能匹配到就是跑完了，马上验收。
- 看进度：`rg -o '"toolName":"\w+"' <日志> | tail -5`。

## 4. 验收
被叫醒后立刻检查：产物在不在，内容是否达到第 1 步写的完成标准。然后回报用户结果，不是回报「Pi 说做完了」。
不合格就补充说明再派，最多两次；还不行换备用 agent 或 Bot 自己接手。

## 规矩
- 删除、发送消息或邮件、付款、发帖，永远不交给 Pi，由 Bot 在用户确认后自己做。
- Pi 没有沙箱，所以任务书里必须限定目录、禁止删除。
- 不打印密钥。
- 多个 Bot 之间靠共享文件交接，少互相叫醒。
