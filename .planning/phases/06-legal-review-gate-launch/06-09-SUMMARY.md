---
phase: 06-legal-review-gate-launch
plan: 06-09
subsystem: records
tags: [legal-review, cold-read, uat, checker, provenance, gap-closure]

requires:
  - phase: 06-legal-review-gate-launch
    provides: "Rounds 1-5 of cold reads, their corrections, and the four-brief standing set"
provides:
  - "The four round-5 gaps closed at source: G-06-17 (README), G-06-18 (LEGAL-REVIEW), G-06-19 (tooling and briefs), G-06-20 (the last closing round's own text)"
  - "A new build assertion: run_trigger_test.py --self-test compares INIT-EVENTS.md's documented init-event key set against the committed transcript tarball"
  - "The standing set widened — the fourth brief now reads every gap-closure commit range, not just the last one, and the whole-tree sweep runs two readers"
  - "A self-audit of this round's own added sentences that found and fixed eight further defects before closing"
affects: [phase-06-verification, round-6-cold-read]

actuals:
  tokens: 23000
  tasks: 21
  commits: 25

tech-stack:
  added: []
  patterns:
    - "Quoted-string and named-symbol citation anchors in place of path:N, extended to generated files"
    - "A recorded sweep command must be re-run after it is written down, because writing it down can change its own output"
    - "Counts sitting next to machine-readable data get asserted, not restated"

key-files:
  created: []
  modified:
    - README.md
    - LEGAL-REVIEW.md
    - tools/check_repo.py
    - evals/trigger/run_trigger_test.py
    - evals/trigger/INIT-EVENTS.md
    - evals/benchmark/bench-deal-brief.md
    - .planning/WINDOWS.md
    - .planning/phases/06-legal-review-gate-launch/06-UAT.md

key-decisions:
  - "Withdrew a correction rather than deleting it: 06-08's list/file 'fix' retired an accurate quotation, and the withdrawn marker is kept so a later round does not re-fix the same sentence"
  - "Ran prong 3's sweep instead of retracting its claim, because the round-4 objection to prong 2 applies verbatim"
  - "Did not ship a gate for the bench brief's timeline comparison — the brief states it in both orientations, so any frozen-literal gate would have to guess; filed as a WINDOWS id 17 candidate"
  - "Added a second whole-tree sweep reader on the same no-file brief, and made round 6 measure each reader's unique findings so the marginal value stops being a guess"
  - "Did not touch 03-03-PLAN.md or 03-03-SUMMARY.md, which carry the inherited fifteen-label miscount — completed planning artifacts are a historical record"

patterns-established:
  - "Self-reference check: after committing a grep/ls-files literal into prose, re-run it — twice this round the act of recording a command changed what it returns"
  - "A plan is not a source of truth over the record it was written from; task 20's own text asserted a sweep-reader yield the UAT record contradicts"
  - "Commit-message attributions are resolved with git log before the message is composed, never recalled"

requirements-completed: []

coverage:
  - id: D1
    description: "G-06-17 closed — README's three false statements (proxy-source scope, output-styles scanning, derivative regeneration trigger) corrected against the code they describe"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py"
        status: pass
      - kind: other
        ref: "python3 tools/generate_derivatives.py --check"
        status: pass
    human_judgment: true
    rationale: "Whether the corrected sentences read as honest and bounded to a first-time reader is the DIST-06 prose judgement no code here performs; it is round 6's subject."
  - id: D2
    description: "G-06-18 closed — eight LEGAL-REVIEW statements corrected: two unresolvable citations re-anchored, the source-row arithmetic, the surviving retracted phrase, prong 3's missing command, the withdrawn list/file correction, the non-existent machine check, the seven/six self-test count, and the TSDR 'answered' claim"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py"
        status: pass
      - kind: other
        ref: "git grep -rln \"Command of the Message spine is carved\" -- ':!LEGAL-REVIEW.md' ':!.planning'"
        status: pass
    human_judgment: true
    rationale: "Seven of the eight are prose corrections in a record no checker reads for meaning; only a cold reader can confirm the restatements are true and complete."
  - id: D3
    description: "G-06-19 closed — the citation code's block comment and scope comment corrected against their own docstring, INIT-EVENTS.md's key set corrected to 24 and asserted, the element-label count corrected to fourteen with its counting rule stated, and the bench brief's reversed comparison fixed"
    verification:
      - kind: unit
        ref: "python3 evals/trigger/run_trigger_test.py --self-test (init-event key-set case)"
        status: pass
      - kind: unit
        ref: "python3 tools/check_repo.py --self-test"
        status: pass
      - kind: unit
        ref: "python3 tools/check_repo.py --mutation-test (58 codes discrimination-proven)"
        status: pass
      - kind: unit
        ref: "python3 evals/benchmark/run_benchmark.py --self-test"
        status: pass
    human_judgment: false
  - id: D4
    description: "G-06-20 closed — the last two statements 06-08 wrote about its own new code and about ledger row 12's reader count"
    verification:
      - kind: unit
        ref: "python3 tools/check_repo.py --self-test"
        status: pass
    human_judgment: true
    rationale: "The strip_fences claim is verified by an AST census committed in the message, but whether row 12's restated reader count now matches every other statement of it in the file is a cross-document read."
  - id: D5
    description: "The standing set amended for round 6 — fourth brief widened from the last round's diff to every gap-closure commit range, whole-tree sweep taken from one reader to two, both recorded in 06-UAT.md and WINDOWS.md id 17 with the round-5 measurement pinned"
    verification:
      - kind: other
        ref: "gsd-tools windows status (ok: true, 32 rows, table re-derives byte-identically from the JSON fence)"
        status: pass
    human_judgment: true
    rationale: "Whether the widened brief actually reaches the defects it was widened for is only observable by running round 6."
  - id: D6
    description: "Task 18 self-audit — eight defects in this round's own added sentences found and fixed before closing, five of them class 1"
    verification:
      - kind: other
        ref: "every command literal committed this round re-run against the tree (8 checks, all reproducing their stated output)"
        status: pass
    human_judgment: true
    rationale: "A self-audit cannot certify its own completeness; round 6's readers are the check on it, which is this phase's standing closure condition."

duration: 95min
completed: 2026-09-22
status: complete
---

# Phase 06 Plan 09: Round-5 gap closure Summary

**All four round-5 gaps closed at source across five shipped files plus two records, one new build assertion added with a mutation probe and control, the cold-read brief widened past the last round's diff, and a self-audit that found eight further defects in the round's own prose before it closed.**

## Performance

- **Duration:** ~95 min
- **Tasks:** 21 planned, 21 executed
- **Commits:** 25 (21 task commits, 4 of them carrying self-audit fixes; 6 self-audit commits in total)
- **Files modified:** 8

## Accomplishments

- **Closed G-06-17 through G-06-20** — the eighteen checkably-false statements round 5 found, each corrected against the thing it describes rather than reworded.
- **Shipped one new assertion.** `run_trigger_test.py --self-test` now extracts the init-event key set from the committed transcript tarball and compares it to the block `INIT-EVENTS.md` publishes. Proven with a mutation probe on three sibling copies outside the repository: unmutated control rc=0, key-removed copy rc=1 with the assertion's own message naming `subtype`, heading-removed copy rc=1 through the loud `ValueError` branch rather than a silent empty-set pass.
- **Withdrew a correction instead of compounding it.** 06-08 "fixed" a quotation that was accurate: `check_repo.py` states its `source-gate-incomplete` ceiling twice, one word apart — "list" in the violation-code catalogue the paragraph cites, "file" in the function docstring. The marker is kept, restated, so a later round does not fix it a third time.
- **Gave prong 3 the command it claimed to have**, rather than retracting the claim — two sweeps over the whole tracked tree, both recorded with their real output including the one that matches the file it is recorded in.
- **Changed the method, not just the text.** The fourth standing brief read only the last round's diff and structurally could not see two of round 5's findings, authored by 06-05 and 06-06. It now reads every gap-closure commit range. The whole-tree sweep goes to two readers, with round 6 instructed to measure each reader's unique findings.
- **Audited the round's own added sentences and found eight more defects**, five of them the same class-1 scope overstatement round 5 measured as the largest.

## Task Commits

| # | Task | Commit |
|---|---|---|
| 1 | Bound README's proxy-source claim | `ade21af` |
| 2 | Scope README's output-styles claim to the local clone | `80a8bfd` |
| 3 | Correct README's regeneration trigger to four sources | `e6dfe0b` |
| 4 | Re-anchor three citations by quoted string | `89a9547` |
| 5 | Correct the source-row arithmetic | `dcc4643` |
| 6 | Restate the surviving "live unadjudicated" | `aa6da1d` |
| 7 | Run and record prong 3's sweeps | `0df417e` |
| 8 | Withdraw the list/file correction | `d9aef55` |
| 9 | Delete the launch section's machine-check claim | `44cc648` |
| 10 | Correct "seven self-tests" to six | `672a222` |
| 11 | Reconcile the TSDR "answered" claim | `e43829f` |
| 12 | Correct the citation code's block comment | `392c071` |
| 13 | Correct the "Both already carry" scope comment | `36ef0a9` |
| 14 | Correct and assert INIT-EVENTS.md's key set | `bac300a` |
| 15 | Correct the element-label count and state its rule | `ca5fdbf` |
| 16 | Correct the bench brief's reversed comparison | `afe8ea2` |
| 17 | Correct the last two closing-round statements | `7852bf3` |
| 19 + 20 | Widen the fourth brief; add a second sweep reader | `7323db5` |
| 21 | Resync the reproduced ledger rows 12 and 17 | `a15e357` |
| 18 | Self-audit (6 commits) | `f547989`, `9332f03`, `7ec801a`, `8f75cc6`, `05f2233`, `c50ae72` |

## Files Created/Modified

- `README.md` — three corrections: the proxy-source claim bounded to the three registry lists, the output-styles claim scoped to the local clone with the plugin case disclosed as untested, the regeneration trigger corrected to the generator's four reference files with the fifth named as not a source.
- `LEGAL-REVIEW.md` — eight corrections plus prong 3's two recorded sweeps and the resynced reproduction of ledger rows 12 and 17.
- `tools/check_repo.py` — four docstring/comment corrections: the citation block comment, the `CITATION_RECORD_PATHS` scope comment, the element-label count with its counting rule stated in the same sentence, and the `strip_fences` comparison dropped.
- `evals/trigger/run_trigger_test.py` — `documented_init_key_set()`, `observed_init_key_sets()` and a new self-test case (+96 lines).
- `evals/trigger/INIT-EVENTS.md` — `subtype` added in sorted position; the block now asserted rather than restated.
- `evals/benchmark/bench-deal-brief.md` — the Timeline comparison corrected to "longer than".
- `.planning/WINDOWS.md` — id 17 amended through the JSON fence, table re-rendered from it.
- `.planning/phases/06-legal-review-gate-launch/06-UAT.md` — a fifth "seven self-tests" site corrected and a new standing-set section for round 6.

## Decisions Made

1. **Withdrew rather than deleted the list/file correction.** A withdrawn correction is a record this file needs; deleting it leaves the next round free to "fix" the same sentence again. The separate question — making the two `check_repo.py` docstrings agree — is backlog, noted in the marker, not done here.
2. **Ran prong 3's sweep rather than stating no command was needed.** The round-4 reader's objection to prong 2 was that an unqualified negative needs a recorded command; it applies here verbatim.
3. **Did not ship a gate for the bench brief's timeline.** The canonical figures are machine-readable, but the brief states the comparison in both orientations — the programme is longer, the window is shorter, both correct — so a frozen-literal gate would have to guess which orientation a sentence uses. Filed as a candidate in WINDOWS id 17 alongside enforcement-scope checking. This is the sixth time this repository has refused a fuzzy proxy.
4. **Yes to a second sweep reader**, on the same no-file brief, with round 6 measuring each reader's unique findings and a stated exit condition (drop back to one if the marginal yield is zero for two consecutive rounds).
5. **Adopted 03-03-PLAN.md's own 14-entry verification list as the element-label definition**, and stated the rule in the same sentence, because "element label" is defined in no committed file and that is why the miscount survived three phases.
6. **Left `.planning/WINDOWS.md`'s round-1 historical text intact.** It says "seven self-tests rc=0" and already carries its own inline correction in the same reason field. The literal grep target the plan set was not achievable without erasing the record.

## Deviations from Plan

### Auto-fixed issues

**1. [Rule 1 — plan claim wrong against the record] Task 20's sweep-reader yield**
- **Found during:** Task 18
- **Issue:** The plan asserted all eight of round 5's pre-Phase-6 findings were reached by the single sweep reader, and that it found "four two-file contradictions plus" two more. `06-UAT.md`'s own test records give the sweep four findings in total, three of them pre-Phase-6; the other five came from the file-named briefs.
- **Fix:** Wrote the measured numbers into the standing-set section, with a marker recording that the claim came from the plan and that a plan is not a source of truth over the UAT record.
- **Verification:** Per-brief yields recomputed from 06-UAT.md: 3 + 8 + 4 + 3 = 18.
- **Committed in:** `7ec801a`

**2. [Rule 1 — plan list wrong] The strip_fences census**
- **Found during:** Task 17
- **Issue:** The plan named six functions that read raw and never call `strip_fences`. One of them, `check_results_breakdown_count`, calls it at the top of its body.
- **Fix:** Replaced the list with an AST census of all 51 `check_*` functions — 15 call it, 36 do not — and rested the correction on the census rather than the list.
- **Verification:** AST walk re-run; committed in the message.
- **Committed in:** `7852bf3`

**3. [Rule 1 — verify criterion not achievable as literally written] Task 10's grep**
- **Found during:** Task 10
- **Issue:** The plan's verify was `git grep -n "seven self-tests"` returns nothing. Four of the remaining matches are the phrase quoted inside correction markers and UAT findings, and one is WINDOWS id 17's round-1 historical text with its correction adjacent.
- **Fix:** Corrected both live assertions and classified every remaining match in the commit message, rather than erasing the record to satisfy a literal grep.
- **Verification:** Every remaining occurrence enumerated and classified.
- **Committed in:** `672a222`

**4. [Rule 2 — missing from the plan] Task 11's second error**
- **Found during:** Task 11
- **Issue:** The gap said the two TSDR endpoints that failed in research were re-attempted and one did not answer. `06-RESEARCH.md`:457-459 records three failures, and `tsdrapi.uspto.gov` is not among them — it was attempted for the first time at the review.
- **Fix:** Restated all three affected sentences to what the table and the research record hold.
- **Committed in:** `e43829f`

---

**Total deviations:** 4 (3 × Rule 1, 1 × Rule 2). **Impact:** all four made the corrections more accurate than the plan specified. No scope creep; nothing outside the plan's files was touched.

## Issues Encountered

**The self-audit found eight defects in this round's own added sentences.** Five class 1 (scope overstatement about a mechanical thing), two class 3 (a count next to the thing it counts), one class 2 (a reference resolving to the wrong content). Fixed in six commits, each naming its class:

1. `f547989` — the quoted-string anchor task 4 recorded became self-referential when it was written down; the recorded grep returned six files, not three. The identical defect task 7 had caught and disclosed two tasks earlier.
2. `9332f03` — "four other methodology sections" was three, measured against `9f841df`.
3. `7ec801a` — the second-reader justification overstated the sweep's yield (above).
4. `8f75cc6` — two markers: the "remote" strings were attributed to one function when they sit at three sites, and "the only recorded whole-repo sweep was prong 2's" was false against two other tree-wide sweeps in the same file.
5. `05f2233` — task 3's README rewrite reused the generator comment's sentence but narrowed its referent from five sources to four, making a true claim false for 20 of 28 rules.
6. `c50ae72` — task 7's new paragraph attributed the order-provenance concession to prong 2's correction, which does not make it.

**What this says about the round.** 06-08's self-audit found seven and its code-review gate two more, and round 5 still found eight in its output. This round's self-audit found eight, in the same proportions round 5 measured — class 1 largest. The two self-reference defects are new in kind and neither was catchable by reading the sentence back: both needed the command re-run after it was committed to prose.

## Next Steps

**Phase 6 verification, then round 6's cold read.** The four gaps are closed at source; whether they are closed in fact is what round 6's readers decide, against a standing set that now runs six readers with a widened fourth brief and a doubled sweep. `WINDOWS.md` id 12 closes when a round returns none; five rounds have not.

## Self-Check: PASSED

- All 21 tasks executed and committed atomically.
- All 10 CI commands green at HEAD: `check_repo.py --self-test`, `--mutation-test` (58 codes discrimination-proven), `check_repo.py` 0 violations, six `evals/` self-tests, `generate_derivatives.py --check`.
- Every command literal this round committed into prose re-run against the tree and reproducing its stated output (8 checks).
- `gsd-tools windows status` → `ok: true`, 32 rows, rendered table re-derives byte-identically from the JSON fence.
- `REQUIREMENTS.md` carries no `[x]` beside an UNVERIFIED note; LEG-04 and LEG-05 remain unchecked, correctly.
- No completed planning artifact from an earlier phase was modified.
