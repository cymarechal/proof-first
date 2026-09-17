---
phase: 04-distribution-worked-examples
plan: 08
subsystem: docs
tags: [readme, install, documentation, distribution]

requires:
  - phase: 04-distribution-worked-examples
    provides: "04-07's gate baseline of 44 codes discrimination-proven, and 04-05's byte-identical ✗/✓/Rules-applied lines in examples/before-after.md"
provides:
  - "README restructured so the before/after pair leads the file, each install route states its own runnability, maintainer instruction sits below Status, the layout legend agrees with the tree, and two over-broad sentences are narrowed to what the catalog/measurements actually support"
affects: [04-09, 04-10]

actuals:
  tokens: 2195
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns: []

key-files:
  created: []
  modified:
    - README.md

key-decisions:
  - "Defect (d) (measured-models caveat) resolved by naming claude-sonnet-5 explicitly as the only model behind the anchored figures and stating that RESULTS-mod04.md's claude-opus-5 sessions are superseded and unanchored, rather than dropping the model count without naming anything — the plan allowed either repair; this one keeps a concrete, checkable identifier in the caveat."
  - "Task 1's lead-in trim was unnecessary beyond the section move itself: relocating '## Before and after' ahead of 'What this is' alone dropped the first ✗ line from 23 to 14, twelve lines under the 20-line ceiling with no wording change required — Task 2 then narrowed the lead-in's content for defect (e) independently."
  - "README.md's tree entry kept its '— this file' annotation (dropping only the '(exists' marker prefix) rather than deleting the annotation outright, since it is genuinely useful orientation for a reader and carries no marker-vocabulary claim once 'exists' is removed."

requirements-completed: [DIST-06]

coverage:
  - id: D1
    description: "The before/after pair leads the README inside the first screen — first ✗ line moved from line 23 to line 14"
    requirement: DIST-06
    verification:
      - kind: integration
        ref: "tools/check_repo.py#check_readme_before_after_order"
        status: pass
    human_judgment: true
    rationale: "check_readme_before_after_order enforces heading order only; no persistent check asserts the ✗ line's distance from the top of the file (04-09 registers readme-example-lead-distance for that). Line 14 is this session's measurement, not a permanent gate."
  - id: D2
    description: "Each install route states whether it is runnable today (routes 3-4 from a local clone; routes 1-2 blocked on publication)"
    requirement: DIST-06
    verification:
      - kind: integration
        ref: "tools/check_repo.py#check_readme_install_paths"
        status: pass
    human_judgment: true
    rationale: "check_readme_install_paths only asserts the four anchor strings are present somewhere in the file; no check reads the added runnability paragraph's content or asserts it distinguishes the routes correctly."
  - id: D3
    description: "'## Keeping derivatives in sync' (maintainer instruction) moved out of the install path, from between Install and Status to after Status"
    requirement: DIST-06
    verification:
      - kind: other
        ref: "ad-hoc heading-index probe: python3 -c \"...H=[...]\" confirms 'Keeping derivatives in sync' index > 'Status' index"
        status: pass
    human_judgment: true
    rationale: "No repository check enforces this heading's position; only the three headings readme-before-after-order tracks (Before and after, Install, Status) are gated. A future edit could move it back with no CI failure."
  - id: D4
    description: "Repository-layout legend and tree agree: all 19 '(exists)' markers and the unused 'planned' term removed, legend states every path shown exists, every filename in the tree resolves to a real file on disk"
    requirement: DIST-06
    verification:
      - kind: other
        ref: "ad-hoc probes: t.count('(exists)')==0, t.count('planned')==0, and a filename-existence scan over the fenced tree returning an empty missing list"
        status: pass
    human_judgment: true
    rationale: "04-09 registers readme-layout-legend-drift to make this permanent; today's 0/0 counts are this session's measurement, not yet a CI gate."
  - id: D5
    description: "Before/after lead-in no longer claims every rule in the catalog exists to turn a paragraph into its rewrite (false for PF-5.1-PF-5.3 and PF-2.14-PF-2.17)"
    requirement: DIST-06
    verification:
      - kind: other
        ref: "grep -c 'Every rule' README.md == 0"
        status: pass
    human_judgment: true
    rationale: "The grep is a literal-string proxy for the narrowed claim's absence; whether the replacement sentence itself is accurate to the catalog is a semantic judgment no check performs."
  - id: D6
    description: "Status caveat no longer asserts 'both measured models are Anthropic-hosted' when only claude-sonnet-5 sits behind the anchored MOD-04 figures; claude-sonnet-5 is now named explicitly and claude-opus-5's superseded, unanchored sessions are disclosed"
    requirement: DIST-06
    verification:
      - kind: other
        ref: "python3 -c \"'both measured models' in t, len(re.findall(r'claude-(?:sonnet|opus)-5',t))\" -> (False, 3)"
        status: pass
    human_judgment: true
    rationale: "The probe confirms the literal over-broad phrase is gone and a model identifier is present; whether the rewritten sentence accurately represents RESULTS-mod04.md's anchored-vs-superseded distinction is a semantic judgment."
  - id: D7
    description: "The full gate holds at 44 codes discrimination-proven throughout both tasks, with 0 violations and 0 unexpected CONTROL"
    requirement: DIST-06
    verification:
      - kind: integration
        ref: "python3 tools/check_repo.py --self-test"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py --mutation-test"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py"
        status: pass
      - kind: integration
        ref: "python3 tools/generate_derivatives.py --check"
        status: pass
    human_judgment: false

duration: 35min
completed: 2026-09-17
status: complete
---

# Phase 4 Plan 08: README Gap-Closure (G-04-6) Summary

**Repaired all six concrete README defects `04-UAT.md` test 4 found — moved the before/after pair to lead the file, stated each install route's runnability, relocated maintainer instruction below Status, and narrowed two unmeasured claims — while holding the gate at 44 codes discrimination-proven throughout.**

## Performance

- **Duration:** 35 min
- **Started:** 2026-09-17T10:05:00Z (approx.)
- **Completed:** 2026-09-17T10:40:00Z (approx.)
- **Tasks:** 2 completed
- **Files modified:** 1 (`README.md`)

## Accomplishments

- **Defect (f) — lead distance.** Moved `## Before and after` to be the first `## ` heading in the file, ahead of `## What this is`. The first `✗` line moved from **line 23** to **line 14**, well inside the first screen and under the 20-line ceiling — achieved purely by the section move, with no lead-in wording change required for the line budget.
- **Defect (a) — install runnability.** Added one paragraph to `## Install`, immediately after the existing publish-location sentence, stating that routes 3 and 4 (output style, system prompt) work today from a local clone, and routes 1 and 2 (skills CLI, Claude Code marketplace) name the disclosed `<owner>/<repo>` placeholder and will not resolve until the repository is published.
- **Defect (c) — maintainer instruction relocated.** Moved `## Keeping derivatives in sync` from between `## Install` and `## Status` to immediately after `## Status`, out of a first-time reader's install path. Body, heading, and the named `python3 tools/generate_derivatives.py` command are unchanged.
- **Defect (e) — unmeasured catalog claim narrowed.** The before/after lead-in no longer claims "every rule in this skill exists to turn a paragraph like the one on the left into the one on the right" (false for PF-5.1-PF-5.3 and PF-2.14-PF-2.17, which govern check mode and review markers, not paragraph rewriting). Narrowed to: "the rules cited below turned a paragraph like the one on the left into the one on the right."
- **Defect (d) — measured-models caveat corrected.** The Status caveat no longer states "both measured models are Anthropic-hosted" while naming only one in the figures above it. Now names `claude-sonnet-5` explicitly as the model behind the anchored figures and states that `RESULTS-mod04.md`'s `claude-opus-5` sessions are superseded and unanchored.
- **Defect (b) — layout legend and tree reconciled.** Removed all 19 `(exists)` markers from the fenced repository tree and the legend's reference to a `planned` marker that appeared zero times in the tree. The legend now states plainly that every path shown exists in this repository today — verified by resolving every filename in the tree against the working directory (empty missing list).
- **Gate integrity held throughout.** `python3 tools/check_repo.py --self-test` passes, `--mutation-test` reports `44 codes discrimination-proven` with `0 unexpected` on CONTROL and no FIRE-ONLY line, `check_repo.py` prints `check_repo: 0 violations`, and `generate_derivatives.py --check` exits 0 — unchanged from the 04-07 baseline. This plan registered no new violation code.

## Task Commits

Each task was committed atomically:

1. **Task 1: Restructure — lead with the example, state each route's runnability, move maintainer instruction out of the install path** - `b59dba6` (docs)
2. **Task 2: Narrow the two unsupported claims and repair the self-contradicting layout legend** - `6c50822` (docs)

**Plan metadata:** (this commit, made after this SUMMARY)

## Files Created/Modified

- `README.md` — before-and-after section relocated to lead the file; a runnability paragraph added to Install; `## Keeping derivatives in sync` relocated below `## Status`; the before/after lead-in narrowed; the measured-models caveat corrected; all 19 `(exists)` markers removed from the layout tree and the legend sentence rewritten.

## Decisions Made

- Defect (d) resolved by naming `claude-sonnet-5` explicitly rather than dropping the model count silently — keeps the caveat concrete and checkable (`claude-(?:sonnet|opus)-5` still matches) rather than vaguer.
- No lead-in wording trim was needed to satisfy the 20-line ✗-line ceiling: the section move alone (Task 1) achieved line 14. The sentence-level narrowing of the lead-in (defect e) was made independently in Task 2, exactly as the plan's task boundary specified.
- Kept the `README.md` tree entry's `— this file` annotation while dropping only the `(exists` marker text, since the annotation itself carries no marker-vocabulary claim and remains useful orientation.

## Deviations from Plan

None — plan executed exactly as written. Both tasks' full `<verify>` and `<acceptance_criteria>` blocks were run and passed on the first attempt; no auto-fix, blocking issue, or architectural question arose.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `04-09` can now register `readme-example-drift`, `readme-example-lead-distance`, and `readme-layout-legend-drift` against this repaired structure: the first ✗ line is at 14 (would have been FIRE-ONLY at the pre-plan 23), and the layout legend now agrees with the tree (would also have been FIRE-ONLY against the pre-plan `planned`/`(exists)` mismatch).
- **Residual not closed by this plan** (per the plan's own `<artifacts_this_phase_produces>` instruction): whether README genuinely reads well to a first-time reader — the `verification: backstop` truth in this plan's `must_haves` — stays a semantic judgment no code in this repository performs. `.planning/WINDOWS.md` entry 12 (DIST-06's prose-quality half, unrun-verify, open) is unchanged by this plan and should be re-evaluated by the phase's verification step once `04-09` lands, per the plan's explicit instruction not to close or reclassify it here.
- `REQUIREMENTS.md`'s DIST-06 row already reads `[x]` with an UNVERIFIED caveat and an explicit instruction not to re-mark Complete from a SUMMARY's `requirements-completed` field; this SUMMARY copies `[DIST-06]` from the plan frontmatter per the summary template's contract, but does not itself attempt to flip or otherwise alter that row — closure of DIST-06's prose-quality half remains routed through end-of-phase verification, unaffected by this field.

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-17*
