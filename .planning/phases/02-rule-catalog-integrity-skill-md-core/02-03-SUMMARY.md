---
phase: 02-rule-catalog-integrity-skill-md-core
plan: 03
subsystem: rule-catalog
tags: [agent-skill, skill-md, rule-catalog, integrity, ci-checker]

# Dependency graph
requires:
  - phase: 02-rule-catalog-integrity-skill-md-core
    provides: "02-01's frozen three-file skills/proof-first/ folder, the marker grammar (GAP/REVIEW/retention), the 31-rule ID allocation map, catalog-id-drift; 02-02's PF-1 Command of the Message spine and the 247-line mid-draft checkpoint"
provides:
  - "PF-2 — Proof and integrity, completed: four Proof rules (PF-2.1-PF-2.4) that attach evidence, name its source, and license confidence by adjacency; seven Integrity rules (PF-2.11-PF-2.17) — two refusals against invented metrics/references and five markers, four of which are the numbered presales hazards (commitment, reference, competitor, compliance)"
  - "The closed REVIEW category-to-rule mapping stated once in SKILL.md, machine-checkable via a plain grep"
affects: [02-04, 02-05, 02-06]

# Actuals (#2632)
actuals:
  tokens: 3035
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A generic bracket-form placeholder in explanatory prose (e.g. 'REVIEW (category)') can accidentally satisfy the same regex a later acceptance criterion uses to count real category instances — reworded to a non-matching form (angle-bracket placeholder) rather than loosening the check, mirroring 02-02's currency-regex avoidance pattern"
    - "Mechanical (no-example) vs judgment-carrying (worked ✗/✓ pair) rule bodies coexist inside the same numbered section, distinguished only by D-02's own criterion, not by a sub-heading — verified structurally via an awk range scan rather than visual inspection"

key-files:
  created: []
  modified:
    - skills/proof-first/SKILL.md
    - skills/proof-first/references/checklist.md
    - NUMBERING.md

key-decisions:
  - "The pre-existing Marker vocabulary section's illustrative bracket form used the literal placeholder text 'REVIEW (category)', authored by 02-01 before any concrete REVIEW category existed in the file. Once PF-2.14-PF-2.17 introduced the four real categories, that placeholder satisfied the same 'REVIEW (\\w+)' pattern this plan's own acceptance criterion uses to assert exactly four categories exist. Reworded the placeholder to 'REVIEW (<one of the four categories below>)', which does not match the regex, without touching the frozen bracket grammar, keyword casing, or category vocabulary itself (Rule 1 bug fix)."
  - "PF-2.1 through PF-2.4 (Proof) carry no ✗/✓ example per D-02's mechanical-rule criterion; PF-2.12 through PF-2.17 (Integrity, six new rules) each carry exactly one, matching PF-2.11's existing shape. Kept every Proof rule body at or under 6 lines and every new Integrity rule body at or under 12, leaving the file at 373 lines against the 430-line Task-2 ceiling and the 500-line CAT-08 hard ceiling, with 02-04's nine rules still to come."
  - "PF-2.16's ✗ example draws on the incumbent's 62% estate share (a Canonical-figures percentage) rather than an invented figure, and PF-2.14's ✗/✓ pair draws on the 8-month examination window against the 14-month comparable-programme duration, keeping every worked figure traceable to examples/deal-brief.md's Canonical figures table (unlisted-figure enforced)."

requirements-completed: [CAT-02, INT-01, INT-02, INT-03, INT-04, INT-05, INT-06]

coverage:
  - id: D1
    description: "PF-2 — Proof and integrity authored in full: PF-2.1-PF-2.4 (Proof, mechanical, no example) attach evidence, name its source, and license confidence by adjacency without hedging; PF-2.12/PF-2.13 (Integrity refusals/gaps) refuse an invented reference and mark an additive-sweep absence like any other gap; PF-2.14-PF-2.17 (Integrity hazards) are four separately numbered, citable rules each raising its own frozen REVIEW category (commitment, reference, competitor, compliance)"
    requirement: "CAT-02, INT-01, INT-02, INT-03, INT-04, INT-05, INT-06"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (live run, both tasks) — check_repo: 0 violations"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test (Task 2, full CI job order) — self-test PASS, mutation-test PASS: 13 codes proven live"
        status: pass
      - kind: other
        ref: "~20 acceptance-criteria grep/awk one-liners from 02-03-PLAN.md Tasks 1-2 (heading order/count, Replace-with count, stated-count sentence, NUMBERING.md/checklist.md row counts and reserved-range counters, no-example check on Proof rules, exampled check on all six new Integrity rules, four REVIEW categories exactly, per-hazard category match, ID-range containment, line-count ceiling)"
        status: pass
    human_judgment: true
    rationale: "SOURCES.md's reproduction boundary (no framework wording reproduced) and the plan's own <human-check> (PF-2.11/PF-2.12 read as refusals not preferences with no marker-substituting figure or anonymised client; PF-2.14's example does not itself create a warranty and PF-2.17's example states the narrower truth rather than omitting the SOC 2 gap; the Integrity section discusses authorization/disclosure, not only fabrication) are semantic judgments no tool in this project's stack performs. Per workflow.human_verify_mode=end-of-phase this is harvested into the phase's UAT batch rather than halting this plan, exactly as 02-01's and 02-02's equivalent human-checks were deferred. A self-read against all three points during execution found no issue in any of them (see Next Phase Readiness)."
  - id: D2
    description: "NUMBERING.md and references/checklist.md stay in agreement with SKILL.md's defined headings and stated count sentence at both task boundaries (16/16/16 after Task 1, 22/22/22 after Task 2); PF-2's Allocated/Next-free counters updated twice (1->5->11 Allocated, PF-2.12->PF-2.12->PF-2.18 Next free)"
    requirement: "CAT-02"
    verification:
      - kind: integration
        ref: "catalog-id-drift (mutation-test, re-proven live after content growth) + awk row-count/reserved-range checks against NUMBERING.md and checklist.md"
        status: pass
    human_judgment: false
  - id: D3
    description: "Every PF-2 ID respects the Proof (PF-2.1-PF-2.10) / Integrity (PF-2.11-PF-2.20) sub-block boundary NUMBERING.md declares, and the closed REVIEW category vocabulary (commitment/reference/competitor/compliance) maps one-to-one onto PF-2.14-PF-2.17 with no other category appearing anywhere in the file"
    requirement: "INT-03, INT-04, INT-05, INT-06"
    verification:
      - kind: other
        ref: "grep -oE '^### PF-2\\.[0-9]+' | sed range-containment check -> '1 2 3 4 11 12 13 14 15 16 17'; grep -oE 'REVIEW \\([a-z]+\\)' | sort -u -> exactly commitment/competitor/compliance/reference"
        status: pass
    human_judgment: false

duration: 14min
completed: 2026-09-11
status: complete
---

# Phase 2 Plan 3: PF-2 Proof and Integrity Summary

**Eleven PF-2 rules now stand complete in `SKILL.md` — four mechanical Proof rules that attach evidence and license confidence by adjacency, and seven Integrity rules where the four presales hazards (commitment, reference, competitor, compliance) are each a separately numbered, citable rule raising its own frozen REVIEW category — catalog now states 22 rules in 4 sections at 373 lines.**

## Performance

- **Duration:** 14 min
- **Started:** 2026-09-11T00:49:00Z
- **Completed:** 2026-09-11T01:03:00Z
- **Tasks:** 2 (both `type="auto"`)
- **Files modified:** 3

## Accomplishments

- Authored the four Proof rules (Task 1): `PF-2.1` (every claim carries its evidence), `PF-2.2` (name the source of the evidence), `PF-2.3` (adjacent evidence licenses an unhedged claim — hedging is never the repair for missing evidence), `PF-2.4` (no evidence: cut the claim and mark the gap in its place) — placed before `PF-2.11` so the section reads in ascending ID order, opened with a paragraph naming the Proof/Integrity sub-block split.
- Authored the six remaining Integrity rules (Task 2): `PF-2.12` (never invent a reference customer, a logo, or a named account — a refusal, demonstrated with a marker rather than a plausible anonymised substitute), `PF-2.13` (an absence found by the additive sweep is marked like any other gap), `PF-2.14` (flag commitment-shaped language, drawn from the 8-month examination window against the 14-month comparable-programme duration), `PF-2.15` (flag customer reference details that need disclosure permission), `PF-2.16` (flag competitor comparisons, drawn from the incumbent's 62% estate share), `PF-2.17` (flag compliance, certification, and export claims, drawn from the SOC 2 Type I/Type II gap and the observation-window/submission-date mismatch — the example states the narrower truth rather than resolving the gap by omission).
- Closed the section with one paragraph stating the closed REVIEW category-to-rule mapping.
- Registered all ten new IDs in `NUMBERING.md`'s Allocated IDs table (ascending) and updated PF-2's reserved-range counters (`Allocated` 1→5→11, `Next free` PF-2.12→PF-2.12→PF-2.18); added the matching ten rows to `references/checklist.md`.
- Updated the stated-count sentence twice (`12 rules in 4 numbered sections` → `16` → `22`), keeping SKILL.md, NUMBERING.md, and checklist.md in agreement at both checkpoints.
- Re-ran the full CI job order (`--self-test`, `--mutation-test`, live check) after Task 2's growth — all 13 violation codes still proven live, 0 live violations.

## Task Commits

1. **Task 1: PF-2 Proof — attach the evidence, name its source, and license confidence by adjacency** — `a5eafdb` (feat)
2. **Task 2: PF-2 Integrity — one refusal for invented references, and a numbered rule for each of the four presales hazards** — `5f8744e` (feat)

**Plan metadata commit:** recorded below after STATE.md/ROADMAP.md/REQUIREMENTS.md updates.

## Files Created/Modified

- `skills/proof-first/SKILL.md` — completed `## PF-2 — Proof and integrity` (11 rules total, 247→373 lines across the two tasks)
- `skills/proof-first/references/checklist.md` — 10 new PF-2 rows, ascending by ID
- `NUMBERING.md` — 10 new Allocated IDs rows, PF-2 reserved-range counters updated twice

## Decisions Made

- The pre-existing Marker vocabulary section (authored by 02-01, before any concrete REVIEW category existed) used the literal placeholder `REVIEW (category)`. Once this plan introduced the four real categories, that placeholder collided with the `REVIEW (\w+)` pattern this plan's own acceptance criterion uses to assert exactly four categories exist anywhere in the file. Reworded the placeholder to `REVIEW (<one of the four categories below>)` — the regex no longer matches it, and the frozen bracket grammar, keyword casing, and the four category names themselves are unchanged. See Deviations below.
- Every worked figure in this plan's new ✗/✓ pairs (`8-month`, `14 months`, `62%`, `2026-10-30`) traces to `examples/deal-brief.md`'s Canonical figures table, keeping `unlisted-figure` clean without inventing any fact.
- Kept Proof rule bodies at or under 6 lines (no example, per D-02) and new Integrity rule bodies at or under 12 lines (one ✗/✓ pair each), landing the file at 373 lines — comfortably under the 430-line Task-2 ceiling and the 500-line CAT-08 hard ceiling, with 02-04's nine remaining rules still to come.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Reworded the Marker vocabulary section's `REVIEW (category)` placeholder to stop it satisfying the four-category grep check**
- **Found during:** Task 2, acceptance-criteria verification pass (`grep -oE 'REVIEW \([a-z]+\)' skills/proof-first/SKILL.md | sort -u`)
- **Issue:** 02-01's Marker vocabulary section illustrates the REVIEW bracket form with the placeholder text `[<rule> REVIEW (category): what needs confirming]`. That placeholder is itself matched by the same regex this plan's own acceptance criterion (and, later, Phase 5's linter) uses to enumerate real REVIEW categories — so the file reported five distinct matches (`category`, `commitment`, `competitor`, `compliance`, `reference`) instead of exactly the four this catalog defines.
- **Fix:** Reworded the placeholder to `[<rule> REVIEW (<one of the four categories below>): what needs confirming]`, which does not match the `REVIEW \([a-z]+\)` pattern. The bracket form, the keyword `REVIEW`, and the four category names/mapping are unchanged — only the illustrative placeholder text moved from a literal fifth pseudo-category to a non-matching angle-bracket description.
- **Files modified:** `skills/proof-first/SKILL.md`
- **Verification:** `grep -oE 'REVIEW \([a-z]+\)' skills/proof-first/SKILL.md | sort -u` → exactly `REVIEW (commitment)`, `REVIEW (competitor)`, `REVIEW (compliance)`, `REVIEW (reference)`; `python3 tools/check_repo.py` → `check_repo: 0 violations`.
- **Committed in:** `5f8744e` (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug).
**Impact on plan:** No scope creep — the fix only reworded one illustrative placeholder string in prose written by an earlier plan; no rule content, marker grammar, or category vocabulary was touched.

### Acceptance-Criterion Discrepancy (verification-script bug, not an implementation defect)

**The Allocated-IDs `sort -c` ordering check fails, but it already failed on the file exactly as 02-02 left it, before this plan changed anything.**

Task 1's acceptance criteria include:
```
awk '/^## Allocated IDs/{f=1;next} /^## /{f=0} f && /^\| PF-/ {split($0,c,"|"); gsub(/ /,"",c[2]); print c[2]}' NUMBERING.md | sort -c
```
expected to exit 0. Running this exact command against the file as committed by 02-02 (`git show fb5f6f1:NUMBERING.md`, before any of this plan's edits) already fails: `sort: disorder: PF-1.13`, exit 1. `NUMBERING.md`'s own "Rows are kept sorted ascending by ID" convention treats an ID's suffix as a dotted integer pair (`PF-1.2` < `PF-1.5` < `PF-1.9` < `PF-1.13`), which is not the same order plain ASCII `sort` produces (`PF-1.13` < `PF-1.2` byte-for-byte, since `'1' < '2'` at the fourth character). This mismatch was already present the moment `PF-1.13` and `PF-1.2` first coexisted in the table (02-02), independent of anything this plan authored — confirmed by running the identical command against the pre-plan file and observing the identical first failure point. Rows added by this plan (`PF-2.1`-`PF-2.4`, `PF-2.12`-`PF-2.17`) were placed in the same established dotted-integer ascending order as every other section (verified separately via the `grep -oE '^### PF-2\.[0-9]+'` heading-order check and the `sed '.*\.'` numeric range-containment check, both of which pass), so the substantive requirement — IDs sorted ascending by the convention this file itself defines and every other plan has followed — is met. No code in `tools/check_repo.py` depends on this exact `sort -c` shape; `parse_numbering` reads the table by row, not by verifying byte-order. This is the same class of pre-existing verification-script discrepancy 02-01 documented for the `## PF-2 sub-blocks` row-count awk pattern.

## Issues Encountered

None beyond the deviation and acceptance-criterion discrepancy documented above.

## Authentication Gates

None — no external service or CLI authentication was required.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `PF-2`'s eleven rules are complete and registered; `02-04` can allocate `PF-3.2`/`PF-3.3`, `PF-4`, and `PF-5` without renumbering anything here.
- The measured 373-line total (up from 247 after 02-02) stays comfortably under both the 430-line Task-2 ceiling this plan set for itself and the 500-line CAT-08 hard ceiling, with 02-04's nine rules still to author.
- Self-read of the plan's `<human-check>` during execution (not a formal sign-off, since `workflow.human_verify_mode=end-of-phase` defers the formal one to phase-end UAT): (1) `PF-2.11`/`PF-2.12` read as refusals — "Refuse to state...", "Refuse to name..." — and neither `✓` line substitutes a plausible figure or an anonymised client for the marker; (2) `PF-2.14`'s example states a fact and a review marker without itself promising a date, and `PF-2.17`'s example states the SOC 2 Type I/Type II gap plainly rather than omitting it; (3) `PF-2.15` discusses disclosure permission specifically, so the Integrity section is not fabrication-only. Open item carried into end-of-phase UAT for an actual human sign-off, per the same deferral 02-01/02-02 used.
- No blockers for `02-04`.

## Self-Check: PASSED

- `[ -f skills/proof-first/SKILL.md ]` → FOUND
- `[ -f skills/proof-first/references/checklist.md ]` → FOUND
- `[ -f NUMBERING.md ]` → FOUND
- `git log --oneline --all | grep -q a5eafdb` → FOUND
- `git log --oneline --all | grep -q 5f8744e` → FOUND
- `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` → all green, 13 codes proven live, 0 live violations
- All Task 1 and Task 2 acceptance criteria re-run: all PASS except the pre-existing `sort -c` script discrepancy documented above (does not affect any code-enforced check)
- File-wide `### PF-` heading count (22) = `**Replace with:**` line count (22) = checklist.md PF row count (22) = NUMBERING.md Allocated IDs PF row count (22) = the stated rule count (22)

---
*Phase: 02-rule-catalog-integrity-skill-md-core*
*Completed: 2026-09-11*
