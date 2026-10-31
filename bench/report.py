#!/usr/bin/env python3
"""Write report.md for a results directory from its raw files.

    bench/report.py results/<run>/

Reads env.json, llama-bench.jsonl and spec.jsonl (bench/run.sh writes them)
and never edits them: the raw files are the record, and this report can be
regenerated from them at any time. Standard library only.
"""
import json
import pathlib
import sys

SECTIONS = {
    "gpu-vs-cpu": "GPU (Vulkan) vs CPU, empty context",
    "depth": "GPU as the context fills (-ub 256)",
    "tuning": "GPU tuning at 8k context: micro-batch and flash attention",
    "kv-type": "GPU tuning at 8k context: KV cache type",
}


def load_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def test_name(r):
    t = f"pp{r['n_prompt']}" if r["n_prompt"] else f"tg{r['n_gen']}"
    return f"{t} @ d{r['n_depth']}" if r.get("n_depth") else t


def device(r):
    return "CPU" if r["n_gpu_layers"] == 0 or r.get("devices") == "none" else r.get("devices", "GPU")


def env_section(env):
    s, c, m, g, sw, p = (env[k] for k in ("system", "cpu", "memory", "gpu", "software", "power"))
    lines = [
        f"# {env['label']}: {sw['llama_cpp']}",
        "",
        f"- **Machine:** {s['vendor']} {s['product']} ({s['product_version']}), BIOS {s['bios']} ({s['bios_date']})",
        f"- **CPU:** {c['model']}, {c['cores']} cores / {c['threads']} threads, governor {c['governor']}, EPP {c['epp']}",
        f"- **Memory:** {m['total_gib']} GiB visible, {m['available_gib']} GiB available at start; "
        f"GPU reserve {g['vram_reserve_mib']} MiB, GTT {round(g['gtt_mib'] or 0)} MiB",
        f"- **Software:** {sw['os']}, kernel {sw['kernel']}, Mesa {sw['mesa_vulkan_drivers']}",
        f"- **Devices:** {'; '.join(sw['devices'])}",
        f"- **Power:** AC {'yes' if p['ac_online'] else 'NO'}, profile {p['platform_profile']}, "
        f"battery {p['battery']}; load average {env['load_average_1m']}",
        f"- **Captured:** {env['captured']}",
        "",
    ]
    for w in env.get("warnings", []):
        lines.append(f"> ⚠️ {w}")
    if env.get("warnings"):
        lines.append("")
    return lines


def bench_section(rows):
    lines = []
    for model in dict.fromkeys(r["model_filename"] for r in rows):
        mrows = [r for r in rows if r["model_filename"] == model]
        first = mrows[0]
        lines += [f"## {pathlib.Path(model).name}", "",
                  f"{first['model_type']}, {first['model_size'] / 2**30:.2f} GiB, {first['model_n_params'] / 1e9:.2f} B params", ""]
        for key, title in SECTIONS.items():
            srows = [r for r in mrows if r.get("section") == key]
            if not srows:
                continue
            lines += [f"### {title}", "",
                      "| device | threads | ubatch | flash attn | KV | test | t/s |",
                      "|---|--:|--:|---|---|---|--:|"]
            for r in srows:
                kv = r["type_k"] if r["type_k"] == r["type_v"] else f"{r['type_k']}/{r['type_v']}"
                lines.append(f"| {device(r)} | {r['n_threads']} | {r['n_ubatch']} | {r['flash_attn']} | {kv} "
                             f"| {test_name(r)} | {r['avg_ts']:.1f} ± {r['stddev_ts']:.1f} |")
            lines.append("")
    return lines


def spec_section(rows):
    if not rows:
        return []
    lines = ["## Speculative decoding (server, 256 tokens, temperature 0)", "",
             "| target | draft | type | alone t/s | with draft t/s | speed-up | accepted |",
             "|---|---|---|--:|--:|--:|--:|"]
    for r in rows:
        a, w, kind = r["alone"], r["with_draft"], r.get("type", "draft-simple")
        if not a or not w:
            lines.append(f"| {r['target']} | {r['draft']} | {kind} | failed | | | |")
            continue
        base, spec = a["predicted_per_second"], w["predicted_per_second"]
        # No draft counters means the draft was loaded but never used (e.g.
        # an upstream build run without --spec-type), not a 1.00x result.
        acc = f"{w['draft_n_accepted']} / {w['draft_n']}" if w.get("draft_n") else "**not drafting**"
        lines.append(f"| {r['target']} | {r['draft']} | {kind} | {base:.1f} | {spec:.1f} | {spec / base:.2f}x | {acc} |")
    return lines + [""]


def main():
    run = pathlib.Path(sys.argv[1])
    env = json.loads((run / "env.json").read_text())
    lines = env_section(env)
    lines += bench_section(load_jsonl(run / "llama-bench.jsonl"))
    lines += spec_section(load_jsonl(run / "spec.jsonl"))
    errors = run / "errors.log"
    if errors.exists() and errors.read_text().strip():
        lines += ["## Errors", "", "```", errors.read_text().strip(), "```", ""]
    (run / "report.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
