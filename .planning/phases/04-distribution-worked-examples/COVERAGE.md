# API Coverage — Phase 4: Distribution & Worked Examples

Most of this phase writes static distribution artifacts (two JSON plugin manifests, two generated
Markdown derivatives, one examples file, a README rewrite) plus stdlib-only Python tooling. The one
external package this phase names — `skills` on npm — appears only inside a documented
`npx skills add` command an end user runs from README; this repository never invokes it, adds no
dependency manifest, and remains zero-dependency. That zero-dependency statement is still true and
is not what changed below.

**Corrected 2026-09-21 by 04-15.** This file previously read "calls no external API, SDK or service
at any point." That became false when `04-15` shipped `evals/routes/run_routes.py`, which drives
live headless `claude -p` sessions through the local Claude Code CLI to measure route equivalence —
40 sessions in total (4 committed under `evals/routes/probe/`, 36 under `evals/routes/raw/`), billed
to the operator's own authenticated subscription. This is the same live-session shape Phase 3's
`evals/conformance/run_conformance.py` and Phase 5's `evals/benchmark/run_benchmark.py` already
record, and it is recorded here for the same reason: a coverage file that understates what a phase
calls is the failure this repository's own standard exists to prevent.

No dependency manifest is added by any of it. The `claude` binary is already installed, the runner
imports only the Python standard library, and `--self-test` — the only mode CI runs — makes no
subprocess call and no network call at all.

The deterministic detector was run at planning time against this phase's ROADMAP scope and returned
`{"detected": false, "signals": []}`. That verdict was correct for the scope as planned then, and
`04-15` was added to the phase afterwards; the detector was not re-run.
