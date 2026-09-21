---
phase: 06-legal-review-gate-launch
plan: 06-05
subsystem: docs
tags: [readme, legal-review, reproduction-boundary, broken-windows, evidence-discipline]

requires:
  - phase: 06-01
    provides: SOURCES.md rows verified and the LEG-04 source gate
  - phase: 06-02
    provides: LEGAL-REVIEW.md, its reproduction-boundary dispositions and the name-collision searches
  - phase: 06-03
    provides: README's claim region and the results-file pointers the corrections are checked against
  - phase: 06-04
    provides: the ledger sweep and the launch deferral this round reconciles the gate header with
provides:
  - README's evidence-discipline claim bounded to the two codes that enforce it
  - README's route count reconciled with run_routes.py's ROUTES tuple
  - README carrying Arm B, the trigger measurement of the description that ships
  - the id-6 reproduction disposition restated on grounds NUMBERING.md supports
  - a first examination of the PF-1 Command of the Message element list, left open as WINDOWS id 29
  - LEGAL-REVIEW.md's verdict layer separated from its reasoning layer
  - the second round's human observations recorded, superseding three "not performed" findings
affects: [launch, publication, any later review reading LEGAL-REVIEW.md's ledger]

actuals:
  tokens: 11500
  tasks: 8
  commits: 6

tech-stack:
  added: []
  patterns:
    - "Ledger label 'Closed on reasoning' for entries that close on a written judgement with no shipped-content change"

key-files:
  created: []
  modified:
    - README.md
    - LEGAL-REVIEW.md
    - NUMBERING.md
    - .planning/WINDOWS.md

key-decisions:
  - "Task 1: bound the evidence-discipline claim to the claim region and name the third case neither code covers — figures quoted in prose outside it — rather than widening the codes."
  - "Task 2: state four install routes and three measured arms in the same sentence, with the reason routes 1 and 2 collapse, instead of silently restating three."
  - "Task 4a: drop the limitation count rather than replace 'one' with 'three' — the benchmark result is arguably a fourth, and an exact count would repeat the same over-claim in the other direction."
  - "Task 5: restate the id-6 reasoning and state the false premise as corrected, rather than patch it silently. The MEDDPPCC correction is recorded in the disposition itself."
  - "Task 5: prong 4 is answered honestly — 'Economic Buyer' and 'Paper Process' are recorded as sitting ON the prong, with the choice not to rename made explicit."
  - "Task 6: examine the PF-1 element list and leave it open. The plan required examination, not disposal, and the reasoning does not reach a close."
  - "Task 7: keep 'Gate status: PASSED' (tools/check_repo.py's source-gate-incomplete requires exactly one PASSED/OPEN/FAILED line) but move it below the disclaimer and state, next to it, the narrow thing the code defines it to assert."
  - "Task 7: add a fourth ledger label rather than move ids 3 and 6 to Waived — neither was measured, so Waived's definition fits no better than Fixed's. WINDOWS.md's three-state schema divergence is named rather than hidden."
  - "Task 8: LEGAL-REVIEW.md is append-only, so sections 1-3 of '## Human observations' were amended only in their headings and superseded by a new section 4, not rewritten."

patterns-established:
  - "Claim scoping: when a README sentence cites a code as its enforcement, the sentence's scope must equal the code's scope, and any third category the code does not reach is named explicitly."
  - "Reproduction-boundary reads run every SOURCES.md prong explicitly, applying or excluding each by name, rather than arguing only the prong that first looked live."
  - "A diligence record's reduced read — headings, bolded lead-ins and ledger column alone — must carry no legal conclusion; prose disclaimers do not govern the verdict layer."

requirements-completed: []

coverage:
  - id: D1
    description: "README's evidence-discipline claim is true of README as it stands, scoped to the claim region and naming the unenforced third case"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations); README.md:232-247 read against tools/check_repo.py:405-421"
        status: pass
    human_judgment: true
    rationale: "Whether the rewritten paragraph reads as honest scoping rather than a hedge is a reader judgement no code here performs — the same class as WINDOWS id 17."
  - id: D2
    description: "No README sentence states a route count disagreeing with run_routes.py's ROUTES tuple without explaining the collapse in the same sentence"
    verification:
      - kind: other
        ref: "grep -n 'route' README.md against evals/routes/run_routes.py:113 ROUTES = ('skill-on','style-on','prompt-on')"
        status: pass
    human_judgment: false
  - id: D3
    description: "Every trigger figure in README comes from a RESULTS-trigger.md block measuring the description currently shipped"
    verification:
      - kind: other
        ref: "head -14 skills/proof-first/SKILL.md | shasum -a 256 == d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675, the Arm B block's recorded hash; 45/45 and 9/25 read from that block's Totals"
        status: pass
    human_judgment: false
  - id: D4
    description: "The id-6 disposition contains no sentence falsifiable from NUMBERING.md, and applies or excludes all four SOURCES.md prongs by name"
    verification:
      - kind: other
        ref: "LEGAL-REVIEW.md:186-258 read against NUMBERING.md:64-77 and SOURCES.md:11-22"
        status: pass
    human_judgment: true
    rationale: "Whether the restated grounds actually carry the conclusion is the judgement the entry now ends on; it is recorded as live, not settled."
  - id: D5
    description: "The PF-1 Command of the Message element list is examined by name under '## Reproduction boundary' and registered in WINDOWS.md"
    verification:
      - kind: other
        ref: "LEGAL-REVIEW.md:260 '### The PF-1 sub-block list'; .planning/WINDOWS.md entry 29, open, pointing at that section"
        status: pass
    human_judgment: false
  - id: D6
    description: "LEGAL-REVIEW.md's reduced read — headings, bolded lead-ins, ledger column — states no legal conclusion"
    verification:
      - kind: other
        ref: "grep '^#' + grep '^\\*\\*' + the ledger Disposition column, read as a set"
        status: pass
    human_judgment: true
    rationale: "The gap is about what a skimming reader consumes. A person has to perform the reduced read; the mechanical extraction only supplies the text."
  - id: D7
    description: "WINDOWS.md frontmatter counts match its rows and no entry's reason asserts a blocker this round cleared"
    verification:
      - kind: other
        ref: "open_count 9 / waived_count 9 / fixed_count 11 / total_count 29 against 29 JSON entries; stale-premise scan over description+reason"
        status: pass
    human_judgment: false
  - id: D8
    description: "All ten commands .github/workflows/ci.yml declares exit 0"
    verification:
      - kind: integration
        ref: ".github/workflows/ci.yml — 10 commands, all rc=0"
        status: pass
    human_judgment: false

duration: 55min
completed: 2026-09-21
status: complete
---

# Phase 06 Plan 05: Gap closure Summary

**Three places where a statement about the work outran the work are corrected at the source: README's evidence-discipline claim is bounded to what its codes enforce, the id-6 disposition is restated on grounds its own registry supports, and LEGAL-REVIEW.md's verdict layer no longer reads as clearance.**

## Performance

- **Duration:** 55 min
- **Tasks:** 8 of 8
- **Files modified:** 4
- **Commits:** 6

## Accomplishments

- **README no longer claims an evidence discipline it does not enforce.** The sentence that said every number in README is sourced, model- and date-stamped and checked by `tools/check_repo.py` is replaced by one that matches the two codes it cites, plus an explicit statement of the third category neither code reaches: figures quoted from a results file in prose outside the claim region.
- **README carries the measurement of what ships.** The superseded n=1 trigger run is replaced by Arm B — 45 of 45 must-fire, 9 of 25 must-not-fire over-fires, at n=5 on `claude-sonnet-5`, 2026-09-20. The shipped `SKILL.md`'s head-14 sha256 matches Arm B's recorded hash exactly.
- **The id-6 disposition rests on something true.** Its load-bearing premise — that the block order "*is* the acronym, letter by letter" — is false: the eight shipped blocks give M-E-D-D-P-P-C-C, and four of eight positions are letter-ambiguous. The correction is stated in the disposition rather than patched out of it, and the conclusion is re-argued on the thinness of the expression. All four `SOURCES.md` prongs are now applied or excluded by name.
- **The PF-1 element list is examined for the first time and left open.** Neither id 3 nor id 6 had read `NUMBERING.md`'s seven Command of the Message sub-blocks, which is the stronger instance on every axis — no acronym defence, a live unadjudicated mark, and a harder prong-4 case. Registered as `WINDOWS.md` id 29 with the cheap alternative named.
- **The diligence record reads as a record.** `Gate status: PASSED` moved below the disclaimer with the narrow thing it asserts stated next to it; the two `Disposition:` verdicts became `Read at this review:`; the unbounded negative about third parties' rights is bounded; the disclaimer-sufficiency assertion is replaced by what the files state; and ids 3 and 6 moved to a new `Closed on reasoning` label because nothing shipped changed for either.
- **The second round's observations are on the record.** Sections 1-3 of `## Human observations` recorded three checks as not performed on premises that had expired the same day. A new section 4 supersedes them with what the driven `/config` session and the five independent readers actually returned.

## Task Commits

1. **Tasks 1-2: README evidence-discipline claim and route count** — `d67012e` (fix)
2. **Tasks 3-4: trigger measurement and four README inconsistencies** — `441b344` (fix)
3. **Task 5: id-6 reproduction reasoning and NUMBERING.md namespace name** — `0b8a865` (fix)
4. **Task 6: PF-1 Command of the Message element list** — `7260702` (docs)
5. **Task 7: separate the record from the opinion** — `0476564` (docs)
6. **Task 8: second-round observations and ledger reconciliation** — `36fbf6c` (docs)

Tasks 1-2 and 3-4 were committed in pairs: each pair touches only `README.md` and the second of each pair depends on the first's rewrap, so splitting them would have produced a commit whose diff is dominated by reflow.

## Files Created/Modified

- `README.md` — evidence-discipline claim bounded; route count reconciled; trigger figures replaced with Arm B; limitation count dropped; the deal-brief, MOD-04-threshold and "What exists today" inconsistencies fixed.
- `LEGAL-REVIEW.md` — id-6 disposition restated; PF-1 sub-block section added; gate header relocated and bounded; verdict-register language removed; ledger given a fourth label and re-counted; human-observations section 4 appended.
- `NUMBERING.md` — the `MC-` namespace is no longer called "the MEDDICC completeness audit" over an eight-block table that spells no such acronym.
- `.planning/WINDOWS.md` — entry 29 added; the fenced JSON reconciled with three table-only edits from the UAT round; the rendered table regenerated.

## Decisions Made

See `key-decisions` in the frontmatter. The two worth repeating here:

**The gate token stayed `PASSED`.** `tools/check_repo.py`'s `source-gate-incomplete` requires exactly one readable `Gate status:` line reading `PASSED`, `OPEN` or `FAILED`, and it defines `PASSED` narrowly: no `SOURCES.md` row still reads `unverified`. That is true. Renaming the line would have tripped the code; changing the value to `OPEN` would have asserted something the code does not mean. The fix was to move it below the disclaimer and state the code's own definition, and the code's own declared ceiling, immediately next to it.

**Ids 3 and 6 got a new label rather than `Waived`.** `Waived` in this file means measured, disclosed and accepted with the measurement named. Neither entry was measured. Moving them there would have swapped one inaccurate label for another, so the file gained `Closed on reasoning` and states plainly that `.planning/WINDOWS.md`'s three-state schema folds both into `fixed`.

## Deviations from Plan

### 1. WINDOWS.md ledger repair, required before Task 6's append could run

- **Found during:** Task 6.
- **Issue:** `gsd-tools windows append` refused the write: the fenced JSON — the ledger's sole source of truth — disagreed with the rendered table for ids 12, 14, 15, 16, 17 and 27. Two distinct causes. For 12, 16 and 17 the UAT round's findings had been written into the rendered table only, leaving the JSON stale. For 14, 15 and 27 the rendered table had lost the `\|` escaping their descriptions require, so those rows were unparseable rather than wrong.
- **Fix:** the three newer reasons were reconciled into the JSON, and the whole table was regenerated from the JSON using the same escaping rule `broken-windows.cjs`'s `renderTable` applies.
- **Verification:** `gsd-tools windows append` then succeeded; frontmatter reads 9 open / 9 waived / 11 fixed / 29 total against 29 JSON entries.
- **Committed in:** `7260702`.

### 2. Marker literals cannot be quoted in README's Task 1 rewrite

- **Found during:** Task 1.
- **Issue:** the first rewrite named the claim region by quoting both HTML comment markers. `readme-claim-unsourced` fired — it requires exactly one of each in the file, and quoting them makes two.
- **Fix:** the paragraph refers to "the frozen pair of `claim-region` HTML comments" without reproducing the literals.
- **Verification:** `python3 tools/check_repo.py` green.
- **Committed in:** `d67012e`.

### 3. A wrong count caught in the Task 3 rewrite before commit

- **Found during:** Task 3 self-check.
- **Issue:** the first draft said three near-miss phrasings accounted for the nine Arm B over-fires. The table shows two (5 of 5 and 4 of 5); the other three over-fired 0 of 5.
- **Fix:** corrected to two, with the per-row split stated.
- **Verification:** re-read against `evals/trigger/RESULTS-trigger.md`:86-90.
- **Committed in:** `441b344`.

---

**Total deviations:** 3, all auto-fixed. **Impact on plan:** none on scope. Deviation 1 is repair of pre-existing state, not new work.

## Issues Encountered

**One finding surfaced during verification and deliberately not acted on.** README:109 reads "The installed skill has to be triggered and was not in 3 of its 12 sessions, while the output style and the pasted prompt are unconditionally on once selected." The 3-of-12 figure is correct (`RESULTS-routes.md`'s Activation table: skill-on activated 9 of 12). Each half of the sentence is true. But the contrast invites a reader to take the other two arms as 12 of 12 on the same metric, and the same table reads style-on 11 of 12 and prompt-on 8 of 12 — prompt-on activates *less* often than skill-on. This is the class the plan's own "Out of scope" section put in backlog: a placement judgement, not a false statement. Recorded here rather than fixed, because fixing it was not in this plan's scope and the cheapest honest fix (state all three activation figures) changes a sentence the plan did not open.

## Executor note

**The `gsd-executor` subagent was not dispatched.** This session carries a standing instruction not to call the Agent tool, so the plan ran inline in the orchestrator context. The routing was legal independently of that: `execute-plan.md`'s `parse_segments` routes to Pattern C (inline, main context) when `TASK_COUNT <= workflow.inline_plan_threshold`, and this plan's prose `## Task N` headings yield a `<task>`-tag count of 0 against a threshold of 2. Commit protocol, self-check and this SUMMARY were followed as written.

## User Setup Required

None.

## Next Phase Readiness

The three UAT gaps this plan was written against (G-06-2, G-06-3, G-06-6) are closed at the source. Phase 6's remaining open items are decisions rather than work: the `Ardent Digital` and `Gina Almeida` rename decisions, whether a captured `/config` render satisfies id 16's human-observation condition, and `WINDOWS.md` id 29 on the PF-1 sub-block labels. Publication stays deferred by the 06-04 operator decision; nothing here changes that.

## Self-Check: PASSED

- Every `**Verify:**` clause in `06-05-PLAN.md` re-run; all eight pass. Task 3's is the sharpest: `head -14 skills/proof-first/SKILL.md | shasum -a 256` returns `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`, byte-identical to the hash `RESULTS-trigger.md` records for the Arm B block README now cites.
- All ten commands `.github/workflows/ci.yml` declares exit 0, re-run after the final edit.
- `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` returns `0`. This plan declares no `requirements` in its frontmatter, so `requirements-completed` is empty by design.
- `git log --oneline --grep="06-05"` returns the six task commits plus the plan's own creation commit.
