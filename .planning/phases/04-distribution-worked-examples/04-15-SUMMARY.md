---
phase: 04-distribution-worked-examples
plan: 15
subsystem: testing
tags: [eval-harness, claude-code-cli, output-styles, system-prompt, benchmark, stdlib-python]

requires:
  - phase: 05-evaluation-harness
    provides: "run_benchmark.py's proven shapes for driving isolated headless `claude -p` sessions and scoring them offline — skip-if-exists resumability, SessionFailedError, the unscoreable path, the content-addressed artifact SHA, and the clock-independent renderer"
  - phase: 03-conformance
    provides: "run_conformance.py's score_transcript(), reused unchanged as the family-line scorer for all three arms"
  - phase: 04-distribution-worked-examples
    provides: "tools/generate_derivatives.py and the two derivatives whose preamble this plan makes true"
provides:
  - "evals/routes/run_routes.py — a stdlib-only route-equivalence runner with --self-test, --probe, live matrix and --report-only modes"
  - "evals/routes/probe/ — 4 committed activation-probe records proving each route switches on against an unrouted control"
  - "evals/routes/raw/ — 36 committed generation records, the reduced matrix authorised at the spend checkpoint"
  - "evals/routes/RESULTS-routes.md — the published null result, recomputable from those records with one command"
  - "derivative-comparison-claim-stale — the 49th violation code, binding the derivative preamble to whether the measurement exists"
  - "A measured answer to Phase 4's only unanswered success criterion, replacing a four-round-stale `blocked — deferred by design`"
affects: [phase-06, LEG-04, CAT-10, distribution-routes, DIST-03, DIST-04, DIST-05]

actuals:
  tokens: 103000
  tasks: 4
  commits: 6

tech-stack:
  added: []
  patterns:
    - "Activation probe before matrix spend: prove every arm is switched on against an unrouted control, with a coded session cap and a defined refusal branch, before authorising the paid run"
    - "Two-sided conjunction violation code: three fixture roots rather than two, because a code that fires on `A and B` needs a fixture for `A without B` to prove it is not a presence-only check"
    - "Spend checkpoint re-priced from probe records rather than from the plan's estimate"

key-files:
  created:
    - "evals/routes/run_routes.py"
    - "evals/routes/RESULTS-routes.md"
    - "evals/routes/probe/ (4 records)"
    - "evals/routes/raw/ (36 records)"
  modified:
    - "tools/generate_derivatives.py"
    - "tools/check_repo.py"
    - "output-styles/proof-first.md"
    - "prompts/system-prompt.md"
    - ".github/workflows/ci.yml"
    - "README.md"
    - ".planning/WINDOWS.md"
    - ".planning/phases/04-distribution-worked-examples/COVERAGE.md"
    - ".planning/phases/04-distribution-worked-examples/04-UAT.md"

key-decisions:
  - "Published the null result as a null result. Every pair of arms overlaps on the mechanical proxy count, so the report says the measurement did not distinguish the routes and refuses the word `equivalent`. The distinction between those two statements is enforced in code: separation_verdict() will only assert separation on non-overlapping observed ranges."
  - "Ran the activation probe before the matrix, and kept its records. Whether a headless session honours a project-scoped output style was UNVERIFIED in this environment at plan time. It does, on the first form tried. The two fallback forms were never needed and the docstring says they are therefore unproven rather than implying otherwise."
  - "Re-priced the spend checkpoint from the probe's own records instead of the plan's estimate. The plan quoted $10.25 full / $5.10 reduced from one Phase 5 sample; the probe showed prompt-on at $0.49/session, putting the real figures at ~$20 / ~$10. The operator authorised against the corrected numbers. The matrix then came in at $5.35 because the probe's prompt-on session was itself an outlier — the estimate was wrong in both directions and the records are what settle it."
  - "Registered the 49th code rather than refusing it. Unlike the cross-sentence contradiction code 04-14 refused, this is a literal-substring presence conjunction with a stated ceiling, and the sentence it guards has independent reader value: a reader meeting `No benchmark has compared` has no way to tell whether it is still true."
  - "Counted UAT test 2 as measured_inconclusive, not passed. The test expected a positive equivalence finding; the records support the absence of a detected difference. Marking it passed would be the CR-01 overstatement again."
  - "Corrected the report after a cold read, in the renderer rather than the file. Two figures were misreadable: skill-on's highest mean (which pools 3 never-activated sessions) and style-on's 12/12 conformant against 11/12 activated (which is not an arithmetic error). Both now carry the sentence that prevents the misreading."

patterns-established:
  - "Stale-blocker detection: a deferral records WHY it is blocked, and nothing re-reads that reason when the dependency lands. G-04-9's root cause is exactly this, and it survived four gap-closure rounds with a green gate."
  - "Arms that are not a level playing field are reported as such, not averaged. The skill-on arm must pass a trigger the other two do not have, so a null result between them is partly a statement about trigger behaviour."

requirements-completed: []

coverage:
  - id: D1
    description: "A stdlib-only route-equivalence runner whose self-test proves per-route session setup, the record schema, all four unscoreable paths, temp-dir removal, skip-if-exists resumability, the aggregator and a clock-independent renderer — offline, on a machine with no `claude` binary"
    requirement: "DIST-05"
    verification:
      - kind: unit
        ref: "python3 evals/routes/run_routes.py --self-test (21 cases)"
        status: pass
      - kind: unit
        ref: "env PATH=/usr/bin:/bin python3 evals/routes/run_routes.py --self-test"
        status: pass
      - kind: automated_ui
        ref: "AST import scan against the declared stdlib set — EXTRA_IMPORTS []"
        status: pass
    human_judgment: false
  - id: D2
    description: "Every published route arm proven switched on against an unrouted control run on the same scenario, with the probe's own records committed"
    requirement: "DIST-03"
    verification:
      - kind: e2e
        ref: "evals/routes/probe/ — 4 live sessions; control activated=false/no-family, all three routes activated=true"
        status: pass
    human_judgment: false
  - id: D3
    description: "A 36-session route-equivalence measurement whose every figure recomputes from committed records with one offline command"
    requirement: "DIST-04"
    verification:
      - kind: e2e
        ref: "evals/routes/raw/ — 36 records, 0 unscoreable, per-scenario prompt/model/effort equality asserted across arms"
        status: pass
      - kind: integration
        ref: "python3 evals/routes/run_routes.py --report-only && git diff --exit-code evals/routes/RESULTS-routes.md"
        status: pass
    human_judgment: false
  - id: D4
    description: "The generated derivative preamble states what was measured and points at the records, and a violation code fails the build if the stale denial returns while the results file exists"
    requirement: "DIST-05"
    verification:
      - kind: unit
        ref: "python3 tools/check_repo.py --mutation-test — 49 codes discrimination-proven, CONTROL 0 unexpected, no FIRE-ONLY"
        status: pass
      - kind: unit
        ref: "python3 tools/generate_derivatives.py --check (exit 0 — both derivatives are generator output)"
        status: pass
    human_judgment: false
  - id: D5
    description: "The equivalence verdict published is no stronger than the records support, and the caveats are not contradicted elsewhere in the file"
    verification: []
    human_judgment: true
    rationale: "Whether a published verdict overstates its evidence is a judgment about prose against tables, not a property any check in this repository can assert. A cold read was performed and produced two corrections (commit 8a14222); a second, independent cold read by someone who has not seen this plan is the honest bar and has not happened."

duration: 95min
completed: 2026-09-21
status: complete
---

# Phase 4 Plan 15: Route Equivalence Measured Summary

**The output style, the pasted system prompt and the installed skill folder were compared head to head for the first time across 36 live sessions, and the honest finding is that this measurement could not tell them apart — published as exactly that, not as equivalence.**

## Performance

- **Duration:** ~95 min (including ~40 min of live-session wall-clock)
- **Tasks:** 4 of 4 (one a blocking spend checkpoint)
- **Files created/modified:** 51 (45 of them committed measurement records)
- **Live sessions driven:** 40 (4 probe + 36 matrix), $6.34 total

## Accomplishments

- **Answered Phase 4's only unanswered success criterion.** Roadmap criterion 3 — turn the discipline on as an output style or paste it as a system prompt "and get equivalent behavior either way" — had read `blocked — deferred by design` since the phase began, on the ground that it waited on Phase 5. Phase 5 completed on 2026-09-18. The premise expired and the item did not notice, surviving four gap-closure rounds with a green gate. G-04-9 records that root cause.
- **Proved the output-style route works at all.** Whether a headless `claude -p` session honours a project-scoped output style was UNVERIFIED in this environment; two earlier probes had failed for unrelated reasons. It does, on the first activation form tried. The unrouted control cited zero rule markers where all three routes cited them.
- **Published a null result rather than manufacturing a finding.** skill-on 7.9 [1–14], style-on 7.1 [3–11], prompt-on 6.3 [1–10]. Every pair overlaps. The report says the measurement did not distinguish the routes and names the difference between that and equivalence.
- **Found the asymmetry that actually matters for choosing a route.** style-on reached the artifact-family line in 12 of 12 sessions and activated in 11 of 12; skill-on activated in only 9 of 12, because it must first be triggered. The unconditionally-on routes are not handicapped the way the installed skill is. This is CAT-10's residual landing inside a different measurement, and it is disclosed on the arm that carries it.
- **Made the repository's own documentation true again.** The derivative preamble stopped denying a comparison that now exists; README's routes 3 and 4 state what was and was not observed; COVERAGE.md stopped claiming this phase calls no external service when it now drives 40 live sessions.

## Task Commits

1. **Task 1: the runner and its self-test** — `3097563` (feat)
2. **Task 2: activation probe against an unrouted control** — `f9e597d` (test)
3. **Task 3: spend checkpoint** — resolved `reduced-matrix` by the operator, re-priced from Task 2's records
4. **Task 4A/4B: matrix and report** — `93d3697` (feat)
5. **Task 4C/4D: preamble made true, 49th code registered** — `c579b82` (fix)
6. **Task 4E: README, COVERAGE, ledger, UAT** — `db12d46` (docs)
7. **Cold-read corrections to the report** — `8a14222` (docs)

## Files Created/Modified

- `evals/routes/run_routes.py` — the runner: three route setups, activation detection, unscoreable handling, aggregator, renderer, 21 self-test cases
- `evals/routes/probe/` — 4 activation-probe records including the unrouted control
- `evals/routes/raw/` — 36 matrix records, every one committed including any that had failed
- `evals/routes/RESULTS-routes.md` — written only by `--report-only`; hand-editing it is caught by the re-render diff
- `tools/generate_derivatives.py` — `_render_preamble()` and its docstring
- `tools/check_repo.py` — `derivative-comparison-claim-stale`, three fixture roots, one mutation
- `.github/workflows/ci.yml` — the tenth command
- `README.md`, `.planning/WINDOWS.md`, `COVERAGE.md`, `04-UAT.md` — made true against the finding

## Decisions Made

See `key-decisions` in the frontmatter. The load-bearing one: `separation_verdict()` will only assert a difference between arms on non-overlapping observed ranges, so the refusal to say "equivalent" on overlapping data is enforced by code rather than by the author's restraint at writing time.

## Deviations from Plan

### 1. The spend checkpoint was re-priced before being presented

- **Found during:** Task 3
- **Issue:** The plan's cost figures ($10.25 full / $5.10 reduced) were multiplied out from a single committed Phase 5 `skill-on` record at $0.142/session. The probe showed `prompt-on` at $0.494/session, because the whole system prompt rides every call. The real figures were ~$20 / ~$10.
- **Fix:** Presented the checkpoint with figures recomputed from Task 2's own records alongside the plan's, so the authorisation was given against measured numbers.
- **Outcome:** Reduced matrix authorised; it then cost $5.35, because the probe's single `prompt-on` session was itself an outlier. Both estimates were wrong; the 36 records are what settle it.

### 2. A sixth required caveat was added to the renderer

- **Found during:** Task 4B
- **Issue:** Task 3's `reduced-matrix` option states that with one scenario per family "the report must say so." The plan's five required caveats did not include it.
- **Fix:** Added `scenario coverage` to `REQUIRED_CAVEATS` and `CAVEAT_TEXT`, so the renderer emits it and the self-test's missing-caveat guard covers it.

### 3. The plan's `has not been observed here` grep was unsatisfiable

- **Found during:** Task 4E
- **Issue:** Acceptance required `grep -cF 'has not been observed here' README.md` to print `1`. It printed `0` at HEAD, before any edit: the sentence is line-wrapped in README as `has not\nbeen observed here`, so the flat-string grep never matched it. The criterion was mis-measured at plan time.
- **Fix:** Verified the criterion's intent instead — that the negotiated `/config` disclosure survives untouched. Confirmed two ways: the README diff contains no `+`/`-` line touching that sentence, and a whitespace-normalised count of the phrase is exactly 1.

### 4. Two cold-read corrections to the report

- **Found during:** Task 4's `<human-check>`
- **Issue:** `skill-on` shows the highest mean proxy count, which a reader would take as "the installed skill writes worst" — when that arm pools 3 sessions in which the skill never activated. Separately, `style-on` shows 12/12 conformant against 11/12 activated, which reads as an arithmetic error but is not.
- **Fix:** Both explained in `build_routes_results_md()` so the explanation is generator output, not a hand edit. Committed `8a14222`. No figure changed.

---

**Total deviations:** 4 — 1 checkpoint re-pricing, 2 additive corrections to the report, 1 plan-measurement error worked around with the criterion's intent verified.

## What this plan did NOT close

- **The null result's four limits** — trigger asymmetry between arms, one scenario per family, the headless proxy for route 4, and n=3 on one model. All four cost sessions to close, not code. `.planning/WINDOWS.md` entry 28.
- **DIST-03, DIST-04, DIST-05** stay unchecked in REQUIREMENTS.md. The requirement marks are the verifier's to move; this plan recorded a measurement.
- **The interactive `/config` picker** (entry 16) and **the publish-location placeholder** (entry 11) are untouched and stay routed to Phase 6's LEG-04.
