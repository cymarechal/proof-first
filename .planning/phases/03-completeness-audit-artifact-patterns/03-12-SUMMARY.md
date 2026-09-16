---
phase: 03-completeness-audit-artifact-patterns
plan: 12
subsystem: eval-harness
tags: [mod-04, anchored-scorer, self-check-ordering-gate, windows-ledger, gap-closure]

# Dependency graph
requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: "03-09's anchored score_transcript() (FAMILY_LINE_WINDOW_CHARS=400, both offsets computed against the same stripped string) and 03-11's self-check ordering-gate lever -- this plan measures whether that lever moved MOD-04's conformance rate under the anchored instrument"
provides:
  - "The first MOD-04 measurement produced entirely under 03-09's anchoring fix: Arm A (post-03-11 skill) 3/10 (30.0%) scoreable claude-sonnet-5 sessions conformant; Arm B (paired same-instrument baseline, pre-03-11 skill materialised from git) 4/10 (40.0%) -- a -10.0 percentage-point delta selecting the pre-committed rule's Branch 4"
  - "evals/conformance/RESULTS-mod04.md gains a '## Pre-committed disposition rule (03-12)' section (committed before any session ran) and a '## Anchored remeasurement result (03-12)' section with re-derivable arithmetic and caveats"
  - "WINDOWS.md entry 8 disposed: waived (accepted, disclosed residual -- not fixed), per Branch 4"
affects: [phase-5-eval-harness, phase-6-legal-review, any future lever aimed at MOD-04]

# Actuals (#2632)
actuals:
  tokens: 11462
  tasks: 3
  commits: 25

tech-stack:
  added: []
  patterns:
    - "Materialise a paired baseline via git archive into a directory outside the repo, verify its blob SHA against an independently-derived expectation recorded BEFORE any session runs, and pass it as --skill-src -- repeats 03-08's pattern, this time against the anchored scorer"
    - "One claude -p invocation per Bash call, one run block per invocation, one commit per run block -- durable against interruption (this round survived a real mid-Task-2 usage-limit reset with zero data loss because every completed session was already committed)"

key-files:
  created: []
  modified:
    - evals/conformance/RESULTS-mod04.md
    - .planning/WINDOWS.md
    - .planning/REQUIREMENTS.md
    - .planning/phases/03-completeness-audit-artifact-patterns/03-UAT.md

key-decisions:
  - "Branch 4 fired mechanically: M_A=10>=8, M_B=10>=8, N_A/M_A=0.30<0.875, and (N_A/M_A)-(N_B/M_B)=-0.10<0.10. Applied exactly as the pre-committed rule (committed in 0f47e8b, before any session ran) prescribes."
  - "Did not reproduce Branch 4's template label 'did not move' where the measured evidence says otherwise. The mechanical disposition (WINDOWS.md waived, MOD-04 stays [ ], 03-UAT.md stays partially_resolved) was honored exactly, but every written record states the true finding: a 10.0-percentage-point DECLINE (30.0% vs 40.0%), not flat movement -- while also disclosing that at n=10 per arm this delta sits within plausible sampling noise for a true rate difference of zero. This is 03-08-PLAN.md's own precedent (write the true finding when the branch template's phrase would misstate measured evidence), applied a second time."
  - "Two Rule-3 blocking fixes were required before Task 1 could satisfy its own 'git status --porcelain prints nothing' verify gate: (1) pre-existing uncommitted drift in .planning/milestone.lock and .planning/state.json (session-lock/timestamp bookkeeping left dirty by the prior interrupted executor session) was committed separately as housekeeping; (2) the repository had no .gitignore at all, so an untracked .gsd/ dispatch-isolation-sentinel directory was permanently tripping every clean-tree assertion this plan's tasks require -- added a minimal .gitignore (.gsd/, __pycache__/, *.pyc) as a blocking fix, not scope creep, since the plan cannot pass its own verify gates without it."
  - "All three levers this project has now measured for MOD-04 (03-05 instruction restatement, 03-07 five-value family line plus presence gate, 03-11 self-check ordering re-scan) have failed to reach the 87.5% closure bar, and the one lever different in kind from pure instruction wording (03-11's mechanical ordering gate) is the one measured, for the first time, under an instrument proven not to inflate the rate. The anchored figures (30.0%/40.0%) are markedly lower than every prior unanchored figure for this residual (5/6, 14/16, 16/20, 5/11), consistent with CR-01's documented bias direction (toward looking MORE conformant, never less) -- this suggests a meaningful fraction of the earlier apparent 'improvement' was scorer artifact, not skill behavior."
  - "This plan performed no human paraphrase read and touched no AUD-01/ART-0x checkbox; Task 3 explicitly re-asserted all nine other requirement IDs' checkbox states are undrifted before the final commit."

patterns-established:
  - "When a branch table's template phrasing and the measured evidence disagree, write the measured finding and say so explicitly in the SUMMARY -- honoring the mechanical disposition (status/checkbox/gate state) is not the same obligation as reproducing the template's prose, and conflating the two would itself be a form of the overclaim this plan's prohibitions exist to prevent."

requirements-completed: []
  # MOD-04 stays [ ] -- Branch 4 is an accepted, disclosed residual, not a satisfied
  # requirement. WINDOWS.md entry 8 moves from open to waived (not fixed). AUD-01 and
  # ART-01..04 remain [ ] and Phase-6 LEG-04-owned, verified untouched. AUD-02, AUD-03,
  # MOD-03, MOD-05 remain [x] and untouched. grep -c "^- \[x\].*UNVERIFIED"
  # .planning/REQUIREMENTS.md returns 0.

coverage:
  - id: D1
    description: "The pre-committed disposition rule (branch table, arm definitions, 0.875 bar, attempt cap, both arms' expected SKILL.md blob SHAs) is committed to evals/conformance/RESULTS-mod04.md alone, before any session in this round ran, with a fixed commit subject that git log --reverse proves precedes every 'anchored MOD-04 run block' commit"
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "git log --format='%s' --reverse -- evals/conformance/RESULTS-mod04.md | grep -nE 'pre-committed disposition rule|anchored MOD-04 run block' | head -1 -- prints the disposition-rule subject"
        status: pass
      - kind: other
        ref: "grep -c '^## Pre-committed disposition rule (03-12)' evals/conformance/RESULTS-mod04.md == 1"
        status: pass
    human_judgment: false
  - id: D2
    description: "Both anchored arms exist as durable, individually committed run blocks: Arm A (post-03-11 skill, blob fadc48613f71fb29d55b42f70805225f9087a2b9) 10 scoreable sessions plus 2 retried timeouts; Arm B (pre-03-11 skill materialised from commit c7c1df45e5042636565747f31d4eb5c38513dbac, blob 9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a) 10 scoreable sessions plus 1 retried timeout -- every exclusion carries a machine-produced reason= field, none silently absent"
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "git diff 0f47e8b..878b937 -- evals/conformance/RESULTS-mod04.md | grep -cE '^\\+- 20' == 23 (12 Arm A lines + 11 Arm B lines); grep -c '^- 20..-..-.. \\| model=claude-sonnet-5' evals/conformance/RESULTS-mod04.md == 58 (>=51 required)"
        status: pass
      - kind: other
        ref: "git diff 5ce0ebb..HEAD -- evals/conformance/run_conformance.py produces no output -- instrument byte-identical to its post-03-09 state throughout the measurement"
        status: pass
    human_judgment: false
  - id: D3
    description: "N_A/M_A and N_B/M_B computed by hand from the committed run blocks (re-derived independently twice across the interruption, both times identical): N_A=3, M_A=10 (30.0%); N_B=4, M_B=10 (40.0%); delta=-10.0pp. Branch 4 selected mechanically and applied to all four MOD-04 trackers with identical figures"
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "evals/conformance/RESULTS-mod04.md '## Anchored remeasurement result (03-12)' section -- arithmetic re-derivable from the run blocks above it; WINDOWS.md entry 8 status=waived; REQUIREMENTS.md MOD-04 stays [ ] with the same figures; 03-UAT.md G-03-2 stays partially_resolved with the same figures"
        status: pass
      - kind: other
        ref: "python3 -c anchor probe over WINDOWS.md's fenced JSON block -- entry 8 status == 'waived', JSON parses"
        status: pass
    human_judgment: false
  - id: D4
    description: "No checked box sits beside an UNVERIFIED annotation anywhere in REQUIREMENTS.md; AUD-01 and ART-01..04 remain [ ] and Phase-6-owned; AUD-02, AUD-03, MOD-03, MOD-05 remain [x] and untouched; all four project gate commands pass with --mutation-test reporting 31 codes"
    requirement: "N/A"
    verification:
      - kind: integration
        ref: "grep -c \"^- \\[x\\].*UNVERIFIED\" .planning/REQUIREMENTS.md == 0; grep -cE '^- \\[ \\] \\*\\*(AUD-01|ART-01|ART-02|ART-03|ART-04)\\*\\*' .planning/REQUIREMENTS.md == 5; python3 tools/check_repo.py --self-test / --mutation-test (31 codes) / plain (0 violations); python3 evals/conformance/run_conformance.py --self-test"
        status: pass
    human_judgment: false
  - id: D5
    description: "The interpretive framing of Branch 4 -- stating a measured 10-point decline rather than reproducing the template's 'did not move' phrase, while also disclosing that this delta is within plausible sampling noise at n=10 per arm -- is a substantive judgment call a human should be able to reread and confirm is honest and not softened or alarmed in either direction"
    requirement: "MOD-04"
    verification: []
    human_judgment: true
    rationale: "This is the same class of interpretive choice 03-08-PLAN.md made (writing the true finding where a branch template's phrase would misstate the evidence), not a mechanically checkable fact. A human reviewer should confirm the framing above (decline stated plainly, noise caveat also stated plainly, neither buried) reads as calibrated rather than either alarmist or minimizing."

duration: "~3h wall-clock across an interrupted/resumed executor session (a Claude Code usage-limit reset occurred after Task 2's live measurement completed and before Task 3's arithmetic; the coordinator confirmed on resume that all 23 run-block commits were already durable in git, so Task 3 re-derived the arithmetic from the committed blocks rather than from memory, exactly as the plan's design intends)"
completed: 2026-09-16
status: complete
---

# Phase 3 Plan 12: Anchored MOD-04 remeasurement — Branch 4 (measured decline, within noise) disposed across all four trackers

**The first MOD-04 measurement produced entirely under 03-09's anchoring fix shows the 03-11 ordering-gate lever at 30.0% (3/10) against a paired pre-03-11 baseline at 40.0% (4/10) — a 10-point decline the pre-committed rule's own arithmetic reads as "did not move" (Branch 4), so `WINDOWS.md` entry 8 is waived as an accepted, disclosed residual and `MOD-04` stays `[ ]`.**

## Performance

- **Duration:** ~3h wall-clock (interrupted mid-Task-2 by a Claude Code usage-limit reset; resumed cleanly from committed state per the coordinator's verification, no data re-derived from memory)
- **Started:** 2026-09-16T06:18:00Z (approx., prior session)
- **Completed:** 2026-09-16T09:18:35Z
- **Tasks:** 3/3 completed
- **Files modified:** 4 plan-scoped (plus 2 preparatory housekeeping commits: planning lockfile sync, a new repo-root `.gitignore`)

## Accomplishments

- **The pre-committed disposition rule is in git history before any session ran.** `evals/conformance/RESULTS-mod04.md` gained `## Pre-committed disposition rule (03-12)` in its own commit (`0f47e8b`), carrying the six-branch table, both arms' definitions, the `0.875` bar, the 30-invocation attempt cap, and both arms' expected `SKILL.md` blob SHAs derived independently of any prior plan's figures (`fadc4861...` for Arm A at HEAD, `9612649e...` for Arm B via `c7c1df4...`, the last commit before `03-11` Task 1). `git log --reverse` proves this commit precedes all 24 later commits this plan made to the same file.
- **Both anchored arms are measured and durably committed.** Arm A (post-`03-11` skill): 12 attempted, 2 timeouts retried, 10 scoreable — 3 conformant, 7 `no-family`, 0 `rule-before-family`. Arm B (pre-`03-11` skill, materialised via `git archive` and blob-SHA-verified before any session ran): 11 attempted, 1 timeout retried, 10 scoreable — 4 conformant, 6 `no-family`, 0 `rule-before-family`. Every invocation ran in the foreground with `--timeout 480`, one fixture per invocation, committed immediately — exactly the durability pattern `03-08`'s post-mortem recommended, and it paid off: a real Claude Code usage-limit reset interrupted the executor mid-Task-2, and zero data was lost because every completed session was already a git commit.
- **The arithmetic was independently re-derived twice** (once before the interruption, once after, both by the coordinator's own instruction to re-derive from committed blocks rather than trust memory) and matched exactly both times: `N_A=3, M_A=10` (30.0%), `N_B=4, M_B=10` (40.0%), delta `-10.0` percentage points.
- **Branch 4 fires by arithmetic, not judgment**: `M_A=10>=8` and `M_B=10>=8` (not under-sampled), `N_A/M_A=0.30<0.875` (not closed, not improved-to-bar), `(N_A/M_A)-(N_B/M_B)=-0.10`, which is `<0.10` (fails Branch 3's improvement threshold, satisfies Branch 4's).
- **The written disposition states the true finding rather than the branch template's exact phrase.** Branch 4's table label is "did not move" — the measured delta is a 10-point *decline*, and every record (`RESULTS-mod04.md`, `WINDOWS.md`, `REQUIREMENTS.md`, `03-UAT.md`) says so plainly, while also disclosing that at `n=10` per arm this swing is within plausible sampling noise for a true rate difference of zero. This mirrors `03-08-PLAN.md`'s own precedent exactly.
- **All four MOD-04 trackers carry identical figures and the branch-prescribed state**: `WINDOWS.md` entry 8 is `waived` (not `fixed`) with a reason citing the anchored rates and all three measured levers; `REQUIREMENTS.md` `MOD-04`'s annotation gained the anchored figures alongside every prior round's, checkbox unchanged at `[ ]`; `03-UAT.md` gap `G-03-2` stays `partially_resolved` with its evidence block extended, prior figures retained verbatim.
- **The other nine requirement IDs are confirmed undrifted**: `AUD-01` and `ART-01`..`ART-04` remain `[ ]` and Phase-6-owned; `AUD-02`, `AUD-03`, `MOD-03`, `MOD-05` remain `[x]` and untouched. The UNVERIFIED-adjacency scan (`grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md`) returns `0`.
- **All four project gate commands pass**, `--mutation-test` reporting `31 codes discrimination-proven` (unchanged — this plan adds no violation code), and `run_conformance.py --self-test` confirms the instrument is byte-identical to its post-`03-09` state throughout the entire measurement.

## Task Commits

1. **Task 1: Commit the pre-committed disposition rule to git before any session runs** — `0f47e8b` (docs)
2. **Task 2: Run both anchored arms as one durable invocation per session** — 23 commits, one per invocation:
   - Arm A: `c1472a1`, `9bcddbd`, `82b35f2`, `be3477c`, `1ef1a99`, `04837a2`, `499cc36`, `e73baab`, `37809e1`, `39614c3`, `96477a9`, `2286b94`
   - Arm B: `cdca1bd`, `775729e`, `557d7fa`, `358329c`, `05e101a`, `4b0b81f`, `32b0366`, `fda8d8a`, `7754bf1`, `abb9238`, `c8f5e66`
3. **Task 3: Apply the pre-committed branch to the four records that track MOD-04** — `878b937` (docs)

**Preparatory housekeeping (before Task 1, blocking fixes per Rule 3, needed for the plan's own "git status --porcelain prints nothing" verify gates):**
- `98ed8b0` (docs) — synced pre-existing uncommitted drift in `.planning/milestone.lock` and `.planning/state.json` (left dirty by the prior interrupted executor session)
- `364a291` (chore) — added a repo-root `.gitignore` (`.gsd/`, `__pycache__/`, `*.pyc`); the repository previously had none, and an untracked `.gsd/` dispatch-isolation-sentinel directory was permanently tripping every clean-tree assertion this plan's tasks require

## Files Created/Modified

- `evals/conformance/RESULTS-mod04.md` — `## Pre-committed disposition rule (03-12)` section, 23 new anchored run blocks (Arm A and Arm B), and `## Anchored remeasurement result (03-12)` with re-derivable arithmetic and caveats
- `.planning/WINDOWS.md` — entry 8 status `open` → `waived`, description and reason replaced with the anchored figures and the true-finding framing
- `.planning/REQUIREMENTS.md` — `MOD-04`'s annotation extended with the anchored figures alongside all prior rounds; checkbox unchanged at `[ ]`
- `.planning/phases/03-completeness-audit-artifact-patterns/03-UAT.md` — gap `G-03-2`'s `post_fix_evidence` extended with the anchored measurement; `status: partially_resolved` unchanged
- `.gitignore` (created, preparatory) — `.gsd/`, `__pycache__/`, `*.pyc`
- `.planning/milestone.lock`, `.planning/state.json` (preparatory) — session-lock/timestamp sync, no content this plan is responsible for

## Decisions Made

See `key-decisions` in frontmatter for full rationale. Summary:
- Branch 4 selected by arithmetic (`M_A=10>=8`, `M_B=10>=8`, `N_A/M_A=0.30<0.875`, delta `-0.10<0.10`), applied exactly.
- The written disposition states the true finding (a 10-point decline, disclosed as within plausible sampling noise at `n=10`) rather than reproducing Branch 4's "did not move" label where it would understate the measured direction.
- Two Rule-3 blocking fixes (lockfile sync, new `.gitignore`) were required before Task 1's own verify gate could pass; neither touches plan-scoped content.
- The anchored figures (30.0%/40.0%) are markedly lower than every prior unanchored figure for this residual, consistent with CR-01's documented optimistic-ceiling bias — a meaningful share of the earlier apparent improvement across `03-05`→`03-07`→`03-08` was likely scorer artifact rather than skill behavior change.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Pre-existing uncommitted planning-lockfile drift blocked Task 1's clean-tree verify gate**
- **Found during:** Pre-Task-1 setup, `git status --porcelain` check before starting
- **Issue:** `.planning/milestone.lock` and `.planning/state.json` carried uncommitted session-lock/timestamp drift left by the prior interrupted executor session. Task 1's `<verify>` requires `git status --porcelain` to print nothing after the rule-only commit.
- **Fix:** Committed the two files separately, before Task 1, as housekeeping.
- **Files modified:** `.planning/milestone.lock`, `.planning/state.json`
- **Verification:** `git status --porcelain` clean after the commit.
- **Committed in:** `98ed8b0`

**2. [Rule 3 - Blocking] No `.gitignore` existed at the repo root; an untracked `.gsd/` sentinel directory permanently tripped every clean-tree assertion**
- **Found during:** Pre-Task-1 setup, same `git status --porcelain` check
- **Issue:** `.gsd/dispatch-isolation-sentinel.json` (a GSD runtime artifact, regenerated per session) showed as untracked with no `.gitignore` to exclude it, which would fail every one of this plan's four `git status --porcelain` verify checks regardless of what the plan itself changed.
- **Fix:** Added a minimal `.gitignore` (`.gsd/`, `__pycache__/`, `*.pyc`).
- **Files modified:** `.gitignore` (created)
- **Verification:** `git status --porcelain` clean; `.gsd/` no longer appears as untracked.
- **Committed in:** `364a291`

---

**Total deviations:** 2 auto-fixed (both Rule 3, blocking). **Impact:** Both were necessary preconditions for this plan's own verify gates to be satisfiable at all; neither touches plan-scoped content (`RESULTS-mod04.md`, `WINDOWS.md`, `REQUIREMENTS.md`, `03-UAT.md`). No scope creep.

## Issues Encountered

- **One live-measurement interruption:** a Claude Code usage-limit reset occurred after Task 2's 23 live sessions were fully committed and before Task 3's arithmetic began. Per the durable-commit-per-invocation design this plan and `03-08` both use, zero data was lost — the coordinator verified on resume that HEAD was `c8f5e66` with all 23 run blocks committed, and Task 3 re-derived `N_A/M_A` and `N_B/M_B` from the committed blocks (via `git diff 0f47e8b..HEAD`) rather than from pre-interruption memory, matching the pre-interruption computation exactly.
- **Three timeouts occurred across 23 attempted sessions** (2 in Arm A, 1 in Arm B), all retried successfully per the plan's retry protocol; none counted against a completed session's verdict, and none pushed the round anywhere near the 30-invocation attempt cap (23 total attempts used).

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `MOD-04` stays `[ ]`. Per Branch 4, `WINDOWS.md` entry 8 is now `waived` rather than `open` — the residual is accepted and disclosed as a known, measured limitation, not hidden and not claimed satisfied. Re-opening it (if a future lever is proposed) is a one-line `gsd-tools windows` operation; nothing about this disposition is a permanent close.
- Three levers (instruction restatement, content-lever plus presence gate, mechanical ordering re-scan) have now each been measured against MOD-04 and none reached the 87.5% bar. What would change that calculus: a lever that does not rely on the model correctly following either restated instructions or a self-check it performs on its own output — for example, a post-generation mechanical repair (not just detection) that the skill or a wrapping tool applies before the response reaches the user, rather than trusting the model's own re-scan to catch and fix its own ordering violation.
- `evals/conformance/run_conformance.py` is unchanged by this plan (verified byte-identical to its post-`03-09` state) and remains available for the next attempt at this measurement, whatever lever it targets.
- `AUD-01` and `ART-01` through `ART-04` remain Phase 6 LEG-04's to close via an actual human paraphrase-boundary read; this plan performed no such read and claims none.

## Self-Check: PASSED

- `git log --oneline --all | grep -q 0f47e8b` → FOUND
- `git log --oneline --all | grep -q 878b937` → FOUND
- All 23 Task-2 run-block commit hashes listed above found in `git log --oneline --all`.
- Re-ran all plan-level `<verification>` commands: `check_repo.py --self-test` → PASS, verified-codes catalogue includes `skill-family-order-gate-missing`; `--mutation-test` → `mutation-test PASS: 31 codes discrimination-proven`; plain `check_repo.py` → `check_repo: 0 violations`; `run_conformance.py --self-test` → `self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable`.
- Round integrity check: `git log --format='%s' --reverse -- evals/conformance/RESULTS-mod04.md | grep -E 'pre-committed disposition rule|anchored MOD-04 run block' | head -1` → prints the disposition-rule subject.
- `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` → `0`.
- `grep -cE '^- \[ \] \*\*(AUD-01|ART-01|ART-02|ART-03|ART-04)\*\*' .planning/REQUIREMENTS.md` → `5`.
- `WINDOWS.md` entry 8 JSON `status` field → `waived`; `03-UAT.md` `G-03-2` `status` → `partially_resolved` (unchanged).
- `evals/conformance/run_conformance.py` confirmed byte-identical to its post-`03-09` state (`git diff 5ce0ebb..HEAD -- evals/conformance/run_conformance.py` produces no output).
- Working tree clean (`git status --porcelain` prints nothing) at every commit boundary this plan made.

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-16*
