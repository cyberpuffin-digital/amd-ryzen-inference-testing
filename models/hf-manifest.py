#!/usr/bin/env python3
"""Keep a Hugging Face model manifest (models/*.tsv) pinned and current.

The manifest is what models/fetch.sh downloads: one row per file,

    repo <TAB> revision <TAB> path <TAB> bytes <TAB> sha256 (LFS oid; - for small non-LFS files)

and this tool writes and refreshes those rows from the Hugging Face API, so
no pin is copied by hand:

    hf-manifest.py add    MANIFEST REPO PATH [PATH ...]   # append rows pinned at the repo's current main
    hf-manifest.py check  MANIFEST                        # report what changed upstream; exit 1 if anything did
    hf-manifest.py update MANIFEST [--repo REPO]          # re-pin rows to the repo's current main
    hf-manifest.py --self-test                            # check the logic offline (no network)

"Changed" means the FILE changed: its LFS oid (sha256) or size differs at the
repo's current main. A repo whose main moved only for a README edit is
reported as "moved" and re-pinned by `update`, but nothing is re-downloaded,
because models/fetch.sh keeps a file whose size and recorded sha256 still match.
A file deleted upstream is reported and left pinned at its old revision,
which Hugging Face keeps serving.

Public repos only; no token is read or sent.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

API = "https://huggingface.co/api/models"
HEADER = "# repo\trevision\tpath\tbytes\tsha256 (LFS oid; - for small non-LFS files)"


def get_json(url):
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.load(resp)


def head_sha(repo):
    return get_json(f"{API}/{repo}/revision/main")["sha"]


def tree(repo, rev):
    """{path: (bytes, sha256 or '-')} for every file at rev."""
    url = f"{API}/{repo}/tree/{urllib.parse.quote(rev)}?recursive=true"
    files = {}
    for entry in get_json(url):
        if entry.get("type") != "file":
            continue
        lfs = entry.get("lfs")
        files[entry["path"]] = (entry["size"], lfs["oid"] if lfs else "-")
    return files


def read_manifest(path):
    """(lines, rows): lines keeps comments and blanks in place; rows indexes the data lines."""
    with open(path) as f:
        lines = f.read().splitlines()
    rows = []
    for i, line in enumerate(lines):
        if not line.strip() or line.startswith("#"):
            continue
        repo, rev, fpath, size, sha = line.split("\t")
        rows.append({"line": i, "repo": repo, "rev": rev, "path": fpath, "bytes": int(size), "sha": sha})
    return lines, rows


def format_row(r):
    return f"{r['repo']}\t{r['rev']}\t{r['path']}\t{r['bytes']}\t{r['sha']}"


def plan(rows, heads, trees):
    """Compare each row with its repo's current main. Pure: no network.

    heads: {repo: sha}; trees: {repo: {path: (bytes, sha)}} at that sha.
    Returns a list of (row, status, new_row) where status is one of
    current, moved, changed, gone.
    """
    out = []
    for r in rows:
        head = heads[r["repo"]]
        if r["rev"] == head:
            out.append((r, "current", r))
            continue
        upstream = trees[r["repo"]].get(r["path"])
        if upstream is None:
            out.append((r, "gone", r))
            continue
        new = dict(r, rev=head, bytes=upstream[0], sha=upstream[1])
        same = (upstream[0], upstream[1]) == (r["bytes"], r["sha"])
        out.append((r, "moved" if same else "changed", new))
    return out


def fetch_upstream(rows):
    heads, trees = {}, {}
    for repo in sorted({r["repo"] for r in rows}):
        heads[repo] = head_sha(repo)
        trees[repo] = tree(repo, heads[repo])
    return heads, trees


def cmd_add(args):
    try:
        lines, rows = read_manifest(args.manifest)
    except FileNotFoundError:
        lines, rows = [HEADER], []
    have = {(r["repo"], r["path"]) for r in rows}
    head = head_sha(args.repo)
    files = tree(args.repo, head)
    for p in args.paths:
        if (args.repo, p) in have:
            print(f"skip  {args.repo}/{p} (already in the manifest)")
            continue
        if p not in files:
            sys.exit(f"error: {args.repo} has no {p} at main ({head[:12]})")
        size, sha = files[p]
        lines.append(format_row({"repo": args.repo, "rev": head, "path": p, "bytes": size, "sha": sha}))
        print(f"add   {args.repo}/{p} ({size / 1e9:.1f} GB) @ {head[:12]}")
    with open(args.manifest, "w") as f:
        f.write("\n".join(lines) + "\n")


def cmd_check(args, write=False):
    lines, rows = read_manifest(args.manifest)
    if args.repo:
        rows = [r for r in rows if r["repo"] == args.repo]
    heads, trees = fetch_upstream(rows)
    changed = 0
    for old, status, new in plan(rows, heads, trees):
        name = f"{old['repo']}/{old['path']}"
        if status == "changed":
            changed += 1
            print(f"CHANGED {name}: {old['rev'][:12]} -> {new['rev'][:12]}, "
                  f"{old['bytes'] / 1e9:.2f} -> {new['bytes'] / 1e9:.2f} GB")
        elif status == "gone":
            print(f"GONE    {name}: not at main any more; stays pinned at {old['rev'][:12]}")
        elif status == "moved":
            print(f"moved   {name}: repo at {new['rev'][:12]}, file unchanged")
        if write and status in ("changed", "moved"):
            lines[old["line"]] = format_row(new)
    if write:
        with open(args.manifest, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"{args.manifest}: {changed} file(s) re-pinned to new content; fetch to download them")
        return 0
    print(f"{changed} file(s) changed upstream" if changed else "all files current")
    return 1 if changed else 0


def self_test():
    rows = [
        {"line": 1, "repo": "a/x", "rev": "r1", "path": "m.gguf", "bytes": 10, "sha": "s1"},
        {"line": 2, "repo": "a/x", "rev": "r1", "path": "draft.gguf", "bytes": 5, "sha": "s2"},
        {"line": 3, "repo": "b/y", "rev": "h2", "path": "n.gguf", "bytes": 7, "sha": "s3"},
        {"line": 4, "repo": "a/x", "rev": "r1", "path": "old.gguf", "bytes": 3, "sha": "s4"},
    ]
    heads = {"a/x": "h1", "b/y": "h2"}
    trees = {"a/x": {"m.gguf": (11, "s1b"), "draft.gguf": (5, "s2")}, "b/y": {"n.gguf": (7, "s3")}}
    got = {(o["path"], s): n for o, s, n in plan(rows, heads, trees)}
    assert ("m.gguf", "changed") in got, got
    assert got[("m.gguf", "changed")] == dict(rows[0], rev="h1", bytes=11, sha="s1b")
    assert ("draft.gguf", "moved") in got and got[("draft.gguf", "moved")]["rev"] == "h1"
    assert ("n.gguf", "current") in got
    assert ("old.gguf", "gone") in got and got[("old.gguf", "gone")]["rev"] == "r1"
    assert format_row(rows[0]) == "a/x\tr1\tm.gguf\t10\ts1"
    print("self-test ok")


def main():
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return 0
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("manifest")
    a.add_argument("repo")
    a.add_argument("paths", nargs="+")
    for name in ("check", "update"):
        c = sub.add_parser(name)
        c.add_argument("manifest")
        c.add_argument("--repo", help="only this repo")
    args = p.parse_args()
    if args.cmd == "add":
        cmd_add(args)
        return 0
    return cmd_check(args, write=args.cmd == "update")


if __name__ == "__main__":
    sys.exit(main())
