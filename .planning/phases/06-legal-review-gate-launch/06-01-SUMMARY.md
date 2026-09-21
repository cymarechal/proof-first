---
phase: 06-legal-review-gate-launch
plan: 01
subsystem: testing
tags: [check_repo, mutation-testing, provenance, legal, stdlib-python]

requires:
  - phase: 02-skill-and-linter
    provides: "tools/check_repo.py, its ALL_CHECK_CODES/MUTATIONS registration pattern, and the split_sections()/table_rows() Markdown table helpers this check reuses"
  - phase: 03-examples-and-conformance
    provides: "the MUTATION_SOURCES widening precedent set by 03-14 for 'evals', copied here for 'SOURCES.md'"
provides:
  - "One confirmed SOURCES.md row: the Andy Whyte MEDDICC book, carrying an absolute https URL and an ISO-8601 retrieval date"
  - "source-row-unconfirmed — the first check that reads SOURCES.md at all, making a verified-but-unsourced row a build failure"
  - "'SOURCES.md' in MUTATION_SOURCES, so the mutation harness can reach the real approved-source list"
affects: [06-02, 06-03, 06-04, legal review gate, LEG-04]

actuals:
  tokens: 11000
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns:
    - "Provenance-as-build-gate: a Markdown status cell claiming confirmation must name what was read and when, or CI fails"

key-files:
  created: []
  modified:
    - SOURCES.md
    - tools/check_repo.py

key-decisions:
  - "Confirmed against openlibrary.org — a public, non-paywalled bibliographic catalogue — rather than the mark-holder's own site, which sells training and sits nearer SOURCES.md's Out of bounds list"
  - "The check performs no network call, by design and by declared ceiling, so CI never depends on a third party's uptime"
  - "A malformed row fires rather than being skipped, because a row that lost its Status column would otherwise read as out of scope"
  - "unverified rows are out of scope entirely — firing on them would make the pre-review state a build failure and collapse the tracer into 06-02"

patterns-established:
  - "Two declared ceilings in the docstring beside the code entry: no fetch, no semantic judgement — the file's existing convention for stating what a check cannot do"
  - "Widening MUTATION_SOURCES carries a comment naming why, and a matching note in _copy_repo_subset()'s docstring"

requirements-completed: [LEG-04]

coverage:
  - id: D1
    description: "The Andy Whyte MEDDICC book row in SOURCES.md reads `verified` and carries https://openlibrary.org/books/OL38629171M plus the retrieval date 2026-09-21; the other five rows are untouched and still read `unverified`"
    requirement: LEG-04
    verification:
      - kind: other
        ref: "python3 -c \"...\" — row matches '| verified | https://... (retrieved YYYY-MM-DD) |'; unverified count 5; to-confirm count 5; git diff --numstat shows exactly 1 1"
        status: pass
    human_judgment: false
  - id: D2
    description: "source-row-unconfirmed fires on a verified row missing a URL, missing a valid retrieval date, or carrying a well-shaped impossible date; fires on a row whose cell count is wrong; is silent on unverified rows and on an absent SOURCES.md"
    requirement: LEG-04
    verification:
      - kind: unit
        ref: "python3 tools/check_repo.py --self-test — names source-row-unconfirmed among verified codes"
        status: pass
    human_judgment: false
  - id: D3
    description: "source-row-unconfirmed is discrimination-proven against this repository's own SOURCES.md, not merely registered: silent on the unmutated copy, firing on a mutated one"
    requirement: LEG-04
    verification:
      - kind: integration
        ref: "python3 tools/check_repo.py --mutation-test — 'mutation-test PASS: 50 codes discrimination-proven', CONTROL 0 violations, no FIRE-ONLY line for this code"
        status: pass
    human_judgment: false
  - id: D4
    description: "The whole repository gate stays green: check_repo reports 0 violations and all ten commands .github/workflows/ci.yml declares exit zero"
    verification:
      - kind: integration
        ref: "each of the ten CI commands run in sequence — all exit 0"
        status: pass
    human_judgment: false
  - id: D5
    description: "The confirming page is a public, non-paywalled source of the kind SOURCES.md's Out of bounds section permits, and no wording from it entered SOURCES.md, tools/check_repo.py, or either commit message"
    requirement: LEG-04
    verification: []
    human_judgment: true
    rationale: "Both are backstop truths in the plan's own must_haves. Whether a catalogue record is in bounds, and whether a citation stopped short of reproduction, are the semantic judgements SOURCES.md itself states no tool in this stack performs. 06-02's legal review record is the named owner."

duration: 22 min
completed: 2026-09-21
status: complete
---

# Phase 6 Plan 01: Source Provenance Tracer Summary

**`source-row-unconfirmed` — the first check that reads `SOURCES.md` at all — plus one row confirmed against a public catalogue record, taking the mutation harness from 49 to 50 discrimination-proven codes**

## Performance

- **Duration:** 22 min
- **Started:** 2026-09-21T09:09:41Z
- **Completed:** 2026-09-21T09:31:43Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- The approved-source rule has teeth for the first time. `SOURCES.md` has stated since 2026-09-10 that a concept with no listed source does not ship; before this plan no check read the file, it was absent from `MUTATION_SOURCES`, and a row could have been flipped to `verified` with an empty `Where` cell without any of ten CI commands noticing.
- One row now names what was read and when: the Andy Whyte MEDDICC book, confirmed against `https://openlibrary.org/books/OL38629171M`, retrieved 2026-09-21. The Open Library edition record carries the full title including its subtitle, the author, publisher Nielsen, publish date 2020-11-25 and ISBN 9781838239701 — all matching the row.
- `source-row-unconfirmed` is discrimination-proven against the repository's own file, not only against a fixture: the mutation strips the confirmed row's `Where` cell back to its pre-confirmation placeholder while leaving the status reading `verified`, which is the real defect — a row hand-edited to claim provenance nobody recorded.
- The five remaining rows still say plainly that they have not been confirmed. That is 06-02's work, over a mechanism this plan has now proven end to end.

## Task Commits

1. **Task 1: One source row, confirmed against a live page and recorded with provenance** — `e051616` (docs)
2. **Task 2: `source-row-unconfirmed` — the check, its mutation, and green CI** — `c0fca5f` (feat)

## Files Created/Modified

- `SOURCES.md` — one row's `Status` cell `unverified` → `verified` and its `Where` cell `to confirm at LEG-04` → `https://openlibrary.org/books/OL38629171M (retrieved 2026-09-21)`. Exactly one line changed; the `Last reviewed:` date is deliberately untouched, since re-dating the file would claim a review that has not happened yet.
- `tools/check_repo.py` — `SOURCES_PATH`, `SOURCES_TABLE_HEADINGS`, `SOURCES_ROW_CELLS`, `_SOURCES_RETRIEVED_RE`, `check_source_row_unconfirmed()`, `SOURCES_CHECK_CODES`, `run_sources_checks()`; registration in `ALL_CHECK_CODES` and `run_all_checks()`; `'SOURCES.md'` appended to `MUTATION_SOURCES` with a comment naming why and a matching note in `_copy_repo_subset()`'s docstring; `_mutate_source_row_unconfirmed()` and its `MUTATIONS` entry; five self-test fixture builders and their assertions; a `datetime` import; and the docstring code-list entry stating both declared ceilings.

## Decisions Made

- **Open Library over the mark-holder's own site.** `SOURCES.md`'s Out of bounds list rules out vendor training-portal content and paid course material. A bibliographic catalogue record run by the Internet Archive is none of those, is stable, and is not selling anything — a cleaner confirmation than a page belonging to a party that also sells certification in the same methodology.
- **The subtitle drove the source choice.** Open Library's *work* record carries only `MEDDICC`; its *edition* record `OL38629171M` carries the full subtitle, so the edition URL is what was recorded. The Google Books API, tried first, returned HTTP 429 from this network.
- **A prefix test, not a URL regex.** What counts as a well-formed URL is an argument this check does not need to have; `https://` on a whitespace-delimited token cannot be satisfied by prose, which is the actual failure mode.
- **The date is validated, not just matched.** `(retrieved 2026-13-45)` matches the shape and is not a date, so `datetime.date.fromisoformat` runs on the captured group.
- **Violations sort on their own message.** Every violation from this check shares one subject, so the live run's `(code, subject)` sort cannot order them; sorting on the message makes two offending rows report in a fixed order regardless of how the tables were written.

## Deviations from Plan

None - plan executed exactly as written.

Two self-inflicted corrections were made and fixed before the task commit, neither of them a deviation from the plan:

- The comment added beside `'SOURCES.md'` in `MUTATION_SOURCES` originally contained parentheses, which broke the plan's own acceptance regex `MUTATION_SOURCES = \(([^)]*)\)`. Reworded to carry the same fact without them.
- `good_root` in the self-test needed its own clean `SOURCES.md` so the final every-code-fires-on-bad / silent-on-good loop covers the new code; the absent-file direction is therefore asserted against `results_good_root`, which ships no sources file. A comment saying otherwise was corrected in the same edit.

## Issues Encountered

The Google Books API returned HTTP 429 (rate limited) from this network on two attempts, once through the fetch tool and once through `curl`. Recorded rather than retried around: Open Library answered on the first request and is the better source anyway. No lookup failure affected the recorded row — the URL committed is one that was fetched and read in this execution, and the page's title and author were confirmed against the row before the edit.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The LEG-04 vertical is proven on one row: a real lookup, a committed provenance record, a registered check, a mutation that discriminates against the real file, and a green ten-command gate.
- 06-02 expands over this mechanism — five remaining rows plus the three rights-holder statements — and adds the completeness half, `source-gate-incomplete`, which needs the review record to exist before it can fire.
- The `Where` cell format is now frozen and enforced: one absolute `https://` URL, then ` (retrieved YYYY-MM-DD)`, nothing else.
- `SOURCES.md`'s `Last reviewed:` line still reads 2026-09-10 and must be re-dated by 06-02, not before.

---
*Phase: 06-legal-review-gate-launch*
*Completed: 2026-09-21*
