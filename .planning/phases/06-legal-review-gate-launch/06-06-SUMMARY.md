---
phase: 06-legal-review-gate-launch
plan: 06-06
subsystem: docs
tags: [readme, legal-review, reproduction-boundary, broken-windows, evidence-discipline, check-repo]

requires:
  - phase: 06-01
    provides: SOURCES.md rows verified and the LEG-04 source gate
  - phase: 06-02
    provides: LEGAL-REVIEW.md, its reproduction-boundary dispositions, and the name-collision searches that expired the no-network premise
  - phase: 06-03
    provides: README's claim region and the results-file pointers the corrections are checked against
  - phase: 06-04
    provides: the ledger sweep and the launch deferral
  - phase: 06-05
    provides: the round-1 corrections this round re-reads, and the two defects it introduced
provides:
  - README reconciled with the /config observation this project had already recorded
  - the "no benchmark has run" sentence corrected in the shipped skill and both derivatives
  - benchmark-run-claim-stale, a new check_repo.py code, discrimination-proven
  - the PF-1 counterweight corrected and WINDOWS id 29 re-read against the true facts
  - the expired no-network premise swept out of the tracked tree
  - LEGAL-REVIEW.md's append-only rule reconciled with the file's own history
  - "`## Human observations` section 5, recording round 2"
  - three backlog items filed in WINDOWS.md rather than dropped
affects: [launch, publication, installed users of the skill, any later review reading LEGAL-REVIEW.md]

actuals:
  tokens: 31000
  tasks: 12
  commits: 13

tech-stack:
  added: []
  patterns:
    - "A stale-claim guard is one code per literal with its own mutation, not one code matching several literals — a folded-in literal is registered but never independently discrimination-proven"

key-files:
  created: []
  modified:
    - README.md
    - LEGAL-REVIEW.md
    - skills/proof-first/references/artifact-patterns.md
    - output-styles/proof-first.md
    - prompts/system-prompt.md
    - tools/check_repo.py
    - evals/benchmark/bench-deal-brief.md
    - evals/proxy-sources.md
    - .planning/WINDOWS.md

key-decisions:
  - "Task 3: the widened guard is a sibling code (benchmark-run-claim-stale), not a second literal folded into check_derivative_comparison_claim as the plan's letter said. The mutation harness maps one code to one mutation, so a folded-in literal would be registered but never discrimination-proven — this repository's own named recurring defect (WINDOWS id 10). Deviation recorded in the commit."
  - "Task 3: the new code matches case-insensitively and scans the skill sources as well as the derivatives, unlike its sibling. The sentence is hand-written prose rather than generator output, and the real defect took the source path, which a derivative-only scan cannot see until the next regeneration."
  - "Task 6: the second of the plan's two permitted outcomes was taken. The mutation probe against an unmutated sibling control confirmed README's 31 and 28 can be changed to 37 and 44 with check_repo.py still at 0 violations, so the README sentence stopped claiming enforcement rather than a new code being added."
  - "Task 7: option 1 of two — carry every arm's activation figure (9/12, 11/12, 8/12) rather than drop the measurement, and state what MARKER_RE.search can and cannot separate."
  - "Task 8: the plan said a fourth occurrence should trigger a repo-wide sweep. Two more were found, so the sweep was done rather than the one file fixed."
  - "Task 9: WINDOWS id 29 stays open, but on different footing. The first of its two deciding questions is answered by the files rather than by a judgement, and the remedy priced at one file costs three plus a regeneration — a change to shipped content, so a version decision."
  - "Task 11: the append-only rule was restated (option 1) rather than the superseded text restored (option 2). The distinction encoded: a record of what was and was not done is evidence and is preserved, as `## Human observations` sections 1 to 3 were; a reading that was simply wrong about a file in this repository is not."
  - "Task 12: the three backlog items were filed as WINDOWS entries 30, 31 and 32 rather than mentioned in prose, so they carry closure conditions and appear in open_count."
  - "Self-audit: the round re-read its own added sentences and found two more checkably-false statements, one of its own making. Both corrected in a thirteenth commit rather than left for round 3."

patterns-established:
  - "Gap-closure rounds re-read the sentences they added, not only the ones they fixed. 06-05 introduced two defects this way; this round introduced one and caught it before shipping."
  - "\"Repo-wide\" claims are checked against the full tracked tree, including .planning/, or scoped explicitly to the shipped tree."
  - "A ledger row whose recorded justification turns out false is re-dispositioned visibly — the entry states whether its status changed and why — rather than having the fact corrected underneath an unchanged reason."

requirements-completed: []
---

# 06-06 — Gap closure for Phase 6 UAT, round 2

## What this round was

`/gsd-verify-work 06` round 2 gave three questions to five independent headless readers, none of
whom had written the text they read. Two of the three returned fourteen checkably-false statements —
six in `LEGAL-REVIEW.md`, eight in `README.md` — every one re-verified against a committed file
before being recorded. The third question, the opinion register, passed on its own criterion.

All twelve tasks are complete. Every correction was checked against the file named beside it in the
plan.

## The three findings that mattered most

**One shipped to installed users.** `skills/proof-first/references/artifact-patterns.md` stated "no
benchmark has run" while `evals/benchmark/RESULTS.md` records 96 generations measured 2026-09-18.
The sentence was carried verbatim into `output-styles/proof-first.md` and `prompts/system-prompt.md`
by the generator, so it reached every install route. The point it was making — that the
artifact-family table is not evidence a convention wins deals — is kept; the false premise is
replaced by what the benchmark does and does not establish.

**One was created by the round sent to fix defects.** 06-05 wrote the `/config` observation into
`LEGAL-REVIEW.md` and left `README.md` asserting the picker "has not been observed here". Two
committed files said opposite things about the same observation.

**One was the round-1 defect reintroduced in the paragraph rewritten to remove it.** G-06-6's first
finding was README claiming enforcement machinery it does not have; 06-05's replacement paragraph
named `catalog-count-mismatch` as checking README's inventory counts, which it does not — it reads
`SKILL.md` against `NUMBERING.md` and never opens README.

## The one place a mechanical gate was the right answer

Thirteen of the fourteen were left to reading, for the reason `WINDOWS.md` id 17 records: the defect
class is entailment between two independently-phrased passages, which pattern matching over one file
cannot perform. The fourteenth was a fixed string whose sibling literal already had a guard, so it
got a code.

`benchmark-run-claim-stale` was added to `tools/check_repo.py` with its own self-test fixtures and
its own mutation. It differs from its sibling in two deliberate ways, both because the sentence is
hand-written prose rather than generator output: it matches case-insensitively, and it scans the
skill sources as well as the derivatives. `--mutation-test` reports **57 codes discrimination-proven**,
up from 56.

The plan asked for the literal to be added to the existing `STALE_COMPARISON_CLAIM` check. It is a
sibling code instead. The mutation harness maps one code to one mutation, so a second literal folded
into the existing code would have been registered but never independently discrimination-proven —
which is this repository's own named recurring defect, `WINDOWS.md` id 10.

## The self-audit, and what it caught

The round re-read the sentences it had added rather than only the ones it had fixed. Two statements
did not survive.

One was written by this round: Task 10 replaced a false claim about where "Economic Buyer" and
"Paper Process" sit with "repo-wide the two appear only in `NUMBERING.md`, in this file, and in
`check_repo.py`'s fixtures". `.planning/` is tracked — 178 files — and both strings appear across it.
Scoped to the shipped tree, with `.planning/` named rather than quietly excluded.

The second is pre-existing and was surfaced by checking the first. The ledger section said the
register "lives under `.planning/`, which a reader of this repository cannot see". A reader can: it
is tracked, and README cites `.planning/WINDOWS.md` by entry number in two places.

Both are corrected in the round's thirteenth commit.

## CI

All ten commands from `.github/workflows/ci.yml`, run after the final commit:

| Command | Result |
|---|---|
| `check_repo.py --self-test` | PASS |
| `check_repo.py --mutation-test` | PASS — 57 codes discrimination-proven, control clean |
| `check_repo.py` | 0 violations |
| `run_conformance.py --self-test` | PASS |
| `lint.py --self-test` | PASS |
| `run_benchmark.py --self-test` | PASS |
| `run_routes.py --self-test` | PASS |
| `run_trigger_test.py --self-test` | PASS |
| `stats.py --self-test` | PASS |
| `generate_derivatives.py --check` | PASS |

This is the fifth consecutive round in which all ten were green while checkably-false statements sat
in the tree, which is `WINDOWS.md` id 17's thesis and the argument against a fuzzy-proxy gate rather
than for one.

## Ledger

`WINDOWS.md`'s JSON fence was edited as the source of truth and the markdown table re-rendered from
it; every rendered row round-trips against the JSON and `gsd-tools windows status` parses the result.
Counts: **12 open, 9 waived, 11 fixed, 32 total.**

Ids 12, 17 and 29 were re-dispositioned. Three new entries were filed rather than dropped:

- **30** — README's "drafted twice" omitting the 3 repeats. Not a falsehood, but two consecutive
  rounds of cold readers tripped on it.
- **31** — the reasoning critiques of the id-6 prong answers, which are argument-quality judgements
  rather than checkable falsehoods.
- **32** — `evals/proxy-sources.md`'s two source rows, the last provenance in the repository resting
  on the expired no-network premise. Restated in the past tense by this round; re-fetching was out of
  scope.

## Out of scope, as the plan specified

The PF-1 sub-block rename and the two conceded MC labels (the decision belongs to whoever owns
`WINDOWS.md` ids 29 and 6); a new checker code for README's inventory counts; reopening test 8; and
re-measuring anything — no figure in this round was found wrong.
