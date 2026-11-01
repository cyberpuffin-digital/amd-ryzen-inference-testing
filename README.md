# amd-ryzen-inference-testing

## TL;DR: what to run on a Radeon 780M

Three picks, from the [first baseline](analysis/2026-10-31-fw13-7840u-baseline.md)
(Framework Laptop 13, Ryzen 7 7840U, 32 GB; upstream llama.cpp build 12020, Vulkan):

| Pick | Model | File | Generation | Prompt | GPU memory (GTT) it needs |
|---|---|--:|--:|--:|---|
| **Default** | Gemma 4 26B-A4B, Q4_0, with its MTP draft head | 14.6 GB | **~41 t/s** (25 without MTP) | ~490 t/s | ~17 GiB: raise GTT (below) |
| **Largest** | Qwen3-30B-A3B-Instruct-2507, UD-Q4_K_XL | 17.7 GB | **~36 t/s** | ~440 t/s | ~20 GiB: raise GTT (below) |
| **Small and fast** | Gemma 4 E4B, Q4_0, with its MTP draft head | 4.6 GB | **~58 t/s** (24 without MTP) | ~610 t/s | fits the default |

The first two are mixture-of-experts models: each token reads only a few
billion parameters, so they generate faster than a dense 8B model while
holding far more knowledge. Picks are by speed at each size; this repository
doesn't measure answer quality, so try them on your own tasks.

**Settings** (all three; the reasons are in the baseline write-up):

```
llama serve -m <model> -dev Vulkan0 -ngl 99 -fa on -ctk q8_0 -ctv q8_0 -ub 256 -c 16384 -np 1 --jinja
# Gemma 4 only, the MTP draft head:  -md mtp-<model>.gguf --spec-type draft-mtp -ngld 99 -devd Vulkan0
```

- **Use an upstream llama.cpp build.** Distro packages lag: against Ubuntu's
  8681, upstream read prompts 28-41% faster, and 8681 can't load Gemma 4 E4B
  or use MTP.
- **Raise GTT** (the GPU's share of RAM, half by default) for the two large
  models: add `ttm.pages_limit=6291456` (24 GiB) to the kernel command line
  and reboot. Near-full GTT froze an older kernel; see
  [hardware/780m.md](hardware/780m.md).
- **Don't add a draft model to Qwen3-30B-A3B**: drafting made it slower (0.75x).
- **Gemma 4 thinks before answering.** Give it room (`max_tokens` in the
  hundreds), or switch it off with `--reasoning off`.

**Switch between all three from one server**, loading each on demand
([serve/](serve/)):

```bash
bench/build-llama-cpp.sh                                   # upstream llama.cpp with Vulkan
grep -E '^#|26B-A4B|E4B-it|30B-A3B' models/780m-32gb.tsv > /tmp/picks.tsv
models/fetch.sh ~/models /tmp/picks.tsv                    # the three picks, ~39 GB
serve/run.sh                                               # http://127.0.0.1:8080
```

Then pick `gemma-4-26b-a4b`, `qwen3-30b-a3b` or `gemma-4-e4b` in the web UI's
model menu, or as `"model"` in any OpenAI-compatible client; embeddings are
`nomic-embed-text` on `/v1/embeddings`. Two models stay loaded at most (a chat
model and the embedder): the router unloads the least recently used one when a
new model would leave under 2 GiB of GPU memory free, so the two large chat
models are never loaded together. Switching chat models takes 10-20 seconds.
`LISTEN_DOCKER=1 serve/run.sh` also listens on the Docker bridge gateway, for
containers on the same machine (`host.docker.internal`), without exposing the
router on the LAN; a host firewall must still admit the port from Docker
networks.

Speeds are from one run of each test. MTP gains were measured on a code prompt
at temperature 0; in a chat test through the server, Gemma 4 E4B with MTP
generated 49-54 t/s.

## About

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
- **Results:** [results/](results/). First baseline, distro vs upstream llama.cpp on nine models: [analysis/2026-10-31-fw13-7840u-baseline.md](analysis/2026-10-31-fw13-7840u-baseline.md).

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
bench/      build-llama-cpp.sh, run.sh, capture-env.sh, report.py, redact.py
analysis/   compare.py (runs side by side) and write-ups of what the results show
.githooks/  pre-commit, commit-msg, pre-push: refuse private names (bench/redact.py)
.forgejo/   CI: the same check on every push and pull request
models/     pinned model sets (*.tsv), fetch.sh, hf-manifest.py
hardware/   per-hardware notes: settings, gotchas, open questions
results/    one directory per run; raw files are never edited
docs/       background and decisions
```

## Privacy

Results identify hardware by a label you choose, not by hostname. The capture
reads no serial numbers, UUIDs, MAC or IP addresses, hostnames or usernames.

As a second layer, everything a run writes passes through
`bench/redact.py filter`: home-directory paths become `~`, and private names
become `[redacted]`. What counts as private is never listed in this
repository, since that list would publish it. It is derived from your machine
(hostname, DNS search domains, username), plus a local file for anything else,
such as internal domains or other hosts: copy
[`bench/redact.example.txt`](bench/redact.example.txt) to
`~/.config/amd-ryzen-inference-testing/redact.txt`. All IPv4 and IPv6 addresses
(private, CGNAT and public; loopback excepted) and MAC addresses are built in. `bench/redact.py patterns` shows what is in use.

The same patterns guard commits. Enable the hooks once per clone:

```bash
git config core.hooksPath .githooks
```

They refuse a commit whose files, author or message contain a private name,
and a push whose commits do, on every remote. CI runs the same check on every
push and pull request (`.forgejo/workflows/sanitize.yaml`), with the private
list held as a repository secret and matches reported by pattern number only.
Read a results directory before you commit it anyway.

## Contributing

Runs from other Ryzen APUs are very welcome, especially other Phoenix/Hawk
Point machines, Strix Point, and anything with a different memory
configuration. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Code (`bench/`, `models/*.sh`, `models/*.py`) is [MIT](LICENSE). Results,
model sets and documentation are [CC BY 4.0](LICENSE-DATA).
