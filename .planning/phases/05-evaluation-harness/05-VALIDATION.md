---
phase: "5"
slug: "evaluation-harness"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-18"
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Derived from `05-RESEARCH.md` § Validation Architecture.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None — this repo has no pytest/unittest framework. House pattern: every script implements its own `--self-test` mode with inline assertions (`tools/check_repo.py`, `evals/conformance/run_conformance.py`). |
| **Config file** | none — no framework is installed and none should be |
| **Quick run command** | `python3 evals/lint.py --self-test` |
| **Full suite command** | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py && python3 evals/lint.py --self-test && python3 evals/benchmark/run_benchmark.py --self-test` |
| **Estimated runtime** | ~10 seconds (all offline, zero network calls) |

---

## Sampling Rate

- **After every task commit:** Run `python3 evals/lint.py --self-test` (and `python3 evals/benchmark/run_benchmark.py --self-test` once that file exists)
- **After every plan wave:** Run the full suite command above
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

**The live paid benchmark matrix is NOT part of routine sampling.** It runs once, during the plan that owns it, and its output is committed. It must never become a CI step or a per-commit check — it calls a live model and costs real money on every invocation.

---

## Per-Task Verification Map

Task IDs are assigned by the planner; this map is keyed by requirement until plans exist.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| TBD | A | 1 | EVAL-01 | — | Linter counts proxy violations deterministically; self-test green | unit (offline) | `python3 evals/lint.py --self-test` | ❌ W0 | ⬜ pending |
| TBD | A | 1 | EVAL-02 | — | Every shipped proxy term traces to one of exactly two named external sources; none traces only to this repo | unit (offline) | `python3 evals/lint.py --self-test` | ❌ W0 | ⬜ pending |
| TBD | A | 1 | EVAL-03 | — | Linter output carries the deletion-test / not-a-compliance-verdict disclaimer | unit (offline) | `python3 evals/lint.py --self-test` | ❌ W0 | ⬜ pending |
| TBD | B | 2 | EVAL-04 | V5 | All four artifact families present in `scenarios.json`, ≥1 scenario each; scenario ids drawn only from the committed file | unit (offline) | `python3 evals/benchmark/run_benchmark.py --self-test` | ❌ W0 | ⬜ pending |
| TBD | B | 2 | EVAL-05 | — | Every raw generation record carries `model`, `effort`, and the args it was produced with | unit (offline, fixture raw files) | `python3 evals/benchmark/run_benchmark.py --self-test` | ❌ W0 | ⬜ pending |
| TBD | B | 2 | EVAL-11 | V12 | Raw filenames follow the fixed template; every figure in RESULTS.md resolves to a committed `raw/` file | unit (offline) | `python3 evals/benchmark/run_benchmark.py --report-only` | ❌ W0 | ⬜ pending |
| TBD | B | 2 | EVAL-12 | — | `--report-only` rebuilds RESULTS.md byte-identically from the same `raw/` with zero network calls | unit (offline; assert `subprocess.run` is never reached on this path) | `python3 evals/benchmark/run_benchmark.py --self-test` | ❌ W0 | ⬜ pending |
| TBD | C | 3 | EVAL-06 | — | ≥3 raw records per (model, scenario, condition) cell; RESULTS.md prints mean **and** range | unit (offline, over committed `raw/`) | `python3 evals/benchmark/run_benchmark.py --report-only` | ❌ W0 | ⬜ pending |
| TBD | C | 3 | EVAL-07 | — | Every judgement record is label-stripped and both orders are present per pair | unit (offline, fixture judge files) | `python3 evals/benchmark/run_benchmark.py --self-test` | ❌ W0 | ⬜ pending |
| TBD | C | 3 | EVAL-08 | Tampering | Judge schema always carries `persuasive_force` as a key distinct from `evidence` and `clarity`; a schema-invalid reply is recorded `unscoreable`, never partially accepted | unit (offline) | `python3 evals/benchmark/run_benchmark.py --self-test` | ❌ W0 | ⬜ pending |
| TBD | C | 3 | EVAL-09 | — | RESULTS.md carries both `## Mechanical proxy counts` and `## Judged persuasion` headings; no merged composite figure | unit (offline, text check) | `python3 evals/benchmark/run_benchmark.py --self-test` | ❌ W0 | ⬜ pending |
| TBD | C | 3 | EVAL-10 | — | Caveats section names all five required items: position bias, judge-family bias, baseline prompt parity, proxy provenance, sample size | unit (offline, text check) | `python3 evals/benchmark/run_benchmark.py --self-test` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Every artifact below is net-new — this phase inherits no test infrastructure of its own.

- [ ] `evals/lint.py` — the linter, with `--self-test`
- [ ] `evals/proxy-sources.md` — the two-source provenance registry the linter's provenance checks read
- [ ] `evals/benchmark/run_benchmark.py` — runner + judge + aggregator, with `--self-test` and `--report-only`
- [ ] `evals/benchmark/scenarios.json` and `evals/benchmark/bench-deal-brief.md` — the committed scenario set and its fresh fictional deal
- [ ] Committed fixture JSON under `evals/benchmark/` (generation + judgement records) so `--self-test` can validate real record shapes offline, mirroring `evals/conformance/transcripts/*.txt`
- [ ] `.github/workflows/ci.yml` — add `python3 evals/lint.py --self-test` and `python3 evals/benchmark/run_benchmark.py --self-test` alongside the existing `run_conformance.py --self-test` line. **The live paid matrix must not be added to CI.**

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| The live generation matrix actually runs against pinned models and produces the committed `raw/` files | EVAL-05, EVAL-06 | The call is paid, non-deterministic, and inherently live — it cannot be asserted offline, only its recorded output can | Run `python3 evals/benchmark/run_benchmark.py` once with `claude auth status` showing `loggedIn: true`; confirm the expected record count lands under `evals/benchmark/raw/` |
| Published numbers in RESULTS.md match what the committed raw files actually recompute to | EVAL-11, EVAL-12 | Guards against a hand-edited RESULTS.md — the failure this check exists to catch is a human editing the published number, which no self-test on the generator can see | `python3 evals/benchmark/run_benchmark.py --report-only && git diff --exit-code evals/benchmark/RESULTS.md` — a non-empty diff means the published file was not generated from the committed raw data |
| No published claim outruns the evidence (no p-values, no "significant", no cross-provider generalization) | EVAL-10, and the project's "measured claims or no claims" constraint | Semantic judgement — the research explicitly rejects building a semantic overclaim detector as over-engineering | Human read of RESULTS.md against 05-RESEARCH.md § Decision 8's six named overclaims |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
