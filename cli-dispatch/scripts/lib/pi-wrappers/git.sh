#!/bin/sh
log="${PI_RUN_DENIED_LOG:-}"
real="${PI_RUN_REAL_GIT:-}"
deny=0
for a in "$@"; do
  if [ "$a" = "push" ] || [ "$a" = "send-pack" ]; then
    deny=1
    break
  fi
done
if [ "$deny" -eq 1 ]; then
  if [ -n "$log" ]; then
    printf 'git push %s\n' "$*" >> "$log" 2>/dev/null
  fi
  printf 'pi-run: denied command(git push)\n' >&2
  exit 1
fi
if [ -n "$real" ] && [ -x "$real" ]; then
  exec "$real" "$@"
fi
printf 'pi-run: git wrapper missing real git\n' >&2
exit 127
