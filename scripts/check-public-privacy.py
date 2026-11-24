#!/usr/bin/env python3
"""Lightweight privacy & secret guard for public skill content.

Scans tracked text files in this repository (or paths passed on argv) for
obvious personal identifiers, contact info, private host paths, internal IDs,
and secrets. All matched snippets are masked before printing.

Exit codes:
  0 - clean
  1 - potential leak(s) detected
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

ALLOWED_EMAIL_SUFFIXES = (
    "@users.noreply.github.com",
    "@example.com",
    "@example.org",
)
ALLOWED_EMAILS = {"noreply@github.com", "cursoragent@cursor.com"}

SAFE_HOME_USERS = {"user", "me", "example", "your-user", "<user>"}
SAFE_IPV4_PREFIXES = ("0.", "127.")


def mask_value(kind: str, raw: str) -> str:
    val = raw.strip()
    if kind in ("PRIVATE_KEY", "SECRET_TOKEN", "WEBHOOK_URL"):
        return f"{val[:6]}***{val[-4:]}" if len(val) > 12 else "***"
    if kind == "EMAIL":
        local, _, domain = val.partition("@")
        masked = f"{local[:2]}***{local[-1:]}" if len(local) > 3 else "***"
        return f"{masked}@{domain}"
    if kind == "UUID":
        return f"{val[:8]}-****-****-****-{val[-4:]}"
    if kind == "PHONE":
        return f"{val[:3]}****{val[-2:]}"
    if kind in ("IPV4", "TAILSCALE"):
        parts = val.split(".")
        return f"{parts[0]}.{parts[1]}.***.***" if len(parts) == 4 else "***"
    if kind == "PRIVATE_PATH":
        return re.sub(
            r"(/(?:Users|home)/|\\Users\\)([A-Za-z0-9._-]+)",
            lambda m: m.group(1) + m.group(2)[:2] + "***",
            val,
        )
    return val[:4] + "***"


RULES: list[tuple[str, re.Pattern[str]]] = [
    ("PRIVATE_KEY", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    (
        "SECRET_TOKEN",
        re.compile(
            r"\b(?:"
            r"ghp_[A-Za-z0-9]{20,}|"
            r"gho_[A-Za-z0-9]{20,}|"
            r"github_pat_[A-Za-z0-9_]{20,}|"
            r"sk-[A-Za-z0-9\-_]{20,}|"
            r"xox[baprs]-[A-Za-z0-9\-]{10,}|"
            r"AIza[0-9A-Za-z\-_]{30,}|"
            r"AKIA[0-9A-Z]{16}|"
            r"Bearer\s+(?!\$|<)[A-Za-z0-9\-_\.]{16,}"
            r")"
        ),
    ),
    (
        "WEBHOOK_URL",
        re.compile(
            r"https?://(?:"
            r"hooks\.slack\.com/|"
            r"discord(?:app)?\.com/api/webhooks/|"
            r"open\.feishu\.cn/open-apis/bot/v2/hook/|"
            r"qyapi\.weixin\.qq\.com/cgi-bin/webhook/|"
            r"oapi\.dingtalk\.com/robot/send"
            r")[^\s\"'<>]*",
            re.I,
        ),
    ),
    ("EMAIL", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("PHONE", re.compile(r"(?<!\d)(?:\+?86[-\s]?)?1[3-9]\d{9}(?!\d)")),
    (
        "UUID",
        re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
    ),
    (
        "TAILSCALE",
        re.compile(
            r"[A-Za-z0-9._-]+\.ts\.net\b|"
            r"\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3}\b",
            re.I,
        ),
    ),
    (
        "IPV4",
        re.compile(
            r"\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}"
            r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b"
        ),
    ),
    (
        "PRIVATE_PATH",
        re.compile(
            r"(?:/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|[A-Za-z]:\\Users\\[A-Za-z0-9._-]+)"
        ),
    ),
    ("INTERNAL_REF", re.compile(r"\bsand-workflow:[A-Za-z0-9_-]+", re.I)),
]


def is_ignored_match(kind: str, val: str) -> bool:
    if kind == "EMAIL":
        low = val.lower()
        return low in ALLOWED_EMAILS or any(
            low.endswith(s) for s in ALLOWED_EMAIL_SUFFIXES
        )
    if kind == "IPV4":
        return val.startswith(SAFE_IPV4_PREFIXES)
    if kind == "PRIVATE_PATH":
        user = re.split(r"[/\\]", val.rstrip("/\\"))[-1].lower()
        return user in SAFE_HOME_USERS
    return False


def list_target_files(args: list[str]) -> list[pathlib.Path]:
    if args:
        return [pathlib.Path(a) for a in args if pathlib.Path(a).is_file()]
    out = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=REPO_ROOT,
        text=True,
    )
    return [
        REPO_ROOT / line
        for line in out.splitlines()
        if line and (REPO_ROOT / line).is_file()
    ]


def scan_text(label: str, text: str) -> list[tuple[str, int, str, str]]:
    hits: list[tuple[str, int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for kind, rx in RULES:
            for match in rx.finditer(line):
                val = match.group(0)
                if is_ignored_match(kind, val):
                    continue
                hits.append((label, lineno, kind, mask_value(kind, val)))
    return hits


def main(argv: list[str]) -> int:
    if argv == ["--stdin"]:
        hits = scan_text("<stdin>", sys.stdin.read())
    else:
        hits = []
        for path in list_target_files(argv):
            if path.resolve() == pathlib.Path(__file__).resolve():
                continue
            raw = path.read_bytes()
            if b"\x00" in raw[:8192]:
                continue
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                continue
            try:
                label = str(path.resolve().relative_to(REPO_ROOT))
            except ValueError:
                label = str(path)
            hits.extend(scan_text(label, text))

    if hits:
        print(f"Found {len(hits)} potential privacy/secret issue(s):")
        for label, lineno, kind, masked in hits:
            print(f"  [{kind}] {label}:{lineno} -> {masked}")
        return 1

    print("OK: no obvious secrets, UUIDs, personal contacts, or private paths found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
