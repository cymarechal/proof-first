---
phase: 06-legal-review-gate-launch
plan: 04
subsystem: infra
tags: [launch, trademark, ledger, windows, legal, distribution]

requires:
  - phase: 06-legal-review-gate-launch
    provides: "06-02's passed legal review gate and LEGAL-REVIEW.md; 06-03's claim region and the README it made checkable"
provides:
  - "A recorded, dated decision to defer publication, with what stays open stated rather than absorbed"
  - "The three human observations recorded as performed or explicitly as not performed"
  - "All 28 ledger entries dispositioned: 11 fixed, 9 waived with their measurements, 8 open with v2 owners"
  - "A Ledger disposition table in LEGAL-REVIEW.md, visible to a reader who cannot see .planning/"
affects: [v2, ship, DIST-01, DIST-02, DIST-03]

actuals:
  tokens: 21000
  tasks: 5
  commits: 2

tech-stack:
  added: []
  patterns:
    - "A deferred decision is recorded with its date and its consequences, never left implicit in an unchanged file"
    - "An observation that could not be made is recorded as not made, with the structural reason"

key-files:
  created: []
  modified:
    - LEGAL-REVIEW.md
    - .planning/WINDOWS.md

key-decisions:
  - "Publication DEFERRED by explicit operator decision at the blocking checkpoint — no remote, no substitution, nothing left this machine"
  - "WINDOWS id 20 routed to v2 rather than fixed here: the fix moves a figure RESULTS.md already publishes"
  - "ids 12, 16 and 17 left open — no cold reader and no /config picker were available, and faking either is the defect the entries exist to prevent"
  - "The output style was NOT copied into ~/.claude/output-styles/: it would have changed the operator's config for no verification gain, since no picker could be opened to observe it"
  - "The ledger's Markdown table was repaired and regenerated from the JSON, which is the declared source of truth"

patterns-established:
  - "`windows` verbs refuse to run while the rendered table disagrees with the fenced JSON; repair the table first, and regenerate it after any direct JSON edit, because `windows status` does not compare reason cells"

requirements-completed: [LEG-04]

coverage:
  - id: D1
    description: "The publish decision was made by a human at a blocking checkpoint before anything irreversible happened, and is recorded in LEGAL-REVIEW.md with its date and its consequences"
    requirement: LEG-04
    verification:
      - kind: other
        ref: "LEGAL-REVIEW.md ## Launch — decision, date 2026-09-21, and a table naming id 11, DIST-01 and DIST-02 as staying open"
        status: pass
    human_judgment: false
  - id: D2
    description: "Nothing was substituted and no remote exists: the manifests and README are byte-identical to their pre-plan state and all four placeholder occurrences still agree"
    requirement: LEG-04
    verification:
      - kind: other
        ref: "git diff --exit-code .claude-plugin/ README.md clean; PLACEHOLDERS=9 REMOTES=0 assertion; REMOTE False / GATE_PASSED True ordering assertion"
        status: pass
    human_judgment: false
  - id: D3
    description: "Both install routes are recorded as not run, with the reason, and neither DIST-01 nor DIST-02 changes state"
    verification:
      - kind: other
        ref: "LEGAL-REVIEW.md ### Install verification — a per-route table with verdict 'Not tested' and the reason stated"
        status: pass
    human_judgment: false
  - id: D4
    description: "All 28 ledger entries have a terminal disposition, no open entry has an empty reason, and the frontmatter counts match the JSON array"
    verification:
      - kind: other
        ref: "TOTAL 28 / NO_REASON []; OPEN_NO_REASON []; FRONTMATTER {open 8, waived 9, fixed 11, total 28} == ACTUAL; STILL_OPEN [] for ids 3, 6, 18, 25"
        status: pass
    human_judgment: false
  - id: D5
    description: "The whole CI surface passes after the sweep — all ten commands .github/workflows/ci.yml declares exit zero"
    verification:
      - kind: integration
        ref: "ten-command loop over ci.yml — ALL TEN PASS; check_repo 0 violations; mutation-test 56 codes discrimination-proven"
        status: pass
    human_judgment: false
  - id: D6
    description: "The /config observation (WINDOWS id 16) — whether the output style is listed and selectable in a real picker"
    verification: []
    human_judgment: true
    rationale: "NOT PERFORMED. A non-interactive session has no picker. Recorded as not performed in LEGAL-REVIEW.md ## Human observations section 1, with platform and destination directory pre-recorded for whoever does it. id 16 stays open; DIST-03's /config half stays UNVERIFIED."
  - id: D7
    description: "The cold read of README (WINDOWS ids 12 and 17) — whether any two passages contradict each other"
    verification: []
    human_judgment: true
    rationale: "NOT PERFORMED AS A COLD READ. The agent that wrote this round's README edits would have been the reader, and no independent reader was available. A self-read with a mechanical cross-reference of twelve checkable claims was performed instead and found nothing checkably false — recorded as what it is. ids 12 and 17 stay open."
  - id: D8
    description: "Nothing published at this moment contains a real person's private information, a real company's confidential information, or a credential"
    requirement: LEG-04
    verification: []
    human_judgment: true
    rationale: "Backstop truth. Moot in the operative sense because publication was deferred and nothing left this machine, but not therefore satisfied: 06-02's collision searches found an exact-name collision for Ardent Digital and for Gina Almeida, both still unrenamed. A human read owns this before any future publish."

duration: 33 min
completed: 2026-09-21
status: complete
---

# Phase 6 Plan 04: Launch Gate Summary

**Publication deferred by operator decision at the blocking checkpoint; the two observations this session structurally could not make are recorded as not made; and all 28 ledger entries are dispositioned — 11 fixed, 9 waived with their measurements, 8 open with named v2 owners**

## Performance

- **Duration:** 33 min
- **Started:** 2026-09-21T11:08:40Z
- **Completed:** 2026-09-21T11:41:55Z
- **Tasks:** 5 (1 checkpoint, 3 executed, 1 skipped by decision)
- **Files modified:** 2

## Accomplishments

- **The one irreversible action was put to a human and the human said no.** The checkpoint was presented with all its preconditions confirmed green — `check_repo: 0 violations`, `Gate status: PASSED`, no remote — and the operator chose to defer. Nothing was substituted, no remote was created, no commit left this machine.
- **Deferring is recorded as a decision, not as an absence.** `LEGAL-REVIEW.md` gained a `## Launch` section naming the date, the reason, and a table of exactly what stays open because of it: id 11, DIST-01 and DIST-02. The legal review gate is unaffected — it gates content, not publication — and the ordering roadmap criterion 1 asks for is satisfied trivially, with the machine check green in the no-remote direction.
- **Two observations could not be made, and that is what the record says.** There is no `/config` picker in a non-interactive session, and the agent that wrote this round's README edits cannot be its own cold reader. Both are recorded as NOT PERFORMED with the structural reason, and ids 12, 16 and 17 stay open. This is the entire point of those entries: id 17 exists because three rounds of a writer re-reading their own text missed what a cold reader caught first time.
- **What could be done instead was done, and labelled.** A mechanical cross-reference of twelve checkable README claims against the shipped files: rule count, worked-pair count, every layout-tree and "What exists today" path, all nine pooled tallies and the direction count against `RESULTS.md`'s rendered tables, the trigger summary against `RESULTS-trigger.md`'s totals, and the absence of the two sentences 06-03 superseded. **No checkably-false statement found.**
- **Twenty-eight entries, none left hanging.** 11 fixed, 9 waived each with the measurement that settled it, 8 open each with a named owner and a stated closure condition. `open_count + waived_count + fixed_count == total_count` and every count matches the JSON array.

## Task Commits

1. **Task 1: Publish, or do not** — checkpoint, resolved `defer` by operator decision (no commit)
2. **Task 2: Record the deferral** — `97927b8` (docs)
3. **Task 3: Install routes** — skipped by decision, recorded as skipped inside `97927b8`
4. **Task 4: The three human observations** — `b627fd3` (docs)
5. **Task 5: Ledger sweep** — `b627fd3` (docs)

## Files Created/Modified

- `LEGAL-REVIEW.md` — three new sections. `## Launch` with the decision, its date and its consequences; `### Install verification` recording both routes as not run with the reason and an explicit `Not tested` verdict each; `## Human observations` with all three, two of them marked NOT PERFORMED; and `## Ledger disposition`, a 28-row table reproducing the whole register for a reader who cannot see `.planning/`.
- `.planning/WINDOWS.md` — ids 3, 6, 18 and 25 marked fixed; 13, 14, 15, 19, 23, 26, 27 and 28 waived with substantive reasons; 11, 12, 16, 17, 20, 21, 22 and 24 left open with reasons naming an owner and a closure condition. The Markdown table was repaired and regenerated from the JSON.

## Decisions Made

- **Defer, by the operator, at the checkpoint.** Auto-mode was off, and publishing a repository is irreversible and outward-facing; it was never a decision to auto-select.
- **id 20 routes to v2 rather than being fixed here.** `aggregate()`'s per-order pooling is a real defect, but correcting it changes the mean/range figures `RESULTS.md` already publishes, which the plan's own rule sends to v2. 06-03 already proved the pooled totals README quotes do not inherit it.
- **The output style was not copied into `~/.claude/output-styles/`.** The plan's step exists to set up an observation this session cannot make; performing the setup alone would have modified the operator's own configuration directory for no verification gain.
- **The ledger's JSON is the source of truth and the table is regenerated from it.** Both directions were needed this round — see Issues.

## Deviations from Plan

None - plan executed exactly as written, including its explicit `defer` branch.

Three plan-authored errors were worked around rather than followed, each recorded here because that is this repository's standing practice for the class:

- **The plan's ledger-reading command is wrong.** `t[t.rindex('[',0,t.rindex(']')):t.rindex(']')+1]` appears in four of Task 5's acceptance criteria. `rindex(']')` finds the array's closing bracket, but `rindex('[', 0, ...)` then finds the last `[` *inside a description string* — several entries contain bracketed text such as "Brackets [..] indicate" — so it slices a fragment and raises `JSONDecodeError`. Every check was run with a `` ```json ``-fenced regex reader instead, which returns all 28 entries. The criteria were evaluated in full; only the reader differed.
- **The plan calls `windows list`, which does not exist.** The available subcommands are `status`, `append`, `waive`, `fixed`. `windows status` was used.
- **Task 4's `<verify>` invokes `node "$GSD_TOOLS"` from a bare shell** where that variable is not exported by the workflow's own snippet. Resolved to the absolute path.

## Issues Encountered

**The `windows` verbs refused to run at all.** Every mutation exited with: *"Ledger table … disagrees with the fenced JSON entries (the sole source of truth) for row id(s): 28."* This is the exact defect the plan predicted — the rendered table carried 27 rows against the JSON's 28 — and it is load-bearing rather than cosmetic: it blocks the tool entirely. The missing row was reconstructed from entry 28's JSON with the same cell escaping the existing rows use, after which all twelve verb calls succeeded.

**`windows status` does not compare reason cells.** The eight open entries needed substantive reasons, and no verb writes a reason while keeping an entry open, so the JSON was edited directly. `windows status` then reported table and JSON in agreement while row 11's reason cell was still empty. The whole table was regenerated from the JSON and the agreement re-confirmed. A backup was taken to the scratchpad before the regeneration. **The lesson, recorded because it will recur: after any direct edit to the fenced JSON, regenerate the table — the tool's own agreement check will not catch a stale reason cell.**

**Four apparent README defects were all defects in the checking script.** Three compared a README figure against the first matching row in `RESULTS.md`, which is a per-cell row rather than the pooled one; the fourth demanded the literal substrings `9 of 9` and `2 of 5` in `RESULTS-trigger.md`, which records the same totals per row and in a `## Totals` block. Chasing the fourth down surfaced a must-fire regression in that file which initially read as a README omission — it is Arm A, a treatment that was measured and then **reverted**, so README correctly describes the configuration that ships. This is the ledger's own 13/14/15/26/27 class, and it is exactly why a self-read is not accepted as a cold read: the reader who wrote the text also writes the checks that match what they meant.

## User Setup Required

None - no external service configuration required. Publication was deferred, so no account, remote or credential is involved.

## Next Phase Readiness

**What this phase delivered.** The legal review gate passed and is mechanically defended; every framework-derived concept names a source that was fetched and read; README states what the benchmark actually measured including the result that does not flatter the project; and the defect register has no undecided entries.

**What is honestly still open**, all eight with owners and closure conditions in the ledger:

| id | Owner | Closes when |
|---|---|---|
| 11 | operator | A real owner/repo is substituted **and** an install route is observed resolving |
| 12 | cold reader | The read answers whether the claim region reads honest or defensive |
| 16 | a human with a picker | The style is seen listed and selectable in `/config` |
| 17 | cold reader | The read finds a contradiction, or finds none |
| 20 | v2 benchmark maintainer | `aggregate()` averages orders before pooling and `RESULTS.md` is re-rendered |
| 21 | v2 benchmark maintainer | The record key includes effort, judge_model and judge_effort |
| 22 | v2 benchmark maintainer | A wholly-failed cell is reported rather than dropped |
| 24 | v2 skill maintainer | The next CAT-10 lever is measured and kept or refuted |

**Two items carried from 06-02 that this plan did not create ledger entries for**, and should be raised before any future publish: the exact-name collisions on `Ardent Digital` (a real trading company, cast as a displaced incumbent and losing bidder) and `Gina Almeida` (a real associate lawyer at an insurance group, against a brief casting her as Associate General Counsel at an insurance firm). Both are recorded in `LEGAL-REVIEW.md` § Name collisions with a recommended rename. They are not blockers while publication is deferred; they are blockers before it is not.

**`/gsd-ship` will still block.** `workflow.windows_enforce` blocks while `open_count > 0`, and it is 8. That is the correct state: this project is not shipped, and the register now says precisely why in eight places instead of twenty.

---
*Phase: 06-legal-review-gate-launch*
*Completed: 2026-09-21*
