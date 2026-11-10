# Pi 派活入口（`scripts/pi-run.sh`）

一行调用本 skill 的 `scripts/pi-run.sh`。Pi 经本机 **Magpie** 网关走 **Antigravity** 账号额度（`magpie accounts add antigravity`），默认模型 `magpie/antigravity/gemini-3.8-flash`。按档位启用 **bwrap** 沙箱、`--tools` 白名单、断网后仅转发 **MAGPIE_ADDR**、包装拒绝 `curl`/`wget`/`sudo`/`git push`/`rm -r`、运行前 **quota** 闸门、**`--expect`** 验收。永远不加 `--dangerously-skip-permissions`。

数据与产物默认落在 `DISPATCH_HOME`（未设置时为 `~/.pi-dispatch`）下的 `tasks/`、`out/`、`logs/`、`status/`、`runs/`。

## 环境变量

| 变量 | 默认 | 说明 |
| :--- | :--- | :--- |
| `DISPATCH_HOME` | `~/.pi-dispatch` | 任务根：含 `tasks/` `out/` `logs/` `status/` `runs/` 与 `.pi.lock.*` |
| `PI_BIN` | `command -v pi` | Pi 可执行文件 |
| `MAGPIE_BIN` | `command -v magpie` | Magpie CLI（`quota` 等） |
| `MAGPIE_ADDR` | `127.0.0.1:3425` | 网关地址；沙箱内经 unix 转发连此地址 |
| `PI_AGENT_DIR` | `~/.pi/agent` | Pi 配置目录；每轮复制到 run 目录，避免写回真目录 |
| `DISPATCH_RO_ROOTS` | （空） | 冒号分隔的额外 **只读** 挂载根（替代以往写死的仓库根） |
| `PI_RUN_THINKING` | `medium` | 默认 `--thinking`；复杂/高质量任务运行时加 `--thinking high` |
| `PI_RUN_QUOTA_FAIL_PCT` | `90` | Gemini 5 小时窗口超过此百分比则 `FAIL: quota` |
| `PI_RUN_LIB_DIR` | 脚本旁 `lib/` | `pi-netfwd.py` 与 `pi-wrappers/` |

## 命令行

```bash
export DISPATCH_HOME="${DISPATCH_HOME:-$HOME/.pi-dispatch}"
mkdir -p "$DISPATCH_HOME"/{tasks,out,logs,status,runs}
R="/path/to/cli-dispatch/scripts/pi-run.sh"   # 或 skill 安装目录下

# 只读扫描，结果写 --out（默认 $DISPATCH_HOME/out）
"$R" --profile scan --out "$DISPATCH_HOME/out" \
  --task "$DISPATCH_HOME/tasks/某任务.md" --expect "$DISPATCH_HOME/out/report.md"

# 改某个项目并跑测试
"$R" --profile code /path/to/项目 -p '跑测试并修失败' --expect /path/to/项目/ok.txt

# 只写产物目录
"$R" --profile write "$DISPATCH_HOME/out" -p '在本目录写 result.txt，内容为 ok'

# 模型短名：flash（默认）、pro、claude；默认 --thinking medium，复杂/高质量任务加 --thinking high
"$R" --profile write "$DISPATCH_HOME/out" --model pro --thinking high -p '...'

# 后台：立刻打印 run_id
"$R" --profile scan --bg --task ./task.md
# 读 $DISPATCH_HOME/status/<run_id>.json
```

成功打印一行 `OK` 与产物路径（退出 0）；失败打印 `FAIL: ...`（非 0）。`--bg` 时前台退出 0 只表示已排队，真结果看 status JSON。

## 权限档位

| 档位 | 目录 | `--tools` | 说明 |
| :--- | :--- | :--- | :--- |
| `scan` | `--out` 可写 | `read,ls,grep,find,write` | 无 bash；`$HOME` 与 `DISPATCH_RO_ROOTS` 只读 |
| `code` | 项目目录 RW | 上表 + `edit,bash,powershell,codemode,tool_search` | 可跑测试构建 |
| `write` | 产物目录 RW | `read,ls,grep,find,write,edit` | 无 bash |

沙箱默认 **开**：`--unshare-net`，仅 Magpie 端口经 `pi-netfwd.py` 可达。缺 **bubblewrap** 时直接失败（不要用 `--no-sandbox` 凑合）。

## 状态 JSON 字段

`$DISPATCH_HOME/status/<run_id>.json`：

| 字段 | 含义 |
| :--- | :--- |
| `run_id` | 本次运行 id |
| `status` | `queued` → `running` → `ok` / `fail` |
| `reason` | `OK ...` 或 `FAIL: ...` |
| `artifacts` | 通过的 `--expect` 路径列表 |
| `duration_seconds` | 执行耗时（不含排队） |
| `usage` | 自 `pi --mode json` 汇总的 token / cost |
| `log` / `stdout` / `stderr` | 日志路径 |
| `model` / `profile` / `thinking` / `sandbox` | 运行参数 |
| `denied_actions` | 越权或包装拒绝项；非空则整次 fail |
| `queued_at` / `started_at` / `finished_at` | 时间戳 |
| `pi_exit` | Pi 进程退出码 |

## 并发与清理

- 锁：`$DISPATCH_HOME/.pi.lock.0` / `.pi.lock.1`，最多 **2** 个并发；`--queue-timeout` 默认 60m。
- 日志：`$DISPATCH_HOME/logs/` 内超过 **14** 天文件每次运行删除；不自动清 `runs/`、`status/`、`out/`。

任务书模板：`templates/TASK_TEMPLATE.md`。`--task` 全文作 prompt，并尝试从「成功标准」提取绝对路径为默认 `--expect`。
