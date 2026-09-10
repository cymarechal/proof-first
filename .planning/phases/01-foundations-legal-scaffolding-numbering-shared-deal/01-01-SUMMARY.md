---
phase: 01-foundations-legal-scaffolding-numbering-shared-deal
plan: 01
subsystem: legal-scaffolding
tags: [python, stdlib, github-actions, markdown-registries, numbering, ci]

# Dependency graph
requires: []
provides:
  - "NUMBERING.md: the frozen PF/MC ID registry — six PF section ranges, PF-1's seven-element sub-block layout (ceiling PF-1.28), eight MC dimension blocks, empty Allocated/Deprecated tables, exhaustion and versioning rules"
  - "tools/check_repo.py: a stdlib-only checker enforcing all three registries (nine violation codes: dup-id, range-id, revived-id, undefined-id, dup-figure-key, figure-order, unlisted-figure, pointer-missing, pointer-duplicated), with fixture-based --self-test"
  - ".github/workflows/ci.yml: single-job CI running the self-test then the live check on every push/PR"
  - "examples/deal-brief.md: the Canonical figures table interface, seeded with six figures for the $4-8M regulated mid-enterprise deal (D-09)"
  - "NOTICES.md: the verbatim attribution pointer string and its four-file carriers list (D-14)"
affects: [01-02, 01-03, 01-04, phase-2, phase-3, phase-4, phase-5, phase-6]

# Actuals (#2632)
actuals:
  tokens: 6555
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Registries as machine-readable interfaces: NUMBERING.md ranges, the Canonical figures table, and the attribution pointer block are all parsed by one checker rather than treated as prose formatting."
    - "Stdlib-only checker with inline fixture self-tests: --self-test builds known-bad/known-good fixtures in a temp directory and asserts each violation code fires on bad and stays silent on good, matching the SimpleEnglish ste_lint.py precedent."

key-files:
  created:
    - NUMBERING.md
    - tools/check_repo.py
    - .github/workflows/ci.yml
    - examples/deal-brief.md
    - NOTICES.md
  modified: []

key-decisions:
  - "PF-1 ceiling resolved to PF-1.28 (widen-to-28), not the PF-1.20 research proposal — four slots per Command of the Message element: Before scenario 1.1-1.4, After scenario 1.5-1.8, Required Capabilities 1.9-1.12, Metrics 1.13-1.16, Proof Points 1.17-1.20, Differentiators 1.21-1.24, Positive Business Outcomes 1.25-1.28. Resolved via the plan's blocking-human checkpoint; written verbatim into NUMBERING.md."
  - "Canonical figures seeded with 6 keys for a $6M/3-year regulated mid-enterprise deal, 3 bidders, 62% incumbent estate share, 55% technical scoring weight, 2026-10-30 submission date — plan 02 cites these rather than re-deriving them."
  - "Attribution pointer string frozen verbatim in NOTICES.md, with 4 carrier files (SKILL.md, completeness-audit.md, artifact-patterns.md, README.md) named as required carriers — none exist yet, so the checker currently skips all four (absence, not contradiction)."

patterns-established:
  - "A section's reserved range is a hard ceiling enforced by tools/check_repo.py, never a soft convention — widening requires a major-version NUMBERING.md edit."
  - "Absence tolerance: the checker exits 0 when skills/, README.md, or Allocated/Deprecated data rows do not exist yet. Only contradiction (a violation against data that does exist) fails the build."

requirements-completed: [CAT-07, EX-01, LEG-03]

coverage:
  - id: D1
    description: "NUMBERING.md registry frozen: nine sections, six PF ranges, seven PF-1 sub-blocks (ceiling PF-1.28), eight MC blocks, zero-row Allocated/Deprecated tables"
    requirement: "CAT-07"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "tools/check_repo.py implements all nine violation codes, stdlib-only, with fixture-based self-tests proving each code fires on a known-bad fixture and stays silent on a known-good one"
    requirement: "CAT-07"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test (names all 9 codes in pass summary)"
        status: pass
      - kind: other
        ref: "python3 -c \"import ast,sys; ...\" import-purity check (stdlib-only)"
        status: pass
    human_judgment: false
  - id: D3
    description: ".github/workflows/ci.yml runs the checker self-test then the live check on every push/PR, installing no packages"
    requirement: "CAT-07"
    verification:
      - kind: other
        ref: "grep -cF 'runs-on: ubuntu-latest' .github/workflows/ci.yml; grep -c 'pip install' .github/workflows/ci.yml == 0"
        status: pass
    human_judgment: true
    rationale: "The workflow's structure and command lines are verified locally; an actual green run inside GitHub Actions requires a push to GitHub, which this execution environment cannot perform."
  - id: D4
    description: "examples/deal-brief.md's Canonical figures table seeded with 6 unique, ascending, correctly-typed rows plus the fictional-parties disclaimer and Last reviewed marker"
    requirement: "EX-01"
    verification:
      - kind: other
        ref: "awk row-count and sort -c ordering checks over '## Canonical figures'"
        status: pass
    human_judgment: false
  - id: D5
    description: "NOTICES.md defines the exact attribution pointer string in a fenced block and lists the four required carrier files"
    requirement: "LEG-03"
    verification:
      - kind: other
        ref: "grep -cF 'Concepts here are paraphrased from publicly described sales frameworks.' NOTICES.md == 1"
        status: pass
    human_judgment: false

# Metrics
duration: 20min
completed: 2026-09-10
status: complete
---

# Phase 1 Plan 1: Foundations Scaffolding Summary

**Nine-section `NUMBERING.md` ID registry (PF-1 widened to PF-1.28 across seven Command-of-the-Message sub-blocks), a stdlib-only `tools/check_repo.py` enforcing all nine violation codes with fixture self-tests, single-job CI, and the frozen Canonical-figures/attribution-pointer table shapes in `examples/deal-brief.md` and `NOTICES.md`.**

## Performance

- **Duration:** 20 min
- **Started:** 2026-09-10T06:13:00Z (approx., continuation dispatch)
- **Completed:** 2026-09-10T06:33:30Z
- **Tasks:** 2 (Task 1 checkpoint resolved by human decision prior to this continuation)
- **Files modified:** 5 created (NUMBERING.md, tools/check_repo.py, .github/workflows/ci.yml, examples/deal-brief.md, NOTICES.md)

## Accomplishments
- Froze the `PF-<section>.<n>` / `MC-<n>` ID registry in `NUMBERING.md`, including the resolved `PF-1.28` ceiling and its seven named sub-blocks, with zero rules allocated
- Built a stdlib-only Python checker (`tools/check_repo.py`) proving ID, figure, and attribution integrity across all three registries — 9 violation codes, each with a known-bad and known-good fixture in `--self-test`
- Wired a single GitHub Actions job (`check`) that runs the self-test then the live check on every push/PR with zero package installs
- Seeded `examples/deal-brief.md`'s `## Canonical figures` table with 6 figures for a $6M/3-year regulated mid-enterprise deal
- Froze `NOTICES.md`'s verbatim attribution pointer string and its 4-file carriers list

## Task Commits

Each task was committed atomically:

1. **Task 2: End-to-end "an allocated rule ID is verified by CI"** - `5b124ba` (feat)
2. **Task 3: Extend the proven path to the deal-brief and attribution registries** - `d487e32` (feat)

**Plan metadata:** committed alongside STATE.md/ROADMAP.md updates (next commit)

_Note: Task 1 was a `checkpoint:decision` (gate="blocking-human") resolved by the human before this continuation agent was dispatched — no separate commit, its resolution is written into `NUMBERING.md` in Task 2._

## Files Created/Modified
- `NUMBERING.md` - Authoritative PF/MC ID registry: namespaces, reserved ranges, PF-1 sub-blocks, MC blocks, Allocated/Deprecated tables, exhaustion and versioning rules, next-free-ID lookup
- `tools/check_repo.py` - Stdlib-only checker: ID-integrity (dup-id, range-id, revived-id, undefined-id), figure-integrity (dup-figure-key, figure-order, unlisted-figure), and attribution-integrity (pointer-missing, pointer-duplicated) checks, plus `--self-test`
- `.github/workflows/ci.yml` - Single `check` job: checkout, setup-python 3.11, run self-test then live check
- `examples/deal-brief.md` - Title, `Last reviewed:` marker, fictional-parties disclaimer, and the seeded `## Canonical figures` table (plan 02 fills the rest)
- `NOTICES.md` - Title, orienting sentence, `## Attribution pointer` fenced block, and `### Files required to carry it` list (plan 03 fills the rest)

## Decisions Made

**Checkpoint resolution (Task 1, resolved by human before this continuation):** `PF-1`'s reserved range is `PF-1.1`-`PF-1.28` (the `widen-to-28` option), four slots per Command of the Message element — Before scenario `1.1`-`1.4`, After scenario `1.5`-`1.8`, Required Capabilities `1.9`-`1.12`, Metrics `1.13`-`1.16`, Proof Points `1.17`-`1.20`, Differentiators `1.21`-`1.24`, Positive Business Outcomes `1.25`-`1.28`. This supersedes the `PF-1.20` figure proposed in `.planning/research/ARCHITECTURE.md:166`, which was a research proposal rather than a locked decision — seven elements do not divide evenly into twenty slots, and Positive Business Outcomes (the element most likely to grow) would otherwise be left with only two slots. Rationale recorded verbatim in `NUMBERING.md`'s `## PF-1 sub-blocks` section.

Other decisions followed the plan and CONTEXT.md directly:
- Canonical figures seeded per D-09's deal scale (regulated mid-enterprise, $4-8M/3yr, 3 bidders): `total-contract-value=$6,000,000`, `contract-term-years=3`, `bidder-count=3`, `incumbent-share-of-estate=62%`, `rfp-technical-scoring-weight=55%`, `rfp-submission-date=2026-10-30`.
- Attribution pointer string frozen exactly as CONTEXT.md D-14/the plan specified, with the four carrier paths CONTEXT.md D-14 named.
- Checker filename/location `tools/check_repo.py`, per the plan's A-03 assumption (avoids collision with Phase 5's `evals/proof_lint.py`).

## Deviations from Plan

None - plan executed exactly as written. The Task 1 checkpoint decision was supplied externally (human answer to the dispatched checkpoint) rather than re-derived by this executor, per the continuation instructions.

## Issues Encountered

- The `Write` tool appended a stray literal `</content>` line to the end of each newly created file on the first pass (`NUMBERING.md`, `tools/check_repo.py`, `.github/workflows/ci.yml`, `examples/deal-brief.md`, `NOTICES.md`), which broke Python syntax in `check_repo.py` and would have left a stray line in the Markdown files. Caught immediately by running the self-test/live-run verification commands (which failed with `SyntaxError`), stripped the trailing artifact from each file, and re-verified before committing. No file shipped with the artifact.
- The disclaimer sentence in `examples/deal-brief.md` initially wrapped mid-phrase across two source lines, which defeated the required literal `grep -F` substring match (`any resemblance to a real company, person, or transaction is unintended`). Rewrote the sentence onto one unwrapped line and re-verified.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plans 02, 03, and 04 can now cite `NUMBERING.md`'s PF/MC ranges, `examples/deal-brief.md`'s six Canonical figures keys, and `NOTICES.md`'s exact attribution pointer string rather than re-deriving them.
- `tools/check_repo.py` is live in CI; any future plan adding `skills/`, `README.md`, or more `examples/` content is automatically checked against all nine violation codes.
- No blockers. The MEDDIC/MEDDICC trademark status noted in STATE.md remains open for Phase 6's LEG-04 gate, unaffected by this plan.

---
*Phase: 01-foundations-legal-scaffolding-numbering-shared-deal*
*Completed: 2026-09-10*

## Self-Check: PASSED

All 5 created files confirmed present on disk (`NUMBERING.md`, `tools/check_repo.py`,
`.github/workflows/ci.yml`, `examples/deal-brief.md`, `NOTICES.md`), plus this SUMMARY.md itself.
Both task commits (`5b124ba`, `d487e32`) confirmed present in `git log`. Plan-level `<verification>`
re-run (self-test, live check, file existence, heading count, double-run diff) — all pass.
