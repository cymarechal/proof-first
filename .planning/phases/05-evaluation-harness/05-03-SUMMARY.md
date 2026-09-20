---
phase: 05-evaluation-harness
plan: 03
subsystem: testing
tags: [benchmark, judge, live-matrix, claude-code-cli, pairwise-judging, honest-reporting]

requires:
  - phase: 05-evaluation-harness
    provides: "05-02's offline aggregator/renderer (load_raw_records(), aggregate(),
      build_results_md(), generate_report(), the RESULTS_SECTION_HEADINGS/REQUIRED_CAVEATS
      drift-guard machinery) — this plan extends it with a judge and spends real money running
      it against a live matrix"
provides:
  - "The blind pairwise judge (build_judge_prompt(), run_judgement(), average_orders(),
    judge_summary()): label-stripped prompt, both orders averaged per dimension, ties kept as
    ties, unscoreable replies excluded rather than defaulted — proven offline with every call
    faked before one dollar was spent"
  - "192 committed raw records under evals/benchmark/raw/ (96 generations, 96 judgements) from
    one authorised full-matrix live run — the first and only paid invocation this phase makes"
  - "evals/benchmark/RESULTS.md, generated only by --report-only from those 192 records, byte-
    identical on re-render, carrying six named caveats (the sixth, judge construct validity,
    added by this continuation to close a Decision 8 item-5 gap the orchestrator's review found)"
  - "The measured, unflattering finding: the skill wins decisively on evidence, wins moderately
    on clarity, and LOSES on persuasive_force against this LLM judge, while mechanical proxy
    counts are close to a wash — reported straight, with no conclusion drawn beyond the data"
affects: [06-publication-and-launch]

actuals:
  tokens: 173655
  tasks: 3
  commits: 4

tech-stack:
  added: []
  patterns:
    - "Sixth-caveat drift guard: REQUIRED_CAVEATS/CAVEAT_TEXT extended by one key
      ('judge construct validity'); build_results_md()'s per-caveat self-test loop iterates the
      constant, so the new key is automatically covered by the existing drift guard with zero
      new test-writing — only the fixture-render case's name needed updating since it no longer
      states a fixed caveat count"
    - "Never hand-edit a generated report: the item-5 gap was closed in the renderer
      (run_benchmark.py), then RESULTS.md was regenerated via --report-only and the re-render
      diff checked clean — exactly the mechanism EVAL-10/EVAL-11 exist to enforce"

key-files:
  created:
    - evals/benchmark/raw/*.json (192 files: 96 generation records, 96 judgement records)
    - evals/benchmark/RESULTS.md
  modified:
    - evals/benchmark/run_benchmark.py (blind pairwise judge added by the prior agent; this
      continuation added the sixth REQUIRED_CAVEATS/CAVEAT_TEXT key and renamed the
      fixture-render self-test case)

key-decisions:
  - "Closed Decision 8 item 5 (no LLM-judge-as-buyer-proxy disclosure) by adding a sixth named
    caveat to the module constant the drift-guard self-test already checks, rather than hand-
    editing RESULTS.md — a hand edit is exactly what the re-render diff exists to catch."
  - "Reported the judged-persuasion loss (skill loses 7/3/38 win/tie/loss on persuasive_force)
    as the measured finding with no softening, per this repository's 'measured claims or no
    claims' constraint. This is material to Phase 6's LEG-05 README claims: they cannot cite a
    persuasion improvement this run did not find."
  - "Recorded $18.21 as the GENERATION cost only, not the run total — the 96 judgement records
    carry no cost_usd/usage fields (run_judgement() does not record them), so the judge pass's
    dollar cost is unrecorded and unrecoverable from committed data. Named as a Task 1
    judgement-record schema gap rather than estimated and presented as measured."

requirements-completed: [EVAL-05, EVAL-06, EVAL-07, EVAL-08, EVAL-09, EVAL-10, EVAL-11, EVAL-12]

coverage:
  - id: D1
    description: "Blind pairwise judge built and self-tested offline (label-stripping, both
      orders averaged, ties kept, unscoreable replies excluded) before any live spend"
    requirement: EVAL-07
    verification:
      - kind: unit
        ref: "python3 evals/benchmark/run_benchmark.py --self-test"
        status: pass
    human_judgment: false
  - id: D2
    description: "192 raw records (96 generations, 96 judgements) committed under
      evals/benchmark/raw/, at least three scoreable generations per (model, scenario,
      condition) cell"
    requirement: EVAL-11
    verification:
      - kind: other
        ref: "python3 -c \"import glob;n=len(glob.glob('evals/benchmark/raw/*.json'));j=len(glob.glob('evals/benchmark/raw/*__judge__*.json'));print(n,j)\" -> 192 96"
        status: pass
    human_judgment: false
  - id: D3
    description: "RESULTS.md generated only by --report-only, re-render byte-identical to the
      committed file (git diff --exit-code clean), carrying both figure sections and all six
      named caveats including the judge-construct-validity disclosure this continuation added"
    requirement: EVAL-09
    verification:
      - kind: other
        ref: "python3 evals/benchmark/run_benchmark.py --report-only && git diff --exit-code evals/benchmark/RESULTS.md"
        status: pass
    human_judgment: false
  - id: D4
    description: "Human read of RESULTS.md against 05-RESEARCH.md Decision 8's six named
      overclaims, confirming each is absent (anchored headline, no cross-provider claim, linter
      count not a verdict, no false statistical precision, judge-as-buyer-proxy disclosed, no
      composite figure)"
    requirement: EVAL-10
    verification: []
    human_judgment: true
    rationale: "Reading published prose for overclaims against a named checklist is a semantic
      judgment call, not something a grep-based check can certify — the orchestrator performed
      this read directly (see Deviations) and this continuation closed the one gap it found."
  - id: D5
    description: "check_repo.py --mutation-test wall time measured with evals/benchmark/raw/
      committed (192 files), confirming it still stays well under the 60s threshold that would
      require excluding raw/ from the mutation-test copy"
    requirement: EVAL-12
    verification:
      - kind: other
        ref: "time python3 tools/check_repo.py --mutation-test -> 4.989s total, 'mutation-test PASS: 48 codes discrimination-proven'"
        status: pass
    human_judgment: false

duration: 3d (05-03 spans 2026-09-18 09:58 UTC live run through this continuation's 2026-09-20 close; this continuation's own work was under 15 minutes of tool time)
completed: 2026-09-20
status: complete
---

# Phase 05 Plan 03: Live Benchmark Matrix and Blind Pairwise Judge Summary

**192 committed raw records from one authorised $18.21+ live matrix run, judged blind and pairwise by claude-opus-5 — the skill wins decisively on evidence and moderately on clarity, but LOSES on the persuasive_force dimension itself, a result reported straight per this repo's "measured claims or no claims" standard.**

## Performance

- **Duration:** This continuation's own work (regenerate report, run gates, write SUMMARY) took under 15 minutes of tool time. The plan's live matrix itself ran ≈72 minutes of wall-clock against a ≈58-minute estimate (see Deviations/Issues for the interruption).
- **Started (this continuation):** 2026-09-20 (session start)
- **Completed:** 2026-09-20
- **Tasks:** 3/3 (Task 1 judge, Task 2 checkpoint authorised full-matrix, Task 3 live run + this continuation's item-5 fix)
- **Files modified (this continuation):** 2 (`evals/benchmark/run_benchmark.py`, `evals/benchmark/RESULTS.md`)

## Accomplishments

- The blind pairwise judge (`build_judge_prompt`, `run_judgement`, `average_orders`,
  `judge_summary`) was built and proven offline in Task 1, with every failure mode faked before
  any live call: label-stripping, both-orders averaging, tie handling, unscoreable exclusion.
- The full matrix (8 scenarios × 2 models × 3 repeats × 2 conditions = 96 generations, plus 96
  judge calls for 48 pairs in both orders) was authorised at the Task 2 checkpoint and run once
  live. All 192 raw records are committed under `evals/benchmark/raw/`.
- `evals/benchmark/RESULTS.md` was generated from those records, reviewed against
  `05-RESEARCH.md` Decision 8's six named overclaim risks, and found to have one real gap: no
  statement that the judge score is an LLM proxy for a technical evaluator's reaction, not a
  measurement of real buyer behaviour. This continuation closed that gap by adding a sixth key
  (`judge construct validity`) to `REQUIRED_CAVEATS`/`CAVEAT_TEXT`, regenerated the report, and
  confirmed the re-render diff is clean.
- All seven gate commands pass with `evals/benchmark/raw/` committed (192 files), including a
  measured `--mutation-test` wall time of 4.989s — well under the 60s threshold that would have
  required excluding `raw/` from the mutation-test copy.

## Task Commits

Committed by the prior (stalled) agent, verified present in `git log` by this continuation:

1. **Task 1: The blind pairwise judge, built and proven with every call faked** - `8957280` (feat)
2. **Task 3 (CLI wiring): wire the live matrix CLI entry point** - `4449764` (feat)
3. **Task 3 (raw records): commit live benchmark matrix raw records** - `22faaab` (feat)

Committed by this continuation:

4. **Task 3 (close-out fix): add judge construct validity caveat to close Decision 8 item 5** - `ac14c74` (fix)

**Plan metadata:** this SUMMARY's own commit (docs, follows below)

## Files Created/Modified

- `evals/benchmark/raw/*.json` (192 files, committed by the prior agent) - one generation or
  judgement record per file; the only source `RESULTS.md`'s figures are permitted to recompute
  from
- `evals/benchmark/RESULTS.md` (created by this continuation's `--report-only` regeneration) -
  the published report: two never-blended figure sections plus six named caveats
- `evals/benchmark/run_benchmark.py` (modified by this continuation) - added the
  `judge construct validity` key to `REQUIRED_CAVEATS`/`CAVEAT_TEXT` and renamed the
  fixture-render self-test case from `...-five-caveats-...` to `...-all-caveats-...` since it
  no longer states a fixed count

## Decisions Made

- **Renderer fix, not a hand edit.** The Decision 8 item-5 gap (no judge-as-buyer-proxy
  disclosure) was closed by adding a sixth key to `REQUIRED_CAVEATS`/`CAVEAT_TEXT` in
  `run_benchmark.py`, inheriting the existing per-caveat drift-guard self-test automatically
  (it iterates the constant), then regenerating `RESULTS.md` via `--report-only`. `RESULTS.md`
  was never hand-edited — the re-render diff exists precisely to catch that class of defect.
- **Report the loss.** Judged persuasion aggregate (24 cells per dimension, skill-on vs
  skill-off): `evidence` wins 45 / ties 1 / losses 2; `clarity` wins 32 / ties 3 / losses 13;
  `persuasive_force` wins 7 / ties 3 / **losses 38**. Mechanical proxy counts (16 model/scenario
  pairs): skill-on has fewer violations in 8, more in 7, equal in 1; summed mean violations
  skill-off 131.3 vs skill-on 119.6 — close to a wash. This LLM judge rates the skill's output
  LESS persuasive on the exact dimension the skill is named for, while the skill makes writing
  markedly more evidence-dense and somewhat clearer. No conclusion is drawn beyond what these
  numbers show. This is material to Phase 6's LEG-05 README claims, which cannot cite a
  persuasion improvement this run did not find.
- **$18.21 is the generation cost only, not the run total.** Summed `cost_usd` across the 96
  generation records = $18.21. The 96 judgement records carry no `cost_usd` and no populated
  `usage` — `run_judgement()` does not record them — so the judge pass's dollar cost is
  unrecorded and unrecoverable from the committed data. This is named here as a gap in Task 1's
  judgement-record schema, not estimated and presented as measured. An authorised estimate for
  comparison purposes only: ≈$48 total (generation + judge), which would put judge cost at
  roughly $30 against the $18.21 generation figure — not a measurement.
- **Wall clock and the interruption, disclosed per the MOD-04 precedent.** First invocation
  started 2026-09-18T09:58:11Z and exited 2026-09-18T10:58:19Z having written 164 records (96
  generations + 68 judgements), zero error records, zero unscoreable records — its parent shell
  was reaped, so the process died with the shell. This is NOT the usage-limit signature the plan
  warned about; it is a harness/process-lifecycle interruption. 28 opus judgements were
  outstanding: `rfp-rfi-2` repeats 1-2 in both orders, and all of `solution-proposal-1`,
  `solution-proposal-2`, `demo-discovery-1`, `demo-discovery-2`. The run was resumed detached at
  ~11:00Z; existing cells were skipped and NOT re-paid for (the skip-if-exists resumability
  Task 2's checkpoint named as a risk-lowering fact); the run completed ~11:10Z with all 192
  records. Total wall clock ≈72 minutes against the ≈58-minute estimate. Every record produced
  by the interrupted first invocation was kept, exactly as the MOD-04 precedent
  (`evals/conformance/RESULTS-mod04.md`) kept its own contaminated 20-session run rather than
  deleting it.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug, carried forward from Task 1] `JUDGE_SCHEMA` nests scores under `text_a`/
`text_b` rather than as a flat top-level 3-key object**
- **Found during:** Task 1 (the prior agent's work, documented here for completeness since this
  SUMMARY closes the whole plan)
- **Issue:** `05-RESEARCH.md` Decision 7's worked example sketches a flat `{dimension: value}`
  shape, which cannot say which anonymous text (A or B) a given score belongs to — Decision 5's
  both-orders-average-per-dimension arithmetic requires knowing that.
- **Fix:** `JUDGE_SCHEMA` nests the three dimension keys under `text_a`/`text_b`, so one judge
  call scores both anonymous texts at once (96 judge calls = 48 pairs × 2 orders, matching the
  plan's own cost arithmetic).
- **Files modified:** `evals/benchmark/run_benchmark.py`
- **Committed in:** `8957280` (Task 1 commit, prior agent)

**2. [Rule 1/2 - This continuation's own fix] Missing Decision 8 item-5 disclosure**
- **Found during:** Task 3 close-out — orchestrator review of the generated `RESULTS.md` against
  `05-RESEARCH.md` Decision 8's six named overclaims found item 5 unaddressed: no statement that
  the judge is an LLM proxy for a technical evaluator's reaction, not a measurement of real
  buyer behaviour.
- **Fix:** Added a sixth key (`judge construct validity`) to `REQUIRED_CAVEATS`/`CAVEAT_TEXT`,
  covered automatically by the existing per-caveat drift-guard self-test loop, then regenerated
  `RESULTS.md` via `--report-only` (never hand-edited). Renamed the fixture-render self-test
  case since its old name (`...-five-caveats-...`) stated a caveat count that was no longer
  true.
- **Files modified:** `evals/benchmark/run_benchmark.py`, `evals/benchmark/RESULTS.md`
- **Verification:** `python3 evals/benchmark/run_benchmark.py --self-test` exits 0 and names
  `results-render-fixture-two-headings-all-caveats-byte-identical` and `per-caveat-drift-guard`
  among cases exercised; `git diff --exit-code evals/benchmark/RESULTS.md` clean after
  re-render.
- **Committed in:** `ac14c74`

---

**Total deviations:** 2 (1 carried forward from Task 1 documentation, 1 this continuation's own
fix). **Impact on plan:** the item-5 fix was necessary to satisfy EVAL-10's overclaim-avoidance
requirement; no scope creep, no live model call made.

## Issues Encountered

- The prior agent's session stalled after committing the raw records and generating an
  UNTRACKED `RESULTS.md`, leaving the plan one gap short of Task 3's `<verify>` human-check
  criterion. This continuation was scoped narrowly to that one gap plus the closing paperwork,
  per the dispatching orchestrator's brief — no re-run of any live model call, no re-reading of
  the full 210-line `RESULTS.md` (the orchestrator's review, reproduced verbatim in this
  SUMMARY's Decisions section, was trusted rather than re-derived).
- `run_judgement()`'s missing `cost_usd`/`usage` fields (see Decisions) mean the judge pass's
  true dollar cost cannot be recovered after the fact. This is disclosed rather than patched
  retroactively, since patching would require inventing a number the committed records do not
  contain.

## Gate Commands (real output)

```
$ python3 evals/benchmark/run_benchmark.py --self-test
self-test PASS - fake-envelope cases exercised: duplicate-id, missing-family, unknown-family,
empty-scenarios-file, success, skip-if-exists, non-zero-exit, is-error, array-envelope,
committed-fixture-schema, no-vocabulary-leakage, no-entity-collision, family-coverage-positive,
family-coverage-negative, cell-enumeration-96, run-matrix-skip-if-exists,
run-matrix-durability-on-interruption, judge-prompt-label-stripping, judge-scored,
judge-skip-if-exists, judge-missing-dimension-unscoreable,
judge-reply-validation-out-of-range-non-integer-unparseable, judge-non-zero-exit,
run-judge-matrix-catches-session-failed, run-judge-matrix-skips-missing-generation-pair,
average-orders-identical-and-missing-order, judge-summary-tie-and-excluded-pair,
committed-judgement-fixture-schema, load-raw-records-empty-file,
load-raw-records-unparseable-file, load-raw-records-sorted-order, generate-report-empty-dir,
aggregate-below-3-repeats-reports-actual-n, win-tie-loss-rows-shuffle-invariant,
results-render-fixture-two-headings-all-caveats-byte-identical, per-caveat-drift-guard,
report-only-no-subprocess-call, self-test-never-writes-real-results-path

$ python3 evals/benchmark/run_benchmark.py --report-only
wrote /Users/cymarechal/devoteam/devoteam/technical-presales/evals/benchmark/RESULTS.md (15307 chars)

$ git diff --exit-code evals/benchmark/RESULTS.md
(no output, exit 0 — clean)

$ python3 tools/check_repo.py
check_repo: 0 violations

$ python3 tools/check_repo.py --self-test
self-test PASS - verified violation codes: artifact-family-section-missing,
before-after-citation-missing, before-after-family-missing, before-after-spelled-count,
catalog-count-mismatch, catalog-count-unstated, catalog-id-drift, catalog-opening-rule-count,
derivative-rule-coverage-incomplete, dup-figure-key, dup-id, example-rule-narration,
example-sentence-length, figure-order, framework-statement-missing,
frontmatter-description-invalid, frontmatter-name-mismatch, frontmatter-unknown-key,
frontmatter-unparseable, license-missing, mc-catalog-id-drift, mc-count-mismatch,
mc-count-unstated, mc-rule-in-skill, plugin-manifest-invalid, plugin-manifest-version-mismatch,
pointer-duplicated, pointer-missing, pointer-unparseable, publish-location-drift, range-id,
readme-before-after-order, readme-example-drift, readme-example-lead-distance,
readme-install-path-missing, readme-layout-legend-drift,
readme-output-style-destination-missing, readme-results-pointer-missing,
results-breakdown-count-mismatch, revived-id, skill-derivative-stale,
skill-family-line-gate-missing, skill-family-order-gate-missing, skill-token-budget-exceeded,
skill-too-long, source-label-in-skill-content, undefined-id, unlisted-figure

$ python3 tools/check_repo.py --mutation-test
mutation-test PASS: 48 codes discrimination-proven
real  0m4.989s (measured via `time`; compare to ~1s pre-phase and 2.2s after Task 1)

$ python3 evals/conformance/run_conformance.py --self-test
self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable

$ python3 tools/generate_derivatives.py --check
(no output, exit 0)

$ python3 evals/lint.py --self-test
The deletion test -- whether removing a term changes a sentence's technical meaning -- is a
semantic judgment this linter does not perform. A violation count from this module is a count
of mechanical proxies for that judgment, not a compliance verdict on a document.
self-test PASS - verified violation codes: buzzword-term, claim-without-adjacent-number,
proxy-term-source-invalid, proxy-term-source-is-internal, proxy-term-unsourced,
sentence-over-ceiling, unbounded-modal, unquantified-superlative
```

`python3 tools/check_repo.py --mutation-test` wall time with `evals/benchmark/raw/` committed
(192 files): **4.989s total** (`time` output: `0m1.03s user 0m3.88s system 98% cpu 0m4.989s
total`). This compares to the ~1s figure measured before this phase's files existed
(`05-03-PLAN.md`'s Interfaces table) and stays well under the 60s threshold `05-03-PLAN.md`
names as the trigger for excluding `evals/benchmark/raw` from `_copy_repo_subset()` — no
exclusion was needed.

## Known Stubs

None — every figure in `RESULTS.md` recomputes from committed `raw/` records; no placeholder or
mock data was introduced.

## Threat Flags

None beyond what `05-03-PLAN.md`'s own threat model already registers (T-05-13 through T-05-19,
T-05-SC) — this continuation touched only the caveats-rendering path, which is covered by
T-05-15 (a published figure with no committed record behind it) via the re-render diff check.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Phase 6 (Publication and Launch) can now draft LEG-05 README claims against real measured
  numbers — but the measured finding does NOT support a persuasion-improvement claim on the
  `persuasive_force` dimension (7 wins / 3 ties / 38 losses against skill-off). Phase 6 must
  either cite the evidence and clarity wins honestly, disclose the persuasion result as-is, or
  investigate the judge rubric / skill further before drafting any headline persuasion claim.
- `evals/benchmark/raw/`, `evals/benchmark/RESULTS.md`, and `evals/benchmark/run_benchmark.py`
  are all committed and self-tested; no further live spend is required to read or re-verify this
  phase's numbers.
- Every one of the 32 (model, scenario, condition) cells holds exactly 3 scoreable generations —
  the ≥3 floor EVAL-06 requires is met everywhere with NO margin. A future re-run with any
  additional exclusion would drop a cell below the floor; this fragility is worth naming for
  whoever plans a follow-up measurement.

---
*Phase: 05-evaluation-harness*
*Completed: 2026-09-20*

## Self-Check: PASSED

- FOUND: evals/benchmark/RESULTS.md
- FOUND: evals/benchmark/run_benchmark.py
- FOUND: .planning/phases/05-evaluation-harness/05-03-SUMMARY.md
- FOUND commit: 8957280
- FOUND commit: 4449764
- FOUND commit: 22faaab
- FOUND commit: ac14c74
- Raw record count: 192 total, 96 judgement records (matches D2 claim)

## Post-verification fix (2026-09-20)

**Defect (05-REVIEW.md CR-01, Critical):** `generate_report()` fell through to
`datetime.datetime.now(datetime.timezone.utc).date().isoformat()` for `as_of_date` whenever the
caller did not pass one explicitly — which is every real invocation, since `main()`'s
`--report-only` path never passes one. This is a live clock read in a path this phase's own
EVAL-11/EVAL-12 acceptance criteria require to be a pure function of the committed
`evals/benchmark/raw/` records.

**This had already published a false measurement date in the committed artifact.** The
committed `RESULTS.md` headline read `Measured 2026-09-20 across claude-opus-5, claude-sonnet-5
(96 generations recorded)`, but every one of the 192 records in `evals/benchmark/raw/` carries a
`timestamp` between `2026-09-18T09:58:22Z` and `2026-09-18T11:10:18Z` — the matrix ran on
2026-09-18. A `--report-only` re-render performed after midnight UTC on 2026-09-20 silently moved
the headline two days forward. This broke 05-RESEARCH.md Decision 8 item 1 (the headline must
carry the run date, not the render date), narrowed the plan's re-render acceptance criterion to
"clean only within a single UTC day" rather than a durable proof, and violated the EVAL-11/EVAL-12
pure-function requirement for `--report-only`.

**Fix:** Added `_as_of_date_from_records()`, which derives `as_of_date` from the generation
records' own `timestamp` fields (excluding judgement records) — the single shared date if every
generation shares one UTC date, or an explicit `'{earliest} to {latest}'` span if the run crosses
a UTC-date boundary, never a silently-collapsed single day. `generate_report()`'s default now
calls this instead of reading the clock; the explicit `as_of_date=` parameter is unchanged, so the
existing fixture self-tests that pass `as_of_date='2026-09-18'` explicitly keep passing untouched.
No `datetime.datetime.now()` call remains anywhere in the render path (`load_raw_records` →
`aggregate` → `judge_summary` → `build_results_md`).

**New self-test (`cr01-report-only-render-is-clock-independent`):** monkey-patches the module's
`datetime.datetime` class to two different fake "current" dates (2099-01-01 and 2000-06-15,
chosen far from any real date to make a regression unmissable) and renders the same committed
`results-render` fixture records under each. Asserts (1) the two renders are byte-identical, (2)
neither fake clock date appears anywhere in the output, and (3) the headline correctly reads the
fixture records' own date, `Measured 2026-09-18`. This is the exact reproduction of the shipped
defect — a clock read where a data-derived value belongs — and would have failed before the fix.

**Corrected headline:** `evals/benchmark/RESULTS.md` was regenerated via
`python3 evals/benchmark/run_benchmark.py --report-only` (never hand-edited) and now reads:

    Measured 2026-09-18 across claude-opus-5, claude-sonnet-5 (96 generations recorded).

A repeat `--report-only` run reproduces this byte-for-byte (`git diff --exit-code
evals/benchmark/RESULTS.md` is clean), including across the real calendar-day boundary this
defect crossed — the acceptance criterion is now a durable proof, not a same-day coincidence.

**Gates re-run, all pass:** `tools/check_repo.py` (0 violations), `tools/check_repo.py
--self-test` (48 codes verified), `tools/check_repo.py --mutation-test` (48 codes
discrimination-proven), `evals/conformance/run_conformance.py --self-test` (4 verdicts
discriminated), `tools/generate_derivatives.py --check` (clean), `evals/lint.py --self-test` (8
codes verified), `evals/benchmark/run_benchmark.py --self-test` (38 cases, including the new
clock-independence case).

**Scope:** This fix addresses CR-01 only. CR-02 (unpaired judgement-order pooling), CR-03
(missing effort/judge-model in the record key), CR-04 (silent missing-cell gap in the mechanical
table), and the Warnings from 05-REVIEW.md are explicitly out of scope here and are tracked in
`.planning/WINDOWS.md` (entries 20–23) for separate remediation.
