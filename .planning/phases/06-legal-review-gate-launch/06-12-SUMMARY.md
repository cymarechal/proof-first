---
phase: 06-legal-review-gate-launch
plan: 06-12
subsystem: testing
tags: [legal-review, cold-read, launch-gate, ledger, name-collisions, reverse-index]

requires:
  - phase: 06-legal-review-gate-launch
    provides: "Rounds 1-8 of the cold read, the five-brief standing set, and the eleven prior gap-closure plans whose text this round audits"
provides:
  - "Group E closed: the ten shipped-file findings of round 8, corrected across four shipped files"
  - "The launch gate stops misreporting itself — the two open name collisions have the ledger row the review had claimed since 06-02"
  - "Change 5 widened from the literals a round writes to a reverse index over the files a round edits, back-tested against the two findings that motivated it"
  - "The reproduced ledger re-rendered from the fence twice, at 34 entries and again at 35"
affects: [round-9 cold read, LEG-04, LEG-05, gsd-verify-work]

actuals:
  tasks: 12
  commits: 12

tech-stack:
  added: []
  patterns:
    - "Reverse index: for every file a round edits, re-run every committed literal and re-derive every stated measurement in every OTHER shipped file that names that path"
    - "Whitespace-flattened scanning, because a measurement split across a docstring wrap is invisible to a line-bounded regex"
    - "Command literals pinned to the commit they were true at, rather than restated live, where the rule behind them is not clearer than the number"

key-files:
  created: []
  modified:
    - README.md
    - LEGAL-REVIEW.md
    - tools/check_repo.py
    - evals/benchmark/bench-deal-brief.md
    - .planning/WINDOWS.md

key-decisions:
  - "E8 closed the launch-gate finding by making the routing land, not by deleting the sentences. examples/deal-brief.md still carries both names and the review states neither collision is closed by it, so the items are open; the defect was that seven rounds of prose claimed a register row that no round had ever written."
  - "One ledger row, not two, for the two rename decisions. They are one decision class with one owner, and the review's What-remains-open items 1 and 2 both point at it."
  - "E11's rule is file-scoped rather than sentence-scoped, and the ceiling is declared on the row. Sentence scope would have missed C1: at 06-11's tip the paragraph holding `grep -c '^|.*20%'` says 'each brief' and names examples/deal-brief.md only three paragraphs later."
  - "E10 restated the 13-spelled-cardinals claim by rule and pinned the 20% claim to two commits. The rule was clearer than the count in one case and not in the other, which is the line the plan drew."
  - "E1's first draft said README 'enforces only the first' of three kinds. Replaced before commit: the layout-tree check enforces part of the second kind, so the sentence now states each kind's enforcement separately."
  - "E6's first draft tied the pattern's ordinal offset to the Human observations section numbers. Those run 1-5 over 06-02's observations and have nothing to do with the Phase 4 rounds; two sequences that agree on 'fourth' by coincidence are not one sequence."

patterns-established:
  - "A record that says an item is routed somewhere is a checkable claim about that somewhere. Grep the destination before writing the sentence, and again before believing it."
  - "The reverse index runs after the SUMMARY commit, not at the task — the round's last edits are the ones most likely to falsify a literal elsewhere."

requirements-completed: []

coverage:
  - id: E1
    description: "G-06-30 (A1) — README's number taxonomy names three kinds and states each one's enforcement"
    verification:
      - kind: other
        ref: "sed -n '291p;299,309p' README.md reads as one taxonomy; :307's 'third case' now has an antecedent; python3 tools/check_repo.py -> 0 violations"
        status: pass
    human_judgment: true
    rationale: "Whether the three-kind taxonomy reads coherently end to end is a reading judgement. Round 9 is the reader."
  - id: E2
    description: "G-06-30 — the checker's 23-file count states why the 23rd is real, so the refutation does not have to be re-derived a third time"
    verification:
      - kind: other
        ref: "open-audit hook over a true `python3 tools/check_repo.py` subprocess: 23 files, 22 opened from frames inside the checker and 1 (tools/check_repo.py) from the interpreter's own load, matching the bullet item for item"
        status: pass
    human_judgment: false
  - id: E3
    description: "G-06-31 (B1) — the seven source labels' locations enumerated as measured, not summarised"
    verification:
      - kind: other
        ref: "_source_label_pattern run over the tracked tree per label: all seven in NUMBERING.md, five also in the two deal briefs, pain alone in four more; claim covers measurement for all seven with zero extras and zero missing"
        status: pass
    human_judgment: false
  - id: E4
    description: "G-06-31 (B2) — the two bullets that read one sweep at two scopes now name their scopes"
    verification:
      - kind: other
        ref: "outside .planning/, this record and the checker, 'decision process' and 'competition' resolve to NUMBERING.md alone (21 and 26 .planning/ files respectively); the header states that each bullet names its slice where narrower"
        status: pass
    human_judgment: false
  - id: E5
    description: "G-06-31 (B3) — the review-date universal restated over the dates that occur"
    verification:
      - kind: other
        ref: "every date attached to a performed check enumerated: 2026-09-21 (the source pass), 2026-09-22 (the three edition re-fetches), 2026-09-21 to 2026-09-23 (the cold-read rounds); each non-09-21 date is stated at its own check"
        status: pass
    human_judgment: false
  - id: E6
    description: "G-06-31 (B4) — ledger row 17's round count qualified to this phase"
    verification:
      - kind: other
        ref: "grep -rn 'rounds of the pattern' LEGAL-REVIEW.md .planning/WINDOWS.md -> 0 hits; the offset is stated against the Phase 4 rounds G-04-3/G-04-4/G-04-8 the WINDOWS.md description names"
        status: pass
    human_judgment: false
  - id: E7
    description: "G-06-31 (B5) — owner.url placed at marketplace.json's top level in both files that misplaced it"
    verification:
      - kind: other
        ref: "json.load: 'owner' in d -> True, 'owner' in d['plugins'][0] -> False; _publish_locations_in reads homepage/repository off plugins[0] and owner off data; both docstring and record corrected, :6334 and the catalogue entry left as they were"
        status: pass
    human_judgment: false
  - id: E8
    description: "G-06-31 (B7) — the launch gate's two open name collisions carried by ledger id 34"
    verification:
      - kind: other
        ref: "grep -c for each name in .planning/WINDOWS.md: 0 before, 2 after (fence and table); every WINDOWS.md id cited in LEGAL-REVIEW.md resolves to an entry whose status matches the word the review uses; windows status ok: true"
        status: pass
    human_judgment: true
    rationale: "Whether the two names should be renamed or kept is the project owner's decision, not this round's. The round's job was to make the register hold the question the review said it held."
  - id: E9E11
    description: "G-06-31 (B6) — the reproduced ledger re-rendered from the fence, after each of the round's two ledger writes"
    verification:
      - kind: other
        ref: "35 contiguous rows; dispositions 9 Fixed / 2 Closed on reasoning / 9 Waived / 15 Open folding to the fence's 11 fixed / 9 waived / 15 open with zero row-by-row mismatches; all four stated totals read 35; the parenthesised open-id list equals the fence's open set"
        status: pass
    human_judgment: false
  - id: E10
    description: "G-06-32 (C1 + C2) — the two committed literals a later round falsified"
    verification:
      - kind: other
        ref: "grep -c '^|.*20%': 4/4 at 2e93a0c, 4/5 at 4c3e911 — now pinned to both commits; SPELLED_CARDINAL_RE over examples/deal-brief.md: 13 at fd1b17b, 15 at 4c3e911, 16 at HEAD — now restated by rule in both docstring copies"
        status: pass
    human_judgment: false
  - id: E11
    description: "G-06-32 (structural) — change 5 widened to the reverse index, recorded as ledger id 35"
    verification:
      - kind: other
        ref: "back-test over 06-11's edit set at 8eca37d: 4 edited shipped files named by 5, 2, 7 and 12 other shipped files, surfacing 59 command literals and 994 stated measurements, returning both C1 ('four for each brief') and C2 ('not invented -- 13') by their own wording"
        status: pass
    human_judgment: false
  - id: E12
    description: "Self-audit of the round's own added sentences, then the post-SUMMARY pass at the widened scope"
    verification:
      - kind: unit
        ref: "all ten CI commands green; no [x] beside an UNVERIFIED requirement; LEG-04 and LEG-05 read Pending; windows status ok: true"
        status: pass
    human_judgment: false
---

# 06-12 — round 8 gap closure

Twelve tasks, five files, twelve commits before this summary. Group E is closed. G-06-34's
twenty-two `.planning/` findings stay backlog under the owner's 2026-09-23 gate
scope (ledger id 33), and nothing in this round reopened that decision: every
`.planning/`-vs-shipped divergence it touched had the record stale and the
shipped file correct, or the record current and the reproduction stale.

## The launch-gate finding

`LEGAL-REVIEW.md` told a reader at four sites that **Ardent Digital** and
**Gina Almeida** were open items routed to `.planning/WINDOWS.md` for a
decision before wider distribution. `grep -c` returned **0** for each name in
that file. The only collision rows — ids 1 and 18 — both read `fixed`, and the
reproduced ledger's own row 1 said a collision "is routed as a new open item"
that did not exist.

The items are genuinely open: `examples/deal-brief.md` still carries both
names, and the review's own text says neither collision is closed by it. So the
routing landed rather than the sentences being deleted. Ledger id 34 was
appended through the JSON fence, one open row covering both rename decisions,
naming both names so the grep that failed now succeeds. The claim had stood
since `6cc615a` (06-02) — that commit, not a remembered round count, is what
the record now cites.

## What this round measured about its own instruments

- **Change 1** (widened gap-closure range): not re-measured this round; round 9
  records it again, per the plan's own note.
- **Change 2** (second sweep reader): first of the two consecutive zero rounds
  its exit condition needs. Round 9 decides.
- **Change 5**: widened, and the widening is the round's structural output.
  06-11 re-ran nineteen literals at `80641fd` and all nineteen held, while its
  own `4c3e911` falsified two committed literals it never re-derived. The
  forward rule reaches the literals a round *writes*; both of these were written
  by earlier rounds. Only one of the two sat in a file 06-11 never opened —
  the other sat in `tools/check_repo.py`, which it opened and edited three
  times. That is the sharper version of the finding and it was caught by this
  round's self-audit, against a sentence the plan itself had supplied.

## Deviations from the plan

Six, all recorded, none silent.

1. **E1 touched two sentences the plan did not enumerate.** The plan named
   `:291` only. Restating it to three kinds leaves `:302`'s "one of the three"
   ambiguous between three kinds and three inventory items, so "The other kind"
   and "One of the three" were re-pointed. The plan's own constraint required it.
2. **E1's first draft was false and was replaced before commit.** "Enforces only
   the first of them" is contradicted by `readme-layout-tree-stale`, which
   enforces one item of the second kind. Each kind's enforcement is now stated
   separately.
3. **E6's first draft asserted a false causal link** between the pattern's
   ordinal and the Human observations section numbers. Those sections run 1-5
   over 06-02's observations; the pattern's first three instances are Phase 4's
   G-04-3, G-04-4 and G-04-8. Both give "fourth" by coincidence.
4. **E7 also corrected a run-on the fix created** and re-verified the adjacent
   nine-times placeholder literal, which still reads 9.
5. **E9 also scoped the ledger section's own date.** Adding rows opened on
   2026-09-23 falsified "what was decided about it at the Phase 6 launch gate on
   2026-09-21" — the same class E5 had just corrected upstream in the same file.
6. **E11 added a second ledger write, so E9's render was redone.** The plan
   anticipated id 34 and sequenced E9 after E8; id 35 was not anticipated. The
   reproduction was re-rendered a second time, fence first both times.

## The plan's own figures, re-derived before use

Every figure the plan stated was re-run against the tree before its edit. All
held:

- `grep -c '^|.*20%'`: 4/4 at `2e93a0c`, 4/5 at `4c3e911` and at HEAD.
- `SPELLED_CARDINAL_RE` over `examples/deal-brief.md`: 13 at `fd1b17b`, 15 at
  `4c3e911`, 16 at HEAD. The sibling "5 raw regex matches for `skills/**`" is
  still exactly 5 — but only under the mark-line rule; a raw scan of those files
  finds 48, and the scope is now stated so the 5 cannot be re-derived as the
  wrong number.
- `owner` top-level `True`, `plugins[0]` `False`.
- The four files carrying `pain` beyond the two briefs: exactly the four named.

One plan sentence did **not** hold and is the deviation above: "in files it
never opened" is true of one literal, not two.

## Closure

This plan does not close the phase. `WINDOWS.md` id 12 and the LEG-04/LEG-05
checkboxes stay open until a round of cold reads returns none; **eight have run
and none has**. Round 9 reads what this round wrote — including, for the first
time, under the reverse index this round put in the ledger.
