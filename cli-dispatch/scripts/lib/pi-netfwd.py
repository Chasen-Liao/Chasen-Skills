#!/usr/bin/env python3
"""Forward TCP <-> TCP or Unix socket. Used to expose 127.0.0.1:3425 inside a bwrap netns."""
from __future__ import annotations

import argparse
import errno
import os
import selectors
import socket
import sys
import threading


def parse_addr(kind: str, value: str):
    if kind == "unix":
        return "unix", value
    host, port = value.rsplit(":", 1)
    return "tcp", (host, int(port))


def make_listening(kind, addr):
    if kind == "unix":
        try:
            os.unlink(addr)
        except FileNotFoundError:
            pass
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(addr)
        os.chmod(addr, 0o600)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addr)
    sock.listen(128)
    sock.setblocking(False)
    return sock


def connect_peer(kind, addr, timeout=3):
    if kind == "unix":
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect(addr)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect(addr)
    sock.settimeout(None)
    sock.setblocking(True)
    return sock


def pipe(a: socket.socket, b: socket.socket):
    try:
        while True:
            data = a.recv(65536)
            if not data:
                try:
                    b.shutdown(socket.SHUT_WR)
                except OSError:
                    pass
                break
            b.sendall(data)
    except OSError:
        pass
    finally:
        try:
            a.close()
        except OSError:
            pass


def handle(client, peer_kind, peer_addr):
    try:
        peer = connect_peer(peer_kind, peer_addr)
    except OSError as e:
        try:
            client.close()
        except OSError:
            pass
        sys.stderr.write(f"pi-netfwd: connect failed: {e}\n")
        return
    t1 = threading.Thread(target=pipe, args=(client, peer), daemon=True)
    t2 = threading.Thread(target=pipe, args=(peer, client), daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    try:
        peer.close()
    except OSError:
        pass


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--listen-tcp", metavar="HOST:PORT")
    g.add_argument("--listen-unix", metavar="PATH")
    g2 = p.add_mutually_exclusive_group(required=True)
    g2.add_argument("--connect-tcp", metavar="HOST:PORT")
    g2.add_argument("--connect-unix", metavar="PATH")
    p.add_argument("--ready-file", metavar="PATH", help="create this file after listen succeeds")
    args = p.parse_args()

    if args.listen_tcp:
        lkind, laddr = parse_addr("tcp", args.listen_tcp)
    else:
        lkind, laddr = parse_addr("unix", args.listen_unix)
    if args.connect_tcp:
        pkind, paddr = parse_addr("tcp", args.connect_tcp)
    else:
        pkind, paddr = parse_addr("unix", args.connect_unix)

    sock = make_listening(lkind, laddr)
    if args.ready_file:
        with open(args.ready_file, "w", encoding="utf-8") as f:
            f.write("ready\n")
    # stay in foreground; parent uses --die-with-parent / trap
    while True:
        try:
            sel = selectors.DefaultSelector()
            sel.register(sock, selectors.EVENT_READ)
            sel.select()
            client, _ = sock.accept()
            client.setblocking(True)
            threading.Thread(target=handle, args=(client, pkind, paddr), daemon=True).start()
        except OSError as e:
            if e.errno == errno.EINTR:
                continue
            raise


if __name__ == "__main__":
    main()
