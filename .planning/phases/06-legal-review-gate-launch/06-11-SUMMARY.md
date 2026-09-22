---
phase: 06-legal-review-gate-launch
plan: 06-11
subsystem: testing
tags: [legal-review, cold-read, checker, correction-markers, ledger, publish-location]

requires:
  - phase: 06-legal-review-gate-launch
    provides: "Rounds 1-7 of the cold read, the five-brief standing set, and the ten prior gap-closure plans whose text this round audits"
provides:
  - "Group C closed: the ten shipped-file findings of round 7, corrected across four shipped files"
  - "LEGAL-REVIEW.md's inline correction-marker convention retired — 44 markers removed, substance kept, the change record moved to git history"
  - "publish-location-drift extended to route 2's in-session install command, the third of three README commands carrying the placeholder"
  - "The standing set for round 8, with the two open calibration questions decided on the record"
affects: [round-8 cold read, LEG-04, LEG-05, gsd-verify-work]

actuals:
  tasks: 9
  commits: 9

tech-stack:
  added: []
  patterns:
    - "Corrections recorded in git history rather than quoted inline — `git log -S'<wording>' -- <file>` as the recovery path"
    - "AST attribution for enclosing-scope claims about Python source, in place of eye-counted grep output"
    - "Audit-hook (`sys.addaudithook` on `open`) file-scope tracing, which sees the interpreter loading the script itself"

key-files:
  created: []
  modified:
    - tools/check_repo.py
    - LEGAL-REVIEW.md
    - examples/deal-brief.md
    - evals/conformance/RESULTS-mod04.md
    - .planning/WINDOWS.md

key-decisions:
  - "C1 extended the checker rather than narrowing the README sentence. Bounding the claim would have left a real gap documented instead of closed; the probe showed `/plugin marketplace add` was unguarded and now fires like the other two."
  - "The new pattern is separate from MARKETPLACE_ADD_RE rather than folded into it, because that regex is also check_readme_install_paths' route-2 anchor, where the CLI form is the text being asserted present."
  - "C9 dissolved C3 and C2 rather than fixing them. Retiring the marker convention removes the taxonomy paragraph that must stay true about itself, and the false enumeration lived inside a marker."
  - "Corrections went to the ledger before the reproduction, every time, including the two the round discovered for itself. That ordering is round 7's structural finding (A5) and it bound this round twice."
  - "Groups A, B and D1 were left as backlog per the 2026-09-23 owner decision, except where a Group C edit forced a ledger row open. Two rows were forced and both were corrected ledger-first."
  - "Every plan figure was re-derived before its edit. Nine held; one did not — the plan said the marker convention authored findings C, D and E, and E is not marker-authored."

patterns-established:
  - "A record's change history lives in git, not in the record. The prose keeps what a correction established; git keeps what it replaced."
  - "A universal a single command must satisfy is not asserted at all where the qualified form will do — and where the universal is kept, the exception is named in the same breath."
  - "Mutation probes run against an unmutated sibling control, before and after the edit, with the message asserted and not only the exit code."

requirements-completed: []

coverage:
  - id: C1
    description: "publish-location-drift now reads all three README commands carrying the placeholder, not two"
    verification:
      - kind: other
        ref: "mutation probe on scratch copies with unmutated control: pre-edit :79 -> 0 violations, :66 -> fires; post-edit control 0, :66/:73/:79 each fire"
        status: pass
      - kind: unit
        ref: "python3 tools/check_repo.py --self-test; --mutation-test (58 codes)"
        status: pass
    human_judgment: false
  - id: C2C3C9
    description: "G-06-28 — the correction-marker convention retired, and the two findings it authored dissolved with it"
    verification:
      - kind: other
        ref: "grep -cE '\\*(Corrected|Added|Updated|Clarified) 2026-' LEGAL-REVIEW.md -> 0 (43 before); no `*Correction withdrawn*` remains; AST re-derivation of the economic-buyer partition (2 module-level, 9 in 6 functions)"
        status: pass
    human_judgment: true
    rationale: "Whether the prose still reads coherently with 1,154 words of correction apparatus removed is a judgement only a reader who did not write it can make. Round 8 is that reader."
  - id: C4
    description: "G-06-27 — the Human observations lead-in labels sections 1-3 by what they share, independence, rather than by a performance claim section 3's own heading contradicts"
    verification:
      - kind: other
        ref: "the three `###` headings read NOT OBSERVED / NOT PERFORMED AS A COLD READ / PERFORMED BUT NOT COLD; the new label matches all three"
        status: pass
    human_judgment: true
    rationale: "A summary label over three headings is a reading judgement; the headings are the check."
  - id: C5
    description: "G-06-26 — Q2/Q5's 20% has its own canonical row, the mid/low tiers are named as the bench brief names them, and the value-collision and bare-count ceilings are stated"
    verification:
      - kind: other
        ref: "pre-edit: deleting rfp-security-weight -> unlisted-figure 20% in three files, control 0. post-edit: same deletion -> 0 (the new -mid row covers it), both 20% rows deleted -> the three again, -low deleted -> 15% in the three"
        status: pass
      - kind: unit
        ref: "python3 tools/check_repo.py (0 violations, figure-order holds with -low before -mid before -top)"
        status: pass
    human_judgment: false
  - id: C6
    description: "G-06-26 — RESULTS-mod04.md addresses the anchored measurement by round, and counts nine genuine sonnet sessions rather than ten"
    verification:
      - kind: other
        ref: "awk NR>=198,219 | grep -c 'model=claude-sonnet-5' -> 10; the same piped to grep -c 'marker_at=None, marker=None' -> 1; the file's own :226 tally resolves as 10 opus + 1 sonnet"
        status: pass
    human_judgment: false
  - id: C7
    description: "G-06-25 — the checker docstring points at README's `## Status`, where the 23-file enumeration is, anchored by quoted string"
    verification:
      - kind: other
        ref: "awk NR>=332,400 README.md | grep 'opens 23' -> nothing; grep -n 'A live run opens 23 files' README.md -> 180, inside `## Status` (132). Audit-hook trace of a live run -> exactly 23 repository files, matching README item for item"
        status: pass
    human_judgment: false
  - id: C8
    description: "G-06-25 — the path-literal claim is stated at the edge that holds, in the checker and in both copies of ledger id 17"
    verification:
      - kind: other
        ref: "AST body scan excluding docstrings: check_record_citations [], check_source_gate_incomplete [], check_readme_claim_unsourced ['README.md' x2]. git grep for the universal outside .planning/ -> no output"
        status: pass
    human_judgment: false
  - id: D2D4
    description: "The round's own instruments: self-audit at the widened scope, and the standing set for round 8"
    verification:
      - kind: other
        ref: "the self-audit found two further sites of C8's universal (the ledger and its shipped reproduction) and one unstated ceiling in C5's own rewritten paragraph; gsd-tools windows status ok:true with table and JSON fence in agreement"
        status: pass
    human_judgment: true
    rationale: "Whether the standing set reaches round 8's defects is what round 8 measures; this round can only record it."

duration: 1 session
completed: 2026-09-23
status: complete
---

# Phase 06 Plan 11: Round 7 gap closure — the ten shipped-file findings, and the convention that authored two of them

Round 7's twenty-three findings split ten shipped and thirteen in `.planning/`. The project owner
bounded the blocking gate to files that ship on 2026-09-23, so this plan closed **Group C** — the
ten — and left Groups A, B and D1 as tracked backlog. Nine tasks, nine commits, all ten CI commands
green throughout.

## What changed

**C1 — `publish-location-drift` reads three README commands, not two.** `README.md`:45-46 claimed
the build fails "if any command or manifest carrying it stops naming the same GitHub owner segment
as the others". Measured on a scratch copy of HEAD with an unmutated control, before the edit:
mutating the owner in `npx skills add` fired; mutating it in the in-session
`/plugin marketplace add` left the checker at 0 violations. Extended rather than bounded — a
narrowed sentence would have documented the gap instead of closing it. After the edit all three
command positions fire and the control is still 0. Both docstrings enumerating the README positions
were updated with it, so the enumeration does not become round 8's finding.

**C9 — the inline correction-marker convention is retired, and it takes C3 and C2 with it.** The
convention required each in-place correction to quote the wording it removed, which wrote retired
strings back into the tracked tree for the next reader to check as live claims. Two of round 7's
three findings against this file were that mechanism reading back. 44 markers removed — the 43 the
convention's own grep matched, plus the `*Correction withdrawn …*` form that grep could not see,
which is the fifth form finding D was about. What each correction *established* — a measurement, a
ceiling, a concession to a reader — is kept in the file's own voice. What each correction
*replaced* now lives only in git history, which records it with date and authorship and cannot be
falsified by being written down. Both recovery commands were verified to resolve before being
written down.

This dissolves C3 rather than fixing it: with no marker taxonomy asserted, there is no universal
for a single grep to keep true. It dissolves C2 too — the false enumeration existed only inside a
06-10 marker — but the measurement was re-derived anyway, by AST rather than by eye:
`grep -in 'economic buyer' tools/check_repo.py` returns eleven lines, **two** module-level and
**nine** inside **six** functions, against the record's one and ten-inside-seven. The seventh
function it named, `_mutate_record_citation_unresolvable`, contains no occurrence.

**C4** relabels the Human observations lead-in by what sections 1-3 actually share. **C5** gives
Q2/Q5's 20% its own canonical row and renames the 15% tier `-low`, following the scheme
`bench-deal-brief.md` already uses; the same edit states the value-collision ceiling, because
adding the correct row does not let the build tell two 20% rows apart. **C6** addresses the
anchored measurement by round rather than by row position, and corrects ten genuine sonnet sessions
to nine. **C7** points the checker's opening docstring at `## Status`, where the 23-file
enumeration is. **C8** states the path-literal claim at the edge that holds.

## What the self-audit found

D2's widened scope — every file the round edits, not only its added sentences — paid twice.

C8's universal turned out to have three copies, all written by 06-10: the checker docstring C8
corrected, `WINDOWS.md`'s ledger id 17, and `LEGAL-REVIEW.md`'s reproduction of it. Correcting only
the docstring would have left the shipped reproduction stating the refuted form — round 7's
structural finding run in the opposite direction. Both were corrected, ledger first.

C5's own rewritten paragraph claimed the build holds four kinds of figure. It holds three;
`unlisted-figure`'s docstring declares the bare-count gap. Stated in the paragraph this round wrote.

## Deviations from Plan

**[Rule 1 — plan figure wrong] C9's finding attribution.** The plan states the marker convention
"authored findings C, D and E of this round directly". Verified against `06-UAT.md` before writing
it down: findings C, D and E are the three LEGAL-REVIEW.md findings, and C and D are
marker-authored, but E (`:907-908`, the "not performed" summary label) is a plain mislabel authored
by 36fbf6c, with no marker involved. The retired convention authored **two** of three, not three.
The corrected figure is what the new paragraph in `LEGAL-REVIEW.md` states. Verification:
`06-UAT.md` findings A-K at `:2140-2337`.

**[Rule 2 — missing critical] Ledger rows 12 and 17 had gone stale inside C9's blast radius.**
Both LEGAL-REVIEW cells said six rounds and "six have not"; seven have run. They sit inside the four
ledger cells C9 had to touch to remove their markers, so leaving them would have shipped a
checkably-false statement in the file this plan exists to clean. Corrected ledger-first through
`WINDOWS.md`'s JSON fence with the rendered table reconciled, then in the reproduction. Round 7's
figures were re-derived from `06-UAT.md` first, and "ten CI commands green every time" was
re-measured at `ad073b9`, the commit round 7 read: all ten pass. Commits fa6111f, 9656ca7.

**Total deviations:** 1 plan-figure correction, 1 scope addition forced by a blocking task.
**Impact:** both narrow the claims this round commits rather than widening the work.

## Backlog this round confirmed and did not close

Per the 2026-09-23 gate scope. All are real; none gates the phase.

- **Groups A and B** — thirteen `.planning/` findings, G-06-29. The ledger rows (A1-A5), the six
  record corrections (B1-B6).
- **D1** — SHA reachability as a checkable class, `.planning/`-scoped.
- **C8's universal survives in three more `.planning/` files**: `STATE.md`:48 (live status), and
  `06-VERIFICATION.md` / `06-10-SUMMARY.md` (historical records of what 06-10 decided, where
  rewriting would falsify the history rather than correct a live claim).
- **`06-UAT.md`:19's `round_7_result`** still reads "12 of 23 live in `.planning/`" where the same
  file's `:2593` and `:2609` read thirteen. 743b1bb corrected this count and reports having fixed it
  "at every site"; this site survived.

## The standing set for round 8, and the two calibration questions

**Carried unchanged:** the four file-named briefs, the whole-tree sweep at two readers (change 2),
the gap-closure-range brief at every closure range rather than the last (change 1), the
`.planning/` brief (change 3), the widened self-audit (D2), and the post-SUMMARY re-run of committed
command literals (change 5).

**What this round measured.** Change 1 paid one finding in twenty-three, a second consecutive round
of one-in-the-twenties; its exit condition — a round whose widening reaches nothing the narrow range
would have — is not met, so it stays. Change 2's second sweep reader returned two unique findings
(I and J); nonzero, so the earliest it can retire is after a round 8 that is also zero. Change 3
returned thirteen of twenty-three on its first run and has never had a second. Change 5 reached a
window 06-10's own pass could not, and this round ran it again (below).

**Decision 1 — the `.planning/` brief stays at one reader.** It is the highest-yield brief in the
set, and that is the argument against doubling it, not for: as of the 2026-09-23 gate scope
everything it finds is non-blocking backlog by construction, and a second reader would spend the
round's largest marginal cost where it cannot move the gate. What changes instead is coverage, at
no extra reader: round 7's reader declared three areas out of scope — phases 01-05 plan files read
in full, `.planning/debug/`, and `.planning/research/` — while its machine scan already covered all
187 files for citations, SHAs and command literals. Round 8's brief names those three as in scope.
Revisit if round 8's single reader again returns more than a third of the round.

**Decision 2 — a zero-refutation round is a caution about the round, not a calibration signal.**
Rounds 1-6 each refuted or corrected at least one reader claim; round 7 refuted none of
twenty-three. That is not evidence the readers got better. Thirteen of the twenty-three came from a
brief on its first pass over ground no reader had swept in six rounds, where the unambiguous
defects were still unpicked — the condition under which a refutation is least likely, not the
condition under which reader precision is best demonstrated. On the record: **no calibration
conclusion is drawn from round 7's zero.** The reading that will mean something is the fifth brief's
second run, and the threshold is set now so it cannot be set afterwards to fit the result — if
round 8 also refutes nothing across two consecutive runs of a brief over already-swept ground, the
verification step is the thing to examine, not the readers.

## Closure

Not closed by this plan, and deliberately. The requirement checkboxes stay unchecked and
`WINDOWS.md` id 12 stays open until a round of cold reads returns none; seven have not. Group C is
the blocking work and it is done, but this round wrote the sentences a round-8 reader will be
checking, and **seven consecutive self-checks have each missed what an independent read then
found.** The phase closes on round 8's read of the shipped tree, not on this plan's own verdict.

Next: `/gsd-verify-work 06` for round 8, against the standing set as recorded above.
