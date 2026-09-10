---
phase: 01-foundations-legal-scaffolding-numbering-shared-deal
plan: 03
subsystem: legal-scaffolding
tags: [mit-license, trademark-notice, attribution, sources-registry]

# Dependency graph
requires:
  - phase: 01-01
    provides: "NOTICES.md's frozen title, orienting sentence, and attribution-pointer fenced block (must not be disturbed); tools/check_repo.py's pointer-missing/pointer-duplicated checks"
provides:
  - "LICENSE: unmodified root MIT license text, copyright line 'Proof First contributors'"
  - "NOTICES.md: '## Scope of this file' (precedence, no-trademark-grant, coverage-default, notice-before-content sentences) and '## Framework statements' with three individually named, fixed-order, five-element subsections for Command of the Message, the MEDDIC/MEDDICC family (contested ownership, no single holder), and Challenger"
  - "SOURCES.md: the operative reproduction-boundary rule, the paraphrase/reproduction definition with its one mechanically-checked string (the attribution pointer), three source tables (message articulation, qualification checklist, commercial teaching), and the out-of-bounds list"
affects: [01-04, phase-2, phase-3, phase-6]

# Actuals (#2632)
actuals:
  tokens: 3100
  tasks: 3
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Legal-instrument separation of concerns: LICENSE carries only unmodified MIT text; every non-grant sentence (precedence, non-affiliation, paraphrase boundary, sourcing rule) lives in NOTICES.md or SOURCES.md instead, so a tool or reader diffing LICENSE never sees drift."
    - "Honest-unverified-over-fabricated-citation: every SOURCES.md row is marked unverified with 'to confirm at LEG-04' rather than asserting a checked location this environment could not actually open (no live network access), mirroring 01-02's unrun-verify handling in .planning/WINDOWS.md."

key-files:
  created:
    - LICENSE
    - SOURCES.md
  modified:
    - NOTICES.md

key-decisions:
  - "All six SOURCES.md rows marked `unverified` (Where: 'to confirm at LEG-04') rather than `confirmed`, because this execution environment has no live network access to actually open a public location and confirm it resolves to the named source — matching planner_assumption A-05's own framing that source confirmation is deliberately manual and this executor cannot perform that read. Titles named (Force Management's public materials on Command of the Message; Andy Whyte's MEDDICC book and a MEDDIC-family public overview page; Dixon/Adamson's 'The Challenger Sale' and 'The Challenger Customer') are recorded as candidate sources for Phase 6's LEG-04 reviewer to open and check, not as verified citations."
  - "MEDDIC-family NOTICES.md statement records ownership as claimed by multiple parties and contested, per D-13 and the standing STATE.md blocker, with an explicit line that a ruling on one spelling (MEDDPICC, per PITFALLS.md:71) is not treated as covering another (MEDDIC/MEDDICC)."
  - "Closing sentence added after the three framework statements stating that none positions this project as a version, implementation, edition, or automation of any named framework — this is the sentence the Task 2 manual reviewer check specifically looked for and is a direct answer to PITFALLS.md:66-93's nominative-fair-use warning."

patterns-established:
  - "A public notices file states a review date per framework subsection (`Last reviewed:`), not once for the whole file — a future correction to one framework's status does not force a diff-noise touch to the other two."

requirements-completed: [LEG-01, LEG-02, LEG-03]

coverage:
  - id: D1
    description: "LICENSE (unmodified MIT text) and NOTICES.md's '## Scope of this file' section (precedence, no-trademark-grant, coverage-default, notice-before-content sentences) written; attribution-pointer block left byte-for-byte undisturbed"
    requirement: "LEG-01"
    verification:
      - kind: other
        ref: "head -1 LICENSE == 'MIT License'; grep -cF 'Copyright (c) 2026 Proof First contributors' LICENSE == 1; find . -maxdepth 2 -name 'LICENSE*' | wc -l == 1"
        status: pass
      - kind: other
        ref: "python3 -c \"...need=['## Scope of this file','grants no rights in any third-party trademark','unless a file states otherwise']...\" == no missing"
        status: pass
      - kind: other
        ref: "grep -cF 'Concepts here are paraphrased from publicly described sales frameworks.' NOTICES.md == 1"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "NOTICES.md '## Framework statements' section: three fixed-order, individually named subsections (Command of the Message / MEDDIC-family / Challenger), each with Mark, Rights-holder, Non-affiliation, Paraphrase boundary, and Last reviewed date; MEDDIC-family records contested multi-party ownership with no single holder and no claim on mark validity or proceeding outcomes"
    requirement: "LEG-02"
    verification:
      - kind: other
        ref: "python3 -c \"...heading order == ['Command of the Message','MEDDIC, MEDDICC, and related marks','Challenger']...\""
        status: pass
      - kind: other
        ref: "python3 -c \"...each subsection carries all 5 labelled elements...\" == incomplete: []"
        status: pass
      - kind: other
        ref: "grep -cF 'claimed by multiple parties' NOTICES.md; grep -cF 'Force Management'; grep -cF 'Challenger Inc.'; grep -c 'Last reviewed:' >= 3; grep -cF 'not affiliated with' >= 3"
        status: pass
      - kind: manual_procedural
        ref: "Reviewer read-through of NOTICES.md end to end, recorded below"
        status: pass
    human_judgment: false
  - id: D3
    description: "SOURCES.md: the operative rule, the paraphrase/reproduction boundary (naming the attribution pointer as the one mechanically-checked string and LEG-04 as owner of the semantic judgement), three source tables with 2 rows each (6 total, all honestly unverified), and the out-of-bounds list"
    requirement: "LEG-03"
    verification:
      - kind: other
        ref: "python3 -c \"...need=[6 headings + 'Last reviewed:'+'LEG-04'+'training-portal'+'no tool in this project']...\" == missing: []"
        status: pass
      - kind: other
        ref: "grep -E '^#{1,6} ' SOURCES.md | grep -cE 'Command of the Message|MEDDIC|Challenger' == 0"
        status: pass
      - kind: other
        ref: "python3 -c \"...6 status-bearing rows; 0 unverified rows carrying http...\""
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py"
        status: pass
      - kind: manual_procedural
        ref: "Reviewer attempt to open each 'confirmed' row's location — vacuously satisfied, all 6 rows are unverified by design"
        status: pass
    human_judgment: false

# Metrics
duration: 12min
completed: 2026-09-10
status: complete
---

# Phase 1 Plan 3: Legal Scaffolding Summary

**Unmodified MIT `LICENSE`, a `NOTICES.md` scope section separating the copyright grant from the trademark position, three individually named and fixed-order framework statements (Force Management / contested MEDDIC family / Challenger Inc.), and a `SOURCES.md` reproduction boundary with six honestly-unverified candidate source rows for Phase 6's LEG-04 gate.**

## Performance

- **Duration:** 12 min
- **Started:** 2026-09-10T07:05:00Z (approx.)
- **Completed:** 2026-09-10T07:17:00Z
- **Tasks:** 3
- **Files modified:** 3 (`LICENSE` created, `NOTICES.md` extended, `SOURCES.md` created)

## Accomplishments
- Shipped an unmodified MIT `LICENSE` at the repository root, and drew the exact scope line between it and `NOTICES.md` in a new `## Scope of this file` section — precedence sentence, no-trademark-grant sentence, coverage-default sentence, and a sentence stating notices ship before the content they cover
- Wrote three separately named, fixed-order framework statements into `NOTICES.md` (`## Framework statements`), each carrying the same five labelled elements (Mark, Rights-holder, Non-affiliation, Paraphrase boundary, Last reviewed), with the MEDDIC/MEDDICC/MEDDPICC family recorded as contested multi-party ownership rather than attributed to one holder, and a closing sentence ruling out version/implementation/edition/automation framing for all three
- Created `SOURCES.md` at the repository root: the operative sourcing rule, an honest definition of the paraphrase/reproduction boundary (naming the one mechanically-checked string — the attribution pointer — and Phase 6's LEG-04 gate as the owner of everything else), three per-framework source tables with two candidate rows each, and the out-of-bounds list
- Left the frozen `NOTICES.md` attribution-pointer fenced block byte-for-byte untouched throughout all three tasks, confirmed by grep count staying at exactly 1 after every edit

## Task Commits

Each task was committed atomically:

1. **Task 1: MIT license and the scope boundary between copyright and trademark** - `94b1674` (feat)
2. **Task 2: Three separately named framework statements** - `fcd15de` (feat)
3. **Task 3: The approved-source list and the reproduction boundary** - `0ba93f8` (feat)

**Plan metadata:** committed alongside STATE.md/ROADMAP.md updates (next commit)

## Files Created/Modified
- `LICENSE` - Unmodified MIT license text, copyright line "Proof First contributors"
- `NOTICES.md` - Added `## Scope of this file` and `## Framework statements` (three subsections); attribution-pointer block from 01-01 left untouched
- `SOURCES.md` - New: the sourcing rule, the reproduction-boundary definition, three source tables, and the out-of-bounds list

## Decisions Made

- **`Last reviewed:` dates written into `NOTICES.md`:** all three framework subsections carry `2026-09-10` — Command of the Message, the MEDDIC/MEDDICC family, and Challenger.
- **`SOURCES.md` confirmed-vs-unverified count:** 0 `confirmed` rows, 6 `unverified` rows (2 per source table). This execution environment has no live network access to actually open and check a public location, so every candidate source — including well-known, high-confidence titles such as "The Challenger Sale" (Dixon & Adamson) and "MEDDICC" (Andy Whyte) — is recorded as `unverified` with `Where: to confirm at LEG-04` rather than asserted as checked. This mirrors 01-02's handling of its own unreachable `<manual>` checks (logged, not silently marked done) and is the more honest posture than marking rows `confirmed` on training-knowledge confidence alone.
- **Outcome of all three reviewer checks:**
  1. Task 2's manual read-through of `NOTICES.md` (no version/implementation/edition/automation framing anywhere; no assertion or denial of mark validity or proceeding outcome) — **performed and passed**, recorded above and in the Deviations section below.
  2. Task 3's manual check ("a reviewer opens each `confirmed` row's location and confirms it resolves") — **vacuously satisfied**: no row in `SOURCES.md` is `confirmed`, so there is no location to open. Phase 6's LEG-04 gate is the first point at which any row can move from `unverified` to `confirmed`.
  3. The plan's own end-to-end `<verification>` block (LICENSE, NOTICES.md structure, SOURCES.md structure, self-test, live check) — **all pass**, shown above.

## Deviations from Plan

None - plan executed exactly as written. One clarification worth recording: Task 3's action text names specific real book titles as illustrative candidates ("the frameworks' originators' own published books and their own public web pages"); this executor selected concrete, plausible real titles (Andy Whyte's "MEDDICC" book; Dixon & Adamson's "The Challenger Sale" and "The Challenger Customer") rather than leaving the rows generic, on the reasoning that a named, unverified candidate is more useful to Phase 6's reviewer than an unnamed placeholder — but every one of them is marked `unverified` with no URL, so no citation is asserted as checked.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 04 and Phase 6's LEG-04 gate can now cite a concrete `LICENSE`/`NOTICES.md` scope boundary, three named framework statements, and `SOURCES.md`'s six candidate rows rather than re-deriving them.
- **Outstanding before the repository goes public (carried forward, not new):** the two `unrun-verify` items already logged in `.planning/WINDOWS.md` from 01-02 (name-collision search; comparison read-through), plus — new from this plan — all six `SOURCES.md` rows need a human with live web access to actually open each `Where` location and either promote it to `confirmed` or replace it with a source that does resolve. Recording this here rather than in `.planning/WINDOWS.md` since the plan's own `unverified` status column already carries this signal machine-readably; Phase 6's LEG-04 gate is the named owner.
- The MEDDIC/MEDDICC trademark status noted in STATE.md remains open and is not resolved by this plan — `NOTICES.md` states it as contested rather than assuming safety by extension, per the standing blocker.
- No new blockers introduced.

---
*Phase: 01-foundations-legal-scaffolding-numbering-shared-deal*
*Completed: 2026-09-10*

## Self-Check: PASSED

`LICENSE`, `NOTICES.md`, and `SOURCES.md` confirmed present on disk, plus this SUMMARY.md itself.
All three task commits (`94b1674`, `fcd15de`, `0ba93f8`) confirmed present in `git log`. Plan-level
`<verification>` re-run: `head -1 LICENSE` == `MIT License`; license-file count == 1; NOTICES.md
carries `## Scope of this file`, the undisturbed pointer block, and the three fixed-order framework
subsections; SOURCES.md carries all six sections, six status-bearing rows (all `unverified`), and no
framework mark in any heading; `check_repo.py --self-test` and the live run both exit 0 with 0
violations; all three `<manual>` reviewer checks recorded above as performed.
