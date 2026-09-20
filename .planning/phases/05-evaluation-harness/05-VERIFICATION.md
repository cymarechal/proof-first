---
phase: 05-evaluation-harness
verified: 2026-09-20T00:00:00Z
status: passed
score: "5/5 must-haves verified"
behavior_unverified: 0
overrides_applied: 0
---

# Phase 5: Evaluation Harness Verification Report

**Phase Goal:** Anyone can reproduce a credible, honestly-caveated measurement of the skill's
effect using only committed scripts and data.

**Verified:** 2026-09-20
**Status:** passed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth (ROADMAP Success Criteria) | Status | Evidence |
|---|---|---|---|
| 1 | A deterministic linter counts rule-proxy violations using only the Python standard library, passes its own self-test, and states plainly the deletion test is a semantic judgment it cannot perform | ✓ VERIFIED | `python3 evals/lint.py --self-test` re-run independently → exits 0, prints both disclaimer sentences and names all 8 codes. AST-import check (re-derived from plan `<verify>`) confirms only `argparse, json, pathlib, re, sys`. |
| 2 | The linter's buzzword proxy list is sourced independently of the skill's own worked examples, so the measured improvement isn't circular | ✓ VERIFIED | `evals/proxy-sources.md` binds every term to source `A` (Wikipedia MOS:WTW) or `B` (GSA plain-language); `proxy-term-unsourced`/`-invalid`/`-is-internal` are enforced and self-tested. `grep -n "worked-examples" evals/lint.py evals/proxy-sources.md` shows the file referenced only in disclosure prose (the honest "cannot prove a human never looked" ceiling), never as a term source — confirmed by direct read. |
| 3 | A committed scenario set drives generations across all four artifact families, run headlessly across multiple pinned Claude models, at least three times per cell | ✓ VERIFIED | `evals/benchmark/scenarios.json` = 8 scenarios, 2 per family (`rfp-rfi`, `solution-proposal`, `executive-summary`, `demo-discovery`), no `PF-`/`MC-` tokens (re-grepped, zero hits). Independently recomputed cell coverage from `evals/benchmark/raw/*.json`: 32 (model, scenario, condition) generation cells, every one exactly `n=3` scoreable records (min=max=3) — the ≥3 floor met everywhere, with no margin. Two models (`claude-sonnet-5`, `claude-opus-5`) confirmed in both raw filenames and RESULTS.md. |
| 4 | A blind pairwise judge scores skill-on against skill-off with labels stripped and both text orders run, scoring persuasive force as its own dimension so a flat-but-clean draft can't pass on clarity alone | ✓ VERIFIED | `build_judge_prompt()` asserted label-stripped by its own self-test case (`judge-prompt-label-stripping`, re-run and confirmed passing). Sample judgement record read directly (`evals/benchmark/raw/*__judge__demo-discovery-1*order1.json`) shows `order: 1`, `text_a_condition`/`text_b_condition`, and three independent scores (`evidence`, `clarity`, `persuasive_force`) with `persuasive_force` never derived from the other two — self-test case `judge-missing-dimension-unscoreable` proves the negative. Both orders present for every scoreable pair; `judge_summary()` win/tie/loss re-summed independently from RESULTS.md's own table: `persuasive_force` totals 7 wins / 3 ties / 38 losses, matching the SUMMARY's disclosed figure exactly. |
| 5 | Published results report mechanical-proxy counts and judged persuasion as two separately labeled figures with variance alongside the mean, name honest caveats, and every raw generation/judgement is committed so any number can be recomputed with one documented command | ✓ VERIFIED | `evals/benchmark/RESULTS.md` carries `## Mechanical proxy counts` and `## Judged persuasion` as two distinct top-level sections, each row showing `n`, `Mean`, and `Range` — no composite figure found anywhere (re-grepped for a blended score, none exists). Caveats section names all six items (five required + the added `judge construct validity`) with real content, not labels. `python3 evals/benchmark/run_benchmark.py --report-only && git diff --exit-code evals/benchmark/RESULTS.md` re-run independently → clean (0 diff). 192 raw JSON files committed and git-tracked (96 generation + 96 judgement), confirmed via `git status --short` (clean working tree) and `ls evals/benchmark/raw \| wc -l` = 192. |

**Score:** 5/5 truths verified (0 present, behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `evals/lint.py` | Stdlib-only linter, 8 codes, self-test, disclaimer | ✓ VERIFIED | 674 lines (per SUMMARY); self-test re-run green; imports checked stdlib-only |
| `evals/proxy-sources.md` | External-source registry, ≥12 rows, label A/B | ✓ VERIFIED | 93 lines; provenance ceiling stated; read directly |
| `evals/benchmark/bench-deal-brief.md` | Fresh fictional deal, zero shared entities with `examples/deal-brief.md` | ✓ VERIFIED | `grep` for the four named entities (Halverton Mutual, Kestrel Systems Group, Diane Osoria, Marcus Feld) returned zero matches |
| `evals/benchmark/scenarios.json` | 8 scenarios, 2/family | ✓ VERIFIED | Re-parsed independently: 8 entries, 4 families × 2 each |
| `evals/benchmark/run_benchmark.py` | Runner, matrix, judge, aggregator, renderer | ✓ VERIFIED | Self-test names 36 distinct fake-envelope/assertion cases, all passing |
| `evals/benchmark/raw/` | 192 committed JSON records | ✓ VERIFIED | 192 files, 96 `__judge__`, git-tracked, working tree clean |
| `evals/benchmark/RESULTS.md` | Two-section report, byte-stable from raw | ✓ VERIFIED | Re-render diff clean; both headings and all six caveats present |
| `.github/workflows/ci.yml` | Runs both self-tests, no live-model command | ✓ VERIFIED | Read directly — single `run:` block, `evals/lint.py --self-test` and `evals/benchmark/run_benchmark.py --self-test` both present, no live invocation anywhere |

### Key Link Verification

| From | To | Via | Status |
|---|---|---|---|
| `evals/lint.py` | `evals/proxy-sources.md` | provenance cross-check at self-test time | ✓ WIRED — `proxy-term-unsourced` etc. fire against a mutated registry copy in self-test |
| `.github/workflows/ci.yml` | `evals/lint.py` / `run_benchmark.py` | `--self-test` on every push/PR | ✓ WIRED — confirmed by direct file read |
| `evals/benchmark/run_benchmark.py` | `evals/lint.py` | `_load_lint_module()` execs the linter source to compute the mechanical-proxy half | ✓ WIRED — RESULTS.md's "Mechanical proxy counts" section is populated with real per-cell means, not zeros |
| `evals/benchmark/RESULTS.md` | `evals/benchmark/raw/` | `--report-only` is the only writer | ✓ WIRED — re-render diff is clean |

### Requirements Coverage

All 12 EVAL-* IDs declared across the three plans' frontmatter (`requirements:` fields union to exactly EVAL-01 through EVAL-12, no gaps, no orphans) are marked `Complete` with `[x]` in `.planning/REQUIREMENTS.md` (lines 69-80, cross-referenced against the traceability table at lines 168-179). No `[x]` sits adjacent to an `UNVERIFIED` marker anywhere in the file (checked with `grep -n "UNVERIFIED"` — the 10 UNVERIFIED hits found all belong to unrelated pre-existing requirements from Phases 3/4/6, none are EVAL-*).

| Requirement | Source Plan | Status | Evidence |
|---|---|---|---|
| EVAL-01 | 05-01 | ✓ SATISFIED | linter self-test, verified above |
| EVAL-02 | 05-01 | ✓ SATISFIED | provenance registry + allow-list codes |
| EVAL-03 | 05-01 | ✓ SATISFIED | disclaimer present in every mode |
| EVAL-04 | 05-02 | ✓ SATISFIED | 8 scenarios, 4 families, no vocabulary leak |
| EVAL-05 | 05-02/05-03 | ✓ SATISFIED | 2 pinned models, effort recorded, raw records carry full schema |
| EVAL-06 | 05-03 | ✓ SATISFIED | every cell n=3, RESULTS.md prints mean + range |
| EVAL-07 | 05-03 | ✓ SATISFIED | label-stripped, both orders, offline-proven judge |
| EVAL-08 | 05-03 | ✓ SATISFIED | `persuasive_force` independent key, unscoreable-if-missing |
| EVAL-09 | 05-02/05-03 | ✓ SATISFIED | two separate headed sections, no composite |
| EVAL-10 | 05-02/05-03 | ✓ SATISFIED | all caveats present with real content |
| EVAL-11 | 05-02/05-03 | ✓ SATISFIED | 192 files committed, re-render diff clean |
| EVAL-12 | 05-02/05-03 | ✓ SATISFIED | `--report-only` documented, zero-subprocess proven |

### Anti-Patterns Found

None. `grep` for `TBD|FIXME|XXX|TODO|HACK|PLACEHOLDER` across all phase-modified files (`evals/lint.py`, `evals/proxy-sources.md`, `evals/benchmark/run_benchmark.py`, `evals/benchmark/bench-deal-brief.md`, `evals/benchmark/scenarios.json`, `evals/benchmark/RESULTS.md`) returned zero hits.

### Behavioral Spot-Checks / Probe Execution

All of this phase's own instruments are its "probes." Every one was re-run independently by this
verifier (not merely quoted from SUMMARY or the orchestrator's notes) and matched:

| Check | Command | Result | Status |
|---|---|---|---|
| Linter self-test | `python3 evals/lint.py --self-test` | exit 0, 8 codes, disclaimer printed | ✓ PASS |
| Benchmark self-test | `python3 evals/benchmark/run_benchmark.py --self-test` | exit 0, 36 named cases | ✓ PASS |
| Repo checker | `python3 tools/check_repo.py` | `check_repo: 0 violations` | ✓ PASS |
| Repo checker self-test | `python3 tools/check_repo.py --self-test` | PASS, 48 codes | ✓ PASS |
| Mutation test | `python3 tools/check_repo.py --mutation-test` | PASS, 48 codes discrimination-proven | ✓ PASS |
| Conformance self-test | `python3 evals/conformance/run_conformance.py --self-test` | PASS, 4 verdicts discriminated | ✓ PASS |
| Derivatives check | `python3 tools/generate_derivatives.py --check` | exit 0 | ✓ PASS |
| Report re-render + diff | `--report-only && git diff --exit-code evals/benchmark/RESULTS.md` | clean, 0 diff | ✓ PASS |
| Entity-collision grep | `grep <4 entities> evals/benchmark/bench-deal-brief.md` | no matches | ✓ PASS |
| Cell-floor recompute | manual Python recompute over `raw/*.json` | 32/32 cells at exactly n=3 | ✓ PASS |
| persuasive_force totals recompute | manual sum over RESULTS.md's own table | 7/3/38, matches SUMMARY | ✓ PASS |

### Honest-Result Integrity Check (pay-particular-attention item 1)

Confirmed directly against the committed `RESULTS.md` and re-derived by independent recomputation
(not copied from the SUMMARY): the skill wins decisively on `evidence` (45/1/2 across the 24
per-dimension win/tie/loss rows), wins moderately on `clarity` (32/3/13), and **loses on
`persuasive_force`** (7/3/38) — the dimension the skill is named for. Mechanical proxy counts are
close to a wash (skill-on fewer in 8 of 16 model/scenario pairs, more in 7, equal in 1; summed
mean 131.3 → 119.6, independently spot-checked against several rows in the "Mechanical proxy
counts" table). `RESULTS.md`'s own prose states this plainly with no softening or spin — the
caveats section and the win/tie/loss table are the report's own numbers, not a narrative gloss.
`05-03-SUMMARY.md` states the same finding in its Decisions section without hedging ("This LLM
judge rates the skill's output LESS persuasive on the exact dimension the skill is named for").
This is judged to satisfy the "measured claims or no claims" constraint, not violate it.

### Disclosed Gaps (pay-particular-attention items 2 and 3)

Both confirmed present and honestly framed, not silently omitted:

- **Judge cost gap (item 2):** Judgement records carry no `cost_usd`/`usage` fields — confirmed by
  direct inspection of a sample judgement record (see truth #4 evidence above; the JSON has no
  such keys). `05-03-SUMMARY.md`'s Decisions section states "$18.21 is the generation cost only,
  not the run total" and explicitly names the missing judge-pass cost as "a gap in Task 1's
  judgement-record schema, not estimated and presented as measured." `RESULTS.md` itself makes no
  cost claim, sidestepping the risk of the gap leaking into the published report.
- **Interruption disclosure (item 3):** `05-03-SUMMARY.md`'s Decisions section discloses the first
  invocation dying at 164/192 records (reaped parent shell, zero error records, not a usage-limit
  exhaustion), the detached resume, and the ≈72-minute total wall clock against the ≈58-minute
  estimate — following the MOD-04 precedent of keeping rather than deleting records from an
  interrupted run. All 192 records are present and none show signs of having been dropped.

### Requirement ID Accounting (pay-particular-attention item 4)

Confirmed: `05-02-SUMMARY.md` frontmatter declares `requirements-completed: [EVAL-04]` only,
leaving EVAL-05/09/10/11/12 `Pending` at that point (by design — those IDs are shared with
`05-03`, whose own frontmatter also declares them). `05-03-SUMMARY.md` frontmatter declares
`requirements-completed: [EVAL-05, EVAL-06, EVAL-07, EVAL-08, EVAL-09, EVAL-10, EVAL-11,
EVAL-12]`. Cross-referencing both against the live `.planning/REQUIREMENTS.md`: all twelve EVAL-*
IDs are now `[x]` Complete with no ID left Pending and no ID double-counted incorrectly.

### Recurring Hazard Check (pay-particular-attention item 5)

`grep -n "UNVERIFIED" .planning/REQUIREMENTS.md` returns 10 hits, all belonging to CAT-10, AUD-01,
ART-01 through ART-04, MOD-04, EX-02, DIST-01, DIST-02, and DIST-06 — none are EVAL-* IDs, and
none of those lines carry a `[x]` checkbox (all are `[ ]`). No `[x]`-adjacent-to-`UNVERIFIED`
condition exists for this phase's requirement set.

### Human Verification Required

None. Every must-have this phase declares was either mechanically re-verified by this verifier
independently (not merely trusted from SUMMARY/orchestrator claims) or is explicitly scoped as a
`verification: backstop` truth in the PLAN frontmatter (e.g., "the shipped terms are a defensible
sample," "the eight scenarios are realistic presales tasks," "no published claim outruns the
evidence") — these backstop truths were already given a human read during plan execution (05-03
Task 3's `<human-check>` was executed by the orchestrator during the phase and its finding, one
real gap, was closed by this continuation's sixth-caveat fix, independently confirmed present in
the committed `RESULTS.md`). No further human verification item is outstanding.

### Gaps Summary

None. All five ROADMAP success criteria hold under independent re-verification (re-run gate
commands, re-read committed files, re-derived figures rather than trusting SUMMARY prose). The
phase's headline finding is unflattering (the skill loses on `persuasive_force`) and is reported
straight in both `RESULTS.md` and the SUMMARY, which is the correct behavior under this project's
"measured claims or no claims" constraint — not a defect. The one known, disclosed instrument gap
(missing judge-pass `cost_usd`) is named honestly rather than patched with an invented number, and
does not block the phase goal: reproducibility of the published figures does not depend on cost
tracking. Working tree is clean; no uncommitted phase artifacts.

### Post-verification fix note (2026-09-20, same day)

CR-01 from `05-REVIEW.md` (Critical) was found after this verification report's initial pass:
`generate_report()`'s default `as_of_date` was a live clock read
(`datetime.datetime.now(...).date().isoformat()`), never exercised by an `--as-of-date` flag,
so every real `--report-only` invocation took the clock branch. This had already published a
false headline date in the committed artifact — `RESULTS.md` read `Measured 2026-09-20` for a
matrix whose `raw/` records are all timestamped 2026-09-18.

Truth #5's evidence above and Check "Report re-render + diff" in the Behavioral Spot-Checks
table were both true statements about the code as it stood at verification time — `--report-only`
re-rendered a clean diff against the then-committed `RESULTS.md`, because both the prior render
and this verifier's re-render happened on the same calendar day (2026-09-20), and a clock-driven
default produces the same wrong date twice within one UTC day. That made the re-render proof
correct only incidentally, and only within a single UTC day — not the durable, data-derived proof
EVAL-11/EVAL-12 require.

**Fix applied** (see `05-03-SUMMARY.md`'s "Post-verification fix" section for full detail):
`as_of_date` is now derived from the committed generation records' own `timestamp` fields via a
new `_as_of_date_from_records()` helper — no clock read remains anywhere in the render path. A
new self-test (`cr01-report-only-render-is-clock-independent`) monkey-patches the module's clock
to two different fake dates and proves the render is byte-identical and clock-independent under
both. `RESULTS.md` was regenerated via `--report-only` (never hand-edited) and now correctly
reads `Measured 2026-09-18 across claude-opus-5, claude-sonnet-5 (96 generations recorded)` — the
actual run date carried by the raw records, not the render date. `git diff --exit-code
evals/benchmark/RESULTS.md` is clean after re-render, and this now holds regardless of which
calendar day the re-render is performed on — the exact durability gap this fix closes.

Truth #5 and its Behavioral Spot-Check are re-affirmed **VERIFIED** with this correction: the
re-render proof is strengthened from same-day-coincidentally-clean to genuinely data-derived and
clock-independent, and the published headline now names the correct date. No other truth,
artifact, or requirement in this report is affected — CR-01 was scoped to the headline
`as_of_date` value only, never to the aggregation, judging, or caveat logic this report already
verified. This phase's `status: passed` verdict stands unchanged; CR-02, CR-03, CR-04, and the
`05-REVIEW.md` Warnings remain open, tracked in `.planning/WINDOWS.md` (entries 20-23), and are
out of scope for this note.

---

_Verified: 2026-09-20_
_Verifier: Claude (gsd-verifier)_
_Post-verification fix appended: 2026-09-20_
