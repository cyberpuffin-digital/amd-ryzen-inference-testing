#!/usr/bin/env bash
# Build upstream llama.cpp with the Vulkan backend and install it beside any
# distro package, one directory per commit.
#
#   bench/build-llama-cpp.sh             # latest master
#   REF=<commit or tag> bench/build-llama-cpp.sh
#
#   SRC=<dir>     clone location (default ~/src/llama.cpp)
#   PREFIX=<dir>  install root (default ~/.local/opt/llama.cpp)
#
# Installs to $PREFIX/<short sha> and points $PREFIX/current at it, so the
# previous build is one `ln -sfn <sha> $PREFIX/current` away. Benchmark a
# build with LLAMA_BIN=$PREFIX/current/bin bench/run.sh <label>.
#
# Debian/Ubuntu build dependencies:
#   sudo apt install build-essential cmake git libssl-dev libvulkan-dev glslc spirv-headers
set -euo pipefail

SRC=${SRC:-$HOME/src/llama.cpp}
PREFIX=${PREFIX:-$HOME/.local/opt/llama.cpp}
REF=${REF:-}

missing=()
for p in build-essential cmake git libssl-dev libvulkan-dev glslc spirv-headers; do
    dpkg -s "$p" >/dev/null 2>&1 || missing+=("$p")
done
if ((${#missing[@]})) && command -v dpkg >/dev/null; then
    echo "missing build dependencies: sudo apt install ${missing[*]}" >&2
    exit 1
fi

if [[ ! -d $SRC/.git ]]; then
    git clone https://github.com/ggml-org/llama.cpp "$SRC"
fi
git -C "$SRC" fetch --tags origin
if [[ -n $REF ]]; then
    git -C "$SRC" checkout --detach "$REF"
else
    git -C "$SRC" checkout --detach origin/master
fi
sha=$(git -C "$SRC" rev-parse --short HEAD)
dest=$PREFIX/$sha

cmake -S "$SRC" -B "$SRC/build-vulkan" -DCMAKE_BUILD_TYPE=Release \
    -DGGML_VULKAN=ON -DGGML_NATIVE=ON -DBUILD_SHARED_LIBS=OFF -DLLAMA_BUILD_TESTS=OFF \
    -DCMAKE_INSTALL_PREFIX="$dest"
cmake --build "$SRC/build-vulkan" -j"$(nproc)"
cmake --install "$SRC/build-vulkan"
ln -sfn "$sha" "$PREFIX/current"

# Newer builds install one `llama` binary with subcommands; older ones,
# llama-cli and friends.
if [[ -x $dest/bin/llama ]]; then
    "$dest/bin/llama" version
    "$dest/bin/llama" cli --list-devices
else
    "$dest/bin/llama-cli" --version
    "$dest/bin/llama-cli" --list-devices
fi
echo "installed $dest; $PREFIX/current -> $sha"
