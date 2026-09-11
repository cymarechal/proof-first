---
gsd_state_version: 1.0
current_phase: 02
current_phase_name: Rule Catalog & Integrity — SKILL.md Core
status: executing
stopped_at: Completed 02-03-PLAN.md
last_updated: "2026-09-11T00:57:50.547Z"
last_activity: 2026-09-11
last_activity_desc: Phase 02 execution started
state_head: df594ff06ebbcd68be571f9a16348166a28b98c0
progress:
  total_phases: 6
  completed_phases: 1
  total_plans: 13
  completed_plans: 10
  percent: 17
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-10)

**Core value:** A technical evaluator finishes the document believing the author genuinely understands their problem — because complex things were made simple without being made wrong.
**Current focus:** Phase 02 — Rule Catalog & Integrity — SKILL.md Core

## Current Position

Phase: 02 (Rule Catalog & Integrity — SKILL.md Core) — EXECUTING
Plan: 4 of 6
Status: Ready to execute
Last activity: 2026-09-11 — Phase 02 execution started

Progress: [██░░░░░░░░] 17%

## Performance Metrics

**Velocity:**

- Total plans completed: 7
- Average duration: - min
- Total execution time: 0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01 | 7 | - | - |

**Recent Trend:**

- Last 5 plans: none yet
- Trend: -

*Updated after each plan completion*
**Per-Plan Metrics:**

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| Phase 01 P01 | 20 min | 2 tasks | 5 files |
| Phase 01 P02 | 24 min | 2 tasks | 2 files |
| Phase 01 P03 | 12min | 3 tasks | 3 files |
| Phase 01 P04 | 20min | 2 tasks | 1 files |
| Phase 01 P05 | 35 min | 2 tasks | 1 files |
| Phase 01 P06 | 30 min | 3 tasks | 1 files |
| Phase 01 P07 | 25 min | 2 tasks | 2 files |
| Phase 02 P01 | 11 min | 3 tasks | 5 files |
| Phase 02 P02 | 8 min | 2 tasks | 3 files |
| Phase 02 P03 | 14min | 2 tasks | 3 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Roadmap: 6 phases derived from 53 v1 requirements at "standard" granularity — matches research's suggested structure after independent validation against the actual requirement set.
- Roadmap: CAT-07 (numbering namespaces) and EX-01 (shared deal brief) frozen in Phase 1, not treated as later cleanup — retrofitting reserved ranges after organic numbering would force the exact renumbering the scheme exists to prevent.
- Roadmap: MOD-03/04/05 (three-category check output, artifact classification, citation guarantee) placed in Phase 3, not Phase 2, because they have real dependencies on the MEDDICC checklist and artifact patterns; MOD-01/02 (basic draft/check) stay in Phase 2 since they only need the prose catalog.
- Roadmap: LEG-04 (legal review gate) and LEG-05 (README badges) held to a dedicated Phase 6, separate from Phase 1's general legal scaffolding (LEG-01/02/03) — the MEDDIC/MEDDICC/MEDDPICC trademark litigation risk is load-bearing, not a footnote.
- Roadmap: Phase 4 (distribution) and Phase 5 (eval harness) both depend only on Phases 2-3 and not on each other — flagged as parallelizable given config's parallelization setting.
- [Phase 01]: 01-01: PF-1 ceiling resolved to PF-1.28 (widen-to-28) via the plan's blocking-human checkpoint -- four slots per Command of the Message element (Before scenario 1.1-1.4, After scenario 1.5-1.8, Required Capabilities 1.9-1.12, Metrics 1.13-1.16, Proof Points 1.17-1.20, Differentiators 1.21-1.24, Positive Business Outcomes 1.25-1.28), superseding the PF-1.20 research proposal.
- [Phase 01]: 01-01: Canonical figures and attribution pointer registries frozen -- 6-key Canonical figures table in examples/deal-brief.md ($6M/3yr deal, 3 bidders, 62% incumbent share, 55% scoring weight, 2026-10-30 submission date) and the verbatim NOTICES.md attribution pointer string with its 4-file carriers list, both enforced by tools/check_repo.py in CI.
- [Phase 01]: [Phase 01]: 01-02: examples/deal-brief.md completed with the full deal spine, an 18-key Canonical figures table (adding annual-run-rate-current, examination-window-months, legal-review-days, oracle-database-count, rfp-commercial-weight, rfp-question-weight-mid, rfp-question-weight-top, rfp-security-weight, security-review-days, settlement-batch-window-hours, vendor-comparable-duration-months, vm-count), and renamed rfp-technical-scoring-weight to rfp-technical-weight (value unchanged, 55%) to match the plan's own verify script.
- [Phase 01]: [Phase 01]: 01-02: Inconvenient facts (unmeasured settlement-batch overrun, SOC 2 Type II gap, technical evaluator's stated incumbent preference, examination window shorter than Kestrel's comparable-programme duration) and Customer source material (5 scored RFP questions Q1-Q5 weighted 30/20/15/15/20, discovery quotes incl. verbatim "landing zone", economic-buyer priorities, decision criteria, paper process) added per D-08.
- [Phase 01]: [Phase 01]: 01-02: Task 2's two <manual> reviewer checks (name-collision web search over 9 invented names; no-real-product-comparison read-through) could not be completed in this environment (no live network access) -- logged as open unrun-verify items in .planning/WINDOWS.md pending human confirmation before the repo goes public.
- [Phase 01]: 01-03: All 6 SOURCES.md rows marked unverified (Where: 'to confirm at LEG-04') rather than confirmed -- this execution environment has no live network access to check a public location, so no citation is asserted as checked even for high-confidence titles (Dixon/Adamson's 'The Challenger Sale'; Andy Whyte's 'MEDDICC').
- [Phase 01]: 01-03: NOTICES.md's MEDDIC-family framework statement records ownership as claimed by multiple parties and contested, with no single holder named and no claim on mark validity or litigation outcomes -- matching the standing STATE.md blocker and D-13.
- [Phase 01]: 01-03: LICENSE/NOTICES.md scope boundary established -- LICENSE governs copyright only (unmodified MIT text), NOTICES.md governs trademark/attribution/precedence, and all repo content is MIT-licensed unless a file states otherwise.
- [Phase 01]: [Phase 01]: 01-04: README.md written at repo root (six sections: What this is, Status, Repository layout, Rule numbering, Versioning, License and notices) -- claim-free per LEG-05/PROJECT.md's evidence rule, documents the target layout (skills/proof-first/ and the rest) without pre-creating any of it, and is proven as the first real (non-fixture) carrier of NOTICES.md's attribution pointer.
- [Phase 01]: [Phase 01]: 01-04: Full-repository integrity sweep and phase-closing legal read completed -- all eight Phase 1 files present/non-empty/checker-clean, no framework mark outside NOTICES.md, no proprietary framework text reproduced anywhere. Phase 1 is internally consistent and complete; LEG-04/LEG-05 and the WINDOWS.md open items remain correctly deferred to Phase 6.
- [Phase 01]: [Phase 01]: 01-05: Attribution-pointer parsing rewritten on split_sections() with a new pointer-unparseable code and carrier-path containment, closing the CR-01/BLOCKER false-green defect against production NOTICES.md/README.md content.
- [Phase 01]: 01-06: check_repo.py's three open WARNINGs closed -- unlisted-figure's exempt region bounded by the Canonical figures table's own rows (not just the next heading), MC ID range enforcement split into per-dimension blocks (mc_ranges) instead of one aggregate range, and both undeclared ceilings (value-collision matching, code-point key ordering) written into the module docstring with a pinned fixture. WR-02's stronger key-binding fix deferred to a later phase (likely Phase 5) since it would rewrite the frozen Canonical figures interface. — Closes the WARNING-class findings 01-VERIFICATION.md and 01-REVIEW.md left behind the BLOCKER; the plan's own must_haves required per-block MC enforcement and end-of-file figure coverage as CAT-07/EX-01 edge cases.
- [Phase 01]: 01-07: --mutation-test mode added to tools/check_repo.py, injecting one named defect per violation code (all 10) into a throwaway copy of the real repository and asserting it fires; wired into CI between the self-test and the live check, closing the regression class behind Phase 1's BLOCKER rather than only today's instances. — The verifier's strongest evidence was a manual mutation (delete the pointer line, observe 0 violations); committing that method as a CI-enforced mode prevents any future edit from silently making a check inert again.
- [Phase 02]: 02-01: Checkpoint resolved adopt-as-proposed — marker keywords GAP/REVIEW (categories commitment/reference/competitor/compliance), register heading '## Unresolved before this document is sent', and the 31-rule ID allocation map frozen exactly as proposed, no field amended. — These become one-way interfaces Phases 3-5 bind to (check output grouping, committed examples, linter parsing); amending after adoption would invalidate published artifacts.
- [Phase 02]: 02-01: SKILL.md's marker-vocabulary section uses a <rule> placeholder instead of the checkpoint's illustrative concrete IDs (PF-2.17, PF-3.3), since those sub-rules are allocated by later plans (02-03/02-04) and citing them now would fail undefined-id. — The marker grammar itself (bracket form, keywords, categories, rule-number-first ordering) is unchanged from the frozen decision — only the illustrative example numbers are deferred.
- [Phase 02]: [Phase 02]: 02-02: PF-1's nine rules reference two future rule mechanisms (a PF-5 before/after presence check, a PF-2 competitor-flag rule) whose IDs are not yet allocated -- worded as prose describing the mechanism's catalog location rather than citing the literal unallocated PF-#.# token, avoiding the same undefined-id forward-reference trap 02-01 already hit.
- [Phase 02]: [Phase 02]: 02-02: unlisted-figure's currency regex absorbs a trailing sentence-punctuation comma into the matched token, turning a valid Canonical figures value into a reported-unmatched string -- fixed by rewording two example sentences (not touching the checker), a declared ceiling of the existing tool rather than a defect.
- [Phase 02]: [Phase 02]: 02-03: PF-2 Proof and Integrity complete — eleven rules (PF-2.1-PF-2.4 Proof, PF-2.11-PF-2.17 Integrity), each of the four presales hazards (commitment/reference/competitor/compliance) its own numbered rule raising its own frozen REVIEW category. Reworded 02-01's generic 'REVIEW (category)' placeholder to avoid colliding with the four-category grep check (Rule 1 bug fix, grammar unchanged).

### Pending Todos

None yet.

### Blockers/Concerns

- MEDDICC/MEDDIC trademark status beyond the "MEDDPICC ruled generic" ruling (E.D. Pa., April 2026) is unresolved. Must be reconfirmed against current sources before Phase 6's legal review gate (LEG-04) closes — do not assume the whole acronym family is safe by extension.
- Linter's buzzword-proxy word list (EVAL-02) must be sourced independently from SKILL.md's own worked examples, or the Phase 5 benchmark becomes circular — flag explicitly during Phase 5 planning, not left implicit.
- README badges (LEG-05) have a hard dependency on Phase 5's benchmark having actually run — sequence Phase 6 accordingly, do not draft badge claims early.
- RESOLVED 2026-09-10: both .planning/WINDOWS.md unrun-verify items (name-collision web search over the 9 invented names; independent read-through confirming no real-product/company comparison) were signed off at Phase 01 UAT. Ledger open_count is now 0.
- `.planning/` is git-tracked and its research files carry framework marks in headings (`### ...MEDDICC...`, `### ...Challenger...`, `### Command of the Message...`). The Phase 01 mark sweep covered the eight shipped files only. Before the repo goes public, either exclude `.planning/` or extend the sweep to it — routed to Phase 6 LEG-04. Recorded in 01-SECURITY.md Observations.
- `pointer-*` checks in tools/check_repo.py still cannot fire when NOTICES.md is absent (`run_notices_checks()` early-returns). The equivalent hole in the LEG-02 check was closed in Phase 01; this one was left as out-of-scope. Same "check that cannot fire" class — worth a ticket.

## Deferred Items

Items acknowledged and deferred at milestone close, most recent first:

| Category | Item | Status | Deferred At | Milestone |
|----------|------|--------|-------------|-----------|
| *(none)* | | | | |

## Session Continuity

Last session: 2026-09-11T00:57:50.467Z
Stopped at: Completed 02-03-PLAN.md
Resume file: None
