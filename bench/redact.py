#!/usr/bin/env python3
"""Keep private names out of results and out of the public repository.

    bench/redact.py filter < in > out     # replace private names with [redacted]
    bench/redact.py check FILE...         # exit 1 if any file contains one
    bench/redact.py check --staged        # the files staged for commit (pre-commit hook)
    bench/redact.py check --message FILE  # a commit message (commit-msg hook)
    bench/redact.py check --push RANGE    # pushed commits: tree, messages, identities (pre-push hook)
    bench/redact.py patterns              # list the patterns in use (to check the setup)

What counts as private is never written in this repository, since a list of
private names in a public file would publish them. It comes from:

- this machine: its hostname (short and fully qualified), the DNS search
  domains in /etc/resolv.conf, and the username;
- a local file, one regular expression per line (# for comments), for
  anything else: internal domains, other hosts, project names. Default
  ${XDG_CONFIG_HOME:-~/.config}/amd-ryzen-inference/redact.txt, or
  $REDACT_FILE. See bench/redact.example.txt.

Also built in, because they are never wanted in published results: private
IPv4 addresses (RFC 1918) and MAC addresses.

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

BUILT_IN = [
    r"\b(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    r"\b192\.168\.\d{1,3}\.\d{1,3}\b",
    r"\b172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}\b",
    r"\b[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}\b",
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
    pats = [re.escape(n) for n in derived_names()]
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
    """[(line number, matched text)] for every private name in text."""
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for p in pats:
            hits += [(n, m.group(0)) for m in p.finditer(line)]
    return hits


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def report(where, hits):
    for n, m in hits:
        # Show where, not the whole line: the line itself may be the leak.
        print(f"{where}:{n}: private name '{m}'", file=sys.stderr)
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


def main():
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
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
