#!/usr/bin/env bash
# Bot 一行入口：Pi 经本机 Magpie 调用 Antigravity（默认 Gemini 3.8 Flash）。
# 按档位用 bwrap 沙箱 + --tools 白名单，解析 --mode json 的 usage，按 denied / --expect 判成败。
# 永远不加 --dangerously-skip-permissions。不改 Pi 全局默认模型。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="${PI_RUN_LIB_DIR:-$SCRIPT_DIR/lib}"

DISPATCH_HOME="${DISPATCH_HOME:-$HOME/.pi-dispatch}"
LOG_DIR="${PI_RUN_LOG_DIR:-$DISPATCH_HOME/logs}"
STATUS_DIR="${PI_RUN_STATUS_DIR:-$DISPATCH_HOME/status}"
RUNS_DIR="${PI_RUN_RUNS_DIR:-$DISPATCH_HOME/runs}"
LOCK_DIR="${PI_RUN_LOCK_DIR:-$DISPATCH_HOME}"
DEFAULT_OUT="${PI_RUN_DEFAULT_OUT:-$DISPATCH_HOME/out}"

if [[ -z "${PI_BIN:-}" ]]; then
  PI_BIN="$(command -v pi 2>/dev/null || true)"
fi
if [[ -z "${MAGPIE_BIN:-}" ]]; then
  MAGPIE_BIN="$(command -v magpie 2>/dev/null || true)"
fi

MAGPIE_ADDR="${MAGPIE_ADDR:-127.0.0.1:3425}"
PI_AGENT_DIR="${PI_AGENT_DIR:-$HOME/.pi/agent}"
REAL_HOME="$HOME"
REAL_USER="${USER:-$(id -un)}"
CALLER_PATH="${PATH}"
DISPATCH_RO_ROOTS="${DISPATCH_RO_ROOTS:-}"

DEFAULT_TIMEOUT="20m"
DEFAULT_QUEUE_TIMEOUT="60m"
DEFAULT_PROVIDER="${PI_RUN_PROVIDER:-magpie}"
DEFAULT_THINKING="${PI_RUN_THINKING:-medium}"
GW_HELLO="${PI_RUN_GW:-http://${MAGPIE_ADDR}/api/hello}"
QUOTA_FAIL_PCT="${PI_RUN_QUOTA_FAIL_PCT:-90}"

usage() {
  cat <<'USAGE'
用法:
  pi-run.sh --profile scan [--out DIR] [--task FILE | -p '...'] [--expect PATH]... [--bg]
  pi-run.sh --profile code <项目目录> [--task FILE | -p '...'] [--expect PATH]... [--bg]
  pi-run.sh --profile write <输出目录> [--task FILE | -p '...'] [--expect PATH]... [--bg]

常用选项:
  --profile scan|code|write  权限档位（code/write 后须跟目录）
  --out DIR                  scan 的产物目录，默认 \$DISPATCH_HOME/out
  --task FILE                用任务书全文作为 prompt；成功标准里的绝对路径会作为默认 --expect
  --expect PATH              结束后必须存在且非空的产物（可重复）
  --model NAME               flash（默认）、pro、claude，或完整 id（映射成 magpie/antigravity/…，避免落到 -tiered）
  --provider NAME            Pi provider，默认 magpie
  --thinking LEVEL           off|minimal|low|medium|high|xhigh|max，默认 medium（复杂/高质量任务用 high）
  --timeout DUR              执行超时（默认 20m；不含排队），如 20m / 60s / 1h
  --queue-timeout DUR        等锁上限（默认 60m），超时判 fail
  --sandbox                  默认已开启 bwrap 沙箱
  --no-sandbox               关闭沙箱（仍保留 --tools 白名单；无网络隔离）
  --bg                       后台跑，立刻打印 run_id；结果写入 \$DISPATCH_HOME/status/<run_id>.json
  -h, --help                 显示本说明

环境: DISPATCH_HOME（默认 ~/.pi-dispatch）、PI_BIN、MAGPIE_BIN、MAGPIE_ADDR（默认 127.0.0.1:3425）、
PI_AGENT_DIR（默认 ~/.pi/agent）、DISPATCH_RO_ROOTS（冒号分隔的额外只读根，可选）。
固定行为: 经 MAGPIE_ADDR 的 Magpie 网关调用 Pi；默认模型 magpie/antigravity/gemini-3.8-flash；
默认 --no-session --no-context-files --no-skills --no-prompt-templates --mode json；
日志在 \$DISPATCH_HOME/logs/（每次运行只删除其中超过 14 天的文件）；
最多同时 2 个并发。Gemini 5 小时窗口用量超过 90% 时直接 FAIL: quota。
永远不加 --dangerously-skip-permissions。
USAGE
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

map_model() {
  local raw="${1:-flash}"
  case "$raw" in
    flash|gemini-3.8-flash|antigravity/gemini-3.8-flash|magpie/antigravity/gemini-3.8-flash)
      printf '%s\n' "magpie/antigravity/gemini-3.8-flash"
      ;;
    pro|gemini-pro-agent|antigravity/gemini-pro-agent|magpie/antigravity/gemini-pro-agent)
      printf '%s\n' "magpie/antigravity/gemini-pro-agent"
      ;;
    claude|claude-sonnet-4-6|antigravity/claude-sonnet-4-6|magpie/antigravity/claude-sonnet-4-6)
      printf '%s\n' "magpie/antigravity/claude-sonnet-4-6"
      ;;
    magpie/*)
      printf '%s\n' "$raw"
      ;;
    antigravity/*)
      printf '%s\n' "magpie/$raw"
      ;;
    *)
      printf '%s\n' "$raw"
      ;;
  esac
}

if [[ ! -x "$PI_BIN" ]]; then
  echo "pi-run: pi 不存在或不可执行: $PI_BIN" >&2
  exit 127
fi

PROFILE=""
PROFILE_DIR=""
OUT_DIR=""
TASK_FILE=""
PROMPT=""
MODEL_FLAG="flash"
PROVIDER="$DEFAULT_PROVIDER"
BG=0
USE_SANDBOX=1
PRINT_TIMEOUT="$DEFAULT_TIMEOUT"
QUEUE_TIMEOUT="$DEFAULT_QUEUE_TIMEOUT"
THINKING="$DEFAULT_THINKING"
EXPECTS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --profile)
      if [[ $# -lt 2 ]]; then
        echo "pi-run: --profile 需要 scan、code <目录> 或 write <目录>" >&2
        exit 2
      fi
      PROFILE="$2"
      shift 2
      case "$PROFILE" in
        scan) ;;
        code|write)
          if [[ $# -lt 1 || "$1" == -* ]]; then
            echo "pi-run: --profile $PROFILE 后面必须跟一个目录" >&2
            exit 2
          fi
          PROFILE_DIR="$1"
          shift
          ;;
        *)
          echo "pi-run: 未知档位 '$PROFILE'（应为 scan、code 或 write）" >&2
          exit 2
          ;;
      esac
      ;;
    --out)
      if [[ $# -lt 2 ]]; then
        echo "pi-run: --out 需要目录" >&2
        exit 2
      fi
      OUT_DIR="$2"
      shift 2
      ;;
    -p|--prompt)
      if [[ $# -lt 2 ]]; then
        echo "pi-run: -p/--prompt 需要文本" >&2
        exit 2
      fi
      PROMPT="$2"
      shift 2
      ;;
    --task)
      if [[ $# -lt 2 ]]; then
        echo "pi-run: --task 需要文件" >&2
        exit 2
      fi
      TASK_FILE="$2"
      shift 2
      ;;
    --expect)
      if [[ $# -lt 2 ]]; then
        echo "pi-run: --expect 需要路径" >&2
        exit 2
      fi
      EXPECTS+=("$2")
      shift 2
      ;;
    --model)
      if [[ $# -lt 2 ]]; then
        echo "pi-run: --model 需要模型短名或 id" >&2
        exit 2
      fi
      MODEL_FLAG="$2"
      shift 2
      ;;
    --provider)
      if [[ $# -lt 2 ]]; then
        echo "pi-run: --provider 需要名称" >&2
        exit 2
      fi
      PROVIDER="$2"
      shift 2
      ;;
    --thinking)
      if [[ $# -lt 2 ]]; then
        echo "pi-run: --thinking 需要级别" >&2
        exit 2
      fi
      THINKING="$2"
      shift 2
      ;;
    --timeout)
      if [[ $# -lt 2 ]]; then
        echo "pi-run: --timeout 需要时长，如 20m" >&2
        exit 2
      fi
      PRINT_TIMEOUT="$2"
      if ! to_seconds "$PRINT_TIMEOUT" >/dev/null; then
        echo "pi-run: 无法解析 --timeout '$PRINT_TIMEOUT'（支持 20m / 60s / 1h / 秒数）" >&2
        exit 2
      fi
      shift 2
      ;;
    --queue-timeout)
      if [[ $# -lt 2 ]]; then
        echo "pi-run: --queue-timeout 需要时长，如 60m" >&2
        exit 2
      fi
      QUEUE_TIMEOUT="$2"
      if ! to_seconds "$QUEUE_TIMEOUT" >/dev/null; then
        echo "pi-run: 无法解析 --queue-timeout '$QUEUE_TIMEOUT'（支持 20m / 60s / 1h / 秒数）" >&2
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
    --cwd)
      echo "pi-run: 已忽略 --cwd（工作目录由 --profile 决定）" >&2
      if [[ $# -ge 2 ]]; then shift 2; else shift; fi
      ;;
    --dangerously-skip-permissions|--skip-permissions)
      echo "pi-run: 已忽略 $1（禁止使用）" >&2
      shift
      ;;
    *)
      echo "pi-run: 未知参数: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$THINKING" in
  off|minimal|low|medium|high|xhigh|max) ;;
  *)
    echo "pi-run: 未知 --thinking '$THINKING'（应为 off|minimal|low|medium|high|xhigh|max）" >&2
    exit 2
    ;;
esac

if [[ -z "$PROFILE" ]]; then
  echo "pi-run: 必须指定 --profile scan|code|write" >&2
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
    # 只读内置工具；保留 write 以便写 --out。无 bash/powershell/codemode。
    TOOLS="read,ls,grep,find,write"
    ;;
  code)
    if [[ ! -d "$PROFILE_DIR" ]]; then
      echo "pi-run: 项目目录不存在: $PROFILE_DIR" >&2
      exit 2
    fi
    WORK_DIR="$(abs_dir "$PROFILE_DIR")"
    OUT_DIR="${OUT_DIR:-$WORK_DIR}"
    # 只读工具 + 写入/执行（bash/powershell/codemode）；tool_search 只放 code，以免在 scan/write 里声明未授权工具。
    TOOLS="read,ls,grep,find,write,edit,bash,powershell,codemode,tool_search"
    ;;
  write)
    OUT_DIR="$(abs_dir "$PROFILE_DIR")"
    WORK_DIR="$OUT_DIR"
    # 只读工具 + 原有 write/edit；无 bash。
    TOOLS="read,ls,grep,find,write,edit"
    ;;
esac

if [[ -n "$TASK_FILE" && ! -f "$TASK_FILE" ]]; then
  echo "pi-run: 任务书不存在: $TASK_FILE" >&2
  exit 2
fi

MODEL="$(map_model "${MODEL_FLAG:-flash}")"
if [[ -n "${PI_RUN_MODEL:-}" && "$MODEL_FLAG" == "flash" ]]; then
  MODEL="$(map_model "$PI_RUN_MODEL")"
fi

mkdir -p "$LOG_DIR" "$STATUS_DIR" "$RUNS_DIR" "$LOCK_DIR"
find "$LOG_DIR" -mindepth 1 -maxdepth 1 -type f -mtime +14 -delete 2>/dev/null || true

ts="$(date +%Y%m%d_%H%M%S)"
run_id="${PI_RUN_ID:-${ts}-$$}"
run_dir="$RUNS_DIR/$run_id"
mkdir -p "$run_dir" "$run_dir/real" "$run_dir/sessions" "$run_dir/pi-agent"
chmod 700 "$run_dir"

stdout_file="$LOG_DIR/${run_id}.stdout.jsonl"
stderr_file="$LOG_DIR/${run_id}.stderr.log"
pi_log_file="$LOG_DIR/${run_id}.pi.log"
status_file="$STATUS_DIR/${run_id}.json"
prompt_file="$run_dir/prompt.md"
expect_file="$run_dir/expects.txt"
denied_file="$run_dir/denied.log"
sandbox_note="$run_dir/sandbox.txt"
: >"$denied_file"
chmod 600 "$denied_file"

if [[ -n "$TASK_FILE" ]]; then
  cp -a "$TASK_FILE" "$prompt_file"
  if [[ -z "$PROMPT" ]]; then
    PROMPT="$(cat "$prompt_file")"
  fi
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
    for m in re.finditer(r"(?<![A-Za-z0-9_])(/(?:tmp|home|Users|var)[^\s`）)\]\"']+)", section):
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

if [[ -z "$PROMPT" ]]; then
  echo "pi-run: 需要 -p/--prompt 或 --task" >&2
  usage >&2
  exit 2
fi
printf '%s\n' "$PROMPT" >"$prompt_file"
: >"$expect_file"
if [[ ${#EXPECTS[@]} -gt 0 ]]; then
  printf '%s\n' "${EXPECTS[@]}" >"$expect_file"
fi

write_queued_status() {
  python3 - "$status_file" "$run_id" "$pi_log_file" "$stdout_file" "$stderr_file" "$(iso_now)" "$MODEL" "$PROFILE" "$THINKING" "$USE_SANDBOX" <<'PY'
import json, sys
status_file, run_id, log, stdout, stderr, queued_at, model, profile, thinking, sandbox = sys.argv[1:]
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
        "model": model,
        "profile": profile,
        "thinking": thinking,
        "sandbox": sandbox == "1",
        "queued_at": queued_at,
        "started_at": None,
        "finished_at": None,
    }, f, ensure_ascii=False, indent=2)
    f.write("\n")
PY
}

write_fail_now() {
  local reason="$1"
  python3 - "$status_file" "$reason" "$(iso_now)" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
reason, finished_at = sys.argv[2], sys.argv[3]
data = {}
if path.exists() and path.stat().st_size:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = {}
data.update({"status": "fail", "reason": reason, "finished_at": finished_at})
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(reason)
PY
}

write_queue_timeout() {
  write_fail_now "FAIL: queue timeout after $QUEUE_TIMEOUT"
}

patch_status() {
  python3 - "$status_file" "$@" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
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
    data[key] = None if val == "__NULL__" else val
    i += 2
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
}

quota_check() {
  python3 - "$MAGPIE_BIN" "$QUOTA_FAIL_PCT" <<'PY'
import json, subprocess, sys
magpie, limit = sys.argv[1], float(sys.argv[2])
try:
    proc = subprocess.run([magpie, "quota", "--json"], check=False, capture_output=True, text=True, timeout=30)
except Exception as e:
    print(f"FAIL: quota check failed ({e})")
    sys.exit(1)
if proc.returncode != 0 or not (proc.stdout or "").strip():
    err = (proc.stderr or proc.stdout or "no output").strip().splitlines()
    msg = err[-1] if err else "no output"
    print(f"FAIL: quota check failed ({msg})")
    sys.exit(1)
try:
    data = json.loads(proc.stdout)
except json.JSONDecodeError as e:
    print(f"FAIL: quota check failed (invalid json: {e})")
    sys.exit(1)
accounts = data if isinstance(data, list) else [data]
for acc in accounts:
    for w in acc.get("windows") or []:
        name = str(w.get("name") or "").lower()
        pool = str(w.get("pool") or "").lower()
        if "gemini" in pool and "5" in name and "hour" in name:
            used = float(w.get("used") or 0)
            if used > limit:
                print(f"FAIL: quota (Gemini 5 hours used {used:.2f}% > {limit:.0f}%)")
                sys.exit(1)
            sys.exit(0)
print("FAIL: quota check failed (Gemini 5 hours window not found)")
sys.exit(1)
PY
}

build_inner_run() {
  local mid="$MODEL"
  local prov="$PROVIDER"
  if [[ "$mid" == magpie/* ]]; then
    prov="magpie"
    mid="${mid#magpie/}"
  fi
  cat >"$run_dir/inner-run.sh" <<EOF
#!/bin/bash
set -euo pipefail
export HOME="$REAL_HOME"
export TMPDIR=/tmp
export XDG_CACHE_HOME=/tmp/xdg-cache
export XDG_STATE_HOME=/tmp/xdg-state
export XDG_RUNTIME_DIR=/tmp/runtime
export PI_CODING_AGENT_SESSION_DIR="$PI_AGENT_DIR/sessions"
export PI_RUN_DENIED_LOG="$denied_file"
export PI_RUN_REAL_GIT="$run_dir/real/git"
export PI_RUN_REAL_RM="$run_dir/real/rm"
export PATH="$CALLER_PATH"
mkdir -p /tmp/xdg-cache /tmp/xdg-state /tmp/runtime
if [[ "$USE_SANDBOX" == "1" ]]; then
  python3 "$LIB_DIR/pi-netfwd.py" --listen-tcp $MAGPIE_ADDR --connect-unix "$run_dir/magpie.sock" --ready-file /tmp/pi-fwd.ready &
  for i in \$(seq 1 80); do
    [[ -f /tmp/pi-fwd.ready ]] && break
    sleep 0.05
  done
  if [[ ! -f /tmp/pi-fwd.ready ]]; then
    echo "pi-run: inner magpie forwarder not ready" >&2
    exit 1
  fi
fi
exec "$PI_BIN" -p --mode json \\
  --no-session --no-context-files --no-skills --no-prompt-templates \\
  --thinking "$THINKING" --tools "$TOOLS" \\
  --provider "$prov" --model "$mid" \\
  -- "\$(cat "$prompt_file")"
EOF
  chmod 700 "$run_dir/inner-run.sh"
}

HOST_FWD_PID=""
start_host_forwarder() {
  HOST_FWD_PID=""
  [[ "$USE_SANDBOX" -eq 1 ]] || return 0
  python3 "$LIB_DIR/pi-netfwd.py" \
    --listen-unix "$run_dir/magpie.sock" \
    --connect-tcp "$MAGPIE_ADDR" \
    --ready-file "$run_dir/host-fwd.ready" \
    >"$run_dir/host-fwd.log" 2>&1 &
  HOST_FWD_PID=$!
  local _
  for _ in $(seq 1 80); do
    if [[ -f "$run_dir/host-fwd.ready" ]]; then
      return 0
    fi
    sleep 0.05
  done
  return 1
}

stop_host_forwarder() {
  if [[ -n "${HOST_FWD_PID:-}" ]]; then
    kill "$HOST_FWD_PID" 2>/dev/null || true
    wait "$HOST_FWD_PID" 2>/dev/null || true
    HOST_FWD_PID=""
  fi
}

prepare_pi_agent() {
  local src="$PI_AGENT_DIR"
  local dst="$run_dir/pi-agent"
  mkdir -p "$dst"
  local f
  for f in settings.json models-store.json models.json auth.json AGENTS.md; do
    if [[ -e "$src/$f" ]]; then
      cp -a "$src/$f" "$dst/$f"
    fi
  done
  chmod 700 "$dst"
}

setup_wrappers() {
  local src="$LIB_DIR/pi-wrappers"
  if [[ -x /usr/bin/git ]]; then
    cp -a /usr/bin/git "$run_dir/real/git"
  elif [[ -x /bin/git ]]; then
    cp -a /bin/git "$run_dir/real/git"
  fi
  if [[ -x /bin/rm ]]; then
    cp -a /bin/rm "$run_dir/real/rm"
  elif [[ -x /usr/bin/rm ]]; then
    cp -a /usr/bin/rm "$run_dir/real/rm"
  fi
  cp -a "$src/git.sh" "$run_dir/wrap-git"
  cp -a "$src/rm.sh" "$run_dir/wrap-rm"
  cp -a "$src/curl.sh" "$run_dir/wrap-curl"
  cp -a "$src/wget.sh" "$run_dir/wrap-wget"
  cp -a "$src/sudo.sh" "$run_dir/wrap-sudo"
  chmod 755 "$run_dir"/wrap-*
}

maybe_ro() {
  local p="$1"
  if [[ -e "$p" ]]; then
    BWRAP_ARGS+=(--ro-bind "$p" "$p")
  fi
}

maybe_wrap() {
  local dest="$1"
  local wrap="$2"
  if [[ -e "$dest" || -L "$dest" ]]; then
    BWRAP_ARGS+=(--ro-bind "$wrap" "$dest")
  fi
}

ro_bind_roots() {
  local IFS=':'
  local root
  for root in $DISPATCH_RO_ROOTS; do
  [ -n "$root" ] || continue
  maybe_ro "$root"
  done
}

write_bwrap_runner() {
  BWRAP_ARGS=(
    --die-with-parent
    --unshare-user
    --unshare-pid
    --unshare-net
    --clearenv
    --setenv HOME "$REAL_HOME"
    --setenv USER "$REAL_USER"
    --setenv LOGNAME "$REAL_USER"
    --setenv LANG C.UTF-8
    --setenv LC_ALL C.UTF-8
    --setenv TERM xterm-256color
    --setenv PATH "$CALLER_PATH"
    --setenv TMPDIR /tmp
    --setenv XDG_CACHE_HOME /tmp/xdg-cache
    --setenv XDG_STATE_HOME /tmp/xdg-state
    --setenv XDG_RUNTIME_DIR /tmp/runtime
    --proc /proc
    --dev /dev
    --tmpfs /tmp
    --chdir "$WORK_DIR"
  )
  maybe_ro /usr
  maybe_ro /usr/local
  maybe_ro /bin
  maybe_ro /sbin
  maybe_ro /lib
  maybe_ro /lib64
  maybe_ro /etc
  maybe_ro "$REAL_HOME"
  ro_bind_roots
  BWRAP_ARGS+=(--bind "$OUT_DIR" "$OUT_DIR")
  if [[ "$WORK_DIR" != "$OUT_DIR" ]]; then
    BWRAP_ARGS+=(--bind "$WORK_DIR" "$WORK_DIR")
  fi
  BWRAP_ARGS+=(--bind "$denied_file" "$denied_file")
  BWRAP_ARGS+=(--bind "$run_dir/magpie.sock" "$run_dir/magpie.sock")
  BWRAP_ARGS+=(--bind "$run_dir/pi-agent" "$PI_AGENT_DIR")
  if [[ -d "$PI_AGENT_DIR/install" ]]; then
    BWRAP_ARGS+=(--ro-bind "$PI_AGENT_DIR/install" "$PI_AGENT_DIR/install")
  fi
  if [[ -d "$PI_AGENT_DIR/npm" ]]; then
    BWRAP_ARGS+=(--ro-bind "$PI_AGENT_DIR/npm" "$PI_AGENT_DIR/npm")
  fi
  if [[ -d "$PI_AGENT_DIR/bin" ]]; then
    BWRAP_ARGS+=(--ro-bind "$PI_AGENT_DIR/bin" "$PI_AGENT_DIR/bin")
  fi
  BWRAP_ARGS+=(--ro-bind "$run_dir/inner-run.sh" "$run_dir/inner-run.sh")
  BWRAP_ARGS+=(--ro-bind "$prompt_file" "$prompt_file")
  BWRAP_ARGS+=(--ro-bind "$LIB_DIR/pi-netfwd.py" "$LIB_DIR/pi-netfwd.py")
  BWRAP_ARGS+=(--ro-bind "$run_dir/real" "$run_dir/real")
  maybe_wrap /usr/bin/curl "$run_dir/wrap-curl"
  maybe_wrap /bin/curl "$run_dir/wrap-curl"
  maybe_wrap /usr/bin/wget "$run_dir/wrap-wget"
  maybe_wrap /bin/wget "$run_dir/wrap-wget"
  maybe_wrap /usr/bin/sudo "$run_dir/wrap-sudo"
  maybe_wrap /bin/sudo "$run_dir/wrap-sudo"
  maybe_wrap /usr/bin/git "$run_dir/wrap-git"
  maybe_wrap /bin/git "$run_dir/wrap-git"
  maybe_wrap /usr/bin/rm "$run_dir/wrap-rm"
  maybe_wrap /bin/rm "$run_dir/wrap-rm"
  cat >"$sandbox_note" <<EOF
sandbox=bwrap --unshare-net
writable=$WORK_DIR $OUT_DIR
tools=$TOOLS
thinking=$THINKING
model=$MODEL
hard: ro \$HOME (+ DISPATCH_RO_ROOTS) except writable binds; net only MAGPIE_ADDR via unix socket forwarder; wrappers over curl/wget/sudo/git push/rm -r
soft: --tools allowlist (scan has no bash)
Pi state: per-run copy under PI_AGENT_DIR; install/npm/bin are ro binds; tmpfs /tmp
EOF
  {
    printf '#!/bin/bash\nset -euo pipefail\nexec bwrap'
    local a
    for a in "${BWRAP_ARGS[@]}"; do
      printf ' %q' "$a"
    done
    printf ' -- /bin/bash %q\n' "$run_dir/inner-run.sh"
  } >"$run_dir/bwrap-run.sh"
  chmod 700 "$run_dir/bwrap-run.sh"
}

run_unsandboxed() {
  cat >"$sandbox_note" <<EOF
sandbox=off
tools=$TOOLS
thinking=$THINKING
model=$MODEL
note: --no-sandbox skips bwrap; --tools allowlist still applies; no net or filesystem isolation
EOF
  export PI_RUN_DENIED_LOG="$denied_file"
  export PI_RUN_REAL_GIT="${PI_RUN_REAL_GIT:-/usr/bin/git}"
  export PI_RUN_REAL_RM="${PI_RUN_REAL_RM:-/bin/rm}"
  bash "$run_dir/inner-run.sh"
}

run_and_judge() {
  if ! curl -s -o /dev/null --max-time 2 "$GW_HELLO"; then
    write_fail_now "FAIL: magpie gateway not answering at $MAGPIE_ADDR (run: magpie serve)"
    return 1
  fi

  local qmsg qrc
  set +e
  qmsg="$(quota_check)"
  qrc=$?
  set -e
  if [[ $qrc -ne 0 ]]; then
    write_fail_now "${qmsg:-FAIL: quota check failed}"
    return 1
  fi

  if [[ "$USE_SANDBOX" -eq 1 ]]; then
    if ! command -v bwrap >/dev/null 2>&1; then
      write_fail_now "FAIL: bwrap not found (install bubblewrap: apt install bubblewrap / brew install bubblewrap; do not use --no-sandbox in production)"
      return 1
    fi
    if [[ ! -x "$LIB_DIR/pi-netfwd.py" ]]; then
      write_fail_now "FAIL: missing $LIB_DIR/pi-netfwd.py"
      return 1
    fi
  fi

  build_inner_run
  setup_wrappers
  prepare_pi_agent
  trap stop_host_forwarder EXIT

  local start end elapsed pi_rc timeout_secs
  timeout_secs="$(to_seconds "$PRINT_TIMEOUT")"
  start="$(date +%s.%N)"
  patch_status status running started_at "$(iso_now)"

  if [[ "$USE_SANDBOX" -eq 1 ]]; then
    if ! start_host_forwarder; then
      stop_host_forwarder
      write_fail_now "FAIL: host magpie forwarder not ready"
      return 1
    fi
  fi

  if [[ "$USE_SANDBOX" -eq 1 ]]; then
    write_bwrap_runner
    runner="$run_dir/bwrap-run.sh"
  else
    cat >"$sandbox_note" <<EOF
sandbox=off
tools=$TOOLS
thinking=$THINKING
model=$MODEL
note: --no-sandbox skips bwrap; --tools allowlist still applies; no net or filesystem isolation
EOF
    runner="$run_dir/inner-run.sh"
  fi
  set +e
  timeout --signal=TERM --kill-after=15s "$timeout_secs" \
    bash "$runner" >"$stdout_file" 2>"$stderr_file"
  pi_rc=$?
  set -e
  stop_host_forwarder
  trap - EXIT

  end="$(date +%s.%N)"
  elapsed="$(python3 -c 'import sys; print(round(float(sys.argv[2])-float(sys.argv[1]), 3))' "$start" "$end")"
  {
    echo "provider=$PROVIDER model=$MODEL profile=$PROFILE thinking=$THINKING sandbox=$USE_SANDBOX cwd=$WORK_DIR tools=$TOOLS exit=$pi_rc duration=$elapsed"
    echo "---- stderr ----"
    cat "$stderr_file" 2>/dev/null || true
    echo "---- denied ----"
    cat "$denied_file" 2>/dev/null || true
  } >"$pi_log_file"

  python3 - "$status_file" "$run_id" "$stdout_file" "$stderr_file" "$pi_log_file" "$expect_file" "$denied_file" "$elapsed" "$pi_rc" "$(iso_now)" "$MODEL" "$PRINT_TIMEOUT" "$PROFILE" "$THINKING" "$USE_SANDBOX" <<'PY'
import json, os, re, sys
from pathlib import Path

(status_file, run_id, stdout_file, stderr_file, log_file, expect_file,
 denied_file, elapsed, pi_rc, finished_at, model, timeout, profile,
 thinking, sandbox) = sys.argv[1:]
pi_rc = int(pi_rc)
elapsed = float(elapsed)
expects = [ln.strip() for ln in Path(expect_file).read_text(encoding="utf-8").splitlines() if ln.strip()]

existing = {}
sp = Path(status_file)
if sp.exists() and sp.stat().st_size:
    try:
        existing = json.loads(sp.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        existing = {}

raw = Path(stdout_file).read_text(encoding="utf-8", errors="replace")
err = Path(stderr_file).read_text(encoding="utf-8", errors="replace")
denied_text = Path(denied_file).read_text(encoding="utf-8", errors="replace") if Path(denied_file).exists() else ""

reasons = []
events = []
parse_error = None
for i, line in enumerate(raw.splitlines(), 1):
    s = line.strip()
    if not s:
        continue
    try:
        events.append(json.loads(s))
    except json.JSONDecodeError as e:
        parse_error = f"line {i}: {e}"
        break

usage = None
denied_actions = []

def add_usage(u):
    global usage
    if not isinstance(u, dict):
        return
    if usage is None:
        usage = {
            "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0,
            "totalTokens": 0, "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "total": 0},
        }
    for k in ("input", "output", "cacheRead", "cacheWrite", "totalTokens"):
        try:
            usage[k] = usage.get(k, 0) + float(u.get(k) or 0)
        except (TypeError, ValueError):
            pass
    c = u.get("cost") or {}
    if isinstance(c, dict):
        for k in ("input", "output", "cacheRead", "cacheWrite", "total"):
            try:
                usage["cost"][k] = usage["cost"].get(k, 0) + float(c.get(k) or 0)
            except (TypeError, ValueError):
                pass

# Prefer per-turn message_end usage; else last message_update per turn.
turn_usage = None
for ev in events:
    typ = ev.get("type") if isinstance(ev, dict) else None
    if typ == "turn_start":
        turn_usage = None
    if typ in ("message_update", "message_end", "turn_end") and isinstance(ev.get("usage"), dict):
        turn_usage = ev["usage"]
    msg = ev.get("message") if isinstance(ev, dict) else None
    if isinstance(msg, dict) and isinstance(msg.get("usage"), dict):
        turn_usage = msg["usage"]
    if typ == "turn_end" and turn_usage:
        add_usage(turn_usage)
        turn_usage = None
if turn_usage:
    add_usage(turn_usage)

deny_re = re.compile(
    r"pi-run: denied command\(([^)]+)\)|Read-only file system|EROFS|Permission denied|Network is unreachable",
    re.I,
)
settings_noise_re = re.compile(r"Invalid settings file|settings\.json\.lock", re.I)

def looks_denied(text: str) -> bool:
    if not text:
        return False
    cleaned = "\n".join(ln for ln in text.splitlines() if not settings_noise_re.search(ln))
    return bool(deny_re.search(cleaned))

def forbidden_bash(cmd: str) -> str | None:
    if not cmd:
        return None
    s = cmd.strip()
    # rough argv split is enough for deny detection
    if re.search(r'(^|[;&|\n]|\bsudo\s+|[\s])curl(\s|$)', s) or re.search(r'\bcurl\b', s):
        if re.search(r'(^|[;&|\n]\s*)curl\b', s) or re.search(r'\bsudo\s+curl\b', s):
            return "curl"
    if re.search(r'(^|[;&|\n]\s*)wget\b', s):
        return "wget"
    if re.search(r'(^|[;&|\n]\s*)sudo\b', s):
        return "sudo"
    if re.search(r'\bgit\b.*\bpush\b', s) or re.search(r'(^|[;&|\n]\s*)git\s+push\b', s):
        return "git push"
    if re.search(r'(^|[;&|\n]\s*)rm\s+-[A-Za-z]*[rR]', s) or re.search(r'\brm\s+--recursive\b', s):
        return "rm -r"
    if "pi-run: denied command" in s:
        m = re.search(r"denied command\(([^)]+)\)", s)
        return m.group(1) if m else "command"
    return None

call_args = {}
for ev in events:
    if not isinstance(ev, dict):
        continue
    typ = ev.get("type")
    cid = ev.get("toolCallId") or ev.get("id")
    if typ == "tool_execution_start":
        call_args[cid] = ev.get("args") or {}
    if typ == "tool_execution_end" and ev.get("isError"):
        result = ev.get("result") or {}
        blob = json.dumps(result, ensure_ascii=False) if not isinstance(result, str) else result
        name = str(ev.get("toolName") or "tool")
        args = ev.get("args") or call_args.get(cid) or {}
        if name in ("write", "edit") and looks_denied(blob):
            denied_actions.append(f"{name}")
        elif name == "bash":
            cmd = ""
            if isinstance(args, dict):
                cmd = str(args.get("command") or args.get("cmd") or "")
            why = forbidden_bash(cmd) or forbidden_bash(blob)
            if why:
                denied_actions.append(f"bash:{why}")
            # incidental EROFS (e.g. ln into a ro path) is not a denied action

for ln in denied_text.splitlines():
    s = ln.strip()
    if s and s not in denied_actions:
        denied_actions.append(s)

if looks_denied(err) and not denied_actions:
    denied_actions.append("sandbox denial")

if parse_error and events:
    # trailing garbage after valid events
    pass
elif parse_error and not events:
    reasons.append(f"FAIL: invalid json ({parse_error})")
elif not events and pi_rc == 0:
    reasons.append("FAIL: empty json output")

if pi_rc == 124 or pi_rc == 137:
    reasons.append(f"FAIL: timeout after {timeout}")
elif pi_rc != 0:
    reasons.append(f"FAIL: pi exit {pi_rc}")

if denied_actions:
    reasons.append("FAIL: denied " + ", ".join(denied_actions))

blob = (raw + "\n" + err).lower()
for needle, label in (
    ("not signed in", "not signed in"),
    ("unauthorized", "unauthorized"),
    ("invalid api key", "invalid api key"),
    ("no models yet", "no models yet"),
    ("econnrefused", "gateway connection refused"),
    ("unknown provider", "unknown provider"),
    ("requested entity was not found", "model not found"),
):
    if needle in blob and not any(label in r for r in reasons):
        reasons.append(f"FAIL: {label}")

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

# usage counts were summed per turn; keep ints when whole
if usage:
    for k in ("input", "output", "cacheRead", "cacheWrite", "totalTokens"):
        v = usage[k]
        usage[k] = int(v) if float(v).is_integer() else v

payload = {
    "run_id": existing.get("run_id", run_id),
    "status": "ok" if ok else "fail",
    "reason": verdict,
    "artifacts": present,
    "duration_seconds": elapsed,
    "usage": usage,
    "log": log_file,
    "stdout": stdout_file,
    "stderr": stderr_file,
    "pi_exit": pi_rc,
    "model": model,
    "profile": profile,
    "thinking": thinking,
    "sandbox": sandbox == "1",
    "denied_actions": denied_actions,
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
  local wait_secs deadline now got
  wait_secs="$(to_seconds "$QUEUE_TIMEOUT")"
  deadline="$(python3 -c "import time,sys; print(time.time()+float(sys.argv[1]))" "$wait_secs")"
  exec 8>>"$LOCK_DIR/.pi.lock.0"
  exec 9>>"$LOCK_DIR/.pi.lock.1"
  got=0
  while true; do
    if flock -n 8; then got=8; break; fi
    if flock -n 9; then got=9; break; fi
    now="$(python3 -c 'import time; print(time.time())')"
    if python3 -c "import sys; sys.exit(0 if float(sys.argv[1])>=float(sys.argv[2]) else 1)" "$now" "$deadline"; then
      break
    fi
    sleep 0.2
  done
  if [[ "$got" -eq 0 ]]; then
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
