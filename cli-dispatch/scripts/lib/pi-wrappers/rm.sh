#!/bin/sh
log="${PI_RUN_DENIED_LOG:-}"
real="${PI_RUN_REAL_RM:-}"
deny=0
for a in "$@"; do
  case "$a" in
    --recursive) deny=1 ;;
    --*) ;;
    -*)
      flags=$(printf '%s' "$a" | tr -d '-')
      case "$flags" in
        *[rR]*) deny=1 ;;
      esac
      ;;
  esac
done
if [ "$deny" -eq 1 ]; then
  if [ -n "$log" ]; then
    printf 'rm %s\n' "$*" >> "$log" 2>/dev/null
  fi
  printf 'pi-run: denied command(rm -r)\n' >&2
  exit 1
fi
if [ -n "$real" ] && [ -x "$real" ]; then
  exec "$real" "$@"
fi
printf 'pi-run: rm wrapper missing real rm\n' >&2
exit 127
