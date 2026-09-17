---
phase: 04-distribution-worked-examples
plan: 02
subsystem: worked-examples
tags: [ex-02, check_repo, mutation-test, examples, artifact-family]

requires:
  - phase: 01-legal-scaffolding-numbering-deal-brief
    provides: examples/deal-brief.md's 18-row Canonical figures table and the People/Pain
      points/Customer source material this plan's four pairs are grounded in
  - phase: 03-completeness-audit-artifact-patterns
    provides: the frozen ARTIFACT_FAMILY_SECTIONS tuple and each family's Order convention in
      references/artifact-patterns.md
  - phase: 04-distribution-worked-examples
    provides: 04-01's established three-part contract (check function, self-test fixture pair,
      MUTATIONS entry) this plan's two new codes follow exactly
provides:
  - examples/before-after.md — one document-level before/after pair per artifact family, frozen
    order, every after column citing an allocated rule ID
  - Two new check_repo.py violation codes (before-after-family-missing,
    before-after-citation-missing) making family coverage, pair completeness, family order, and
    citation presence build failures rather than conventions
affects: [04-04-readme-and-install-docs]

actuals:
  tokens: 6492
  tasks: 2
  commits: 3

tech-stack:
  added: []
  patterns:
    - "Reused ARTIFACT_FAMILY_SECTIONS (declared once in tools/check_repo.py) rather than a second
      typed copy — before-after-family-missing imports the same frozen tuple
      artifact-family-section-missing already binds to"
    - "Section-presence + pair-completeness + order-comparison folded into one check function
      (before_after_family_missing) over one parsed document, per plan decision P4-10 — mirrors the
      existing pointer-unparseable precedent of one code covering more than one structural condition"
    - "TDD RED/GREEN split within a single-file checker: RED commit adds self-test scaffolding and
      explicit assertions with no implementation, confirmed failing for the right reason
      (python3 tools/check_repo.py --self-test exits 1 with exactly the three expected FAIL lines
      and no unrelated errors); GREEN commit implements both checks, wiring, docstring bullets, and
      MUTATIONS entries"

key-files:
  created:
    - examples/before-after.md
  modified:
    - tools/check_repo.py

key-decisions:
  - "Split the plan's single combined bad-fixture description into two self-test roots
    (beforeafter_bad_root for the three co-occurring conditions — missing heading, section missing
    its ✓ half, section with no rule token — and beforeafter_order_bad_root, isolated, for the
    heading-order condition alone). The check's own action text gates the ordering comparison on
    'while all four are present'; combining a missing-heading fixture with a heading-order swap in
    one file is structurally impossible under that guard, so a literal single-fixture reading would
    have been unimplementable. This is an implementation-detail resolution of an already fully
    specified check (same class as 04-01's publish-location-drift owner-segment normalization), not
    a new architectural surface — documented here rather than escalated as Rule 4."

requirements-completed: [EX-02]

coverage:
  - id: D1
    description: "Four document-level before/after pairs exist under the four frozen family
      headings, in the frozen order, each after column citing at least one allocated PF-/MC- rule
      ID, every figure in the file traceable to the Canonical figures table"
    requirement: EX-02
    verification:
      - kind: unit
        ref: "tools/check_repo.py --self-test (before-after-family-missing, before-after-citation-missing fixtures)"
        status: pass
      - kind: integration
        ref: "tools/check_repo.py --mutation-test (before-after-family-missing, before-after-citation-missing mutations against the real file)"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py (live run against the real repo)"
        status: pass
    human_judgment: false
  - id: D2
    description: "A missing family heading, a half-written pair (missing ✗ or ✓ half), a reordered
      family sequence, and an uncited family section are each a CI-enforced build failure rather
      than a convention"
    requirement: EX-02
    verification:
      - kind: unit
        ref: "tools/check_repo.py --mutation-test (37 codes discrimination-proven, up from 35; CONTROL 0 unexpected; 0 FIRE-ONLY)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Each pair's after column demonstrates the rewrite the cited rule asks for, rather
      than restating the rule's own wording back to the reader, and each before column is a
      recognisable real-draft failure rather than a caricature"
    verification: []
    human_judgment: true
    rationale: "Content-quality correctness is a semantic judgment no file-reading checker in this
      stack performs — the plan itself authors this as a verification: backstop truth so the
      verifier abstains rather than silently passing. Harvested into end-of-phase UAT per
      workflow.human_verify_mode: end-of-phase, matching 04-01's precedent for its own
      human_judgment-true deliverable (D4)."

duration: ~55min
completed: 2026-09-17
status: complete
---

# Phase 4 Plan 2: Worked Before/After Examples and Their Enforcement Summary

**`examples/before-after.md` ships one document-level before/after pair per artifact family, each
after column citing real rule IDs grounded in the shared deal brief, made mechanical by two new
`check_repo.py` codes proven live by a TDD RED/GREEN split — discrimination-proven total moved from
35 to 37, CONTROL still clean, no code FIRE-ONLY.**

## Performance

- **Duration:** ~55 min
- **Started:** 2026-09-17T06:25:00Z (approx, following 04-01's session handoff)
- **Completed:** 2026-09-17T07:24:38Z
- **Tasks:** 2
- **Files modified:** 2 (1 created, 1 modified)

## Accomplishments

- Created `examples/before-after.md`: one whole-passage before/after pair for each of the four
  frozen artifact families (RFP and RFI response, Solution proposal, Executive summary, Demo and
  discovery material), in the frozen order, every fact grounded in `examples/deal-brief.md` (the
  850-VM/40-Oracle-instance estate, the 6-hour settlement-batch window, the SOC 2 Type I/II gap, the
  8-month examination window against the 14-month comparable programme, Marcus Feld's and Diane
  Osoria's own discovery-call words, and the Q1 30% scored-question weight), and every after column
  citing at least one of the 39 allocated rule IDs (`PF-2.1`, `MC-11`, `PF-1.9`, `PF-2.14`,
  `PF-2.17`, `PF-0.1`, `PF-1.25`, `PF-2.11`, `PF-3.3`, `MC-31`).
- Added `before-after-family-missing`: one check folding three structural conditions over a single
  parse — missing family heading, a present family section missing its ✗ or ✓ half, and (only once
  all four headings are present) the four headings appearing out of `ARTIFACT_FAMILY_SECTIONS`'
  own order — per plan decision P4-10, mirroring `pointer-unparseable`'s precedent of one code
  covering more than one structural condition.
- Added `before-after-citation-missing`: each present family section must carry at least one
  `PF-#.#` or `MC-#` token, reusing `check_undefined_id`'s token shapes rather than a third copy.
- Both codes reuse `ARTIFACT_FAMILY_SECTIONS` (declared once, imported, never redeclared) and are
  wired into a new `EXAMPLE_CHECK_CODES`/`run_example_checks` pair, folded into `ALL_CHECK_CODES`
  and `run_all_checks` exactly as `04-01` wired `PLUGIN_CHECK_CODES`/`run_plugin_checks`.
- Executed as a genuine TDD RED/GREEN cycle: the RED commit adds three self-test scratch roots
  (`beforeafter_good_root`, `beforeafter_bad_root`, `beforeafter_order_bad_root`) and explicit
  assertions with no implementation behind them — `python3 tools/check_repo.py --self-test` exits 1
  with exactly the three expected `FAIL` lines and nothing else, confirming the test fails for the
  right reason. The GREEN commit implements both checks, the docstring bullets, and two `MUTATIONS`
  entries (delete a family heading; strip every rule token from one section), turning the same
  self-test suite fully green and the mutation-test's discrimination-proven total from 35 to 37.

## Task Commits

1. **Task 1: Author `examples/before-after.md`** - `add2907` (feat)
2. **Task 2 RED: Add failing self-test for before-after family/citation checks** - `18cc361` (test)
3. **Task 2 GREEN: Implement `before-after-family-missing` and `before-after-citation-missing`** - `96e8b26` (feat)

**Plan metadata:** committed alongside this SUMMARY.

## Files Created/Modified

- `examples/before-after.md` - Four document-level before/after pairs, one per frozen artifact
  family, every after column citing an allocated rule ID
- `tools/check_repo.py` - `BEFORE_AFTER_PATH` constant, `check_before_after_families`,
  `check_before_after_citations`, `EXAMPLE_CHECK_CODES`, `run_example_checks`, two docstring
  bullets, two self-test fixture-generator functions plus three scratch roots and their assertions,
  two `MUTATIONS` entries and their mutate functions

## Decisions Made

See `key-decisions` in frontmatter — the single-vs-two-fixture-root split for the self-test suite,
required by the ordering check's own "only once all four are present" guard.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1-adjacent, documented not escalated] Split the plan's single combined bad-fixture into
two isolated self-test roots**
- **Found during:** Task 2 RED phase, designing `beforeafter_bad_root`
- **Issue:** The plan's fixture-design note describes one bad root combining a missing heading, a
  missing pair-half, a heading-order swap, and a missing citation. The check's own action text
  gates the order comparison on "while all four are present" — a fixture missing one heading
  entirely cannot simultaneously demonstrate the order-swap condition, since the guard suppresses
  the order check whenever fewer than four headings are present. A literal single-fixture reading
  was internally inconsistent with the check's own specified behavior.
- **Fix:** Split into `beforeafter_bad_root` (the three co-occurring conditions: missing heading,
  missing ✓ half, missing citation) and `beforeafter_order_bad_root` (all four headings present,
  fully compliant otherwise, two swapped relative to the frozen order) — isolating the order
  condition the way `family_order_bad_root`/`family_bad_root` already isolate sibling gates
  elsewhere in this file.
- **Files modified:** `tools/check_repo.py`
- **Verification:** All five `<behavior>` scenarios from the plan's task 2 are exercised across the
  two fixtures; `python3 tools/check_repo.py --self-test` passes with both codes in the verified
  list.
- **Committed in:** `18cc361` (RED commit), `96e8b26` (GREEN commit)

---

**Total deviations:** 1 (implementation-detail fixture-design resolution, forced by the check's own
declared ordering guard). **Impact on plan:** No scope change — every `<behavior>` scenario the
plan specifies is still tested, split across two isolated roots rather than one combined root. No
requirement or acceptance criterion was altered.

## Issues Encountered

None — every plan-level `<verify>` and `<acceptance_criteria>` command ran and passed exactly as
written, including the scratch-copy mutation proof script.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- EX-02's structural half is fully CI-enforced: family coverage, pair completeness, family order,
  and citation presence are all build failures.
- **EX-02's content-quality half is unverified by any check in this repository** — whether each
  after column genuinely demonstrates the cited rule's rewrite rather than restating the rule's own
  wording, and whether each before column is a recognisable real-draft failure rather than a
  caricature, is a semantic judgment provisional pending end-of-phase UAT (see `must_haves.truths`'
  `verification: backstop` entry and coverage item D3 above).
- `skills/proof-first/SKILL.md` and `skills/proof-first/references/worked-examples.md` are
  byte-identical to their state before this plan (verified via `git diff --stat` across all three
  of this plan's commits showing no change to either path) — SKILL.md's token margin remains
  available for `04-03`.
- `examples/` now holds exactly `deal-brief.md` and `before-after.md`, matching the plan's own
  verification requirement.
- Ready for `04-03`.

## Self-Check: PASSED

- `[ -f examples/before-after.md ]` → FOUND
- `git log --oneline --all | grep -q add2907` → FOUND
- `git log --oneline --all | grep -q 18cc361` → FOUND
- `git log --oneline --all | grep -q 96e8b26` → FOUND
- `python3 tools/check_repo.py` → `check_repo: 0 violations`
- `python3 tools/check_repo.py --self-test` → PASS, verified codes include both
  `before-after-family-missing` and `before-after-citation-missing`
- `python3 tools/check_repo.py --mutation-test` → `mutation-test PASS: 37 codes
  discrimination-proven`, CONTROL `0 violations ... (0 known-open ..., 0 unexpected)`, 0 FIRE-ONLY
  lines
- Re-ran every plan-level `<acceptance_criteria>` script from both tasks: all pass, including the
  scratch-copy mutation proof and the docstring-bullet-count script

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-17*
</content>
