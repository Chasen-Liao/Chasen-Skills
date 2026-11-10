# agy 派活入口

一行调用本 skill 的 `scripts/agy-run.sh`。默认模型 `gemini-3.8-flash-high`（可用 `AGY_MODEL` 覆盖），权限用会话级 `--settings`，不改全局配置。登录 token 依赖系统 keyring；无头环境需能访问 dbus 会话（见 `AGY_XDG_RUNTIME_DIR` / `AGY_DBUS_SESSION_BUS_ADDRESS`）。部分 Google 账号不支持 `--mode auto`，脚本会自动忽略。默认开启 `--sandbox`，并发限制 1（后来的任务排队）。执行超时默认 20m（`--timeout`，不含排队）；排队上限默认 60m（`--queue-timeout`）。

数据与产物默认落在 `DISPATCH_HOME`（未设置时为 `~/.agy-dispatch`）下的 `out/`、`logs/`、`status/`、`runs/`、`tasks/`。

```bash
export DISPATCH_HOME="${DISPATCH_HOME:-$HOME/.agy-dispatch}"
R="./scripts/agy-run.sh"   # 或 skill 安装目录下的 scripts/agy-run.sh

# 只读扫描，结果写进 --out（默认 $DISPATCH_HOME/out）
"$R" --profile scan --out "$DISPATCH_HOME/out" \
  --task "$DISPATCH_HOME/tasks/某任务.md" --expect "$DISPATCH_HOME/out/report.md"

# 改某个项目
"$R" --profile code /path/to/某项目 \
  -p '跑测试并修失败用例' --expect /path/to/某项目/ok.txt

# 只写产物目录
"$R" --profile write "$DISPATCH_HOME/out" \
  -p '在本目录写 result.txt，内容为 ok'

# 后台跑，立刻拿到 run_id；状态会先是 queued，拿到锁后变成 running
"$R" --profile scan --bg --task ./task.md
# 读 $DISPATCH_HOME/status/<run_id>.json，直到 status 为 ok 或 fail

# 关闭沙箱（仅当默认沙箱跑不通时）
"$R" --profile scan --no-sandbox -p '...'
```

成功打印一行 `OK` 和产物路径（退出码 0）；失败打印 `FAIL: ...`（非 0）。即使 agy 自己报 `status: SUCCESS` 且 exit 0，只要 JSON 里 `denied_actions` 非空，或 `--expect` 的文件不存在/为空，也判失败。

任务书模板：`templates/TASK_TEMPLATE.md`（目标 / 可读写范围 / 成功标准 / 禁止事项）。`--task` 会把全文当作 prompt，并尝试从「成功标准」里提取绝对路径作为默认 `--expect`。

档位放行：

- `scan`：可读 `AGY_SCAN_READ_DIRS`（冒号分隔，默认 `$HOME`）；可写 `--out`；命令仅 `du` / `ls` / `stat` / `sha256sum`
- `code <项目>`：可读写该项目；放行常见构建测试（npm/pnpm/yarn、pytest、go/cargo test/build、make、node）和只读 git
- `write <目录>`：只能读写该产物目录

三档都拒绝 `git push`、`rm -rf`、`sudo`、`curl`/`wget`、`bash -c` / `sh -c`。永远不加 `--dangerously-skip-permissions`。每次运行只删除 `$DISPATCH_HOME/logs/` 下超过 14 天的文件，不自动清理 `runs/`、`status/`、`out/`。
