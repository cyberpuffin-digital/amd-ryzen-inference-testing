# Results

One directory per run: `<date>_<hardware label>_<llama.cpp build>`. Each holds
`env.json` (hardware, versions, power state), `llama-bench.jsonl`, `spec.jsonl`
and a generated `report.md`. Raw files are never edited after a run.

| Run | Hardware | llama.cpp | Notes |
|---|---|---|---|
| [2026-10-31_fw13-7840u_b8681-distro](2026-10-31_fw13-7840u_b8681-distro/report.md) | Framework 13, Ryzen 7 7840U, Radeon 780M, 32 GB (GTT 24 GiB) | 8681 (Ubuntu package) | Baseline. Gemma 4 E2B/E4B fail to load (missing tensor). |
| [2026-10-31_fw13-7840u_b12020](2026-10-31_fw13-7840u_b12020/report.md) | same | 12020 (upstream, `0ec4027a2`) | Baseline. Comparison and findings: [analysis/2026-10-31-fw13-7840u-baseline.md](../analysis/2026-10-31-fw13-7840u-baseline.md) |
