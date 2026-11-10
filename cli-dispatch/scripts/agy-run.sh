#!/usr/bin/env bash
# Bot 一行入口：固定 Gemini 3.8 Flash High，按档位注入会话级 --settings，
# 解析 headless JSON，按 denied_actions / status / --expect 判成败。
# 永远不加 --dangerously-skip-permissions。不改全局 settings.json。
set -euo pipefail

DISPATCH_HOME="${DISPATCH_HOME:-$HOME/.agy-dispatch}"
MODEL="${AGY_MODEL:-gemini-3.8-flash-high}"
LOG_DIR="${AGY_LOG_DIR:-$DISPATCH_HOME/logs}"
STATUS_DIR="${AGY_STATUS_DIR:-$DISPATCH_HOME/status}"
RUNS_DIR="${AGY_RUNS_DIR:-$DISPATCH_HOME/runs}"
LOCK_FILE="${AGY_LOCK_FILE:-$DISPATCH_HOME/.agy.lock}"
DEFAULT_OUT="${AGY_DEFAULT_OUT:-$DISPATCH_HOME/out}"
SCAN_READ_DIRS="${AGY_SCAN_READ_DIRS:-$HOME}"

if [[ -z "${AGY_BIN:-}" ]]; then
  AGY_BIN="$(command -v agy 2>/dev/null || true)"
fi
DEFAULT_TIMEOUT="20m"
DEFAULT_QUEUE_TIMEOUT="60m"

usage() {
  cat <<'EOF'
用法:
  agy-run.sh --profile scan [--out DIR] [--task FILE | -p '...'] [--expect PATH]... [--bg]
  agy-run.sh --profile code <项目目录> [--task FILE | -p '...'] [--expect PATH]... [--bg]
  agy-run.sh --profile write <输出目录> [--task FILE | -p '...'] [--expect PATH]... [--bg]

常用选项:
  --profile scan|code|write  权限档位（code/write 后须跟目录）
  --out DIR                  scan 的产物目录，默认 $DISPATCH_HOME/out
  --task FILE                用任务书全文作为 prompt；成功标准里的绝对路径会作为默认 --expect
  --expect PATH              结束后必须存在且非空的产物（可重复）
  --timeout DUR              agy 执行超时（默认 20m；不含排队时间），如 20m / 60s / 1h
  --queue-timeout DUR        等锁上限（默认 60m），超时判 fail
  --sandbox                  默认已开启终端沙箱
  --no-sandbox               关闭沙箱
  --bg                       后台跑，立刻打印 run_id；结果写入 $DISPATCH_HOME/status/<run_id>.json
  -h, --help                 显示本说明

环境: DISPATCH_HOME（默认 ~/.agy-dispatch）、AGY_BIN（默认 PATH 中的 agy）、
AGY_SCAN_READ_DIRS（scan 可读目录，冒号分隔，默认 $HOME）、AGY_MODEL（默认 gemini-3.8-flash-high）。
固定行为: unset 付费 API 变量；日志在 $DISPATCH_HOME/logs/（删除其中超过 14 天的文件）；
会话级 --settings（不写全局配置），并发限制 1（排队）。
EOF
}

to_seconds() {
  local v="$1"
  if [[ "$v" =~ ^([0-9]+)([smhSMH])$ ]]; then
    local n="${BASH_REMATCH[1]}"
    local u="${BASH_REMATCH[2]}"
    u="$(printf '%s' "$u" | tr 'SMH' 'smh')"
    case "$u" in
      s) printf '%s\n' "$n" ;;
      m) printf '%s\n' $((n * 60)) ;;
      h) printf '%s\n' $((n * 3600)) ;;
    esac
  elif [[ "$v" =~ ^[0-9]+$ ]]; then
    printf '%s\n' "$v"
  else
    return 2
  fi
}

iso_now() {
  date +%Y-%m-%dT%H:%M:%S%z | sed -E 's/([0-9]{2})([0-9]{2})$/\1:\2/'
}

if [[ -z "$AGY_BIN" || ! -x "$AGY_BIN" ]]; then
  echo "agy-run: agy 不存在或不可执行（设置 AGY_BIN 或确保 agy 在 PATH 中）: ${AGY_BIN:-<未找到>}" >&2
  exit 127
fi

# 无头环境若 agy 凭系统 keyring 登录，可设置 AGY_XDG_RUNTIME_DIR / AGY_DBUS_SESSION_BUS_ADDRESS。
if [[ -n "${AGY_XDG_RUNTIME_DIR:-}" ]]; then
  export XDG_RUNTIME_DIR="$AGY_XDG_RUNTIME_DIR"
fi
if [[ -n "${AGY_DBUS_SESSION_BUS_ADDRESS:-}" ]]; then
  export DBUS_SESSION_BUS_ADDRESS="$AGY_DBUS_SESSION_BUS_ADDRESS"
elif [[ -n "${XDG_RUNTIME_DIR:-}" && -z "${DBUS_SESSION_BUS_ADDRESS:-}" && -S "${XDG_RUNTIME_DIR}/bus" ]]; then
  export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"
fi

unset GEMINI_API_KEY
unset GOOGLE_API_KEY
unset GOOGLE_GEMINI_BASE_URL
unset AGY_ADC_AUTH
unset GOOGLE_APPLICATION_CREDENTIALS
unset GOOGLE_GENAI_USE_VERTEXAI
unset GOOGLE_GENAI_USE_ENTERPRISE

PROFILE=""
PROFILE_DIR=""
OUT_DIR=""
TASK_FILE=""
BG=0
USE_SANDBOX=1
PRINT_TIMEOUT="$DEFAULT_TIMEOUT"
QUEUE_TIMEOUT="$DEFAULT_QUEUE_TIMEOUT"
TIMEOUT_SET=0
EXPECTS=()
AGY_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --profile)
      if [[ $# -lt 2 ]]; then
        echo "agy-run: --profile 需要 scan、code <目录> 或 write <目录>" >&2
        exit 2
      fi
      PROFILE="$2"
      shift 2
      case "$PROFILE" in
        scan) ;;
        code|write)
          if [[ $# -lt 1 || "$1" == -* ]]; then
            echo "agy-run: --profile $PROFILE 后面必须跟一个目录" >&2
            exit 2
          fi
          PROFILE_DIR="$1"
          shift
          ;;
        *)
          echo "agy-run: 未知档位 '$PROFILE'（应为 scan、code 或 write）" >&2
          exit 2
          ;;
      esac
      ;;
    --out)
      if [[ $# -lt 2 ]]; then
        echo "agy-run: --out 需要目录" >&2
        exit 2
      fi
      OUT_DIR="$2"
      shift 2
      ;;
    --task)
      if [[ $# -lt 2 ]]; then
        echo "agy-run: --task 需要文件" >&2
        exit 2
      fi
      TASK_FILE="$2"
      shift 2
      ;;
    --expect)
      if [[ $# -lt 2 ]]; then
        echo "agy-run: --expect 需要路径" >&2
        exit 2
      fi
      EXPECTS+=("$2")
      shift 2
      ;;
    --timeout)
      if [[ $# -lt 2 ]]; then
        echo "agy-run: --timeout 需要时长，如 20m" >&2
        exit 2
      fi
      PRINT_TIMEOUT="$2"
      TIMEOUT_SET=1
      if ! to_seconds "$PRINT_TIMEOUT" >/dev/null; then
        echo "agy-run: 无法解析 --timeout '$PRINT_TIMEOUT'（支持 20m / 60s / 1h / 秒数）" >&2
        exit 2
      fi
      shift 2
      ;;
    --queue-timeout)
      if [[ $# -lt 2 ]]; then
        echo "agy-run: --queue-timeout 需要时长，如 60m" >&2
        exit 2
      fi
      QUEUE_TIMEOUT="$2"
      if ! to_seconds "$QUEUE_TIMEOUT" >/dev/null; then
        echo "agy-run: 无法解析 --queue-timeout '$QUEUE_TIMEOUT'（支持 20m / 60s / 1h / 秒数）" >&2
        exit 2
      fi
      shift 2
      ;;
    --sandbox)
      USE_SANDBOX=1
      shift
      ;;
    --no-sandbox)
      USE_SANDBOX=0
      shift
      ;;
    --bg)
      BG=1
      shift
      ;;
    --dangerously-skip-permissions)
      echo "agy-run: 已忽略 --dangerously-skip-permissions（禁止使用）" >&2
      shift
      ;;
    *)
      AGY_ARGS+=("$1")
      shift
      ;;
  esac
done

if [[ -z "$PROFILE" ]]; then
  echo "agy-run: 必须指定 --profile scan|code|write" >&2
  usage >&2
  exit 2
fi

abs_dir() {
  local raw="$1"
  mkdir -p "$raw"
  python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$raw"
}

case "$PROFILE" in
  scan)
    OUT_DIR="$(abs_dir "${OUT_DIR:-$DEFAULT_OUT}")"
    WORK_DIR="$OUT_DIR"
    ;;
  code)
    if [[ ! -d "$PROFILE_DIR" ]]; then
      echo "agy-run: 项目目录不存在: $PROFILE_DIR" >&2
      exit 2
    fi
    WORK_DIR="$(abs_dir "$PROFILE_DIR")"
    OUT_DIR="${OUT_DIR:-$WORK_DIR}"
    ;;
  write)
    OUT_DIR="$(abs_dir "$PROFILE_DIR")"
    WORK_DIR="$OUT_DIR"
    ;;
esac

if [[ -n "$TASK_FILE" && ! -f "$TASK_FILE" ]]; then
  echo "agy-run: 任务书不存在: $TASK_FILE" >&2
  exit 2
fi

mkdir -p "$LOG_DIR" "$STATUS_DIR" "$RUNS_DIR"
# 只清理 logs/ 里超过 14 天的文件，不动 runs/、status/、out/。
find "$LOG_DIR" -mindepth 1 -maxdepth 1 -type f -mtime +14 -delete 2>/dev/null || true

ts="$(date +%Y%m%d_%H%M%S)"
run_id="${AGY_RUN_ID:-${ts}-$$}"
run_dir="$RUNS_DIR/$run_id"
mkdir -p "$run_dir"

settings_file="$run_dir/settings.json"
stdout_file="$LOG_DIR/${run_id}.stdout.json"
stderr_file="$LOG_DIR/${run_id}.stderr.log"
agy_log_file="$LOG_DIR/${run_id}.agy.log"
status_file="$STATUS_DIR/${run_id}.json"
prompt_file="$run_dir/prompt.md"
expect_file="$run_dir/expects.txt"

# 会话级 settings：文件路径形式的 --settings。不写全局配置。
# command() 按前缀匹配；deny 优先于 allow。
python3 - "$PROFILE" "$WORK_DIR" "$OUT_DIR" "$settings_file" "$USE_SANDBOX" "$SCAN_READ_DIRS" <<'PY'
import json, os, sys
profile, work_dir, out_dir, path, use_sandbox, scan_dirs_raw = sys.argv[1:]
scan_dirs = [d.strip() for d in scan_dirs_raw.split(":") if d.strip()]
if not scan_dirs:
    scan_dirs = [os.path.expanduser("~")]
common_deny = [
    "command(git push)",
    "command(rm -rf)",
    "command(rm -r)",
    "command(sudo)",
    "command(curl)",
    "command(wget)",
    "command(regex:curl .*)",
    "command(bash -c)",
    "command(sh -c)",
]
if profile == "scan":
    allow = [f"read_file({d})" for d in scan_dirs]
    allow += [
        f"write_file({out_dir})",
        "command(du)",
        "command(ls)",
        "command(stat)",
        "command(sha256sum)",
    ]
    trusted = [out_dir]
    non_ws = True
elif profile == "code":
    allow = [
        f"read_file({work_dir})",
        f"write_file({work_dir})",
        "command(npm test)",
        "command(npm run)",
        "command(node)",
        "command(pnpm test)",
        "command(pnpm run)",
        "command(yarn test)",
        "command(yarn run)",
        "command(yarn build)",
        "command(python -m pytest)",
        "command(python3 -m pytest)",
        "command(pytest)",
        "command(go test)",
        "command(go build)",
        "command(cargo test)",
        "command(cargo build)",
        "command(make)",
        "command(git status)",
        "command(git diff)",
        "command(git log)",
        "command(git show)",
        "command(git rev-parse)",
        "command(git ls-files)",
        "command(git blame)",
        "command(git remote -v)",
    ]
    trusted = [work_dir]
    non_ws = False
else:
    allow = [
        f"read_file({out_dir})",
        f"write_file({out_dir})",
    ]
    trusted = [out_dir]
    non_ws = False

settings = {
    "agentMode": "accept-edits",
    "allowNonWorkspaceAccess": non_ws,
    "trustedWorkspaces": trusted,
    "enableTerminalSandbox": use_sandbox == "1",
    "permissions": {"allow": allow, "deny": common_deny},
}
if use_sandbox == "1":
    settings["toolPermission"] = "proceed-in-sandbox"
with open(path, "w", encoding="utf-8") as f:
    json.dump(settings, f, ensure_ascii=False, indent=2)
    f.write("\n")
PY
chmod 600 "$settings_file"

# 处理 --task：写入 prompt，并从「成功标准」段提取默认 expect。
if [[ -n "$TASK_FILE" ]]; then
  cp -a "$TASK_FILE" "$prompt_file"
  mapfile -t TASK_EXPECTS < <(python3 - "$TASK_FILE" <<'PY'
import re, sys
from pathlib import Path
text = Path(sys.argv[1]).read_text(encoding="utf-8")
parts = re.split(r"(?m)^##\s+", text)
section = ""
for part in parts:
    if part.startswith("成功标准") or part.startswith("成功標準"):
        section = part
        break
if not section:
    section = text
paths = []
for m in re.finditer(r"(?m)产物路径\s*[:：]\s*`?(\S+?)`?\s*$", section):
    paths.append(m.group(1).strip("。.;，,"))
if not paths:
    for m in re.finditer(r"(?<![A-Za-z0-9_])(/[^\s`）)\]\"']+)", section):
        p = m.group(1).rstrip("。.;，,")
        if p not in paths:
            paths.append(p)
for p in paths:
    print(p)
PY
)
  if [[ ${#EXPECTS[@]} -eq 0 && ${#TASK_EXPECTS[@]} -gt 0 ]]; then
    EXPECTS+=("${TASK_EXPECTS[@]}")
  fi
fi

printf '%s\n' "${EXPECTS[@]+"${EXPECTS[@]}"}" > "$expect_file"

# 组装传给 agy 的参数：去掉危险开关，补上固定项。
filtered=()
has_model=0
has_log=0
has_settings=0
has_format=0
has_timeout=0
has_prompt=0
has_add_dir=0
has_sandbox=0
i=0
while [[ $i -lt ${#AGY_ARGS[@]} ]]; do
  a="${AGY_ARGS[$i]}"
  case "$a" in
    --dangerously-skip-permissions)
      echo "agy-run: 已忽略 --dangerously-skip-permissions（禁止使用）" >&2
      i=$((i + 1))
      continue
      ;;
    --no-sandbox)
      USE_SANDBOX=0
      i=$((i + 1))
      continue
      ;;
    --sandbox)
      has_sandbox=1
      if [[ "$USE_SANDBOX" -eq 0 ]]; then
        i=$((i + 1))
        continue
      fi
      ;;
    --mode)
      if [[ $((i + 1)) -lt ${#AGY_ARGS[@]} && "${AGY_ARGS[$((i + 1))]}" == "auto" ]]; then
        echo "agy-run: 已忽略 --mode auto（部分账号不支持，将使用默认模式）" >&2
        i=$((i + 2))
        continue
      fi
      ;;
    --model|--model=*) has_model=1 ;;
    --log-file|--log-file=*) has_log=1 ;;
    --settings|--settings=*) has_settings=1 ;;
    --output-format|--output-format=*) has_format=1 ;;
    --print-timeout|--print-timeout=*)
      has_timeout=1
      if [[ "$TIMEOUT_SET" -eq 1 ]]; then
        echo "agy-run: --timeout $PRINT_TIMEOUT 优先于传入的 --print-timeout" >&2
        if [[ "$a" == --print-timeout ]]; then
          i=$((i + 2))
        else
          i=$((i + 1))
        fi
        continue
      fi
      ;;
    -p|--print|--prompt|--prompt=*) has_prompt=1 ;;
    --add-dir|--add-dir=*) has_add_dir=1 ;;
  esac
  filtered+=("$a")
  i=$((i + 1))
done

if [[ -n "$TASK_FILE" && "$has_prompt" -eq 0 ]]; then
  filtered+=(-p "$(cat "$prompt_file")")
  has_prompt=1
fi

if [[ "$has_prompt" -eq 0 ]]; then
  echo "agy-run: 需要 -p/--prompt 或 --task（只支持 headless 一行调用）" >&2
  exit 2
fi

final=()
if [[ "$has_model" -eq 0 ]]; then
  final+=(--model "$MODEL")
fi
if [[ "$has_log" -eq 0 ]]; then
  final+=(--log-file "$agy_log_file")
fi
if [[ "$has_settings" -eq 0 ]]; then
  final+=(--settings "$settings_file")
else
  echo "agy-run: 警告：调用方自带 --settings，档位权限可能被覆盖" >&2
fi
if [[ "$has_format" -eq 0 ]]; then
  final+=(--output-format json)
fi
if [[ "$has_timeout" -eq 0 || "$TIMEOUT_SET" -eq 1 ]]; then
  final+=(--print-timeout "$PRINT_TIMEOUT")
fi
if [[ "$has_add_dir" -eq 0 ]]; then
  final+=(--add-dir "$WORK_DIR")
fi
if [[ "$USE_SANDBOX" -eq 1 && "$has_sandbox" -eq 0 ]]; then
  final+=(--sandbox)
fi
final+=("${filtered[@]}")

patch_status() {
  python3 - "$status_file" "$@" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
# remaining argv: key value key value...
args = sys.argv[2:]
data = {}
if path.exists() and path.stat().st_size:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = {}
i = 0
while i < len(args):
    key = args[i]
    val = args[i + 1] if i + 1 < len(args) else ""
    if val == "__NULL__":
        data[key] = None
    else:
        data[key] = val
    i += 2
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
}

write_queued_status() {
  python3 - "$status_file" "$run_id" "$agy_log_file" "$stdout_file" "$stderr_file" "$(iso_now)" <<'PY'
import json, sys
status_file, run_id, log, stdout, stderr, queued_at = sys.argv[1:]
with open(status_file, "w", encoding="utf-8") as f:
    json.dump({
        "run_id": run_id,
        "status": "queued",
        "reason": "",
        "artifacts": [],
        "duration_seconds": None,
        "usage": None,
        "log": log,
        "stdout": stdout,
        "stderr": stderr,
        "queued_at": queued_at,
        "started_at": None,
        "finished_at": None,
    }, f, ensure_ascii=False, indent=2)
    f.write("\n")
PY
}

write_queue_timeout() {
  local finished
  finished="$(iso_now)"
  python3 - "$status_file" "$QUEUE_TIMEOUT" "$finished" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
timeout, finished_at = sys.argv[2], sys.argv[3]
data = json.loads(path.read_text(encoding="utf-8"))
reason = f"FAIL: queue timeout after {timeout}"
data.update({
    "status": "fail",
    "reason": reason,
    "finished_at": finished_at,
})
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(reason)
PY
}

run_and_judge() {
  local start end elapsed agy_rc
  start="$(date +%s.%N)"
  patch_status status running started_at "$(iso_now)"
  set +e
  (
    cd "$WORK_DIR"
    exec "$AGY_BIN" "${final[@]}" </dev/null
  ) >"$stdout_file" 2>"$stderr_file"
  agy_rc=$?
  set -e
  end="$(date +%s.%N)"
  elapsed="$(python3 -c 'import sys; print(round(float(sys.argv[2])-float(sys.argv[1]), 3))' "$start" "$end")"
  local finished
  finished="$(iso_now)"

  python3 - "$status_file" "$run_id" "$stdout_file" "$stderr_file" "$agy_log_file" "$expect_file" "$elapsed" "$agy_rc" "$finished" <<'PY'
import json, os, sys
from pathlib import Path

status_file, run_id, stdout_file, stderr_file, log_file, expect_file, elapsed, agy_rc, finished_at = sys.argv[1:]
agy_rc = int(agy_rc)
elapsed = float(elapsed)
expects = [ln.strip() for ln in Path(expect_file).read_text(encoding="utf-8").splitlines() if ln.strip()]

existing = {}
sp = Path(status_file)
if sp.exists() and sp.stat().st_size:
    try:
        existing = json.loads(sp.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        existing = {}

raw = Path(stdout_file).read_text(encoding="utf-8", errors="replace").strip()
data = None
parse_error = None
if raw:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        start = raw.rfind("{")
        end = raw.rfind("}")
        if start != -1 and end > start:
            try:
                data = json.loads(raw[start:end + 1])
            except json.JSONDecodeError as e:
                parse_error = str(e)
        else:
            parse_error = "stdout is not JSON"

reasons = []
usage = None
agy_status = None
denied = []
duration = elapsed

if parse_error:
    reasons.append(f"FAIL: invalid json ({parse_error})")
elif data is None:
    reasons.append("FAIL: empty json output")
else:
    agy_status = data.get("status")
    usage = data.get("usage")
    if data.get("duration_seconds") is not None:
        try:
            duration = float(data["duration_seconds"])
        except (TypeError, ValueError):
            duration = elapsed
    denied = data.get("denied_actions") or []
    if agy_status and agy_status != "SUCCESS":
        reasons.append(f"FAIL: status {agy_status}")
    if denied:
        bits = []
        for item in denied:
            if isinstance(item, dict):
                action = str(item.get("action") or "")
                name = str(item.get("display_name") or "")
                bits.append(f"{action}({name})" if name else action or "?")
            else:
                bits.append(str(item))
        reasons.append("FAIL: denied " + ", ".join(bits))
    # 命中 permissions.deny 时，agy 往往不填 denied_actions，只把拒绝写进 response。
    blob = str(data.get("response") or "")
    try:
        blob += "\n" + Path(stderr_file).read_text(encoding="utf-8", errors="replace")
    except OSError:
        pass
    import re
    if re.search(r"Matches user-configured deny rule|permission check failed for command|Permission denied for command", blob, re.I):
        cmds = re.findall(r"Permission denied for command\(([^)]+)\)", blob)
        if not cmds:
            raw = re.findall(r'permission check failed for command "([^"]+)"', blob)
            cmds = [c if c.startswith("command(") else f"command({c})" for c in raw]
        if cmds:
            # 去重，且避免与 denied_actions 重复报同一条
            extra = [c for c in dict.fromkeys(cmds) if f"FAIL: denied {c}" not in " ".join(reasons) and not any(c in r for r in reasons)]
            if extra:
                reasons.append("FAIL: denied " + ", ".join(extra))
        elif not any(r.startswith("FAIL: denied") for r in reasons):
            reasons.append("FAIL: denied (user-configured deny rule)")

if agy_rc != 0:
    reasons.append(f"FAIL: agy exit {agy_rc}")

present = []
for p in expects:
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        reasons.append(f"FAIL: missing artifact {p}")
    else:
        present.append(p)

if reasons:
    verdict = " / ".join(reasons)
    ok = False
else:
    verdict = "OK" + ((" " + " ".join(present)) if present else "")
    ok = True

payload = {
    "run_id": existing.get("run_id", run_id),
    "status": "ok" if ok else "fail",
    "reason": verdict,
    "artifacts": present,
    "duration_seconds": duration,
    "usage": usage,
    "log": log_file,
    "stdout": stdout_file,
    "stderr": stderr_file,
    "agy_status": agy_status,
    "agy_exit": agy_rc,
    "denied_actions": denied,
    "queued_at": existing.get("queued_at"),
    "started_at": existing.get("started_at"),
    "finished_at": finished_at,
}
with open(status_file, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(verdict)
sys.exit(0 if ok else 1)
PY
}

acquire_and_run() {
  local wait_secs rc
  wait_secs="$(to_seconds "$QUEUE_TIMEOUT")"
  # fd 9 持锁直到本函数/子 shell 结束；排队时间不含在 --timeout 里。
  exec 9>"$LOCK_FILE"
  if ! flock -w "$wait_secs" 9; then
    write_queue_timeout
    return 1
  fi
  run_and_judge
}

write_queued_status

if [[ "$BG" -eq 1 ]]; then
  echo "$run_id"
  (
    acquire_and_run
  ) >"$run_dir/wrapper.log" 2>&1 &
  disown $! || true
  exit 0
fi

acquire_and_run
