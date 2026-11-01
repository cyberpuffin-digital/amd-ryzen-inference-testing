#!/usr/bin/env python3
"""Compare runs side by side, as Markdown.

    analysis/compare.py results/<run A>/ results/<run B>/ [...] > comparison.md

Reads each run's env.json, llama-bench.jsonl and spec.jsonl (bench/run.sh)
and prints, per model, the same tests from every run in adjacent columns,
then the tuning grids and speculative decoding. A run that couldn't load a
model shows "fail" (its errors.log says why); a test a run didn't do shows
"–". Columns are named by llama.cpp build. Standard library only.
"""
import json
import pathlib
import sys


def load_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class Run:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.env = json.loads((self.path / "env.json").read_text())
        self.rows = load_jsonl(self.path / "llama-bench.jsonl")
        self.spec = load_jsonl(self.path / "spec.jsonl")
        version = self.env["software"]["llama_cpp"]
        self.name = version.split("(")[1].split(",")[0].strip() if "(build" in version else version.replace("version: ", "")
        errors = self.path / "errors.log"
        self.failed = errors.read_text() if errors.exists() else ""

    def models(self):
        return list(dict.fromkeys(pathlib.Path(r["model_filename"]).name for r in self.rows))

    def get(self, model, section, gpu, test, depth=0, ub=None, fa=None, kv=None):
        for r in self.rows:
            if pathlib.Path(r["model_filename"]).name != model or r.get("section") != section:
                continue
            if (r["n_gpu_layers"] > 0) != gpu or test_name(r) != test or r["n_depth"] != depth:
                continue
            if ub is not None and r["n_ubatch"] != ub:
                continue
            if fa is not None and bool(r["flash_attn"]) != fa:
                continue
            if kv is not None and (r["type_k"], r["type_v"]) != kv:
                continue
            return r["avg_ts"]
        return None

    def did_fail(self, model):
        return model in self.failed


def test_name(r):
    return f"pp{r['n_prompt']}" if r["n_prompt"] else f"tg{r['n_gen']}"


def cell(run, model, value):
    if value is not None:
        return f"{value:.1f}"
    return "fail" if run.did_fail(model) else "–"


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" if i == 0 else "--:" for i in range(len(header))) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return out + [""]


def main():
    runs = [Run(p) for p in sys.argv[1:]]
    if not runs:
        sys.exit(__doc__)
    names = [r.name for r in runs]
    # Every model any run measured; a run that failed on one shows "fail".
    models = list(dict.fromkeys(m for r in runs for m in r.models()))
    out =["# Comparison: " + " vs ".join(names), ""]
    for r in runs:
        e = r.env
        out.append(f"- **{r.name}**: `{r.path.name}`, kernel {e['software']['kernel']}, GTT {round(e['gpu']['gtt_mib'] or 0)} MiB, "
                   f"{e['memory']['available_gib']} GiB available, load {e['load_average_1m']}"
                   + (f", warnings: {'; '.join(e['warnings'])}" if e.get("warnings") else ""))
    out += ["", "Values are tokens per second (llama-bench mean). pp = prompt processing, tg = generation, "
            "d = context already filled.", ""]

    tests = [
        ("GPU pp512", "gpu-vs-cpu", True, "pp512", 0),
        ("GPU tg128", "gpu-vs-cpu", True, "tg128", 0),
        ("CPU pp512", "gpu-vs-cpu", False, "pp512", 0),
        ("CPU tg128", "gpu-vs-cpu", False, "tg128", 0),
        ("pp2048 @ 0", "depth", True, "pp2048", 0),
        ("pp2048 @ 8k", "depth", True, "pp2048", 8192),
        ("pp2048 @ 16k", "depth", True, "pp2048", 16384),
        ("tg64 @ 0", "depth", True, "tg64", 0),
        ("tg64 @ 8k", "depth", True, "tg64", 8192),
        ("tg64 @ 16k", "depth", True, "tg64", 16384),
    ]
    out += ["## Throughput by model", ""]
    for m in models:
        rows = []
        for label, section, gpu, test, depth in tests:
            vals = [r.get(m, section, gpu, test, depth) for r in runs]
            row = [label] + [cell(r, m, v) for r, v in zip(runs, vals)]
            if len(runs) == 2 and all(v is not None for v in vals) and vals[0]:
                row.append(f"{(vals[1] / vals[0] - 1) * 100:+.0f}%")
            elif len(runs) == 2:
                row.append("")
            rows.append(row)
        header = ["test"] + names + (["change"] if len(runs) == 2 else [])
        out += [f"### {m}", ""] + table(header, rows)

    out += ["## Tuning at 8k context (GPU, pp2048 / tg64)", "",
            "Micro-batch (ub) and flash attention (fa), then KV cache type with ub 256 and fa on.", ""]
    for m in models:
        rows = []
        for ub in (256, 512):
            for fa in (False, True):
                row = [f"ub {ub}, fa {'on' if fa else 'off'}"]
                for r in runs:
                    pp = r.get(m, "tuning", True, "pp2048", 8192, ub=ub, fa=fa)
                    tg = r.get(m, "tuning", True, "tg64", 8192, ub=ub, fa=fa)
                    row.append(f"{cell(r, m, pp)} / {cell(r, m, tg)}")
                rows.append(row)
        for kv in (("f16", "f16"), ("q8_0", "q8_0"), ("f16", "q8_0"), ("q8_0", "f16")):
            row = [f"KV {kv[0]}/{kv[1]}"]
            for r in runs:
                pp = r.get(m, "kv-type", True, "pp2048", 8192, kv=kv)
                tg = r.get(m, "kv-type", True, "tg64", 8192, kv=kv)
                row.append(f"{cell(r, m, pp)} / {cell(r, m, tg)}")
            rows.append(row)
        out += [f"### {m}", ""] + table(["setting"] + names, rows)

    out += ["## Speculative decoding (server, 256 tokens, temperature 0)", ""]
    rows = []
    for r in runs:
        for s in r.spec:
            a, w = s["alone"], s["with_draft"]
            if not a or not w:
                rows.append([r.name, s["target"], s["draft"], s.get("type", "draft-simple"), "fail", "", "", ""])
                continue
            base, fast = a["predicted_per_second"], w["predicted_per_second"]
            acc = f"{w['draft_n_accepted']} / {w['draft_n']}" if w.get("draft_n") else "not drafting"
            rows.append([r.name, s["target"], s["draft"], s.get("type", "draft-simple"),
                         f"{base:.1f}", f"{fast:.1f}", f"{fast / base:.2f}x", acc])
    out += table(["build", "target", "draft", "type", "alone", "with draft", "speed-up", "accepted"], rows)
    print("\n".join(out))


if __name__ == "__main__":
    main()
