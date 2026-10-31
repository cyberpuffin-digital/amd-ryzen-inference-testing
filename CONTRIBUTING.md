# Contributing

## Submitting a run

1. Follow "Reproduce a run" in the [README](README.md). Use a label that names
   the hardware, not you: `<maker><model>-<cpu>`, e.g. `fw13-7840u`, `minipc-8845hs`.
2. Run it idle, on AC, in the performance power profile, with the browser
   closed. If you can't, keep the warnings: they're recorded in `env.json`
   and shown in the report.
3. Keep private names out. Put your internal domains and host names in
   `~/.config/amd-ryzen-inference/redact.txt` (see
   `bench/redact.example.txt`) **before** running, and enable the hooks with
   `git config core.hooksPath .githooks`; see "Privacy" in the README. Then
   read `env.json` and `report.md` yourself before committing.
4. Open a pull request adding `results/<date>_<label>_<build>/` unchanged.
   If your hardware is new here, add or extend a note in `hardware/`.

## Ground rules

- **Raw files are the record.** Never edit `env.json` or the `.jsonl` files
  after a run. `report.md` is generated and can be rebuilt with
  `bench/report.py <dir>`.
- **Measured or untested, always say which.** Hardware notes mark each claim.
  A later measurement that contradicts a note corrects it in place, with the
  date and the run that showed it.
- **Change one thing between runs you mean to compare,** and say what it was
  in the pull request.

## Licensing

By contributing you agree that code is released under MIT and results and
documentation under CC BY 4.0, as described in the README.
