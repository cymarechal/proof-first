---
phase: 01-foundations-legal-scaffolding-numbering-shared-deal
plan: 02
subsystem: shared-example-data
tags: [markdown-registries, fictional-deal, canonical-figures, rfp]

# Dependency graph
requires:
  - phase: 01-01
    provides: "examples/deal-brief.md's frozen Canonical figures table format and its 6-key seed, plus tools/check_repo.py's unlisted-figure/dup-figure-key/figure-order checks"
provides:
  - "examples/deal-brief.md: the complete one-page fictional deal brief -- parties, estate/target platforms, people, pain points, timeline, inconvenient facts, and customer source material (scored RFP questions, discovery quotes, economic-buyer priorities, decision criteria, paper process)"
  - "Canonical figures table extended to 18 keys (19 rows including the table separator, which tools/check_repo.py's own key-order logic tolerates), all currency/percent/date values in prose traceable to a table row"
affects: [phase-2, phase-3, phase-4, phase-5, phase-6]

# Actuals (#2632)
actuals:
  tokens: 5200
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Canonical figure values may repeat across distinct keys without penalty -- tools/check_repo.py's unlisted-figure check matches against the SET of all table values, not per-key, so a per-question RFP weight can reuse an existing top-level weight's value (e.g. 20%) with no new row, or get its own row when no existing value matches."

key-files:
  created: []
  modified:
    - examples/deal-brief.md
    - .planning/WINDOWS.md

key-decisions:
  - "Renamed the 01-01-seeded key `rfp-technical-scoring-weight` to `rfp-technical-weight` (value unchanged at 55%) because Task 1's own verify script hard-codes that literal key name for the three-weight sum-to-100 check. Did not rename `total-contract-value` or `incumbent-share-of-estate` to the `deal-tcv`/`incumbent-estate-share` names the plan's artifacts_this_phase_produces section used, since neither the acceptance criteria nor the verify scripts reference those names -- that section's naming was aspirational/inconsistent with what 01-01 actually seeded, and read_first's \"don't restate seeded values under different names\" instruction governed the rest."
  - "Added two new Canonical figures rows (`rfp-question-weight-mid`=15%, `rfp-question-weight-top`=30%) so all five per-question RFP weights (30/20/15/15/20, summing to 100) resolve against the figures table -- two values (30%, 15%) had no existing match; the other three cells (20%, 20%, and none needing 55/25/62) reused the existing `rfp-security-weight` value of 20% with no new row, per the plan's explicit allowance to reuse a value that genuinely matches."
  - "Deal scale: Halverton Mutual (US mid-market insurance/retirement services), 3 bidders, $6,000,000/3-year contract, 850 VMs, 40 Oracle databases, RFP due 2026-10-30, 8-month examination window vs. Kestrel's own 14-month comparable-programme duration (deliberately the longer of the two, per D-08's inconvenient-facts requirement)."
  - "Both Task 2 <manual> reviewer checks (name-collision web search; no-comparative-claim read-through) could not be completed as specified -- this environment has no live network access for the web search, and no independent second reviewer was available. Logged both as open `unrun-verify` entries in .planning/WINDOWS.md (ids 1-2) rather than silently marking the plan complete without them; the executor performed a best-effort substitute for each (see Deviations)."

patterns-established: []

requirements-completed: [EX-01]

coverage:
  - id: D1
    description: "The deal spine (deal-in-one-paragraph, parties, estate/target platforms, people and roles, pain points, timeline) written into examples/deal-brief.md, with the Canonical figures table extended from 6 to 16 keys"
    requirement: "EX-01"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py"
        status: pass
      - kind: other
        ref: "row-count/order/dup-key check over '## Canonical figures' (>=16 rows, ascending, unique)"
        status: pass
      - kind: other
        ref: "rfp-technical-weight + rfp-commercial-weight + rfp-security-weight sum-to-100 check"
        status: pass
      - kind: other
        ref: "grep -c 'Halverton Mutual' examples/deal-brief.md"
        status: pass
    human_judgment: false
  - id: D2
    description: "Inconvenient facts section (unmeasured settlement-batch overrun, SOC 2 Type II gap, Priya Raghunathan's stated incumbent preference, examination window shorter than Kestrel's comparable-programme duration) and Customer source material (scored RFP Q1-Q5, discovery quotes incl. verbatim 'landing zone', economic-buyer priorities, decision criteria, paper process) written into examples/deal-brief.md"
    requirement: "EX-01"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py"
        status: pass
      - kind: other
        ref: "8-heading presence check"
        status: pass
      - kind: other
        ref: "Q1-Q5 weight sum-to-100 check"
        status: pass
      - kind: other
        ref: "grep -cF 'landing zone' examples/deal-brief.md"
        status: pass
    human_judgment: false
  - id: D3
    description: "The two <manual> reviewer checks in Task 2 (name-collision web search against the 9 invented names; a read-through confirming no sentence compares two real products or companies)"
    requirement: "EX-01"
    verification: []
    human_judgment: true
    rationale: "The name-collision check requires a live web search this environment cannot perform, and the no-comparison read-through is a semantic judgement the plan itself calls out as needing an independent human reviewer, not the executor who wrote the text. The executor performed a best-effort substitute for both (grep-assisted re-read for the comparison check; training-knowledge assessment for the name check) and logged both as open unrun-verify items in .planning/WINDOWS.md rather than treating the substitute as equivalent to the specified check."

# Metrics
duration: 24min
completed: 2026-09-10
status: complete
---

# Phase 1 Plan 2: Shared Deal Brief Summary

**Completed `examples/deal-brief.md`: the Halverton Mutual / Kestrel Systems Group cloud-migration RFP brief, with a full deal spine, four deliberately vendor-unfavorable facts, five scored RFP questions, and a Canonical figures table extended from 6 to 18 keys, all machine-verified against `tools/check_repo.py`.**

## Performance

- **Duration:** 24 min
- **Started:** 2026-09-10T06:35:42Z
- **Completed:** 2026-09-10T06:59:30Z
- **Tasks:** 2
- **Files modified:** 2 (`examples/deal-brief.md`, `.planning/WINDOWS.md`)

## Accomplishments
- Wrote the deal-in-one-paragraph, Parties, Estate and target platforms, People and roles, Pain points, and Timeline sections naming all four invented parties (Halverton Mutual, Kestrel Systems Group, Ardent Digital, Vantage Nine Consulting), all five invented people, and the real migration-source/target platform nouns (VMware vSphere, Oracle Database, Amazon EC2, Amazon Aurora PostgreSQL, AWS Control Tower)
- Extended the Canonical figures table from 6 to 18 keys — every currency amount, percentage, and ISO date in the brief's prose traces to an exact table row, machine-checked by `tools/check_repo.py`'s `unlisted-figure`/`dup-figure-key`/`figure-order` codes
- Wrote the Inconvenient facts section: an unmeasured settlement-batch overrun, a SOC 2 Type II certification gap, the technical evaluator's stated preference for the incumbent, and an examination window shorter than Kestrel's own comparable-programme duration — real material for Phase 2's six integrity requirements
- Wrote the Customer source material section in Halverton Mutual's own voice: five scored RFP questions (Q1-Q5, weights 30/20/15/15/20 summing to 100), four discovery-call quotes including a verbatim "landing zone" retention example, the economic buyer's stated priorities, a Decision criteria table mirroring the three top-level RFP weights, and the paper process (security/procurement/legal review sequence)

## Task Commits

Each task was committed atomically:

1. **Task 1: The deal spine — parties, estate, people, pain, timeline, and the complete figures table** - `99600ec` (feat)
2. **Task 2: Customer source material and the facts that are awkward for the vendor** - `e26e93b` (feat)

**Plan metadata:** committed alongside STATE.md/ROADMAP.md updates (next commit)

## Files Created/Modified
- `examples/deal-brief.md` — Complete fictional deal brief: deal spine, inconvenient facts, customer source material, and an 18-key Canonical figures table
- `.planning/WINDOWS.md` — Two `unrun-verify` entries recording the Task 2 `<manual>` checks that need an independent human reviewer with live web access

## Decisions Made

- **Key rename to satisfy Task 1's own verify script:** renamed 01-01's `rfp-technical-scoring-weight` to `rfp-technical-weight` (value unchanged, 55%), because Task 1's verify command hard-codes that literal key name in its three-weight sum-to-100 check. Did not rename `total-contract-value` or `incumbent-share-of-estate` to the `deal-tcv`/`incumbent-estate-share` names used in the plan's own `artifacts_this_phase_produces` section, since no acceptance criterion or verify script references those alternate names — that section's naming disagreed with what plan 01-01 actually seeded, and the rest of Task 1's `read_first` instruction ("does not restate them with different values") governed.
- **Two new Canonical figures rows added for the per-question RFP weights:** `rfp-question-weight-mid` (15%) and `rfp-question-weight-top` (30%). The other three per-question weight cells (20%, 20%, and the top-level weights) reuse existing table values rather than adding redundant rows, per the plan's explicit allowance ("acceptable only when the value genuinely matches").
- **Deal magnitudes:** $2,300,000 current annual run rate, 8-month regulatory examination window, 14-month vendor comparable-programme duration (deliberately longer than the examination window, per D-08), 850 VMs, 40 Oracle databases, 15/10 business-day security/legal review durations.
- **Both `<manual>` reviewer checks logged, not silently skipped:** this execution environment has no live network access and no second independent reviewer, so the plan's two `<manual>` verify steps (name-collision web search; no-real-product-comparison read-through) could not be completed as literally specified. Rather than mark them done or omit them, both were logged as open `unrun-verify` entries in `.planning/WINDOWS.md` and a best-effort substitute was performed for each (see Deviations).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Renamed a 01-01-seeded canonical figure key to match Task 1's verify script**
- **Found during:** Task 1 (writing the complete figures table)
- **Issue:** Plan 01-01 seeded `rfp-technical-scoring-weight`, but this plan's own Task 1 verify script requires the literal key `rfp-technical-weight` to compute the three-weight sum-to-100 check. Without the rename, that verify command would find zero matches for the key and fail.
- **Fix:** Renamed the key to `rfp-technical-weight`, keeping its value (55%) unchanged.
- **Files modified:** examples/deal-brief.md
- **Verification:** `python3 -c "...rfp-technical-weight...sum(w)==100"` exits 0 with `[55, 25, 20] 100`.
- **Committed in:** 99600ec (Task 1 commit)

**2. [Rule 3 - Blocking] Added two Canonical figures rows so all five per-question RFP weights resolve**
- **Found during:** Task 2 (writing the Scored RFP questions table)
- **Issue:** `tools/check_repo.py`'s `unlisted-figure` check flags any percentage in `examples/**/*.md` prose (including table cells) that has no matching Canonical figures value. Two of the five per-question weights (30%, 15%) had no existing match in the table.
- **Fix:** Added `rfp-question-weight-top` (30%) and `rfp-question-weight-mid` (15%) as new keyed rows, per the plan's explicit instruction to add per-question weights as their own keyed rows when no existing value matches.
- **Files modified:** examples/deal-brief.md
- **Verification:** `python3 tools/check_repo.py` exits 0 with `check_repo: 0 violations`; Q-weight sum check returns `[30, 20, 15, 15, 20] 100`.
- **Committed in:** e26e93b (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (both Rule 3 - blocking issues that would have failed the plan's own verify scripts without the fix)
**Impact on plan:** Both fixes were necessary to make the plan's own verify commands pass; no scope creep, no value changes to pre-existing seeded figures beyond the one key rename.

## Issues Encountered

- Task 2's two `<manual>` verify steps (a name-collision web search over the nine invented names, and an independent human read-through confirming no sentence compares two real products or companies) cannot be completed by this executor: there is no live network access in this environment, and the executor is not an independent reviewer of its own text. Resolution: performed a best-effort substitute for each (see Decisions), and logged both as open `unrun-verify` entries in `.planning/WINDOWS.md` (entry ids 1 and 2, phase `01`, file `examples/deal-brief.md`) so the gap is visible to `/gsd-ship`'s ledger gate rather than silently closed. A human with live web access should confirm before the repository goes public, per T-01-04 in the plan's threat register.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Phases 2-6 can now cite `examples/deal-brief.md`'s full cast, figures, inconvenient facts, and customer source material rather than re-deriving them: Phase 2's integrity rules have real material (SOC 2 gap, unmeasured overrun, incumbent-preferring evaluator, tight timeline) to fire on; Phase 3's artifact patterns can mirror the five scored RFP questions and the three top-level decision-criteria weights; Phase 5's benchmark scenario set is not drawn from an artificially favorable proving ground.
- `tools/check_repo.py` continues to pass in CI against the now-18-key Canonical figures table; any later phase adding `skills/`, `README.md`, or more `examples/` content is automatically checked against all nine violation codes.
- **Outstanding before the repository goes public:** the two logged `unrun-verify` items in `.planning/WINDOWS.md` (name-collision search; comparison read-through) need a human with live web access to close. This does not block Phase 1's own completion but should be resolved before Phase 6's legal review gate (LEG-04).
- No other blockers. The MEDDIC/MEDDICC trademark status noted in STATE.md remains open for Phase 6, unaffected by this plan.

---
*Phase: 01-foundations-legal-scaffolding-numbering-shared-deal*
*Completed: 2026-09-10*

## Self-Check: PASSED

`examples/deal-brief.md` and `.planning/WINDOWS.md` confirmed present on disk, plus this
SUMMARY.md itself. Both task commits (`99600ec`, `e26e93b`) confirmed present in `git log`.
Plan-level `<verification>` re-run: `check_repo.py --self-test` and live run both exit 0 with
no `FAIL`; Canonical figures table has 18 keyed rows (19 counting the header separator, which
`tools/check_repo.py`'s own key-order logic tolerates), sorted ascending, no duplicate key; all
eight Task 2 headings present; both `<manual>` reviewer checks recorded above as performed via
best-effort substitute and logged as open items in `.planning/WINDOWS.md` pending human
confirmation.
