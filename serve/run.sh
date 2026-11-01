#!/usr/bin/env bash
# Serve the recommended models from one llama.cpp router: an OpenAI-compatible
# API and web UI where the model is picked by name and loaded on demand. Up to
# two models stay loaded (a chat model plus the small embedding model); the
# router unloads the least recently used one whenever a new model would leave
# less than MEMORY_MARGIN_MIB of GPU memory free, so two large chat models are
# never resident together.
#
#   serve/run.sh                 # http://127.0.0.1:8080, presets from serve/780m-presets.ini.in
#
#   LLAMA_BIN=<dir>   llama.cpp build (default ~/.local/opt/llama.cpp/current/bin)
#   MODELS_DIR=<dir>  where models/fetch.sh put the models (default ~/models)
#   PRESETS=<file>    another preset template (@MODELS_DIR@ is filled in)
#   HOST, PORT        listen address (default 127.0.0.1:8080); HOST may be a comma list
#   LISTEN_DOCKER=1   also listen on the Docker bridge gateway (docker0), so
#                     containers reach the router as host.docker.internal
#                     without it being exposed on the LAN
#   MODELS_MAX        models loaded at once (default 2)
#   MEMORY_MARGIN_MIB GPU memory to keep free when loading (default 2048)
#
# Pick a model with "model": "gemma-4-26b-a4b" (or qwen3-30b-a3b,
# gemma-4-e4b) in a request, or from the model menu in the web UI. Embeddings:
# "model": "nomic-embed-text" on /v1/embeddings.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
LLAMA_BIN=${LLAMA_BIN:-$HOME/.local/opt/llama.cpp/current/bin}
MODELS_DIR=${MODELS_DIR:-$HOME/models}
PRESETS=${PRESETS:-$here/780m-presets.ini.in}
HOST=${HOST:-127.0.0.1}
PORT=${PORT:-8080}
MODELS_MAX=${MODELS_MAX:-2}
MEMORY_MARGIN_MIB=${MEMORY_MARGIN_MIB:-2048}

if [[ ${LISTEN_DOCKER:-0} == 1 ]]; then
    gw=$(ip -4 -o addr show docker0 2>/dev/null | awk '{sub("/.*", "", $4); print $4}')
    if [[ -n $gw ]]; then
        HOST=$HOST,$gw
    else
        echo "warning: LISTEN_DOCKER=1 but there is no docker0 interface; listening on $HOST only" >&2
    fi
fi

if [[ ! -x $LLAMA_BIN/llama ]]; then
    echo "error: no upstream llama.cpp at $LLAMA_BIN (bench/build-llama-cpp.sh builds one;" >&2
    echo "  router mode, --spec-type and Gemma 4 E-series need it)" >&2
    exit 1
fi

# Presets need absolute paths; render the template, and refuse to start with
# a preset whose model file is missing rather than fail at first request.
rendered=${XDG_CONFIG_HOME:-$HOME/.config}/amd-ryzen-inference-testing/presets.ini
mkdir -p "$(dirname "$rendered")"
sed "s#@MODELS_DIR@#$MODELS_DIR#g" "$PRESETS" >"$rendered"
missing=0
while read -r path; do
    [[ -f $path ]] || { echo "missing model file: $path (models/fetch.sh)" >&2; missing=1; }
done < <(sed -n -E 's/^(model|spec-draft-model|mmproj) *= *//p' "$rendered")
((missing == 0)) || exit 1

exec "$LLAMA_BIN/llama" serve --models-preset "$rendered" \
    --models-max "$MODELS_MAX" --models-memory-margin "$MEMORY_MARGIN_MIB" \
    --host "$HOST" --port "$PORT"
