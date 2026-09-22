---
phase: 06-legal-review-gate-launch
plan: 06-10
subsystem: testing
tags: [legal-review, cold-read, checker, self-test, mutation-test, conformance, provenance]

requires:
  - phase: 06-legal-review-gate-launch
    provides: "Rounds 1-6 of the cold read, the standing brief set, and the nine prior gap-closure plans whose text this round audits"
provides:
  - "Twenty-five checkably-false statements from round 6 corrected across four shipped files and two planning records"
  - "catalogue_matches_registry() — the first mechanical guard this phase has shipped against the scope-absolute class"
  - "A read-tracer measurement of which check_* frame opens which path, replacing three false scope absolutes with data"
  - "The standing set for round 7: a fifth .planning/ brief, a widened self-audit scope, and a re-run-after-SUMMARY rule"
affects: [round-7 cold read, LEG-04, LEG-05, gsd-verify-work]

actuals:
  tokens: 35508
  tasks: 27
  commits: 32

tech-stack:
  added: []
  patterns:
    - "Docstring-catalogue-versus-registry assertion in --self-test"
    - "Read-tracer (pathlib.Path.read_text wrapper recording the enclosing check_* frame) as a build-time instrument, not a shipped check"
    - "Measurements pinned to the HEAD they were taken at, never written as live counts"

key-files:
  created: []
  modified:
    - tools/check_repo.py
    - LEGAL-REVIEW.md
    - SOURCES.md
    - evals/conformance/RESULTS-mod04.md
    - .planning/WINDOWS.md
    - .planning/phases/06-legal-review-gate-launch/06-UAT.md

key-decisions:
  - "Task 20 shipped the catalogue assertion and refused the frozen path-to-readers map, on a measurement rather than a preference: the three readers whose absence produced this round's findings all reach their paths through module constants or a glob and carry no path literal in their bodies, so a static scan would have found none of them."
  - "Enumerations that a round falsifies by writing them down are dropped rather than re-counted. Three sites lost a count and kept the scoped result or the counting rule instead."
  - "Measurements that move with HEAD are pinned to the commit they were taken at. Three copies of the change-1 figure were pinned after the round's own task-4 commit moved one arm from 0 to 1."
  - "The plan's own numbers were treated as claims to verify, not as inputs. Two were wrong and the tree decided both."

patterns-established:
  - "Correction markers: four forms in use (Corrected, Added, Updated, Clarified), covered by one grep, with Clarified explicitly counted"
  - "Scope sentences point at the one place the scope is enumerated rather than restating it"
  - "Mutation probes run against an unmutated sibling control and assert on messages, not just exit codes"

requirements-completed: []

coverage:
  - id: D1
    description: "G-06-21 — twelve false statements in LEGAL-REVIEW.md corrected against re-run measurements"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations); OpenLibrary edition records re-fetched live 2026-09-22"
        status: pass
    human_judgment: true
    rationale: "Prose truth against the tree is what the cold read exists to test; a green checker is exactly the condition under which all six rounds found these."
  - id: D2
    description: "G-06-22 — eleven false statements across RESULTS-mod04.md, check_repo.py and SOURCES.md corrected"
    verification:
      - kind: other
        ref: "all ten .github/workflows/ci.yml commands rc=0; read-tracer confirms the 23-file scope and the per-path reader lists"
        status: pass
    human_judgment: true
    rationale: "Same as D1 — the checker was green while every one of these was false."
  - id: D3
    description: "catalogue_matches_registry() asserts the docstring catalogue against ALL_CHECK_CODES in both directions"
    verification:
      - kind: unit
        ref: "python3 tools/check_repo.py --self-test"
        status: pass
      - kind: other
        ref: "mutation probe on sibling copies: control exit 0/0 FAIL, entry-deleted exit 1, phantom-entry exit 1, both asserting on message text"
        status: pass
    human_judgment: false
  - id: D4
    description: "G-06-23 — the round's own record corrected, and the standing set for round 7 recorded"
    verification:
      - kind: other
        ref: "gsd-tools windows status ok:true at 32 rows; 06-UAT.md 24 tests / 5 pass / 19 issue matching its Summary block"
        status: pass
    human_judgment: true
    rationale: "Whether the three process changes actually reach the defects they target is what round 7 measures; this round can only record them."

duration: 95min
completed: 2026-09-22
status: complete
---

# Phase 06 Plan 10: Round-6 gap closure Summary

**Twenty-five checkably-false statements corrected across six files, and the first mechanical guard this phase has shipped against its dominant defect class — a self-test assertion that the checker's own violation-code catalogue matches its registry, which caught 57 listed against 58 implemented.**

## Performance

- **Duration:** ~95 min
- **Tasks:** 27 planned, 27 executed
- **Commits:** 32
- **Files modified:** 6

## Accomplishments

- **G-06-21, twelve statements in `LEGAL-REVIEW.md`.** All three OpenLibrary edition records were re-fetched live; `OL38629171M` carries no `by_statement` field, so "three rows" became two plus a named alternative confirmation method. Two enumerations were dropped rather than re-counted, because each had been falsified by the round that wrote it.
- **G-06-22, eleven statements across three files.** The CR-01 banner was scoped to the commit boundary its own closing paragraph already drew; six inverted `above`/`below` references were corrected where the gap listed three; two timeout attributions were corrected while the published `N_A`/`M_A` and `N_B`/`M_B` figures were independently re-derived and explicitly fenced against reopening.
- **Task 20 settled, with a command behind it.** `catalogue_matches_registry()` ships in `--self-test`. It is exact rather than a proxy — both sides are lists the module already holds — and it caught the live instance the round found.
- **Three false scope absolutes replaced by measurement.** A read-tracer recorded the enclosing `check_*` frame of every read in a live run. `readme-claim-unsourced` reads all four `evals/*/RESULTS*.md`; `SOURCES.md` and `LEGAL-REVIEW.md` are each read by three codes. The comment now lists readers per path instead of denying them.
- **G-06-23, the round's own record.** The fourth brief's range notation was corrected at both sites through `WINDOWS.md`'s JSON fence; the finding counts were corrected to seven and three; one citation in round 6's own finding was shown not to resolve even at `66322b1` and re-anchored.

## Task Commits

| Task | Commit |
|---|---|
| 1 `by_statement` claim | `d33b78a` |
| 2 prong-3 wording | `692e9fb` |
| 3 bullet pointer | `7d7f6ac` |
| 4 fixture self-contradiction | `5e9b6de` |
| 5 non-existent entity check | `3710b9a` |
| 6 occurrence count + counting rule | `2c80f22` |
| 7 correction-marker universal | `aeb8bfc` |
| 8 publish-location count | `9e69ebd` |
| 9 ledger row 15 AST claim | `add066d` |
| 10 ledger row 30 ground | `331077b` |
| 11 "two existing sentences" | `b41b17a` |
| 12 unscoped sweep enumeration | `0154c3a` |
| 13 CR-01 banner scope | `411cbb9` |
| 14 six inverted directions | `06ddefd` |
| 15 timeout attributions + figure fence | `17534a6` |
| 16 checker opening scope | `d448ed6` |
| 17 missing catalogue entry | `4dc3eb7` |
| 18 ten offline commands | `cdf5384` |
| 19 three scope absolutes + SOURCES stamp | `42595c4` |
| 20 catalogue assertion | `ca6e9d4` |
| 21 range notation (2 sites) | `1c41a2a`, `2c0b6c5` |
| 22 finding counts + citation | `68b411e`, `4e8b05c` |
| 23-26 standing set for round 7 | `81495a3`, `fa098bc`, `508da39`, `2f7b978`, `3182a3d` |
| 27 self-audit + record closure | `2ee08a1`, `de2ec28` |

## Decisions Made

- **Ship the catalogue assertion; refuse the frozen map — on evidence.** The plan permitted either. The frozen path-to-readers map was refused because the three readers whose absence produced this round's findings reach their paths through `CITATION_RECORD_PATHS`, `SOURCES_PATH`/`LEGAL_REVIEW_PATH` and `CLAIM_SOURCE_GLOB`; none carries a path literal in its body, so the static scan that would assert the map without tracing would have found zero of the three. The tracer stays a build-time instrument. A regex over comment prose was refused outright, as six times before.
- **Drop counts instead of correcting them, where the count moves when written.** Three sites lost an enumeration and kept the scoped result or the counting rule. The correction-marker paragraph, the unexcluded sweep, and the phrase-occurrence count are all now stated as properties or rules rather than tallies.
- **Pin measurements to the HEAD they were taken at.** The change-1 figure appeared in three places as a live `..HEAD` count. This round's own task-4 commit moved one arm from 0 to 1, by quoting the wording it removed exactly as the correction convention requires. All three copies are pinned to `66322b1`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Plan figure wrong against the tree] Task 15's "second attempt in each case"**
- **Found during:** Task 15
- **Issue:** The plan stated all three timeout attributions should move to the second attempt. Arm A's `A-rfp-answer` timeout genuinely is the first attempt.
- **Fix:** Corrected the two that were wrong (Arm A `B-proposal-section`, Arm B `A-rfp-answer`) and left the one that was right.
- **Verification:** Re-derived twice — from the run blocks in file order, and independently from the 23 per-block commit subjects carrying `repeat=` and `(timeout, excluded)`/`(retry)` labels. The two agree.
- **Committed in:** `17534a6`

**2. [Rule 1 - Plan figure wrong against the tree] Task 6's "correct to four"**
- **Found during:** Task 6
- **Issue:** The plan said the phrase occurs four times. It did when the plan was written; task 5's edit removed one before task 6 ran.
- **Fix:** Replaced the tally with the counting rule, and recorded that the count moved inside the round.
- **Verification:** Line-based and wrap-tolerant counts both re-run after the edit.
- **Committed in:** `2c80f22`

**3. [Rule 2 - Missing from plan, same class] Three more inverted directional references**
- **Found during:** Task 14
- **Issue:** The gap named three; checking them surfaced three more of the identical class in two other sections.
- **Fix:** All six corrected in one change, replacing direction with a name or a commit wherever possible.
- **Committed in:** `06ddefd`

**4. [Rule 2 - Missing from plan, same class] Round 6's own finding C cited a line that never resolved**
- **Found during:** Task 22
- **Issue:** Finding C cited `06-UAT.md`:1417 and `:1907`. At `66322b1`, `:1907` held an unrelated gaps-block line.
- **Fix:** Both sites re-anchored by field name.
- **Committed in:** `4e8b05c`

**5. [Rule 2 - Missing from plan, same class] `LEGAL-REVIEW.md` ledger rows 12 and 17 stopped at round 5**
- **Found during:** Task 27
- **Issue:** Row 12 read "five rounds" and "five have not" after six had run; row 17 opened "Eighth round of the pattern" and then enumerated five.
- **Fix:** Round 6 recorded in both; row 17's ordinal replaced by the enumeration, which is checkable.
- **Committed in:** `2f7b978`

**6. [Rule 1 - Self-audit] Two defects in this round's own added sentences**
- **Found during:** Task 27
- **Issue:** "No set of four exists anywhere in that check" — `_owner_segment` normalises four GitHub URL forms. And "edited twice", a count taken from the plan rather than from `git log -L`, which shows three.
- **Fix:** Both restated with the counterexample named and the three SHAs given.
- **Committed in:** `2ee08a1`

---

**Total deviations:** 6 auto-fixed (2 plan figures falsified by the tree, 3 same-class findings beyond the gap's enumeration, 1 self-audit pair)
**Impact on plan:** No scope creep. Items 3-5 are the same defect classes the gap names, found by checking the instances it listed; leaving them would have handed round 7 findings this round was the only place to fix.

## Issues Encountered

- **A correction can falsify its own verify command.** Task 2's first draft quoted the phrase it removed, and the plan's verify command then matched the correction itself. Rewritten to state the prong's real wording without reproducing the wrong one. The same mechanism moved the change-1 measurement at task 4, where reproducing the removed wording is required by the correction convention — handled there by pinning the measurement instead.

## Post-SUMMARY re-run of committed command literals (change 5, first execution)

The rule this round wrote into the standing set was run against this round, after the SUMMARY
commit `a952906` landed. Eleven command literals were re-run at that HEAD:

| Literal | Prose says | Re-run says |
|---|---|---|
| the four-form correction-marker grep over `LEGAL-REVIEW.md` | lists every marker | 43 markers, 0 missed |
| wrap-tolerant vs line-based count of the PF-1 label phrase | the two disagree by one | 3 vs 2 |
| `git grep -o '<owner>/<repo>' -- .claude-plugin README.md \| wc -l` | nine | 9 |
| `git grep -n 'import ast' -- '*.py'` and the `ast.` forms | nothing | nothing |
| scoped `Command of the Message spine is carved` sweep | exactly three files | 3 |
| `ade21af^..66322b1` / `d67012e^..66322b1` added-line arms | 0 and 1 | 0 and 1 |
| `ci.yml` distinct scripts / commands | eight / ten | 8 / 10 |
| a live run of the checker opens | 23 files | 23 |
| docstring catalogue vs `ALL_CHECK_CODES` | 58 vs 58, empty diff | 58 vs 58, empty |
| the two `RESULTS-mod04.md` split counts | 14 and 12 | 14 and 12 |
| `visual arrangement` outside `.planning/` | nothing | nothing |

Nothing moved. That is the outcome to record, not a reason to skip the step: the rule exists
because `LEGAL-REVIEW.md`'s sweep count was true when written and false five commits later, and
this round's own change-1 measurement moved from 0 to 1 mid-round for exactly that reason. The
mid-round catch is recorded under Decisions Made; this table is the post-SUMMARY pass, and it is
clean.

## Next Phase Readiness

- All ten CI commands green: `check_repo.py --self-test` (58 codes), `--mutation-test` (58 discrimination-proven), live run 0 violations, six `evals/` self-tests, and `generate_derivatives.py --check`.
- `gsd-tools windows status` ok at 32 rows; `WINDOWS.md` frontmatter matches its JSON fence exactly.
- `LEG-04` and `LEG-05` stay unchecked by design. This round corrected its own record; whether the corrections hold is round 7's independent read, not this round's self-check.
- Round 7 runs five briefs, eight readers: the two file-named hunts, the two-reader whole-tree sweep, the gap-closure-range brief at `d67012e^..HEAD`, and the new one-reader `.planning/` sweep.

---
*Phase: 06-legal-review-gate-launch*
*Completed: 2026-09-22*
