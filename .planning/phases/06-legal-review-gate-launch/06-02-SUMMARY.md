---
phase: 06-legal-review-gate-launch
plan: 02
subsystem: testing
tags: [check_repo, mutation-testing, provenance, trademark, legal, stdlib-python]

requires:
  - phase: 06-legal-review-gate-launch
    provides: "06-01's source-row-unconfirmed, the frozen Where-cell format, SOURCES_CHECK_CODES/run_sources_checks, and 'SOURCES.md' in MUTATION_SOURCES"
provides:
  - "All six SOURCES.md rows verified against live public pages, each with a URL and an ISO-8601 retrieval date"
  - "LEGAL-REVIEW.md — the dated diligence record behind NOTICES.md and SOURCES.md, with a frozen machine-read gate marker"
  - "source-gate-incomplete — a declared pass over an incomplete source list is a build failure"
  - "framework-statement-stale-review — a re-dated review that left a statement unread is a build failure"
  - "Three NOTICES.md framework statements reconfirmed against what changed since 2026-09-10"
affects: [06-03, 06-04, LEG-04, LEG-05, WINDOWS.md ledger]

actuals:
  tokens: 33000
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns:
    - "Evidence log separate from normative notice: NOTICES.md states the posture, LEGAL-REVIEW.md carries the dated evidence, one frozen marker binds them"
    - "A failed lookup is recorded as a failure with its HTTP status, never rounded to an assumption"

key-files:
  created:
    - LEGAL-REVIEW.md
  modified:
    - SOURCES.md
    - NOTICES.md
    - tools/check_repo.py

key-decisions:
  - "The register was observed live and active against a court order directing cancellation — recorded as an observation, with no interpretation of the gap between the two"
  - "The MEDDPICC genericness holding supports one narrow point in the id-6 reasoning and no more: genericness of a term and protectability of an expression are separate questions under separate law"
  - "The MC block order is the acronym itself, not a source's chosen arrangement — reordering would produce a different word, not a rearranged list"
  - "Challenger's statement records both the operating corporate entity and the acquirer, because naming only one goes stale faster"
  - "A search-aggregator claim about a Force Management transaction was NOT recorded, because no primary source confirmed it"

patterns-established:
  - "Mutation probes for new self-test assertions run as siblings inside tools/ at the real REPO_ROOT depth, with an unmutated control, and assert on the failure message not just the exit code"

requirements-completed: [LEG-04]

coverage:
  - id: D1
    description: "All six SOURCES.md rows read verified, each carrying a distinct absolute https URL and an ISO-8601 retrieval date; the Out of bounds section is byte-identical to HEAD"
    requirement: LEG-04
    verification:
      - kind: other
        ref: "row-shape, date-validity/uniqueness and count assertions; diff of the Out of bounds section against HEAD reports IDENTICAL"
        status: pass
    human_judgment: false
  - id: D2
    description: "LEGAL-REVIEW.md exists with exactly one Gate status line and one Review date line, states it is not legal advice, and names the case, the registration number and both WINDOWS.md ids it disposes of"
    requirement: LEG-04
    verification:
      - kind: other
        ref: "single-match assertions on both frozen markers plus a required-literals check for 'not legal advice', 2:24-cv-01836, 6,489,058, WINDOWS.md id 3, WINDOWS.md id 6"
        status: pass
    human_judgment: false
  - id: D3
    description: "All three NOTICES.md statements carry the review date, keep all four labelled elements in order, retain both no-prediction sentences, and leave the attribution pointer untouched"
    requirement: LEG-04
    verification:
      - kind: other
        ref: "three-identical-dates assertion tied to LEGAL-REVIEW.md's review date; label counts 3/3/3/3; required-literals check; git diff on the pointer line reports POINTER_UNTOUCHED"
        status: pass
    human_judgment: false
  - id: D4
    description: "source-gate-incomplete fires on a PASSED gate over an incomplete list and on an unreadable or doubled gate line; is silent on OPEN, on a complete list, and when no review record exists"
    requirement: LEG-04
    verification:
      - kind: unit
        ref: "python3 tools/check_repo.py --self-test — six fixture roots, all directions asserted"
        status: pass
      - kind: integration
        ref: "sibling mutation probe with unmutated control: disabling the unverified branch turns the assertion red with the expected message"
        status: pass
    human_judgment: false
  - id: D5
    description: "framework-statement-stale-review fires per statement with no date, an unparseable date, or a date before the review date; is silent when dates are current and when no review record exists; two offenders are two distinguishable subjects in sorted order"
    requirement: LEG-04
    verification:
      - kind: unit
        ref: "python3 tools/check_repo.py --self-test — five fixture roots including the two-offender ordering and distinct-subject cases"
        status: pass
      - kind: integration
        ref: "sibling mutation probe with unmutated control: disabling the older-date branch turns the assertion red with the expected message"
        status: pass
    human_judgment: false
  - id: D6
    description: "Both new codes are discrimination-proven against the repository's own files, taking the harness from 50 to 52, and the whole ten-command CI gate stays green"
    verification:
      - kind: integration
        ref: "python3 tools/check_repo.py --mutation-test — 'mutation-test PASS: 52 codes discrimination-proven', CONTROL 0 violations, no FIRE-ONLY line; all ten CI commands exit 0"
        status: pass
    human_judgment: false
  - id: D7
    description: "Every invented party and person in both deal briefs was searched live and its collision outcome recorded — 9 parties and 10 persons, 1 party collision and 5 person collisions found"
    requirement: LEG-04
    verification:
      - kind: manual_procedural
        ref: "LEGAL-REVIEW.md § Name collisions — two tables, one row per name, enumerated from the files rather than from WINDOWS.md id 1's count"
        status: pass
    human_judgment: false
  - id: D8
    description: "Every recorded source says what its row claims; the reproduction-boundary reasoning for WINDOWS.md ids 3 and 6 is sound; no source wording entered any file or commit message; LEGAL-REVIEW.md does not read as legal advice"
    requirement: LEG-04
    verification: []
    human_judgment: true
    rationale: "All four are backstop truths in the plan's own must_haves. Whether a paraphrase crosses into reproduction, and whether a diligence record reads as the advice it disclaims, are exactly the semantic judgements SOURCES.md states no tool in this stack performs. A human read is the only thing that establishes them."

duration: 41 min
completed: 2026-09-21
status: complete
---

# Phase 6 Plan 02: Legal Review Gate Summary

**Six confirmed sources, three rights-holders reconfirmed against what actually changed, a dated diligence record, and two codes that make a declared pass and a re-dated statement mechanically un-fakeable — 52 codes discrimination-proven**

## Performance

- **Duration:** 41 min
- **Started:** 2026-09-21T09:34:12Z
- **Completed:** 2026-09-21T10:15:38Z
- **Tasks:** 3
- **Files modified:** 4 (1 created)

## Accomplishments

- **Every framework-derived concept now names a source that was fetched and read.** All six `SOURCES.md` rows carry a distinct absolute URL and the date it was retrieved. The two Challenger book rows were confirmed against bibliographic edition records whose `by_statement` matched each row's author list verbatim; the three vendor pages were each checked for a login or paywall before acceptance.
- **The register gap closed, and it closed in the direction nobody predicted.** The two USPTO endpoints that returned 503 and 403 during research were retried. The TSDR status view answered: Registration No. 6,489,058 is recorded **LIVE/REGISTRATION/Issued and Active** on a page TSDR itself stamped 2026-09-21 05:36:50 EDT, owner Lahoutifard Darius, most recent prosecution entry a Section 8 courtesy reminder dated 2026-09-21. A court directed cancellation on 2026-04-21; the register has not been amended. Both facts are recorded; the gap between them is not interpreted.
- **The docket is still live.** Re-queried today: `dateTerminated` is null and the most recent entry is 2026-09-14, "Response in Opposition to Motion". `NOTICES.md`'s existing refusal to predict an outcome was not a hedge to tidy up — it is the correct posture, and it survives verbatim.
- **Two reproduction-boundary questions closed with reasoning, not verdicts.** `WINDOWS.md` id 6 turned on a point worth stating plainly: the eight MC dimensions' order is not a source's chosen arrangement that this repository copied — it *is* the acronym, and reordering it would produce a different word rather than a rearranged list. The genericness ruling is engaged with and explicitly not over-read: it is a trademark holding about a term, not a copyright holding about an expression.
- **Nineteen names searched; six collisions found.** `Ardent Digital` is the exact name of a real trading company and the brief casts it as a displaced incumbent and losing bidder. `Gina Almeida` matches a real associate lawyer at an insurance group against a brief that casts her as Associate General Counsel at an insurance firm — name and role both. Four further person collisions are common-name coincidences in neutral roles.
- **The gate cannot lie now.** `source-gate-incomplete` refuses a declared pass over an unfinished list, and refuses an unreadable or doubled gate line too — deleting the marker is not a way around the check. `framework-statement-stale-review` ties every statement's date to the review record's date, so a bare date bump has nothing standing behind it.

## Task Commits

1. **Task 1: Confirm the five remaining source rows against live pages** — `90b5447` (docs)
2. **Task 2: Reconfirm the three rights-holders, and write the review record** — `6cc615a` (docs)
3. **Task 3: `source-gate-incomplete` and `framework-statement-stale-review`, both discrimination-proven** — `e2e4aa2` (feat)

## Files Created/Modified

- `LEGAL-REVIEW.md` *(new, 281 lines)* — `Review date: 2026-09-21`, `Gate status: PASSED`, a scope statement saying in plain words that this is a non-lawyer's diligence record and not legal advice, a dated section per framework, the source-row confirmations by reference, the id-3 and id-6 dispositions with their reasoning and their stated limits, two name-collision tables, the USPTO lookup results including the HTTP 401, and six open items.
- `SOURCES.md` — five rows `unverified` → `verified` with URL and retrieval date. `Last reviewed:` moved to 2026-09-21 only now that all six are done.
- `NOTICES.md` — Command of the Message rights-holder reconfirmed; MEDDIC-family statement gained one public-record paragraph naming case, docket, court, judge, filing date, ruling date, holding, registration number, registrant, the docket's un-terminated state and the register's observed state; Challenger statement names the operating entity and the acquirer and keeps its successor clause. All three re-dated. The attribution pointer block is byte-identical.
- `tools/check_repo.py` — `LEGAL_REVIEW_PATH`, the frozen gate constants, `_REVIEW_DATE_RE`, `FRAMEWORK_STATEMENT_HEADINGS`, `_LAST_REVIEWED_RE`, `_framework_section()`, `_review_date()`, `check_source_gate_incomplete()`, `check_framework_statement_stale_review()`; both codes appended to `SOURCES_CHECK_CODES` and dispatched from the existing `run_sources_checks()`; `'LEGAL-REVIEW.md'` in `MUTATION_SOURCES` with its reason; two `MUTATIONS` entries; eleven new self-test fixture roots with their assertions; both docstring entries with all declared ceilings.

## Decisions Made

- **The register observation is reported, not explained.** A court order directing cancellation and a register still showing the mark live are two separate facts. Writing a sentence reconciling them would be the repository taking a position in live litigation, which the plan forbids and which `NOTICES.md` has refused since 2026-09-10.
- **The genericness ruling was given exactly the weight it carries.** It establishes that the term is not a source identifier — useful, and the reason it appears in the id-6 reasoning at all. It establishes nothing about whether an expression of the methodology is protectable, because that is copyright and the ruling is trademark. A record that conflated the two would be worse than one that names the boundary it cannot cross.
- **A claim without a primary source was left out.** A search aggregator reported a 2021 corporate transaction involving Force Management. No primary source confirmed it, so it is recorded in `LEGAL-REVIEW.md` as explicitly not recorded as fact, and `NOTICES.md` names Force Management because that is what Force Management's own current pages show.
- **The gate check fires on an absent or doubled marker, not only on a false pass.** Silence there would make deleting the `Gate status:` line a way around the check.
- **`good_root` in the self-test deliberately ships no `LEGAL-REVIEW.md`.** Its `_good_notices()` statements carry no `Last reviewed:` line, and both new codes are specified to stay silent with no review record to compare against — so the absence is the fixture, not an omission. A comment in the file says so.
- **Open-source bibliographic catalogues over mark-holders' own sites for the book rows.** Continued from 06-01: stable, public, non-paywalled, and not selling training in the methodology being cited.

## Deviations from Plan

None - plan executed exactly as written.

Two adjustments were made inside the plan's own instructions, both committed with their task:

- `_bad_sources()` gained a fourth row reading `unverified`. `bad_root` must make every registered code fire, and `source-gate-incomplete` needs an incomplete list to fire over. The row is out of scope for `source-row-unconfirmed`, so that fixture's asserted count of three is unchanged, and the docstring records why the row is there.
- `_bad_notices()` gained the three framework headings with stale dates and *without* their required non-affiliation and rights-holder language. This lets `framework-statement-stale-review` fire on `bad_root` while `framework-statement-missing` keeps firing there too — one fixture, two defects, neither masking the other.

## Issues Encountered

**The mutation probe would not run outside the repository.** `REPO_ROOT` is `Path(__file__).resolve().parent.parent`, so a copy of `check_repo.py` placed in a scratch directory fails its own self-test for reasons unrelated to the mutation — the unmutated control failed first, which is exactly why a control was run. Re-running the probes as siblings inside `tools/` gave a green control and two reds with the expected messages; the probe files were removed afterwards and `git status` confirms only `check_repo.py` was left modified.

**A comment's parentheses broke an acceptance regex.** The plan's own `MUTATION_SOURCES` check uses `\(([^)]*)\)`, which stops at the first `)`. A comment added beside `'LEGAL-REVIEW.md'` was written without parentheses for that reason — the same correction 06-01 had already made for `'SOURCES.md'`.

**Google Books returned HTTP 429** on the book lookups, as it had in 06-01. Open Library answered every request and carried the subtitles and `by_statement` fields the rows needed.

## Measurements

| Metric | At HEAD (2026-09-21, pre-phase) | After 06-01 | After 06-02 |
|---|---|---|---|
| Codes discrimination-proven | 49 | 50 | **52** |
| `--mutation-test` wall time | 8.1 s | 9.6 s | **9.9 s** |
| `check_repo.py` lines | ~7,065 | 7,382 | 7,862 |

Wall time remains far under the 60-second remedy trigger 05-03 set. The growth is the copy cost of three more codes over a `MUTATION_SOURCES` set that now includes two more root files; it is not superlinear.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **LEG-04's gate is passed and mechanically defended.** `Gate status: PASSED` is true and, for the first time, checkable: it cannot be declared over an unfinished list, and the statements behind it cannot be re-dated without being re-read.
- **Carried to 06-04, which owns `.planning/WINDOWS.md`** (06-02's `files_modified` does not include it, and 06-04's prohibition states 06-02 closes ids 3 and 6 *on its recorded reasoning* while 06-04 writes every entry's disposition):
  - ids **3** and **6** are dispositioned in `LEGAL-REVIEW.md` and ready to close.
  - id **18** is discharged — the bench-brief collision search ran; its "no live network access" premise had expired.
  - id **1** should note that `examples/deal-brief.md`'s search re-ran and found a collision the original pass did not.
  - **Two new ledger entries are needed**: the `Ardent Digital` rename decision and the `Gina Almeida` rename decision, both open, both routed from `LEGAL-REVIEW.md` § Name collisions.
- **One recorded fact has a shelf life.** The register state for Reg. No. 6,489,058 was true on 2026-09-21 against an active docket. The next review re-reads it rather than carrying this one forward; `LEGAL-REVIEW.md` says so in its own open-items list.
- 06-03 is unblocked: it publishes what the benchmark supports and makes an unsourced claim a build failure, over a source list that is now complete.

---
*Phase: 06-legal-review-gate-launch*
*Completed: 2026-09-21*
