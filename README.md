# amd-ryzen-inference

Reproducible measurements of local LLM inference on AMD Ryzen APUs: the CPU,
the integrated Radeon GPU and, where it can be used, the NPU, all sharing one
pool of system memory.

Most published AMD numbers are for Strix Halo or discrete Radeon cards. This
repository starts with the older and far more common **Radeon 780M**
(Ryzen 7040 "Phoenix" / 8040 "Hawk Point"), found in many laptops and mini
PCs, to find out what it can usefully run, and how to get the most from it.

Every result records the hardware, firmware settings, kernel, Mesa and
llama.cpp versions, power state, the exact model file (pinned by Hugging Face
commit and SHA-256), the command and the raw output, so anyone with the same
hardware can repeat it.

## Status

- **Hardware so far:** Radeon 780M (Framework Laptop 13, Ryzen 7 7840U, 32 GB). Notes: [hardware/780m.md](hardware/780m.md).
- **Engine:** llama.cpp with the Vulkan (RADV) backend, comparing a distro package with an upstream build. Why this engine: [docs/engine-choice.md](docs/engine-choice.md).
- **Results:** [results/](results/). The first full baseline run is in progress.

## Reproduce a run

```bash
# 1. Build dependencies (Debian/Ubuntu), then upstream llama.cpp with Vulkan
sudo apt install build-essential cmake git jq libssl-dev libvulkan-dev glslc spirv-headers mesa-vulkan-drivers
bench/build-llama-cpp.sh                 # -> ~/.local/opt/llama.cpp/<sha>, `current` points at it

# 2. Models, pinned by commit and checksum (~64 GB; resumable)
models/fetch.sh ~/models models/780m-32gb.tsv

# 3. Benchmark: idle, on AC, performance power profile, browser closed
powerprofilesctl set performance
LLAMA_BIN=~/.local/opt/llama.cpp/current/bin bench/run.sh <label>    # label names the hardware, e.g. fw13-7840u
```

`bench/run.sh` writes `results/<date>_<label>_<build>/` with `env.json`,
`llama-bench.jsonl`, `spec.jsonl` and a generated `report.md`. It warns (and
records the warning) when conditions would skew the numbers: on battery, not in
the performance profile, system busy, a browser running, a download running.
`QUICK=1` runs only the GPU-vs-CPU comparison.

What it measures for each model:
- GPU (Vulkan) against CPU (8 threads), prompt processing and generation
- prompt processing and generation as the context fills: 0, 8k and 16k tokens
- tuning at 8k: micro-batch 256/512, flash attention on/off, KV cache f16/q8_0
- speculative decoding through the llama.cpp server: small draft models, and MTP/EAGLE3 draft heads where the build supports them

## Keeping models current

Upstream repositories re-upload GGUF files (template fixes, better quants).
`models/hf-manifest.py check models/780m-32gb.tsv` reports which pinned files
changed; `update` re-pins them, and `models/fetch.sh` then downloads only what
changed. A repository that changed only its README is re-pinned without a
download.

## Layout

```
bench/      build-llama-cpp.sh, run.sh, capture-env.sh, report.py
models/     pinned model sets (*.tsv), fetch.sh, hf-manifest.py
hardware/   per-hardware notes: settings, gotchas, open questions
results/    one directory per run; raw files are never edited
docs/       background and decisions
```

## Privacy

Results identify hardware by a label you choose, not by hostname. The capture
reads no serial numbers, UUIDs, MAC or IP addresses, hostnames or usernames,
and home-directory paths are rewritten to `~` before anything is written.
Check a results directory before you commit it anyway.

## Contributing

Runs from other Ryzen APUs are very welcome, especially other Phoenix/Hawk
Point machines, Strix Point, and anything with a different memory
configuration. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Code (`bench/`, `models/*.sh`, `models/*.py`) is [MIT](LICENSE). Results,
model sets and documentation are [CC BY 4.0](LICENSE-DATA).
