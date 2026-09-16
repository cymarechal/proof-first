---
phase: 03-completeness-audit-artifact-patterns
plan: 11
subsystem: eval-harness
tags: [mod-04, self-check-gate, check-repo, mutation-test, ordering-lever]

# Dependency graph
requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: "03-08's disposition rule (closure requires a lever other than instruction wording) and its own named untried lever (extend the self-check gate from presence to ordering); 03-10's 30-code discrimination-proven baseline in tools/check_repo.py"
provides:
  - "SKILL.md's self-check first pass rewritten from a presence gate to an ordering gate: re-scan the drafted response, confirm no PF-/MC- marker stands before the artifact-family line, and repair (move the line to the top, re-check) before returning"
  - "skill-family-order-gate-missing, a 31st discrimination-proven violation code anchoring the ordering clause against silent deletion"
  - "A fixed sibling mutation function (_mutate_skill_family_line_gate_missing), whose literal-string match on the old pass name would have silently stopped discriminating once this plan renamed that pass"
affects: [03-12 (measures this lever under 03-09's anchored scorer), phase-5-eval-harness]

# Actuals (#2632)
actuals:
  tokens: 10500
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns:
    - "A checker whose docstring and mutation function both name their sibling check by exact match string are coupled to that sibling's prose -- renaming the prose without checking the mutation function's own literal match silently converts a discrimination-proven code into a permanently-passing no-op. Match by structural position (list index) rather than by prose label where the label itself is what a plan might legitimately rewrite."

key-files:
  created: []
  modified:
    - skills/proof-first/SKILL.md
    - tools/check_repo.py

key-decisions:
  - "Renamed the self-check's first pass from 'Family-line pass' to 'Family-order pass' rather than keeping the old label with new content -- the pass now gates on position, not presence, and the old name would have described the wrong mechanism to a future reader."
  - "Fixing _mutate_skill_family_line_gate_missing()'s broken match (Rule 3, blocking: mutation-test regressed from 30 to 29 discrimination-proven the moment Task 1's rename landed) is scoped to the mutation function only. check_skill_family_line_gate() itself -- the actual check logic -- is untouched and verified byte-identical to its pre-task state, so WR-04 (case-sensitive anchor matching) stays exactly as unfixed as the plan requires."
  - "check_skill_family_order_gate() matches its two anchors case-insensitively, unlike its case-sensitive sibling -- a deliberate, disclosed choice (per 03-REVIEW.md WR-04) rather than an accidental inconsistency, and WR-04 itself is left unfixed."
  - "The four deleted rationale clauses were matched and removed verbatim, exactly as named in the plan's action list, at a clause boundary each time -- no other prose in SKILL.md was surveyed or touched."

patterns-established:
  - "A checker code and its own mutation-test coverage should be considered part of the same change surface as the prose it reads -- editing gated instruction text without re-running --mutation-test would have shipped a silently defanged sibling code."

requirements-completed: []  # This plan edits and mechanically guards; it measures nothing.
  # MOD-04 stays [ ] -- 03-12 is the measurement plan. WINDOWS.md entry 8 stays open,
  # 03-UAT.md gap G-03-2 stays partially_resolved. grep -c "^- \[x\].*UNVERIFIED"
  # .planning/REQUIREMENTS.md returns 0.

coverage:
  - id: D1
    description: "SKILL.md's self-check first pass requires a re-scan of the drafted response, forbids a rule marker before the family line, and states the repair (move to top, re-check) -- gating on ordering, not presence"
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "python3 -c anchor probe over the '## Self-check before delivering' section body -- prints RESCAN ORDER"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py -- check_repo: 0 violations"
        status: pass
    human_judgment: false
  - id: D2
    description: "SKILL.md's estimated token count stays at or below 4,900 with at least 100 tokens of headroom under the 5,000-token ceiling, paid for by deleting four named rationale clauses and nothing else"
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "python3 -c token probe: 3710 words, 4823 estimated tokens, 177 headroom (>= 100 floor)"
        status: pass
    human_judgment: false
  - id: D3
    description: "skill-family-order-gate-missing exists, registered in CATALOG_CHECK_CODES/ALL_CHECK_CODES, self-tested in three directions (fires on missing-both, silent on both-present, silent on no-self-check-section), has a MUTATIONS entry, and is discrimination-proven at a total of 31 codes"
    requirement: "MOD-04"
    verification:
      - kind: unit
        ref: "python3 tools/check_repo.py --self-test -- verified-codes list includes skill-family-order-gate-missing"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py --mutation-test -- final line: mutation-test PASS: 31 codes discrimination-proven; skill-family-order-gate-missing line reads mutation-test OK:"
        status: pass
    human_judgment: false
  - id: D4
    description: "check_skill_family_line_gate() (the sibling check function) is byte-identical to its pre-task state; its mutation function was fixed (Rule 3) after Task 1's pass rename silently broke its literal-string match, dropping discrimination-proven count to 29 before the fix"
    requirement: "N/A"
    verification:
      - kind: other
        ref: "Byte-comparison of check_skill_family_line_gate()'s source text before/after this plan's commits: identical. mutation-test OK line for skill-family-line-gate-missing present after the fix."
        status: pass
    human_judgment: false
  - id: D5
    description: "No requirement checkbox moved: MOD-04 stays [ ], WINDOWS.md entry 8 stays open, 03-UAT.md G-03-2 stays partially_resolved, and no line in REQUIREMENTS.md reads [x] next to UNVERIFIED"
    requirement: "N/A"
    verification:
      - kind: other
        ref: "grep -c \"^- \\[x\\].*UNVERIFIED\" .planning/REQUIREMENTS.md == 0; WINDOWS.md entry 8 status field == open; 03-UAT.md G-03-2 status == partially_resolved"
        status: pass
    human_judgment: false
  - id: D6
    description: "This SUMMARY makes no claim that the ordering lever improves live-session conformance -- that measurement belongs to 03-12"
    verification: []
    human_judgment: true
    rationale: "Whether the prose reads as an over-claim is a judgment a human should confirm; the plan's own prohibitions forbid stating or implying a conformance improvement here, and this SUMMARY was written to honor that, but a second reader should verify the wording actually holds that line."

duration: 20min
completed: 2026-09-16
status: complete
---

# Phase 3 Plan 11: Self-check ordering gate — extend "family line present" to "family line precedes any rule marker"

**`SKILL.md`'s self-check now re-scans its own drafted response and repairs the ordering before returning, and a 31st discrimination-proven `check_repo.py` code (`skill-family-order-gate-missing`) makes deleting that clause a build failure — a lever different in kind from the two instruction-wording restatements already measured and found insufficient.**

## Performance

- **Duration:** ~20 min
- **Tasks:** 2/2 completed
- **Files modified:** 2

## Accomplishments

- Rewrote the self-check's first numbered pass from a presence-only gate ("confirm the first line names the artifact family or states **No family fits:**") to an ordering gate: re-scan the drafted response from its first character before returning, confirm no `PF-` or `MC-` marker stands before the artifact-family line, and — when one does — move the family line to the top and re-check before returning. The two literal anchors Task 2's checker keys on (`re-scan`, `before any rule marker`) land naturally in the prose.
- Paid for the added words by deleting four named rationale (WHY-not-WHAT) clauses at clause boundaries: the "report, never a corrected document" sentence's 34-word trailing clause in `## Check mode`; the 18-word "write mode writes, check mode explains" clause in `## Write mode`; the 17-word "so a writer whose own RFP vocabulary gets stripped" clause, also in `## Write mode`; and the 12-word "so a thin-input draft comes back heavily marked" clause in the self-check's additive sweep. Every sentence each clause trailed is left grammatical and still states its requirement in full.
- Budget arithmetic: 3,757 words before -> 3,710 words after (net -47: +34 from the rewritten pass 1, -81 from the four deletions). Estimated tokens: 4,884 -> 4,823. Headroom under the 5,000-token ceiling: 116 -> 177 (comfortably above the 100-token floor).
- Added `check_skill_family_order_gate()` to `tools/check_repo.py` as a direct sibling of `check_skill_family_line_gate()`: same declared ceiling (silent when the self-check section is entirely absent), same per-missing-anchor firing shape, matching `re-scan` and `before any rule marker` case-insensitively (a disclosed departure from the sibling's case-sensitive match, per `03-REVIEW.md` WR-04, not a fix of WR-04 itself). Registered in `CATALOG_CHECK_CODES`/`ALL_CHECK_CODES`, given a module-docstring entry with a Declared-ceiling sentence naming `evals/conformance/run_conformance.py` as the instrument for live-session behavior, a self-test fixture pair, and a `MUTATIONS` entry that replaces the ordering pass with pre-03-11 presence-only wording against the real `SKILL.md`.
- Found and fixed one Rule 3 blocking regression mid-task: `_mutate_skill_family_line_gate_missing()` matched the literal string `"1. Family-line pass"`, which Task 1's rename to `"Family-order pass"` silently broke — the mutation stopped modifying anything, and `--mutation-test` regressed from 30 to 29 discrimination-proven codes (the sibling's own mutation coverage lost). Fixed by matching on list position (`"1. "`) instead of pass name, so a future rename of that pass's label can't silently defang this code's own mutation coverage again. `check_skill_family_line_gate()` itself — the check's actual logic — was verified byte-identical to its pre-task state; only its mutation function changed.
- All four of the project's real CI gate commands pass, and `--mutation-test`'s final line reads `mutation-test PASS: 31 codes discrimination-proven`.

## Task Commits

1. **Task 1: Extend the self-check first pass from presence to ordering, and pay for it out of named restatement** - `5ce0ebb` (feat)
2. **Task 2: Anchor the ordering gate with `skill-family-order-gate-missing`, discrimination-proven at 31 codes** - `c4dacae` (feat)

_Task 1 is `type="tracer"`. Its own `<verify>` (token-headroom probe, `check_repo.py`, PF- heading count, anchor probe) was re-run end-to-end as the tracer feedback gate before Task 2 started — all four passed (`HUMAN_VERIFY_MODE=end-of-phase`, no `<human-check>` in the tracer's `<verify>`, so this is the automated re-run-then-continue path per checkpoints.md row 3; no checkpoint synthesized)._

## Files Created/Modified

- `skills/proof-first/SKILL.md` - self-check pass 1 rewritten from presence to ordering gate with a stated repair; four named rationale clauses deleted to pay for it; 31 `### PF-` headings, the artifact-family phrase, and the `No family fits` value all unchanged
- `tools/check_repo.py` - new `check_skill_family_order_gate()`, `_mutate_skill_family_order_gate_missing()`, a `MUTATIONS` entry, `CATALOG_CHECK_CODES`/`run_catalog_checks()` registration, a module-docstring entry with a Declared-ceiling sentence, a self-test fixture pair (`family_order_good_root`/`family_order_bad_root`) with matching assertions, and a fix to `_mutate_skill_family_line_gate_missing()`'s match target (list position instead of pass name)

## Decisions Made

See `key-decisions` in frontmatter for full rationale. Summary:
- The self-check's first pass was renamed `Family-line pass` -> `Family-order pass` since its mechanism changed from presence to ordering; the old name would have misdescribed the new gate.
- The sibling mutation function's broken match (a direct, foreseeable consequence of the rename) was fixed under Rule 3 (blocking issue), scoped to the mutation function only — the check function itself is untouched, preserving the plan's own "sibling check is not touched" acceptance criterion.
- The new code matches case-insensitively, a disclosed departure from its case-sensitive sibling per WR-04, which stays unfixed as this round's scope requires.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] `_mutate_skill_family_line_gate_missing()`'s literal-string match broke when Task 1 renamed the pass it targets**
- **Found during:** Task 2, first `--mutation-test` run after adding `skill-family-order-gate-missing` — the sibling code `skill-family-line-gate-missing` unexpectedly reported `mutation-test FAIL`, and the total dropped to 29 discrimination-proven (should have stayed at 30 plus the new code, i.e. 31).
- **Issue:** `_mutate_skill_family_line_gate_missing()` filtered lines starting with the literal `"1. Family-line pass"`. Task 1 renamed that pass to `"1. Family-order pass"` as part of rewriting it from a presence gate to an ordering gate, so the mutation function's filter matched nothing — the mutated copy was identical to the control copy, and the check never fired on it.
- **Fix:** Changed the filter to match on the pass's list position (`"1. "`) rather than its name, so it targets whichever text occupies the self-check section's first numbered item regardless of what that pass is currently called. Verified no other line in `SKILL.md` starts with `"1. "`, `"2. "`, or `"3. "` outside the self-check section, so the broader match introduces no new false-positive mutation target.
- **Files modified:** `tools/check_repo.py`
- **Verification:** `python3 tools/check_repo.py --mutation-test` now reports `mutation-test OK: skill-family-line-gate-missing ...` and the final line reads `mutation-test PASS: 31 codes discrimination-proven`.
- **Committed in:** `c4dacae` (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 3, blocking). **Impact:** Necessary to keep the plan's own verification gate (`--mutation-test` reporting 31 discrimination-proven codes) truthful. No scope creep: `check_skill_family_line_gate()`'s actual check logic was not touched, verified byte-identical to its pre-task state.

## Issues Encountered

None beyond the deviation above.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The ordering lever is implemented and mechanically guarded (31st discrimination-proven code), but **not measured**. `03-12` measures it under `03-09`'s anchored scorer and disposes of `MOD-04` under a rule committed before the number is known — nothing in this SUMMARY should be read as evidence the lever works.
- `MOD-04` stays `[ ]`, `WINDOWS.md` entry 8 stays `open`, `03-UAT.md` gap `G-03-2` stays `partially_resolved` — all three unchanged by this plan's commits.
- `check_repo.py` now carries 31 discrimination-proven codes (30 -> 31), all four project CI gate commands pass, and the token budget holds 177 tokens of headroom (above the 100-token floor).
- A pattern worth carrying into future plans that touch gated instruction text: a checker's own mutation-test coverage should be treated as part of the same review surface as the prose it protects — a prose rename can silently defang a sibling's discrimination proof without any of the four live gate commands catching it on a first pass (only `--mutation-test`'s own per-code FAIL line surfaced it here).

## Self-Check: PASSED

- `git log --oneline --all | grep -q 5ce0ebb` -> FOUND
- `git log --oneline --all | grep -q c4dacae` -> FOUND
- `skills/proof-first/SKILL.md` and `tools/check_repo.py` both found on disk with the claimed edits present (`grep -c '^### PF-' skills/proof-first/SKILL.md` -> `31`; `grep -n "def check_skill_family_order_gate" tools/check_repo.py` -> found).
- Re-ran all four plan-level `<verification>` commands: `check_repo.py --self-test` -> PASS, verified-codes list includes `skill-family-order-gate-missing`; `--mutation-test` -> `mutation-test PASS: 31 codes discrimination-proven`; plain `check_repo.py` -> `check_repo: 0 violations`; `run_conformance.py --self-test` -> `self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable`.
- Token probe: `3710 4823 177` (word count, estimated tokens, headroom) -> headroom `177 >= 100`.
- Anchor probe: `RESCAN ORDER`.
- `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` -> `0`.
- `WINDOWS.md` entry 8 `status` field -> `open`; `03-UAT.md` `G-03-2` `status` -> `partially_resolved`.
- `check_skill_family_line_gate()` source text confirmed byte-identical before/after this plan's commits.

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-16*
