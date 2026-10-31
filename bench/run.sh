#!/usr/bin/env bash
# Benchmark GGUF models with llama.cpp on an AMD Ryzen APU, and record the
# raw results with everything needed to reproduce them.
#
#   bench/run.sh <label> [model.gguf ...]        # default: every model under $MODELS_DIR
#
#   LLAMA_BIN=<dir>   llama.cpp build to test (default: llama-bench etc. on PATH).
#                     Upstream builds install one `llama` binary with
#                     subcommands; older and distro builds install llama-bench,
#                     llama-server and llama-cli. Both work.
#   MODELS_DIR=<dir>  where to look for models (default ~/models)
#   QUICK=1           GPU vs CPU only: no depth sweep, tuning grid or speculation
#   SPEC=0            skip the speculative-decoding pairs
#   REPS=<n>          llama-bench repetitions (default 3)
#
# <label> names the hardware, e.g. fw13-7840u; it replaces the hostname.
# Writes results/<date>_<label>_<build>/:
#   env.json          bench/capture-env.sh: hardware, versions, power state
#   llama-bench.jsonl one llama-bench row per line, plus "section"
#   spec.jsonl        speculative-decoding runs through the llama.cpp server
#   report.md         generated from the above by bench/report.py
# Everything written passes through bench/redact.py filter: home paths become
# ~, and private names (hostname, search domains, username, your local
# redact.txt, private IPs and MACs) become [redacted].
#
# Long-context runs use -ub 256: on the 780M, the default 512 with a 2048-token
# prompt on 16k of context ran one GPU dispatch past amdgpu's compute timeout
# (vk::DeviceLostError). See hardware/780m.md.
set -uo pipefail

label=${1:?usage: bench/run.sh <label> [model.gguf ...]}
shift
here=$(cd "$(dirname "$0")" && pwd)
repo=$(dirname "$here")
MODELS_DIR=${MODELS_DIR:-$HOME/models}
REPS=${REPS:-3}
QUICK=${QUICK:-0}
SPEC=${SPEC:-1}
PORT=${PORT:-8099}

# Speculative-decoding pairs (target:draft:type, by file name), run when both
# files are present. draft-simple is a separate small model, which must share
# its target's vocabulary; draft-mtp and draft-eagle3 are draft heads trained
# for one model. Builds without --spec-type (llama.cpp before it was added,
# e.g. distro 8681) run draft-simple pairs only.
SPEC_PAIRS=(
    "Qwen3-4B-Q4_K_M.gguf:Qwen3-0.6B-Q8_0.gguf:draft-simple"
    "Qwen3-8B-Q4_K_M.gguf:Qwen3-0.6B-Q8_0.gguf:draft-simple"
    "Qwen3-8B-Q4_K_M.gguf:Qwen3-1.7B-Q8_0.gguf:draft-simple"
    "Qwen3-30B-A3B-Instruct-2507-UD-Q4_K_XL.gguf:Qwen3-0.6B-Q8_0.gguf:draft-simple"
    "gemma-4-E4B-it-Q4_0.gguf:mtp-gemma-4-E4B-it-Q4_0.gguf:draft-mtp"
    "gemma-4-26B-A4B-it-Q4_0.gguf:mtp-gemma-4-26B-A4B-it-Q4_0.gguf:draft-mtp"
    "gpt-oss-20b-MXFP4.gguf:eagle3-gpt-oss-20b-Q8_0.gguf:draft-eagle3"
)

# --- Which llama.cpp.
bin=${LLAMA_BIN:-}
if [[ -n $bin && -x $bin/llama ]]; then
    BENCH=("$bin/llama" bench) SERVER=("$bin/llama" serve) VERSION=("$bin/llama" version)
else
    p=${bin:+$bin/}
    BENCH=("${p}llama-bench") SERVER=("${p}llama-server") VERSION=("${p}llama-cli" --version)
fi
version=$("${VERSION[@]}" 2>&1 | grep -m1 version)
build=$(grep -o -E 'build [0-9]+' <<<"$version" | tr -d ' ' | sed 's/build/b/')
[[ -n $build ]] || build="b$(grep -o -E '[0-9]+' <<<"$version" | head -1)-distro"

out="$repo/results/$(date +%Y-%m-%d)_${label}_${build}"
mkdir -p "$out"
sanitize() { python3 "$here/redact.py" filter; }

# --- Models: projectors and built-in draft heads can't be benchmarked alone.
if (($#)); then
    models=("$@")
else
    mapfile -t models < <(find "$MODELS_DIR" -name '*.gguf' -size +100M \
        ! -name 'mmproj-*' ! -name 'mtp-*' ! -name 'eagle3-*' | sort)
fi
((${#models[@]})) || { echo "no .gguf files under $MODELS_DIR" >&2; exit 1; }

# --- Environment, and warnings about conditions that skew results.
"$here/capture-env.sh" "$label" "${bin:-}" | sanitize >"$out/env.json"
warnings=()
jq -e '.power.ac_online' "$out/env.json" >/dev/null || warnings+=("on battery")
jq -e '.power.platform_profile == "performance"' "$out/env.json" >/dev/null || warnings+=("power profile is not performance")
jq -e '.load_average_1m <= 1.0' "$out/env.json" >/dev/null || warnings+=("system busy (load average > 1)")
pgrep -x 'firefox|chrome|chromium|code|steam' >/dev/null && warnings+=("browser, editor or game running")
pgrep -x 'rsync|curl' >/dev/null && warnings+=("download running")
to_json_list() { printf '%s\n' "$@" | jq -R . | jq -s 'map(select(length > 0))'; }
jq --argjson w "$(to_json_list "${warnings[@]}")" --argjson m "$(to_json_list "${models[@]}")" \
    '. + {warnings: $w, models: $m}' "$out/env.json" | sanitize >"$out/env.json.tmp" &&
    mv "$out/env.json.tmp" "$out/env.json"
for w in "${warnings[@]}"; do echo "warning: $w" >&2; done
echo "results: $out" >&2

bench() {
    # One llama-bench call; each JSON row gets the section name. A model that
    # fails to load is logged to errors.log and the run continues.
    local section=$1 rows
    shift
    echo "[$section] $*" >&2
    rows=$("${BENCH[@]}" -o jsonl -r "$REPS" "$@" 2> >(sanitize >>"$out/stderr.log"))
    if [[ -n $rows ]]; then
        jq -c --arg s "$section" '. + {section: $s}' <<<"$rows" | sanitize >>"$out/llama-bench.jsonl"
    else
        echo "[$section] failed: $*" | sanitize >>"$out/errors.log"
    fi
}

server_run() {
    # Start the server with the given flags, send one fixed completion at
    # temperature 0, print its timings as JSON.
    local log pid resp
    log=$(mktemp)
    "${SERVER[@]}" --port "$PORT" -dev Vulkan0 -ngl 99 -fa on -c 4096 "$@" >"$log" 2>&1 &
    pid=$!
    for _ in $(seq 180); do
        curl -sf "localhost:$PORT/health" >/dev/null && break
        kill -0 $pid 2>/dev/null || break
        sleep 1
    done
    resp=$(curl -sf "localhost:$PORT/completion" -H 'Content-Type: application/json' -d '{
        "prompt": "Write a Python function that parses an ISO 8601 date string and returns a datetime, with docstring and three doctests.\n\n```python\n",
        "n_predict": 256, "temperature": 0, "cache_prompt": false}')
    kill $pid 2>/dev/null
    wait $pid 2>/dev/null
    if [[ -n $resp ]]; then
        jq -c '.timings'
    else
        grep -m1 -i -E 'error|failed' "$log" | sanitize >>"$out/errors.log"
        echo null
    fi <<<"$resp"
    rm -f "$log"
}

for m in "${models[@]}"; do
    bench gpu-vs-cpu -m "$m" -dev Vulkan0 -ngl 99 -fa 1 -p 512 -n 128
    bench gpu-vs-cpu -m "$m" -dev none -ngl 0 -t 8 -p 512 -n 128
    ((QUICK)) && continue
    bench depth -m "$m" -dev Vulkan0 -ngl 99 -fa 1 -ub 256 -p 2048 -n 64 -d 0,8192,16384
    bench tuning -m "$m" -dev Vulkan0 -ngl 99 -ub 256,512 -fa 0,1 -p 2048 -n 64 -d 8192
    bench kv-type -m "$m" -dev Vulkan0 -ngl 99 -ub 256 -fa 1 -ctk f16,q8_0 -ctv f16,q8_0 -p 2048 -n 64 -d 8192
done

if ((SPEC && !QUICK)); then
    # Upstream made speculation opt-in with --spec-type (default none): without
    # it, a draft model is loaded and silently never used.
    has_spec_type=0
    "${SERVER[@]}" --help 2>&1 | grep -q -- '--spec-type' && has_spec_type=1
    for pair in "${SPEC_PAIRS[@]}"; do
        IFS=: read -r tname dname type <<<"$pair"
        t=$(find "$MODELS_DIR" -name "$tname" -print -quit)
        d=$(find "$MODELS_DIR" -name "$dname" -print -quit)
        [[ -n $t && -n $d ]] || continue
        type_flag=()
        if ((has_spec_type)); then
            type_flag=(--spec-type "$type")
        elif [[ $type != draft-simple ]]; then
            continue
        fi
        echo "[speculative] $tname + $dname ($type)" >&2
        base=$(server_run -m "$t")
        spec=$(server_run -m "$t" -md "$d" -ngld 99 -devd Vulkan0 "${type_flag[@]}")
        jq -n -c --arg t "$tname" --arg d "$dname" --arg type "$type" \
            --argjson base "$base" --argjson spec "$spec" \
            '{target: $t, draft: $d, type: $type, alone: $base, with_draft: $spec}' >>"$out/spec.jsonl"
    done
fi

python3 "$here/report.py" "$out"
echo "report: $out/report.md" >&2
