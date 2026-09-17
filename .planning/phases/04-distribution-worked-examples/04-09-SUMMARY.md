---
phase: 04-distribution-worked-examples
plan: 09
subsystem: testing
tags: [check-repo, mutation-test, readme, self-test, ci]

# Dependency graph
requires:
  - phase: 04-08
    provides: README rewritten to lead with the before/after pair (line 14), all four
      install routes stating their own runnability, and the layout legend/tree carrying
      zero stray markers -- the clean content this plan's three codes measure.
provides:
  - "readme-example-drift: every README line reproducing an example (✗/✓/`Rules applied:`)
    is enforced, character for character, against examples/before-after.md"
  - "readme-example-lead-distance: README's first ✗ line is enforced at or below a
    frozen 20-line ceiling, and its total absence is also a build failure"
  - "readme-layout-legend-drift: README's '## Repository layout' legend and its fenced
    tree are enforced to agree on marker vocabulary, in both directions"
affects: ["04-verify-work", "phase-04-uat-followup"]

# Actuals (#2632)
actuals:
  tokens: 21000
  tasks: 3
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Tracer-first task ordering: Task 1 (readme-example-drift) proved the whole
      registration path -- constant, check, docstring bullet, extended fixture, new
      root pair, isolation assertions, mutation registration -- before Tasks 2 and 3
      repeated the same shape faster."
    - "Frozen numeric ceiling with disclosed margin (README_FIRST_EXAMPLE_MAX_LINE = 20)
      rather than a measured-value transcription, so a future contributor raising it
      is a visible, argued-for change rather than a silent drift."

key-files:
  created: []
  modified:
    - tools/check_repo.py

key-decisions:
  - "README_FIRST_EXAMPLE_MAX_LINE frozen at 20 (not the measured 14), per the plan's
    explicit prohibition on transcribing today's file into the ceiling."
  - "readme-example-drift and readme-example-lead-distance both read raw text (no
    strip_fences), matching check_readme_install_paths's precedent: the reproduced
    ✗/✓/Rules-applied lines are plain prose, and fence-stripping would change what is
    compared."
  - "readme-layout-legend-drift returns silent (not violating) when README.md has no
    '## Repository layout' heading at all, matching publish-location-drift's established
    'carrier with nothing to say is silent' posture."
  - "Declared and left open in the verify-only ad-hoc import-name regex used in this
    plan's own Task 3 <verify> block (not part of check_repo.py itself): it is a naive
    line-prefix match, not an AST-aware import extractor, and it already misfires on
    the pre-04-09 baseline file (confirmed via git stash) -- documented as a
    plan-authored-script limitation rather than force-fit, matching the 03-04/04-01/
    04-03/04-04 precedent of not editing content to satisfy a broken ad-hoc check."

requirements-completed: []  # DIST-06's structural half was already CI-enforced by 04-04;
                             # this plan closes no new requirement ID (see plan frontmatter).

coverage:
  - id: D1
    description: "readme-example-drift registered end to end: check function, docstring
      bullet, extended _good_readme_install fixture, new drift root pair, isolation
      assertions, and a registered mutation -- 44 to 45 codes."
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test"
        status: pass
    human_judgment: false
  - id: D2
    description: "readme-example-lead-distance registered: fires on no-example and
      late-example fixtures separately, silent on the good install fixture and on
      README-less roots, frozen ceiling of 20 -- 45 to 46 codes."
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test"
        status: pass
    human_judgment: false
  - id: D3
    description: "readme-layout-legend-drift registered: both mismatch directions
      proven in one bad fixture, silent when the layout heading is absent -- 46 to 47
      codes. All four gate commands (self-test, mutation-test, check_repo.py,
      generate_derivatives.py --check) pass at the plan's close."
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test"
        status: pass
      - kind: other
        ref: "python3 tools/generate_derivatives.py --check"
        status: pass
    human_judgment: false

duration: 21min
completed: 2026-09-17
status: complete
---

# Phase 4 Plan 9: README example-drift, lead-distance, and layout-legend checks Summary

**Three new `check_repo.py` codes mechanise the reproduced-pair identity README's own prose
asserts, the promise that README leads with an example, and the legend/tree marker
agreement UAT test 4 found broken -- discrimination-proven total moves 44 to 47.**

## Performance

- **Duration:** 21 min
- **Completed:** 2026-09-17T10:31Z
- **Tasks:** 3
- **Files modified:** 1 (`tools/check_repo.py`)

## Accomplishments

- **`readme-example-drift`** (Task 1, tracer): every README.md line beginning with `✗`,
  `✓`, or `Rules applied:` must be, character for character, a line of
  `examples/before-after.md`. Silent before any read when either file is absent (the
  both-files-required precondition, proven live against `readme_install_good_root`,
  which ships a reproduced-looking README with no `examples/before-after.md` at all).
  Fires once per unmatched README line, naming the line number and an eight-word
  prefix.
- **`readme-example-lead-distance`** (Task 2): README must carry a `✗` line, and the
  first one must sit at or below the frozen `README_FIRST_EXAMPLE_MAX_LINE` ceiling of
  20 -- fixed at 20 rather than the measured value, with a code comment stating that
  raising it is a deliberate weakening of DIST-06 requiring justification, not a
  transcription of whatever the file happens to measure today. Both firing conditions
  (no example at all; example too late) are proven on separate fixtures.
- **`readme-layout-legend-drift`** (Task 3): within README's `## Repository layout`
  section, the set of quoted markers the legend prose explains must equal the set of
  parenthesised markers the fenced tree uses, in both directions. Silent when the
  section is absent, matching `publish-location-drift`'s established "carrier with
  nothing to say is silent" posture. One bad fixture exercises both mismatch
  directions at once.
- All four CI gate commands pass at the plan's close: `--self-test` (47 verified
  codes), `--mutation-test` (`mutation-test PASS: 47 codes discrimination-proven`, `0
  unexpected` on CONTROL, no FIRE-ONLY line), `check_repo.py` (`check_repo: 0
  violations` against the real repository -- proving README and
  `examples/before-after.md` genuinely agree line for line after `04-05` and `04-08`),
  and `generate_derivatives.py --check`.

## Task Commits

Each task was committed atomically:

1. **Task 1: Register readme-example-drift end to end — check, fixtures, mutation, 44 to 45 codes** - `2b81401` (feat)
2. **Task 2: Register readme-example-lead-distance — 45 to 46 codes** - `48dcbed` (feat)
3. **Task 3: Register readme-layout-legend-drift — 46 to 47 codes** - `717cf4f` (feat)

No separate plan-metadata commit was made for task code; this SUMMARY/STATE/ROADMAP
update is committed separately per the sequential-executor protocol.

## Files Created/Modified

- `tools/check_repo.py` - three new check functions
  (`check_readme_example_drift`, `check_readme_example_lead_distance`,
  `check_readme_layout_legend_drift`), five new constants
  (`README_CROSS_CHAR`, `README_CHECK_CHAR`, `README_APPLIED_RULES_PREFIX`,
  `README_FIRST_EXAMPLE_MAX_LINE`, `README_LAYOUT_HEADING`), two new bounded regexes
  (`README_LAYOUT_LEGEND_MARKER_RE`, `README_LAYOUT_TREE_MARKER_RE`), an extended
  `_good_readme_install()` fixture, six new fixture builders
  (`_readme_drift_before_after`, `_readme_drift_before_after_bad`,
  `_late_example_readme`, `_no_example_readme`, `_good_readme_layout`,
  `_bad_readme_layout`), six new self-test roots, three new mutation functions, and
  three new `MUTATIONS` entries. File grew from 5813 to 6327 lines.

## Decisions Made

See `key-decisions` in the frontmatter above. The most consequential: freezing
`README_FIRST_EXAMPLE_MAX_LINE` at 20 with a stated margin over the measured
pre-repair value of 23 (the real, repaired file now measures 14), so the constant is a
real constraint a future contributor must argue against, not a passive transcription
of whatever the file happens to say today.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed the `_late_example_readme()` filler-line count so the
ballot-cross line genuinely lands past the ceiling, not exactly at it**
- **Found during:** Task 2, self-test verification
- **Issue:** The plan's own interfaces measurements and my first draft used 10 filler
  lines, which pushed the fixture's first `✗` line to exactly line 20 -- equal to, not
  past, `README_FIRST_EXAMPLE_MAX_LINE`, so the "late" firing condition would not have
  fired.
- **Fix:** Increased filler to 15 lines, landing the `✗` line at 25 (comfortably past
  20).
- **Files modified:** `tools/check_repo.py`
- **Verification:** `--self-test` asserts `readme-example-lead-distance` fires on
  `readme_lead_late_root`; confirmed passing.
- **Commit:** `48dcbed` (Task 2 commit)

### Documented, Not Force-Fit

**1. [Plan-authored verify-script limitation] Task 3's own ad-hoc import-name regex
over-matches prose lines starting with "from"/"import"**

- **Found during:** Task 3, running the plan's own `<verify>` command
  `python3 -c "import ast,pathlib,re;...re.findall(r'^\s*(?:import|from)\s+...')..."`.
- **Issue:** This one-off diagnostic (not part of `check_repo.py` itself, and not a
  registered check) is a naive per-line prefix match, not an AST-aware import
  extractor. It matches any docstring/comment line that happens to start with
  "from " or "import " -- e.g. "from the surrounding prose", "from this file, the
  divergence...". This produces spurious entries (`different`, `some`, `the`, `this`)
  alongside the genuine stdlib names.
- **Confirmed pre-existing, not introduced by this plan:** running the identical
  command against the committed pre-04-09 baseline (`git stash` + rerun) produces the
  exact same four spurious entries. Five of the six offending lines already existed in
  the file before this plan touched it (module docstring lines and two mutation-function
  docstrings from earlier phases); this plan's own new docstring text (`check_readme_
  layout_legend_drift`'s reference to `FENCE_RE` isolating the tree "away from the
  surrounding prose") was reworded specifically to avoid adding a seventh instance.
- **Not fixed:** per the established 03-04/04-01/04-03/04-04 precedent, a
  plan-authored verification script's own limitation is documented rather than
  force-fit by rewriting unrelated, pre-existing docstring prose across the file. The
  load-bearing evidence that imports are genuinely stdlib-only is the four real CI gate
  commands, all of which pass, plus a direct read of the six `import`/`from` lines at
  the top of the module (lines 698-705), which are exactly
  `{argparse, hashlib, json, re, shutil, sys, tempfile, pathlib}`.
- **Files modified:** none (documentation only, this SUMMARY).
- **Verification:** manual `git stash` comparison against baseline, and direct
  inspection of the module's actual `import`/`from` statements.

---

**Total deviations:** 1 auto-fixed (Rule 1 - fixture arithmetic), 1 documented-not-fixed
(pre-existing plan-authored verify-script limitation).
**Impact on plan:** No scope creep; both items were caught and resolved (or correctly
left alone) while running the plan's own acceptance criteria, consistent with prior
phase-4 plans' precedent.

## Issues Encountered

None beyond the two items already covered under Deviations.

## User Setup Required

None - no external service configuration required.

## WINDOWS.md Entry 12 -- What This Plan Covers Mechanically vs. What Remains a Semantic Judgment

Per this plan's own `<output>` instruction, recording explicitly for the phase's
verification step:

**Now mechanically enforced (this plan):**
- README's reproduced example lines can never silently drift from
  `examples/before-after.md` (`readme-example-drift`).
- README's first before/after example can never silently regress past line 20, or
  disappear entirely (`readme-example-lead-distance`).
- README's repository-layout legend and its fenced tree can never silently disagree on
  marker vocabulary, in either direction (`readme-layout-legend-drift`).

**Still a semantic judgment, per the plan's own `<gap_coverage>` scoping (not
mechanised, and not claimed to be):**
- G-04-6 (a) whether the install routes are genuinely runnable as described.
- G-04-6 (d) whether the models-count caveat is accurately scoped.
- G-04-6 (e) whether the catalog-effect claim is over-broad.
- Whether README reads well to a first-time reader overall (DIST-06's prose-quality
  half) -- this is the residual WINDOWS.md entry 12 itself names, and it is narrowed
  by this plan (two of its seven structural components are now build failures if they
  regress) but not closed. The phase's verification step should re-evaluate entry 12's
  description against what is now mechanical, rather than marking it resolved.

## Next Phase Readiness

- `check_repo.py` now enforces 47 discrimination-proven codes with 0 live violations
  and 0 unexpected CONTROL violations. `04-10` (G-04-7, per this plan's own
  `<gap_coverage>` table) can proceed against this baseline.
- No blockers. `.planning/config.json`'s `mode: yolo` and this plan's `autonomous: true`
  meant no checkpoints were encountered; the plan carried no `type="checkpoint:*"` task.

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-17*

## Self-Check: PASSED

- `tools/check_repo.py` exists on disk.
- SUMMARY.md exists on disk.
- Commits `2b81401`, `48dcbed`, `717cf4f` all found in `git log --oneline --all`.
- All plan-level `<verification>` commands re-run clean at close: `--self-test` (47
  verified codes), `--mutation-test` (`mutation-test PASS: 47 codes
  discrimination-proven`, 0 unexpected CONTROL, no FIRE-ONLY), `check_repo.py`
  (`check_repo: 0 violations`), `generate_derivatives.py --check` (exit 0).
