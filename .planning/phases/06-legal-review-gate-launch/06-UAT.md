---
status: complete
phase: 06-legal-review-gate-launch
source: [06-VERIFICATION.md]
started: 2026-09-21
updated: 2026-09-22
rounds: 6
round_2: "06-05 gap closure — tests 7-9 re-ask tests 2, 3 and 6 of the corrected files"
round_2_result: "1 passed, 2 issues — G-06-7 and G-06-9 opened 2026-09-21"
round_3: "06-06 gap closure — tests 10-12 re-ask tests 7 and 9 of the corrected files, plus a new whole-tree sweep bound to no named file"
round_3_result: "0 passed, 3 issues — G-06-10, G-06-11 and G-06-12 opened 2026-09-22, all three closed by 06-07 the same day"
round_4: "06-07 gap closure — tests 13-16 re-ask tests 10-12 of the corrected files, plus the first run of the four-brief standing set"
round_4_result: "0 passed, 4 issues — G-06-13, G-06-14, G-06-15 and G-06-16 opened 2026-09-22; 17 findings, 10 of them authored by the closing commit"
round_5: "06-08 gap closure — tests 17-20 re-ask tests 13-16 of the corrected files; the four-brief standing set, second run"
round_5_result: "0 passed, 4 issues — G-06-17, G-06-18, G-06-19 and G-06-20 opened 2026-09-22; 18 findings, 8 of them authored by the closing commit. All four closed by 06-09."
round_6: "06-09 gap closure — tests 21-24; the four-brief standing set as 06-09 amended it: fourth brief widened to every gap-closure commit range, whole-tree sweep at two readers. Seven readers, run as subagents because the headless claude -p route was blocked this session."
round_6_result: "1 passed, 3 issues — G-06-21, G-06-22 and G-06-23 opened 2026-09-22; 25 findings. README returned zero for the first time in six rounds. 9 of 25 authored by a gap-closure round (4 by the last, down from 8 of 18); 16 predate the closures and 8 predate Phase 6. Both of 06-09's structural changes measured and both paid."
---

## Current Test

[testing complete — round 6; 3 gaps open]

## How these six were performed

The six items were recorded as human-judgement checkpoints because the executing session could not
perform them. Two of the three stated reasons had expired by this session and were re-checked
rather than honoured:

- **"No independent reader was available"** (tests 2, 3, 4, 6). Five independent readers were run as
  separate headless `claude -p` sessions in a scratch directory holding only the files under review,
  each given a neutral brief that did not name the wanted answer, each writing to its own output
  file. None had written the text it read. Two readers were given the README contradiction hunt
  independently so their findings could be cross-checked against each other.
- **"A non-interactive session has no `/config` picker"** (test 5). An interactive Claude Code
  session was driven in a pty and its rendered terminal output captured. This observes the picker
  programmatically rather than with a human eye; what it cannot speak to is stated in the test.

Every finding a reader returned was re-verified against the repository before being recorded here.
One reader finding was refuted on verification and is recorded as refuted.

**All ten CI commands were green while the three false statements were in the tree.** Run
2026-09-21 from `.github/workflows/ci.yml`: `check_repo.py --self-test` PASS,
`--mutation-test` PASS (56 codes discrimination-proven), `check_repo.py` **0 violations**, and the
six self-tests in `evals/` and `tools/generate_derivatives.py --check` all rc=0. This is the
fourth consecutive round matching WINDOWS.md id 17's pattern — a green mechanical gate and a false
sentence found by a reader on the first pass — and it is the argument against building a
fuzzy-proxy gate for this class, not for it.

## How tests 7-9 were performed

Round 2, 2026-09-21. Five independent readers, run as separate headless `claude -p` sessions on
`claude-opus-5` in a scratch directory holding the committed tree with `.planning/` and `.claude/`
removed, each on a neutral brief that did not name the wanted answer, each writing to its own output
file. None had written the text it read. The README contradiction hunt was given to two of them
independently, as in round 1, so their findings could be cross-checked against each other.

Every finding below was re-verified against the repository before being recorded. Findings that are
reasoning critiques rather than checkable falsehoods are recorded as observations, not gaps.

**All ten CI commands were green again while every false statement below was in the tree.** Run
2026-09-21 from `.github/workflows/ci.yml`: `check_repo.py --self-test` PASS, `--mutation-test` PASS
(56 codes discrimination-proven), `check_repo.py` **0 violations**, and the six self-tests in
`evals/` and `tools/generate_derivatives.py --check` all rc=0. *Corrected 2026-09-22 (06-09):
this read "seven". Commit `9f841df`, the round-5 UAT edit, removed three such lines from this
file's other methodology sections and missed this one; `evals/` holds six scripts and `ci.yml`
runs six.* This is the fifth consecutive round matching `WINDOWS.md` id 17's pattern.


## How tests 10-12 were performed

Round 3, 2026-09-22, against commit `034c75d`. Five independent readers, run as separate headless
`claude -p` sessions on `claude-opus-5` in five separate scratch directories, each holding its own
copy of the committed tree with `.planning/` and `.claude/` removed, each on a neutral brief that did
not name the wanted answer, each writing to its own output file. None had written the text it read.
Two briefs were given to two readers each so their findings could be cross-checked; a fifth reader
was given a whole-tree contradiction sweep bound to no single file, which is new this round.

- Readers 1 and 2 — README contradiction hunt (test 11).
- Readers 3 and 4 — `LEGAL-REVIEW.md`'s reproduction-boundary material (test 10).
- Reader 5 — any two committed files that cannot both be true (test 12).

Every finding below was re-verified against the repository before being recorded, and convergence is
noted per item. Findings that are reasoning critiques rather than checkable falsehoods are recorded
as observations, not gaps. One reader finding was adjudicated against on a 2-to-1 split and is
recorded as an observation.

**A limitation of the setup, stated because it bounds what these readers could reach.** `.planning/`
is tracked in this repository but was removed from the readers' trees, so README's two
`.planning/WINDOWS.md` cross-references (`:96`, `:153`) and `LEGAL-REVIEW.md`'s ledger provenance
were outside what any reader could check. Reader 3 said so unprompted. Those were checked by this
session instead: `WINDOWS.md` entries 16 and 24 carry what the two files cite.

**The sweep brief, recorded verbatim so the next round runs it rather than reinventing it.** This is
the one that found all three of test 12's statements, in three files six earlier readers across two
rounds had no reason to open. It costs the same as a file-scoped reader.

> You are reading a software repository you did not write. Your task: find places where two committed
> files in this repository state things that cannot both be true.
>
> Do not restrict yourself to any one file. Pay particular attention to:
> - statements about whether a measurement, benchmark, search, review or observation has or has not
>   been performed;
> - counts of anything (rules, examples, routes, runs, sessions, dimensions, files, violations);
> - descriptions of what a script or an automated check does, measured against what its code does;
> - claims about what some other file contains or does not contain;
> - statements about the environment this repository was built in.
>
> Note that skills/proof-first/SKILL.md, output-styles/proof-first.md and prompts/system-prompt.md
> carry overlapping generated text and all three ship to users: a sentence that is stale in one is
> stale in all three.
>
> For each finding: both file paths with line numbers, both quoted texts, and one sentence saying why
> they cannot both be true. Open the files and check; do not report suspicions.
>
> End with a list of what you checked and found consistent.
>
> Work only from files in this directory. Output plain text, no preamble.

The two file-scoped briefs are the round-1 and round-2 briefs unchanged, one pointed at `README.md`
and one at `LEGAL-REVIEW.md`, each asking only for statements a committed file contradicts and
requiring the reader to open that file before writing a finding down.

**The standing brief set, from round 4 on — four briefs, not three.** Recorded here by 06-07 task 12
because three rounds have each found a class the round before could not see, and the fix is the brief
set rather than any one correction:

1. `README.md` — contradiction hunt, file-scoped.
2. `LEGAL-REVIEW.md` — contradiction hunt plus reasoning critique, file-scoped.
3. **The whole-tree sweep above, bound to no named file.** Non-negotiable: it is the only brief that
   can reach a contradiction between two files neither of the first two names, and it found three
   on its first run.
4. **One brief pointed at whatever the last gap-closure round rewrote.** Four of round 3's eleven
   findings were authored by the round that was closing round 2, and two of round 2's fourteen by the
   round closing round 1. The closing round's own new sentences are the highest-yield unread surface
   in the repository, and no brief has ever been aimed at them directly.

A round that runs fewer than four is not comparable with round 3 and must not be read as cleaner
than it.

**All ten CI commands were green again while all eleven false statements below were in the tree.**
Run 2026-09-22 from `.github/workflows/ci.yml`: `check_repo.py --self-test` PASS,
`--mutation-test` PASS (57 codes discrimination-proven), `check_repo.py` **0 violations**, and the
six self-tests in `evals/` and `tools/generate_derivatives.py --check` all rc=0. This is the sixth
consecutive round matching `WINDOWS.md` id 17's pattern, and the third in which the gap-closure round
that fixed the previous round's findings authored one of the next round's.


## How tests 13-16 were performed

Round 4, 2026-09-22, against commit `38c873b`. **Six readers across the four-brief standing set** this
repository recorded after round 3 — the first round to run it. Each reader was a separate headless
`claude -p` session on `claude-opus-5`, in its own copy of the committed tree with `.planning/` and
`.claude/` removed, on a brief that did not name the wanted answer, writing to its own output file.
None had written the text it read.

| Brief | Readers | Test |
|---|---|---|
| `README.md` contradiction hunt | 2 | 14 |
| `LEGAL-REVIEW.md` reproduction-boundary material | 2 | 13 |
| Whole-tree sweep, bound to no named file | 1 | 15 |
| **What the last gap-closure round rewrote** (new) | 1 | 16 |

The fourth brief was added because four of round 3's eleven findings were authored by the round
closing round 2. Its reader was given `RECENT-CHANGES.txt` — the 202 added lines of commit `908b90b`,
grouped by file — and asked to verify every citation, count, scope claim and absolute in them against
the tree. **It was the highest-yield reader of the round.** It justified the brief on first use.

Every finding below was re-verified against the repository before being recorded. Attribution is
`git blame` on each cited line.

**All ten CI commands were green while all seventeen false statements below were in the tree.** Run
2026-09-22 at `38c873b`: `check_repo.py --self-test` PASS, `--mutation-test` PASS (57 codes
discrimination-proven), `check_repo.py` **0 violations**, and the six self-tests in `evals/` and
`tools/generate_derivatives.py --check` all rc=0. Seventh consecutive round of `WINDOWS.md` id 17's
pattern.

**The round's result, stated before the detail, because it reverses the trend.** Round 4 found *more*
than round 3 (17 against 11), and **ten of the seventeen are in text commit `908b90b` wrote while
closing round 3.** Round 3's corrections were verified to hold — again, by readers who did not make
them — and the round that made them introduced more defects than it closed. The `.planning/` absence
bounds what these readers could reach, as in round 3; reader 6 flagged it unprompted.


## How tests 17-20 were performed

Round 5, 2026-09-22, against commit `398842c`. **Six readers across the same four-brief standing
set**, second run. Each reader was a separate headless `claude -p` session on `claude-opus-5`, in
its own copy of the committed tree with `.planning/` and `.claude/` removed, on a brief that did
not name the wanted answer, writing to its own output file. None had written the text it read.

| Brief | Readers | Test |
|---|---|---|
| `README.md` contradiction hunt | 2 | 17 |
| `LEGAL-REVIEW.md` reproduction-boundary material | 2 | 18 |
| Whole-tree sweep, bound to no named file | 1 | 19 |
| What the last gap-closure round rewrote | 1 | 20 |

Reader 6 was given `RECENT-CHANGES.txt` — the added lines of `git diff 38c873b..398842c` outside
`.planning/`, 658 lines grouped by file — and asked to verify every citation, count, scope claim and
absolute in them against the tree.

Every finding below was re-verified against the repository by the orchestrator before being
recorded; the verification is quoted in each test's evidence block rather than taken from the
reader. Attribution is `git blame` on each cited line, plus a read of the same line at `38c873b`
where the surviving text is older than the contradiction it now sits in.

**All ten CI commands were green while all eighteen false statements below were in the tree.** Run
2026-09-22 at `398842c`: `check_repo.py --self-test` PASS, `--mutation-test` PASS (58 codes
discrimination-proven), `check_repo.py` **0 violations**, and the six self-tests in `evals/` and
`tools/generate_derivatives.py --check` all rc=0. Eighth consecutive round of `WINDOWS.md` id 17's
pattern.

**The round's result.** Eighteen findings against round 4's seventeen — the count did not fall. The
last round's share did: **8 of 18, against 10 of 17.** The fourth brief justified itself a second
time, and this round it converged with the other briefs rather than standing alone.

**By `git blame`, a gap-closure round authored ten of the eighteen — not eight.** Two are older
closures, not the last one: `README`:196 was written by **06-05**, closing round 1, and
`LEGAL-REVIEW`:913's "seven self-tests" by **06-06**, closing round 2. Both have survived every
round since. The pattern this phase keeps recording is not that the *last* closure is the defect
source; it is that *a closure* is, and the earlier ones are still in the tree.

**The remaining eight predate Phase 6's gap closures entirely**: `README`:53 (04-13),
`README`:306 (04-08), `LEGAL-REVIEW`:119 and :170 (06-02), :723 (06-04),
`evals/trigger/INIT-EVENTS.md` (02-10), `check_repo.py`:239 (03-03, where `03-03-PLAN.md`'s own
frozen list already disagreed with the prose above it), and `bench-deal-brief.md`:107 (05-02). Four
rounds of cold reads had not reached them, because until round 3 every brief named a file, and no
reader had opened `evals/trigger/`, the `## Launch` section or `artifact-patterns.md`'s label
inventory until this one. Zero of the eighteen are regressions of an earlier fix.

**Three of the eight closing-round findings are the same defect shape**: the round asserted a
property of its own new code that the code's own docstring, written in the same batch, denies.


## How tests 21-24 were performed

Round 6, 2026-09-22, against commit `66322b1`. **Seven readers across the four-brief standing set**,
first run of the set as 06-09 amended it. Each reader worked in its own copy of the committed tree
with `.planning/` and `.claude/` removed, on a brief that did not name the wanted answer, and none
had written the text it read.

| Brief | Readers | Test |
|---|---|---|
| `README.md` contradiction hunt | 2 | 21 |
| `LEGAL-REVIEW.md` reproduction-boundary material | 2 | 22 |
| Whole-tree sweep, bound to no named file | **2** (first run at two) | 23 |
| What **any** gap-closure round rewrote | 1 | 24 |

**The reader harness changed this round, and not by choice.** Rounds 1-5 ran each reader as a
headless `claude -p` session. In this session that route is refused by the permission classifier,
which blocked the invocation and stated that other tools may be used for the same goal. The seven
readers were therefore run as independent subagents instead. The property the test depends on is
unchanged — a separate context, its own copy of the tree, a brief that names no answer, no
authorship of the text under review — but the mechanism is not the one rounds 1-5 used, and this
entry records that rather than letting the round read as a like-for-like repeat.

**The fourth brief's range as specified was wrong, and the corrected range was run.** The standing
set carried into this round — recorded in `WINDOWS.md` id 17 and in this file's own standing-set
table for the next round, not in the reader table above — named `d67012e..HEAD`, glossed as "the
first commit of the 06-05 closure onward". Those are different ranges: `d67012e..HEAD` excludes
`d67012e`'s own changes. Demonstrated — the line
`36 headless sessions, three measured arms, four artifact families` is live in `README.md` at
`66322b1`, was added by `d67012e`, and appears as an added line in `d67012e^..HEAD` but not in
`d67012e..HEAD`. Reader 7 was given `d67012e^..HEAD`, the range the gloss requires: 86 commits and
1,714 added lines across 15 files outside `.planning/`, measured at `66322b1`, which was HEAD when
the reader ran. The figure moves with every later commit and is recorded against that HEAD for
that reason. *Corrected 2026-09-22 (06-10): this said "the standing set above", which pointed at the
reader table two paragraphs up; that table has no Input column and names no range. Both sites that
do carry the range were corrected to the caret form by 06-10 task 21.*

**Three findings came from the orchestrator, not from a reader, and could not have come from one.**
Every reader tree has `.planning/` stripped, so no reader can check a claim whose subject is a
`.planning/` file — or any claim whose truth depends on `.planning/` being present, which is why
`LEGAL-REVIEW.md`:571's sweep count is unreachable by the four readers who had that file open. This
is a standing gap in the harness: the record that governs the round is the one surface the round
does not read.

Every reader finding below was re-verified against the repository by the orchestrator before being
recorded, and the verification is quoted in each test's evidence block rather than taken from the
reader. Three reader claims did not survive that check and are recorded as refuted or corrected
rather than dropped silently.

**All ten CI commands were green while all twenty-five false statements below were in the tree.**
Run 2026-09-22 at `66322b1`: `check_repo.py --self-test` PASS, `--mutation-test` PASS (58 codes
discrimination-proven), `check_repo.py` **0 violations**, and the six self-tests in `evals/` plus
`tools/generate_derivatives.py --check` all rc=0. Ninth consecutive round of `WINDOWS.md` id 17's
pattern.

### The round's result, and what changed in the diagnosis

**Twenty-five findings, against eighteen in round 5.** The count rose, and the reason is that the
briefs reached further back, not that the tree got worse. The attribution moved sharply:

| | Round 5 | Round 6 |
|---|---|---|
| Total findings | 18 | **25** |
| Authored by *a* gap-closure round | 10 (56%) | **9 (36%)** |
| — by the **last** closure | 8 (44%) | **4 (16%)** |
| — by **earlier** closures | 2 (11%) | **5 (20%)** |
| Predating the closures entirely | 8 (44%) | **16 (64%)** |

**The last closing round's share more than halved.** 06-09 authored 4 of 25 against 06-08's 8 of 18.
Its self-audit and the code-review gate are working on the surface they cover.

**What replaced it is old text.** Eight findings come from Phases 1 and 3: `check_repo.py`'s opening
scope sentence and its violation-code catalogue (`5b124ba`, plan 01-01), `SOURCES.md`'s review stamp
(`0ba93f8`, 01-03), `RESULTS-mod04.md`'s unanchored banner and its CR-01 section (`fbe0aa6`, 03-09),
both double-counted sessions (`878b937`, 03-12), and one mutation-scope comment (`82535c7`, 03-16).
Every one has survived six rounds of cold reads and every CI run since it was written. The
conclusion this supports is not that the closing rounds stopped being a defect source — five of the
nine closure-authored findings are from 06-08 and 06-06, not 06-09 — but that the defect population
is older and larger than five rounds of file-named briefs could see.

**Both of 06-09's structural changes are now measured, and both paid.**

*Change 1, the widened fourth brief.* One of reader 7's two unique findings —
`LEGAL-REVIEW.md`:383-384, authored by 06-08's `33569f8` — returns **0 matches** in
`git diff ade21af^..HEAD` (the 06-09 range a diff-scoped brief would have been given this round) and
**1** in `d67012e^..HEAD`. `33569f8` provably predates the 06-09 range. The widening reached exactly
one finding no diff-scoped brief could have seen, on its first run.

*Change 2, the second sweep reader.* Sweep A returned 9 findings, sweep B returned 7, and 3 were
shared. **Sweep B produced 4 findings the first sweep reader did not** — 16% of the round's total.
The standing set's exit condition is a marginal yield of zero for two consecutive rounds; this is
the first measurement and it is not zero. Two sweep readers stay.

**The README brief returned nothing, for the first time in six rounds.** Two readers, cross-checked,
zero gaps. Both independently instrumented the checker to confirm the 23-file surface, both mutated
the stated counts to confirm the checker does not catch them, and both regenerated all four results
files byte-identical. The one finding raised was refuted on verification — see test 21.

**The largest single defect class this round is the scope absolute**: a sentence claiming that no
other code, no other check, or no other file does something, written next to the code it describes
and falsified by code added later in the same file. Six of the twenty-five are that shape
(`check_repo.py` T1, T3, T4, T5, T6 and `LEGAL-REVIEW.md` L7), and `T6` has the cleanest causal
chain of the round: 06-08's `3589842` added `check_record_citations`, which reads `LEGAL-REVIEW.md`,
and thereby falsified a comment sixteen lines away saying no other check does. 06-09 then edited
that same comment block (`36ef0a9`) and corrected one sentence while three false scope absolutes
stayed in it.

## The standing set, as amended by 06-09 — what round 6 must run

Round 5's diagnosis changed the fourth brief's scope, and added a second sweep reader. Both
decisions are recorded here rather than only in a commit message, because this is the table the
next round reads.

| Brief | Readers | Input |
|---|---|---|
| `README.md` contradiction hunt | 2 | the file |
| `LEGAL-REVIEW.md` reproduction-boundary material | 2 | the file |
| Whole-tree sweep, bound to no named file | **2** (was 1; changed 06-09) | the tree, no file named to either reader |
| What **any** gap-closure round rewrote (amended 06-09; was "the last") | 1 | the union of every gap-closure commit range — `d67012e^..HEAD` today, the first commit of the 06-05 closure onward (notation corrected by 06-10 task 21; the two-dot form excludes `d67012e`'s own changes, which the gloss requires) |

**Change 1 — the fourth brief widens past the last round's diff.** Through round 5 this brief was
given the diff of the round that had just closed. Round 5 proved the blind spot: `README`:196 was
authored by **06-05**, closing round 1, and `LEGAL-REVIEW`'s "seven self-tests" by **06-06**,
closing round 2. Both survived every read since, and no diff-scoped brief could ever have seen
them, because neither is in the last round's diff. The rule this phase has been recording is
therefore not "the closing round is the defect source" but **"a closing round is, and the earlier
ones are still in the tree."** The input widens to the union of every gap-closure commit range. It
costs one session and nothing else: the reader already does this work, it was only looking at a
smaller window than the defect population occupies.

**The measurement that justifies change 1, pinned to round 5 and not restated as a live count.** At
round 5 (2026-09-22, commit `398842c`), 10 of 18 findings were authored by a gap-closure round: 8
by the last one, 06-08, and 2 by earlier ones, 06-05 and 06-06. A future round must be able to see
whether widening the window moved that split, so these figures stay pinned to round 5 rather than
being carried forward as a running claim.

**Change 2 — a second sweep reader, and why yes rather than no.** The sweep is the only brief that
names no file, and round 5 measured exactly what that route returns. Its one reader produced four
findings, recorded as test 19: `check_repo.py`:4470-4476 contradicting its own module docstring,
`INIT-EVENTS.md`'s 23-key block, the "fifteen frozen element labels" count in two `check_repo.py`
docstrings, and the bench brief's reversed timeline. **Three of those four predate Phase 6's
closures entirely**, in `evals/trigger/`, `artifact-patterns.md`'s label inventory and
`bench-deal-brief.md` — places no other brief had opened in five rounds. The fourth was 06-08's own
text, which the diff-scoped fourth brief was pointed straight at and did not catch.

The round's other five pre-Phase-6 findings came from the file-named briefs — two in `README` from
the contradiction hunt, three in `LEGAL-REVIEW` from the reproduction-boundary brief — so the sweep
is not the only route to old text. It is the only route to *unnamed* text, and one reader carrying
that whole surface is a single point of failure over the largest unexplored area. The cost of a
second is one session.

*Corrected 2026-09-22 (06-09), by this round's own self-audit: the paragraph above first said all
eight pre-Phase-6 findings were reached by the sweep reader, and that it found "four two-file
contradictions plus" two more. Both are wrong against this file's own test records — the sweep
reader returned four findings in total, three of them pre-Phase-6. The claim was carried over from
06-09-PLAN.md's task 20, which asserted it; a plan is not a source of truth over the UAT record it
was written from.*

The second reader gets **the same no-file brief, independently** — not a narrower one. Naming files
to it, or partitioning the tree between the two, would collapse it into the file-named briefs and
destroy the property that makes the sweep valuable. Two readers on one identical unnamed brief is
the arrangement the `README.md` hunt has used since round 1 precisely so their findings can be
cross-checked.

This also converts "plausibly high and unmeasured" into measured. Round 6 records how many of the
second sweep reader's findings the first did not produce, and vice versa. If the marginal yield is
zero for two consecutive rounds, drop back to one reader and record that; until then the marginal
value of a second sweep reader is unknown, which is the reason to run it, not the reason to skip
it.

## The standing set, as amended by 06-10 — what round 7 must run

Round 6 confirmed both of 06-09's changes and added three of its own. This is the table round 7
runs; the paragraphs after it say why each line is where it is, and what would retire it.

| Brief | Readers | Input |
|---|---|---|
| `README.md` contradiction hunt | 2 | the file |
| `LEGAL-REVIEW.md` reproduction-boundary material | 2 | the file |
| Whole-tree sweep, bound to no named file | 2 | the tree, no file named to either reader |
| What **any** gap-closure round rewrote | 1 | the union of every gap-closure commit range — `d67012e^..HEAD` today |
| **`.planning/` record sweep** (new; 06-10 task 25) | 1 | `.planning/`, with the shipped tree available for checking |

**Change 3 — a fifth brief, over `.planning/`.** Three of round 6's twenty-five findings came from
the orchestrator rather than from any reader, and could not have come from one: every reader tree
has `.planning/` stripped, so no reader can check a claim whose subject is a `.planning/` file. The
record that governs the round is the one surface the round does not read. The fifth brief inverts
the current arrangement — the reader is given `.planning/` and may open the shipped tree to check
what it finds, rather than being given the tree with `.planning/` removed. One reader, one session.
Round 6 supplies its first measurement in advance: 06-10's own audit of this file, run under change
4 below, found that finding C cited two sites as `06-UAT.md`:1417 and `:1907`, and that `:1907` did
not resolve even at `66322b1`, the HEAD the finding was written against. That is exactly the class
no reader could reach.

**Change 4 — the self-audit's scope widens from the round's own added sentences to every
`.planning/` file the round edited.** 06-09's task-18 self-audit read its own added sentences and
found eight defects, and it was the strongest single instrument of that round. Two of round 6's
three orchestrator findings were nonetheless in files 06-09 had written to and not re-read. Added
sentences and touched files are different sets, and the difference is where those two sat.

**Change 5 — every closure plan ends by re-running the command literals it committed, after the
SUMMARY lands.** `LEGAL-REVIEW.md`'s unexcluded-sweep count was true when `f547989` wrote it
("fix(06-09): task 18 self-audit — the round's own quoted-string anchor was self-referential") and
false five commits later, falsified by `10cfa1e` ("docs(06-09): complete gap closure for round 5 —
21 tasks, 8 files, 1 new assertion, 8 self-audit defects"), the round's own SUMMARY commit. No
self-audit can see that: the audit runs before the SUMMARY exists. The remedy is a final task, run
after the SUMMARY commit, that re-runs every command literal the round wrote into prose and
corrects what moved. Round 6's own write-up did this to itself, caught one, and recorded the catch.
06-10 ran it too, and the sentence it changed is recorded in `06-10-SUMMARY.md`.

**Both of 06-09's changes stay, and the measurement is what keeps them.** Change 1, the widened
fourth brief, reached the `LEGAL-REVIEW.md` bullet summarising the two source-coined labels as
sitting in a production constant "rather than in a fixture" — `:383-384` at `66322b1`, authored by
06-08's `33569f8` ("fix(06-08): task 14 self-audit — seven defects found in this round's own
work"). The added-line sweep for that phrase over `ade21af^..HEAD`, the 06-09 range a diff-scoped
brief would have used, returns 0 matches; the same sweep over `d67012e^..HEAD` returns 1. One finding a diff-scoped brief provably could
not see. Change 2, the second sweep reader, produced 4 findings the first did not — 16% of round
6's 25. Neither exit condition is met: the fourth brief retires when a round's widening reaches
nothing the narrow range would have, and the second sweep reader retires after **two consecutive**
rounds of zero marginal yield. Round 7 records the second sweep measurement again. One round of
nonzero yield is not a decision either way, which is the same standard the `README.md` brief is
being held to after returning its first zero this round.

## Tests

### 1. The six confirmed sources are in bounds, and nothing was reproduced from them
expected: Every URL in SOURCES.md is public and outside the "Out of bounds" list, and no wording from any of them appears in this repository.
result: pass
evidence: |
  All six URLs fetched 2026-09-21, all HTTP 200.

  Public, no login/registration/paywall:
  - The three openlibrary.org records redirect an automated client to a `verify_human` bot
    interstitial. That is an anti-scraping challenge, not a gate: the records returned over the
    unauthenticated JSON API (`/books/<id>.json`) with title and publish date — MEDDICC (Nov 25,
    2020), The challenger sale (2011), The challenger customer (2015). The interstitial's only
    "Log In / Sign Up" text is ordinary site navigation.
  - The two forcemanagement.com pages and the meddicc.com page are public marketing pages.

  Out of bounds, checked hardest on the vendor page as the test directs: meddicc.com's own login
  link resolves to `https://mos.meddicc.com/login` — the training portal, on a different subdomain.
  SOURCES.md cites `https://meddicc.com/meddpicc-sales-methodology-and-process` and never
  `mos.meddicc.com`. The claim in LEGAL-REVIEW.md's "Source rows" section is accurate.

  Reproduction: word-shingle overlap between all six sources and SOURCES.md, NOTICES.md,
  LEGAL-REVIEW.md, README.md, NUMBERING.md, `skills/**`, `output-styles/**`, `prompts/**` and the
  phase-06 commit messages. At N=8 every hit is a title, subtitle or author list — citations by
  SOURCES.md's own rule ("Titles, publishers, URLs and dates are citations"). At N=6, with those
  citation strings excluded, exactly one residual survives across the whole corpus: the
  MEDDPICC dimension-name sequence in LEGAL-REVIEW.md. That string is the subject of test 2 and is
  adjudicated there, not here. No run of a source's own prose appears anywhere.

### 2. The reproduction-boundary reasoning for WINDOWS ids 3 and 6 is sound
expected: The id-6 acronym distinction holds, and the section engages the 2026-04-21 genericness holding correctly — neither ignoring nor over-reading it.
result: issue
reported: "The id-6 distinction does not hold as written — its load-bearing premise is false against the repository's own NUMBERING.md, and the disposition tests one of SOURCES.md's four reproduction prongs. The ruling half is sound."
severity: major
evidence: |
  **The acronym distinction — does not hold.** Three defects, each checked against NUMBERING.md:

  1. LEGAL-REVIEW.md:173-176 says the order "*is* the acronym, letter by letter". The eight blocks
     NUMBERING.md freezes are Metric, Economic Buyer, Decision Criteria, Decision Process, Paper
     Process, **Pain**, Champion, Competition. Their initials spell **M-E-D-D-P-P-C-C**. The repo
     ships "Pain", not "Identify Pain", so position 6 contributes P, not I. The shipped names do
     not spell MEDDPICC, and do not spell MEDDICC either. The premise is false.
  2. "Reordering the dimensions ... would produce a different word" is false for at least two
     swaps. Decision Criteria (MC-11-15) and Decision Process (MC-16-20) both begin with D;
     Champion (MC-31-35) and Competition (MC-36-40) both begin with C. Swapping either pair leaves
     the letter string unchanged. For those positions the order is a chosen sequence the mnemonic
     does not constrain — which is the thing SOURCES.md's definition covers.
  3. The disposition argues one of SOURCES.md's four reproduction prongs. The fourth — "a term
     coined by a source and adopted here as this repository's own label" — is never tested, even
     though the section's own third step says "The eight names are **labels** for the blocks".
     The id-3 disposition runs all its relevant prongs explicitly; id-6 does not.

  **Scope gap, larger than the item examined.** NUMBERING.md:26-40 carves PF-1 into "seven named
  sub-blocks, **one per Command of the Message element**" — Before scenario, After scenario,
  Required Capabilities, Metrics, Proof Points, Differentiators, Positive Business Outcomes — frozen
  in that order in a table. On SOURCES.md's own definition that is a source's ordered list
  reproduced in its order, for a live `®` mark with no adjudication of any kind, and no acronym
  defence is available for it. Neither id 3 (which read PF-0.1 and PF-3.1 wording) nor id 6 (which
  read the MC list) examined it.

  **The ruling half — sound.** LEGAL-REVIEW.md:180-186 states the genericness/protectability
  separation correctly and uses it to *refuse* an inference. It neither ignores the 2026-04-21
  holding nor over-reads it into copyright. One residual: the affirmative point it keeps
  (:186-188) is about "the term", but the ruling is on MEDDPICC while NUMBERING.md:9 names the
  namespace MEDDICC, and LEGAL-REVIEW.md:95-96 elsewhere refuses to extend the holding across
  spellings.

  The id-6 conclusion is probably defensible. The reasoning recorded for it is not what makes it so,
  and for an append-only diligence record whose declared value is that the reasoning is written
  down, a false load-bearing premise is the defect.

### 3. LEGAL-REVIEW.md does not read as legal advice
expected: A reader cannot come away treating any part of it — particularly the trademark sections and the reproduction-boundary dispositions — as a professional opinion.
result: issue
reported: "Independent reader's verdict: yes, a reader could reasonably come away treating parts of it as a professional opinion. The disclaimer is well written but does not reach the verdict layer, which is what a skimming reader consumes."
severity: major
evidence: |
  The opening disclaimer (:7-21) does say, in words, everything the test requires. The defect is
  structural: the document has a heavily-hedged reasoning layer and an unhedged verdict layer, and
  the verdicts are what travel.

  - `Gate status: PASSED` is **line 5** — above the disclaimer at line 7. "PASSED" on a document
    named LEGAL-REVIEW.md is clearance language. It is qualified only at :312.
  - The same header sits against :244-250, which routes Ardent Digital and Gina Almeida as open
    items needing a rename decision "before wider distribution". The gate reads PASSED while
    content items are unresolved.
  - The ledger books ids 3 and 6 as **Fixed**, which :420-421 defines as "the defect is gone from
    shipped content". No shipped content changed for either — a judgement was recorded. Under the
    file's own taxonomy these are not Fixed, and the 11/9/8 counts at :455 inherit it.
  - `Disposition: closed, boundary not crossed` (:138) is a finding of non-infringement in form.
    "Disposition" is itself a term of art for how an adjudicator resolves a matter.
  - :155 "stated publicly at this level of generality by many sources and **by none exclusively**"
    is an unbounded negative assertion about third parties' rights that the described diligence
    cannot establish — and it is broader than the walk-back three lines later at :158.
  - :187 "not a source identifier the repository could be seen to be **trading on**" applies a
    court holding to the author's own exposure, in trademark's own framing, with "therefore".
  - :240-241 "which is the disclaimer that makes a coincidental name a coincidence rather than a
    depiction" asserts that a specific mitigation is sufficient to defeat a class of claim, and the
    sentence after it enumerates elements found unmet.

  Where it holds, and this is real: the register/cancellation gap refused rather than explained
  (:78-82), "Deliberately not done" (:95-98), the aggregator report "not recorded as a fact"
  (:34-36), failed lookups recorded as failures including the HTTP 401 (:84-86, :254-258), and the
  Challenger section throughout (:100-113).

### 4. README's claim region reads as an honest report of a mixed result
expected: A technical evaluator meeting the project for the first time feels the unfavourable dimension was reported plainly rather than buried.
result: pass
evidence: |
  Independent reader's verdict: honest report of a mixed result, not a burial, and not close to one.

  - The loss is pre-announced outside the region at :163 ("The benchmark measured that directly and
    found the opposite") and then restated inside it.
  - :181 is subject-verb-number with no hedge and no lead-in clause: "On persuasive force, the
    skill-on draft lost 38 pairs."
  - The asymmetry runs *against* the project. The two favourable dimensions bundle win/tie/loss into
    one sentence each; the unfavourable one isolates the loss in its own short sentence and pushes
    the consolation figures into a second. The loss gets more sentence-level prominence, not less.
  - Caveats follow the number in a separate paragraph. Nothing pre-softens it.
  - "four pairs out of five" rounds 79.2% against the project rather than for it.
  - :183 forecloses the cheapest available excuse unprompted: "the direction is the same for both
    models rather than driven by one."
  - The proxy paragraph volunteers a second unflattering result unprompted.

  One non-blocking observation, recorded rather than actioned: the prompt-length confound at
  :191-192 is disclosed only against the losing result, but it is a property of the whole
  experiment and applies equally to the evidence and clarity wins, which carry no caveat paragraph.
  A skimmer takes away "the loss may be an artifact" without the matching "so may the wins."

### 5. The output style is listed and selectable in /config
expected: "proof-first" is listed in Claude Code's /config output-style picker and selecting it persists for the session.
result: pass
evidence: |
  Performed against Claude Code 2.1.267 on Darwin 25.6.0, in an interactive session driven in a pty
  with its rendered terminal output captured. Scoped to a throwaway project's own
  `.claude/output-styles/` — the variant README:83-84 names — so the operator's configuration
  directory was not touched.

  `/config` -> filter "output style" -> Enter -> Space opens "Preferred output style", which renders:

      ❯ 1. Default ✔
        2. Proactive
        3. Concise
        4. Explanatory
        5. Learning
        6. simple-english:simple-english
        7. proof-first — Write or check RFP and RFI responses, solution proposals, executive
           summaries, and demo or discovery documents for technical presales and bid teams. ...

  `proof-first` is listed, as entry 7, with its `description` frontmatter rendered as the entry's
  summary.

  **Selectable and persistent.** Walking the cursor down to entry 7 and pressing Enter set the row
  to `❯ Output style   proof-first`. Closing the panel, reopening `/config` and filtering again
  still read `proof-first`. It was written to disk as
  `.claude/settings.local.json` -> `{"outputStyle": "proof-first"}`, so it outlives the session
  rather than only lasting it — README:75-76 ("once selected it stays on for the whole session")
  understates this rather than overstating it.

  **Two controls, because a picker that always shows the same thing proves nothing:**
  - Opening the picker and pressing Esc without confirming left the row at `default` and wrote no
    settings file. The observed value is caused by the selection, not by the file being present.
  - An earlier run whose cursor wrapped past entry 7 landed on `Explanatory`, confirmed it, and the
    row then read `Explanatory` on reopen. The row tracks the entry actually chosen.

  What this does not establish: the observation was made by automation reading a terminal, not by a
  human eye, and it covers one platform and the project-scoped directory rather than
  `~/.claude/output-styles/`. WINDOWS.md id 16's closure condition is written as a human
  observation; whoever owns that entry decides whether a captured render of the real picker
  satisfies it.

### 6. A cold read of README by someone who did not write it
expected: No two passages of README contradict each other; particular attention to the claim region against "## Status" and against the repository-layout tree.
result: issue
reported: "Two independent cold readers, converging. Three checkably-false statements in README, each contradicted by the repository's own committed files — including one that a mechanical cross-reference had examined and dismissed."
severity: major
evidence: |
  Two readers were run independently on the same brief. Findings below are only those re-verified
  against the repository; one reader finding was refuted and is recorded as refuted.

  **Confirmed, checkably false:**

  1. **README:231-233** — "Every number this README carries is sourced from a committed results
     file under `evals/`, states the model versions and the date it was produced, and is checked by
     `tools/check_repo.py`". The checker's own docstring says the opposite, in terms
     (`tools/check_repo.py`:405-415): "The region is bounded because README legitimately carries
     numbers that are not measured claims." The 31-rule count (:120), the 28 worked pairs (:125)
     and the 14 recorded observations (:127) are sourced from no results file, carry no model
     string and no date, and are checked by neither code. Both codes named in the same sentence are
     claim-region-scoped, so the machinery cited as proof cannot reach the claim it is cited for.
     This is the most serious of the three: it is an unqualified claim about the project's own
     evidence discipline, in a project whose stated constraint is measured claims or no claims.

  2. **README:139-140** — "`evals/routes/run_routes.py` — ... measures whether **the four install
     routes** deliver equivalent behaviour". The script's own docstring line 2 says "Route-
     equivalence measurement for Proof First's **three** distribution routes", and its constant is
     `ROUTES = ('skill-on', 'style-on', 'prompt-on')`. `RESULTS-routes.md`:3 says "36 sessions
     across **3** route(s)". README's own :104 says "the three routes".

  3. **README:131-133** — cites the superseded trigger figures. It reports "the recorded run: 9 of
     9 must-fire ... and 2 of 5 near-miss" as what `RESULTS-trigger.md` holds. That file records
     three runs; WINDOWS.md entry 24 states the 2026-09-20 n=1 observation "was superseded by the
     CAT-10 gap-closure round's paired n=5 measurement", and `RESULTS-trigger.md`:166 records that
     the shipped description "still measures `OF_B/SN_B = 9/25` over-fires at n=5". Arm B is the
     shipped configuration, so a current measurement of what ships exists and README does not carry
     it. Note the self-read recorded at LEGAL-REVIEW.md:378-384 reached this exact spot and
     dismissed it as Arm A, the reverted treatment. Arm A was correctly excluded; Arm B was the
     thing missed. That is precisely the failure mode WINDOWS id 17 describes — a reader checking
     their own text writes the checks that match what they meant.

  **Confirmed, minor:**

  4. :202 "one measured v1 limitation" against the trigger over-fire (:131-133) and the skill-on
     non-activation in 3 of 12 sessions (:108), both measured, both limitations, both disclosed.
  5. :7-8 "the one shared canonical deal brief this repository ships" against
     `evals/benchmark/bench-deal-brief.md`, which the layout tree asserts exists and which does.
  6. MOD-04 given two thresholds: "names its artifact family **before drafting**" (:135-136) versus
     "before its **first rule citation**" (:202-203). `run_conformance.py`:5 says "before its first
     rule marker", so :202-203 is the accurate one.
  7. "What exists today" omits `tools/generate_derivatives.py`, `.github/workflows/ci.yml`,
     `scenarios.json`, `proxy-sources.md` and `bench-deal-brief.md`, all asserted by the layout tree
     and all present. `generate_derivatives.py` is the sharpest: :240-248 instructs the reader to
     run it.

  **Refuted on verification, recorded so it is not re-raised:** one reader argued 96 generations /
  48 pairs / 16 cells cannot be consistent. It is consistent. Counted from the committed raw
  records: 2 models x 8 scenarios = 16 cells, x 2 conditions x 3 repeats = 96 generations, and
  16 x 3 = 48 pairs. The second reader recomputed independently and also found it clean. The claim
  region does not state the 3 repeats, which is what misled the first reader — an under-
  specification, not a falsehood, and not recorded as a gap.

### 7. The id-6 disposition and the PF-1 section hold up to a reader who did not write them
expected: |
  Round 2, against `LEGAL-REVIEW.md`:186-302 and `NUMBERING.md`. Gap G-06-2 was found by a reader
  who checked the disposition's premise against the registry next to it. 06-05 restated the
  reasoning; this test asks the same question of the restatement, by a reader who did not write it.

  Specifically: (a) is any sentence in the id-6 disposition falsifiable from `NUMBERING.md`, as the
  MEDDPPCC premise was; (b) do the prong-2 and prong-4 answers actually carry the conclusion, or do
  they restate the question; (c) the PF-1 section reaches "left open" — is leaving it open the
  honest reading of its own argument, or is it a finding dressed as an open question.
result: issue
reported: "Two independent readers. The id-6 restatement is materially better and its own correction paragraph miscounts; the PF-1 section's load-bearing counterweight is false against three shipped files, and the error propagates into the ledger and into What remains open."
severity: major
evidence: |
  **(a) The PF-1 counterweight is false against three shipped files — the most serious of the six.**
  `LEGAL-REVIEW.md`:289-291 states "the list appears in an internal ID registry rather than in
  `SKILL.md`, the output style or the system prompt — nothing a reader of the shipped skill sees
  names these seven elements as a set in this order." All three named files carry the identical
  sentence, naming all seven as a set, in exactly the table's order, under the framework's name:

      skills/proof-first/SKILL.md:63
      output-styles/proof-first.md:87
      prompts/system-prompt.md:75
      "The Command of the Message spine is carved into seven sub-blocks, each reserved four IDs:
       Before scenario, After scenario, Required Capabilities, Metrics, Proof Points,
       Differentiators, and Positive Business Outcomes."

  The section enumerates the three surfaces one by one and is wrong on all three. `:299-301` inherits
  it — "the exposure ... is confined to `NUMBERING.md` ... since no shipped file cites them" — and so
  do `## What remains open` item 5 (`:383-384`, "frozen in `NUMBERING.md`") and ledger row 29
  (`:628`, "in NUMBERING.md"). This is the counterweight that justifies leaving id 29 open rather
  than acting, and the remedy it prices is understated: renaming touches `NUMBERING.md` and
  `SKILL.md` plus a `generate_derivatives.py` run, not one file.

  **(b) The correction paragraph miscounts, falsifiable from `NUMBERING.md` directly.** `:204-207`
  says Decision Criteria/Decision Process and Champion/Competition "both give" their letter, "so
  four of the eight positions could be swapped with no change to any spelling." `NUMBERING.md`:77-78
  is `Paper Process` then `Pain` — a third same-initial pair. The count is six, not four. The same
  paragraph spells M-E-D-D-P-P-C-C one sentence earlier (`:203`) and then omits the P pair from the
  list it is enumerating. The defect is inside the paragraph whose job is correcting a wrong premise,
  and commit 0b8a865's own message repeats the undercount.

  **(c) `:236-237` "block headings in `completeness-audit.md`" is false.** Neither "Economic Buyer"
  nor "Paper Process" occurs anywhere in `skills/proof-first/references/completeness-audit.md`;
  its headings are MC ids plus rule titles. Repo-wide the two strings appear only in `NUMBERING.md`,
  `check_repo.py` fixtures and `LEGAL-REVIEW.md` itself. The sentence exists to show the two conceded
  prong-4 terms have a second, more exposed home, and the second home does not exist. Note the true
  fact is narrower and better for the entry than the false one.

  **(d) `:268` cites `NUMBERING.md`:26-40 for the PF-1 carve-up.** The heading is at `:31`, the prose
  at `:33-35`, the table at `:37-45`. Line 26 is a PF-2 row of a different table, and the cited span
  ends at "After scenario", excluding five of the seven elements the same sentence then enumerates.
  Both readers found this independently. The same wrong range was carried in round 1's own evidence
  for test 2 — the error propagated from the finding into the fix.

  **(e) `:296` "are the same two live questions id 6 ends on" is contradicted by the same file.**
  `## What remains open` lists them as separate items: item 5 (`:383-387`) is registry-counts-as-
  shipping plus prong-4-attribution-vs-renaming; item 6 (`:388-390`) is MC expression thinness plus
  where Economic Buyer and Paper Process sit. Different pairs. The claimed equivalence is what
  licenses "open" rather than "closed" for id 29.

  **(f) `:16` declares the file append-only — "later reviews add sections, they do not rewrite
  earlier ones".** Commit 0b8a865 removed 32 lines and added 64, rewriting the id-6 section in place;
  the falsified acronym reasoning is gone from the file. Its substance survives in the "Correcting
  the earlier reading first" paragraph, so the record is not lost — but the file's own rule was not
  followed, and the header says so ("the earlier entry's reasoning corrected").

  **What the restatement got right, recorded so the improvement is not lost.** All four `SOURCES.md`
  prongs are now applied or explicitly excluded by name. The false MEDDPPCC premise is stated as
  corrected rather than quietly dropped, and `NUMBERING.md`:9-13 now carries the M-E-D-D-P-P-C-C
  correction itself. Prong 4 concedes "Economic Buyer" and "Paper Process" sit on the prong rather
  than finding them off it, and records the choice not to rename. The 2026-04-21 ruling paragraph is
  bounded to the trademark question. Reader 1 verified the eight names, the MC-1..MC-40 span, the
  deal-brief grounding of all eight audit questions, and the ruling/docket facts as accurate.

  **Reasoning critiques, recorded as observations rather than gaps** (not checkably false; see the
  prose-gap stopping rule): prong 2 rests on a thinness/merger judgement `SOURCES.md` does not
  contain, and its one argumentative clause ("many independent publishers") is an unrecorded lookup;
  prong 4 concedes the prong is met and then records position instead of disposing, which is
  disclosure substituted for justification against `SOURCES.md`:16's "and none of them ships";
  prong 1 answers a narrowed question ("sentence-level wording"); and `:277-279` spends an acronym
  defence that `:202-208` retracted forty lines earlier.

### 8. LEGAL-REVIEW.md's reduced read states no legal conclusion
expected: |
  Round 2, against `LEGAL-REVIEW.md`. Read the file's headings, bolded lead-ins and the ledger's
  Disposition column **alone**, skipping every line of prose. Nothing in that reduced read should
  state a legal conclusion about this repository's exposure.

  This is gap G-06-3's own test, re-run against the corrected file by a reader who did not make the
  corrections. Two specific things to judge rather than confirm: whether `Gate status: PASSED`,
  still present because `source-gate-incomplete` requires it, now reads as the narrow machine-checked
  fact the surrounding section says it is; and whether `Closed on reasoning` reads as an honest
  fourth state or as a softer word for the same closure.
result: pass
evidence: |
  Independent reader's verdict on the test as written: **the reduced read states no legal conclusion.**
  Not one heading, bolded lead-in, Disposition cell or standalone line asserts that this repository
  does or does not infringe. Every heading names a subject, every bolded lead-in names an act
  (`Read`, `Confirmed`, `Changed`, `Not performed`, `Ledger effect`), and every Disposition cell
  names a ledger state rather than a legal one. Strictly parsed, the skim yields an activity log.

  **The two things the test asked to judge rather than confirm:**

  - `Gate status: PASSED` — the move below the disclaimer did not fix what it was meant to fix. The
    reader: "Moving it down did not fix the problem; it produced exactly this reader." It is still a
    bare all-caps standalone line under a heading that promises findings, and its entire narrowing
    lives in prose the reduced read skips. Recorded as an observation, not a gap: the narrowing IS
    present, adjacent, and correct, and `source-gate-incomplete` requires the token.
  - `Closed on reasoning` — read as an honest fourth state. The reader folded it into the resolved
    bucket when counting impressions but did not find it a softer word for the same closure, and the
    `:582-595` definitions plus the named `WINDOWS.md` schema divergence were not challenged.

  **The residual, recorded and not actioned.** The reader's own summary: "the document does not lie
  to the skimmer. It just loses to them." Its honest position is carried by prose, while its
  structure hands a skimmer a PASS and a ledger where 20 of 29 rows end in a word meaning resolved.
  The one element signalling a live copying question — "This is the prong that engages" — is inline
  body text, so the three prongs that do not apply look identical to the one that does in a skim.
  Against that, the caution signals that do survive the skim are real: "This record is not legal
  advice and never becomes it.", "The per-rule reproduction judgement is permanent, not closable.",
  nine `Open — v2` cells, and `Decision: DEFER PUBLICATION.`

  One reader claim checked and partly refuted: `**Result: no checkably-false statement found.**`
  (`:495`) was called a stale bolded verdict outranking its own correction. Its heading — which the
  reduced read includes — is `### 2. Cold read of README — NOT PERFORMED AS A COLD READ AT 06-02
  (superseded by § 4)`. The supersession is disclosed in an element the reduced read reads, so this
  is a salience judgement, not a stale statement. Not recorded as a gap.

### 9. A cold read of the corrected README finds no checkably-false statement
expected: |
  Round 2, against `README.md`. Gap G-06-6 was three false statements found by two independent
  readers while all ten CI commands were green. 06-05 corrected them and self-checked. A reader who
  did not write the corrections reads README against the committed files and reports any statement
  that a file in this repository contradicts.

  Two known places to press, recorded so they are not rediscovered as new: the rewritten
  evidence-discipline paragraph at :232-247, which now makes a scoping claim about which numbers
  are enforced, and :109's activation contrast — "was not in 3 of its 12 sessions, while the output
  style and the pasted prompt are unconditionally on once selected" — where
  `evals/routes/RESULTS-routes.md`:15-17 reads style-on 11 of 12 and prompt-on 8 of 12. The second
  is already recorded as a placement judgement rather than a falsehood; a cold reader deciding
  otherwise is the finding.
result: issue
reported: "Two independent cold readers, converging on four statements; three more found by one reader each and one by the session. Seven checkably-false statements in total, each contradicted by a committed file — including one the 06-05 gap-closure round created, and one in the paragraph 06-05 rewrote to fix this exact defect class."
severity: major
evidence: |
  Two readers on the same brief, independently, as in round 1. Findings below are only those
  re-verified against the repository. Convergence is noted per item.

  **1. README says the `/config` picker has not been observed; this round's own record says it was.
  Created by 06-05.** `README.md`:86-88 — "That a Claude Code session then lists it in `/config` has
  not been observed here" — and `:89-91` — "the picker is the one link in this route nothing here
  exercises." `LEGAL-REVIEW.md`:536-541 records the observation with date, platform, harness version,
  entry position and two controls; ledger row 16 (`:615`) repeats it. Commit 36fbf6c wrote the
  observation into `LEGAL-REVIEW.md` and left README asserting the opposite. (Reader 5.)

  **2. Three shipped files still state that no benchmark has run.**
  `skills/proof-first/references/artifact-patterns.md`:144 — "no benchmark has run, and this
  repository makes measured claims or none" — carried verbatim into `output-styles/proof-first.md`:695
  and `prompts/system-prompt.md`:683. `README.md`:187 and `evals/benchmark/RESULTS.md`:1 record 96
  generations measured 2026-09-18. This is the only finding of the round that ships to an installed
  user. The guard for exactly this regression exists and matches a different literal:
  `tools/check_repo.py`:4264, `STALE_COMPARISON_CLAIM = 'No benchmark has compared'`. (Both readers.)

  **3. `README.md`:134 "three runs against the shipped skill description."**
  `evals/trigger/RESULTS-trigger.md`:101 records Arm A as a 551-character description, head-14 sha256
  `9049c7d8…`, against the shipped `d5dd651a…` carried by the other two runs, and `:152-156` records
  it reverted. Two of three, not three. README's own `:139-140` says so five lines later. (Both
  readers, and found independently by this session before either returned.)

  **4. `README.md`:43-44 — `publish-location-drift` "fails the build if any command or manifest
  carrying it stops agreeing with the others."** `tools/check_repo.py`:724-726 declares the opposite
  in terms: "it also compares owner segments only, so a repository-name-only drift under an unchanged
  owner is not detected." `_publish_locations_in` (`:3620`) returns owner segments. A carrier whose
  repo half drifts has stopped agreeing and the build still passes. (Both readers.)

  **5. The benchmark's sessions are not prompted with `bench-deal-brief.md`.** `README.md`:171-172
  ("the separate deal brief the benchmark's sessions are prompted with") and `:9-10` ("used only to
  prompt the benchmark's sessions"). `evals/benchmark/run_benchmark.py`:295 sends
  `scenario['prompt']` and nothing else; the brief is read exactly once, inside `--self-test` at
  `:1646`, to assert entity disjointness. "Thornfield", the brief's buyer, appears 0 times in
  `scenarios.json` and 0 times across the 96 committed raw records. The brief's own `:9` states the
  accurate relation — "it grounds Phase 5's benchmark scenarios". The separation half of README's
  claim does hold. (Both readers.)

  **6. `README.md`:264-265 claims codes check the inventory counts; none reads them. Same defect
  class as G-06-6 #1, reintroduced in the paragraph rewritten to fix it.** The sentence: "Different
  codes check those — `catalog-count-mismatch`, `readme-layout-tree-stale` and their neighbours read
  the counted artefact and compare." `catalog-count-mismatch` (`check_repo.py`:198-202) compares a
  `skills/*/SKILL.md` stated count against `NUMBERING.md`; it never opens README. Settled by mutation
  probe against an unmutated sibling control, both from `git archive HEAD`:

      control (unmutated):  check_repo: 0 violations   rc=0
      mutant (README 31-rule->37-rule, 31 rules->37 rules, 28 worked->44 worked, 4 replacements):
                            check_repo: 0 violations   rc=0

  The checker is green over the defect the sentence claims it catches. (Reader 5; probe by this
  session.)

  **7. The activation contrast at `README.md`:111-112.** "The installed skill has to be triggered and
  was not in 3 of its 12 sessions, while the output style and the pasted prompt are unconditionally
  on once selected." The 3-of-12 figure comes from `evals/routes/RESULTS-routes.md`:15's Activation
  column, whose metric is `run_routes.py`:487, `MARKER_RE.search(text)` over output text. On that
  same metric `prompt-on` scores 8 of 12 (`:17`) — worse than skill-on's 9 of 12 — immediately after
  README names it unconditionally on. Round 1 recorded this as a placement judgement rather than a
  falsehood; test 9's own text named "a cold reader deciding otherwise" as the finding, and reader 4
  decided otherwise. Recorded as confirmed on that instruction. (Reader 4.)

  **8. `evals/benchmark/bench-deal-brief.md`:10-12 still asserts an expired premise.** "This
  environment has no live network access, so the name-collision web search ... could not be repeated
  here for this brief's names; that is an open, disclosed unrun-verify item, not a completed check."
  `LEGAL-REVIEW.md`:617, ledger row 18, books that same search **Fixed**: "Closed by 06-02's
  searches; the premise that this environment has no network had expired." Two committed files, one
  open and one closed on the same item. (Found by this session; neither reader was pointed at that
  file.)

  **Recurring under-specification, recorded not actioned.** `README.md`:188 "Each scenario was
  drafted twice" against `evals/benchmark/RESULTS.md`:214 "each cell above is measured at 3 repeats".
  Round 1 adjudicated this as under-specification rather than a falsehood after it misled a reader;
  round 2 readers split on it again, one calling it compressed phrasing and one a contradiction. Two
  rounds of readers have now tripped on the same unstated factor. Not recorded as a gap, on round 1's
  adjudication, but the repeat is the evidence that stating the 3 repeats would be cheaper than
  defending the omission a third time.

  **What both readers verified as consistent, recorded so it is not re-checked.** 31 rules across
  SKILL.md / NUMBERING.md / checklist.md; 28 worked pairs; 8 MC dimensions with initials
  M-E-D-D-P-P-C-C; the before/after pair reproduced character-for-character from
  `examples/before-after.md`; every claim-region benchmark figure against `RESULTS.md` including the
  16-cell 8/1/7 split and the both-models direction, recomputed by hand by both readers; the
  conformance figures, CR-01 and the 03-15 disposition section; Arm B's 45/45 and 9/25; the routes
  run's 36 sessions and overlapping ranges; every one of the layout tree's paths existing on disk;
  stdlib-only imports across all eight Python files; and the ten CI commands in `ci.yml`.

### 10. The reproduction-boundary material holds up to readers who did not write it
expected: |
  Round 3, against `LEGAL-REVIEW.md`'s MEDDICC/MEDDPICC and PF-1 material and the ledger rows and
  `## What remains open` items that depend on it. Gap G-06-7 was six checkably-false statements found
  by two readers; 06-06 corrected all six. This test asks the same question of the corrected file, by
  readers who did not make the corrections: is any sentence in that material falsifiable from another
  committed file, and do the stated conclusions follow from the reasons given?
result: issue
reported: "Two independent readers, converging on five of seven. The six corrections from round 2 all hold and were verified as accurate. Seven different checkably-false statements survive in the same material — five of them in text 06-05 wrote that round 2 did not reach, one in the sentence 06-06's own self-audit commit wrote, and one spread across three places that disagree with each other. The worst is that the file's prong-4 classification of the eight MC names is the opposite of the classification this repository's own checker enforces."
severity: major
evidence: |
  **1. The prong-4 six/two split is the opposite of what `check_repo.py` enforces. (Both readers.)**
  `LEGAL-REVIEW.md`:249-252 — "Applied honestly, the eight split. "Metric", "Pain", "Champion",
  "Competition", "Decision Criteria" and "Decision Process" are ordinary business English that stands
  on its own outside this framework family. "Economic Buyer" and "Paper Process" are not". And
  `:308` — "They are not neutral English the way "Metric" or "Competition" are."

  `tools/check_repo.py`:2952-2965 freezes the same eight strings one-and-seven the other way:

      SOURCE_COINED_LABELS = (
          # ... The ordinary-English
          # word for a measurement ('metric') is deliberately excluded ...
          'economic buyer', 'paper process', 'decision criteria',
          'decision process', 'champion', 'competition', 'pain',
      )

  `metric` is the only one of the eight this repository treats as ordinary English. Five strings the
  review calls ordinary business English — pain, champion, competition, decision criteria, decision
  process — are strings `check_source_label_in_skill_content` (`:2977-3009`) makes a build failure in
  shipped skill content, on the stated ground that they are source-coined. `:308` names "Competition"
  as the example of neutral English; `:2963` names it in the coined tuple. The split is the load-
  bearing step of the prong-4 disposition, and the repository's own enforcement code contradicts it.

  **2. The occurrence enumeration is false against two committed files, and miscalls a production
  constant a fixture. (Both readers.)** `:253-256` — "they are index terms in `NUMBERING.md`'s
  registry and nowhere else that ships ... across the shipped tree the two appear only in
  `NUMBERING.md`, in this file, and in `check_repo.py`'s fixtures."

      examples/deal-brief.md:75          ### Economic buyer stated priorities
      examples/deal-brief.md:89          ### Paper process
      examples/deal-brief.md:26          ... Chief Financial Officer, the economic buyer.
      evals/benchmark/bench-deal-brief.md:130   ### Economic buyer stated priorities
      evals/benchmark/bench-deal-brief.md:145   ### Paper process
      evals/benchmark/bench-deal-brief.md:54,185  ... the economic buyer ...

  The case defence is unavailable: this repository's own matcher for these exact labels is
  `re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)` (`check_repo.py`:2974). Both files ship —
  `README.md`:141 calls `examples/deal-brief.md` "the one canonical fictional deal every worked
  example cites", and the same `LEGAL-REVIEW.md` entry leans on it at `:230-231`. Separately,
  `check_repo.py`:2958-2959 is `SOURCE_COINED_LABELS`, the module-level constant the production check
  reads — not a fixture; and "Paper Process" occurs in no fixture in that file at all, only at
  `:2959`. The sentence at `:259-260` calls this "a narrower fact ... better for this entry than the
  one it replaces". The narrower fact is itself wrong, and it was written by commit a18f492 — 06-06's
  own self-audit, titled "correct two statements this round's own self-audit falsified".

  **3. Prong 2 reinstates the mnemonic the correction fifteen lines above retired. (Both readers.)**
  `:224-225` — "the prong has to be answered on that footing rather than on a mnemonic that the
  shipped block names do not spell." `:239` — "and organised around a mnemonic: at that thinness, the
  expression and the idea it organises are hard to separate". `:301` reinstates it a second time as
  the contrast that makes PF-1 stronger than id 6 — "The MC blocks could at least be argued to follow
  a mnemonic that many publishers teach". The correction exists to remove that ground; two later
  passages spend it anyway.

  **4. `NUMBERING.md` does not declare what `:298-299` says it declares. (Both readers.)**
  "It is a source's ordered list, in that source's order, and `NUMBERING.md` says so in its own words.
  Id 6 at least had to be argued into that description; this one declares it." `NUMBERING.md`:33-35
  says "carved into seven named sub-blocks, one per Command of the Message element" — a one-to-one
  correspondence of labels. Nothing in `:31-54` addresses whose order the table is in; the remaining
  prose is slot arithmetic. The contrast is available in the repository:
  `completeness-audit.md`:12-15 does address order provenance for the MC side and declines to concede
  it. No equivalent sentence exists for PF-1 in either direction. This is the entry's first and
  strongest ground for ranking PF-1 above id 6.

  **5. The rename cost is stated three times and counted two ways, and neither matches the tree.
  (Both readers, and found independently by this session before either returned.)** `:340-342` —
  "it costs three files rather than one — `NUMBERING.md`, `skills/proof-first/SKILL.md`, and a
  `python3 tools/generate_derivatives.py` run" — enumerates two files and one command and calls it
  three files. `:433` and `:731` both say "three files and a regeneration", making the regeneration an
  addition to three rather than one of them. The tree gives four: `git grep -l "Positive Business
  Outcomes"` returns `NUMBERING.md`, `skills/proof-first/SKILL.md`, `output-styles/proof-first.md`,
  `prompts/system-prompt.md` — two hand edits and two regenerated files, all four of which must be
  committed because `generate_derivatives.py --check` compares against the committed files.

  **6. "nowhere else that ships" uses a sense of "ships" `README.md` denies. (Reader 3.)** `:253`
  presupposes `NUMBERING.md` ships. `README.md`:367-369 — "`NOTICES.md`, `SOURCES.md`,
  `NUMBERING.md`, `examples/`, `tools/`, and `evals/` stay at the repository root and never ship to
  an installed user." Four lines later the same passage uses "the shipped tree" to include
  `NUMBERING.md`, `LEGAL-REVIEW.md` and `check_repo.py`, none of which ship on README's definition.
  Two incompatible senses in one passage, and the repository contradicts the first.

  **7. Prong 2's stated basis contradicts prong 4's stated finding, thirteen lines apart. (Reader 4.)**
  `:237` — "Eight blocks, each labelled with the shortest ordinary English for the thing it covers".
  `:250-252` — ""Economic Buyer" and "Paper Process" are not — both are terms of art this family put
  into circulation, and both are adopted here verbatim as block labels." Both cannot describe the
  same eight labels.

  **What the round-2 corrections got right, verified and recorded so the improvement is not lost.**
  Both readers checked all six and found all six correct. The PF-1 counterweight now names
  `SKILL.md`:63, `output-styles/proof-first.md`:87 and `prompts/system-prompt.md`:75, and all three
  carry the byte-identical seven-element sentence (reader 3 verified the bytes). The swappable-
  position count is six and recomputes from `NUMBERING.md`:73-80's three same-initial pairs. The
  `completeness-audit.md` claim is true and is mechanically enforced. The `NUMBERING.md`:31-45
  citation resolves. `:296`'s equivalence claim is gone and items 5 and 6 are described as separate.
  The append-only rule at `:16-24` now states the correction exception with its conditions. Reader 3
  additionally recomputed every ledger count (32 entries; 9 fixed, 2 closed on reasoning, 9 waived,
  12 open) row by row and found them right, and confirmed the six `SOURCES.md` rows all read verified.

  **Reasoning critiques, recorded as observations rather than gaps** (not checkably false; prose-gap
  stopping rule): prong 2's "many independent publishers" clause is a premise recorded in no committed
  file — `SOURCES.md`:41-44 lists two sources for this family — and it is the clause that converts a
  conceded reproduction into a thin one (both readers, independently, and it survives from round 2's
  own backlog); `:56` says the section "ends on two live questions" while items 5 and 6 carry three
  between them (reader 3); `:39`'s bolded "Content items still needing a decision: 2" excludes id 29,
  which `:344-345` classifies as a change to shipped content awaiting a version decision, though the
  prose at `:54-57` discloses it separately and the two name-collision items are the ones routed
  "before wider distribution" (reader 3); prong 4 still records position instead of disposing, which
  the ledger concedes at `:733` (both readers); and `:254-255`'s "its headings are MC ids plus rule
  titles" is true of the eight `###` headings but not of the file's `#` and `##` headings (reader 4).

### 11. A cold read of the corrected README finds no checkably-false statement
expected: |
  Round 3, against `README.md`. Gap G-06-9 was eight false statements found by two readers and this
  session; 06-06 corrected all eight and added a checker code for the one that shipped. This test
  asks the same question of the corrected file, by readers who did not make the corrections.
result: issue
reported: "Three independent readers converged on one statement — and it is a claim 06-06 newly imported into README while correcting a different false claim about the same file. Every one of round 2's eight corrections holds. One further reader finding was adjudicated against 2-to-1 and is recorded as an observation."
severity: major
evidence: |
  **1. README says the two deal briefs share no figure. They share one, byte for byte. (Readers 1, 2
  and 5, independently.)** `README.md`:9-11 — "`evals/benchmark/bench-deal-brief.md` is a second,
  separate brief, which grounds the benchmark's scenarios and shares no company, person, platform or
  figure with the one the examples are written against."

  The two briefs' `Canonical figures` tables — each declared by its own file to be the registry of
  every figure it owns — carry an identical row:

      examples/deal-brief.md:116               | rfp-security-weight | 20% | percent | Weight the
      evals/benchmark/bench-deal-brief.md:177    buyer's top-level scoring rubric assigns to the
                                                 security section of the response |

  Same key, same value, same type, same description. `comm -12` over the two files' table rows
  returns it and nothing else substantive. Both decision-criteria tables also read
  `| Security posture | 20% |` (`examples/deal-brief.md`:87, `bench-deal-brief.md`:143). Every other
  same-named key was deliberately varied — technical 55%/50%, commercial 25%/30%, legal-review-days
  10/8, security-review-days 15/12 — which is what makes the one that was not a slip rather than a
  policy. The company, person and platform thirds of the claim do hold; reader 1 checked all nine
  invented names and the platform lists.

  `evals/benchmark/bench-deal-brief.md`:8 has carried this claim about itself since 05-02
  (commit 1577910). What is new is that commit 3a37839 — 06-06's fix for round 2's finding 5, titled
  "correct what bench-deal-brief.md is for" — replaced README's old sentence, which made no such
  claim, with one that imports it. The round that closed G-06-9 opened this.

  **Adjudicated against, recorded so it is not re-raised as new.** Reader 1 called `README.md`:186-188
  false — "`run_benchmark.py --self-test` is the only place it is read at run time, to assert it
  shares no named entity with `examples/deal-brief.md`" — because `run_benchmark.py`:1645's
  `shared_deal_brief_entities` tuple holds four strings while `examples/deal-brief.md` invents nine.
  Readers 2 and 5 each examined the same sentence against the same code and listed it as accurate.
  The tuple's scope is a real and understated limit, and it is the same class as round 2's
  `publish-location-drift` finding, which was recorded as a gap and closed by bounding the sentence.
  Recorded here as an observation on the 2-to-1 split rather than a gap, with the bounding edit
  carried to backlog. The substantive property holds today: none of the other five names appears in
  the bench brief.

  **What all three readers verified as consistent, recorded so it is not re-checked.** Every one of
  round 2's eight corrections: the `/config` observation at `:90-98` against `LEGAL-REVIEW.md`:582-594
  including its two controls and three stated limits; `:44-46`'s publish-location ceiling against
  `check_repo.py`:703-727; `:146-154`'s "three runs, two of them against the shipped skill
  description" against the three head-14 hashes; `:184-188` on what the bench brief is for;
  `:279-284`'s inventory-enforcement paragraph, with both readers independently enumerating every
  function in `check_repo.py` that opens README and finding none that reads a stated count;
  `:121-123`'s three activation figures 9/11/8 of 12; and the "no benchmark has run" sentence gone
  from `artifact-patterns.md` and both derivatives. Beyond those: all 40 layout-tree paths exist;
  the reproduced before/after pair is character-for-character `examples/before-after.md`:12-15; the
  31-rule and 28-pair counts recompute from the files; every claim-region figure against
  `RESULTS.md`, with both readers re-summing the 48-row per-cell table to the pooled 45/1/2, 32/3/13
  and 7/3/38 totals and recomputing the 8/1/7 sixteen-cell split and the both-models direction by
  hand; the conformance 3/10 and 4/10 against `RESULTS-mod04.md`:760 and :776, with reader 2
  re-tallying all 23 committed run blocks; the 439-character description length, counted; and the ten
  CI commands in `ci.yml`.

### 12. No two committed files in the repository state things that cannot both be true
expected: |
  Round 3, new this round. Rounds 1 and 2 pointed every reader at a named file, so a contradiction
  between two files neither brief named could not be found. This reader was pointed at no file: find
  any two committed files that cannot both be true, with attention to whether a measurement has been
  performed, to counts, and to what a script's prose says against what its code does.
result: issue
reported: "Three checkably-false statements, none in a file any previous round's brief named. One is the expired no-network premise surviving in the file a companion explicitly routes the reader to — in the round whose own commit was titled 'sweep the expired no-network premise out of the tracked tree'."
severity: major
evidence: |
  **1. The expired no-network premise survives in `evals/lint.py`, and `proxy-sources.md` sends the
  reader to it.** `evals/lint.py`:98-100, in the module docstring's declared ceiling for
  `proxy-term-source-is-internal` — "it does not and cannot confirm a live http(s) URL actually
  serves the content the registry claims (see ceiling 2 above -- **this environment has no live
  network access**)." `evals/proxy-sources.md`:12-14 — "The reason given when this file was written
  was that the environment had no live network access. That premise has since expired —
  `LEGAL-REVIEW.md`'s ledger row 18 records where — and `SOURCES.md`'s own rows were re-confirmed
  against live pages on 2026-09-21". And `evals/proxy-sources.md`:37-38 — "See `evals/lint.py`'s
  module docstring for the full statement of this ceiling."

  The file that records the premise as expired points the reader at the file that still asserts it.
  Three further files agree the premise expired: `LEGAL-REVIEW.md`:720 (ledger row 18, **Fixed**),
  `bench-deal-brief.md`:16-17, and `check_repo.py`:3776-3779. Commit 467ed6e, 06-06 task 8, is titled
  "sweep the expired no-network premise out of the tracked tree"; `git grep` for the premise now
  returns `lint.py`:99 alongside the three files that disclaim it.

  **2. Ledger row 28 miscounts the route report's limits.** `LEGAL-REVIEW.md`:730 — "Measured null
  result published with its **four** named limits." `evals/routes/RESULTS-routes.md`:45-50 publishes
  six bullets, and `evals/routes/run_routes.py`:183-190 freezes `REQUIRED_CAVEATS` at exactly six
  keys with one bullet rendered per key, so the file structurally cannot publish four.

  **3. `run_conformance.py` says it cross-checks three committed fixtures; it enumerates five and
  five are committed.** `:22-23` — "Offline proof that the scorer discriminates **the three
  committed** transcript fixtures correctly" — and `:313-315` — "It then cross-checks the three
  committed transcript fixtures (conformant-family-first.txt, nonconformant-no-family.txt,
  nonconformant-rule-before-family.txt) if present", naming them exhaustively. `:459-465`'s
  `fixture_expectations` holds five, including the two `-late-phrase` fixtures the same docstring's
  own cases 8 and 9 describe, and `ls evals/conformance/transcripts/` returns all five.

  **What this reader checked and found consistent, recorded so it is not re-checked.** The PF and MC
  registries across `NUMBERING.md`, `SKILL.md`, `checklist.md` and `completeness-audit.md` — 31 PF
  IDs, 8 MC IDs, identical ID sets in all three, and the PF-1 seven-by-four arithmetic; the
  derivative triple, with `output-styles/proof-first.md`'s body line-for-line identical to
  `prompts/system-prompt.md` and both carrying the same stamp digest and source list; both stale-claim
  guards satisfied by the current text; the 96 generation records and 96 judge records on disk;
  `DECISION-RULE-cat10.md`'s Clopper-Pearson and Fisher tables recomputed by hand against `stats.py`,
  including `p_attr = 0.0016`; `INIT-EVENTS.md`'s 70+70 sessions against the committed tarball; and
  `RESULTS-mod04.md`'s 23 run blocks re-derived arm by arm.

### 13. The reproduction-boundary material holds up after the round-3 corrections
expected: |
  Round 4, against `LEGAL-REVIEW.md`'s MEDDICC/MEDDPICC and PF-1 material. Gap G-06-10 was seven
  checkably-false statements; 06-07 corrected all seven and adopted `check_repo.py`'s frozen
  seven-of-eight source-coined split in place of the file's own six-and-two. This test asks the same
  question of the corrected file, by two readers who made none of the corrections.
result: issue
reported: "Two independent readers. All seven round-3 corrections hold and the adopted split is verified accurate. Ten different checkably-false statements, nine of them authored by the correcting commit itself — including an enforcement claim naming a check that never opens two of the four files it is offered for, a sentence quoted from SKILL.md that is not in SKILL.md, and the same file cited as both a rename target and a sentence the rename leaves untouched."
severity: major
evidence: |
  **1. The "mechanically held" claim names a check that never opens two of the four files. (Readers 3,
  4 and 6 — all three who could reach it, plus this session independently before any returned.)**
  `LEGAL-REVIEW.md`:288-291 — "Not `skills/proof-first/SKILL.md`, not any `references/*.md`, not
  `output-styles/proof-first.md`, not `prompts/system-prompt.md`. This is not an observation, it is
  mechanically held: `source-label-in-skill-content` fails the build on any of the seven in that
  content, and it is green."

  `tools/check_repo.py`:983 is `SKILL_GLOB = 'skills/*/SKILL.md'`, and the check's candidate set
  (`:2991-2996`) is that file plus the `references/*.md` beside it. It never opens either derivative,
  and its own docstring says so at `:302-305`. The underlying fact is true — zero hits for all seven
  across `skills/`, `output-styles/` and `prompts/` — but for two of the four named files it is
  exactly what the sentence denies it is: an observation. `:322-323` then rests the disposition on it
  ("the first is now mechanically enforced rather than observed"). The derivatives *are* covered, but
  transitively and by a different mechanism — `generate_derivatives.py --check` byte-compares them to
  sources that are scanned — and that is a two-step argument the sentence does not make. Reader 4
  added a live ceiling neither the checker nor the entry records: `check_repo.py`:2999 scans
  `strip_fences(...)`, so a label inside a fenced block in `SKILL.md` would reach both derivatives
  unseen. Presently moot — no file under `skills/proof-first/` contains a fence.

  **2. A sentence quoted from `SKILL.md`:63 is not in `SKILL.md`. (Readers 3, 4 and 6.)**
  `:435-438` — "`NUMBERING.md`:33-35 and `skills/proof-first/SKILL.md`:63 both state the seven
  sub-blocks are "one per Command of the Message element"". `SKILL.md`:63 says "carved into seven
  sub-blocks, each reserved four IDs: Before scenario, …". The quoted phrase occurs only at
  `NUMBERING.md`:33-34, and nowhere in `skills/`, `output-styles/` or `prompts/`.

  **3. The same line is cited as both the rename's target and what the rename leaves in place.
  (Reader 4.)** `:426` names `skills/proof-first/SKILL.md`:63 as one of the two files a rename edits
  by hand; `:436-439` names the same line as one of the "two sentences" left "in place". Both cannot
  hold. The substance fails too, and in the direction that matters: in `SKILL.md`:63 the source-naming
  clause and the seven labels are one sentence, so a rename necessarily rewrites it. The
  "independently of what the labels are called" property holds for `NUMBERING.md`:33-35, where the
  correspondence sentence and the table are separate, and fails for the one shipped file. It
  propagates into `## What remains open` item 5.

  **4. The stated provenance of "four files" returns five. (Readers 3, 4 and 6.)** `:429-431` — "The
  count is `git grep -l "Positive Business Outcomes"` over the tracked tree outside `.planning/`, not
  an estimate." That command now returns `LEGAL-REVIEW.md`, `NUMBERING.md`,
  `skills/proof-first/SKILL.md`, `output-styles/proof-first.md`, `prompts/system-prompt.md` — five,
  because `LEGAL-REVIEW.md`:387 and `:430` carry the string, the second of them inside the quoted
  command. The four-file cost is right; the sentence asserting the number *is* that command's output
  is not. The passage was corrected once already for this class three lines later.

  **5. The by-hand citation under-cites its own file. (Reader 4.)** `:426` cites `NUMBERING.md`:39-45.
  `NUMBERING.md`:48 also carries a label — "six elements would get three slots and Positive Business
  Outcomes (the" — so a rename must edit line 48 too.

  **6. "All three parts were wrong" is wrong about two of the three. (Reader 3.)** `:297-300` says the
  earlier draft's "only in `NUMBERING.md`, in this file, and in `check_repo.py`'s fixtures" had "all
  three parts wrong". "In this file" was correct. "In `check_repo.py`'s fixtures" was correct for
  Economic Buyer — `check_repo.py`:7000-7004 inserts that exact label into a fixture as the firing
  case, and it recurs at `:7029`, `:7036`, `:7051`, `:7059`. What failed was the word **only**. The
  two supporting sub-claims the correction offers are both true and both verified; they just do not
  establish what the sentence says they establish.

  **7. The correction-count in the append-only rule is stale. (Reader 4.)** `:23-26` — "Three
  corrections in this file were made on that basis", listing three from 2026-09-21. Eight lines in the
  file now carry 2026-09-22 corrections from 06-07, six of them in the reproduction-boundary material,
  and the ledger names the round at `:811` and `:836`. By the paragraph's own definition these are
  corrections "on that basis", and neither the count nor the date list covers them.

  **8. "not ordinary English at all" is not what the checker's split says. (Reader 4.)** `:245-247`
  justifies removing prong 2's premise on the ground that "the prong-4 finding below is that seven of
  the eight are not ordinary English at all". The prong-4 finding (`:280-282`) says the seven are
  *source-coined*, which is a different claim, and `check_repo.py`:2955-2957 excludes `metric` for a
  narrower reason — MC-1 and the integrity rules use that word legitimately — saying nothing about the
  other seven being non-English. The same entry supplies the counter-evidence five lines later, at
  `:291-298`, by recording five of the seven in ordinary use as English headings and role designations.

  **9. The checker is misquoted inside quotation marks. (Reader 4.)** `:48` — "only whether the **list**
  it declares a pass over is complete". `check_repo.py`:2131-2133 says "only whether the **file** it
  declares a pass over is complete". Small, and it is the sentence licensing the gate token above the
  reproduction-boundary summary.

  **10. "Two of the four grounds" is three. (Reader 6.)** `:362-363` introduces the PF-1 comparison
  with "Two of the four grounds recorded when this section was written did not survive a reader
  checking them". Three of the four bullets carry a dated `*Corrected 2026-09-22:*`, and the fourth's
  correction says its ground "no longer distinguishes the two entries" — which in a list headed "Why
  it is stronger than id 6" is the same non-survival.

  **What the round-3 corrections got right, verified and recorded.** Both readers checked all seven and
  found all seven correct. Reader 6 additionally verified the adopted split line by line: the
  `SOURCE_COINED_LABELS` tuple bounds, all seven strings, the `check_source_label_in_skill_content`
  violation text, the `metric` exclusion comment, the 03-07 GAP B provenance, the `:302-305` routing to
  LEG-04, the five labels in both deal briefs, the case-insensitive matcher, the `README.md`:369-371
  citation, and that `Decision Process` and `Competition` appear nowhere else. The three-live-questions
  count and the `NUMBERING.md`:31-54 order finding were both confirmed.

  **Reasoning critiques, recorded as observations** (prose-gap stopping rule): id 6 is booked `Closed
  on reasoning` while the entry says prong 2 rests on a test `SOURCES.md` does not contain and prong 4
  is "recorded rather than disposed" — and 06-07's own narrowing made prong 2 weaker, so the closure is
  further from its own definition (`:793-796`) than before (readers 3 and 4, independently); the PF-1
  section's prong-4 engagement and its "the framework's own vocabulary" and "ordered the way the
  framework itself sequences them" claims rest on a read of Force Management material recorded nowhere
  — the same defect 06-07 removed from id 6 fifteen lines earlier, left standing in the parallel entry
  (both readers); "the mark is live and unadjudicated" outruns a register the file says it could not
  reach (reader 3); `completeness-audit.md`:12-15 is over-read as "declining to concede" order
  provenance when it routes provenance to the registry (reader 4); and prong 3's "anywhere in this
  repository" is an unqualified whole-repo negative with no recorded sweep (reader 4).

### 14. A cold read of README after the round-3 corrections
expected: |
  Round 4, against `README.md`. Gap G-06-11 was one false statement; 06-07 bounded it in both files.
  This test asks the same question by two readers who made no correction.
result: issue
reported: "Both round-3 corrections hold. One statement, found by one of the two readers and standing since Phase 1: README says the checker enforces 'all of the above' over a 17-item inventory it does not read eleven of. The second reader examined the same sentence and rejected it, but on a different comparison than the one that falsifies it."
severity: major
evidence: |
  **README.md:175 — "`tools/check_repo.py` — a stdlib-only checker enforcing all of the above, wired
  into CI." (Reader 1.)** "All of the above" is the 17-item inventory at `:136-174`.
  `grep` over the whole 8,554-line checker returns zero hits for `pressure-tests`, `proxy-sources`,
  `scenarios.json`, `lint.py`, `run_routes`, `run_trigger` and `RESULTS-trigger`. Its scan roots
  exclude the directory outright (`check_repo.py`:66-68: "Scan roots are examples/ and skills/;
  evals/ is deliberately excluded"). README itself says the opposite for one of those items at
  `:289`: "`check_repo.py` will not do it for you." Written in commit `58530a6` (Phase 1) and
  survived four rounds of cold reads — this is the first reader to open the checker and count.

  **The 2-to-1 note, recorded so it is not re-litigated.** Reader 2 examined `README.md`:175, checked
  it twice and rejected it — but against a different comparison: the checker's *docstring opening
  sentence* versus its own code list, concluding "the stale sentence is in check_repo.py, not in
  README". That does not reach reader 1's comparison, which is README's "all of the above" against
  what the checker actually reads. Recorded as confirmed on the evidence, with reader 2's reasoning
  noted because it is a real and separate observation: `check_repo.py`:4-5's opening sentence is also
  narrower than the checker it introduces.

  **What both readers verified.** Both round-3 corrections: `:9-12`'s bounded separation claim,
  including the nine-name self-test assertion read against `run_benchmark.py`:1649-1659 and the
  identical `rfp-security-weight` row named as shared; and every earlier round's correction still
  standing. Reader 2 recomputed the route means and ranges from the 36 raw records (7.9, 7.1, 6.3 and
  every pair overlapping) and recounted activation from `"activated": true` (9, 11, 8). Reader 1
  resolved all 31 listed paths. Reader 2 also examined and declined `README.md`:294's regeneration
  instruction as over-broad rather than false, since running the generator after editing
  `worked-examples.md` is a no-op.

### 15. No two committed files state things that cannot both be true
expected: |
  Round 4, the whole-tree sweep bound to no named file. Round 3's sweep found three; 06-07 closed all
  three. This asks the same question again of the whole tree.
result: issue
reported: "Four more contradictions, none of them in a file the other three briefs name, and none created by 06-07. One ships to every installed user: the derivatives tell the reader that every rule the omitted reference file illustrates carries a constructive line in SKILL.md, and eight of them cannot, because this repository's own build gate forbids it."
severity: major
evidence: |
  **1. The derivatives' omission notice is false, and it ships.**
  `output-styles/proof-first.md`:27-30 and `prompts/system-prompt.md`:15-18, written by
  `generate_derivatives.py`:183-186 — "One source is deliberately left out:
  `skills/proof-first/references/worked-examples.md` … every rule it illustrates already carries its
  own constructive line in `skills/proof-first/SKILL.md` — so nothing normative is lost."

  `worked-examples.md` illustrates **eight MC rules** (`## MC-` headings: MC-1, 6, 11, 16, 21, 26, 31,
  36). `SKILL.md` contains **zero** `### MC-` headings, and cannot contain them: `mc-rule-in-skill`
  (`check_repo.py`:144-152) makes an MC rule defined in `SKILL.md` a build failure, and
  `NUMBERING.md`:122-129 records every MC row as "Defined in | completeness-audit.md". The sentence
  cannot be true while the gate holds, and the gate is green. This is the only round-4 finding that
  reaches an installed user.

  **2. `check_repo.py`:4235-4237 — "until then this repository makes no such claim."** The claim
  disclaimed (`:4232-4234`) is "whether a session driven by a derivative reaches the same conclusions
  as one with the skill folder installed". `README.md`:113-115 and `evals/routes/RESULTS-routes.md`:1-3
  publish exactly that measurement, 36 sessions on 2026-09-21. The same file's
  `derivative-comparison-claim-stale` (`:4279-4284`) is built on the opposite premise.

  **3. `generate_derivatives.py`:8-11 — "Phase 5's benchmark is the only place such a statement could
  ever be sourced from."** The same script's `_render_preamble()` (`:189-193`) writes, into both
  derivatives, "A benchmark has compared a session driven by this file against a session with the
  skill folder installed: `evals/routes/RESULTS-routes.md` records what was measured". That is a
  different source, named by the file that says no other could exist; its own `:168-175` docstring
  says the old denial "stopped being true when 04-15 committed `evals/routes/RESULTS-routes.md`."

  **4. `run_benchmark.py`:476-479 — "The five caveats EVAL-10 requires", twice, plus "the same five
  keys", and again at `:2373`.** `REQUIRED_CAVEATS` holds six, `RESULTS.md` renders six bullets, and
  `README.md`:229 says six. The comment sits directly above the constant it miscounts.

  **What the sweep verified as consistent.** All three of round 3's sweep fixes: `evals/lint.py`'s
  restated ceiling, ledger row 28's six limits, and `run_conformance.py`'s five fixtures.

### 16. The sentences the last gap-closure round added survive checking
expected: |
  Round 4, new brief. Four of round 3's eleven findings and two of round 2's fourteen were authored by
  the round that was closing the previous one, and no brief had ever been aimed at that surface. This
  reader was given the 202 lines commit `908b90b` added, grouped by file, and asked to verify every
  citation, count, scope claim and absolute in them against the tree.
result: issue
reported: "The brief paid for itself on first use — highest-yield reader of the round. It converged with the two LEGAL-REVIEW readers on four findings and added two neither could reach, both in the deal brief: a count that is wrong under either way of counting, and a second separation claim presented as mechanically held when no code checks it."
severity: major
evidence: |
  **1. The 20% count is wrong under either counting rule.** `evals/benchmark/bench-deal-brief.md`:18-20
  — "20% carries four different meanings inside this brief alone and three inside the other". Counting
  raw occurrences in the figure and rubric tables gives **four in each** (bench `:128`, `:155`, `:187`,
  `:189`; examples `:63`, `:66`, `:87`, `:116`). Counting distinct meanings gives **two** in the bench
  brief (Q3's weight, restated at `:128` and `:187`; the security weight, at `:155` and `:189`) and
  **three** in the examples brief (Q2's weight, Q5's weight, the security weight). Neither rule
  produces "four … and three", so the two halves are counted on different rules and one is wrong under
  either. The sentence was written to justify not varying the figure, so the reasoning it carries is
  load-bearing.

  **2. The platform half of the separation is presented as mechanically held; nothing checks it.**
  `bench-deal-brief.md`:10-12 — "That separation is the one that matters and the one that is
  mechanically held: `run_benchmark.py --self-test` asserts every invented party and person in
  `examples/deal-brief.md` is absent from this file, and the platform lists are disjoint", restated at
  `:20-22` as "no shared company, person or platform … is the one held mechanically".
  `run_benchmark.py`:1649-1659's tuple holds nine person and party names and no platform name, and a
  grep for `platform`, `VMware`, `Hyper-V` and `vSphere` over `run_benchmark.py` and `check_repo.py`
  returns nothing. The platform lists *are* disjoint — reader 2 confirmed it independently — but that
  is an authored observation, and the sentence puts it inside the mechanical claim. Same defect class
  as finding 1 of test 13, in the same commit.

  **Converged with the LEGAL-REVIEW readers** on the `SKILL.md`:63 misquote, the `source-label-in-
  skill-content` scope, the `git grep -l` provenance, and the "two of the four grounds" miscount.

  **What this reader verified as accurate** — the long list is in test 13's closing paragraph; it
  covers every citation, bound, string and count in the adopted-split passage, plus the
  three-live-questions correction and ledger row 29's state.

### 17. A cold read of README after the round-4 corrections
expected: |
  Round 5, two independent readers, same brief as tests 6, 9, 11 and 14. Round 4 bounded README's
  "enforcing all of the above" to the 23-file surface the checker actually reads. Re-ask the whole
  question of the corrected file: does any statement in README contradict a committed file?
result: issue
reported: "The round-4 correction holds and verifies exactly — I traced a live checker run and got the same 23 files, file for file. Three new statements, none of them in text any round has touched recently: two coverage claims wider than the thing they describe, and one contradiction with the checker's own docstring."
severity: major
evidence: |
  **The round-4 correction verified, independently and mechanically.** `README`:176-182 says a live
  run opens 23 files and enumerates them. I instrumented `pathlib.Path.read_text`, `read_bytes`,
  `Path.open` and `builtins.open` over `python3 tools/check_repo.py`: **exactly 23 in-repo files,
  exactly the ones enumerated**, and the six named as never opened plus the five named below the
  line were all absent. Both README readers ran the same trace independently and got the same set.

  **1. `README`:196 — "the published source for every term `evals/lint.py` counts as a proxy".**
  `evals/proxy-sources.md` holds exactly 30 term rows, which are exactly
  `PROXY_TERMS ∪ SUPERLATIVE_TERMS ∪ HEDGE_TERMS` (22 + 5 + 3). `evals/lint.py` also matches
  `CLAIM_VERBS` (18 terms) and `CONDITION_CUES` (7), and labels the first group a proxy in its own
  violation string — `evals/lint.py`:389, `'{term}' is a claim verb (PF-2.1 proxy)`. **All 25 have
  no row.** `evals/lint.py`:146-147 and :154-155 say so in the code: "Frozen here, not
  registry-sourced". **Authored `441b344` — 06-05, the round-1 gap closure**, and missed by every
  README read since.

  **2. `README`:53-54 — "`output-styles/` at this repository's root is … not a directory Claude Code
  scans, so the file is not offered in `/config` until it is copied to one that is".**
  `tools/check_repo.py`:4118-4122, the docstring of the check that owns this very README claim, says
  the same directory "is where a plugin ships a style from and **is scanned only once the repository
  is installed as a plugin**". Route 2 is exactly that install, and `.claude-plugin/marketplace.json`:11
  sets `"source": "./"`, so the plugin root is the repository root. The counter-reading — that
  README's sentence is scoped to the route-3/4 local-clone paragraph it sits in — is available, and
  is why this is recorded with the scope stated rather than as a bare miscount; but the sentence
  asserts the property of the directory unqualified and draws a consequence from it. Authored
  `63b5dfa`, 04-13.

  **3. `README`:306 — "After editing `skills/proof-first/SKILL.md` or any of its reference files, run
  [the generator]".** README fixes "its reference files" at five, at `:176` and in the layout tree.
  `tools/generate_derivatives.py`:44-46 states the same re-sync step over "the **four** named
  reference files", `DERIVATIVE_SOURCE_NAMES` (:80-86) holds four, and `OMITTED_SOURCE` (:97) is
  `worked-examples.md`, deliberately excluded. Editing the fifth changes no derivative, so neither
  `--check` nor `skill-derivative-stale` can see it — which makes README's next sentence, "skipping
  this step cannot ship silently", true of four files and vacuous for the fifth. Authored `b59dba6`,
  04-08.

  **Checked and holding** (recorded so the negative is visible): the 31-rule and 28-pair counts
  against `NUMBERING.md`, `SKILL.md`:31 and `worked-examples.md`; all ten CI commands; every path in
  the layout tree; the benchmark claim region recomputed from the 96 committed raw records
  (45/1/2, 32/3/13, 7/3/38, 48 pairs, 0 excluded) and the 16-cell direction split; the trigger Arm B
  figures and the shipped-description hash; the route figures; the MOD-04 3/10-vs-4/10 arms; the
  `/config` observation and its two stated limits; the nine invented names and six platform names;
  the reproduced before/after pair, byte-identical.

### 18. The reproduction-boundary material after the round-4 corrections
expected: |
  Round 5, two independent readers, same brief as tests 7, 10 and 13. 06-08 corrected ten statements
  here and re-anchored the file's `check_repo.py` citations to named symbols. Re-ask the whole
  question of the corrected file.
result: issue
reported: "Every round-4 correction holds — both readers checked all ten and the symbol anchors, and none has drifted. Eight new statements. Two of the three citations carrying this section's own central correction now point at blank lines, and the round that broke them is the round that wrote the fix."
severity: major
evidence: |
  **Round 4's corrections verified by readers who did not make them.** All ten corrected statements
  re-checked against the file each one cites; all ten hold. The symbol anchors 06-08 substituted for
  line numbers survive the insertions made after them — which is the property they were chosen for.

  **1. Two of three citations point at blank lines.** `LEGAL-REVIEW.md`:523-527 offers three
  `path:line` pairs as the evidence that "All three carry one identical sentence naming all seven in
  the table's order". `skills/proof-first/SKILL.md`:63 is correct.
  `output-styles/proof-first.md`:87 and `prompts/system-prompt.md`:75 are **empty lines**; the
  sentence is at `:90` and `:78`. **Both resolved correctly at `38c873b`** — verified by reading
  those two lines at that commit. Commit `f909d3c`, the closing round's own first task, added three
  net lines to each derivative's preamble and broke both. Three readers converged on it.
  `record-citation-unresolvable` cannot see it twice over: the lines exist, and `CITATION_RE`
  (`check_repo.py`:4496-4498) requires backticks these three do not have.

  **2. `:169-173` — "Two rows were confirmed against bibliographic edition records … Three rows were
  confirmed against public vendor pages".** `SOURCES.md` carries **three** openlibrary.org edition
  records (`:43`, `:53`, `:54`) and three public pages (`:31`, `:32`, `:44`). The paragraph opens by
  saying all six URLs were fetched and every row checked, then partitions them 2 + 3 = 5. Authored
  `6cc615a`, 06-02; four rounds did not reach it.

  **3. `:536-537` — "asked here against a live unadjudicated mark".** `:476-485`, added by the
  closing round, records that phrase as withdrawn: "**Live on the register:** not established and
  **not claimed**", and "Unadjudicated" restated as "no adjudication of it was found". `:505` says
  it was "answered by restating the point in the one sense this file evidences", and `:437` carries
  the narrowed form. At `38c873b` the phrase occurred once and there was no withdrawal; the closing
  round added the withdrawal in three places and left this occurrence standing.

  **4. `:506-507` — "Prong 3's whole-repo negative … answering it cost one command, recorded
  above".** Prong 3 (`:280-282`) is three sentences and no command. The only recorded whole-repo
  sweep, `git grep -inE 'many (independent )?publishers…'` at `:269`, is attached to prong 2 at
  `:263-272`. A grep of the file for every command it records returns `:25`, `:269`, `:315`, `:330`,
  `:337`, `:345`, `:547`, `:555`, `:577`, `:579` — none about a diagram, figure or visual
  arrangement. Three readers converged. Authored `81dfc6b`, closing round.

  **5. `:53-55` — the "list"/"file" correction retires an accurate quotation.** It says: the word
  inside the quotation marks was "list"; the checker says "file". **The checker says both.**
  `tools/check_repo.py`:484-487, the module docstring's `source-gate-incomplete` entry, carries the
  sentence verbatim with **"list"**; `:2177-2179`, the function docstring, carries it with "file".
  `grep -n "it declares a pass over is complete" tools/check_repo.py` returns one line — `:487`, the
  "list" one — because the function docstring wraps mid-phrase. So the retired quotation was
  accurate, and a reader sent to the checker to find "file" will not find it where the violation-code
  catalogue states the ceiling. Round 4's finding that prompted this correction was itself wrong.
  Two readers found it; a third read the same two docstrings and passed it, which is recorded
  because the facts are not in dispute and the disagreement is about what the marker asserts.
  Authored `22c99f2`, closing round.

  **6. `:722-724` — "the machine check that enforces it — a configured remote requires a passed gate
  — is green in the no-remote direction".** No such check exists. `tools/check_repo.py` imports no
  `subprocess` and no process-spawning module (`grep -c subprocess` → 0), so it cannot observe
  whether a remote is configured. The only code that reads `Gate status:` is `source-gate-incomplete`,
  whose body compares that line against `SOURCES.md`'s row statuses and never looks at a remote. The
  only "remote" strings in the tree are two docstring lines describing the SSH URL form inside
  `publish-location-drift`'s owner normaliser. Authored `97927b8`, 06-04.

  **7. `:910-913` — "the six self-tests in `evals/`" was written as "seven".** `find evals -name
  '*.py'` returns six scripts and `.github/workflows/ci.yml` runs exactly six `python3 evals/`
  commands. The same sentence enumerates CI as 3 + N + 1 and opens with "All ten CI commands", so
  N = 7 makes it eleven. Never true: six at `f54edf7` — **06-06, the round-2 gap closure** — and six
  today. **This
  UAT file carried the same false sentence in three of its own methodology sections and they are
  corrected in this edit.**

  **8. `:119-120` and `:651` — "The two TSDR endpoints that failed during Phase 6 research answered
  this time".** `:131-133` records the second endpoint returning **HTTP 401** and calls it "Recorded
  as a failed lookup"; the table row at `:648` says the same; `:57-58` says "including the two
  lookups that failed". The file uses "answered" as the contrary of the earlier 503 and 403, which
  were themselves HTTP responses — so on its own vocabulary one of the two did not answer. Authored
  `6cc615a`, 06-02.

  **Checked and holding**: the eight block names and their order in `NUMBERING.md`; MEDDPPCC and the
  six swappable positions; `SOURCE_COINED_LABELS`' seven entries and the `metric` exclusion;
  `check_source_label_in_skill_content`'s real glob scope and its `strip_fences` read;
  `_source_label_pattern`'s `re.IGNORECASE`; `grep -c '```'` returning 0 for all six skill files;
  the four-file rename cost and `NUMBERING.md`:48; the wrap-tolerant sweep for "one per Command of
  the Message"; `completeness-audit.md`:12-15 carrying both readings; the two retired citations
  quoted inside correction paragraphs, which still resolve, exactly as the new code's docstring says.

### 19. No two committed files state things that cannot both be true
expected: |
  Round 5, the whole-tree sweep bound to no named file — same brief as tests 12 and 15. Round 4's
  four sweep findings were corrected, including the one that reached every installed user. Re-ask
  the whole question of the corrected tree.
result: issue
reported: "All four round-4 sweep fixes hold, and the user-facing one verifies rule by rule. Four new contradictions, and the sweep reached three directories no brief has ever named — the trigger transcripts, the artifact-patterns element labels, and the bench brief's timeline."
severity: major
evidence: |
  **Round 4's user-facing fix verified rule by rule.** Both derivatives' omission notice now names
  `completeness-audit.md` for the MC rules. I checked every one of the 28 rules `worked-examples.md`
  illustrates (20 PF + 8 MC) against the source the notice names for it: **all 28 carry a
  `Replace with:` line in the named file, none missing**. `SKILL.md` carries 0 `### MC-` headings,
  `completeness-audit.md` carries 8, and each derivative carries 39 constructive lines (31 PF + 8 MC).
  The other three sweep fixes re-checked and holding.

  **1. `tools/check_repo.py`:4470-4476 contradicts its own module docstring, both written in the same
  commit.** The block comment above the new check says: "Nine were the same mechanical defect: a
  `path`:N citation that resolved when it was written and **stopped resolving** when the cited file
  was edited afterwards … **This code closes that class.**" The module docstring at `:986-994` says:
  "Every citation finding four rounds of cold reads produced was a line number that existed and
  pointed at the wrong content … **This code catches none of them.** It is future insurance against
  three shapes **that have not yet occurred here**", and `:978-981` records the full-history replay
  firing **ZERO** times. A citation that stopped resolving is precisely what the code fires on, so
  it cannot both close that class and have never fired. Both readers who saw it converged.
  Authored `3589842`, closing round.

  **2. `evals/trigger/INIT-EVENTS.md`:72-81 — "The init event's full top-level key set" lists 23
  keys.** I unpacked `evals/trigger/transcripts-cat10.tar.gz` (140 `.jsonl` files) and extracted the
  init event from each: **one distinct key set across all 140, and it holds 24 keys.** The missing
  one is **`subtype`** — the key the file's own extraction script at `:42` selects on
  (`e.get('subtype') == 'init'`). A reproduced key set called "full" cannot omit a key every event it
  reproduces carries. Authored `b077b8b`, 02-10; no brief had opened `evals/trigger/` before.

  **3. `tools/check_repo.py`:239 and :2885 — "the fifteen frozen element labels".**
  `artifact-patterns.md` carries **13** element labels across the four family sections, 14 counting
  `**No family fits:**` in the classification section, and 18 counting the four `**Order:**` lines
  the same sentence counts separately. **Fifteen is not reachable under any rule.** It was never
  true: the same 18/4/13 split held at `6bc2dab`, where the docstring was written. The frozen list in
  `03-03-PLAN.md`:354's own verification command has **14 entries** while the plan's prose and
  `03-03-SUMMARY.md` both say fifteen — so the miscount is inherited from Phase 3, not minted here.
  Authored `6bc2dab`, 03-03.

  **4. `evals/benchmark/bench-deal-brief.md` states the same comparison in both directions.**
  `:106-107`: the vendor's comparable programme "took 11 months — **shorter than**, but close to, the
  audit window". `:118-120`: "that audit window is close to, but **shorter than**, Meridian Cloud
  Partners' own comparable-programme duration". The file's own canonical figures settle it —
  `:194` `audit-window-months | 6`, `:208` `vendor-comparable-duration-months | 11` — so 11 > 6 and
  `:107` is the wrong one. The parallel sentence in the other brief, `examples/deal-brief.md`:41,
  has the correct shape ("took 14 months — longer than the examination window"). Authored `1577910`,
  05-02. Two-sided and checkable: the prose contradicts the same file's figure table.

  **Checked and holding**: every count stated in prose next to the thing counted — the 31 rules, the
  28 pairs, `completeness-audit.md`'s 8 dimensions, `NUMBERING.md`'s per-section Allocated and Next
  free columns, `pressure-tests.md`'s 14 observations, `scenarios.json`'s 8 prompts;
  `run_benchmark.py --report-only` and `run_routes.py --report-only` regenerating their RESULTS files
  byte-identically from the committed raw records; every results figure the README cites,
  recomputed from raw; all 53 layout-tree paths.

### 20. The sentences the last gap-closure round added survive checking
expected: |
  Round 5, second run of the fourth brief. It was the highest-yield reader of round 4 on first use
  and the round recorded keeping it permanently. Given the added lines of
  `git diff 38c873b..398842c` outside `.planning/` — 658 lines grouped by file — verify every
  citation, count, scope claim and absolute in them.
result: issue
reported: "It paid for itself again, and this time it converged rather than standing alone — four of its seven findings were also reached by the LEGAL-REVIEW readers or the sweep. Its three unshared findings are the numbered ones in the evidence block below: two are the round asserting a property of its own new code that the code's own docstring denies, and the third is a reader count in a ledger row, which is a different shape. *Corrected 2026-09-22 (06-10) by task 22: this read 'four of its six findings' and 'its two unshared findings are both the same shape'. The evidence block directly beneath this line carries three numbered findings and four converged ones — seven, with three unshared — and the third is not the same shape as the other two."
severity: major
evidence: |
  **1. `tools/check_repo.py`:997-999 — "it reads `strip_fences()` output, **like every other
  content-scanning code here**".** **Six** other check functions state in their own docstrings
  that they read raw and deliberately never call `strip_fences`: `check_results_breakdown_count`,
  `check_readme_install_paths` (`:3871-3872`, "Reads README.md's raw text and never calls
  strip_fences", and the same in the module docstring at `:778-779`), `check_readme_example_drift`
  (`:3954-3955`), `check_readme_example_lead_distance` (`:4003-4004`),
  `check_readme_output_style_destination` (`:4122-4123`) and `check_derivative_comparison_claim`
  (`:4371`). Reproducible: match each `def check_*` docstring for `strip_fences` alongside "raw". Authored `1d477f5` — the commit whose own message is
  "code-review gate — two findings in the round's own new check, both fixed".

  **2. `tools/check_repo.py`:4479-4480 — "Both already carry `path`:N citations".**
  `CITATION_RECORD_PATHS` is `('LEGAL-REVIEW.md', 'README.md')`. I ran the file's own committed
  `CITATION_RE` over both: **`LEGAL-REVIEW.md` 9 citations, `README.md` zero.** README carries no
  citation of that shape anywhere — its only `` `path`: `` hits are backticked paths followed by a
  colon and no number. Authored `3589842`, closing round.

  **3. `LEGAL-REVIEW.md`:976, ledger row 12 — "Round 1's two readers returned PASS on the named
  question".** `:865-866` records the answer to that named question as coming from **one** reader
  ("A reader who had not written it returned PASS"), and `06-UAT.md` test 4 records the same,
  singular. `:843-848` records round 1 as running **five** readers, of which the only pair was given
  the README contradiction hunt — which returned three checkably-false statements, not a PASS. The
  sentence did not exist at `38c873b`; row 12 was rewritten by `2e43583`, closing round.

  **Converged with the other briefs** on the citation-code self-contradiction (finding 1 of test 19),
  the prong-3 command (finding 4 of test 18), the "list"/"file" correction (finding 5 of test 18),
  and the blank-line citations (finding 1 of test 18).

  **Checked and found accurate** — the whole of the new check's code, fixtures and mutation entry
  behave as their comments describe; `len(REQUIRED_CAVEATS)` is 6 and the rendered section carries 6;
  `no-entity-collision` and `no-platform-collision` both exercised and passing; the 20% count the
  round removed is gone; `SOURCE_COINED_LABELS`, the `metric` exclusion and the scope statement all
  read as quoted; the four dated correction markers the round claims are all present.

  **Excluded as not settleable from a committed file**: every claim about individual commits or
  intra-round commit boundaries, since the reader's tree is not a git repository. The orchestrator
  checked those separately by `git blame` and by reading the cited lines at `38c873b`; the
  attributions in tests 17-20 come from that check, not from the reader.

### 21. A cold read of README after the round-5 corrections

expected: |
  Round 6, two readers on the contradiction hunt, cross-checked as since round 1. Given
  `README.md` and the tree, check every count, file name, citation, command name, absolute and
  claim about what a tool checks, against the repository as it actually is.
result: pass
evidence: |
  **Zero findings, and it is a strong zero.** Reader 1 made 66 tool calls, reader 2 made 74. Both
  independently instrumented the checker (`sys.addaudithook` and a `Path.read_text`/`read_bytes`/
  `open` wrapper respectively) and confirmed `README.md`:180-191's "A live run opens 23 files"
  enumeration **item for item**, including the six named as never opened and the five named below
  the line. Both mutated the stated inventory counts in a copy — 31→37/77 and 28→44/99 — and
  confirmed `check_repo: 0 violations`, which is what README:305-307 says will happen. Both
  regenerated `RESULTS.md` and `RESULTS-routes.md` with `--report-only` and got byte-identical
  output. Both recomputed `head -14 SKILL.md | shasum -a 256` to `d5dd651a…` and confirmed Arm B
  is the shipped description. Reader 2 additionally resolved all 54 paths in the layout tree and
  confirmed every one exists, and reverted every mutation with a hash check.

  **One finding raised, refuted on verification.** Reader 2 reported `README.md`:334, "The tree
  below shows this repository's layout", as an unsupported completeness claim: the tree omits
  `LEGAL-REVIEW.md` and `.gitignore` at root, and terminates `evals/trigger/` with `└──` after two
  of its six tracked files. Both omissions are real and I confirmed them. The finding does not
  stand, for reasons the repository already recorded:

  - `git blame` puts both framing sentences in one commit, `6c50822` — *"docs(04-08): **narrow two
    over-broad README claims**, repair layout legend"*. That round replaced a completeness claim
    with the one-directional claim that holds, "Every path it names exists in this repository
    today", which reader 2 verified true across all 54 paths and reader 1 did not contest.
  - `README.md`:299-303 states the scope of the guarantee rather than implying a full tree diff:
    the layout paths are named as inventory, and *"One of the three is checked:
    `readme-layout-tree-stale` fails the build when an immediate subdirectory of `evals/` exists
    and this README's layout tree does not name it."* `check_readme_layout_tree_stale`'s own
    docstring says it is scoped "to one level because a full tree diff would fire on `__pycache__`
    and on every future fixture directory".

  Recording this as a gap would re-open a decision a prior round made deliberately and documented.
  It is an **observation**, under this phase's rule that only checkably-false statements block.

  **Cross-check between the two readers held.** Reader 1 examined the same layout tree and did not
  raise it; reader 2 raised it and bounded its own claim correctly ("the narrower adjacent sentence
  **is** true"). No finding was produced by one reader and contradicted by the other.

  **What this closes and what it does not.** Six rounds of README reads have now produced 3, 8, 2,
  1, 3 and 0 checkably-false statements. This is the first zero. It is a zero on `README.md` only —
  the round's other briefs returned 25 findings elsewhere — so it satisfies no closure condition by
  itself. `WINDOWS.md` id 12 closes on a round that returns none, and this round returned 25.

### 22. The reproduction-boundary material after the round-5 corrections

expected: |
  Round 6, two readers on `LEGAL-REVIEW.md`, cross-checked. Resolve every citation, count, quoted
  string and absolute in the file, and separately note any passage that draws a legal conclusion
  rather than recording reasoning.
result: issue
reported: "Twelve findings. All of round 5's eight corrections hold and the quoted-string anchors 06-09 substituted for broken line citations survived the insertions made after them. The sharpest is that the file's own account of how its bibliographic sources were confirmed is false against the record it names: the MEDDICC edition record carries no `by_statement` field at all, and has carried none since 2023, so it cannot be one of the three that 'matched the row's author list exactly'. Four more are scope or count absolutes the file states about itself and its own tooling."
severity: major
evidence: |
  Readers 3 and 4 had `LEGAL-REVIEW.md` named; reader 7 reached the same file through the
  gap-closure-range brief; readers 5 and 6 reached it through the unnamed sweep. Attribution below
  is `git blame` on each cited line, run by the orchestrator — the reader trees are not git
  repositories and every reader said so unprompted.

  **1. `:188-190` — "Three rows were confirmed against bibliographic edition records whose
  `by_statement` field matched the row's author list exactly."** Readers 3 and 4 independently
  fetched all three records live and got the same result; I re-fetched a third time.
  `https://openlibrary.org/books/OL38629171M.json`, the record `SOURCES.md`:43 cites, **has no
  `by_statement` key**. Its `authors` array resolves to `Mr Andy Whyte`, `Dick Dunkel`,
  `Jack Napoli` against the row's single `Andy Whyte`. The other two rows do match
  (`OL24886401M` → "Matthew Dixon and Brent Adamson"; `OL27219998M` → "Brent Adamson, Matthew
  Dixon, Pat Spenner, and Nick Toman"). **This is not drift**: the record reads `revision: 2`,
  `latest_revision: 2`, `last_modified: 2023-02-04`, so the field was equally absent on the stated
  review date of 2026-09-21. At most two rows carry the confirmation the sentence claims for three.
  Authored `6cc615a`, 06-02.

  **2. `:311` — the prong's `"visual arrangement"` clause.** The sentence puts the phrase in
  quotation marks and attributes it to the prong. `SOURCES.md`:15, the only definition, reads "a
  source's **diagram or figure**"; `LEGAL-REVIEW.md`:206, the file's own restatement, reads "a
  source's diagram". `git grep -n "visual arrangement" -- ':!.planning'` returns **only**
  `LEGAL-REVIEW.md`:311 — the citing sentence itself. No source, no shipped skill file and no other
  part of the record carries the phrase, so there is no such clause to narrow. Authored `0df417e`, 06-09.

  *Scope note, recorded because the rule this phase keeps re-learning applied to this entry as it
  was being written. The first draft of this sentence stated the result of an UNSCOPED
  `git grep "visual arrangement"` — and that sentence was true when verified and false by the time
  it was committed, because writing the finding down put the phrase into `06-UAT.md` at three more
  lines. The sweep is scoped to the shipped tree, where the negative is both the one that matters
  and the one that stays stable. Third consecutive round in which recording a command changed its
  own result; first in which the round's own UAT write-up did it to itself.*

  **3. `:345` — "as the `## Reproduction boundary` bullet above sets out."** `## Reproduction
  boundary` opens at `:198`; the first bullet anywhere in it is `:353`, eight lines **below** the
  citing sentence, and it is the bullet that sets the point out. Found by readers 3, 4 and 7
  independently. I checked the construction across the file: five other backward bullet references
  exist (`:377`, `:401`, `:419`, `:553`, `:622`) and **all five resolve**, so this is an outlier of
  one. Reader 3 described it as one of four such uses, which is wrong — recorded here from my own
  count, not its. Authored `33569f8`, 06-08.

  **4. `:383-384` — "the two labels sit in `SOURCE_COINED_LABELS`, a production constant, rather
  than in a fixture".** The same bullet says at `:380-382`: "`Economic Buyer` is inserted into two
  fixture builders in that file, `_bad_numbering()` and `_mc_numbering_for_count()`."
  `grep -in 'economic buyer' tools/check_repo.py` returns 12 lines across eight enclosing
  functions, most of them fixture builders. The companion half is true — `paper process` occurs
  exactly once, at `:3030`, inside the tuple. Authored `33569f8`, 06-08. **This is the finding the
  widened fourth brief was introduced to reach**: 0 matches in `ade21af^..HEAD`, 1 in
  `d67012e^..HEAD`.

  **5. `:547-548` — "the entity check under `## Reproduction boundary`".** The word "entity"
  occurs in this file at `:174`, `:547` (the citing sentence), `:656` and `:657`. The section runs
  `:198-648`, so inside it the word appears only in the sentence citing it. The only
  entity-collision work is `## Name collisions`, a different section enumerating two files, and
  `run_benchmark.py --self-test`'s two-file assertion — neither is a tree-wide check under the
  cited heading. Authored `8f75cc6`, 06-09, whose subject line is "task 18 self-audit — two more
  scope overstatements in this round's markers": the correction removing two overstatements
  introduced a false citation.

  **6. `:616-617` — "once in the `## Reproduction boundary` quotation and once inside the quoted
  command itself."** Readers 3, 5 and 7 each reported three occurrences using line-based grep.
  **Reader 4 ran a wrap-tolerant count and found four** — `:457-458` carries the string wrapped
  across a line break, invisible to `grep`. Confirmed:
  `re.findall(r'Positive\s+Business\s+Outcomes', text)` returns 4, `text.count(...)` returns 3.
  The clause enumerates two. The sentence predicted this exact failure two lines later — "a grep a
  file runs against itself will break again the next time this file quotes the phrase" — and the
  file then quoted the phrase again. The five-file figure in the same sentence still holds.
  Authored `0447175`, 06-08.

  **7. `:23-25` — "**Every** correction made on that basis carries a dated `*Corrected …*` marker …
  `grep -n 'Corrected 2026-' LEGAL-REVIEW.md` lists them."** The grep returns 25 lines. Two
  in-place corrections made on exactly the stated basis are not among them: `:54`
  `*Correction withdrawn 2026-09-22 (06-09)…*` and `:750` `*Updated 2026-09-22:*`, both correcting
  a statement falsified by `tools/check_repo.py`. Reader 3 found one; reader 7 found both. A third
  form exists, `*Clarified 2026-09-22 (06-08)*` at `:1026`, and is **not counted here** — whether a
  wording clarification is "a statement found false against this repository's own files" is
  arguable, and asserting three would repeat the overcount defect this round is recording.
  Authored `22c99f2`, 06-08; `:54`'s marker by `d9aef55`, 06-09.

  **8. `:771` — "`publish-location-drift` stays silent because all four occurrences still agree."**
  Reader 3 considered this and dropped it, on the reading that "four" meant plugin.json +
  marketplace.json + README's two install commands. Reader 4 pursued it and is right.
  `_publish_locations_in`'s own docstring reads **seven** structured positions: plugin.json's
  `homepage` and `repository` (2), marketplace.json's same two plus `owner.url` (3), README's two
  install-command arguments (2). Literal occurrences are 2 + 2 + 5 = **nine**.
  `PUBLISH_LOCATION_CARRIERS` holds **three**. No available counting rule yields four. Authored
  `97927b8`, 06-04.

  **9. `:1062`, ledger row 15 — "the AST-based stdlib check confirms the real import set."**
  `git grep -nE '\bimport ast\b|ast\.(parse|walk|Import|NodeVisitor)' -- '*.py'` returns **nothing**.
  The only two occurrences of "AST-based" in the shipped tree are this cell and
  `run_benchmark.py`:1012, a comment describing what such a scan *would* flag. The cell asserts in
  the present tense that a check confirms something; the check does not exist. **This is the same
  defect 06-09 deleted at `:791-801` in the same round** — commit `44cc648`, "delete the launch
  section's claim to a machine check that never existed" — left standing one screen away.
  Authored `b627fd3`, 06-04.

  **10. `:1077`, ledger row 30 — "Not a falsehood — no committed file contradicts it".** The row
  defends README's "Each scenario was drafted twice". `evals/benchmark/RESULTS.md` is a committed
  file whose `n` column reads **3** for every one of its 32 cells, and the raw records hold **12**
  drafts per scenario (8 scenarios × 12 = 96). The README sentence is already logged as open item
  30; the new finding is that the row's stated justification for keeping it is itself false.
  Authored `f54edf7`, 06-06.

  **11. `:155-157` — "The two existing sentences".** Both contents named are clauses of a single
  sentence in `NOTICES.md`:70-73. The substance holds: both statements are present and unchanged.
  The count noun does not. Minor. Authored `6cc615a`, 06-02.

  **12. `:571` — "an unexcluded sweep returns six — three shipped files plus three records."**
  Found by the orchestrator, and **unreachable by any reader**: the sweep counts `.planning/` files,
  which every reader tree strips. It returns **seven**. Control run at `f547989`, the commit that
  wrote the sentence, returns exactly six — the sentence was true when written and was falsified
  five commits later by `10cfa1e`, 06-09's own SUMMARY commit, which became the seventh match.
  **The round's self-audit structurally cannot catch this class**: the audit runs before the SUMMARY
  exists, so any command literal whose result the SUMMARY can change is unauditable from inside the
  round. Authored `f547989`, 06-09.

  **Checked and found to hold.** All eight of round 5's LEGAL-REVIEW corrections were re-checked by
  readers who did not make them and every one stands, including the two citations re-anchored by
  quoted string after `f909d3c` broke them — the anchor form survived every insertion made after it,
  which is the property it was chosen for. All nine `` `path` ``:N citations resolve and say what
  the citing sentence says. The prong-3 sweeps reproduce exactly. Both readers fetched the external
  sources live and confirmed the docket caption, number, court, judge, filing date and un-terminated
  state; the 2026-04-21 holding; the TSDR record's `LIVE/REGISTRATION/Issued and Active` state with
  no cancellation recorded; and the Force Management and Challenger page states.

  **Recorded as observations, not findings.** Both readers independently flagged passages that read
  as legal analysis rather than recorded reasoning — the concern G-06-3 closed in round 1. Reader 3
  named five, reader 4 named six, and they converge on three: the idea/expression thinness judgement
  at `:260-263`, the separate-bodies-of-law proposition at `:429-432` which no `SOURCES.md` row is
  cited for, and the name-collision mitigation at `:690-692`. Reader 4 adds `:695-699`, which
  selects two of six collisions as "worth acting on" and recommends a remedy before distribution.
  This is prose judgement, not a checkably-false statement, so it does not block under this phase's
  rule. Both readers noted for balance that the file disclaims explicitly at seven separate points
  and that each flagged passage is hedged in the sentence following it. Routed to the owner as a
  standing question rather than a gap: the disclaimers reach the verdict layer, which is what 06-05
  task 7 fixed, but a reader who has not read the disclaimers first still meets the analysis before
  the hedge.

### 23. No two committed files state things that cannot both be true

expected: |
  Round 6, first run of the sweep at **two** readers, both on the same brief naming no file, run
  independently so their findings can be cross-checked and the second reader's marginal yield
  measured.
result: issue
reported: "Thirteen findings across four files, eleven of them outside the two files the named briefs take as their subject. Two shapes dominate. The first is the scope absolute — a comment saying no other check reads some path, falsified by a check added later in the same file; there are five of those in `check_repo.py`, three inside one sixteen-line comment block that 06-09 edited and partly corrected. The second is `RESULTS-mod04.md` contradicting itself about its own scorer: a banner saying every run block in the file is unanchored, sitting above fourteen anchored ones, and two arms that each name the same session as both the excluded timeout and a counted verdict."
severity: major
evidence: |
  Sweep A returned 9 findings, sweep B returned 7, 3 shared, 13 distinct. Shared findings are marked.

  **`evals/conformance/RESULTS-mod04.md` — four findings, none reachable by a file-named brief.**

  1. **`:13` — "Every run block recorded in this file was produced by an unanchored scorer."**
     `grep -c "within the first 400 chars" evals/conformance/RESULTS-mod04.md` returns **14** — blocks carrying the anchored
     scorer's own evidence string. `grep -c "marker_at=None" evals/conformance/RESULTS-mod04.md` returns 12, the unanchored ones. The
     same file at `:735-737` says of those figures: "every figure below is a precise measurement,
     not an optimistic ceiling". Authored `fbe0aa6`, 03-09. *(Sweep A)*
  2. **`:32`, `:43`, `:53` — "every figure **above** this section", "Every run block recorded
     **above** this section".** The section opens at `:11`. Lines 1-10 hold the title and one
     paragraph — no run block and no figure. The first run block is `:138`. Authored `fbe0aa6`,
     03-09. *(Sweep A)*
  3. **`:752`/`:756` — Arm A names `B-proposal-section` "first attempt" as both the excluded
     timeout and one of seven counted `no-family` verdicts.** The three committed blocks in
     timestamp order: `06:42:11` = `no-family`, `06:48:34` = `unscoreable | reason=timeout`,
     `06:56:50` = `conformant`. The timeout is the **second** attempt. Authored `878b937`, 03-12.
     *(Both sweeps)*
  4. **`:770`/`:772` — the same defect in Arm B on `A-rfp-answer`.** `07:40:29` = `no-family`,
     `07:45:44` = timeout, `07:53:55` = `conformant`. Authored `878b937`, 03-12. *(Both sweeps)*

     **Severity bound, checked rather than assumed:** findings 3 and 4 do not touch the published
     numbers. `README.md`:266-268's "3 of 10 (30.0%)" and "4 of 10 (40.0%)" match
     `RESULTS-mod04.md`:760 and `:776` exactly, and three readers independently re-derived both
     from the committed run blocks. The defect is in per-session attribution prose; the
     denominators hold.

  **`tools/check_repo.py` — six findings.**

  5. **`:4-5` — "This script is a structural and textual consistency check over `NUMBERING.md`,
     `examples/deal-brief.md`, and `NOTICES.md`."** A live run opens **23** files. Four independent
     tracers agree — readers 1, 2, 5, 6 and my own. The same docstring defines codes whose subjects
     are `README.md`, `SOURCES.md`, `LEGAL-REVIEW.md`, both `.claude-plugin/` manifests and both
     derivatives. `README.md`:180-183 states the true scope. Authored `5b124ba`, **plan 01-01** —
     the commit that created the checker. *(Sweep B)*
  6. **`:33` — "Violation codes implemented in this file:" followed by 57 entries.** The file
     implements, self-tests and mutation-proves **58**. The gap is exactly
     `catalog-opening-rule-count`, defined at `:3085`, registered at `:3163`, dispatched at `:3176`
     and mutation-entried at `:5601`. Verified by parsing the catalogue against the self-test's own
     emitted list: one name in the latter and not the former. Authored `5b124ba`, **01-01**.
     *(Both sweeps)*
  7. **`:448` and `:1612` — "a CI badge reports that **ten offline scripts** exited zero."** CI
     invokes **eight** distinct scripts with **ten** commands (`check_repo.py` three times).
     `README.md`:188 states the distinction correctly as "the full list of ten commands", and
     `LEGAL-REVIEW.md`:991-995 corrects exactly this scripts-versus-commands confusion for a
     different count — so the repository has already ruled on the distinction and left this
     instance. Authored `1b63ece`, 06-03. *(Sweep B)*
  8. **`:4753-4757` — "**No check other than** results-breakdown-count-mismatch itself reads
     anything under `evals/` — every other glob and named-path scan in this module targets
     NUMBERING.md, examples/, tools/, or skills/*/SKILL.md paths."** `check_readme_claim_unsourced`
     reads all four `evals/*/RESULTS*.md` files on every live run, via `CLAIM_SOURCE_GLOB` at
     `:1607`. `check_readme_layout_tree_stale` also targets `evals/` via `LAYOUT_TREE_SCAN_DIR`.
     Both clauses are false. Authored `82535c7`, 03-16. *(Sweep A)*
  9. **`:4759-4762` — "**No other check** reads SOURCES.md."** `check_source_gate_incomplete` reads
     it — that is its whole purpose, and the module docstring at `:484-485` says the check "reads
     **two** committed files". `check_record_citations` reads it too. Authored `c0fca5f`, 06-01.
     *(Sweep A)*
  10. **`:4763-4765` — "source-gate-incomplete and framework-statement-stale-review both read it,
      and **no other check does**."** `check_record_citations` reads `LEGAL-REVIEW.md` as one of its
      two `CITATION_RECORD_PATHS`. Authored `e2e4aa2`, 06-02. **Causal chain:** 06-08's `3589842`
      added the check that falsified this sentence, and 06-09's `36ef0a9` then edited this same
      comment block to fix a different sentence in it, leaving three false scope absolutes in
      sixteen lines. *(Sweep A)*

      Findings 8, 9 and 10 were each confirmed by my own `Path.read_text` tracer recording the
      enclosing `check_*` frame, not taken from the reader.

  **`SOURCES.md` — one finding.**

  11. **`:3` — "Last reviewed: 2026-09-10."** All six of its data rows read `(retrieved
      2026-09-21)`. `evals/proxy-sources.md`:13-14 records that "`SOURCES.md`'s own rows were
      re-confirmed against live pages on 2026-09-21". `LEGAL-REVIEW.md`:3 dates the review
      2026-09-21 and `:102` records moving `NOTICES.md`'s stamp "from 2026-09-10 to 2026-09-21" —
      all three `NOTICES.md` stamps now read 2026-09-21. The review that re-fetched all six rows
      updated the sibling file's stamps and not its own. Authored `0ba93f8`, **01-03**. *(Sweep B)*

  **Two findings already recorded under test 22** were also reached through the sweep and are not
  double-counted here: `LEGAL-REVIEW.md`:616-617 (sweep A) and `:1077` (sweep B).

  **Marginal yield of the second sweep reader — the measurement 06-09 asked round 6 to make.**
  Sweep A: 9 findings, 6 unique. Sweep B: 7 findings, 4 unique. Shared: 3 (both double-counted
  sessions and the catalogue omission). **The second reader produced 4 findings the first did not**,
  16% of the round's 25. Its unique four are findings 5, 7, 11 and `LEGAL-REVIEW.md`:1077 — three
  of them the checker's own self-description, which sweep A read past. The standing set's exit
  condition is a marginal yield of zero for two consecutive rounds; this is the first measurement
  and it is not zero. **Two sweep readers stay**, and round 7 records the second measurement.

### 24. The sentences any gap-closure round added survive checking

expected: |
  Round 6, first run of the fourth brief at its widened scope. Given the added lines of every
  gap-closure commit range rather than only the last round's diff, verify every citation, count,
  scope claim and absolute in them against the tree.
result: issue
reported: "The widening paid on its first run, by one finding, and the measurement is clean: `LEGAL-REVIEW.md`:383-384 was authored by 06-08 and returns zero matches in the range a diff-scoped brief would have been given this round. Reader 7 produced 5 findings, 3 of which the LEGAL-REVIEW readers reached independently. Separately, three findings came from the orchestrator over `.planning/`, which no reader can see — and one of them is a claim that was true when written and was falsified by its own round's SUMMARY commit five commits later."
severity: major
evidence: |
  Reader 7 was given `GAP-CLOSURE-CHANGES.txt` — every line added across `d67012e^..HEAD`, 1,714
  lines grouped under 15 file headers — and covered all 15 groups.

  **Reader 7's five findings**, all recorded under test 22 where their subject lives: `:311`
  (unique), `:383-384` (unique), `:345`, `:616-617` and `:23-25` (all three also reached by the
  LEGAL-REVIEW readers). Convergence is 3 of 5, against round 5's 4 of 7.

  **Did the widening pay?** Yes, by exactly one finding, and the test is reproducible:

      $ git diff 'ade21af^..HEAD' -- LEGAL-REVIEW.md | grep -c "rather than in a fixture"
      0
      $ git diff 'd67012e^..HEAD' -- LEGAL-REVIEW.md | grep -c "rather than in a fixture"
      1
      $ git merge-base --is-ancestor 33569f8 'ade21af^' && echo "predates the 06-09 range"
      predates the 06-09 range

  `ade21af^..HEAD` is the 06-09 range — what a brief scoped to "the last gap-closure round" would
  have been given this round. The other unique finding, `:311`, sits in 06-09's own diff and was
  reachable either way. So the widening's measured marginal yield on its first run is **one finding
  in twenty-five**, and that finding is the self-contradicting bullet at the centre of the file's
  prong-4 argument.

  **Three findings from the orchestrator, over the surface no reader reads.** Every reader tree has
  `.planning/` stripped. These are the findings that fact makes invisible:

  **A. The fourth brief's own range specification is wrong, in two committed files.** The standing
  set at `06-UAT.md` and `WINDOWS.md` id 17 (in both the rendered row and the JSON fence) name
  `d67012e..HEAD` and gloss it as "the first commit of the 06-05 closure onward". Those are
  different ranges. Demonstrated:

      $ NEEDLE='36 headless sessions, three measured arms, four artifact families'
      $ grep -c "$NEEDLE" README.md                                        # live at HEAD
      1
      $ git diff d67012e..HEAD  -- README.md | grep '^+' | grep -c "$NEEDLE"
      0
      $ git diff 'd67012e^..HEAD' -- README.md | grep '^+' | grep -c "$NEEDLE"
      1

  A line `d67012e` added is live in `README.md` and invisible to the range the brief specifies.
  Authored `7323db5`, 06-09 — the commit that introduced the widening.

  **B. `LEGAL-REVIEW.md`:571 — "an unexcluded sweep returns six."** Recorded in full as finding 12
  of test 22. It returns seven. The control at `f547989` returns exactly six, so the sentence was
  true when written and was falsified by `10cfa1e`, its own round's SUMMARY commit. **The
  structural point:** a round's self-audit runs before its SUMMARY exists, so a command literal
  whose result the SUMMARY can change cannot be audited from inside the round that writes it. This
  is the third consecutive round in which a recorded command literal was falsified by the act of
  recording it or by what followed, and the first in which the falsifying commit is one the
  self-audit could not have seen.

  **C. `06-UAT.md`, test 20's `reported:` line and the matching `reason:` in its gaps block —
  "four of its six findings were also reached … Its two unshared findings are both the same
  shape."** The evidence block directly beneath the `reported:` line records **three** numbered
  findings and **four** converged ones — seven, with three unshared. The third unshared finding, a
  ledger row's reader count, is also not the same shape as the two it is grouped with. Both figures
  appear in exactly these two places and did not propagate to `VERIFICATION.md` or `WINDOWS.md`.
  Written by the round-5 UAT write-up and not re-read by 06-09, which edited the same file in the
  same round.
  *Corrected 2026-09-22 (06-10): this finding cited the two sites as `06-UAT.md`:1417 and `:1907`.
  At `66322b1`, the HEAD this round was written against, `:1417` resolved and `:1907` did not — the
  second site was at `:1895`, and `:1907` held an unrelated gaps-block line about
  `check_repo.py`:4479-4480. The citation was wrong when written, in the same file and the same
  round as the finding it records. Both sites are now named by their field rather than by line, the
  convention `LEGAL-REVIEW.md` adopted for the same reason.*

  **What this says about the diagnosis.** 06-09's task-18 self-audit read its own added sentences
  and found eight defects. It did not read the round-5 UAT record it was editing, and did not
  re-run the command literals its own SUMMARY commit would go on to change. Finding C is in the
  record that governs the round; finding B is in a shipped file. Both are inside the round's own
  work and outside the window its self-audit covers.

## Summary

total: 24
passed: 5
issues: 19
pending: 0
skipped: 0
blocked: 0

Round 1: tests 1-6 — 3 passed, 3 issues (G-06-2, G-06-3, G-06-6), all three resolved by 06-05.
Round 2: tests 7-9 — 1 passed, 2 issues (G-06-7, G-06-9), both resolved by 06-06.
Round 3: tests 10-12 — 0 passed, 3 issues (G-06-10, G-06-11, G-06-12), all closed by 06-07.
Round 4: tests 13-16 — 0 passed, 4 issues (G-06-13, G-06-14, G-06-15, G-06-16), all closed by 06-08.
Round 5: tests 17-20 — 0 passed, 4 issues (G-06-17, G-06-18, G-06-19, G-06-20), all closed by 06-09.
Round 6: tests 21-24 — **1 passed**, 3 issues (G-06-21, G-06-22, G-06-23), open.

**Round 6: the count rose and the diagnosis moved.** Twenty-five checkably-false statements, against
eighteen in round 5, seventeen in round 4, eleven in round 3, fourteen in round 2 and three in
round 1. The rise is not the tree getting worse — it is the briefs reaching further back, which is
what 06-09 widened them to do.

| | Round 5 | Round 6 |
|---|---|---|
| Total findings | 18 | **25** |
| Authored by *a* gap-closure round | 10 (56%) | **9 (36%)** |
| — by the **last** closure | 8 (44%) | **4 (16%)** |
| — by **earlier** closures | 2 (11%) | **5 (20%)** |
| Predating the closures entirely | 8 (44%) | **16 (64%)** |

**The last closing round's share more than halved** — 06-09 authored 4 of 25 against 06-08's 8 of
18. Its self-audit and its code-review gate move the number on the surface they cover. What they do
not cover is now measured: two of 06-09's four are outside any window a self-audit can see — one
falsified by the round's own SUMMARY commit, one in the UAT record the round was editing.

**Sixteen of the twenty-five predate every gap closure, and eight predate Phase 6 entirely.**
`check_repo.py`'s opening scope sentence and its violation-code catalogue (`5b124ba`, **plan
01-01**, the commit that created the checker), `SOURCES.md`'s review stamp (`0ba93f8`, 01-03),
`RESULTS-mod04.md`'s unanchored banner and CR-01 section (`fbe0aa6`, 03-09), both double-counted
sessions (`878b937`, 03-12) and one mutation-scope comment (`82535c7`, 03-16). Every one survived
six rounds of cold reads and every CI run since it was written.

**The README brief returned zero for the first time.** Six rounds have produced 3, 8, 2, 1, 3 and
**0** README findings. Two readers, cross-checked, both instrumenting the checker and both mutating
the stated counts. The single finding raised was refuted against a commit — `6c50822`,
"narrow two over-broad README claims" — that had already made the decision deliberately.

**Both of 06-09's structural changes were measured this round, and both paid.** The widened fourth
brief reached one finding a diff-scoped brief could not (`LEGAL-REVIEW.md`:383-384, authored by
06-08, 0 matches in `ade21af^..HEAD` and 1 in `d67012e^..HEAD`). The second sweep reader produced
four findings the first did not — 16% of the round — so the exit condition of zero marginal yield
for two consecutive rounds is not met and two readers stay.

**The dominant defect class changed.** Round 5's largest was scope overstatement about a mechanical
guard at 7 of 18. Round 6's is the **scope absolute** — a comment asserting that no other code, no
other check or no other file does something, written beside the code it describes and falsified by
code added later in the same file. Six of twenty-five, five of them in `check_repo.py`, three of
those inside one sixteen-line comment block that 06-09 edited and partly corrected. `T6` has the
full chain: 06-08's `3589842` added the check that falsified the sentence, and 06-09's `36ef0a9`
edited the same block without reading the neighbouring absolutes.

**Zero of the twenty-five is a regression of an earlier fix.** Readers 1 and 2 re-verified the
round-5 README corrections, readers 3 and 4 the eight round-5 LEGAL-REVIEW corrections including
the re-anchored citations, and all hold. Three reader claims were refuted or corrected on
verification rather than recorded: README's layout-tree framing (refuted), reader 3's count of the
backward-bullet construction (corrected from four to six, finding stands), and the occurrence count
at `:616-617` (corrected from three to four by a wrap-tolerant check reader 4 alone ran).

**`WINDOWS.md` id 12's closure condition is a round that returns none. Six have not.**

Round 5's paragraph, kept for comparison:

**Round 5: the count did not fall, and the reason changed.** Eighteen checkably-false statements,
against seventeen in round 4, eleven in round 3, fourteen in round 2 and three in round 1. The
closing round's share fell — **8 of 18, against 10 of 17** — so 06-08's self-audit and its new
code-review gate did move that number, but not to zero, and three of the eight are the same shape:
the round asserting a property of its own new check that the check's own docstring, written in the
same batch, denies.

**And "the closing round" is the wrong frame.** By `git blame`, **ten** of the eighteen were
authored by *a* gap-closure round — eight by 06-08, plus `README`:196 by **06-05** and
`LEGAL-REVIEW`:913 by **06-06**. Those two have survived every round since they were written. The
other eight predate Phase 6's closures: `README`:53 (04-13), `README`:306 (04-08),
`LEGAL-REVIEW`:119 and :170 (06-02), :723 (06-04), `INIT-EVENTS.md` (02-10), `check_repo.py`:239
(03-03, where `03-03-PLAN.md`'s own frozen list already held fourteen against its prose's fifteen),
and `bench-deal-brief.md`:107 (05-02). Four rounds did not reach them because until round 3 every
brief named a file, and no reader had opened `evals/trigger/`, the `## Launch` section or
`artifact-patterns.md`'s label inventory until this one. **Zero of the eighteen are regressions
of an earlier fix**; all seventeen of round 4's corrections — ten in `LEGAL-REVIEW.md`, one in
`README.md`, four found by the sweep and two in the bench brief — were re-checked by readers who did
not make them, and every one stands. The user-facing derivative fix was re-verified rule by rule:
all 28 illustrated rules carry a constructive line in the file the notice names for them.

**The closing round broke two citations that were correct before it ran.** `f909d3c` added three
net lines to each derivative's preamble; `LEGAL-REVIEW.md`:526-527, the two derivative citations,
resolved at `38c873b` and point at blank lines now. 06-08 recorded six of this record's citations
drifting inside its own round (`LEGAL-REVIEW.md`:367-369) and anchored those six to symbols; these
two were outside that sweep because they are not `check_repo.py` citations. On both occasions
`record-citation-unresolvable` — the code built for this class — was silent, because the cited
lines still exist. Here it could not even reach them: `CITATION_RE` requires backticks the three
citations do not carry.

`WINDOWS.md` id 12's closure condition is a round that returns none. Five have not.

Round 4's paragraph, kept for comparison:

**Round 4 reverses the trend and says why.** Seventeen checkably-false statements, against eleven in
round 3, fourteen in round 2 and three in round 1 — and **ten of the seventeen were authored by commit
`908b90b`, the round-3 gap closure itself.** Every one of round 3's corrections was verified to hold by
readers who did not make them; the round that made them introduced more than it closed. The new fourth
brief, aimed at exactly that surface, was the highest-yield reader of the round on its first run.

Round 3's numbers, kept for comparison:

Eleven checkably-false statements that round, against fourteen the round before and three before that.
The corrections themselves are holding: all six round-2 LEGAL-REVIEW corrections and all eight
round-2 README corrections were re-checked by readers who did not make them, and every one stands.
What has not converged is the reading — every one of round 3's eleven findings is in text no earlier
brief pointed a reader at. By `git blame` on the cited lines: four in 06-05 text round 2 did not
reach, three in files no brief had ever named (reached only by the new sweep brief), and four
authored by the closing round itself while fixing something else. Zero are regressions of a fix.
WINDOWS.md id 12's closure condition is a round that returns none; this is not it.

## Gaps

- gap_id: G-06-2
  truth: "LEGAL-REVIEW.md's WINDOWS id-6 disposition rests on sound reasoning"
  status: resolved
  resolved_by: 06-05-PLAN.md
  resolved_at: 2026-09-21
  reason: "Reader verified against NUMBERING.md: the eight shipped dimension names spell MEDDPPCC, not the acronym, so 'it IS the acronym, letter by letter' is false; and Decision Criteria/Decision Process and Champion/Competition are freely swappable without changing the letter string, so 'reordering would produce a different word' is false. The disposition also tests one of SOURCES.md's four reproduction prongs, never reaching the coined-term-as-label prong its own step 3 recites."
  severity: major
  test: 2
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: "id-6 disposition (:161-198): false load-bearing premise; fourth reproduction prong untested"
    - path: "NUMBERING.md"
      issue: ":9 names the namespace MEDDICC over an eight-element table whose extra element is Paper Process"
  missing:
    - "Restate the id-6 reasoning on grounds that survive NUMBERING.md — short unprotectable labels, thin protection where expression merges with a mnemonic — or reopen the entry"
    - "Test the fourth reproduction prong (coined term adopted as this repository's own label) explicitly, as id 3 does for its prongs"
    - "Examine NUMBERING.md's PF-1 seven Command of the Message sub-blocks: an ordered list reproduced in its order, live ® mark, no acronym defence, examined by neither id 3 nor id 6"

- gap_id: G-06-3
  truth: "LEGAL-REVIEW.md cannot be read as a professional legal opinion"
  status: resolved
  resolved_by: 06-05-PLAN.md
  resolved_at: 2026-09-21
  reason: "Independent reader's verdict: parts of it can. The disclaimer does not reach the verdict layer — Gate status: PASSED sits above it at line 5, and the ledger's Fixed entries sit 400 lines below it stripped of every hedge. Specific sentences state conclusions about the author's own exposure rather than recording what was looked at."
  severity: major
  test: 3
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: ":5 Gate status: PASSED above the disclaimer; :138 'boundary not crossed'; :155 'by none exclusively'; :187 'trading on'; :240 'the disclaimer that makes...'; :428/:431 ledger Fixed against the :420 definition"
  missing:
    - "Move or rename Gate status so it does not read as clearance above the disclaimer, and reconcile it with the two name collisions :244-250 leaves open before wider distribution"
    - "Reword the two Disposition: headings to describe what was done rather than what was concluded"
    - "Cut or bound :155 'by none exclusively' and :187's 'could be seen to be trading on'"
    - "Replace :240-241's 'which is the disclaimer that makes...' with what the files state rather than what that accomplishes"
    - "Give the ledger a state for judgement-based closures; ids 3 and 6 are not Fixed under :420's own definition, and the 11/9/8 counts inherit it"

- gap_id: G-06-6
  truth: "No two passages of README contradict each other"
  status: resolved
  resolved_by: 06-05-PLAN.md
  resolved_at: 2026-09-21
  reason: "Two independent cold readers converged on three checkably-false statements, each contradicted by a committed file in this repository: a universal evidence-discipline claim the project's own checker docstring denies, a four-vs-three route count the runner's own docstring denies, and a superseded trigger figure the results file supersedes."
  severity: major
  test: 6
  artifacts:
    - path: "README.md"
      issue: ":231-233 'Every number this README carries is sourced from a committed results file under evals/, states the model versions and the date' — contradicted by tools/check_repo.py:405-415"
    - path: "README.md"
      issue: ":139-140 'the four install routes' — contradicted by run_routes.py:2, ROUTES tuple, RESULTS-routes.md:3 and README's own :104"
    - path: "README.md"
      issue: ":131-133 cites the superseded n=1 trigger figures; RESULTS-trigger.md:166 records the shipped description at OF_B/SN_B = 9/25, n=5"
  missing:
    - "Bound README:231's claim to the claim region, matching what the two checker codes actually enforce and what the checker docstring already says"
    - "Correct README:139-140 to three measured routes, or state that routes 1 and 2 collapse into the skill-on arm"
    - "Carry the Arm B n=5 figure for the shipped description, or say plainly that the n=1 run is superseded"
    - "Minor, same pass: :202 'one measured v1 limitation'; :7-8 'the one ... deal brief'; MOD-04's two thresholds at :135-136 vs :202-203; the five tree paths absent from 'What exists today'"

- gap_id: G-06-7
  truth: "LEGAL-REVIEW.md's id-6 restatement and its new PF-1 section contain no sentence a committed file falsifies"
  status: resolved
  previous_status: failed
  resolved_by: "06-06 tasks 9, 10, 11 (commits d56022c, b931161, 485de7b) — all six corrected, each checked against the file the reader cited. The PF-1 counterweight was corrected in all four places it had propagated to, and the id-29 disposition was re-read against the corrected facts rather than having them patched underneath it. Self-checked, not independently read: the closure condition remains a round-3 cold read."
  reason: "Two independent readers. Six checkably-false statements survive the restatement. The worst is the PF-1 counterweight at :289-291 and :299-301, which asserts the seven-element list appears in no shipped file — SKILL.md:63, output-styles/proof-first.md:87 and prompts/system-prompt.md:75 each carry it as a set in the table's order — and the error propagates into What remains open item 5 and ledger row 29, understating both the exposure and the remedy. The correction paragraph itself miscounts the freely-swappable positions as four when NUMBERING.md gives six."
  severity: major
  test: 7
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: ":289-291 and :299-301 — 'nothing a reader of the shipped skill sees names these seven elements as a set in this order' and 'no shipped file cites them', both false against SKILL.md:63, output-styles/proof-first.md:87, prompts/system-prompt.md:75"
    - path: "LEGAL-REVIEW.md"
      issue: ":204-207 'four of the eight positions' — NUMBERING.md:77-78 makes Paper Process/Pain a third same-initial pair, so six; the same paragraph spells M-E-D-D-P-P-C-C at :203"
    - path: "LEGAL-REVIEW.md"
      issue: ":236-237 'block headings in completeness-audit.md' — neither string occurs in that file"
    - path: "LEGAL-REVIEW.md"
      issue: ":268 cites NUMBERING.md:26-40; the PF-1 content is at :31-45 and the cited span excludes five of the seven elements"
    - path: "LEGAL-REVIEW.md"
      issue: ":296 'the same two live questions id 6 ends on' — :383-390 lists them as separate items 5 and 6 with different content"
    - path: "LEGAL-REVIEW.md"
      issue: ":16 declares the file append-only; commit 0b8a865 rewrote the id-6 section in place (-32/+64)"
  missing:
    - "Correct :289-291 and :299-301 to state that the seven elements ship in SKILL.md and both derivatives, and propagate to :383-384 and ledger row 29 — the counterweight that justifies leaving id 29 open is the false statement"
    - "Correct :204-207 to six positions, and the 0b8a865 commit-message undercount alongside it"
    - "Cut or correct :236-237's completeness-audit.md claim — the narrower true fact favours the entry"
    - "Correct the :268 line citation to NUMBERING.md:31-45"
    - "Reconcile :296 with :383-390, or state the two pairs differ and why id 29 still stays open"
    - "Reconcile the append-only rule at :16 with what 06-05 did — either restate the rule to permit correcting a falsified premise in place, or record the superseded text"
    - "Backlog, not blocking: prong 2's thinness test is not in SOURCES.md and its 'many independent publishers' clause is an unrecorded lookup; prong 4 records position instead of disposing against SOURCES.md:16"

- gap_id: G-06-9
  truth: "No statement in README is contradicted by a committed file in this repository"
  status: resolved
  previous_status: failed
  resolved_by: "06-06 tasks 1-8 (commits 4cb5c9b, 3e3dcd9, 251cad2, c850219, 3a37839, f10f8fc, d11b8a7, 467ed6e) — all eight corrected. Finding 2, the only one that shipped to installed users, also gained a check_repo.py code (benchmark-run-claim-stale, discrimination-proven). Finding 6 was closed by the second of the plan's two permitted outcomes, settled by a mutation probe against an unmutated control. Self-checked, not independently read: the closure condition remains a round-3 cold read."
  reason: "Two independent cold readers converged on four; three more found by one reader each or by the session. Eight in total. One was created by the 06-05 round itself (README still says the /config picker has not been observed while LEGAL-REVIEW.md:536-541 records observing it). One ships to installed users ('no benchmark has run' in artifact-patterns.md and both derivatives). One is the same defect class as G-06-6 #1 reintroduced in the paragraph rewritten to fix it, settled by a mutation probe with an unmutated control: README's inventory counts can be changed to any number and check_repo stays at 0 violations."
  severity: major
  test: 9
  artifacts:
    - path: "README.md"
      issue: ":86-88 and :89-91 — the /config picker 'has not been observed here' and is 'the one link in this route nothing here exercises'; contradicted by LEGAL-REVIEW.md:536-541 and ledger row 16, written this same round by commit 36fbf6c"
    - path: "skills/proof-first/references/artifact-patterns.md"
      issue: ":144 'no benchmark has run' — contradicted by README:187 and evals/benchmark/RESULTS.md:1; ships verbatim in output-styles/proof-first.md:695 and prompts/system-prompt.md:683; check_repo.py:4264's guard matches 'No benchmark has compared', a different literal"
    - path: "README.md"
      issue: ":134 'three runs against the shipped skill description' — RESULTS-trigger.md:101 records Arm A at sha 9049c7d8… against the shipped d5dd651a…; README's own :139-140 says so"
    - path: "README.md"
      issue: ":43-44 publish-location-drift 'fails the build if any ... stops agreeing' — check_repo.py:724-726 declares it compares owner segments only"
    - path: "README.md"
      issue: ":171-172 and :9-10 — bench-deal-brief.md is not what sessions are prompted with; run_benchmark.py:295 sends scenario['prompt'] only and the brief is read once inside --self-test at :1646"
    - path: "README.md"
      issue: ":264-265 'Different codes check those — catalog-count-mismatch ...' — that code reads SKILL.md, not README; mutation probe with control shows 0 violations over mutated README counts"
    - path: "README.md"
      issue: ":111-112 activation contrast — prompt-on scores 8 of 12 on the same MARKER_RE metric README cites for skill-on's 3 non-activations (RESULTS-routes.md:15-17)"
    - path: "evals/benchmark/bench-deal-brief.md"
      issue: ":10-12 still asserts 'This environment has no live network access' and calls the name-collision search an unrun item; LEGAL-REVIEW.md:617 books it Fixed with the premise expired"
  missing:
    - "Correct README:86-91 to record the /config observation and its stated limits, matching LEGAL-REVIEW.md:536-541 — a gap-closure round must not leave the two files disagreeing"
    - "Correct 'no benchmark has run' in artifact-patterns.md:144 and regenerate both derivatives; widen check_repo.py's STALE_COMPARISON_CLAIM guard to catch this literal too, since the guard for its sibling already exists"
    - "Correct README:134 to two of three runs, or drop the count"
    - "Bound README:43-44 to the owner-segment comparison the checker declares"
    - "Correct README:171-172 and :9-10 to the brief's own accurate relation — it grounds the scenario prompts rather than being sent to sessions"
    - "Correct README:264-265: name the codes that actually read README, or state plainly that the inventory counts are unenforced — the third-case sentence two lines later already shows the honest form"
    - "Decide README:111-112: either drop the contrast or carry prompt-on's 8 of 12 beside it"
    - "Reconcile bench-deal-brief.md:10-12 with ledger row 18"
    - "Backlog: README:188 'drafted twice' omits the 3 repeats; two rounds of readers have now tripped on it"

- gap_id: G-06-10
  truth: "LEGAL-REVIEW.md's reproduction-boundary material contains no sentence a committed file falsifies"
  status: resolved
  previous_status: failed
  resolved_by: "06-07 tasks 1-7, 13 (commit 908b90b). Task 1 was a decision: the review adopts check_repo.py's frozen seven-of-eight SOURCE_COINED_LABELS split over its own six-and-two, widening the prong-4 concession from two labels to seven; the disposition is unchanged and the entry now states why rather than leaving it to be noticed. The other six corrected against grep output, not recollection. Prong 2 additionally lost its unrecorded 'many independent publishers' premise — backlog, but inside a sentence two tasks had to rewrite. Self-checked, not independently read: the closure condition remains a round-4 cold read."
  reason: "Two independent readers, converging on five of seven. All six of round 2's corrections hold and were verified accurate; seven different checkably-false statements survive in the same material. The worst is that LEGAL-REVIEW.md:249-252 and :308 classify six of the eight MC names as ordinary business English while tools/check_repo.py:2952-2965 freezes seven of the eight as SOURCE_COINED_LABELS and makes them a build failure in shipped skill content — only 'metric' is excluded. The occurrence enumeration at :253-256, written by 06-06's own self-audit commit, is false against examples/deal-brief.md and evals/benchmark/bench-deal-brief.md, which both carry the two labels as section headings, and miscalls a production constant a fixture."
  severity: major
  test: 10
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: ":249-252 and :308 — the prong-4 six/two split of the eight MC names is the inverse of tools/check_repo.py:2952-2965's SOURCE_COINED_LABELS; :308 names 'Competition' as neutral English and :2963 names it as coined"
    - path: "LEGAL-REVIEW.md"
      issue: ":253-256 'the two appear only in NUMBERING.md, in this file, and in check_repo.py's fixtures' — false against examples/deal-brief.md:26,75,89 and bench-deal-brief.md:54,130,145,185; the repo's own matcher is IGNORECASE (check_repo.py:2974); check_repo.py:2958-2959 is a production constant, and 'Paper Process' is in no fixture there"
    - path: "LEGAL-REVIEW.md"
      issue: ":239 and :301 reinstate the mnemonic ground that the correction at :224-225 retired fifteen lines earlier"
    - path: "LEGAL-REVIEW.md"
      issue: ":298-299 'NUMBERING.md says so in its own words' — NUMBERING.md:33-35 declares a one-per-element correspondence and says nothing about order provenance anywhere in :31-54"
    - path: "LEGAL-REVIEW.md"
      issue: ":340-342 enumerates two files and a command and calls it 'three files'; :433 and :731 say 'three files and a regeneration'; the tree gives four (NUMBERING.md, SKILL.md, and both derivatives)"
    - path: "LEGAL-REVIEW.md"
      issue: ":253 'nowhere else that ships' presupposes NUMBERING.md ships; README.md:367-369 says it never ships to an installed user, and :255's 'the shipped tree' uses the opposite sense four lines later"
    - path: "LEGAL-REVIEW.md"
      issue: ":237 'each labelled with the shortest ordinary English' contradicts :250-252's finding that two of the eight are terms of art, thirteen lines apart in the same section"
  missing:
    - "Reconcile the prong-4 classification at :249-252 and :308 with tools/check_repo.py's SOURCE_COINED_LABELS — either the review adopts the checker's seven-of-eight split and re-reasons the prong on it, or it states why the two classifications answer different questions and the checker's is not the reproduction-boundary one"
    - "Correct :253-256: the two labels appear as section headings in both committed deal briefs, the matcher is case-insensitive, and check_repo.py:2958-2959 is a production constant rather than a fixture"
    - "Cut the mnemonic clause at :239 and the mnemonic contrast at :301, or restate why a ground the correction retired is still available here"
    - "Correct :298-299 — NUMBERING.md declares the element correspondence, not the order; the PF-1 order claim has to be argued exactly as id 6's was"
    - "Settle the rename cost once at four files, and make :340-342, :433 and :731 agree"
    - "Reconcile :253's sense of 'ships' with README.md:367-369, or say which definition this file uses"
    - "Reconcile :237 with :250-252"
    - "Backlog, not blocking: prong 2's 'many independent publishers' clause is a premise in no committed file and carries the thinness conclusion (second round it has been raised); :56 says two live questions where items 5 and 6 carry three; :39's bolded content-item count excludes id 29, which :344-345 classifies as a shipped-content decision"

- gap_id: G-06-11
  truth: "No statement in README is contradicted by a committed file in this repository"
  status: resolved
  previous_status: failed
  resolved_by: "06-07 task 8 (commit 908b90b). Outcome 2, with outcome 1 rejected on evidence — 20% carries four meanings in the bench brief and three in the examples brief, so varying one row would leave the claim false while looking fixed. Claim bounded in README and bench-deal-brief.md in the same commit, identical row named rather than hidden. The company/person/platform separation is now mechanically held over all nine invented names (was four), discrimination-proven against an unmutated control."
  reason: "Three independent readers converged on one statement. README:9-11 says the two deal briefs share 'no company, person, platform or figure'; examples/deal-brief.md:116 and evals/benchmark/bench-deal-brief.md:177 carry a byte-identical Canonical figures row (rfp-security-weight, 20%, same description), and both decision-criteria tables read 'Security posture | 20%'. Every other same-named key between the two briefs was deliberately varied. The claim has been in bench-deal-brief.md:8 since 05-02, but commit 3a37839 — 06-06's fix for round 2's finding 5 — is what imported it into README, so the round that closed G-06-9 opened this."
  severity: major
  test: 11
  artifacts:
    - path: "README.md"
      issue: ":9-11 'shares no company, person, platform or figure with the one the examples are written against' — contradicted by the identical rfp-security-weight row at examples/deal-brief.md:116 and evals/benchmark/bench-deal-brief.md:177"
    - path: "evals/benchmark/bench-deal-brief.md"
      issue: ":8 makes the same claim about itself and has since commit 1577910; it is false against its own :177 read next to examples/deal-brief.md:116"
  missing:
    - "Decide the substance first: either vary the bench brief's rfp-security-weight so the no-shared-figure claim becomes true, or drop 'or figure' from both README:9-11 and bench-deal-brief.md:8 and state what separation the two briefs do hold (company, person and platform, all three verified this round)"
    - "Whichever is chosen, both files must be changed in the same pass — README repeats the brief's own claim, so fixing one leaves the other false"
    - "Backlog: bound README:186-188 to what run_benchmark.py:1645 actually asserts — four names of the nine examples/deal-brief.md invents. Recorded as an observation on a 2-to-1 reader split, not a gap, and it is the same class as round 2's publish-location-drift finding"

- gap_id: G-06-12
  truth: "No two committed files in this repository state things that cannot both be true"
  status: resolved
  previous_status: failed
  resolved_by: "06-07 tasks 9, 10, 11 (commit 908b90b). lint.py's ceiling restated as the property that holds rather than put in the past tense, since an environment-dependent ceiling expires again; ledger row 28 six limits; run_conformance.py five fixtures. git grep for the no-network premise now returns only the three files stating it as expired."
  reason: "A whole-tree sweep bound to no named file — new this round, because rounds 1 and 2 pointed every reader at README or LEGAL-REVIEW.md and so could not reach a contradiction between two other files. Three checkably-false statements. The first is the expired no-network premise still asserted in evals/lint.py:98-100, the file evals/proxy-sources.md:37-38 explicitly routes the reader to for the full statement of that ceiling, and the round that was meant to remove it repo-wide (commit 467ed6e, 'sweep the expired no-network premise out of the tracked tree') missed it."
  severity: major
  test: 12
  artifacts:
    - path: "evals/lint.py"
      issue: ":98-100 'this environment has no live network access' asserted as present fact; contradicted by evals/proxy-sources.md:12-14, LEGAL-REVIEW.md:720, bench-deal-brief.md:16-17 and check_repo.py:3776-3779, and proxy-sources.md:37-38 points the reader at this docstring"
    - path: "LEGAL-REVIEW.md"
      issue: ":730 ledger row 28 'its four named limits' — RESULTS-routes.md:45-50 publishes six and run_routes.py:183-190 freezes REQUIRED_CAVEATS at six keys"
    - path: "evals/conformance/run_conformance.py"
      issue: ":22-23 and :313-315 say 'the three committed transcript fixtures' and name them exhaustively; :459-465 enumerates five and all five are committed"
  missing:
    - "Restate evals/lint.py:98-100's ceiling in the past tense as the other four files do, or cut the parenthetical — the ceiling itself (a URL is never fetched) holds regardless of the environment and does not need the expired premise"
    - "Correct LEGAL-REVIEW.md:730 to six named limits"
    - "Correct run_conformance.py:22-23 and :313-315 to five fixtures, naming the two -late-phrase files the same docstring's cases 8 and 9 already describe"
    - "Consider whether the sweep brief itself belongs in every future round: this reader found three statements in three files no earlier brief had named, at the same cost as a file-scoped reader"

- gap_id: G-06-13
  truth: "LEGAL-REVIEW.md's reproduction-boundary material contains no sentence a committed file falsifies"
  status: resolved
  previous_status: failed
  resolved_by: "06-08 tasks 1-7, 13, 15 (commits 2ace809, 0447175, 22c99f2, 3589842, 389bafa). All ten corrected against the file each reader cited. Task 1 restated the 'mechanically held' claim as the two-step argument it is — source-label-in-skill-content over SKILL.md and references/*.md, plus generate_derivatives.py --check byte-comparing the derivatives — and recorded the fenced-block ceiling the entry had not mentioned. Task 5 removed the correction tally rather than updating it, since a count restated each round is one more statement to keep true. Task 15 re-anchored the file's check_repo.py citations to named symbols after the new code's 36-line docstring shifted five of them, refuting the plan's assumption that line numbers were the only practical anchor. Self-checked, not independently read: the closure condition remains a round-5 cold read."
  reason: "Two independent readers, converging with a third on four. All seven round-3 corrections hold and the adopted seven-of-eight split is verified accurate line by line. Ten new checkably-false statements, nine authored by commit 908b90b while closing round 3. The worst is :288-291, which says the seven labels' absence from four files is 'mechanically held' by source-label-in-skill-content; check_repo.py:983 scopes that check to skills/*/SKILL.md plus references/*.md, so it never opens either derivative, and :322-323 rests the disposition on the claim. Two more are a sentence quoted from SKILL.md:63 that is not in SKILL.md, and the same line cited as both the rename's target and a sentence the rename leaves in place."
  severity: major
  test: 13
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: ":288-291 'mechanically held' — check_repo.py:983's SKILL_GLOB and the candidate set at :2991-2996 never open output-styles/proof-first.md or prompts/system-prompt.md; :322-323 inherits it"
    - path: "LEGAL-REVIEW.md"
      issue: ":435-438 quotes 'one per Command of the Message element' from SKILL.md:63; the phrase occurs only at NUMBERING.md:33-34 and nowhere in skills/, output-styles/ or prompts/"
    - path: "LEGAL-REVIEW.md"
      issue: ":426 names SKILL.md:63 as a by-hand rename target while :436-439 names it as a sentence the rename leaves in place; in SKILL.md:63 the source clause and the seven labels are one sentence, so a rename rewrites it"
    - path: "LEGAL-REVIEW.md"
      issue: ":429-431 'The count is git grep -l \"Positive Business Outcomes\" ... not an estimate' — that command returns five files, because LEGAL-REVIEW.md:387 and :430 carry the string"
    - path: "LEGAL-REVIEW.md"
      issue: ":426 cites NUMBERING.md:39-45 for the by-hand edit; NUMBERING.md:48 also carries a label"
    - path: "LEGAL-REVIEW.md"
      issue: ":297-300 'All three parts were wrong' — 'in this file' was correct and 'in check_repo.py's fixtures' was correct for Economic Buyer (check_repo.py:7000-7004, :7029, :7036, :7051, :7059); what failed was 'only'"
    - path: "LEGAL-REVIEW.md"
      issue: ":23-26 'Three corrections in this file' — eight lines now carry 2026-09-22 corrections from 06-07, named by the ledger at :811 and :836"
    - path: "LEGAL-REVIEW.md"
      issue: ":245-247 'not ordinary English at all' misstates the adopted split, which says source-coined; :291-298 records five of the seven in ordinary English use"
    - path: "LEGAL-REVIEW.md"
      issue: ":48 misquotes check_repo.py:2131-2133 inside quotation marks — 'list' for 'file'"
    - path: "LEGAL-REVIEW.md"
      issue: ":362-363 'Two of the four grounds ... did not survive' — three of the four bullets carry a dated correction"
  missing:
    - "Restate :288-291 as the two-step argument it actually is: source-label-in-skill-content holds SKILL.md and references/*.md, and generate_derivatives.py --check byte-compares the derivatives to those sources. Fix :322-323 to match, and record the fenced-block ceiling (check_repo.py:2999 strips fences) the entry does not mention"
    - "Correct :435-438 — the phrase is NUMBERING.md's alone — and reconcile it with :426 so SKILL.md:63 is not on both sides of the rename; the substance changes, since renaming does rewrite SKILL.md:63"
    - "Correct :429-431's provenance, or drop the sentence and keep the four-file cost with its four citations; add NUMBERING.md:48 to the by-hand range"
    - "Correct :297-300 to name 'only' as the word that failed"
    - "Update :23-26's correction count and date list to cover 06-07's eight, or restate the paragraph so it does not carry a count that every round invalidates"
    - "Correct :245-247 to 'source-coined' and re-check that prong 2's removal still follows"
    - "Correct the :48 quotation to 'file'"
    - "Correct :362-363 to three"
    - "Backlog, not blocking: id 6's Closed-on-reasoning label against its own definition at :793-796, now further from it because 06-07 narrowed prong 2; the PF-1 section's unrecorded Force Management read, which is the same defect 06-07 removed from id 6 and left in the parallel entry; 'live and unadjudicated'; the completeness-audit.md over-read; prong 3's whole-repo negative"

- gap_id: G-06-14
  truth: "No statement in README is contradicted by a committed file in this repository"
  status: resolved
  previous_status: failed
  resolved_by: "06-08 task 8 (commit 4f76e32). README's checker bullet no longer says it enforces all of the above; it names the surface the checker actually reads. The boundary was measured, not asserted — pathlib.Path.read_text/read_bytes/open instrumented over a live check_repo.py run, 23 files opened, 11 claimed-unopened confirmed absent and 17 claimed-opened confirmed present. Two of the plan's own listed items were refuted by that measurement and recorded rather than worked around: RESULTS-trigger.md IS opened, via CLAIM_SOURCE_GLOB. Mechanizing the measurement needs the checker to run itself under a tracer at build time; recorded as a candidate in WINDOWS id 17 rather than shipped half-working."
  reason: "Both round-3 corrections hold and every claim-region figure recomputes. One statement, standing since commit 58530a6 in Phase 1 and missed by four rounds of cold reads: README:175 says tools/check_repo.py enforces 'all of the above' over a 17-item inventory, and the checker reads none of pressure-tests.md, proxy-sources.md, scenarios.json, lint.py, the three other runners or the RESULTS files. check_repo.py:66-68 excludes evals/ from its scan roots outright, and README:289 says the opposite for one of those items."
  severity: major
  test: 14
  artifacts:
    - path: "README.md"
      issue: ":175 'enforcing all of the above' over the :136-174 inventory — zero hits in check_repo.py for seven of the named items; :66-68 excludes evals/; README:289 concedes 'check_repo.py will not do it for you'"
  missing:
    - "Bound README:175 to what the checker reads, naming the boundary the checker already declares at :66-68 — the third-category sentence at :286-289 already shows the honest form"
    - "Consider, separately, that check_repo.py:4-5's own opening sentence is narrower than the checker it introduces (reader 2's observation, not a README defect)"

- gap_id: G-06-15
  truth: "No two committed files in this repository state things that cannot both be true"
  status: resolved
  previous_status: failed
  resolved_by: "06-08 tasks 9, 10, 11 (commits f909d3c, 96030d8, cfff672). Task 9 first, because it was the only round-4 finding that reached an installed user: the derivatives' omission notice now names completeness-audit.md as where the 8 MC constructive lines live instead of SKILL.md, which mc-rule-in-skill forbids from ever carrying them; both derivatives regenerated in the same commit, 39 constructive lines each (31 PF + 8 MC). Task 11 replaced the caveat tally with caveat-count-matches-constant, asserting the rendered bullet count against len(REQUIRED_CAVEATS); mutation probe fails at seven bullets with the assertion's own message, unmutated control passes."
  reason: "Four contradictions from the whole-tree sweep, none in a file the other three briefs name, none created by 06-07, and all three of round 3's sweep fixes verified to hold. One ships to every installed user: both derivatives tell the reader that every rule the omitted worked-examples.md illustrates 'already carries its own constructive line in SKILL.md', while eight of those rules are MC rules that check_repo.py's mc-rule-in-skill gate forbids from SKILL.md and NUMBERING.md routes to completeness-audit.md."
  severity: major
  test: 15
  artifacts:
    - path: "tools/generate_derivatives.py"
      issue: ":183-186 writes the omission notice into both derivatives (output-styles/proof-first.md:27-30, prompts/system-prompt.md:15-18); worked-examples.md carries 8 '## MC-' rules, SKILL.md carries 0 '### MC-' headings, and mc-rule-in-skill (check_repo.py:144-152) makes an MC rule in SKILL.md a build failure"
    - path: "tools/check_repo.py"
      issue: ":4235-4237 'until then this repository makes no such claim' about route equivalence; README:113-115 and evals/routes/RESULTS-routes.md:1-3 publish it, and :4279-4284 is built on the opposite premise"
    - path: "tools/generate_derivatives.py"
      issue: ":8-11 'Phase 5's benchmark is the only place such a statement could ever be sourced from'; the same script's _render_preamble() at :189-193 sources it from evals/routes/RESULTS-routes.md, and :168-175 says the old denial stopped being true at 04-15"
    - path: "evals/benchmark/run_benchmark.py"
      issue: ":476-479 'The five caveats EVAL-10 requires' and 'the same five keys', repeated at :2373; REQUIRED_CAVEATS holds six, RESULTS.md renders six, README:229 says six"
  missing:
    - "Correct the derivatives' omission notice at generate_derivatives.py:183-186 and regenerate both — the honest form names where MC constructive lines live (completeness-audit.md, which the derivatives already carry) instead of claiming SKILL.md carries them. This is the only round-4 finding that reaches an installed user; do it first"
    - "Correct check_repo.py:4235-4237 to match what :4279-4284 already assumes"
    - "Correct generate_derivatives.py:8-11 to name RESULTS-routes.md as the source its own output cites"
    - "Correct run_benchmark.py:476-479 and :2373 to six, and consider rendering the count from len(REQUIRED_CAVEATS) so a comment cannot drift from the constant beneath it"

- gap_id: G-06-16
  truth: "The sentences a gap-closure round adds are checked before the round closes"
  status: resolved
  previous_status: failed
  resolved_by: "06-08 tasks 12, 14 (commits 2e93a0c, 33569f8). The 20% meaning-count was removed rather than restated — a count of meanings is not checkable by any command, and the argument for not varying the figure does not need it. The platform disjointness was asserted rather than split: no-platform-collision checks the six platform names examples/deal-brief.md gives as migration source and target are absent from the bench brief, proven with a mutation probe (appending 'Amazon EC2' fails, exit 1) and an unmutated control (exit 0, brief byte-identical). The fourth brief is kept permanently; task 14 ran it against this round's own added lines and found seven more defects before the round closed, and the code-review gate then found two more in the round's own new check."
  reason: "The new fourth brief, aimed at the closing round's own added lines, was the highest-yield reader of round 4 on first use. Beyond converging with the LEGAL-REVIEW readers on four findings, it reached two neither could: bench-deal-brief.md:18-20's '20% carries four different meanings inside this brief alone and three inside the other', which is wrong under both counting rules (raw occurrences are four and four; distinct meanings are two and three), and :10-12's presentation of the platform-list disjointness as mechanically held when run_benchmark.py:1649-1659 asserts only the nine names and no code compares platforms."
  severity: major
  test: 16
  artifacts:
    - path: "evals/benchmark/bench-deal-brief.md"
      issue: ":18-20 'four different meanings inside this brief alone and three inside the other' — raw occurrences are 4 and 4 (bench :128, :155, :187, :189; examples :63, :66, :87, :116); distinct meanings are 2 and 3; the sentence justifies not varying the figure"
    - path: "evals/benchmark/bench-deal-brief.md"
      issue: ":10-12 and :20-22 present 'no shared company, person or platform' as mechanically held; run_benchmark.py:1649-1659's tuple holds nine names and no platform, and no committed code compares the two briefs' platform lists"
  missing:
    - "Correct the 20% count to one stated rule, or drop the count and keep the conclusion — the argument for not varying the figure does not need a number this fragile"
    - "Split the mechanical claim at :10-12 from the authored one: the nine names are asserted by run_benchmark.py --self-test; the platform disjointness is an observation. Either say so, or add the platform assertion to the self-test the way the entity assertion was added in 06-07"
    - "Keep the fourth brief permanently: on its first run it found 2 defects no other brief reached and confirmed 4 more, and 10 of round 4's 17 findings were in the closing round's own added lines"

- gap_id: G-06-17
  truth: "No statement in README is contradicted by a committed file in this repository"
  status: resolved
  previous_status: failed
  resolved_at: 2026-09-22
  resolved_by: "06-09 tasks 1-3 (commits ade21af, 80a8bfd, e6dfe0b), plus self-audit commit 05f2233. README:196 bounded to the three registry lists proxy-sources.md actually governs; the output-styles claim scoped to the local clone with the plugin-install case the checker docstring names disclosed as untested; the regeneration trigger corrected from \"any of its reference files\" to the generator's four named sources. The round's own self-audit then caught that task 3's rewrite had narrowed a true claim into a false one and corrected it before the round closed. Self-checked, not independently read: the closure condition remains a round-6 cold read."
  reason: "Round 4's correction holds and verifies exactly — an instrumented live run of check_repo.py opens the 23 files README enumerates, file for file, and both README readers reproduced it independently. Three new statements, none in text any recent round touched. The widest is README:196, which offers evals/proxy-sources.md as the published source for every term evals/lint.py counts as a proxy; the file holds exactly the 30 terms of PROXY_TERMS, SUPERLATIVE_TERMS and HEDGE_TERMS, while the linter also matches 18 CLAIM_VERBS and 7 CONDITION_CUES and labels the first group '(PF-2.1 proxy)' in its own violation string. lint.py:146-147 says so itself: 'Frozen here, not registry-sourced'."
  severity: major
  test: 17
  artifacts:
    - path: "README.md"
      issue: ":196 'the published source for every term `evals/lint.py` counts as a proxy' — 25 terms the linter matches and reports on have no row in evals/proxy-sources.md (evals/lint.py:148-156 vs the file's 30 rows). Authored by 441b344, the 06-05 gap closure"
    - path: "README.md"
      issue: ":53-54 '`output-styles/` at this repository's root is … not a directory Claude Code scans' — tools/check_repo.py:4118-4122, the docstring of the check that owns this README claim, says it 'is scanned only once the repository is installed as a plugin'; .claude-plugin/marketplace.json:11 sets source './'"
    - path: "README.md"
      issue: ":306 'or any of its reference files' — README fixes that at five (:176, layout tree); tools/generate_derivatives.py:44-46 states the same step over 'the four named reference files' and :97 excludes worked-examples.md, so an edit to the fifth is invisible to --check and skill-derivative-stale"
  missing:
    - "Bound README:196 to the three lists proxy-sources.md actually governs — the file's own :5-7 already names them (PROXY_TERMS, SUPERLATIVE_TERMS, HEDGE_TERMS) and that sentence is the honest form"
    - "Reconcile README:53-54 with check_repo.py:4118-4122: either scope README's sentence to the local-clone routes it sits under, or state the plugin-install case the checker's docstring names. One of the two files has to move"
    - "Correct README:306 to the four generator sources, or say that editing worked-examples.md needs no regeneration and why — the generator's OMITTED_SOURCE comment already carries the reason"
    - "Consider asserting the proxy-sources coverage mechanically: proxy-term-unsourced already checks the three lists; a fourth assertion over CLAIM_VERBS and CONDITION_CUES would either close the gap or force README's sentence to narrow"

- gap_id: G-06-18
  truth: "LEGAL-REVIEW.md's reproduction-boundary material contains no sentence a committed file falsifies"
  status: resolved
  previous_status: failed
  resolved_at: 2026-09-22
  resolved_by: "06-09 tasks 4-11 (commits 89a9547, dcc4643, aa6da1d, 0df417e, d9aef55, 44cc648, 672a222, e43829f). The two citations f909d3c broke were re-anchored by quoted string rather than by line number, the anchor form 06-08 had already proven against insertions. Two corrections went against the plan: d9aef55 withdrew a correction because the quotation it retired was accurate, and 44cc648 deleted a claimed machine check rather than describing it, because the check never existed. 0df417e ran prong 3's missing command and recorded its output instead of asserting the result. Self-checked, not independently read: the closure condition remains a round-6 cold read."
  reason: "All ten round-4 corrections hold, and the symbol anchors 06-08 substituted for line numbers survived the insertions made after them — the property they were chosen for. Eight new statements. The sharpest is that two of the three citations carrying this section's own central correction now point at blank lines: output-styles/proof-first.md:87 and prompts/system-prompt.md:75 both resolved correctly at 38c873b and were broken by f909d3c, the closing round's own first task, which added three net lines to each derivative preamble. Two more are the round's own new sentences: the prong-3 'one command, recorded above' that names a command answering prong 2, and a correction marker that retires an accurate quotation."
  severity: major
  test: 18
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: ":523-527 — output-styles/proof-first.md:87 and prompts/system-prompt.md:75 are blank lines; the sentence is at :90 and :78. Both resolved at 38c873b; broken by f909d3c"
    - path: "LEGAL-REVIEW.md"
      issue: ":169-173 'Two rows were confirmed against bibliographic edition records … Three … public vendor pages' — SOURCES.md:43, :53, :54 are three openlibrary.org edition records; the 2+3 partition covers five of six rows"
    - path: "LEGAL-REVIEW.md"
      issue: ":536-537 'a live unadjudicated mark' — the phrase :476-485 records as withdrawn ('not established and not claimed'), :505 says was answered by restatement, and :437 carries in narrowed form"
    - path: "LEGAL-REVIEW.md"
      issue: ":506-507 'Prong 3's whole-repo negative … answering it cost one command, recorded above' — prong 3 (:280-282) records no command; the only whole-repo sweep (:269) is attached to prong 2 at :263-272"
    - path: "LEGAL-REVIEW.md"
      issue: ":53-55 the 'list'/'file' correction — check_repo.py:484-487 (module docstring) carries the quoted sentence verbatim with 'list'; :2177-2179 (function docstring) carries it with 'file'. The retired quotation was accurate; round 4's finding that prompted the correction was wrong"
    - path: "LEGAL-REVIEW.md"
      issue: ":722-724 'the machine check that enforces it — a configured remote requires a passed gate' — check_repo.py imports no subprocess (grep -c → 0) and no committed code conditions anything on a configured remote"
    - path: "LEGAL-REVIEW.md"
      issue: ":910-913 'seven self-tests in `evals/`' — six scripts under evals/, six `python3 evals/` commands in ci.yml; 3+7+1 also breaks 'All ten CI commands' in the same sentence. Never true, at f54edf7 or now; authored by the 06-06 gap closure"
    - path: "LEGAL-REVIEW.md"
      issue: ":119-120 and :651 'The two TSDR endpoints that failed … answered this time' — :131-133 and the :648 table row record the second returning HTTP 401, 'Recorded as a failed lookup'; :57-58 says two lookups failed"
  missing:
    - "Re-anchor :523-527's three citations by quoted string, the convention 06-08 adopted for the deal briefs and for check_repo.py — a generated file's line numbers move whenever its preamble does, and this round moved them"
    - "Correct :169-173 to three edition records and three public pages, so the partition covers all six rows"
    - "Remove 'live unadjudicated' at :537, the one occurrence the round-4 withdrawal missed"
    - "Correct :506-507 — either name the command that answers prong 3's negative, or record that prong 3's negative has none, as :266-272 did for prong 2"
    - "Correct :53-55: the checker states the ceiling twice, with 'list' in the module docstring and 'file' in the function docstring. Say that, and withdraw the misquote finding rather than leaving a correction marker over an accurate quotation"
    - "Correct :722-724 — delete the machine-check clause; the ordering argument stands without it"
    - "Correct :910-913 to six"
    - "Reconcile :119-120 and :651 with :131-133 — say the status view answered and the API endpoint returned 401, which is what the table already records"
    - "Backlog, not blocking: id 6's Closed-on-reasoning label against its own definition; the PF-1 section's unrecorded Force Management read; the completeness-audit.md over-read. Carried from round 4 unchanged"

- gap_id: G-06-19
  truth: "No two committed files in this repository state things that cannot both be true"
  status: resolved
  previous_status: failed
  resolved_at: 2026-09-22
  resolved_by: "06-09 tasks 12-16 (commits 392c071, 36ef0a9, bac300a, ca5fdbf, afe8ea2). The citation code's two comments were corrected against their own docstring rather than the docstring softened to match them. bac300a is the round's one new assertion: INIT-EVENTS.md's key set corrected to 24 and held by a new run_trigger_test.py self-test case, discrimination-proven with a mutation probe against an unmutated control. ca5fdbf corrected the element-label count to fourteen and stated the counting rule, so the next reader can re-derive it instead of trusting it."
  reason: "All four of round 4's sweep fixes hold, and the one that reached every installed user verifies rule by rule — all 28 rules worked-examples.md illustrates carry a constructive line in the file the corrected notice names for them. Four new contradictions, in three places no brief has ever named. One is the closing round's new check contradicting its own module docstring in the same commit: the block comment says nine cold-read findings were citations that stopped resolving and 'This code closes that class', while the docstring says the code 'catches none of them' and fired ZERO times over 435 commits."
  severity: major
  test: 19
  artifacts:
    - path: "tools/check_repo.py"
      issue: ":4470-4476 'Nine were the same mechanical defect … This code closes that class' against :986-994 'This code catches none of them … future insurance against three shapes that have not yet occurred here' and :978-981's zero-firing replay. Both written by 3589842"
    - path: "evals/trigger/INIT-EVENTS.md"
      issue: ":72-81 'The init event's full top-level key set' lists 23 keys; all 140 committed transcripts carry 24, the missing one being `subtype` — the key the file's own extractor at :42 selects on"
    - path: "tools/check_repo.py"
      issue: ":239 and :2885 'the fifteen frozen element labels' — artifact-patterns.md carries 13 in the four family sections, 14 with 'No family fits:', 18 counting the Order lines. Never true; 03-03-PLAN.md:354's own frozen list holds 14"
    - path: "evals/benchmark/bench-deal-brief.md"
      issue: ":106-107 'took 11 months — shorter than … the audit window' against :118-120 'that audit window is close to, but shorter than' the same duration; the file's own canonical figures (:194 = 6, :208 = 11) settle it against :107"
  missing:
    - "Correct check_repo.py:4470-4476 to match the docstring beneath it — the nine findings were citations that resolved and pointed at the wrong content, which this code does not catch. The comment is the one place a future reader looks for why the code exists; it must not claim the coverage the docstring spent a paragraph disclaiming"
    - "Correct INIT-EVENTS.md's reproduced key set to the 24 keys the transcripts carry, or stop calling it 'full'. Reproducible: unpack transcripts-cat10.tar.gz and sort the init event's keys"
    - "Correct the fifteen to the count artifact-patterns.md actually carries, in both check_repo.py:239 and :2885, and state the counting rule — 'element label' is defined in no committed file, which is why the miscount survived from Phase 3"
    - "Correct bench-deal-brief.md:107 to 'longer than', matching the canonical figures and the parallel sentence at examples/deal-brief.md:41"
    - "Consider asserting the two timeline figures against the prose, the way caveat-count-matches-constant now asserts the caveat count — the canonical figures table is already machine-readable"

- gap_id: G-06-20
  truth: "The sentences a gap-closure round adds are checked before the round closes"
  status: resolved
  previous_status: failed
  resolved_at: 2026-09-22
  resolved_by: "06-09 tasks 17, 19-21 (commits 7852bf3, 7323db5, a15e357, c5a5a4f). The two remaining closing-round statements were corrected, and the brief itself was changed rather than only its output: the fourth brief's input widened from the last round's diff to the union of every gap-closure commit range, and the whole-tree sweep went from one reader to two, both decisions recorded in this file rather than only in a commit message. Task 18's self-audit found eight defects in this round's own added prose and fixed them; the code-review gate then found a ninth, that the round's own new assertion was narrower than the claim it guards (c5a5a4f). Neither substitutes for the independent read: the closure condition remains a round-6 cold read."
  reason: "The fourth brief justified itself a second time and this round converged rather than standing alone: four of its seven findings were also reached by the LEGAL-REVIEW readers or the sweep. Two of its three unshared findings are the same shape as each other and as one the sweep found — the round asserting a property of its own new code that the code's own docstring denies — and the third is a reader count in a ledger row. (Figures corrected 2026-09-22 by 06-10 task 22; they read six, two and 'both the same shape'.) 8 of round 5's 18 findings are in 06-08's added lines, down from 10 of 17, so the self-audit and the new code-review gate moved the number without closing it. But git blame over all eighteen makes the real figure TEN authored by a gap-closure round: README:196 by 06-05 and LEGAL-REVIEW:913 by 06-06, both surviving every round since. The brief is scoped to the last round's diff and structurally cannot see the earlier ones."
  severity: major
  test: 20
  artifacts:
    - path: "tools/check_repo.py"
      issue: ":997-999 'it reads strip_fences() output, like every other content-scanning code here' — :778-779/:3871-3872, :4122-4123 and :4371 each state they read raw and never call strip_fences. Authored by 1d477f5, the commit fixing two other findings in the same new check"
    - path: "tools/check_repo.py"
      issue: ":4479-4480 'Both already carry `path`:N citations' — the file's own CITATION_RE returns 9 matches in LEGAL-REVIEW.md and 0 in README.md"
    - path: "LEGAL-REVIEW.md"
      issue: ":976 ledger row 12 'Round 1's two readers returned PASS on the named question' — :865-866 and 06-UAT.md test 4 both record one reader; :843-848 records five readers that round, the only pair being the README hunt, which returned three false statements"
  missing:
    - "Correct check_repo.py:997-999 — name the checks that read raw, or drop the comparison; the claim adds nothing the sentence needs"
    - "Correct check_repo.py:4479-4480 — README carries no `path`:N citation; say the scope is where citations are written today plus where they may be written next, which is what the following sentence already says"
    - "Correct LEGAL-REVIEW.md:976 to one reader, and reconcile the row's reader counts with :843-848"
    - "Keep the fourth brief. Second run, second time it justified itself; its convergence with the other briefs this round is evidence the surface is now covered rather than evidence the brief is redundant"
    - "Widen the fourth brief past the last round's diff. Its blind spot is now measured: two of round 5's findings were authored by 06-05 and 06-06 and have survived every round since, and no brief scoped to one diff can reach them. The cheap form is to run it over the union of every gap-closure commit range, which is 06-05..HEAD"
    - "Consider a second sweep reader. Eight of round 5's eighteen predate Phase 6's gap closures, in evals/trigger/, the ## Launch section, artifact-patterns.md's label inventory and the bench brief's timeline — all reached only because the sweep brief names no file. One sweep reader found four; a second would double that sampling at the cost of one session"

- gap_id: G-06-21
  truth: "LEGAL-REVIEW.md's reproduction-boundary material contains no sentence a committed file or a cited source falsifies"
  status: failed
  reason: "All eight round-5 corrections hold, and the quoted-string anchors 06-09 substituted for the citations f909d3c broke survived every insertion made after them — the property they were chosen for. Twelve new statements. The sharpest is :188-190: the file's own account of how its six sources were confirmed says three rows matched a bibliographic `by_statement` field exactly, and the MEDDICC record carries no such field and has carried none since 2023, so the claim cannot be rescued as drift. Four more are scope or count absolutes the file states about itself, including one whose supporting grep the file's own later edits falsified, and one — ledger row 15's 'AST-based stdlib check' — that is the identical defect 06-09 deleted at :791-801 in the same round, left standing one screen away."
  severity: major
  test: 22
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: ":188-190 'Three rows were confirmed against bibliographic edition records whose `by_statement` field matched the row's author list exactly' — openlibrary.org/books/OL38629171M.json has no `by_statement` key, and its three authors (Mr Andy Whyte, Dick Dunkel, Jack Napoli) contradict SOURCES.md:43's single 'Andy Whyte'. revision 2 == latest_revision 2, last_modified 2023-02-04, so the field was absent on the 2026-09-21 review date too. Authored 6cc615a, 06-02"
    - path: "LEGAL-REVIEW.md"
      issue: ":311 quotes a prong clause `\"visual arrangement\"` that exists nowhere — SOURCES.md:15 reads 'a source's diagram or figure' and this file's own restatement at :206 reads 'a source's diagram'. Authored 0df417e, 06-09"
    - path: "LEGAL-REVIEW.md"
      issue: ":345 'as the `## Reproduction boundary` bullet above sets out' — the section opens at :198 and its first bullet is :353, below the citing sentence. Five other backward bullet references (:377, :401, :419, :553, :622) all resolve; this is an outlier of one. Authored 33569f8, 06-08"
    - path: "LEGAL-REVIEW.md"
      issue: ":383-384 'the two labels sit in `SOURCE_COINED_LABELS` … rather than in a fixture' contradicts :380-382 in the same bullet, which says Economic Buyer is inserted into two fixture builders. grep -in 'economic buyer' tools/check_repo.py returns 12 lines across eight functions. Authored 33569f8, 06-08 — reachable only by the widened fourth brief"
    - path: "LEGAL-REVIEW.md"
      issue: ":547-548 'the entity check under `## Reproduction boundary`' — inside that section (:198-648) the word 'entity' occurs only in the citing sentence. Authored 8f75cc6, 06-09, the self-audit commit removing two scope overstatements"
    - path: "LEGAL-REVIEW.md"
      issue: ":616-617 'once … and once' — four occurrences, not two; :457-458 carries the string wrapped across a line break and is invisible to grep. The sentence predicted this failure two lines later. Authored 0447175, 06-08"
    - path: "LEGAL-REVIEW.md"
      issue: ":23-25 'Every correction made on that basis carries a dated `*Corrected …*` marker' — :54 `*Correction withdrawn*` and :750 `*Updated*` are corrections on exactly that basis and the named grep returns neither. A third form, `*Clarified*` at :1026, is NOT counted: its qualification is arguable. Authored 22c99f2, 06-08"
    - path: "LEGAL-REVIEW.md"
      issue: ":771 'all four occurrences still agree with each other' — _publish_locations_in's docstring names seven structured positions, PUBLISH_LOCATION_CARRIERS holds three, literal occurrences are nine. No counting rule yields four. Authored 97927b8, 06-04"
    - path: "LEGAL-REVIEW.md"
      issue: ":1062 ledger row 15 'the AST-based stdlib check confirms the real import set' — no .py file in the tree imports ast or calls ast.parse/walk/Import. Same defect 44cc648 deleted at :791-801 in the same round. Authored b627fd3, 06-04"
    - path: "LEGAL-REVIEW.md"
      issue: ":1077 ledger row 30 'Not a falsehood — no committed file contradicts it' — evals/benchmark/RESULTS.md's n column reads 3 for all 32 cells and the raw records hold 12 drafts per scenario. The README sentence is already open item 30; the row's justification for keeping it is the new finding. Authored f54edf7, 06-06"
    - path: "LEGAL-REVIEW.md"
      issue: ":155-157 'The two existing sentences' — both contents are clauses of one sentence in NOTICES.md:70-73. Substance holds, count noun does not. Minor. Authored 6cc615a, 06-02"
    - path: "LEGAL-REVIEW.md"
      issue: ":571 'an unexcluded sweep returns six' — returns seven. Control at f547989 returns exactly six, so 10cfa1e, the round's own SUMMARY commit, falsified it five commits later. Found by the orchestrator; unreachable by any reader because reader trees strip .planning/"
  missing:
    - "Correct :188-190 to two rows, and say what the MEDDICC row was actually confirmed against — the author keys resolve, so the honest form names them rather than a field that is not there"
    - "Correct :311 to the prong's actual wording ('a source's diagram or figure') or delete the sentence: with no such clause there is nothing to narrow"
    - "Move :345's reference to the bullet's heading or quote its opening words, the anchoring convention this file already adopted for citations that drift"
    - "Correct :383-384 to say the labels sit in a production constant AND in fixture builders, which is what the bullet's own preceding sentence establishes"
    - "Correct :547-548 to name a check that exists, or drop the second example — the prong-3 sweeps alone carry the correction"
    - "Correct :616-617 to four, and state the wrap-tolerant counting rule, since a line-based grep cannot reproduce it. Three of five readers got three using grep"
    - "Correct :23-25 to the marker forms that actually exist, or normalise the three forms to one. A universal whose own grep misses two instances should not be stated as a universal"
    - "Correct :771 to a count that corresponds to something — seven checker-read positions is the figure the conclusion actually rests on"
    - "Delete ledger row 15's claim to an AST-based check, as 44cc648 did for the remote gate, rather than describing a check that does not exist"
    - "Correct ledger row 30's justification: RESULTS.md's n column does contradict 'drafted twice'. The row can still be kept open, but not on that ground"
    - "Correct :155-157 to one sentence with two clauses"
    - "Correct :571 to seven, and state the counting rule. Better: stop enumerating self-referential sweep results in prose, since every round has falsified one"

- gap_id: G-06-22
  truth: "No two committed files in this repository state things that cannot both be true"
  status: failed
  reason: "First run of the sweep at two readers. Thirteen findings across four files, eleven outside the two files the named briefs take as their subject, and eight authored in Phases 1 and 3. Two shapes dominate: the scope absolute in tools/check_repo.py — five instances, three of them inside one sixteen-line comment block 06-09 edited and partly corrected — and RESULTS-mod04.md contradicting itself about its own scorer, with a banner declaring every run block unanchored above fourteen anchored ones, and two arms each naming the same session as both the excluded timeout and a counted verdict. The published conformance figures are unaffected; the defect is in attribution prose. The second sweep reader produced four findings the first did not."
  severity: major
  test: 23
  artifacts:
    - path: "evals/conformance/RESULTS-mod04.md"
      issue: ":13 'Every run block recorded in this file was produced by an unanchored scorer' — 14 blocks carry the anchored evidence string 'within the first 400 chars'; :735-737 in the same file calls their figures 'a precise measurement, not an optimistic ceiling'. Authored fbe0aa6, 03-09"
    - path: "evals/conformance/RESULTS-mod04.md"
      issue: ":32, :43, :53 'every figure above this section' / 'Every run block recorded above this section' — the section opens at :11; lines 1-10 hold a title and one paragraph, and the first run block is :138. Authored fbe0aa6, 03-09"
    - path: "evals/conformance/RESULTS-mod04.md"
      issue: ":752/:756 Arm A names B-proposal-section 'first attempt' as both the excluded timeout and one of seven counted no-family verdicts. Blocks in timestamp order: 06:42:11 no-family, 06:48:34 timeout, 06:56:50 conformant — the timeout is the second attempt. Authored 878b937, 03-12"
    - path: "evals/conformance/RESULTS-mod04.md"
      issue: ":770/:772 the same defect in Arm B on A-rfp-answer: 07:40:29 no-family, 07:45:44 timeout, 07:53:55 conformant. Authored 878b937, 03-12. Bound: README:266-268's 3-of-10 and 4-of-10 match :760 and :776, so the published figures are unaffected"
    - path: "tools/check_repo.py"
      issue: ":4-5 'a structural and textual consistency check over NUMBERING.md, examples/deal-brief.md, and NOTICES.md' — a live run opens 23 files, confirmed by four independent tracers, and the same docstring defines codes over README.md, SOURCES.md, LEGAL-REVIEW.md, both manifests and both derivatives. Authored 5b124ba, plan 01-01"
    - path: "tools/check_repo.py"
      issue: ":33 'Violation codes implemented in this file:' followed by 57 entries; the file implements, self-tests and mutation-proves 58. The gap is catalog-opening-rule-count, defined :3085, registered :3163, dispatched :3176, mutation-entried :5601. Authored 5b124ba, plan 01-01 — the oldest finding this phase has produced"
    - path: "tools/check_repo.py"
      issue: ":448 and :1612 'a CI badge reports that ten offline scripts exited zero' — CI invokes eight distinct scripts with ten commands. README:188 states the distinction correctly and LEGAL-REVIEW:991-995 corrects this exact scripts-vs-commands confusion for another count. Authored 1b63ece, 06-03"
    - path: "tools/check_repo.py"
      issue: ":4753-4757 'No check other than results-breakdown-count-mismatch itself reads anything under evals/' and its supporting clause — check_readme_claim_unsourced reads all four evals/*/RESULTS*.md via CLAIM_SOURCE_GLOB (:1607), and check_readme_layout_tree_stale targets evals/ via LAYOUT_TREE_SCAN_DIR (:1624). Authored 82535c7, 03-16"
    - path: "tools/check_repo.py"
      issue: ":4759-4762 'No other check reads SOURCES.md' — check_source_gate_incomplete reads it (:2217-2220) and the module docstring at :484-485 says that check 'reads two committed files'; check_record_citations reads it too. Authored c0fca5f, 06-01"
    - path: "tools/check_repo.py"
      issue: ":4763-4765 'and no other check does' for LEGAL-REVIEW.md — check_record_citations reads it via CITATION_RECORD_PATHS (:4533). Falsified by 06-08's own 3589842; 06-09's 36ef0a9 then edited this same block and left three false scope absolutes in it. Authored e2e4aa2, 06-02"
    - path: "SOURCES.md"
      issue: ":3 'Last reviewed: 2026-09-10' — all six data rows read '(retrieved 2026-09-21)', proxy-sources.md:13-14 records the 2026-09-21 re-confirmation, and LEGAL-REVIEW:102 records moving NOTICES.md's stamp to 2026-09-21 while this one stayed. Authored 0ba93f8, plan 01-03"
  missing:
    - "Correct RESULTS-mod04.md:13 to name the anchored blocks as an exception, or move the banner below them — it is a file-wide universal sitting above fourteen counterexamples"
    - "Correct the CR-01 section's three 'above this section' references to 'below', or move the section beneath the material it covers"
    - "Correct both arms' per-session attributions to match the committed run blocks: the timeout is the second attempt in each case, not the first. State explicitly that N/M are unaffected so a future reader does not re-open the figures"
    - "Correct check_repo.py:4-5 to the scope README:180-183 already states correctly, or point it at that enumeration rather than restating it"
    - "Add catalog-opening-rule-count to the catalogue — and consider asserting the catalogue against the self-test's own emitted list, which is the one count in this repository that a check could hold for free"
    - "Correct 'ten offline scripts' to eight scripts or ten commands, at both sites"
    - "Correct all three scope absolutes in the :4753-4765 comment block against a tracer run, not against recollection. The block has now been edited twice while leaving false absolutes in it"
    - "Move SOURCES.md:3 to 2026-09-21, matching its own rows and the three NOTICES.md stamps"
    - "Consider whether the scope absolute is mechanizable: 'no other check reads X' is checkable by running the checker under the same Path.read_text tracer this round used. Unlike the semantic classes, this one has a command behind it — it is the enforcement-scope candidate WINDOWS id 17 already records, now with six instances instead of one"

- gap_id: G-06-23
  truth: "The sentences a gap-closure round adds are checked before the round closes, including those outside its own diff"
  status: failed
  reason: "The widened fourth brief paid on its first run, by one finding and measurably: LEGAL-REVIEW:383-384 was authored by 06-08 and returns zero matches in the 06-09 range a diff-scoped brief would have used. Convergence with the file-named readers was 3 of 5, against round 5's 4 of 7. But three findings came from the orchestrator over .planning/, which every reader tree strips — and two of those are inside 06-09's own work and outside any window its self-audit could cover: a command literal falsified by the round's own SUMMARY commit five commits after the audit ran, and a miscount in the UAT record the round was editing but did not re-read. The brief's own range specification is also wrong in two committed files."
  severity: major
  test: 24
  artifacts:
    - path: ".planning/phases/06-legal-review-gate-launch/06-UAT.md"
      issue: "The standing-set table names the fourth brief's input as `d67012e..HEAD` glossed as 'the first commit of the 06-05 closure onward'. Those are different ranges: a line d67012e added is live in README.md at HEAD, appears in `d67012e^..HEAD` and not in `d67012e..HEAD`. Authored 7323db5, 06-09 — the commit that introduced the widening"
    - path: ".planning/WINDOWS.md"
      issue: "id 17 carries the same `d67012e..HEAD` notation with the same gloss, in both the rendered table row and the JSON fence. The JSON is the source of truth: fix the fence and re-render, or `windows append` will block"
    - path: ".planning/phases/06-legal-review-gate-launch/06-UAT.md"
      issue: ":1417 and :1907 'four of its six findings were also reached … Its two unshared findings are both the same shape' — the evidence block directly beneath :1417 records three numbered findings plus four converged, i.e. seven with three unshared, and the third is a different shape from the two it is grouped with. Written by the round-5 UAT write-up; 06-09 edited this file in the same round without re-reading it"
  missing:
    - "Correct the fourth brief's range notation to `d67012e^..HEAD` at both sites, and re-render WINDOWS.md from its JSON fence"
    - "Correct 06-UAT.md:1417 and :1907 to seven findings and three unshared, and drop 'both the same shape'"
    - "Extend the closing round's self-audit past its own added sentences to the .planning/ records it edits in the same round. Two of this round's three orchestrator findings are in files 06-09 wrote to and did not re-read"
    - "Re-run every command literal the round commits into prose AFTER the SUMMARY commit lands, not before. The self-audit structurally cannot see the SUMMARY, and :571 is the third consecutive round in which recording a command changed its result"
    - "Add a fifth standing brief, or widen an existing one, to cover `.planning/`. Three of this round's twenty-five findings were invisible to all seven readers by construction, and the record that governs the round is the one surface no reader reads"
    - "Keep both structural changes. Change 1 reached one finding no diff-scoped brief could see; change 2's second sweep reader produced four unique findings, 16% of the round. Neither exit condition is met"
