---
phase: 02-rule-catalog-integrity-skill-md-core
plan: 02
subsystem: rule-catalog
tags: [agent-skill, skill-md, rule-catalog, command-of-the-message, ci-checker]

# Dependency graph
requires:
  - phase: 02-rule-catalog-integrity-skill-md-core
    provides: "02-01's frozen three-file skills/proof-first/ folder, the marker grammar (GAP/REVIEW/retention), the register heading, the 31-rule ID allocation map, and catalog-id-drift"
provides:
  - "PF-1 — Structure: the nine-rule Command of the Message spine (PF-1.1, PF-1.2, PF-1.5, PF-1.9, PF-1.13, PF-1.14, PF-1.17, PF-1.21, PF-1.25) across all seven frozen sub-blocks, four sub-blocks with one rule and three with headroom unfilled"
  - "A measured mid-draft line count (247 lines) with a recorded projection (~446) against the 500-line ceiling, taken with two authoring plans still available to trim"
affects: [02-03, 02-04, 02-05, 02-06]

# Actuals (#2632)
actuals:
  tokens: 2536
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Avoid a digit-adjacent trailing comma right after a currency/percent/date token in worked prose — CURRENCY_RE's [\\d,]* character class greedily consumes a following comma even when it is sentence punctuation, not a thousands separator, which unlisted-figure then reports as an unmatched figure"
    - "Reference an unallocated forward PF ID by describing its section/mechanism in prose rather than citing the literal PF-#.# token, exactly as 02-01 did with its <rule> placeholder — undefined-id scans skills/ for any PF-#.# token regardless of surrounding context, so a correct-but-early citation fails the same way a wrong one would"

key-files:
  created: []
  modified:
    - skills/proof-first/SKILL.md
    - skills/proof-first/references/checklist.md
    - NUMBERING.md

key-decisions:
  - "PF-1.5's body needed to reference the future presence-requirement rule that will check the before/after pairing, but that rule's ID (in PF-5, Consistency and Voice) is not allocated until a later plan. Worded it as \"a later rule in this catalog's Consistency and Voice section\" instead of citing a concrete PF-5.n token, avoiding the exact undefined-id forward-reference trap 02-01 already hit and documented."
  - "PF-1.21 similarly needed to reference the future competitor-flag integrity rule (planned as roughly PF-2.16, not yet allocated) without citing it by ID — worded as \"this catalog's Proof and Integrity section addresses separately.\" The REVIEW (competitor) marker itself cites PF-1.21, this plan's own rule, which is allocated in the same commit."
  - "Kept the ✓ example for PF-1.2 ($2,300,000 run rate) and PF-1.25 (same figure) as separate sentences rather than comma-joined clauses, because unlisted-figure's currency regex greedily absorbs a directly-following comma into the matched token, turning a valid Canonical-figures value into an unmatched string. This is a property of the checker's declared ceiling, not a data error — documented in the checker's own docstring — so the fix was rewording the prose, not touching the checker."

requirements-completed: [CAT-01, CAT-02]

coverage:
  - id: D1
    description: "PF-1 — Structure section authored in SKILL.md with nine rules distributed across all seven Command of the Message sub-blocks (Before scenario x2, After scenario x1, Required Capabilities x1, Metrics x2, Proof Points x1, Differentiators x1, Positive Business Outcomes x1), each with a statement, a mandatory Replace-with half, and a worked ✗/✓ pair drawn from examples/deal-brief.md"
    requirement: "CAT-01, CAT-02"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (live run, both tasks) — check_repo: 0 violations"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test (Task 2, full CI job order) — self-test PASS, mutation-test PASS: 13 codes proven live"
        status: pass
      - kind: other
        ref: "~20 acceptance-criteria grep/awk one-liners from 02-02-PLAN.md Tasks 1-2 (heading counts, Replace-with counts, ID ordering, sub-block range containment, stated-count sentence, GAP/REVIEW marker presence, line-count ceiling)"
        status: pass
    human_judgment: true
    rationale: "SOURCES.md's reproduction boundary (no Command of the Message wording or ordered-list structure reproduced, concepts paraphrased at public-source generality) is a semantic judgment no tool in this project's stack performs. Per workflow.human_verify_mode=end-of-phase, this is harvested into the phase's end-of-phase UAT batch rather than halting this plan, exactly as 02-01's tracer rule bodies were."
  - id: D2
    description: "NUMBERING.md's Allocated IDs table, PF-1 Allocated/Next-free counters, and references/checklist.md's PF rows all agree with SKILL.md's defined headings and stated count sentence at both task boundaries (7/7/7 after Task 1, 12/12/12 after Task 2)"
    requirement: "CAT-01"
    verification:
      - kind: integration
        ref: "catalog-id-drift (mutation-test, re-proven live after content growth) + awk row-count/order checks against NUMBERING.md and checklist.md"
        status: pass
    human_judgment: false
  - id: D3
    description: "Mid-draft line-count checkpoint measured and recorded before the catalog is finished, per RESEARCH Pattern 1's stated remedy — not deferred to end of phase"
    requirement: "CAT-02"
    verification:
      - kind: other
        ref: "wc -l skills/proof-first/SKILL.md — 247 lines, at or below the plan's 320-line Task 2 acceptance ceiling"
        status: pass
    human_judgment: false

duration: 8min
completed: 2026-09-11
status: complete
---

# Phase 2 Plan 2: PF-1 Command of the Message Spine Summary

**Nine PF-1 rules authored across all seven frozen Command of the Message sub-blocks in `SKILL.md`, each with a `**Replace with:**` half and a worked ✗/✓ pair drawn from the shared deal brief — catalog now states 12 rules in 4 sections, measured at 247 lines against a projected ~446-line total with two authoring plans still left to trim.**

## Performance

- **Duration:** 8 min
- **Started:** 2026-09-11T00:38:56Z
- **Completed:** 2026-09-11T00:46:35Z
- **Tasks:** 2 (both `type="auto"`)
- **Files modified:** 3

## Accomplishments

- Authored `## PF-1 — Structure`, a new section in `SKILL.md` positioned between `PF-0` and `PF-2`, opening with a paragraph naming the seven Command of the Message sub-blocks in `NUMBERING.md`'s own order and stating that unfilled sub-blocks are intentional headroom.
- Authored the four opening-half rules (Task 1): `PF-1.1` (name the before state in the buyer's own terms), `PF-1.2` (name what it costs), `PF-1.5` (pair the after-state with its before), `PF-1.9` (state the capability before the product).
- Authored the five closing-half rules (Task 2): `PF-1.13` (name the measure and baseline), `PF-1.14` (name the baseline's provenance), `PF-1.17` (attach one comparable proof), `PF-1.21` (claim a differentiator only against a named alternative, with a `REVIEW (competitor)` marker), `PF-1.25` (tie the outcome to the priority of the person who owns it).
- Registered all nine IDs in `NUMBERING.md`'s Allocated IDs table (ascending) and updated PF-1's reserved-range counters (`Allocated` 0→4→9, `Next free` PF-1.1→PF-1.10→PF-1.26); added the matching nine rows to `references/checklist.md`.
- Updated the stated-count sentence twice (`7 rules in 4 numbered sections` → `12 rules in 4 numbered sections`), keeping SKILL.md, NUMBERING.md, and checklist.md in agreement at both checkpoints.
- Re-ran the full CI job order (`--self-test`, `--mutation-test`, live check) after Task 2's growth — all 13 violation codes still proven live, 0 live violations.
- Measured the mid-draft line count as RESEARCH Pattern 1 requires: 247 lines after this plan, with 19 rules (13 exampled, 6 unexampled) still to come across `02-03`/`02-04`, projecting to roughly 247 + (13×13) + (6×5) = 446 lines — under the 470-line soft ceiling and the 500-line hard ceiling, with no trimming required yet.

## Task Commits

1. **Task 1: PF-1 opening half — before state, after state, needed capability** — `d4d96b8` (feat)
2. **Task 2: PF-1 closing half — metrics, proof, differentiators, outcomes, line-count checkpoint** — `fb5f6f1` (feat)

**Plan metadata commit:** recorded below after STATE.md/ROADMAP.md/REQUIREMENTS.md updates.

## Files Created/Modified

- `skills/proof-first/SKILL.md` — added `## PF-1 — Structure` (9 rules, 181→247 lines total across the two tasks)
- `skills/proof-first/references/checklist.md` — 9 new PF-1 rows, ascending by ID
- `NUMBERING.md` — 9 new Allocated IDs rows, PF-1 reserved-range counters updated twice

## Decisions Made

- Two rule bodies (`PF-1.5`, `PF-1.21`) needed to reference a mechanism whose concrete rule ID is not allocated until a later plan (a `PF-5` presence check, a `PF-2` competitor-flag rule). Both were worded to describe the mechanism's location in the catalog rather than cite the literal unallocated `PF-#.#` token — see key-decisions above. This is the same avoidance 02-01 already used with its `<rule>` placeholder for the same reason: `undefined-id` scans every `PF-#.#`-shaped token in `skills/`, with no exception for a token that will become valid once a later plan allocates it.
- `unlisted-figure`'s currency regex absorbs a trailing comma that is ordinary sentence punctuation, not a thousands separator, turning a valid canonical figure into a reported-unmatched string. Fixed by rewording the two affected sentences (splitting into two sentences, or dropping the comma) rather than touching the checker — this is a documented, declared ceiling of the existing tool, not a defect introduced by this plan.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Reworded two ✓ examples to avoid a false `unlisted-figure` violation**
- **Found during:** Task 1 and Task 2, first `python3 tools/check_repo.py` run after each
- **Issue:** `PF-1.2`'s and `PF-1.25`'s ✓ examples cited `$2,300,000,` immediately followed by a comma (ordinary sentence punctuation). `unlisted-figure`'s `CURRENCY_RE` (`\$\d[\d,]*(?:\.\d+)?[MKB]?`) greedily consumes the trailing comma into the matched token, producing `$2,300,000,` — a string with no Canonical figures row, even though `$2,300,000` itself is a valid canonical value.
- **Fix:** Reworded both sentences so no comma immediately follows the currency figure (split into two sentences in `PF-1.2`; removed the comma before "and" in `PF-1.25`).
- **Files modified:** `skills/proof-first/SKILL.md`
- **Verification:** `python3 tools/check_repo.py` → `check_repo: 0 violations` after each fix.
- **Committed in:** `d4d96b8` (Task 1), `fb5f6f1` (Task 2) — both fixes are folded into their respective task commits, since they were caught and corrected before either task's commit was made.

---

**Total deviations:** 1 auto-fixed (1 bug, applied twice against the same underlying checker-ceiling pattern).
**Impact on plan:** No scope creep — the fix only reworded prose punctuation around already-canonical figures; no new fact was invented and no checker code was touched.

## Issues Encountered

None beyond the deviation documented above.

## Authentication Gates

None — no external service or CLI authentication was required.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `PF-1`'s nine rules are registered and indexed; `02-03` and `02-04` can allocate their own IDs (`PF-2` Proof rules and the remaining Integrity rules, `PF-3.2`/`PF-3.3`, `PF-4`, `PF-5`) without renumbering anything here.
- The measured 247-line mid-draft checkpoint and its ~446-line projection are recorded for `02-03`/`02-04` to check their own running totals against, per RESEARCH Pattern 1's stated remedy of catching an overrun with sections still left to trim.
- Two rule bodies in this plan reference future rules generically (not by ID) because those IDs are not yet allocated — `02-03`'s Integrity rules and a later `PF-5` presence rule are free to allocate those IDs without this plan needing amendment, since no forward citation was made.
- Open item carried into end-of-phase UAT (per `workflow.human_verify_mode: end-of-phase`, same deferral 02-01 used): a human read of the nine new rule bodies against `SOURCES.md`'s reproduction boundary, confirming no Command of the Message wording or ordered-list structure was reproduced.
- No blockers for `02-03`.

## Self-Check: PASSED

- `[ -f skills/proof-first/SKILL.md ]` → FOUND
- `[ -f skills/proof-first/references/checklist.md ]` → FOUND
- `[ -f NUMBERING.md ]` → FOUND
- `git log --oneline --all | grep -q d4d96b8` → FOUND
- `git log --oneline --all | grep -q fb5f6f1` → FOUND
- `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` → all green, 13 codes proven live, 0 live violations
- All Task 1 and Task 2 acceptance criteria re-run: all PASS (heading counts 7/12, Replace-with counts 7/12, ID ordering, sub-block range containment, stated-count sentence, `REVIEW (competitor)` present ×2, `GAP:` present ×4, line count 181/247 both under ceiling)

---
*Phase: 02-rule-catalog-integrity-skill-md-core*
*Completed: 2026-09-11*
