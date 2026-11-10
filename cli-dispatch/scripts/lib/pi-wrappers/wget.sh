#!/bin/sh
log="${PI_RUN_DENIED_LOG:-}"
cmd="$(basename "$0")"
if [ -n "$log" ]; then
  printf '%s %s\n' "$cmd" "$*" >> "$log" 2>/dev/null
fi
printf 'pi-run: denied command(%s)\n' "$cmd" >&2
exit 1
