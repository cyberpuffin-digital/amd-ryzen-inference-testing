#!/usr/bin/env python3
"""Keep private names out of results and out of the public repository.

    bench/redact.py filter < in > out     # replace private names with [redacted]
    bench/redact.py check FILE...         # exit 1 if any file contains one
    bench/redact.py check --staged        # the files staged for commit (pre-commit hook)
    bench/redact.py check --message FILE  # a commit message (commit-msg hook)
    bench/redact.py check --push RANGE    # pushed commits: tree, messages, identities (pre-push hook)
    bench/redact.py patterns              # list the patterns in use (to check the setup)
    bench/redact.py --self-test           # check the built-in patterns

What counts as private is never written in this repository, since a list of
private names in a public file would publish them. It comes from:

- this machine: its hostname (short and fully qualified), the DNS search
  domains in /etc/resolv.conf, and the username;
- a local file, one regular expression per line (# for comments), for
  anything else: internal domains, other hosts, project names. Default
  ${XDG_CONFIG_HOME:-~/.config}/amd-ryzen-inference/redact.txt, or
  $REDACT_FILE. See bench/redact.example.txt.

In CI (.forgejo/workflows/sanitize.yaml) the local file comes from an Actions
secret, and two switches apply: REDACT_NO_DERIVED=1 skips the machine's own
names (a runner's are irrelevant, and a username like "root" would flag
ordinary text), and REDACT_HIDE_MATCHES=1 reports the pattern's number
instead of the matched text, because public CI logs must not show what was
found.

Also built in, because they are never wanted in published results: every IPv4
and IPv6 address (private, CGNAT and public alike) and MAC addresses.
`bench/redact.py --self-test` checks them against addresses and look-alikes
(version strings, timestamps, C++ scopes).

Home-directory paths are rewritten to ~ by `filter` before the patterns run.
Standard library only.
"""
import getpass
import os
import pathlib
import re
import socket
import subprocess
import sys

_OCTET = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
_H = r"[0-9a-f]{1,4}"
BUILT_IN = [
    # Every IPv4 address, not only private ranges: CGNAT (100.64/10), VPN
    # endpoints and WAN addresses are just as identifying. Each part must be
    # 0-255, and a dotted quad inside a longer run of dots (a 5-part version
    # string) doesn't count.
    rf"(?<![\d.]){_OCTET}(?:\.{_OCTET}){{3}}(?![\d.]*\d)",
    # IPv6: full form (8 groups) or compressed with "::". Eight groups or a
    # "::" are required, so clock times like 12:09:42 don't match, and no
    # letter, digit or underscore may touch either end, so C++ scopes like
    # std::vector and vk::DeviceLostError in llama.cpp's errors don't either.
    rf"(?<![\w:])(?:{_H}:){{7}}{_H}(?![\w:])",
    rf"(?<![\w:])(?:{_H}:){{1,6}}:(?:{_H}(?::{_H}){{0,5}})?(?![\w:])",
    rf"(?<![\w:])::(?:{_H}(?::{_H}){{0,6}})(?![\w:])",
    # MAC addresses.
    r"\b[0-9a-f]{2}(?:[:-][0-9a-f]{2}){5}\b",
]
# Derived names this short are too generic to redact safely (e.g. "lan").
MIN_DERIVED = 4


def redact_file():
    if os.environ.get("REDACT_FILE"):
        return pathlib.Path(os.environ["REDACT_FILE"])
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    return pathlib.Path(base) / "amd-ryzen-inference" / "redact.txt"


def derived_names():
    names = {socket.gethostname(), socket.getfqdn(), getpass.getuser()}
    try:
        for line in pathlib.Path("/etc/resolv.conf").read_text().splitlines():
            parts = line.split()
            if parts and parts[0] in ("search", "domain"):
                names.update(parts[1:])
    except OSError:
        pass
    return sorted(n.rstrip(".") for n in names if n and len(n.rstrip(".")) >= MIN_DERIVED)


def patterns():
    pats = [] if os.environ.get("REDACT_NO_DERIVED") == "1" else [re.escape(n) for n in derived_names()]
    f = redact_file()
    if f.exists():
        for line in f.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                pats.append(line)
    pats += BUILT_IN
    return [re.compile(p, re.IGNORECASE) for p in pats]


def redact(text, pats):
    home = os.path.expanduser("~")
    text = text.replace(home, "~")
    for p in pats:
        text = p.sub("[redacted]", text)
    return text


def find(text, pats):
    """[(line number, matched text, pattern number)] for every private name in text."""
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for i, p in enumerate(pats, 1):
            hits += [(n, m.group(0), i) for m in p.finditer(line)]
    return hits


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def report(where, hits):
    hide = os.environ.get("REDACT_HIDE_MATCHES") == "1"
    for n, m, i in hits:
        # Show where, not the whole line: the line itself may be the leak.
        what = f"(pattern {i})" if hide else f"'{m}'"
        print(f"{where}:{n}: private name {what}", file=sys.stderr)
    return bool(hits)


def check(args, pats):
    bad = False
    if args[:1] == ["--staged"]:
        for path in git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split("\0"):
            if path:
                bad |= report(path, find(git("show", f":{path}"), pats))
        bad |= report("author", find(git("var", "GIT_AUTHOR_IDENT"), pats))
        bad |= report("committer", find(git("var", "GIT_COMMITTER_IDENT"), pats))
    elif args[:1] == ["--message"]:
        bad |= report("commit message", find(pathlib.Path(args[1]).read_text(), pats))
    elif args[:1] == ["--push"]:
        rng = args[1]
        meta = git("log", "--format=%H%n%an <%ae>%n%cn <%ce>%n%B", rng)
        bad |= report(f"commits {rng}", find(meta, pats))
        tip = rng.split("..")[-1]
        for path in git("ls-tree", "-r", "--name-only", "-z", tip).split("\0"):
            if path:
                try:
                    content = git("show", f"{tip}:{path}")
                except (subprocess.CalledProcessError, UnicodeDecodeError):
                    continue
                bad |= report(f"{tip[:12]}:{path}", find(content, pats))
    else:
        for path in args:
            try:
                bad |= report(path, find(pathlib.Path(path).read_text(), pats))
            except UnicodeDecodeError:
                continue
    return 1 if bad else 0


def self_test():
    """Built-in patterns only (no machine or local names). The addresses are
    documentation and reserved ranges, assembled at run time so this file
    contains no literal address for the pre-commit check to trip on."""
    ip4 = lambda *o: ".".join(map(str, o))
    ip6 = ":".join
    must_redact = [
        ip4(192, 0, 2, 17), ip4(10, 1, 2, 3), ip4(100, 64, 1, 2),        # TEST-NET-1, private, CGNAT
        f"endpoint {ip4(203, 0, 113, 9)}:51822",                          # TEST-NET-3 with a port
        ip6(["2001", "db8", "1", "2", "3", "4", "5", "6"]),               # full IPv6
        ip6(["2001", "db8", ""]) + ":1", "fe80" + ":" + ":1/64", ":" + ":1",  # compressed IPv6
        f"[{ip6(['2001', 'db8', ''])}:1]:443",                            # bracketed with a port
        ip6(["aa", "bb", "cc", "dd", "ee", "ff"]), "-".join(["AA"] * 6),  # MAC addresses
    ]
    must_keep = [
        "version: 0.8.0-dev (build 12020, commit 0ec4027a2)",
        "Mesa 26.0.8-1ubuntu0.3, libvulkan 1.4.341.0, kernel 7.0.0-38-generic",
        "captured 2026-10-31T15:59:43Z at 12:09:42",
        "Qwen3-30B-A3B-Instruct-2507-UD-Q4_K_XL.gguf",
        "pp2048 @ d8192 | 81.82 ± 0.00 | GTT 15438 MiB | ratio 1.36x",
        "bios 03.20 (06/23/2026), pci 0x15bf rev 0xc4",
        "a five-part version 1.2.3.4.5",
        "terminate called after throwing an instance of vk::DeviceLostError",
        "std::vector<int> and ggml::cpu and llama_model_loader: - kv 0: general.architecture",
    ]
    pats = [re.compile(p, re.IGNORECASE) for p in BUILT_IN]
    failed = [f"missed: {s}" for s in must_redact if "[redacted]" not in redact(s, pats)]
    failed += [f"false positive: {s} -> {redact(s, pats)}" for s in must_keep if redact(s, pats) != s]
    for f in failed:
        print(f, file=sys.stderr)
    print("self-test " + ("FAILED" if failed else f"ok ({len(must_redact) + len(must_keep)} cases)"))
    return 1 if failed else 0


def main():
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    if cmd == "--self-test":
        return self_test()
    pats = patterns()
    if cmd == "filter":
        sys.stdout.write(redact(sys.stdin.read(), pats))
        return 0
    if cmd == "check":
        return check(args, pats)
    if cmd == "patterns":
        print(f"local file: {redact_file()} ({'found' if redact_file().exists() else 'missing'})")
        for p in pats:
            print(p.pattern)
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
