---
phase: 01-foundations-legal-scaffolding-numbering-shared-deal
plan: 05
subsystem: tooling
tags: [check_repo, notices, attribution, ci, stdlib, python]

# Dependency graph
requires:
  - phase: 01-foundations-legal-scaffolding-numbering-shared-deal
    provides: NOTICES.md's attribution-pointer registry and README.md as its first real carrier (01-01, 01-04)
provides:
  - An attribution-pointer checker that actually parses production NOTICES.md's shape (heading, prose paragraph, fence) instead of only a fixture shape that never matched shipped content
  - A pointer-unparseable violation code that fails loud when the Attribution pointer section yields no usable pointer definition, closing the silent-success path CR-01/BLOCKER described
  - Carrier-path containment (_carrier_is_repo_relative) rejecting absolute, drive-letter, and ..-escaping carrier entries before they are ever opened
  - Declared code-point-equality comparison semantics documented in the module docstring
affects: [01-07 (regression harness over tools/check_repo.py), Phase 2, Phase 4 (add skills/proof-first/SKILL.md and its two reference files as new carriers)]

# Actuals (#2632)
actuals:
  tokens: 2051
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "split_sections() as the single extraction path for any NOTICES.md/NUMBERING.md/deal-brief.md sub-structure, never a regex anchored to a heading line"
    - "fail-loud check functions: a parse failure on an existing input file is always violation material, never a silent empty return (file-level absence is the only legitimate short-circuit)"

key-files:
  created: []
  modified:
    - tools/check_repo.py

key-decisions:
  - "Kept check_pointer()'s existing exact stripped-line equality; no fuzzy/substring loosening, per the plan's explicit prohibition (D-14)."
  - "Scoped both pointer extraction and carrier-list extraction to the Attribution pointer section body (via split_sections()), not the whole document, closing threat T-01-03 (lazy-quantifier DoS) as a side effect of the parser fix."
  - "_carrier_is_repo_relative() runs before any carrier path is joined to repo_root, so an absolute or ..-escaping entry is rejected and never opened (T-01-01)."

patterns-established:
  - "New violation codes register through NOTICES_CHECK_CODES only; ALL_CHECK_CODES and the self-test coverage loop pick them up with no other edit required."

requirements-completed: [LEG-03]

coverage:
  - id: D1
    description: "parse_notices() extracts the pointer from the Attribution pointer section body via split_sections(), tolerating prose between the heading and the fenced block"
    requirement: "LEG-03"
    verification:
      - kind: other
        ref: "grep -A8 'def parse_notices' tools/check_repo.py | grep -q split_sections"
        status: pass
      - kind: other
        ref: "live run against repo as shipped: python3 tools/check_repo.py -> 'check_repo: 0 violations', exit 0"
        status: pass
    human_judgment: false
  - id: D2
    description: "pointer-unparseable violation fires when the Attribution pointer section yields no usable pointer definition (no fence, empty fence, or missing section) instead of silently returning zero violations"
    requirement: "LEG-03"
    verification:
      - kind: other
        ref: "scratch NOTICES.md with '## Attribution pointer' heading deleted -> checker prints 'pointer-unparseable NOTICES.md...' and exits 1"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --self-test names pointer-unparseable among ten verified codes, exit 0"
        status: pass
    human_judgment: false
  - id: D3
    description: "Deleting the attribution pointer from README.md (the real, shipped carrier) now produces pointer-missing and exit 1 -- closes the BLOCKER from 01-VERIFICATION.md/CR-01"
    requirement: "LEG-03"
    verification:
      - kind: other
        ref: "scratch copy of README.md with the pointer line grep -v'd out -> 'pointer-missing README.md does not contain the attribution pointer string', exit 1"
        status: pass
    human_judgment: false
  - id: D4
    description: "Carrier existence matrix: absent carrier -> 0 violations; existing carrier with zero occurrences -> pointer-missing; existing carrier with two occurrences -> pointer-duplicated"
    requirement: "LEG-03"
    verification:
      - kind: other
        ref: "manual matrix run in three scratch trees (carrier absent / present-empty / present-duplicated), all three outcomes matched expected code and exit status"
        status: pass
    human_judgment: false
  - id: D5
    description: "_carrier_is_repo_relative() rejects an absolute, drive-letter, or ..-escaping carrier entry with pointer-unparseable before the path is ever opened (T-01-01)"
    requirement: "LEG-03"
    verification:
      - kind: other
        ref: "scratch NOTICES.md naming '../escaped.md' as a carrier -> 'pointer-unparseable ../escaped.md is a required-carrier entry that is not a repository-relative path', no pointer-missing line naming a path outside the repo"
        status: pass
    human_judgment: false
  - id: D6
    description: "Module docstring documents the code-point-equality comparison rule (no Unicode normalisation, no case folding) and both pointer-unparseable triggers; U+00A0-vs-U+0020 line is reported pointer-missing per self-test fixture"
    requirement: "LEG-03"
    verification:
      - kind: other
        ref: "sed -n '1,50p' tools/check_repo.py | grep -qi normalisation; carrier-lookalike.md fixture (U+00A0 substituted) fires pointer-missing in --self-test's bad_root"
        status: pass
    human_judgment: false
  - id: D7
    description: "python3 tools/check_repo.py imports only the Python standard library; no third-party dependency introduced"
    requirement: "LEG-03"
    verification:
      - kind: other
        ref: "AST import scan asserting imports subset {argparse, re, sys, tempfile, pathlib, shutil, os, ast}"
        status: pass
    human_judgment: false

duration: 35 min
completed: 2026-09-10
status: complete
---

# Phase 1 Plan 5: Attribution-Pointer Enforcement Fixed to Actually Fire Summary

Rewrote `tools/check_repo.py`'s attribution-pointer path so it parses production `NOTICES.md`'s
real shape (heading, prose paragraph, fence) via the house `split_sections()` idiom, fails loud
with a new `pointer-unparseable` code on any unusable pointer definition, and rejects
non-repository-relative carrier paths before they are ever opened — closing the false-green defect
where deleting the pointer from README.md still exited 0.

## Performance

- **Duration:** 35 min
- **Started:** 2026-09-10T09:47:00Z (approx.)
- **Completed:** 2026-09-10T10:22:00Z (approx.)
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments

- `parse_notices()` extracts the pointer from the `Attribution pointer` section body via
  `split_sections()` instead of a regex anchored directly to the heading line, so the explanatory
  prose paragraph production `NOTICES.md` actually has no longer breaks extraction.
- A new `pointer-unparseable` violation code fires when the Attribution pointer section yields no
  usable pointer definition (missing section, missing fence, or empty fence) — the checker no
  longer returns `[]` for a parse failure on a file that exists.
- Deleting the attribution pointer from the real, shipped `README.md` now produces
  `pointer-missing README.md ...` and exit 1 — the specific BLOCKER from `01-VERIFICATION.md`/CR-01
  is closed and proven against production content, not only a self-test fixture.
- `_carrier_is_repo_relative()` rejects an absolute, drive-letter, or `..`-escaping carrier entry
  with `pointer-unparseable` before `check_pointer()` ever opens it, closing threat T-01-01.
- The module docstring now states the pointer-comparison rule (UTF-8 decode + strip, then Python
  string equality — code-point equality, no Unicode normalisation, no case folding) and both
  `pointer-unparseable` triggers.
- `--self-test`'s fixtures (`_bad_notices()`/`_good_notices()`) mirror the production document
  shape; new `_unparseable_notices()` and `_escaping_notices()` fixtures exercise the two new
  failure paths in isolated scratch roots. All ten violation codes are covered and the live repo
  stays at `check_repo: 0 violations`.

## Task Commits

Each task was committed atomically:

1. **Task 1: End-to-end attribution-pointer enforcement against production content** - `3dde78a` (feat)
2. **Task 2: Harden the same path — carrier-path containment, string-equality semantics, duplication** - `45011a2` (feat)

**Plan metadata:** committed in the same pass as this SUMMARY

## Files Created/Modified

- `tools/check_repo.py` - `parse_notices()` rewritten on `split_sections()`; new `POINTER_SECTION`/
  `CARRIERS_MARKER` constants; new `pointer-unparseable` code and `_carrier_is_repo_relative()`
  containment helper wired into `run_notices_checks()`; module docstring extended; `_bad_notices()`/
  `_good_notices()` rewritten to production shape; new `_unparseable_notices()`/`_escaping_notices()`
  fixtures and their scratch roots registered in `self_test()`.

## Decisions Made

- Kept `check_pointer()`'s exact stripped-line string equality unchanged — no loosening to
  substring or fuzzy matching, per the plan's explicit prohibition tied to D-14.
- Scoped both pointer extraction and carrier-list extraction to the `Attribution pointer` section
  body rather than the whole document. This was required by Task 1's action, and it also
  incidentally closes threat T-01-03 (a lazy-quantifier regex scanning an entire
  attacker-influenceable Markdown document) as a side effect of fixing the parser, not as separate
  work.
- `_carrier_is_repo_relative()` runs in `run_notices_checks()` before any carrier path is joined to
  `repo_root`, so a rejected entry is never opened at all (not opened-then-discarded).

## Deviations from Plan

### Auto-fixed Issues

**1. [Task-boundary imprecision, not a Rule 1-4 deviation] `_carrier_is_repo_relative()` landed in Task 1's commit instead of Task 2's**
- **Found during:** Editing Task 1 (an early draft pass wrote both the parser fix and the
  containment helper together before task separation was enforced).
- **Issue:** The plan assigns `_carrier_is_repo_relative()` and its wiring into
  `run_notices_checks()` to Task 2's action block. It was written and committed as part of Task 1
  (commit `3dde78a`) instead.
- **Fix:** No code change was needed — Task 1's own acceptance criteria and the plan's
  `<verification>` block were re-run in full after the fact and all passed with the helper present
  (it has no effect on Task 1's behavior since Task 1 never produces a non-repo-relative carrier
  entry in its fixtures). Task 2's commit (`45011a2`) then added only what remained: the fifth
  carrier entry, the `_escaping_notices()` fixture, and the docstring's two-trigger/normalisation
  wording.
- **Files modified:** `tools/check_repo.py` (both commits).
- **Verification:** All nine Task 1 acceptance criteria and the plan-level `<verification>` block
  were independently re-run against the state at commit `3dde78a` and passed; all Task 2 acceptance
  criteria were re-run against the final state and passed.
- **Committed in:** `3dde78a` (helper), `45011a2` (remaining Task 2 work).

---

**Total deviations:** 1 (task-boundary sequencing only; no functional, security, or correctness
impact — both tasks' acceptance criteria and the plan's full `<verification>` block pass against
the final state).
**Impact on plan:** None on behavior or scope. The containment mitigation (T-01-01) was active one
commit earlier than the plan's task split implies, which is strictly more conservative, not less.

## Issues Encountered

- The Edit tool repeatedly failed to match an intended `old_string` in the `self_test()` fixture-
  registration block because an earlier draft edit had already inserted a real U+00A0 (non-breaking
  space) byte into a scratch-fixture string literal, and byte-for-byte comparison against a
  visually-identical ASCII string silently mismatched. Resolved by reading the file's raw bytes
  (`xxd`) to confirm the actual content, then using a small Python script to perform the
  string-literal replacement precisely (with the U+00A0 written as an explicit ` ` escape in
  the Python *source*, not a raw byte, so the intent is legible in the diff). No repository content
  outside `tools/check_repo.py` was touched during this recovery.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- LEG-03's no-drift mechanism now enforces rather than merely asserts: the attribution-pointer
  check will actually fire when Phase 2 and Phase 4 add `skills/proof-first/SKILL.md` and its two
  reference files as new carriers.
- `tools/check_repo.py` still imports only the Python standard library; both CI modes
  (`--self-test` and the live run) stay green.
- 01-06 (numbering + figures fixes) and 01-07 (regression harness) remain the next gap-closure
  plans in this phase; neither depends on anything this plan introduced beyond the file already
  being green.

---
*Phase: 01-foundations-legal-scaffolding-numbering-shared-deal*
*Completed: 2026-09-10*
