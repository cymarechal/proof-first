---
phase: 03-completeness-audit-artifact-patterns
plan: 01
subsystem: rule-catalog
tags: [agent-skill, skill-md, mc-namespace, completeness-audit, ci-checker, mutation-test]

# Dependency graph
requires:
  - phase: 02-rule-catalog-integrity-skill-md-core
    provides: the 31-rule PF catalog, checklist.md/deletion-test.md/worked-examples.md shapes, and the check_repo.py D-34 triad pattern this plan's MC-namespace additions mirror
provides:
  - "The MC-namespace pipeline proven end-to-end on one dimension (MC-1): reference file, NUMBERING.md registration, checklist index, SKILL.md pointer, and two new CI-enforced drift/structural checks"
  - "A shared _three_way_id_diff helper both catalog-id-drift (PF) and mc-catalog-id-drift (MC) now call, so future definitional-agreement rules cannot drift between the two namespaces"
  - "The frozen checkpoint decision (adopt-as-proposed): eight-ID MC allocation map, four-section check-mode report order, structural-ordering pass as its own section, four artifact-family headings -- binding on 03-02/03-03/03-04"
affects: [03-02, 03-03, 03-04]

# Actuals (#2632)
actuals:
  tokens: 4211
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "MC-namespace reference file modeled on deletion-test.md's shape (trigger paragraph, worked instance, closing 'What this file does not do' section) rather than on checklist.md or worked-examples.md"
    - "Shared three-way divergence comparison (_three_way_id_diff) parameterised by code string and an ordered (label, id_set) list, backing both the PF and MC drift checks"

key-files:
  created:
    - skills/proof-first/references/completeness-audit.md
  modified:
    - NUMBERING.md
    - skills/proof-first/SKILL.md
    - skills/proof-first/references/checklist.md
    - tools/check_repo.py

key-decisions:
  - "Checkpoint resolved adopt-as-proposed (orchestrator-verified against source, not a human user): eight-ID MC map at each dimension block's range start, check-mode section order Integrity flags -> Prose violations -> Completeness gaps -> Structural ordering, ordering pass as its own always-printing section, four artifact-family headings -- all frozen one-way interfaces for 03-02/03-03/03-04."
  - "Tracer feedback gate after Task 1: re-ran the automated <verify> commands and performed the <human-check> paraphrase-boundary reading myself (interactive/end-of-phase mode would normally halt for a checkpoint since the tracer's <verify> carries a <human-check>, but the resume instructions explicitly granted discretion to resolve non-blocking-human gates autonomously) -- passed, logged, and proceeded directly to Task 2 with no idle wait."
  - "mc-catalog-id-drift returns no violations when references/completeness-audit.md does not exist, checked before computing any set -- required because _good_numbering() (the fixture behind most self-test roots) already allocates MC-1/MC-5 with no completeness-audit.md anywhere in those roots; an unguarded implementation would have broken self-test across the whole suite."

requirements-completed: [AUD-02, MOD-05]

coverage:
  - id: D1
    description: "One real MC completeness check (MC-1, Metric dimension) authored in a new completeness-audit.md, registered in NUMBERING.md, indexed in checklist.md's new MC rules section, and pointed at from SKILL.md"
    requirement: AUD-02
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations)"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --self-test (mc-catalog-id-drift, mc-rule-in-skill both verified)"
        status: pass
    human_judgment: true
    rationale: "AUD-01's content-quality half (does MC-1's body read as a genuine completeness finding rather than an invented deficiency, and is it free of source reproduction under SOURCES.md's boundary) is prose-authoring correctness no checker can evaluate. I performed this human-check reading myself per the tracer feedback gate (see key-decisions) and it passed, but the plan's own <output> instructions require this be recorded as provisional pending end-of-phase UAT, not auto-passed off a self-check alone."
  - id: D2
    description: "Two new CI-enforced violation codes (mc-catalog-id-drift, mc-rule-in-skill) closing the MC namespace's registry-drift and never-blended enforcement gaps, each proven live against mutated production content"
    requirement: MOD-05
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test (24 codes discrimination-proven, up from 22; CONTROL: 0 violations; no code fire-only)"
        status: pass
    human_judgment: false

patterns-established:
  - "MC-namespace reference file shape: trigger paragraph naming exactly when to open it, an inherited-ID-order defensive note, one MC-<n> heading per dimension with a diagnostic body and exactly one **Replace with:** line, closed by a 'What this file does not do' section -- the shape 03-02 continues for the remaining seven MC dimensions."

duration: 20min
completed: 2026-09-14
status: complete
---

# Phase 3 Plan 1: Completeness Audit Tracer (MC-1) and Enforcement Summary

**One real MEDDICC-derived completeness check (MC-1, Metric) proven end-to-end through every Phase 3 layer, plus two new CI-enforced codes (`mc-catalog-id-drift`, `mc-rule-in-skill`) taking the mutation-test suite from 22 to 24 discrimination-proven codes.**

## Performance

- **Duration:** ~20 min (this continuation; the prior agent's Task 0 checkpoint dialogue is separately tracked)
- **Completed:** 2026-09-14
- **Tasks:** 2 (Task 0, the checkpoint decision, was resolved by the orchestrator before this continuation started)
- **Files modified:** 5 (1 created, 4 modified)

## Accomplishments

- Authored `skills/proof-first/references/completeness-audit.md`, a new MC-namespace reference file modeled on `deletion-test.md`'s shape, carrying MC-1 (the Metric dimension), the verbatim attribution pointer, an inherited-ID-order defensive note (A3-01), and a closing "What this file does not do" boundary section. Every figure in the file traces exactly to `examples/deal-brief.md`'s Canonical figures table.
- Registered `MC-1` in `NUMBERING.md`'s Allocated IDs table, indexed it in a new `## MC rules` section of `checklist.md`, and added exactly one pointer bullet to `SKILL.md`'s Reference files list naming the trigger condition. `SKILL.md` measured at 3,712 words / ~4,825 estimated tokens after the edit — a 175-token (~135-word) margin remaining, comfortably above the 120-word floor A3-02 set.
- Closed the MC namespace's two structural enforcement gaps in `tools/check_repo.py`: `mc-catalog-id-drift` (three-way registry/definition/checklist agreement per skill folder, silent when `completeness-audit.md` does not exist) and `mc-rule-in-skill` (fails the build if any `SKILL.md` defines an MC rule via heading, turning AUD-02's "never blended" requirement mechanical).
- Extracted `_three_way_id_diff`, the shared comparison body now backing both `check_catalog_id_drift` (PF, refactored, byte-identical output) and `check_mc_catalog_id_drift` (MC) — a future rule about definitional agreement is fixed once, not per namespace.
- Parameterised `parse_checklist(path, section_name='PF rules')` so both existing PF call sites are untouched and the new MC call site passes `'MC rules'`.
- `python3 tools/check_repo.py --self-test && --mutation-test && (bare run)` — the exact CI job order — all green. Mutation-test reports **24 codes discrimination-proven** (up from 22), control copy still `0 violations`, and no code reported fire-only.

## Task Commits

1. **Task 1: End-to-end "one completeness check is CI-visible in the installed skill" — MC-1 only** — `7b460fb` (feat)
2. **Task 2: Close the MC namespace's two enforcement gaps** — `79e9613` (feat)

**Plan metadata:** (this commit, following)

## Files Created/Modified

- `skills/proof-first/references/completeness-audit.md` — new MC-namespace reference file; MC-1 only
- `NUMBERING.md` — first MC Allocated IDs row (`MC-1`)
- `skills/proof-first/references/checklist.md` — new `## MC rules` section
- `skills/proof-first/SKILL.md` — one Reference files pointer bullet
- `tools/check_repo.py` — `MC_HEADING_RE`, `parse_completeness_audit`, `_three_way_id_diff`, `check_mc_catalog_id_drift`, `check_mc_rule_in_skill`, parameterised `parse_checklist`, refactored `check_catalog_id_drift`, two new self-test fixture pairs, two new `MUTATIONS` entries, two new module-docstring entries

## Decisions Made

- **Checkpoint (Task 0) resolved adopt-as-proposed**, by the orchestrator (not a human user), after independently verifying the proposal's premises against `02-CONTEXT.md` D-20/D-21, `SKILL.md`'s existing two-category Check mode shape, and `NUMBERING.md`'s MC reserved blocks table. All four frozen interfaces (eight-ID MC allocation map; check-mode section order `Integrity flags -> Prose violations -> Completeness gaps -> Structural ordering`; the ordering pass as its own always-printing section; the four artifact-family headings) are binding on `03-02`/`03-03`/`03-04`. Details in the checkpoint resolution this plan's continuation prompt carried.
- **Tracer feedback gate**: Task 1's `<verify>` carries a `<human-check>` (the paraphrase-boundary reading against `SOURCES.md`), and the project is in interactive/`end-of-phase` mode (`AUTO_CHAIN=false`, `AUTO_CFG=false` — confirmed via `gsd_run query config-get`), which per the checkpoint reference would normally STOP for a `checkpoint:human-verify` before expansion. My resume instructions explicitly granted discretion to resolve a non-`blocking-human` gate autonomously rather than idle-wait in a spawned continuation session with no human available to respond. I re-ran the tracer's automated verify commands and performed the human-check reading myself: confirmed no contiguous run of source wording, no source's ordered list reproduced (only one dimension authored, with an explicit defensive note on the inherited MC ID order), no source-coined term adopted as this repo's own label, and MC-1's body grounded entirely in `examples/deal-brief.md` facts rather than restating MEDDICC's own definition of "Metric." Logged the pass and proceeded directly to Task 2.
- **`mc-catalog-id-drift`'s absence guard is load-bearing, not optional**: `_good_numbering()`, the fixture behind most existing self-test roots (`good_catalog_root`, `line500_root`, `line501_root`, `token_good_root`, `token_bad_root`, etc.), already allocates `MC-1` and `MC-5` with no `completeness-audit.md` present in any of those roots. Without the early `if not audit_path.exists(): continue` guard, the new check would have reported every one of those roots as "MC ID allocated but undefined," breaking `--self-test` across the whole suite — exactly the trap the plan's `<interfaces>` block flagged as the single highest-risk detail.

## Deviations from Plan

None — plan executed exactly as written, including the exact fixture and mutation shapes specified in Task 2's `<action>` block.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `03-02` can now allocate the remaining seven MC IDs (`MC-6` through `MC-36`) directly against the frozen `<mc_allocation_map>`, author the MC stated-count sentence and its enforcing check (`mc-count-unstated`/`mc-count-mismatch`), and add MC worked pairs to `worked-examples.md` — all using the exact reference-file shape, checklist-section shape, and NUMBERING.md row shape this plan established and proved live.
- `03-03`/`03-04` can proceed against the frozen check-mode report order, structural-ordering-pass shape, and artifact-family headings from the Task 0 checkpoint decision without re-litigating them.
- **Provisional, not fully verified**: AUD-01 is only one of eight dimensions authored here, and only its structural half — the content-quality judgment (does MC-1 read as a genuine completeness finding) is recorded above as `human_judgment: true` pending end-of-phase UAT, per the plan's own instruction not to mark AUD-01 as a completed requirement from this plan. MOD-05's live-session half (a real check-mode conversation never inventing a number) remains permanently unverifiable by any file-reading checker in this repository.

## Self-Check: PASSED

- FOUND: skills/proof-first/references/completeness-audit.md, skills/proof-first/references/checklist.md, NUMBERING.md, tools/check_repo.py, skills/proof-first/SKILL.md
- FOUND commits: 7b460fb, 79e9613
- Re-ran `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` — all pass; mutation-test reports `PASS: 24 codes discrimination-proven`
- `skills/proof-first/references/` holds exactly 4 files (checklist.md, completeness-audit.md, deletion-test.md, worked-examples.md) — `artifact-patterns.md` correctly not pre-created

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-14*
