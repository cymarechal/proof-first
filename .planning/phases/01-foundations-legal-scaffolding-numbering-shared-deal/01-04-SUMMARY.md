---
phase: 01-foundations-legal-scaffolding-numbering-shared-deal
plan: 04
subsystem: legal-scaffolding
tags: [readme, repository-entry-point, integrity-sweep, phase-close]

# Dependency graph
requires:
  - phase: 01-01
    provides: "NUMBERING.md's namespaces/versioning sections and NOTICES.md's frozen attribution-pointer fenced block, both quoted/summarised in README.md"
  - phase: 01-02
    provides: "examples/deal-brief.md as the complete artifact the integrity sweep confirms is present and non-empty"
  - phase: 01-03
    provides: "LICENSE, NOTICES.md's Scope/Framework-statements sections, and SOURCES.md, all linked from README.md's License and notices section and read during the phase-closing legal read"
provides:
  - "README.md: the repository's claim-free entry point -- six sections (What this is, Status, Repository layout, Rule numbering, Versioning, License and notices), documenting the target layout without pre-creating any of it, and carrying the NOTICES.md attribution pointer as its first real (non-fixture) carrier"
  - "A recorded phase-closing integrity sweep proving all eight Phase 1 files exist, non-empty, checker-clean, and free of framework marks in any filename/directory/heading outside NOTICES.md"
  - "A recorded phase-closing legal read confirming no file in the phase reproduces proprietary framework text"
affects: [phase-2, phase-3, phase-4, phase-6]

# Actuals (#2632)
actuals:
  tokens: 1175
  tasks: 2
  commits: 1

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "The attribution pointer is now proven against a real carrier file (README.md), not only against tools/check_repo.py's own fixtures -- pointer-missing/pointer-duplicated enforcement is live against shipped content."
    - "A README documenting a target layout without creating any of it (D-15) -- 'planned' annotations in a fenced tree, not empty placeholder files."

key-files:
  created:
    - README.md
  modified: []

key-decisions:
  - "Task 2's own literal heading-sweep verify command (grep -v '^\\./NOTICES\\.md:' exclusion) produces a false failure on this environment's grep implementation (ugrep, which omits the './' prefix that GNU grep would add when recursing from '.'). Re-ran the equivalent check with --exclude=NOTICES.md instead of the path-prefix exclusion and confirmed the true result: every Markdown heading found outside NOTICES.md across the whole repo (SOURCES.md, NUMBERING.md, README.md, examples/deal-brief.md) carries zero framework marks, and only NOTICES.md's own three named subsections do. This is a verification-tooling environment quirk, not a repository defect -- no file was changed as a result."
  - "No defect found anywhere in the phase's eight files during the phase-closing legal read; README.md was the only file this plan modified, and it needed no follow-up edit after the sweep."

patterns-established: []

requirements-completed: [LEG-03]

coverage:
  - id: D1
    description: "README.md written with all six required sections, documenting the target layout (skills/proof-first/ and the rest) without creating any of it, stating plainly that no measured claim is published yet, and carrying the NOTICES.md attribution pointer exactly once"
    requirement: "LEG-03"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations, README accepted as attribution-pointer carrier)"
        status: pass
      - kind: other
        ref: "grep -cF 'Concepts here are paraphrased from publicly described sales frameworks.' README.md == 1"
        status: pass
      - kind: other
        ref: "grep -F '![' / grep -E '[0-9]+(\\.[0-9]+)?%' / grep -E 'PF-[0-9]+\\.[0-9]+|MC-[0-9]+' README.md -- all zero matches"
        status: pass
      - kind: other
        ref: "python3 -c heading/link-string presence check -- missing: []"
        status: pass
    human_judgment: false
  - id: D2
    description: "Full-repository integrity sweep: all eight Phase 1 files present and non-empty, checker green in both modes, no framework mark in any filename/directory/heading outside NOTICES.md, four ROADMAP success criteria mapped to artifacts"
    requirement: "LEG-03"
    verification:
      - kind: other
        ref: "file-presence test chain -- ALL_PRESENT"
        status: pass
      - kind: other
        ref: "find . -type f -empty -not -path './.git/*' | wc -l == 0"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --self-test (names all 9 codes) and python3 tools/check_repo.py -- both exit 0"
        status: pass
      - kind: other
        ref: "heading sweep (corrected for this environment's grep) and path sweep -- zero framework marks outside NOTICES.md"
        status: pass
    human_judgment: false
  - id: D3
    description: "Phase-closing legal read: all eight Phase 1 files read end to end; every framework-derived concept (NOTICES.md's factual attribution statements, SOURCES.md's category descriptions, NUMBERING.md's PF-1 element-name labels) is stated in this repository's own words and traces to a SOURCES.md source category; no proprietary text, diagram, or reproduced ordered list found anywhere"
    requirement: "LEG-03"
    verification: []
    human_judgment: true
    rationale: "This is the semantic paraphrase-vs-reproduction judgement SOURCES.md itself states no tool in this project's stack performs. Performed as a single-reviewer read in this session (recorded below); Phase 6's LEG-04 gate repeats it against current sources before public launch, per SOURCES.md's own stated ownership."
  - id: D4
    description: "README claims read-through: confirmed no sentence in README.md claims effectiveness, improvement, or comparison to any alternative"
    requirement: "LEG-03"
    verification: []
    human_judgment: true
    rationale: "A judgement about absence of persuasive/effectiveness framing, which the plan itself calls out as not expressible by grep."

# Metrics
duration: 20min
completed: 2026-09-10
status: complete
---

# Phase 1 Plan 4: Repository Entry Point and Phase-Closing Sweep Summary

**Claim-free `README.md` (six sections, target layout documented not pre-created, first real attribution-pointer carrier) plus a recorded full-repository integrity sweep and phase-closing legal read confirming Phase 1 is internally consistent and reproduces no proprietary framework text.**

## Performance

- **Duration:** 20 min
- **Started:** 2026-09-10T07:04:00Z (approx.)
- **Completed:** 2026-09-10T07:24:00Z
- **Tasks:** 2
- **Files modified:** 1 (`README.md` created)

## Accomplishments
- Wrote `README.md` at the repository root: `## What this is`, `## Status`, `## Repository layout`, `## Rule numbering`, `## Versioning`, `## License and notices` — no badges, no images, no percentage token, no numbered rule identifier, and one plain sentence stating no measured claim is published yet
- Documented the full target tree (`skills/proof-first/`, `output-styles/`, `prompts/`, `examples/before-after.md`, `evals/`, `.claude-plugin/`) marked "planned" without creating any of it, per D-15
- Proved the `NOTICES.md` attribution-pointer mechanism against a real shipped file for the first time: `README.md` carries the pointer string exactly once and `tools/check_repo.py` accepts it with 0 violations
- Ran the full-repository integrity sweep: all eight Phase 1 files present and non-empty, checker green in both `--self-test` and live-run modes, zero framework marks in any filename, directory name, or Markdown heading outside `NOTICES.md`
- Performed the phase-closing legal read across all eight Phase 1 files and recorded that nothing reproduces proprietary framework text
- Mapped each of the four ROADMAP Phase 1 success criteria to the artifact that satisfies it (below)

## Task Commits

Each task was committed atomically:

1. **Task 1: A claim-free README that documents the target layout** - `58530a6` (feat)
2. **Task 2: Full-repository integrity sweep and the phase-closing legal read** - no commit; the sweep found no defect in any file, so no file changed under this task. Its output is recorded in this SUMMARY.

**Plan metadata:** committed alongside STATE.md/ROADMAP.md/REQUIREMENTS.md updates (next commit)

## Files Created/Modified
- `README.md` — Repository entry point: what the project is, honest current status, the target repository layout (documented, not pre-created), a pointer at `NUMBERING.md` for rule numbering and versioning, and the License-and-notices section carrying the verbatim attribution pointer

## Decisions Made

- **Grep-implementation quirk, not a repository defect:** Task 2's own literal heading-sweep verify command excludes `NOTICES.md` matches via a `^\./NOTICES\.md:` path-prefix pattern, which assumes GNU-grep-style `./`-prefixed recursive output. This environment's `grep` is `ugrep`, which omits the `./` prefix, so the exclusion never matched and the command's raw output showed the three (legitimate, in-file) `NOTICES.md` headings as if unexcluded. Re-ran the equivalent check with `--exclude=NOTICES.md` and confirmed the true result: zero framework marks in any heading outside `NOTICES.md` anywhere in the repository. No repository file needed a change; this is purely a verification-environment note for whoever next runs this check by hand on macOS/BSD-grep-family systems.
- **Four ROADMAP Phase 1 success criteria mapped to artifacts** (recorded here per the plan's `<output>` instruction):
  1. *"A contributor can look up the next free ID in either namespace without guessing"* → `NUMBERING.md`'s `## Next free ID` section plus the `PF reserved ranges` / `MC reserved blocks` / `Allocated IDs` tables.
  2. *"Every worked example can cite facts from one canonical fictional deal brief"* → `examples/deal-brief.md`'s full deal spine, inconvenient facts, customer source material, and its 18-key `## Canonical figures` table.
  3. *"LICENSE and NOTICES.md individually name all three frameworks with non-affiliation and trademark language"* → `LICENSE`'s unmodified MIT grant plus `NOTICES.md`'s `## Framework statements` (three fixed-order, individually named subsections: Command of the Message, the contested MEDDIC/MEDDICC family, Challenger).
  4. *"Nothing in the repo reproduces proprietary framework text"* → `SOURCES.md`'s `## What counts as reproduction` (the paraphrase/reproduction boundary, naming Phase 6's LEG-04 gate as owner of the semantic judgement) plus this plan's Task 2 phase-closing legal read, recorded below.
- **Final list of paths `README.md` documents as planned but not yet built** (so Phase 4 inherits the exact set): `skills/proof-first/SKILL.md`, `skills/proof-first/references/checklist.md`, `skills/proof-first/references/completeness-audit.md`, `skills/proof-first/references/artifact-patterns.md`, `skills/proof-first/references/deletion-test.md`, `output-styles/proof-first.md`, `prompts/system-prompt.md`, `examples/before-after.md`, `evals/`, `.claude-plugin/`.

## Deviations from Plan

None - plan executed exactly as written. The grep-exclusion quirk noted above is a verification-environment observation, not a deviation from the plan's action or acceptance criteria — the underlying repository state the command was checking (no framework mark outside `NOTICES.md`) was already correct before and after this plan ran.

## Issues Encountered

None. The phase-closing legal read (Task 2) found no reproduction of proprietary framework text in any of the eight Phase 1 files:

- **`LICENSE`** — unmodified, standard MIT license boilerplate; not framework-derived content.
- **`NOTICES.md`** — the three framework statements state only Mark / Rights-holder / Non-affiliation / Paraphrase-boundary / Last-reviewed facts in this repository's own words; no course content, training material, or proprietary diagram is quoted or described in structural detail.
- **`SOURCES.md`** — describes each framework's source category ("message articulation," "qualification checklist," "commercial teaching") at the level of generality the framework's own public materials use; the source tables list candidate titles, not reproduced content.
- **`NUMBERING.md`** — the `PF-1` sub-block element names (Before scenario, After scenario, Required Capabilities, Metrics, Proof Points, Differentiators, Positive Business Outcomes) are structural category labels at the same level of generality Command-of-the-Message-style public materials commonly use; no proprietary ordered list, worked script, or diagram is reproduced. This naming was a locked decision from 01-01 (D-01); this sweep confirms it independently rather than re-litigating it.
- **`README.md`** — no framework name appears anywhere except inside the frozen, verbatim attribution-pointer string itself ("sales frameworks," generic).
- **`examples/deal-brief.md`** — entirely fictional deal narrative and figures; contains no framework-methodology language at all.
- **`tools/check_repo.py`** and **`.github/workflows/ci.yml`** — pure tooling; no framework content.

Read performed and recorded: 2026-09-10, single-reviewer read (this executor). Phase 6's LEG-04 gate is the named owner of repeating this judgement against current sources before public launch, per `SOURCES.md`'s own stated scope.

The second manual check (README claims read-through) also passed: no sentence in `README.md` claims effectiveness, improvement, or comparison to any alternative; the only forward-looking statement is that a benchmark has not run and any future number will be sourced from committed results with model versions and a date.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Phase 1 is complete. All four requirements this phase owns (`CAT-07`, `EX-01`, `LEG-01`, `LEG-02`, `LEG-03`) are satisfied; `LEG-04` and `LEG-05` remain correctly deferred to Phase 6.
- Phase 2 can now cite `README.md`'s repository layout and `NUMBERING.md`'s namespace summary as the frozen scaffolding, and begin drafting `SKILL.md`'s prose rule catalog against the reserved `PF-*` ranges.
- Phase 4 inherits the exact "documented but not yet built" path list from `README.md` (repeated above) as its own scope boundary for what to actually create.
- **Outstanding before the repository goes public (carried forward from 01-02/01-03, not new):** the two `unrun-verify` entries already logged in `.planning/WINDOWS.md` (name-collision web search; independent comparison read-through), and all six `SOURCES.md` rows still marked `unverified`, all need a human with live web access — Phase 6's LEG-04 gate is the named owner. This plan did not close either; they remain open by design.
- The MEDDIC/MEDDICC trademark status noted in `STATE.md` remains open for Phase 6, unaffected by this plan.
- No new blockers introduced.

---
*Phase: 01-foundations-legal-scaffolding-numbering-shared-deal*
*Completed: 2026-09-10*

## Self-Check: PASSED

`README.md` confirmed present on disk, plus this SUMMARY.md itself. Task 1 commit (`58530a6`)
confirmed present in `git log`. Plan-level `<verification>` re-run: all eight Phase 1 files
present and non-empty; `check_repo.py --self-test` and the live run both exit 0 with 0 violations;
`README.md` carries the attribution pointer exactly once, no image syntax, no percentage token,
no rule identifier; no Markdown heading outside `NOTICES.md` and no path outside `.git`/`.planning`/
`.claude` carries a framework mark (re-verified with an `--exclude`-flag form of the heading check
after the literal plan command produced a false positive under this environment's `ugrep`); both
`<manual>` reviewer checks recorded above as performed.
