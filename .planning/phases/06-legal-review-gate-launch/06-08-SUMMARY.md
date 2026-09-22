---
phase: 06-legal-review-gate-launch
plan: 06-08
title: Close the round-4 UAT gaps, and measure whether a citation gate was worth shipping
gap_closure: true
gap_ids: [G-06-13, G-06-14, G-06-15, G-06-16]
completed: 2026-09-22
tasks_completed: 17
executor: inline (orchestrator) — the gsd-executor subagent was not dispatched
subsystem: testing
tags: [check_repo, generate_derivatives, run_benchmark, legal-review, windows-ledger]

requires:
  - phase: 06-legal-review-gate-launch
    provides: rounds 1-3 gap closures (06-05, 06-06, 06-07) and the round-4 UAT findings
provides:
  - All seventeen round-4 checkably-false statements corrected across seven files
  - The one user-facing finding fixed and both derivatives regenerated
  - Two new mechanical assertions — caveat-count-matches-constant, no-platform-collision
  - A new check code, record-citation-unresolvable, shipped with a measurement that bounds it
  - A measured verdict that the citation class the plan targeted is NOT mechanically catchable
affects: [round-5 UAT, any future gap-closure round, WINDOWS ids 12 and 17]

actuals:
  tokens: 21500
  tasks: 17
  commits: 15

tech-stack:
  added: []
  patterns:
    - "Symbol anchors instead of line citations in Python files — a named constant does not drift"
    - "Measurement pinned to its commit, not restated as a live count"
    - "New check codes ship with a history replay that bounds their value, not a claim about it"

key-files:
  created: []
  modified:
    - tools/generate_derivatives.py
    - tools/check_repo.py
    - evals/benchmark/run_benchmark.py
    - evals/benchmark/bench-deal-brief.md
    - LEGAL-REVIEW.md
    - README.md
    - output-styles/proof-first.md
    - prompts/system-prompt.md
    - .planning/WINDOWS.md

key-decisions:
  - "Shipped record-citation-unresolvable despite measuring that it catches none of the findings it was scoped to catch — it meets the repository's bar for a new code, and its docstring states the zero-firing measurement so it cannot be cited as a guard over citation accuracy"
  - "Added the platform assertion rather than splitting the sentence (task 12's stated preference), proven with a mutation probe and an unmutated control"
  - "Removed the 20% meaning-count entirely rather than restating it — a count of meanings is not checkable by any command"
  - "Removed the correction tally from LEGAL-REVIEW.md rather than updating it, per task 5's preferred outcome"
  - "Did not reopen WINDOWS id 6; fixed the Closed-on-reasoning wording instead, because reopening would assert the disposition question is unanswered, which is false"
  - "Anchored LEGAL-REVIEW.md's check_repo.py citations to named symbols, refuting the plan's assumption that line numbers are the only practical anchor in a Python file"
  - "Enforcement-scope checking is mechanizable (this round did it by hand with a tracer) but is recorded as a candidate rather than shipped — it needs the checker to run itself under instrumentation at build time"

patterns-established:
  - "Pattern: a count stated in prose next to the thing it counts gets an assertion against len(), never a literal"
  - "Pattern: cite a Markdown file by heading and quoted string, a Python file by symbol name; reserve line numbers for neither"
  - "Pattern: a self-referential grep is not provenance — scope the command or drop the count"

requirements-completed: []

coverage:
  - id: D1
    description: "Both derivatives' omission notice names where MC constructive lines actually live; nothing normative is claimed to be in SKILL.md that a build gate forbids there"
    requirement: "LEG-05"
    verification:
      - kind: automated_ui
        ref: "python3 tools/generate_derivatives.py --check"
        status: pass
      - kind: unit
        ref: "grep -c 'Replace with:' on each derivative == 39 (31 PF + 8 MC)"
        status: pass
    human_judgment: false
  - id: D2
    description: "bench-deal-brief.md's platform disjointness is mechanically asserted, not observed"
    verification:
      - kind: unit
        ref: "evals/benchmark/run_benchmark.py --self-test#no-platform-collision"
        status: pass
      - kind: unit
        ref: "mutation probe: appending 'Amazon EC2' to the brief fails; unmutated control passes"
        status: pass
    human_judgment: false
  - id: D3
    description: "The EVAL-10 caveat count cannot drift from REQUIRED_CAVEATS"
    verification:
      - kind: unit
        ref: "evals/benchmark/run_benchmark.py --self-test#caveat-count-matches-constant"
        status: pass
      - kind: unit
        ref: "mutation probe: renderer emitting a seventh bullet fails with the assertion's own message"
        status: pass
    human_judgment: false
  - id: D4
    description: "record-citation-unresolvable validates path:N citations in LEGAL-REVIEW.md and README.md"
    verification:
      - kind: unit
        ref: "tools/check_repo.py --self-test (six directions: clean, overrun, missing, inverted, backtick-less, .planning-only)"
        status: pass
      - kind: unit
        ref: "tools/check_repo.py --mutation-test#record-citation-unresolvable (58 codes discrimination-proven)"
        status: pass
    human_judgment: false
  - id: D5
    description: "README.md's checker bullet states the 23-file surface it actually reads instead of 'enforcing all of the above'"
    requirement: "LEG-05"
    verification:
      - kind: other
        ref: "instrumented pathlib.Path.read_text/read_bytes/open over a live check_repo.py run; 11 claimed-unopened files confirmed absent, 17 claimed-opened confirmed present"
        status: pass
    human_judgment: true
    rationale: "The measurement is reproducible but is not wired into CI — mechanizing it needs the checker to execute itself under a tracer at build time, recorded as a candidate in WINDOWS id 17"
  - id: D6
    description: "LEGAL-REVIEW.md's thirteen corrected statements and four answered reasoning critiques"
    requirement: "LEG-04"
    verification: []
    human_judgment: true
    rationale: "Every correction is a prose claim about another committed file. Only a cold reader who did not write them can confirm they hold — the closure condition WINDOWS id 12 states and four rounds have not met"
  - id: D7
    description: "WINDOWS ids 12 and 17 record round 4; LEGAL-REVIEW.md's reproduced ledger resynced"
    verification:
      - kind: other
        ref: "gsd-tools windows status parses; rendered table == JSON across all 32 rows; reproduction reconciled row-for-row by escape-aware parser"
        status: pass
    human_judgment: false

duration: 95min
completed: 2026-09-22
status: complete
---

# 06-08 — Gap closure for Phase 6 UAT, round 4

**All seventeen tasks done. Seventeen checkably-false statements corrected across seven files, two
new mechanical assertions added, and one new check code shipped with a measurement proving it would
have caught none of the findings it was designed for.**

## The one finding that reached a user

`generate_derivatives.py` wrote into both shipped derivatives that every rule `worked-examples.md`
illustrates "already carries its own constructive line in `skills/proof-first/SKILL.md`". Eight of
the twenty-eight are MC rules, and `mc-rule-in-skill` makes an MC rule defined in `SKILL.md` a build
failure — so the claim was not merely wrong, it was forbidden from ever being true.

The honest form was available and no weaker: 20 PF rules in `SKILL.md`, 8 MC rules in
`completeness-audit.md`, both already concatenated sources. Corrected, regenerated, all three files
in one commit (`f909d3c`). Each derivative carries 39 constructive lines — 31 PF + 8 MC.

## Task 17, and why its premise was wrong

The plan's centrepiece was a citation-resolution gate, scoped "to the narrowest thing that would
have caught round 4's findings 2, 4, 5 and 9 and round 3's `:268` finding", and its intended ceiling
paragraph asserted it "would have caught the `README.md`:367-369 slip and the `NUMBERING.md`:26-40
slip".

It was built, it passes, and it discriminates: six self-test directions, a mutation entry firing
against the real record's own first line-range citation, 58 codes discrimination-proven. Then it was
replayed over the whole history, which is what the plan should have asked for before specifying the
ceiling:

| replay over the full history, measured at 06-08 | |
|---|---|
| commits examined | 435 |
| citation-instances examined | 164 |
| distinct citation spellings ever written | 14 |
| commits carrying at least one | 37 |
| **times the code fires** | **0** |

Zero. Every citation finding four rounds of cold reads produced was a line number that *existed* and
pointed at the wrong content — including both slips the plan named. The gate catches a path that
names no file, a range past end-of-file, and an inverted range. This repository has produced none of
those in 435 commits.

It shipped anyway, because it meets the repository's own bar for a new code and is cheap future
insurance — but its docstring carries the zero-firing measurement and forbids citing it as a guard
over citation accuracy. Shipping it silently would have manufactured exactly the finding class tasks
1 and 8 exist to correct: a sentence claiming more coverage than a check's scope has.

**Then it demonstrated its own ceiling, in the same commit.** The 36-line docstring entry it added
shifted every line below it and broke five `LEGAL-REVIEW.md` citations into `check_repo.py`; task 8's
README edit had already broken a sixth twelve lines earlier. The new code was silent on all six,
because every cited line still existed. All six are now anchored to headings, quoted strings, or
named symbols — which refutes the plan's assumption that line numbers are the only practical anchor
in a Python file.

## Where a mechanical check *was* worth it

Two of round 4's three finding classes got code rather than prose.

**The caveat count** (`cfff672`). `run_benchmark.py` said "the five caveats EVAL-10 requires" in a
comment sitting directly above a six-element `REQUIRED_CAVEATS`. Corrected to carry no tally at all,
and `caveat-count-matches-constant` now asserts the rendered bullet count against
`len(REQUIRED_CAVEATS)`. The pre-existing per-caveat guard proved every required key *reaches* the
section; it could not see a seventh bullet emitted from somewhere else. Mutation probe: a sibling
copy whose renderer emits one extra hardcoded bullet fails with `emitted 7 caveat bullet(s),
expected len(REQUIRED_CAVEATS)=6`; the unmutated control copy passes rc=0.

**The platform disjointness** (`2e93a0c`). `bench-deal-brief.md` presented "no shared company,
person or platform" as mechanically held while only the nine entity names were asserted.
`no-platform-collision` now asserts the six platform names `examples/deal-brief.md` gives as its
migration source and target are absent from the bench brief. Mutation probe: appending
`Amazon EC2` to the brief fails with `reuses shared-deal-brief platforms: ['Amazon EC2']`, exit 1;
the restored control passes exit 0 with the brief byte-identical.

**The third class was not mechanized.** README's "enforcing all of the above" was measured by
instrumenting `pathlib.Path.read_text`/`read_bytes`/`open` over a live run: the checker opens 23
files, and six of the 21 inventory bullets above that line are never opened. Turning that into a
build gate needs the checker to execute itself under a tracer, so it is recorded as a candidate in
`WINDOWS.md` id 17 rather than shipped half-working.

## Two corrections to the plan's own findings

Both verified by the same instrumentation, both recorded rather than quietly worked around:

- The plan listed `evals/trigger/RESULTS-trigger.md` as unenforced. It **is** opened, via
  `CLAIM_SOURCE_GLOB = 'evals/*/RESULTS*.md'`. A grep for the literal returns zero because the path
  is reached by glob.
- The plan called README's inventory "17-item". It is 31 bullets, 21 of them above the checker line.

And the plan's preamble said "the one finding that ships to a user is task 12" while G-06-15's record
and task 9's own heading both say task 9. Task 9 ran first; the plan line is corrected in place with
a dated marker (`9384c00`).

## Task 14 — the self-audit found seven defects in this round's own text

Ran over all 595 added lines. Command output, not an assertion that the audit happened.

**Check 1, citations:** 4 real citations in added text, all resolve. The 5 apparent misses are
synthetic fixture strings inside the new self-test, which is correct.

**Check 3, enforcement scope:** found two more citations this round broke in a passage it had not
otherwise touched, and one scope overstatement — the label check described as firing on "shipped
skill content", which reads wider than its globs, since the two derivatives *are* shipped skill
content and it never opens them.

**Absolutes sweep** over 112 sentences carrying *only*/*never*/*nothing*/*every*/*all*/*none*,
against the full tracked tree including `.planning/`. Verified correct: the 23-file surface, the six
unopened items, ten CI commands, nine names and six platforms, 31 PF + 8 MC lines, zero fences in
six files, four-of-four bullets carrying dated markers, five files in the many-publishers sweep.

Four were wrong, all written by this round:

1. "moved all four of them" about the replay figures — three of four moved (435→438 commits,
   164→185 instances, 37→40 carrying); the 14 distinct spellings held.
2. The same sentence was spliced with two `because` clauses.
3. "nine citation-drift findings" was a count not derivable from the UAT. Removed rather than
   guessed, per task 5's own rule.
4. "silent on every one of the four" undercounted — six citations drifted, not four.

Two more were caught before their commits landed: a whole-file `grep -c '20%'` cited as provenance
for "four" when this round's own correction paragraph pushed it to seven (scoped to
`grep -c '^|.*20%'`, which returns four for each brief), and an internal contradiction in the new
README bullet ("all six are scripts … plus the prose file"). A seventh was caught after: the
reproduced ledger's row 17 still said "four citations" after the WINDOWS entry said six.

The plan's line-based verify command for task 2 was also unsatisfiable: `"one per Command of the
Message"` straddles a line break in `NUMBERING.md`, so `git grep` can never find it there. Recorded,
with the wrap-tolerant command that does.

## Answered rather than carried

Round 4's five reasoning critiques (`81dfc6b`). Four answered in the text, one carried with a reason:

- **Id 6's `Closed on reasoning` label.** The wording changes, not the disposition. The label means
  the entry's own question is answered here on stated reasoning; it does not mean nothing is left
  live. Id 6's two subsidiary questions stay on `Open — v2` row 31, linked from both places. Not
  reopened, because reopening asserts the disposition question is unanswered, which is false.
- **The PF-1 entry's unrecorded Force Management read.** "Ordered the way the framework itself
  sequences them" is gone, under exactly the standard 06-07 applied to id 6's "many independent
  publishers" clause twenty lines away. Symmetry noted: the MC side's walk-through order *does* have
  recorded sources, so the absence is specific to this clause.
- **"Live and unadjudicated."** "Live" carried two senses and this file evidences one. Restated as
  current use by the holder, with register status not claimed — the lookup is recorded as not
  attempted separately.
- **Prong 3's whole-repo negative.** Answered rather than carried because it cost one command; the
  sweep is recorded inline and every hit is this record or the defect register discussing the absence.
- **Carried:** the `completeness-audit.md`:12-15 reading is incomplete rather than false. Those lines
  both route provenance to the registry and decline to state the methodology's original order; the
  bullet names only the second. It stays on `WINDOWS.md` id 31 per the standing rule that a judgement
  about argument quality belongs on an open row, not in a correction paragraph.

## Ledger

`WINDOWS.md`'s JSON edited and the whole table re-rendered from it programmatically; no row
hand-edited. The round-trip found a pre-existing divergence — id 6's JSON `reason` carried a leading
space the rendered row did not — so all reason fields were normalized. Table now matches the JSON
field for field across 32 rows, counts agree, `gsd-tools windows status` parses.

`LEGAL-REVIEW.md`'s reproduced ledger was stale at round 2 (id 12) and "fifth round" (id 17):
06-07 updated the JSON and not the reproduction. Both cells rebuilt through an escape-aware parser
and reconciled row for row — 32 rows, ids complete, dispositions consistent under the documented
four-label/three-state mapping, stated count 32 = actual 32.

## Task Commits

1. **Task 9: derivatives' omission notice** — `f909d3c` (fix)
2. **Task 10: route-equivalence denials** — `96030d8` (fix)
3. **Task 11: caveat count + assertion** — `cfff672` (fix)
4. **Task 12: platform assertion + 20% count** — `2e93a0c` (fix)
5. **Task 8: README enforcement claim** — `4f76e32` (fix)
6. **Task 1: two-step label argument** — `2ace809` (fix)
7. **Tasks 2, 3: misquote, contradiction, provenance** — `0447175` (fix)
8. **Tasks 4-7: over-correction, tally, English claim, grounds count** — `22c99f2` (fix)
9. **Tasks 15, 17: citation checker + symbol anchors** — `3589842` (feat)
10. **Task 16: reasoning critiques** — `81dfc6b` (docs)
11. **Task 13: ledger** — `2e43583` (docs)
12. **Task 14: self-audit** — `33569f8` (fix)
13. **Plan preamble correction** — `9384c00` (docs)
14. **Task 14 re-audit: reproduction row 17** — `389bafa` (fix)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Correctness] Task 17's declared ceiling rewritten against a measurement**
- **Found during:** Task 17
- **Issue:** The plan specified a ceiling paragraph asserting the new code "would have caught the
  `README.md`:367-369 slip and the `NUMBERING.md`:26-40 slip". Both are false — at the commits where
  those slips existed the cited lines were in range.
- **Fix:** Replaced the assertion with a full-history replay, reported in the docstring: 435
  commits, 164 citation-instances, 14 distinct spellings, zero firings. A control run confirmed the
  replay had citations to test rather than returning zero for want of input.
- **Verification:** `--self-test` and `--mutation-test` both PASS naming the code; replay and
  control reproduced in this summary.
- **Committed in:** `3589842`

**2. [Rule 1 - Correctness] Task 15's "do not convert check_repo.py citations" instruction reversed**
- **Found during:** Task 15
- **Issue:** The plan said line numbers are "the only practical anchor" in `check_repo.py` and that
  task 17 would put a check under them. Task 17's own commit then broke five such citations, and the
  check was silent on all five.
- **Fix:** Anchored them to `SOURCE_COINED_LABELS`, `_source_label_pattern` and
  `check_source_label_in_skill_content` by name. A named symbol does not drift.
- **Verification:** all five resolve to the intended code; no live line citation into
  `check_repo.py` remains outside quoted retired ones.
- **Committed in:** `3589842`, `33569f8`

**3. [Rule 2 - Missing Critical] The plan's own preamble mis-numbered its priority**
- **Found during:** Before task 1
- **Issue:** "The one finding that ships to a user is task 12" contradicts G-06-15's record and task
  9's own DO THIS FIRST heading. Task 12 is a benchmark fixture that ships to nobody.
- **Fix:** Executed task 9 first; corrected the plan line in place with a dated marker.
- **Committed in:** `9384c00`

---

**Total deviations:** 3 auto-fixed (2 correctness, 1 missing critical)
**Impact on plan:** All three are the plan's own statements failing the standard the plan sets. Task
17's scope was delivered as specified; only its truth claims changed, and they changed toward a
measurement. No scope creep.

## Issues Encountered

**The closing round authored defects again, and the count is the finding.** Seven in this round's own
added sentences — four found by task 14's audit, two caught before their commits landed, one after.
That is up from ten-of-seventeen authored by round 3's closing commit only in the sense that these
were caught inside the round rather than by round 5's readers. Whether that is progress is round 5's
question, not this summary's.

Two of the seven were created by fixing another finding: task 8's README edit broke a citation into
README, and task 17's docstring insertion broke five into `check_repo.py`. Both were mechanical
consequences of adding lines above a line citation, and both are now structurally prevented by the
anchoring convention rather than by care.

## Next Phase Readiness

**The closure condition is unchanged and has still not been met:** `/gsd-verify-work 06` for round 5,
with the four-brief standing set. The fourth brief — aimed at the closing commit's own added lines —
is mandatory, and this round is the strongest case for it yet: it would have been the reader that
caught all seven of the defects above.

All ten CI commands green. Green CI remains necessary and not sufficient: it was green through all
seventeen of round 4's findings, all eleven of round 3's, all fourteen of round 2's and all three of
round 1's. `WINDOWS.md` id 17's pattern, seventh consecutive round.

**The honest note the plan asked for.** `LEGAL-REVIEW.md` is now 1,004 lines, up from 847 — this
round added 157 while correcting 13 statements. Task 5 removed one drifting count and this round then
wrote four more, three of which it caught itself. The plan said that if round 5 again finds most of
its findings in the closing commit's own text, the remedy is to cut the prose rather than keep
correcting it. That threshold is reached on this round's evidence, not round 5's: a record that needs
157 lines of correction paragraphs to fix 13 sentences, and produces 7 new defects doing it, has more
prose than this project can keep true. **Round 5 should cut `LEGAL-REVIEW.md`, not audit it.**

---
*Phase: 06-legal-review-gate-launch*
*Completed: 2026-09-22*
