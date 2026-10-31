#!/usr/bin/env bash
# Fetch every file in a Hugging Face model manifest at its pinned revision.
#
#   models/fetch.sh [dest=~/models] [manifest=models/780m-32gb.tsv]
#   VERIFY_EXISTING=1 models/fetch.sh   # also hash files already present
#
# Layout: <dest>/<org>/<repo>/<path>. Public repos, no token.
#
# Each download goes to <file>.partial (resumable with curl -C -), and is
# renamed into place only after its size and, for LFS files, its SHA-256 match
# the manifest; a <file>.sha256 sidecar records what was verified. A file is
# re-fetched when its sidecar disagrees with the manifest, which is what
# `models/hf-manifest.py update` causes when upstream re-uploads a file.
# Exits non-zero if any file is missing or bad.
set -u
dest=${1:-$HOME/models}
manifest=${2:-$(dirname "$0")/780m-32gb.tsv}
mkdir -p "$dest"
log="$dest/fetch.log"
if ! mountpoint -q "$(df --output=target "$dest" 2>/dev/null | tail -1)"; then
  echo "error: $dest is not on a mounted filesystem" >&2; exit 2
fi
say() { echo "$(date '+%F %T') $*" | tee -a "$log"; }

fails=0
while IFS=$'\t' read -r repo rev path bytes sha; do
  case "$repo" in ''|'#'*) continue ;; esac
  out="$dest/$repo/$path"
  mkdir -p "$(dirname "$out")"
  # A verified download leaves <file>.sha256 beside it. When that disagrees
  # with the manifest, `hf-manifest.py update` re-pinned the file to new
  # content, possibly of the same size, so it is fetched again. Files without
  # one keep the size-only rule.
  if [ -f "$out" ] && [ "$sha" != - ] && [ -f "$out.sha256" ] && [ "$(cat "$out.sha256")" != "$sha" ]; then
    say "stale $repo/$path (re-pinned upstream; replacing)"
  elif [ -f "$out" ] && [ "$(stat -c %s "$out")" = "$bytes" ]; then
    if [ "${VERIFY_EXISTING:-0}" = 1 ] && [ "$sha" != - ]; then
      got=$(sha256sum "$out" | cut -d' ' -f1)
      if [ "$got" != "$sha" ]; then say "BAD   $repo/$path (sha256 mismatch on existing file)"; fails=$((fails+1)); else echo "$sha" > "$out.sha256"; say "ok    $repo/$path (verified)"; fi
    fi
    continue
  fi
  # A .partial already at full size was downloaded but not yet verified (the
  # run was stopped mid-hash, e.g. for a reboot): resuming it would ask for a
  # range past the end, which the server answers with 416. Verify it instead.
  if [ -f "$out.partial" ] && [ "$(stat -c %s "$out.partial")" = "$bytes" ]; then
    say "verify $repo/$path (complete .partial from an earlier run)"
  else
    say "start $repo/$path ($((bytes / 1048576)) MiB)"
    if ! curl -fsSL --retry 5 --retry-delay 10 -C - -o "$out.partial" \
          "https://huggingface.co/$repo/resolve/$rev/$path"; then
      say "FAIL  $repo/$path (curl)"; fails=$((fails+1)); continue
    fi
  fi
  if [ "$(stat -c %s "$out.partial")" != "$bytes" ]; then
    say "FAIL  $repo/$path (size $(stat -c %s "$out.partial") != $bytes)"; fails=$((fails+1)); continue
  fi
  if [ "$sha" != - ] && [ "$(sha256sum "$out.partial" | cut -d' ' -f1)" != "$sha" ]; then
    say "FAIL  $repo/$path (sha256 mismatch; .partial kept for inspection)"; fails=$((fails+1)); continue
  fi
  mv "$out.partial" "$out"
  [ "$sha" != - ] && echo "$sha" > "$out.sha256"
  say "done  $repo/$path"
done < "$manifest"

if [ "$fails" -gt 0 ]; then say "finished with $fails failure(s)"; exit 1; fi
say "all present"
