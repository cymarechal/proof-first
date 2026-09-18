---
phase: 05-evaluation-harness
plan: 02
subsystem: testing
tags: [benchmark, scenarios, aggregator, offline, stdlib, ci]

requires:
  - phase: 05-evaluation-harness
    provides: "05-01's evals/lint.py (lint(), eight violation codes, self-test) — this plan's
      aggregator loads it by path for the mechanical-proxy half of the report"
provides:
  - "A fresh fictional deal (evals/benchmark/bench-deal-brief.md) and 8 committed scenarios
    (2 per artifact family), no entity or vocabulary shared with examples/deal-brief.md or the
    skill's own rule numbers"
  - "A generation runner (run_generation()/run_matrix()) proven offline against fixtures:
    isolated-temp-dir sessions, skip-if-exists resumability, unscoreable-on-failure recording,
    deterministic 96-cell enumeration, durability on interruption"
  - "An offline aggregator/renderer (load_raw_records()/aggregate()/build_results_md()/
    generate_report(), wired to --report-only) that turns committed raw JSON into RESULTS.md with
    two never-blended figure sections and a five-item honest-caveats block, proven to make zero
    subprocess calls"
  - "evals/benchmark/run_benchmark.py --self-test wired into .github/workflows/ci.yml, with no
    live-model command anywhere in the file"
affects: [05-03-benchmark-runner-and-judge]

actuals:
  tokens: 29334
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns:
    - "exec()-based module loading (_load_lint_module()) to reuse evals/lint.py's real lint()
      function from a stdlib-only-import-checked file without adding a non-stdlib import name"
    - "Constant-driven report sections (RESULTS_SECTION_HEADINGS, REQUIRED_CAVEATS + CAVEAT_TEXT)
      so the renderer cannot silently drift from what its own self-test checks"
    - "Single-writer-per-path + skip-if-exists resumability, copied in shape from
      evals/conformance/run_conformance.py"

key-files:
  created:
    - evals/benchmark/bench-deal-brief.md
    - evals/benchmark/scenarios.json
    - evals/benchmark/run_benchmark.py
    - evals/benchmark/fixtures/generation-success-envelope.json
    - evals/benchmark/fixtures/generation-record-example.json
    - evals/benchmark/fixtures/results-render/ (24 committed generation/judgement fixture records)
  modified:
    - .github/workflows/ci.yml

key-decisions:
  - "Judgement record scores nested as {dimension: {condition: value}} rather than
    05-RESEARCH.md Decision 7's flat {dimension: value} worked example -- the flat sketch does
    not say which physical text (A or B) a number belongs to, which Decision 5's
    both-orders-average-per-dimension arithmetic requires knowing. Every top-level field name in
    Decision 7's schema is unchanged; only the internal shape of scores' value is resolved, since
    a live judge-calling function is out of this plan's scope (05-03's to build)."
  - "load_scenarios() validates only per-scenario fields (id/family present and valid) plus
    non-empty file; the all-four-families-covered-with->=2-each completeness check is a
    self-test-only assertion (_assert_family_coverage()) over the shipped file, not a property
    the generic loader enforces -- Task 1's own intermediate 2-scenario file is a legitimate
    load_scenarios() input."
  - "run_generation() itself performs the skip-if-exists check and writes the record on both the
    success and empty-text paths; only a SessionFailedError (non-zero exit, is_error, unparseable
    envelope) is left to run_matrix() (or self_test() acting as a single-cell caller) to catch and
    record as unscoreable -- resolves an ambiguity in the plan's own <behavior> text about which
    function 'writes' versus 'raises'."
  - "run_matrix()/run_generation() are real, complete code paths, not stubs -- they have simply
    never been exercised against a live claude binary in this environment, by design (Task 1's own
    title: 'generated end to end and recorded -- with the generation faked, not paid for')."

patterns-established:
  - "A stdlib-only file that needs another stdlib-only file's function (not a package) loads it by
    reading and exec()'ing its source under a private namespace dict, rather than manipulating
    sys.path and using a live import statement that a downstream AST-based import-allowlist check
    would flag."

requirements-completed: [EVAL-04]

coverage:
  - id: D1
    description: "evals/benchmark/bench-deal-brief.md: a fresh fictional freight-brokerage deal,
      structurally parallel to examples/deal-brief.md, sharing no company, person, platform, or
      figure with it"
    requirement: EVAL-04
    verification:
      - kind: unit
        ref: "evals/benchmark/run_benchmark.py#self_test (no-entity-collision case)"
        status: pass
    human_judgment: true
    rationale: "The mechanical check proves the four named shared-brief entities do not appear in
      the new file; it cannot prove no OTHER entity or fact quietly leaked, and it cannot run the
      name-collision web search Phase 1 ran for the original brief (no live network access in this
      environment) -- both are disclosed as WINDOWS.md open unrun-verify items (ids 18-19)."
  - id: D2
    description: "evals/benchmark/scenarios.json: 8 scenarios, exactly 2 per artifact family, no
      PF-/MC-/proof-first vocabulary leakage toward the skill-off condition"
    requirement: EVAL-04
    verification:
      - kind: unit
        ref: "evals/benchmark/run_benchmark.py#self_test (family-coverage-positive/-negative,
          no-vocabulary-leakage, cell-enumeration-96 cases)"
        status: pass
      - kind: other
        ref: "python3 -c \"...family/dup check...\" (05-02-PLAN.md Task 2 <verify>)"
        status: pass
    human_judgment: true
    rationale: "Whether the eight prompts are realistic presales tasks a bid team would actually
      receive, rather than prompts shaped to favor one condition, is a verification:backstop truth
      per 05-02-PLAN.md's own must_haves -- no mechanical check performs that judgment (WINDOWS.md
      id 19)."
  - id: D3
    description: "run_generation(): isolated-temp-dir claude -p session driver with skip-if-exists
      resumability, both envelope shapes handled, and failure recorded as unscoreable rather than
      scored"
    requirement: EVAL-05
    verification:
      - kind: unit
        ref: "evals/benchmark/run_benchmark.py#self_test (success, skip-if-exists, non-zero-exit,
          is-error, array-envelope, committed-fixture-schema cases)"
        status: pass
    human_judgment: false
  - id: D4
    description: "run_matrix(): deterministic model x condition x scenario x repeat enumeration
      (96 cells for the default matrix), zero subprocess calls against a fully-populated raw
      directory, and durability on interruption (an in-flight cell never destroys already-written
      records)"
    requirement: EVAL-11
    verification:
      - kind: unit
        ref: "evals/benchmark/run_benchmark.py#self_test (cell-enumeration-96,
          run-matrix-skip-if-exists, run-matrix-durability-on-interruption cases)"
        status: pass
    human_judgment: false
  - id: D5
    description: "load_raw_records()/aggregate(): sorted, creation-order-independent raw loading
      that refuses (naming the path) an empty or unparseable file rather than skipping it; a
      below-3-repeats cell reports its actual n, never a silent 3; no stdev/CI/p-value computed
      anywhere"
    requirement: EVAL-11
    verification:
      - kind: unit
        ref: "evals/benchmark/run_benchmark.py#self_test (load-raw-records-empty-file,
          load-raw-records-unparseable-file, load-raw-records-sorted-order,
          aggregate-below-3-repeats-reports-actual-n cases)"
        status: pass
    human_judgment: false
  - id: D6
    description: "build_results_md(): two separately headed top-level sections (Mechanical proxy
      counts, Judged persuasion) never blended into one figure, and a five-item Honest caveats
      section built from a shared constant so it cannot drift from what the self-test checks"
    requirement: EVAL-09
    verification:
      - kind: unit
        ref: "evals/benchmark/run_benchmark.py#self_test
          (results-render-fixture-two-headings-five-caveats-byte-identical, per-caveat-drift-guard
          cases)"
        status: pass
    human_judgment: false
  - id: D7
    description: "Honest caveats section names all five required items (position bias,
      judge-family bias, baseline prompt parity, proxy provenance, sample size) with real content,
      and the rendered report contains no p-value, confidence interval, standard deviation, or the
      word 'significant'"
    requirement: EVAL-10
    verification:
      - kind: unit
        ref: "evals/benchmark/run_benchmark.py#self_test
          (results-render-fixture-two-headings-five-caveats-byte-identical case, forbidden-phrase
          scan)"
        status: pass
    human_judgment: false
  - id: D8
    description: "generate_report()/--report-only: offline recompute from committed raw records
      makes zero subprocess calls (proven by replacing subprocess.run with a function that
      raises), refuses an empty raw directory rather than rendering an empty report, and
      evals/benchmark/RESULTS.md is not committed by this plan"
    requirement: EVAL-12
    verification:
      - kind: unit
        ref: "evals/benchmark/run_benchmark.py#self_test (generate-report-empty-dir,
          report-only-no-subprocess-call, no-committed-results-md cases)"
        status: pass
      - kind: other
        ref: "python3 evals/benchmark/run_benchmark.py --report-only --raw-dir
          evals/benchmark/fixtures/results-render --out /tmp/RESULTS-smoke.md (manual smoke test,
          not committed)"
        status: pass
    human_judgment: false
  - id: D9
    description: ".github/workflows/ci.yml runs run_benchmark.py --self-test as a new build gate,
      with no live-model command anywhere in the file"
    requirement: EVAL-04
    verification:
      - kind: other
        ref: "awk '/run_benchmark\\.py/ ...' .github/workflows/ci.yml (05-02-PLAN.md Task 1
          <verify>)"
        status: pass
    human_judgment: false

duration: ~50min (exact start timestamp not captured; estimated from the extensive research/design
  read phase plus the three commits' own timestamps, 17:25-17:34 local)
completed: 2026-09-18
status: complete
---

# Phase 5 Plan 2: Offline Benchmark Half (Scenarios, Generation Runner, Aggregator) Summary

**A fresh fictional deal, 8 committed benchmark scenarios, and a generation-runner/aggregator/
renderer for Proof First's skill-on/skill-off benchmark, all proven offline against committed
fixtures with zero live model calls made.**

## Performance

- **Duration:** ~50 min (see frontmatter `duration` for the estimation basis)
- **Completed:** 2026-09-18
- **Tasks:** 3
- **Files modified:** 30 (2 files modified, 28 created — including 26 committed fixture JSON
  records)

## Accomplishments

- `evals/benchmark/bench-deal-brief.md` ships a fresh fictional freight-brokerage deal (Thornfield
  Freight Systems / Meridian Cloud Partners, Hyper-V + Microsoft SQL Server migrating to Google
  Cloud), structurally parallel to `examples/deal-brief.md` and sharing zero company, person,
  platform, or figure with it.
- `evals/benchmark/scenarios.json` ships exactly 8 scenarios, 2 per artifact family (`rfp-rfi`,
  `solution-proposal`, `executive-summary`, `demo-discovery`), each pair genuinely exercising a
  different task within its family, with no `PF-`/`MC-`/`proof-first` vocabulary anywhere in a
  prompt.
- `evals/benchmark/run_benchmark.py` (1,399 lines) implements the whole free half of the
  benchmark: `SessionFailedError`, `_git_blob_sha()`, `_write_json_atomic()`, `load_scenarios()`,
  `_unwrap_envelope()` (both CLI envelope shapes), `raw_path_for_generation()`/
  `raw_path_for_judgement()` on the frozen filename templates, `run_generation()` (isolated
  temp-dir sessions, skip-if-exists, unscoreable-on-failure), `run_matrix()` (deterministic
  96-cell default enumeration, zero subprocess calls when fully resumed, durability on
  interruption), `_load_lint_module()` (loads `evals/lint.py`'s real `lint()` without an `import`
  statement), `load_raw_records()`/`aggregate()`/`build_results_md()`/`generate_report()` (the
  offline `--report-only` path), and a 25-case `self_test()` — all runnable on a machine with no
  `claude` binary installed.
- `RESULTS.md`'s renderer keeps `## Mechanical proxy counts` and `## Judged persuasion` as two
  structurally separate sections (never blended), and its `## Honest caveats` section is built
  from a shared `REQUIRED_CAVEATS`/`CAVEAT_TEXT` constant pair so the five required items (position
  bias, judge-family bias, baseline prompt parity, proxy provenance, sample size) cannot silently
  drift from what the self-test checks.
- 26 committed fixture JSON files (2 single-record schema fixtures + 24 records under
  `fixtures/results-render/`, covering 2 models × 2 conditions × 3 repeats plus both judge orders)
  let the self-test render a real report from real committed files, with no
  `evals/benchmark/RESULTS.md` committed (that file is `05-03`'s to write from the live matrix).
- `.github/workflows/ci.yml` runs `python3 evals/benchmark/run_benchmark.py --self-test` as one
  new line, added directly after `05-01`'s linter line, with no live-model command anywhere in the
  file. All seven CI gate commands (the five pre-existing plus `evals/lint.py --self-test` and this
  plan's new line) pass.

## Task Commits

Each task was committed atomically:

1. **Task 1: One scenario, generated end to end and recorded (faked, not paid for)** —
   `1577910` (feat) — tracer task; feedback gate re-ran Task 1's full `<verify>` end-to-end before
   expansion, all green
2. **Task 2: The remaining six scenarios, and the matrix loop that drives all eight** —
   `8331a3e` (feat)
3. **Task 3: The offline aggregator and the report renderer, proven never to shell out** —
   `723137a` (feat)

_Note: all three tasks carried `tdd="true"`; per Phase 5 Plan 1's own established precedent (see
its Deviations section), test assertions and implementation were built and verified together per
task rather than as separate RED/GREEN commits — each task's self-test extension was written
alongside the code it exercises and both landed in the same commit._

## Files Created/Modified

- `evals/benchmark/bench-deal-brief.md` — fresh fictional deal, 172 lines, Canonical figures table
- `evals/benchmark/scenarios.json` — 8 scenarios, 2 per family
- `evals/benchmark/run_benchmark.py` — generation runner, matrix loop, offline aggregator/renderer,
  self-test (1,399 lines)
- `evals/benchmark/fixtures/generation-success-envelope.json` — a committed `claude -p` success
  envelope fixture
- `evals/benchmark/fixtures/generation-record-example.json` — the resulting generation record,
  committed so the schema is an artifact, not only an inline dict
- `evals/benchmark/fixtures/results-render/*.json` (24 files) — generation + judgement records
  proving a real report render from committed files
- `.github/workflows/ci.yml` — one new line, `python3 evals/benchmark/run_benchmark.py --self-test`

## Decisions Made

See `key-decisions` in frontmatter. The one with the most downstream consequence for `05-03`:
judgement records nest `scores` as `{dimension: {condition: value}}` rather than
`05-RESEARCH.md` Decision 7's flat `{dimension: value}` sketch, because the flat shape cannot by
itself say which physical text (A or B) a score belongs to — information Decision 5's own
both-orders-average-per-dimension arithmetic needs. Every top-level field name from Decision 7 is
unchanged; `05-03`'s live judge-calling code must emit `scores` in this nested shape for
`aggregate()` to consume it correctly.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Plan ambiguity] `load_scenarios()`'s family-coverage check moved out of the
generic loader**
- **Found during:** Task 1
- **Issue:** Task 1's `<behavior>` lists `load_scenarios()` raising on "a file missing a family"
  as one of its checks. Read literally as "the file overall does not cover all four families,"
  this would make `load_scenarios()` reject Task 1's own intermediate 2-scenario `scenarios.json`
  (which legitimately covers only 2 of 4 families until Task 2 completes it) — self-contradicting
  the plan's own two-commit structure.
- **Fix:** Read "missing a family" as a per-scenario field check (a scenario object with no
  `family` key), which is what the literal wording most naturally supports and what the shipped
  Task 1 file needed to pass. The all-families-covered-with->=2-each completeness requirement
  (explicitly named in Task 2's own `<behavior>`: "a family carrying only 1 scenario") was
  implemented as a separate, self-test-only `_assert_family_coverage()` function, exercised in
  both directions in Task 2's self-test.
- **Files modified:** `evals/benchmark/run_benchmark.py`
- **Verification:** `python3 evals/benchmark/run_benchmark.py --self-test` (family-coverage
  cases) passes for both the shipped file and negative fixtures.
- **Committed in:** `1577910` (Task 1), extended `8331a3e` (Task 2)

**2. [Rule 1 - Plan ambiguity] Judgement record `scores` shape resolved by documented decision**
- **Found during:** Task 3
- **Issue:** `05-RESEARCH.md` Decision 7's worked judgement-record JSON shows a flat
  `scores: {evidence, clarity, persuasive_force}` dict with no field indicating which text (A or
  B) each number scores — but Decision 5's own both-orders-swap-and-average arithmetic requires
  knowing exactly that, for every dimension independently.
- **Fix:** Nested `scores` as `{dimension: {condition: value}}` (documented in `aggregate()`'s own
  docstring as a refinement, not a paraphrase, of Decision 7). Every top-level field name Decision
  7 specifies is unchanged. A live judge-calling function is out of this plan's scope entirely
  (not in the plan's own "New classes and functions" artifact list) — `05-03` builds it and must
  match this nested shape.
- **Files modified:** `evals/benchmark/run_benchmark.py`
- **Verification:** `aggregate()`/`build_results_md()` self-test cases render a real report from
  24 committed fixture records using this shape.
- **Committed in:** `723137a` (Task 3)

---

**Total deviations:** 2 auto-fixed (2 plan-ambiguity resolutions, Rule 1). Neither changed any
task's stated `<done>` criterion or `<acceptance_criteria>`; both were necessary to make the
plan's own text internally consistent and implementable.
**Impact on plan:** No scope creep. Both resolutions are documented as decisions future plans
(`05-03`) must read before building on this file.

## Issues Encountered

None beyond the two deviations above.

## User Setup Required

None — no external service configuration required. This plan makes zero live model calls; the
`claude auth status` precondition only applies to `05-03`'s live matrix.

## Known Stubs

None. `run_generation()`/`run_matrix()` are complete, real code paths — not placeholders — proven
against committed fixtures with `subprocess.run` monkeypatched; they have simply never been
exercised against a real `claude` binary in this environment, by design (Task 1's own title:
"generated end to end and recorded — with the generation faked, not paid for"). The live matrix
invocation itself is explicitly out of this plan's scope (`05-03`'s to run, behind its own operator
checkpoint) — `main()`'s live-mode branch currently prints a message pointing to `05-03` and exits
1 rather than attempting a live run.

## Threat Flags

None beyond what `05-02-PLAN.md`'s own threat model already names and mitigates (T-05-06 through
T-05-12, T-05-SC) — this plan introduced no new network endpoint, auth path, or schema change
beyond what that threat model already covers. The stdlib-only-imports and no-`shell=True`
mitigations for T-05-06 are mechanically re-verified by this plan's own `<verify>` commands on
every task.

## Next Phase Readiness

- `evals/benchmark/run_benchmark.py` is ready for `05-03` to drive the real live matrix: call
  `run_matrix()` with real models/conditions/scenarios/repeats and a real `claude` binary, add the
  live judge-calling function (not built here — see Decisions), and run
  `python3 evals/benchmark/run_benchmark.py --report-only` to render the real
  `evals/benchmark/RESULTS.md` from the resulting committed raw records.
- `05-03` must emit judgement records with `scores` nested as `{dimension: {condition: value}}` per
  this plan's documented decision, not Decision 7's flat sketch, for `aggregate()` to read them
  correctly.
- EVAL-04 is the only requirement this plan could mark `Complete` — EVAL-05/09/10/11/12 are also
  declared by `05-03-PLAN.md`'s frontmatter and stay `Pending` under the shared-ID gate until
  `05-03` produces its own SUMMARY (`gsd_run query requirements.ready-ids` reported 1/6 ready;
  see `.planning/REQUIREMENTS.md`).
- Two new WINDOWS.md entries (ids 18-19) record this plan's disclosed unrun-verify items: the
  name-collision search for `bench-deal-brief.md`'s invented names, and the scenario-realism
  backstop truth — both mirror Phase 1's precedent and are not blockers to `05-03`.
- No blockers.

---
*Phase: 05-evaluation-harness*
*Completed: 2026-09-18*

## Self-Check: PASSED
