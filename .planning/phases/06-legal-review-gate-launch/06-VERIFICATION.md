---
phase: 06-legal-review-gate-launch
status: human_needed
score: "2/2 must-haves verified. Round 5's four gaps (G-06-17..20) are CLOSED by 06-09 across 21 tasks and 8 files, addressing all eighteen checkably-false statements, and round 5 confirmed every one of 06-08's seventeen corrections holds. Not yet independently read: 06-09 wrote the corrections a round-6 reader would be verifying, and each of the five self-checks so far has missed what an independent reader then found. The round shipped one new build assertion (INIT-EVENTS.md's init-event key set, mutation-probed with an unmutated control and hardened once by the code-review gate) and one method change: the fourth standing brief now reads every gap-closure commit range rather than only the last round's diff, and the whole-tree sweep runs two readers. Task 18's self-audit found eight further defects in the round's own added sentences and fixed them; the code-review gate found a ninth in its new assertion. All ten CI commands green throughout. Requirement checkboxes stay unchecked. Closure condition unchanged — WINDOWS id 12 closes when a round of cold reads returns none; five have not."
verified: 2026-09-22
requirements: [LEG-04, LEG-05]
verifier: inline (orchestrator) — the gsd-verifier subagent was not dispatched
automated_verified: 24
human_verification: 16
human_verification_performed: 20
human_verification_passed: 4
human_verification_issues: 16
uat_round: "/gsd-verify-work 06 round 5, 2026-09-22"
gap_closure_round: "06-09, 2026-09-22 — G-06-17, G-06-18, G-06-19, G-06-20 closed; not yet independently read"
gaps_closed: 16
gaps_open: 0
gaps_open_ids: []
round_4_closure:
  plan: 06-08
  tasks: 17
  commits: 16
  files_changed: 10
  ci_commands_green: 10
  new_assertions: ["caveat-count-matches-constant", "no-platform-collision"]
  new_check_codes: ["record-citation-unresolvable"]
  mutation_codes_proven: 58
  user_facing_findings_fixed: 1
  self_authored_defects_found_and_fixed: 8
  measured_verdict: "record-citation-unresolvable fires 0 times across the full history as measured at 06-08 (435 commits, 164 citation-instances, 14 distinct spellings). The citation class four rounds produced is NOT mechanically catchable; the structural fix that holds is the anchoring convention, not the gate."
  recommendation_to_round_5: "Cut LEGAL-REVIEW.md rather than audit it. This round added 159 lines to correct 13 sentences and authored 8 new defects doing so. The plan set that threshold for round 5's evidence; it is reached on round 4's."
round_5_closure:
  plan: 06-09
  tasks: 21
  commits: 30
  files_changed: 8
  ci_commands_green: 10
  new_assertions: ["init-event key set vs transcripts-cat10.tar.gz"]
  new_check_codes: []
  mutation_codes_proven: 58
  user_facing_findings_fixed: 0
  self_authored_defects_found_and_fixed: 9
  method_changes:
    - "Fourth standing brief widened from the last round's diff to the union of every gap-closure commit range (d67012e..HEAD)"
    - "Whole-tree sweep taken from one reader to two, both on the same no-file brief, with round 6 recording each reader's unique findings"
  measured_verdict: "By git blame, 10 of round 5's 18 findings were authored by a gap-closure round -- 8 by the last one and 2 by 06-05 and 06-06, which no diff-scoped brief could see. The rule this phase records is not that the LAST closure is the defect source but that A closure is, and the earlier ones are still in the tree. Pinned to round 5 so round 6 can see whether widening the window moved the split."
  refused: "No gate for bench-deal-brief.md's timeline comparison. The canonical figures are machine-readable but the brief states the comparison in both orientations, so a frozen-literal gate would have to guess which one a sentence uses. Filed as a WINDOWS id 17 candidate beside enforcement-scope checking -- the sixth fuzzy proxy this repository has refused."
  self_audit:
    defects_found: 8
    classes: "5 scope overstatement, 2 count-next-to-the-thing, 1 reference resolving to wrong content"
    new_in_kind: "Two self-referential commands -- recording a grep literal in prose changed what that grep returns. Neither was catchable by re-reading the sentence; both needed the command re-run after it was committed."
    note: "Task 18's checklist found 8; the code-review gate then found a 9th in the round's own new assertion, which compared the key set but not the 140-transcript count the sentence it guards also claims. Measured: a probe copy with 40 init events stripped passed the check as shipped."
re_verification:
  previous_status: gaps_found
  previous_score: "2/2 must-haves verified. Round 4 ran the four-brief standing set for the first time: all of round 3's corrections hold under independent read, and 17 new checkably-false statements opened 4 gaps (G-06-13..16). Ten of the 17 were authored by the round-3 gap-closure commit itself, up from 4 and 2 in the two rounds before. Requirement checkboxes stay unchecked."
  gaps_closed:
    - "G-06-13 (10 findings, LEGAL-REVIEW.md) — CLOSED by 06-08 tasks 1-7. The two-step 'mechanically held' argument with the strip_fences ceiling declared; the SKILL.md:63 misquote and the both-sides rename contradiction, carried into What-remains-open item 5; the self-referential four-file grep dropped and the by-hand range widened to the prose line below the table; the over-correction corrected part by part; the drifting correction tally removed rather than updated; 'not ordinary English at all' corrected to 'source-coined' with the removal re-checked; the source-gate quotation fixed from 'list' to 'file' and the four-grounds count restated as a property."
    - "G-06-14 (1 finding, README.md) — CLOSED by 06-08 task 8. README:175's 'enforcing all of the above' bounded to the 23-file surface measured by instrumenting the checker's own reads. Standing since 58530a6 in Phase 1, survived four cold-read rounds."
    - "G-06-15 (4 findings, whole-tree sweep) — CLOSED by 06-08 tasks 9-11. The derivatives' omission notice corrected and both regenerated (the only round-4 finding reaching an installed user); both route-equivalence denials corrected to name RESULTS-routes.md; the caveat count dropped and asserted against len(REQUIRED_CAVEATS)."
    - "G-06-16 (2 findings, closing-commit brief) — CLOSED by 06-08 task 12. The 20% meaning-count removed as uncheckable by any command; platform disjointness now asserted by no-platform-collision, mutation-probed against an unmutated control."
  gaps_remaining: []
  regressions: []
  corrections_verified_clean:
    - "Not applicable to this round: 06-08 wrote the corrections it would be verifying. The independent read is round 5's, and it is the closure condition."
  self_audit:
    added_lines_audited: 595
    citation_check: "4 real citations in added text, all resolve; 5 apparent misses are synthetic self-test fixture strings"
    enforcement_scope_check: "found 2 citations this round broke in an untouched passage, plus 1 scope overstatement ('shipped skill content' read wider than the check's globs) — all fixed"
    absolutes_sweep: "112 sentences carrying only/never/nothing/every/all/none checked against the full tracked tree including .planning/"
    defects_this_round_authored: 8
    defects_caught_inside_the_round: 8
    note: "Six citations in LEGAL-REVIEW.md drifted during this round — one from task 8's README edit, five from task 17's own docstring insertion — and the new citation code was silent on all six. That is the code's declared ceiling demonstrated by the commit that added it."
---

# Phase 6 Verification: Legal Review Gate & Launch

**Goal:** The repo is legally cleared and honestly marketed before anyone outside the project sees it.

**Verdict: both success criteria are met by every automated means available, and six deliverables
turn on judgements no tool in this stack performs. The phase is verified but not complete — it waits
on a human.**

## How this verification was run

The `gsd-verifier` subagent could not be dispatched (the Agent tool is not authorised in this
session), so verification was performed inline by the orchestrator against the live codebase, not
against the SUMMARYs' own claims. Every figure below was re-measured during this verification pass.
The caveat that applies to the code review applies here too: **an inline check by the agent that did
the work is weaker than an independent one.** That is precisely why the six human items below are
routed out rather than absorbed.

## Success Criterion 1 — VERIFIED

> A legal review gate passes before public launch, with MEDDIC-family trademark status (including
> the MEDDPICC genericness ruling) reconfirmed against current sources.

| Must-have | Evidence measured 2026-09-21 |
|---|---|
| A review gate exists and passed | `LEGAL-REVIEW.md` line 3 `Review date: 2026-09-21`, line 5 `Gate status: PASSED` |
| The gate precedes public launch | `git remote -v` is empty. Publication was deferred at the 06-04 checkpoint, so the ordering holds trivially; the machine check (a configured remote requires a passed gate) is green |
| MEDDIC-family status reconfirmed against **current** sources | The docket was re-queried live via CourtListener REST v4 during 06-02: `dateTerminated` null, most recent entry 2026-09-14. Not transcribed from the seven-day-old research note |
| The MEDDPICC genericness ruling specifically | Re-fetched from the IPWatchdog press item: ruling 2026-04-21, Reg. No. 6,489,058, registrant Darius Lahoutifard / 01 Consulting LLC, E.D. Pa., Chief Judge Wendy Beetlestone. `2:24-cv-01836` ×1, `6,489,058` ×6, `2026-04-21` ×3 in `LEGAL-REVIEW.md` |
| The register state, which research could not obtain | TSDR status view answered this time: `LIVE/REGISTRATION/Issued and Active` ×2, on a page TSDR stamped 2026-09-21 05:36:50 EDT. Recorded as an observation with no interpretation of the gap against the cancellation order |
| All three rights-holders reconfirmed and re-dated | `NOTICES.md` carries 3 `Last reviewed: 2026-09-21` lines, one per statement, all equal to the review date |
| The refusals survived the update | `no claim about the outcome of any proceeding` ×1 and `is not treated here as covering another` ×1, both still present after the MEDDIC edit |
| Every framework-derived concept traces to a source | `grep -c 'unverified' SOURCES.md` → **0**. All six rows carry a distinct absolute URL and an ISO-8601 retrieval date |
| The gate cannot be faked | `source-gate-incomplete` and `framework-statement-stale-review` both discrimination-proven against the real files |
| The record says what kind of document it is | `not legal advice` ×2 |

## Success Criterion 2 — VERIFIED

> Every claim and badge in README derives only from committed benchmark results in RESULTS.md,
> stating model versions and date.

| Must-have | Evidence measured 2026-09-21 |
|---|---|
| Claims are bounded so they can be checked strictly | Exactly one `<!-- claim-region:start -->` and one `<!-- claim-region:end -->`, start before end |
| Every claim number derives from a committed result | 16 numeric tokens in the region; **0 unsourced** against `evals/*/RESULTS*.md` |
| Every claim states model versions and date | 7 numeric paragraphs; **0 unanchored** — each carries `claude-opus-5` or `claude-sonnet-5` and an ISO-8601 date |
| The figures are the benchmark's, not hand-sums | `--report-only` regenerates `RESULTS.md` with a clean diff; pooled rows 45/1/2, 32/3/13, 7/3/38 and direction 8/1/7 are renderer-emitted |
| The pooled figure is not position-biased | `pooled_summary()` consumes `judge_summary()`'s paired output; a self-test fixture is built so the paired and per-order answers differ, and a sibling probe with an unmutated control confirms the assertion fails if the wrong path is taken |
| Badges | README contains **no Markdown images at all**. `readme-badge-unlisted` guards a two-entry allow-list admitting build status and license only |
| The result is reported, not selected | All three judged dimensions stated with equal prominence; the 38-loss persuasive-force result is in its own sentence, followed by the judge-construct-validity and baseline-prompt-parity caveats |
| Enforcement, not promise | `readme-claim-unsourced`, `readme-claim-unanchored`, `readme-badge-unlisted`, `readme-layout-tree-stale` all discrimination-proven |

## Requirement traceability

| ID | State | Evidence |
|---|---|---|
| LEG-04 | Complete | Declared by 06-01, 06-02 and 06-04; marked only after the last of the three produced a SUMMARY, via `requirements.ready-ids` |
| LEG-05 | Complete | Declared by 06-03 alone; marked on its completion |

No requirement was marked from a SUMMARY's `requirements-completed` field. A grep for `[x]` adjacent
to `UNVERIFIED` in `REQUIREMENTS.md` returns nothing.

## Gate summary

| Gate | Result |
|---|---|
| `python3 tools/check_repo.py` | `0 violations` |
| `--self-test` | PASS, 56 codes named |
| `--mutation-test` | PASS, **56 codes discrimination-proven**, CONTROL 0 violations, no FIRE-ONLY line |
| Full CI surface (10 commands) | ALL TEN PASS |
| Code review (`06-REVIEW.md`) | `status: clean` — 1 low finding, fixed in place |
| Ledger | 28 entries, **11 fixed / 9 waived / 8 open**, frontmatter matches the JSON, no open entry with an empty reason |

The seven codes this phase added took the mutation harness from **49 to 56**, at 10.1 s wall — the
repository's own integrity metric, and still far under the 60-second remedy trigger 05-03 set.

## Human verification required — 6 items

These are the deliverables their own plans classified `human_judgment: true`. None is a gap in the
work; each is a judgement `SOURCES.md` itself states no tool in this project's stack performs.

1. **Sources are in bounds and no wording was carried** (06-01 D5, 06-02 D8). Whether the six
   confirmed pages are the kind `SOURCES.md`'s "Out of bounds" section permits, and whether the
   citations stopped short of reproduction.
2. **The reproduction-boundary reasoning is sound** (06-02 D8). Whether the `WINDOWS.md` id 3 and
   id 6 dispositions engage the 2026-04-21 genericness holding correctly rather than over-reading it.
3. **`LEGAL-REVIEW.md` does not read as legal advice** (06-02 D8). It says it is not; whether it
   *reads* that way is the judgement.
4. **README's claim region reads honest, not defensive** (06-03 D7). It states 38 losses in its own
   sentence and then the caveats. Whether a first-time reader experiences that as an honest report
   of a mixed result is the question the author cannot answer about their own text.
5. **The output style appears in `/config`** (06-04 D6). NOT PERFORMED — a non-interactive session
   has no picker. `WINDOWS.md` id 16 stays open.
6. **A cold read of README** (06-04 D7). NOT PERFORMED AS A COLD READ — the agent that wrote this
   round's edits would have been the reader. A self-read with a twelve-claim mechanical
   cross-reference found nothing checkably false, and is recorded as a self-read.
   `WINDOWS.md` ids 12 and 17 stay open.

Items 5 and 6 are recorded in `LEGAL-REVIEW.md` § Human observations as explicitly not performed,
with the structural reason. That is the honest state, not a gap this phase left untried.


## Human verification — PERFORMED 2026-09-21, 3 passed / 3 issues

The six items above were performed by `/gsd-verify-work 06` and are no longer outstanding. Two of
the three reasons this file gave for not performing them had expired and were re-checked rather
than honoured: five independent headless readers supplied the "no cold reader available" half, and
an interactive Claude Code session driven in a pty supplied the "no `/config` picker" half. Results
and evidence are in `06-UAT.md`; the three failures are planned in `06-05-PLAN.md`.

| # | Item | Result |
|---|---|---|
| 1 | Six sources in bounds, nothing reproduced | **pass** — all six public, `mos.meddicc.com` correctly not cited, no run of source prose at N=6 |
| 2 | Reproduction-boundary reasoning for ids 3 and 6 | **issue (major)** — id-6's premise is false against `NUMBERING.md`; the ruling half is sound |
| 3 | LEGAL-REVIEW.md does not read as legal advice | **issue (major)** — parts of it do; the disclaimer does not reach the verdict layer |
| 4 | README claim region reads as an honest mixed result | **pass** — "not a burial, and not close to one" |
| 5 | Output style listed and selectable in `/config` | **pass** — listed as entry 7, selection persists to `settings.local.json`, two controls |
| 6 | Cold read of README | **issue (major)** — three checkably-false statements, each contradicted by a committed file |

**This changes Success Criterion 2's standing.** It was recorded VERIFIED on the reading that every
claim and badge in README derives only from committed results stating model versions and date. The
cold read found that README:231-233 asserts exactly that, universally, and that the assertion is
false — `tools/check_repo.py`:405-415's own docstring says the region is bounded "because README
legitimately carries numbers that are not measured claims." The enforced claim region is sound; the
sentence claiming the discipline extends past it is not. The criterion is not withdrawn here, but
it should not be read as covering that sentence, and `06-05-PLAN.md` Task 1 corrects it.

**All ten CI commands were green throughout** (`check_repo.py` 0 violations, `--mutation-test` 56
codes discrimination-proven, seven `evals/` self-tests and `generate_derivatives.py --check` rc=0),
which is the fourth consecutive instance of WINDOWS.md id 17's pattern.

## What is honestly still open after this phase

Eight ledger entries, each with a named owner and a closure condition: 11 (publish location,
deferred by operator decision), 12 and 17 (cold read), 16 (`/config`), and 20, 21, 22, 24 (routed to
v2). `/gsd-ship` would block on these if `workflow.windows_enforce` were on; it is off, and the
entries are the record either way.

Two items carried from 06-02 have no ledger entry and should get one before any future publish: the
exact-name collisions on **Ardent Digital** (a real trading company, cast in the brief as a displaced
incumbent and losing bidder) and **Gina Almeida** (a real associate lawyer at an insurance group,
against a brief casting her as Associate General Counsel at an insurance firm). Both are recorded in
`LEGAL-REVIEW.md` § Name collisions with a recommended rename. Not blockers while publication is
deferred; blockers before it is not.

## Gap-closure round — 06-05, verified 2026-09-21

The three gaps above were closed by plan `06-05` in six task commits (`d67012e`..`36fbf6c`). This
section re-verifies each against the files, not against the SUMMARY's claims. Nothing above is
withdrawn or rewritten; the findings stand as recorded and this section records what happened to
them.

| Gap | Closure condition, from `06-UAT.md` | Re-verified against | Verdict |
|---|---|---|---|
| G-06-2 | Restate the id-6 reasoning on grounds that survive `NUMBERING.md`; test the fourth prong; examine the PF-1 list | `LEGAL-REVIEW.md`:186-302, `NUMBERING.md`:9-13 and :64-77, `.planning/WINDOWS.md` id 29 | **closed** |
| G-06-3 | Move/rename the gate line; reword the two `Disposition:` headings; bound :155 and :187; replace the disclaimer-sufficiency claim; give the ledger a state for judgement closures | `LEGAL-REVIEW.md`:21-43, :160, :188, :262, :343, :520-560 | **closed** |
| G-06-6 | Bound README:231's claim; correct the route count; carry Arm B; fix the four minor items | `README.md` diff `7e2170d..HEAD` | **closed** |

### G-06-2 — evidence

The false premise is not patched, it is stated as corrected: `LEGAL-REVIEW.md`:199-209 records that
the eight blocks give **M-E-D-D-P-P-C-C**, that the repository ships "Pain" rather than "Identify
Pain" so position 6 contributes P, and that Decision Criteria/Decision Process and
Champion/Competition are letter-ambiguous, making four of eight positions swappable. Re-measured
against `NUMBERING.md`:68-75 during this pass: correct.

All four `SOURCES.md` prongs are now applied or excluded by name (`:210`, `:215`, `:225`, `:229`).
Prong 4 is answered honestly rather than favourably — "Economic Buyer" and "Paper Process" are
recorded as sitting **on** the prong, with the decision not to rename them made explicit. The
disposition ends on two live questions rather than a finding.

The PF-1 list has a section of its own (`:260`) and is registered as `WINDOWS.md` id 29, open. It is
examined rather than disposed of, which is what the gap asked for. `NUMBERING.md`:9-13 no longer
calls the `MC-` namespace "the MEDDICC completeness audit".

### G-06-3 — evidence

The reduced read the gap defines — headings, bolded lead-ins and the ledger `Disposition` column,
skipping all prose — was re-run mechanically during this pass and carries no legal conclusion. The
specific replacements: "boundary not crossed" is gone; both `Disposition:` verdicts read
"Read at this review:"; "by none exclusively" is bounded to the sources actually read; "trading on"
is gone with the ruling paragraph confined to the trademark question the ruling decided; the
disclaimer-sufficiency assertion is replaced by what the two files state, with the sufficiency
question explicitly not answered.

`Gate status: PASSED` stayed `PASSED` and moved from line 5 to line 25, below the disclaimer.
`tools/check_repo.py`'s `source-gate-incomplete` requires exactly one readable line reading
`PASSED`, `OPEN` or `FAILED`, and defines `PASSED` narrowly — no `SOURCES.md` row reads
`unverified`, which is true. The line now sits inside a section that states that definition, quotes
the code's own "does not judge whether the review behind a declared pass was any good" ceiling, and
names the two content items open for a decision before wider distribution.

The ledger gained a fourth label, `Closed on reasoning`, for ids 3 and 6 — neither is `Fixed` under
the file's own definition, and neither was measured, so `Waived` fits no better. The divergence
from `WINDOWS.md`'s three-state schema is named in the file rather than left for a reader to find.

### G-06-6 — evidence

Each of the three false statements, re-checked against the file that contradicted it:

1. The universal evidence-discipline claim is scoped to the claim region, with the third category
   neither code reaches named explicitly. Re-read against `tools/check_repo.py`:405-421.
2. The route count states four install routes and three measured arms in the same sentence, with
   the collapse explained. `run_routes.py`:113's `ROUTES` tuple holds three.
3. The superseded n=1 figures are replaced by Arm B: 45 of 45 must-fire, 9 of 25 must-not-fire, two
   phrasings at 5 of 5 and 4 of 5. **`head -14 skills/proof-first/SKILL.md | shasum -a 256` returns
   `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`, byte-identical to the hash
   `RESULTS-trigger.md`:68 records for the Arm B block** — so the figure README carries measures the
   description that ships.

The four minor items are fixed and each was re-checked against its own source, including the count
that the round's own draft got wrong: the first draft said three near-miss phrasings accounted for
the nine over-fires; the table shows two. Corrected before commit.

### Checks

All ten commands `.github/workflows/ci.yml` declares exit 0, re-run after the final edit.
`grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` returns `0`. `.planning/WINDOWS.md`'s
frontmatter (9 open / 9 waived / 11 fixed / 29 total) matches its 29 entries.

### Why this is `human_needed` and not `passed`

Every gap is closed against its own closure condition, and the automated side is green. What is
missing is the one thing that found these three gaps in the first place: **a reader who did not
write the text.** The corrections were written and checked by the same agent, which is precisely
the weakness `.planning/WINDOWS.md` id 17 has now measured four consecutive times — ten green CI
commands alongside a false sentence a cold reader caught on the first pass. `WINDOWS.md` ids 12 and
17 both state their own closure as "closes with G-06-6", and closing them on a self-review would
repeat the mistake the round exists to correct.

**LEG-04 and LEG-05 stay `[ ]`.** Both annotations name `06-05-PLAN.md` tasks as their closure
condition and those tasks are done, but `requirements-completed` records implementation, not
verification, and this file is the verification. They close when an independent read confirms the
three corrections.

**One item found during this round's verification and deliberately not fixed.** `README.md`:109
reads "The installed skill has to be triggered and was not in 3 of its 12 sessions, while the output
style and the pasted prompt are unconditionally on once selected." Both halves are true — `skill-on`
activated in 9 of 12 — but the contrast invites a reader to take the other two arms as 12 of 12 on
the same metric, and `RESULTS-routes.md`:15-17 reads `style-on` 11 of 12 and `prompt-on` **8** of
12. `prompt-on` activates less often than `skill-on`. This is a placement judgement rather than a
false statement, the same class `06-05-PLAN.md`'s own "Out of scope" section sent to backlog, and it
is recorded here so the next cold read has it in hand.

---
*Verified: 2026-09-21 (gap-closure round 06-05)*


---

## Gap-closure round — 06-06, verified 2026-09-21

Round 2's two open gaps are closed. Twelve tasks, fifteen commits, all ten CI commands green with
`--mutation-test` at **57 codes discrimination-proven**, up from 56.

### G-06-9 — eight README findings, closed

| # | Finding | Closed by | Evidence |
|---|---|---|---|
| 1 | README said the `/config` picker "has not been observed here" while `LEGAL-REVIEW.md` records observing it | Task 1 | README now states what was observed and carries the same three limits the record states; `WINDOWS.md` 16 stays open |
| 2 | `artifact-patterns.md` + both derivatives: "no benchmark has run" | Task 3 | String absent from `skills/`, `output-styles/`, `prompts/`; derivatives regenerated; new code guards the regression |
| 3 | "three runs against the shipped skill description" — two carry the shipped sha256, one a reverted treatment | Task 2 | "three runs, two of them against the shipped skill description" |
| 4 | `publish-location-drift` described as catching any disagreement | Task 4 | Bounded to the owner-segment comparison the checker's own docstring declares |
| 5 | `bench-deal-brief.md` described as prompting the benchmark's sessions | Task 5 | `run_benchmark.py`:295 sends `scenario['prompt']`; the brief is read once, inside `--self-test` |
| 6 | `catalog-count-mismatch` named as checking README's inventory counts | Task 6 | Mutation probe with unmutated control: 31→37 and 28→44 leaves check_repo at 0, exactly as the control |
| 7 | Activation contrast carrying only `skill-on`'s figure | Task 7 | All three arms carried (9/12, 11/12, 8/12), with what the metric cannot separate stated |
| 8 | `bench-deal-brief.md` stating the expired no-network premise | Task 8 | Repo-wide sweep — three files, not one; `grep` now returns only past-tense records |

### G-06-7 — six LEGAL-REVIEW.md findings, closed

The most serious was the PF-1 counterweight: the entry asserted the seven Command of the Message
elements appear in no shipped file, when `SKILL.md`:63, `output-styles/proof-first.md`:87 and
`prompts/system-prompt.md`:75 each carry them as a set in the table's order. Corrected in all four
places it had propagated to, and — the part that matters — **the disposition was re-read against the
corrected facts rather than having them patched underneath it.** `WINDOWS.md` id 29 stays open, but
on different footing: the first of its two deciding questions is now answered by the files rather
than by a judgement, and the remedy it priced at one file costs three plus a regeneration.

The other five: the same-initial undercount (four → six, `Paper Process`/`Pain` being a third P
pair), the `completeness-audit.md` heading claim (neither string occurs in that file), the
`NUMBERING.md` line citation (`:26-40` → `:31-45`), the id-6 equivalence claim, and the append-only
rule, which was restated to permit correcting a falsified premise in place on the condition that the
correction names what changed.

### The one code this round added

Thirteen of the fourteen findings were left to reading, for the reason `WINDOWS.md` id 17 records.
The fourteenth was a fixed string whose sibling literal already had a guard, so it got a code:
`benchmark-run-claim-stale`. Three behavioural claims in its docstring were each proven against an
unmutated sibling control — it catches a capitalised regression, it catches a derivative-only
regression the source-blind sibling would miss, and it stays silent when the evidence file is absent.

The plan asked for the literal to be folded into the existing check. It is a sibling code instead,
because the mutation harness maps one code to one mutation and a folded-in literal would be
registered without ever being discrimination-proven — `WINDOWS.md` id 10, this repository's own named
recurring defect. Reviewed and upheld in `06-REVIEW.md`.

### What this round did that the last one did not

It re-read the sentences it **added**, not only the ones it fixed. Two more checkably-false
statements turned up, one of its own making:

- "repo-wide the two appear only in `NUMBERING.md`, in this file, and in `check_repo.py`'s fixtures"
  — written by this round's Task 10. `.planning/` is tracked, 178 files, and both strings appear
  across it.
- "The register itself lives under `.planning/`, which a reader of this repository cannot see" —
  pre-existing, surfaced by checking the first. A reader can: it is tracked, and README cites
  `.planning/WINDOWS.md` by entry number twice.

Both corrected before the round closed. 06-05's recorded failure was precisely this, so the habit is
now in the loop — but catching it once is not evidence it holds.

### Why the requirement checkboxes stay unchecked

LEG-04 and LEG-05 both state their closure condition as **an independent read of the corrections**.
This round's corrections were written and checked by the same agent. Every round of this phase has
found that the previous round's self-checked corrections left or introduced defects — three in round
1, fourteen in round 2, two caught in-round here. The phase's must-haves are verified and its gaps
are closed; what is not verified is that the closure is clean, and only a reader who did not write it
can establish that.

**Next: `/gsd-verify-work 06` for a round-3 independent read.** Do not mark the phase complete from
this branch.

---

## Round 3 — independent read, 2026-09-22

The read both requirements name as their closure condition ran. Five readers, five separate scratch
trees, headless `claude -p` on `claude-opus-5`, `.planning/` and `.claude/` removed, neutral briefs,
one writer per output file. Two on README, two on `LEGAL-REVIEW.md`'s reproduction-boundary material,
and one — new this round — pointed at no file at all and asked only for two committed files that
cannot both be true.

**The corrections held.** Every one of round 2's fourteen fixes was re-checked by a reader who had
not written it, and all fourteen stand. Both readers on `LEGAL-REVIEW.md` verified the PF-1
counterweight against all three shipped files byte for byte; all three README readers recomputed the
claim region by hand, including re-summing the 48-row per-cell table to its pooled totals and
re-tallying the 23 conformance run blocks.

**The files did not.** Eleven checkably-false statements, opening G-06-10, G-06-11 and G-06-12. Where
they came from is the finding worth carrying. By `git blame` on each cited line: four are in 06-05
text that round 2's briefs pointed no reader at, three are in files no brief had ever named, and four
were authored by the closing round itself while fixing something else — one of those four importing
into README a claim that had sat unread in `bench-deal-brief.md` since Phase 5. None is a regression
of a fix. The fixes are clean; the briefs were narrower than the defect.

That is why the sweep brief exists from this round on. It cost the same as a file-scoped reader and
returned three statements in three files — `evals/lint.py`, `LEGAL-REVIEW.md`'s ledger, and
`run_conformance.py` — that six earlier readers across two rounds had no reason to open.

**All ten CI commands were green again while all eleven were in the tree** (2026-09-22: `--self-test`
PASS, `--mutation-test` PASS at 57 codes, `check_repo.py` 0 violations, seven `evals/` self-tests and
`generate_derivatives.py --check` all rc=0). Sixth consecutive round of `WINDOWS.md` id 17's pattern.

**Next: `/gsd-execute-phase 06 --gaps-only`** against `06-07-PLAN.md`. Do not mark the phase complete
from this branch.

---

## Gap-closure round — 06-07, verified 2026-09-22

All three round-3 gaps closed, 13 tasks, commit `908b90b`. Eleven corrections across six files.

The one worth recording as more than a fix: `LEGAL-REVIEW.md` and `tools/check_repo.py` held
**opposite** classifications of the same eight MC dimension names — six-and-two against
seven-and-one — and each file was internally consistent, so no string-matching gate could ever have
seen it. The review adopts the checker's frozen split, which widens the prong-4 concession from two
labels to seven. The disposition does not move, and the entry now states why rather than leaving a
reader to find the gap: the closure never rested on the count.

Two closures went past what the plan required, both because the alternative was worse:

- Prong 2's "many independent publishers" clause — a premise recorded in no committed file, filed by
  round 3 as backlog — sat inside a sentence two other tasks had to rewrite. Leaving it would have
  been the exact pattern that produced four of round 3's own findings. Prong 2 now rests on the
  thinness test alone, which `SOURCES.md` does not contain. The entry's weaker half is weaker.
- `run_benchmark.py`'s entity assertion covered four of the nine invented names while README was
  about to claim it covered all of them. Widened to nine and discrimination-proven against an
  unmutated control.

`G-06-11`'s permitted outcome 1 was rejected on evidence, not cost: 20% carries four distinct
meanings inside the bench brief and three inside the examples brief, so varying one row would have
left the claim false while looking fixed.

**The self-audit earned its place this round.** It found three defects in sentences 06-07 had just
written — a line range pointing at the wrong prose, a claim about copying this review cannot
establish, and a citation written against line numbers the same round's own edit had shifted. Five
further citations were converted from line numbers to heading anchors, because both deal briefs are
edited more often than this record is re-read.

All ten CI commands green. `WINDOWS.md`'s table was re-rendered from its JSON rather than
hand-edited, and `LEGAL-REVIEW.md`'s reproduced ledger reconciled against it row by row; no status
and no count changed.

**Next: `/gsd-verify-work 06` for a round-4 independent read**, with the four-brief standing set now
recorded in `06-UAT.md`. Do not mark the phase complete from this branch: three self-checks in a row
have each missed what an independent reader then found.

---
*Verified: 2026-09-22 (gap-closure round 06-07)*

---

## Round 4 — the four-brief standing set, 2026-09-22

Six readers across four briefs, the set recorded after round 3. `38c873b`, `.planning/` and `.claude/`
removed, one writer per output file, none had written what it read.

**Round 3's corrections hold.** All seven `LEGAL-REVIEW.md` fixes, both README fixes and all three
sweep fixes were re-checked by readers who made none of them. The adopted seven-of-eight source-coined
split was verified line by line — tuple bounds, all seven strings, the violation text, the `metric`
exclusion, the 03-07 provenance, the LEG-04 routing.

**And the round that made them wrote ten of this round's seventeen findings.**

| Round | Findings | From the previous closing commit |
|---|---|---|
| 2 | 14 | 2 |
| 3 | 11 | 4 |
| 4 | 17 | **10** |

That is the finding of round 4, and it is about the process rather than the files. Three classes
account for fourteen of the seventeen: a scope overstatement about a mechanical guard, a citation that
does not resolve, and a count stated in prose beside the thing it counts. All three are avoidable and
two are mechanically checkable — which is what 06-08 task 17 attempts, narrowly, with an explicit
instruction not to ship a half-working gate.

**The new fourth brief justified itself on first use.** Aimed at the closing commit's own 202 added
lines, it was the highest-yield reader of the round: two findings no other brief could reach, four
confirmed independently. It is mandatory from here.

**One finding reaches an installed user** and is task 9, ordered first: both derivatives tell the
reader every rule in the omitted `worked-examples.md` carries a constructive line in `SKILL.md`, while
eight of them are MC rules that `mc-rule-in-skill` forbids from `SKILL.md`.

All ten CI commands green throughout — seventh consecutive round of `WINDOWS.md` id 17's pattern.

**Next: `/gsd-execute-phase 06 --gaps-only`** against `06-08-PLAN.md`. Do not mark the phase complete
from this branch.

---
*Verified: 2026-09-22 (UAT round 4)*

## Gap-closure round — 06-09, verified 2026-09-22

Round 5's four gaps closed at source. Twenty-one tasks, eight files, 28 commits.

**What closed.**

| Gap | Findings | Closed by |
|---|---|---|
| G-06-17 | 3, README | Tasks 1-3 — the proxy-source claim bounded to the three registry lists `proxy-term-unsourced` actually governs; the output-styles claim scoped to route 3's local clone with the plugin case disclosed as untested rather than asserted either way; the regeneration trigger corrected to the generator's four reference files, with the fifth named as not a source |
| G-06-18 | 8, LEGAL-REVIEW | Tasks 4-11 — two citations re-anchored by quoted string after `f909d3c` broke them; the source-row arithmetic; the surviving retracted phrase; prong 3's missing command run and recorded; the list/file "correction" withdrawn because the retired quotation was accurate; a machine check that never existed deleted; seven self-tests corrected to six at both live sites; the TSDR "answered" claim reconciled with the table's own 401 |
| G-06-19 | 4, tooling and briefs | Tasks 12-16 — the citation code's block comment and scope comment corrected against their own docstring; `INIT-EVENTS.md`'s key set corrected to 24 and asserted; the element-label count corrected to fourteen with its counting rule stated in the same sentence; the bench brief's reversed comparison fixed |
| G-06-20 | 2, the closing round's own text | Task 17 — the `strip_fences` comparison dropped after an AST census showed 36 of 51 check functions do not call it; ledger row 12's reader count corrected to one |

**The structural change, and why it is the round's real output.** The fourth standing brief read the
diff of the round that had just closed. Two of round 5's eighteen findings were authored by 06-05 and
06-06, closing rounds 1 and 2, and had survived every read since — neither is in the last round's
diff, so no diff-scoped brief could ever have seen them. The brief now reads the union of every
gap-closure commit range. The whole-tree sweep goes from one reader to two, because it is the only
route to text no brief names and three of round 5's oldest findings came through it and nowhere else.
Both are recorded in `06-UAT.md`'s standing-set section and `WINDOWS.md` id 17, with the justifying
measurement pinned to round 5 so round 6 can see whether widening moved the split.

**What the round refused.** No gate for the bench brief's timeline comparison. Its canonical figures
are machine-readable, but the brief states the comparison in both orientations — the programme is
longer, the window is shorter, both correct — so any frozen-literal gate would have to guess which
orientation a sentence uses. Filed as a candidate, not shipped. Sixth refusal of a fuzzy proxy.

**Nine defects in the round's own output, found inside the round.** Task 18's self-audit found eight
— five scope overstatements, two counts, one reference resolving to the wrong section — and the
code-review gate found a ninth, in the assertion the round had just shipped. Two are new in kind:
recording a `grep` literal in prose changed what that `grep` returns, twice, and neither was
catchable by re-reading the sentence. Both needed the command re-run after it was committed.

**This does not close the phase.** 06-09 wrote the corrections a round-6 reader would be verifying,
and five consecutive self-checks have each missed what an independent read then found. LEG-04 and
LEG-05 stay unchecked. All ten CI commands green throughout — ninth consecutive round of
`WINDOWS.md` id 17's pattern.

**Next: `/gsd-verify-work 06`** for round 6, against the amended standing set: six readers, the
fourth brief reading `d67012e..HEAD`, and two whole-tree sweep readers whose unique findings are
recorded separately. Do not mark the phase complete from this branch.

---
*Verified: 2026-09-22 (06-09 gap closure)*
