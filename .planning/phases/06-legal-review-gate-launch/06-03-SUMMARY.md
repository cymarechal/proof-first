---
phase: 06-legal-review-gate-launch
plan: 03
subsystem: testing
tags: [check_repo, benchmark, mutation-testing, claims, readme, stdlib-python]

requires:
  - phase: 05-benchmark
    provides: "run_benchmark.py's judge_summary()/average_orders() paired path, build_results_md(), and the committed raw records under evals/benchmark/raw/"
  - phase: 06-legal-review-gate-launch
    provides: "06-02's passed legal review gate and the SOURCES_CHECK_CODES/MUTATIONS registration pattern the four new codes follow"
provides:
  - "Renderer-emitted pooled win/tie/loss per judged dimension, from the paired path, in evals/benchmark/RESULTS.md"
  - "Renderer-emitted per-cell direction count for the mechanical proxy table"
  - "A delimited claim region in README stating all three judged dimensions with equal prominence"
  - "readme-claim-unsourced, readme-claim-unanchored, readme-badge-unlisted, readme-layout-tree-stale"
affects: [06-04, LEG-05, launch decision]

actuals:
  tokens: 38000
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns:
    - "Claims live in a delimited region so a strict check has a bounded scope it can actually enforce"
    - "A published figure is emitted by the renderer and proven by a clean re-render diff, never typed"

key-files:
  created: []
  modified:
    - evals/benchmark/run_benchmark.py
    - evals/benchmark/RESULTS.md
    - README.md
    - tools/check_repo.py

key-decisions:
  - "The persuasive-force loss gets its own sentence in README, not a subordinate clause — a mixed result reported selectively is the failure this repository exists to prevent"
  - "The pooled total consumes judge_summary()'s paired output, with a self-test fixture built so the paired and per-order answers differ — otherwise the assertion could not detect WINDOWS.md id 20's defect"
  - "The direction count is a count, never a rate: 16 cells does not support a percentage"
  - "The 'trades persuasion for evidence' reading ships labelled as an untested hypothesis, with a pointer to the raw texts"
  - "Token sourcing is substring containment, declared as a ceiling — the check catches a number invented out of nothing, not provenance to the digit"

patterns-established:
  - "New self-test roots must be unioned into bad_codes so the every-code coverage loop sees them; roots that only fire codes on their own are invisible to it"

requirements-completed: [LEG-05]

coverage:
  - id: D1
    description: "RESULTS.md carries a renderer-emitted pooled win/tie/loss row per dimension — evidence 45/1/2, clarity 32/3/13, persuasive_force 7/3/38 — and a re-render leaves no diff"
    requirement: LEG-05
    verification:
      - kind: integration
        ref: "python3 evals/benchmark/run_benchmark.py --report-only && git diff --exit-code evals/benchmark/RESULTS.md — exits 0; pooled-value regex assertion matches all three rows"
        status: pass
    human_judgment: false
  - id: D2
    description: "The pooled totals come from the paired path, not from re-pooling per-order records, and equal the rendered per-cell table's own column sums"
    requirement: LEG-05
    verification:
      - kind: unit
        ref: "run_benchmark.py --self-test — pooled-totals-equal-per-cell-column-sums, pooled-uses-paired-path-not-per-order-pool, pooled-excludes-pair-missing-an-order"
        status: pass
      - kind: integration
        ref: "sibling probe with unmutated control: forcing a per-order-shaped tally turns all three assertions red, including the discrimination guard"
        status: pass
    human_judgment: false
  - id: D3
    description: "RESULTS.md carries a renderer-emitted direction count stating 8 lower, 1 equal, 7 higher, phrased as a count and not a rate; all four headings and all six caveats survive"
    requirement: LEG-05
    verification:
      - kind: unit
        ref: "run_benchmark.py --self-test — mechanical-direction-counts-sum-to-cells; heading/caveat presence assertion over the committed file"
        status: pass
    human_judgment: false
  - id: D4
    description: "README carries exactly one claim-region marker pair; the region states all three dimensions with their nine tallies, the direction count, and both travelling caveats; every region number is sourced and every numeric paragraph is anchored to a model version and a date"
    requirement: LEG-05
    verification:
      - kind: other
        ref: "marker-count/order assertion; region-content assertion; UNSOURCED and UNANCHORED assertions over evals/*/RESULTS*.md both empty"
        status: pass
    human_judgment: false
  - id: D5
    description: "README's layout tree names evals/routes/, the stale 'is Phase 6's work' sentence is gone, and README carries no images at all"
    verification:
      - kind: other
        ref: "TREE_OK True, STALE False, IMAGES [] assertion"
        status: pass
    human_judgment: false
  - id: D6
    description: "All four new codes fire on their defect and stay silent otherwise, are discrimination-proven against the real README, and the whole ten-command gate stays green"
    requirement: LEG-05
    verification:
      - kind: unit
        ref: "python3 tools/check_repo.py --self-test — nine fixture roots covering clean, unsourced, unanchored, unbalanced, no-marker, two-offender, allowed-badge, bad-badge and stale-tree"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py --mutation-test — 'mutation-test PASS: 56 codes discrimination-proven', CONTROL 0 violations, no FIRE-ONLY line; all ten CI commands exit 0"
        status: pass
      - kind: integration
        ref: "four sibling probes with unmutated control — disabling each code's firing branch turns its own assertions red with the expected messages"
        status: pass
    human_judgment: false
  - id: D7
    description: "README's claim region reads as an honest report of a mixed result rather than a selective one, no published claim outruns the evidence, and no Status sentence can be shown false by opening a file this repository ships"
    requirement: LEG-05
    verification: []
    human_judgment: true
    rationale: "All three are backstop truths in the plan's own must_haves. Whether a reader feels the unfavourable dimension was buried, and whether two passages entail a contradiction, are the judgement and entailment classes .planning/WINDOWS.md id 17 records as undetectable by anything in this stack. A cold human read is the only instrument."

duration: 47 min
completed: 2026-09-21
status: complete
---

# Phase 6 Plan 03: Publish What the Benchmark Supports Summary

**README now states that the judge preferred the un-skilled draft in 38 of 48 pairs, next to the evidence and clarity wins, in a delimited claim region where every number must trace to a committed record — 56 codes discrimination-proven**

## Performance

- **Duration:** 47 min
- **Started:** 2026-09-21T10:18:05Z
- **Completed:** 2026-09-21T11:05:22Z
- **Tasks:** 3
- **Files modified:** 4

## Accomplishments

- **The uncomfortable number is published, in its own sentence.** Pooled over 48 both-orders-averaged pairs: evidence 45 wins / 1 tie / 2 losses, clarity 32 / 3 / 13, persuasive force 7 / 3 / **38 losses**. README states all three with equal prominence and says plainly that the judge preferred the un-skilled draft in four pairs out of five, with the direction the same for both models.
- **The figures are computed, not typed.** `pooled_summary()` and `mechanical_directions()` emit them; `--report-only` regenerates `RESULTS.md`; the clean re-render diff is the proof. The plan predicted 45/1/2, 32/3/13, 7/3/38 and 8 lower / 1 equal / 7 higher from its own arithmetic, and the renderer produced exactly those independently.
- **The pooled total provably uses the paired path.** A self-test fixture is built so pairing-then-tallying and pooling-then-tallying give *different* answers — order 1 favours skill-on by 2, order 2 favours skill-off by 5, so the pair is one loss when averaged first and one win plus one loss when pooled per order. The assertion fails if the wrong path is taken, and fails separately if the fixture ever stops discriminating. `WINDOWS.md` id 20's defect cannot silently reach the figure README quotes.
- **A claim in README is now a checkable property.** `readme-claim-unsourced` fails the build on a region number that appears in no committed results file, and on a region whose markers are unbalanced — deleting the end marker is not a way around it. `readme-claim-unanchored` fails it on a numeric paragraph carrying no model version and no date.
- **Two future failure modes closed before they happened.** `readme-badge-unlisted` admits build status and license only, so no shields.io image can ever hang a number on this project that nobody measured. `readme-layout-tree-stale` catches the class that already shipped: `evals/routes/` existed on disk, was named twice in README prose, and was missing from the layout tree, because `readme-layout-legend-drift`'s own docstring says it never compared the tree to the filesystem.

## Task Commits

1. **Task 1: The renderer emits the pooled totals, from the paired path, recomputably** — `187c120` (feat)
2. **Task 2: README states the measured result — all three dimensions, equally** — `002e119` (docs)
3. **Task 3: Four codes that keep README honest after this plan ends** — `1b63ece` (feat)

## Files Created/Modified

- `evals/benchmark/run_benchmark.py` — `pooled_summary()` consuming `judge_summary()`'s paired output, `mechanical_directions()` over the cell means, both rendered by `build_results_md()`; four new self-test cases (`pooled-totals-equal-per-cell-column-sums`, `pooled-excludes-pair-missing-an-order`, `pooled-uses-paired-path-not-per-order-pool`, `mechanical-direction-counts-sum-to-cells`).
- `evals/benchmark/RESULTS.md` — regenerated. Ten added lines: the direction-count sentence inside `## Mechanical proxy counts`, and the pooled table inside `## Judged persuasion`. Not hand-edited at any point.
- `README.md` — `## Status` rewritten. "What exists today" now names `evals/lint.py`, both benchmark files and both routes files; "What does not exist yet" replaced with what genuinely does not exist (no human evaluation, no non-Anthropic model, no persuasion claim); the claim region added; the superseded "deciding what this README states … is Phase 6's work" paragraph retired; `evals/routes/` added to the layout tree.
- `tools/check_repo.py` — the frozen claim-region markers, numeric-token regex, model strings, source glob, badge allow-list and layout-scan constants; `_claim_region()`, `_claim_numeric_tokens()` and four `check_readme_*` functions dispatched from the existing `run_readme_checks()`; four `MUTATIONS` entries against the real README; nine self-test fixture roots with their assertions; four docstring entries with declared ceilings.

## Decisions Made

- **The loss is a sentence, not a clause.** The plan's behaviour contract required it and the reason is the project's own standard: a document that reports two favourable dimensions and tucks the third into a qualifier is exactly the writing this skill exists to make impossible.
- **Caveats follow the number, never soften it.** README states 38 losses, then states that it is one language model's rating against a rubric, that no human evaluator scored any text, and that the skill-off arm received a materially shorter prompt. In that order.
- **The interpretation ships labelled.** "The skill trades persuasive framing for evidence density" is plausible and untested. It appears as an untested hypothesis with `evals/benchmark/raw/` named as where a reader can judge for themselves.
- **Substring sourcing, declared.** `48` is sourced by any file containing `1948`. Tightening this would need token boundaries the results files do not consistently provide, and the check's job is to catch a fabricated number, not to certify provenance — the pointer to the results file does that.
- **`readme-claim-unanchored` stays silent on an unbalanced region.** `readme-claim-unsourced` reports that condition, so one broken region produces one violation rather than two reports of the same fact.

## Deviations from Plan

None - plan executed exactly as written.

One structural discovery changed how the self-test was wired, inside the plan's own instructions:

- New known-bad fixture roots are invisible to the every-code coverage loop unless they are unioned into `bad_codes`. `bad_root` itself ships no `README.md`, so no `readme-*` code has ever fired on it; the seven existing ones are covered through that union. The four new roots were added to it, and a note recording the mechanism is in this SUMMARY's `patterns-established`.

## Issues Encountered

**Two probe passes were needed to prove the assertions live.** The first `sed` probes targeted the wrong indentation and silently changed nothing, producing no failures — which reads identical to "the assertion is dead". The control caught it: an unmutated sibling passed and the mutated one also passed, which is the signature of a probe that did not apply rather than an assertion that does not fire. Re-running at the correct indentation turned both claim-region assertions red with their expected messages. All six probes (four codes plus the two benchmark paths) were finally verified against a green control.

**`REPO_ROOT` is derived from `__file__`,** so probe copies must sit inside the repository at the real depth. Probes were written into `tools/` and `evals/benchmark/`, run, and removed; `git status` confirmed only the intended files remained modified.

## Measurements

| Metric | At HEAD (pre-phase) | After 06-01 | After 06-02 | After 06-03 |
|---|---|---|---|---|
| Codes discrimination-proven | 49 | 50 | 52 | **56** |
| `--mutation-test` wall time | 8.1 s | 9.6 s | 9.9 s | **10.1 s** |
| `check_repo.py` lines | ~7,065 | 7,382 | 7,862 | 8,377 |
| `RESULTS.md` lines | 211 | — | — | 221 |
| README lines | 287 | — | — | 341 |

Wall time is still far under the 60-second remedy trigger 05-03 set, and growth per added code is flat rather than compounding.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **LEG-05 is satisfied and enforced.** Every number README publishes traces to a committed record, states its model versions and its date, and is checked on every CI run.
- **06-04 inherits a README that cannot quietly acquire an unsourced claim.** The launch decision it makes is now the only remaining gate.
- **The claim region is the seam to extend.** Any future measured claim goes inside it, or it is not checked. That is stated in README itself, so a contributor reading only README learns the rule.
- **Carried from 06-02 and still open for 06-04**, which owns `.planning/WINDOWS.md`: ids 3, 6 and 18 dispositioned; id 1 to note the re-run that found a collision; and two new entries for the `Ardent Digital` and `Gina Almeida` rename decisions.
- **One thing no check here can do:** `WINDOWS.md` id 17's entailment class. Nothing detects that two README passages contradict each other. 06-04's cold human read is the only instrument for it, and it is the backstop truth on this plan too.

---
*Phase: 06-legal-review-gate-launch*
*Completed: 2026-09-21*
