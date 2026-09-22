---
phase: 06-legal-review-gate-launch
plan: 06-07
title: Close the round-3 UAT gaps
gap_closure: true
gap_ids: [G-06-10, G-06-11, G-06-12]
completed: 2026-09-22
tasks_completed: 13
executor: inline (orchestrator) — the gsd-executor subagent was not dispatched
---

# 06-07 — Gap closure for Phase 6 UAT, round 3

All thirteen tasks done. Eleven checkably-false statements corrected across six files, plus two more
this round's own self-audit caught in text it had just written.

## What changed, by gap

### G-06-10 — `LEGAL-REVIEW.md`'s reproduction-boundary material (7 findings)

**Task 1 was a decision, not an edit.** The file classified six of the eight MC dimension names as
ordinary business English; `tools/check_repo.py`'s frozen `SOURCE_COINED_LABELS` (03-07 GAP B)
classifies seven of the eight as source-coined and fails the build when any reaches shipped skill
content, excluding only `metric`. Both were this repository's considered positions on the same eight
strings, and they were opposites. **The review now adopts the checker's**, because the checker's
violation string names `SOURCES.md`'s reproduction-boundary clause and answers the same question
prong 4 asks; its scope carve-out is about where it enforces, not about which terms are coined.

The prong-4 concession therefore widens from two labels to seven. The disposition does not move, and
the entry now says why rather than leaving a reader to notice: the closure never rested on the count,
it rested on position — no shipped skill content, `NOTICES.md` carries the attribution, no rule text
taken — and all three hold for all seven, the first now mechanically rather than by observation.
What the widening does change is the price of the stricter reading, which is recorded.

The other six (tasks 2-7): the occurrence enumeration corrected against `git grep -in` (both labels
are headings in both deal briefs; `check_repo.py`:2958-2959 is a production constant, not a fixture);
the mnemonic removed from prong 2 and from the PF-1 comparison, since the correction fifteen lines
above had retired it; `NUMBERING.md` corrected to declare the element correspondence and not the
order; the rename cost settled at four files; "ships" reduced to `README.md`'s single published
sense; and prong 2's "shortest ordinary English" premise removed as refuted by prong 4's own finding.

**One correction went further than the plan required, and it weakens the entry.** Prong 2's sentence
also carried "the order a methodology is conventionally walked through by many independent
publishers" — a premise recorded in no committed file, which round 3 filed as backlog. It sat inside
a sentence tasks 3 and 7 had to rewrite anyway, and leaving a known-unrecorded premise in a sentence
being rewritten is how the last two rounds created their own findings. It is gone. Prong 2 now rests
on the thinness test alone, which `SOURCES.md` does not contain — ledger row 31 already said so and
now carries the whole of that prong. This makes the entry's weaker half weaker, which is the honest
outcome rather than a reason to have kept the clause.

### G-06-11 — the shared deal-brief figure (1 finding)

**Outcome 2, and outcome 1 was rejected on evidence rather than cost.** The plan permitted varying
the bench brief's `rfp-security-weight` so the claim would become true. It would not have: 20%
carries four distinct meanings inside `bench-deal-brief.md` alone (Q3 weight, security posture,
`rfp-question-weight-mid`, `rfp-security-weight`) and three inside `examples/deal-brief.md`, so bare
values were always going to coincide across differently keyed rows. Varying one row would have left
the claim false while looking fixed.

So the claim is bounded to what holds, in both files in the same commit, and the identical row is
named rather than hidden behind the bound. The separation that actually protects the benchmark — no
shared company, person or platform, so no session can draw on the other deal — was verified to hold
with zero overlap across all nine invented names and both platform lists.

**And it is now mechanically held.** `run_benchmark.py`'s `shared_deal_brief_entities` asserted
disjointness over four of the nine invented names; README now states the assertion covers every
invented name, so the tuple was widened to all nine. Discrimination-proven against an unmutated
control: a copy of the tree with "Gina Almeida" appended to the bench brief fails with
`FAIL: bench-deal-brief.md reuses shared-deal-brief entities: ['Gina Almeida']`, a name the old tuple
could not see; the unmutated tree passes. This also closes round 3's 2-to-1 reader split on
`README.md`:186-188, which was backlog.

### G-06-12 — three contradictions no earlier brief could reach (3 findings)

`evals/lint.py`'s ceiling for `proxy-term-source-is-internal` no longer asserts the expired
no-network premise. It was restated as the property that actually holds — the linter never fetches or
resolves a URL, by design and regardless of the environment — rather than put in the past tense,
because a ceiling that depends on an environment fact expires again. `git grep` for the premise now
returns only the three files that state it as expired. Ledger row 28 corrected from four named limits
to six. `run_conformance.py`'s docstring corrected from three committed fixtures to five, naming the
two `-late-phrase` files its own cases 8 and 9 already described.

## Task 13 — the ledger, done last and in the stated order

`WINDOWS.md`'s JSON fence was edited and the whole 32-row table re-rendered from it programmatically,
rather than the three touched rows being hand-edited. Verified with an escape-aware parser (the naive
`split('|')` check reported a false mismatch on id 14, whose description contains an escaped pipe):
32 rows, 32 entries, zero field mismatches, and computed counts 12 open / 9 waived / 11 fixed / 32
total agreeing with the frontmatter. `gsd-tools windows status` parses it, so the table is still
machine-readable.

`LEGAL-REVIEW.md`'s reproduced ledger was then reconciled row by row against `WINDOWS.md`: 32 rows,
no disposition mismatches, and its stated counts (9 fixed, 2 closed on reasoning, 9 waived, 12 open)
reconcile with WINDOWS's 11 fixed once the two `closed on reasoning` rows are folded in, exactly as
the file says. Entries 6, 12 and 17 gained this round's reasons; no status and no count changed.

## Task 12 — the brief set, and this round's own self-audit

The four-brief standing set is recorded in `06-UAT.md`: README, `LEGAL-REVIEW.md`, the whole-tree
sweep, and — new — one pointed at whatever the last gap-closure round rewrote. That fourth brief is
proposed because four of round 3's eleven findings and two of round 2's fourteen were authored by the
round that was closing the previous one, and no brief has ever been aimed at that surface.

**Part B found two defects in sentences this round had just written**, which is the point of doing it:

- A code comment in `run_benchmark.py` cited `examples/deal-brief.md`'s four parties as ":14-16, :22".
  Line 22 is estate prose; the parties are at :13-16. Corrected to a heading-anchored citation.
- `bench-deal-brief.md` gained "no figure was copied across" — not something this review can
  establish, and in tension with the identical row it concedes two sentences earlier. Replaced with
  the checkable statement.

A third was caught by the same pass: `LEGAL-REVIEW.md` cited `README.md`:367-369 for the shipping
definition, which is at :369-371 — the citation was written against line numbers this round's own
README edit had already shifted. Corrected, and the five deal-brief citations were converted from
line numbers to heading anchors for the same reason, since both briefs are edited more often than
this record is re-read.

The absolutes audit ran over every added line and each was checked against the full tracked tree
including `.planning/`:

```
"No shipped skill file carries any of the seven"  -> 0 hits across skills/, output-styles/, prompts/
"All seven appear throughout .planning/"          -> 21-45 files each
every added `file.md:N` citation                  -> 12 of 12 resolve in the current tree
```

## Verification

All ten CI commands green:

```
check_repo.py --self-test              PASS (57 codes)
check_repo.py --mutation-test          PASS (57 codes discrimination-proven)
check_repo.py                          0 violations
run_conformance.py --self-test         rc=0
lint.py --self-test                    rc=0
run_benchmark.py --self-test           rc=0  (entity assertion now over 9 names)
run_routes.py --self-test              rc=0
run_trigger_test.py --self-test        rc=0
stats.py --self-test                   rc=0
generate_derivatives.py --check        rc=0
```

Green CI remains necessary and not sufficient: it was green through all eleven of round 3's findings.
One of them — the classification conflict between `LEGAL-REVIEW.md` and `check_repo.py` — could not
have been caught by any string gate, because both files were internally consistent and only
disagreed with each other. That is recorded on `WINDOWS.md` id 17.

No `SKILL.md` or reference file changed, so no derivative regeneration was needed and none happened.

## What this plan does not establish

The corrections were written and checked by the same session. Every previous round's self-check
missed what an independent reader then found, three times running. The closure condition is
unchanged: `/gsd-verify-work 06` for round 4, with the four briefs now recorded.
