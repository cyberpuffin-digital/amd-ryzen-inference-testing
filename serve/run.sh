#!/usr/bin/env bash
# Serve the recommended models from one llama.cpp router: an OpenAI-compatible
# API and web UI where the model is picked by name, loaded on demand, and the
# previous one unloaded (one in memory at a time).
#
#   serve/run.sh                 # http://127.0.0.1:8080, presets from serve/780m-presets.ini.in
#
#   LLAMA_BIN=<dir>   llama.cpp build (default ~/.local/opt/llama.cpp/current/bin)
#   MODELS_DIR=<dir>  where models/fetch.sh put the models (default ~/models)
#   PRESETS=<file>    another preset template (@MODELS_DIR@ is filled in)
#   HOST, PORT        listen address (default 127.0.0.1:8080)
#
# Pick a model with "model": "gemma-4-26b-a4b" (or qwen3-30b-a3b,
# gemma-4-e4b) in a request, or from the model menu in the web UI.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
LLAMA_BIN=${LLAMA_BIN:-$HOME/.local/opt/llama.cpp/current/bin}
MODELS_DIR=${MODELS_DIR:-$HOME/models}
PRESETS=${PRESETS:-$here/780m-presets.ini.in}
HOST=${HOST:-127.0.0.1}
PORT=${PORT:-8080}

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

exec "$LLAMA_BIN/llama" serve --models-preset "$rendered" --models-max 1 \
    --host "$HOST" --port "$PORT"
