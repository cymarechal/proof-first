---
phase: 04-distribution-worked-examples
verified: 2026-09-21T15:30:00Z
status: human_needed
score: "5/5 roadmap success criteria addressed: 4 VERIFIED, 1 (#3) MEASURED AND NOT ESTABLISHED — the comparison ran and returned a null result, which answers the criterion's question without satisfying its wording"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  round: 6
  previous_status: human_needed
  previous_score: "4/5 roadmap success criteria VERIFIED (structural); 1/5 (#3) correctly routes to human/behavioral verification by explicit project design"
  supersedes: "Rounds 1-5 of this file, retained in full below this frontmatter. Round 6 changes the frontmatter and appends its own section; it does not rewrite the earlier narrative, which remains the record of how the 47-code gate, CR-01, and gaps G-04-1 through G-04-8 were closed."
  gaps_closed:
    - "G-04-9 — 04-UAT.md test 2 had read `blocked — deferred by design` since the phase began, with `Owner: Phase 5`, on the stated ground that it waited on Phase 5's benchmark. Phase 5 completed 2026-09-18. The premise expired and the item did not: it carried the same blocked status and the same completed owner through four subsequent gap-closure rounds, with a green gate throughout, while prompts/system-prompt.md kept emitting the generated sentence `No benchmark has compared a session driven by this file against a session with the skill folder installed`. 04-15 ran the comparison. The root cause recorded is a deferral whose stated blocking reason nothing re-read when the dependency landed — a class no code in this stack can see, because tools/check_repo.py's codes are presence and drift checks over shipped content, not staleness checks over planning premises."
  gaps_remaining: []
  regressions: []
  finding_direction: "The measurement came back null and is published as null. Three routes, 36 headless claude-sonnet-5 sessions at --effort low, 4 artifact families x 3 repeats, zero unscoreable. Mechanical proxy counts: skill-on 7.9 [1-14], style-on 7.1 [3-11], prompt-on 6.3 [1-10]. Every pair of arms overlaps, so the routes were not distinguished. That is a weaker statement than the criterion's own word `equivalent`, and separation_verdict() in evals/routes/run_routes.py enforces the distinction in code — it will only assert a difference between arms on non-overlapping observed ranges, so the refusal to overstate is mechanical rather than a matter of the author's restraint at writing time."
  unexpected_finding: "The activation asymmetry, which no prior round had separated out and which matters more for choosing a route than the prose counts do. style-on reached the artifact-family line in 12 of 12 sessions and carried rule markers in 11 of 12. skill-on carried markers in only 9 of 12, because the installed skill must first be triggered while an output style and a pasted prompt are unconditionally on once selected. This is CAT-10's disclosed trigger residual (WINDOWS entry 24, Phase 2, open) surfacing inside a different measurement. It also confounds the null result: skill-on's arm pools 3 sessions of effectively unrouted output, which pulls that arm toward the baseline. Disclosed on the arm that carries it, in the report and in README, rather than averaged away."
  mechanisation_registered: "A 49th code, derivative-comparison-claim-stale, registered and discrimination-proven in both directions (mutation-test PASS: 49 codes, CONTROL 0 unexpected, no FIRE-ONLY line). It fires only on the conjunction — evals/routes/RESULTS-routes.md exists AND a derivative still carries the literal `No benchmark has compared` — which needed three fixture roots rather than two, because a conjunction check must also prove it stays silent on `A without B`. This is the opposite call from round 5's refusal and the difference is stated: round 5 declined a code for cross-sentence semantic contradiction, which is entailment over two phrasings; this is a literal-substring presence conjunction with a declared ceiling, guarding a sentence whose truth a reader has no way to evaluate unaided."
  requirement_moved: "DIST-05 moved to complete this round, on evidence exercised rather than asserted: skill-derivative-stale and `generate_derivatives.py --check` both enforce regeneration and both are in CI, the re-sync step is documented at README's `## Keeping derivatives in sync`, and 04-15 changed the generator and regenerated both derivatives through it with --check exiting 0. DIST-03 and DIST-04 stay unchecked with their notes rewritten to say what is now measured and what is not. EX-02, DIST-01, DIST-02 and DIST-06 are untouched by this round."
  stopping_rule: "Unchanged from round 5 and still approved: a cold-read finding blocks only if it is CHECKABLY FALSE. Applied this round to 04-15's own output — a cold read of evals/routes/RESULTS-routes.md found two figures a fresh evaluator would misread (skill-on's highest mean, which pools 3 never-activated sessions; style-on's 12/12 conformant against 11/12 activated, which is not an arithmetic error). Both were corrected in the renderer, not the file, in commit 8a14222. No figure changed."
  honest_limit_of_this_round: "The cold read of 04-15's report was performed by the same party that produced the report. That is weaker than the independent cold reads that caught G-04-3, G-04-4 and G-04-8, every one of which was found by a reader who had not written the text. This is recorded as coverage item D5 in 04-15-SUMMARY.md with human_judgment: true, and it is the single largest gap in this round's own confidence."
overrides: []
gaps: []
deferred:
  - truth: "A live install (npx skills add / claude plugin marketplace add) succeeds against the published repository"
    addressed_in: "Phase 6 (LEG-04 launch gate)"
    evidence: "WINDOWS.md entry 11 (open, unchanged): publish location is frozen as the disclosed <owner>/<repo> placeholder; no git remote exists. Untouched by round 6."
  - truth: "A live Claude Code session actually lists and applies the copied output style through /config"
    addressed_in: "Phase 6 (LEG-04 launch gate)"
    evidence: "WINDOWS.md entry 16 (open, narrowed by round 6). What changed: the style's CONTENT is now proven to reach a live session — 04-15 copied it into a headless session's own .claude/output-styles/, named it in that session's .claude/settings.json, and the session cited rule markers an unrouted control did not (evals/routes/probe/). What remains unobserved is exactly the picker: a headless session has no /config, and nothing in this repository can drive an interactive one. The entry is narrower than it was, not closed."
  - truth: "Pasting prompts/system-prompt.md into a harness that is not Claude Code behaves as the measured arm did"
    addressed_in: "Not scheduled — needs a non-Claude harness this repository cannot drive"
    evidence: "WINDOWS.md entry 28 (new, round 6). The prompt-on arm used --append-system-prompt-file against headless Claude Code. That is the closest observable stand-in for route 4 and is not route 4."
  - truth: "The null result between arms is attributable to the routes rather than to run-to-run variance, or to the trigger asymmetry between them"
    addressed_in: "Not scheduled — costs sessions, not code"
    evidence: "WINDOWS.md entry 28 (new, round 6). n=3 per cell, one model, one effort, one scenario per family after the reduced matrix was authorised at 04-15's spend checkpoint. The skill-on arm additionally carries 3 never-activated sessions inside its own mean."
human_verification:
  - test: "Once a real repository/owner exists: run `npx skills add <real-owner>/<real-repo>` and `claude plugin marketplace add <real-owner>/<real-repo> && claude plugin install proof-first@proof-first`."
    expected: "Both commands resolve and install the skill/plugin, including a marketplace.json whose plugin entry is mechanically known-complete (CR-01, closed round 3)."
    why_human: "No git remote is configured; a live install is a network-and-harness behavior no file-reading checker can observe. Unchanged by round 6 — 04-15 touched neither manifest."
  - test: "On a real machine, copy output-styles/proof-first.md to ~/.claude/output-styles/, open an interactive Claude Code session, and confirm the style appears in the /config picker and applies once selected."
    expected: "The style is listed under its own name and, once selected, stays on for the whole session."
    why_human: "Narrowed by round 6 and still open. The style's content is now proven to reach a headless session; the interactive picker is the one remaining link, and a headless session has none. WINDOWS entry 16."
  - test: "Have someone who has not read 04-15-PLAN.md and did not write the report read evals/routes/RESULTS-routes.md cold, as a technical evaluator would."
    expected: "The headline verdict is no stronger than the tables beneath it support; nothing in the Honest caveats section is contradicted elsewhere in the file; the regenerated derivative preamble claims no equal outcome the report did not find; and neither the Mechanical proxy counts table nor the Family-line conformance table leads the reader to a conclusion the data does not carry."
    why_human: "This is the check the phase's own history says matters most: G-04-3, G-04-4 and G-04-8 were each found by an independent cold read against a green gate. The read performed this round was done by the party that wrote the report and produced two corrections (8a14222); it is not a substitute for an independent one. Recorded as D5 in 04-15-SUMMARY.md."
  - test: "Have a person unfamiliar with this project re-read examples/before-after.md's four after-columns."
    expected: "Each after column reads as an applied rewrite grounded in the deal brief, not a paraphrase of the rule text."
    why_human: "EX-02's `verification: backstop` half, unchanged by round 6 — 04-15 modified no example file (`git diff --stat -- examples/` is empty across every commit in this round)."
  - test: "Have a first-time reader open README.md cold and report whether the Install section is actionable without cross-referencing other files."
    expected: "A prospective evaluator picks a route and follows it without confusion."
    why_human: "DIST-06's prose-quality half — WINDOWS.md entry 12, open. Round 6 added two paragraphs to this section (routes 3 and 4's measurement statements), which makes a fresh read more valuable than it was, not less."

---

# Phase 4: Distribution & Worked Examples Verification Report

**Phase Goal:** The finished rule catalog reaches a writer through every distribution channel the project promises, backed by real worked examples.
**Verified:** 2026-09-18T08:10:00Z
**Status:** human_needed
**Re-verification:** Yes — fourth round, closing the two live UAT gaps (G-04-3, G-04-4) found by cold-read human verification against the prior round's `human_needed` report

This report focuses on what changed since `04-VERIFICATION.md`'s prior round (`human_needed`, four
outstanding human-verification items, none a code-level gap). For the full history of rounds one
through three — the seven original UAT gaps, CR-01's closure, and the 47-code gate's build-up — see
that prior report's content, superseded here rather than restated. This round's changes are exactly
7 commits across two plans (`04-12`, `04-13`), 4 files (`examples/before-after.md`,
`tools/check_repo.py`, `README.md`, `.planning/WINDOWS.md`), closing two defects a human UAT pass
found in the prior round's own designated human-verification items #3 and #4.

## What This Round Closed

Round 3 left this phase `human_needed` on four items the project's own design routes to human
judgment rather than a mechanical check. Running those checks (recorded in `04-UAT.md`) surfaced two
concrete, fixable defects inside two of those four items — not new categories of gap, but real
factual/completeness errors a cold reader found where the mechanical gate was silent.

**G-04-3 — closed by 04-12.** `examples/before-after.md:20` claimed AWS Control Tower delivers
governance across Halverton Mutual's on-premises VMware/Oracle estate. Control Tower governs AWS
accounts and OUs, not on-premises infrastructure — a factual error self-contradicting sentence 1 of
its own column and contradicting both `deal-brief.md:22` and `worked-examples.md:32`, introduced as
a side effect of an earlier PF-1.9 capability-first recast (`f8ebf78`). This verifier independently
reproduced the fix at HEAD:
- `grep -n "on-premises estate"` in `examples/before-after.md:20`'s governance sentence → absent;
  the sentence now reads "AWS Control Tower delivers that governance across the new account
  structure", matching both authorities verbatim in scope.
- The Demo column's Feld quotation (line 34, not separately reproduced above) collapses the prior
  fabricated "said... He added..." two-part construction into one attribution, one quotation.
- `python3 tools/check_repo.py` → `check_repo: 0 violations` at HEAD, unchanged.
- Commits `a628a8e`, `baa0395`, `06ebacb`.
- The two items UAT test 3 was originally written to check — PF-1.9's capability-first shape and
  PF-3.3's term-level marking — both PASSED before and after; this was a third, unanticipated defect
  in the sentence the earlier PF-1.9 fix had created.

**G-04-4 — closed by 04-13.** `README.md:38` claimed routes 3 and 4 "work today, from a local
clone." Route 3's output-style file sits at repo-root `output-styles/`, the plugin-root discovery
location, live only once installed as a plugin; a bare clone populates neither
`~/.claude/output-styles/` nor `<project>/.claude/output-styles/`, and no copy step was stated. This
verifier independently reproduced the fix at HEAD:
- `grep -n "work today, from a local clone"` in `README.md` → no match (was present).
- `grep -c "~/.claude/output-styles/"` in `README.md` → 2 (the preamble and the fenced command
  block), plus a stated project-scoped alternative.
- A new violation code, `readme-output-style-destination-missing`, is registered (48th
  discrimination-proven code, up from 47). Its own docstring states an explicit, narrow ceiling —
  it asserts only that README names a destination directory, nothing about whether the copy
  succeeds, whether Claude Code lists or applies the style, or whether any other stated route is
  executable. A wider "route is executable" code was considered and explicitly refused in the
  SUMMARY, on the stated ground that it would repeat CR-01's overstatement (a checker claiming
  coverage it does not have) — the same failure class this phase already paid to close once.
- `python3 tools/check_repo.py --self-test` reproduced by this verifier: PASS, 48 codes listed
  including `readme-output-style-destination-missing`.
- Four of five README secondary defects folded in (lead-in layout mismatch, opaque namespace
  pointer, duplicate placeholder disclosure, unbroken Status paragraph); the fifth (Status section's
  position/density in the file) is explicitly deferred with a stated reason in the SUMMARY, not
  dropped — it is a structural-placement complaint, not a truth defect, and was never what G-04-4
  failed on.
- Commits `63b5dfa`, `fea74ac`, `2d7a0d1`, `8ce83ec`.

**Full project gate reproduced green, independently, at HEAD by this verifier:**
`python3 tools/check_repo.py` → `check_repo: 0 violations`; `--self-test` → PASS, 48 codes,
including the two files' new/repaired content; `generate_derivatives.py --check` → exit 0 (per
04-13's own recorded run; neither derivative was touched this round). Working tree state and blast
radius match both SUMMARYs: wave 1 (04-12) touched `examples/before-after.md` only; wave 2 (04-13)
touched `tools/check_repo.py`, `README.md`, `.planning/WINDOWS.md`. Neither STATE.md, ROADMAP.md,
nor REQUIREMENTS.md was modified by either executor.

**No anti-patterns found.** `grep -n -E "TBD|FIXME|XXX|TODO|HACK|PLACEHOLDER"` across
`examples/before-after.md`, `README.md`, and `tools/check_repo.py` at HEAD returns no matches
(reproduced independently by this verifier, not taken from either SUMMARY).

**One disclosed, non-blocking deviation (04-13, Rule 3):** `.planning/WINDOWS.md`'s rendered table
was mechanically regenerated for pre-existing entry 15 because `gsd-tools windows append` refuses to
write while a row disagrees with its JSON source of truth — a pre-existing backslash-escaping drift
unrelated to this plan's tasks. Only the rendered row changed; entry 15's JSON content, status, and
meaning are unchanged; entry 16 (`unrun-verify`) is the new, legitimate addition this round.

## Goal Achievement

### Observable Truths (roadmap Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Reader sees before/after pairs covering each of the four artifact families, after column citing real, shipped rule numbers | ✓ VERIFIED (structural; content defect G-04-3 fixed this round) | Mechanized findings (`example-rule-narration`, `example-sentence-length`, `before-after-spelled-count`, all 0 violations) stand and are reproduced green. This round additionally fixed a factual defect (AWS Control Tower scope, Feld quotation) a cold human read found in the after columns. The broader content-quality judgment on all four after columns remains an explicit `verification: backstop` truth, routed to human verification #3. |
| 2 | User can install via the skills CLI with one command, and separately as a Claude Code plugin from a marketplace manifest in this repo | ✓ VERIFIED (structural, unchanged) | Unaffected by this round's two plans. CR-01 (closed round 3) still holds; live install stays gated on the pre-existing, disclosed publish-location ceiling — routed to human verification #1 and Phase 6's LEG-04. |
| 3 | User can turn the discipline on permanently as an output style, or paste a system-prompt version, and get equivalent behavior either way | ⚠️ Structural only — routes to human, by design (unchanged) | Neither derivative nor the generator was touched this round. Both derivatives still exist, reproduce byte-for-byte, and cover all rule + family headings. "Equivalent behavior" remains a deliberate `verification: backstop` truth pending Phase 5's benchmark; this verifier abstains rather than inferring a pass from presence. |
| 4 | A documented re-sync step exists that regenerates the output style and system prompt whenever SKILL.md changes | ✓ VERIFIED (unchanged) | Neither plan touched `tools/generate_derivatives.py`. `--check` reproduced exit 0 per 04-13's own gate run. |
| 5 | Reader opens a README that leads with before/after pairs and states an install path for every supported harness | ✓ VERIFIED (structural; content defect G-04-4 fixed this round) | Prior mechanized findings stand (`readme-example-drift`, `readme-example-lead-distance`, `readme-layout-legend-drift`, `readme-before-after-order`, `readme-install-path-missing`), plus a new 48th code (`readme-output-style-destination-missing`) closing the specific false-claim class G-04-4 found. Independently reproduced green. Prose-quality-as-experienced-by-a-cold-reader stays open (WINDOWS entry 12, narrowed), routed to human verification #4. |

**Score:** 4/5 truths (#1, #2, #4, #5) structurally VERIFIED — unchanged in count from the prior
round, because both defects fixed this round (G-04-3, G-04-4) were found *inside* truths #1 and #5's
already-open human-verification items, not new failures of previously-passing truths. 1/5 (#3) is
correctly left unverified by explicit project design (measured-claims-or-none discipline; a
`backstop` truth is never inferred VERIFIED from presence alone). No truth is FAILED, so rule 1 of
the status decision tree does not fire. Rule 2 fires: four human-verification items remain open (two
narrowed to reflect this round's fixes, two unchanged because neither plan touched their underlying
files) — so this round's status stays `human_needed`, not `passed`.

### Required Artifacts (delta from prior round)

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `examples/before-after.md` | Solution proposal column's AWS Control Tower claim true of the product; Demo column's Feld quotation verbatim, single-attribution | ✓ VERIFIED (was ✗ factually defective per G-04-3) | Line 20 now reads "governance across the new account structure", matching `deal-brief.md:22` and `worked-examples.md:32`. Feld quotation collapsed to one attribution, verbatim including the em dash. `check_repo.py` reproduces 0 violations. |
| `README.md` `## Install` section | States route 3's copy step and destination; distinguishes it from route 4 (no step needed) | ✓ VERIFIED (was ✗ falsely claimed both routes work today per G-04-4) | "work today, from a local clone" claim removed; destination directory named twice (preamble + fenced command); route 4 explicitly stated to need no step. |
| `tools/check_repo.py` (README checks) | New code proving README names an output-style destination, with a declared, narrow ceiling | ✓ VERIFIED | `readme-output-style-destination-missing` registered, 48th discrimination-proven code, reproduced via `--self-test`; docstring explicitly disclaims route-executability, avoiding CR-01's overstatement class. |
| `.planning/WINDOWS.md` | Entry 16 filed for the one residual unobserved link (live `/config` listing) | ✓ VERIFIED | Entry 16 (`unrun-verify`) present; entry 15's JSON content unchanged, only its rendered table row was regenerated to match its own source of truth (disclosed, non-blocking deviation). |

All other artifacts (`plugin.json`, `marketplace.json`, the two derivatives, the README checker
codes established in prior rounds) are unchanged from the prior round's ✓ VERIFIED findings — neither
04-12 nor 04-13 touched them — and this verifier's own gate re-run confirms nothing regressed.

### Requirements Coverage

| Requirement | Status | Evidence |
|-------------|--------|----------|
| EX-02 | Structural: SATISFIED (content defect fixed this round). Content-quality: NEEDS HUMAN | G-04-3's specific factual defect closed by 04-12; the broader backstop truth (does every after column genuinely apply its rule) remains human verification #3. Row confirmed `- [ ]` at HEAD, correctly unchecked pending end-of-phase UAT re-confirmation. |
| DIST-01 | Structural: SATISFIED (unchanged). Live flow: NEEDS HUMAN (Phase 6) | Unaffected by this round. |
| DIST-02 | Structural: SATISFIED (unchanged, CR-01 closed round 3). Live flow: NEEDS HUMAN (Phase 6, unrelated disclosed ceiling) | Unaffected by this round. Row confirmed `- [ ]` at HEAD. |
| DIST-03 | Structural: SATISFIED (unchanged). Behavioral: NEEDS HUMAN (by design) | Unaffected by this round. |
| DIST-04 | Structural: SATISFIED (unchanged). Behavioral: NEEDS HUMAN (by design) | Unaffected by this round. |
| DIST-05 | SATISFIED (unchanged) | Unaffected by this round; `generate_derivatives.py --check` still exit 0. |
| DIST-06 | Structural: SATISFIED (false-claim defect fixed this round). Prose-quality: NEEDS HUMAN (WINDOWS.md 12, narrowed) | G-04-4's specific defect closed by 04-13; WINDOWS entry 16 newly tracks the one remaining unobserved link (live `/config` listing). Row confirmed `- [ ]` at HEAD. |

No orphaned requirements. All seven IDs declared across the phase's plans are accounted for above.

**REQUIREMENTS.md checkbox guard:** `grep -c '^- \[x\].*UNVERIFIED' .planning/REQUIREMENTS.md`
reproduced by this verifier → `0` at HEAD. EX-02, DIST-02, and DIST-06's rows are each confirmed
`- [ ]` with their standing "do not mark Complete from a SUMMARY's `requirements-completed` field"
notes intact. Neither 04-12 nor 04-13 ran `requirements.mark-complete`, and this verifier did not
flip any checkbox.

### Anti-Patterns Found

None in the four files this round's two plans modified. `grep -n -E
"TBD|FIXME|XXX|TODO|HACK|PLACEHOLDER"` across `examples/before-after.md`, `README.md`, and
`tools/check_repo.py` returns no matches, reproduced independently by this verifier.

### Open WINDOWS.md entries touching this phase

- **11** (open) — publish location frozen as `<owner>/<repo>` placeholder; no git remote. Routed to
  Phase 6 LEG-04.
- **12** (open, narrowed this round) — DIST-06's prose-quality half unverified by any check; the
  false "works today" claim and missing copy step (G-04-4's primary defect) are now fixed, so what
  remains open is cold-reader prose quality, not completeness.
- **13, 14, 15** (open, `deviation` kind) — disclosed, non-blocking plan-authored verification-script
  errors from prior rounds. Entry 15's rendered table row was mechanically regenerated this round to
  match its own unchanged JSON (see Deviations above); its content, status, and meaning did not
  change.
- **16** (new this round, `unrun-verify`) — a live Claude Code session actually listing and applying
  the copied output style is unobserved in this environment. Routed to Phase 6 LEG-04 alongside 11
  and 12.

## Human Verification Required

See the `human_verification` list in this file's frontmatter — 4 items. Two are narrowed to reflect
this round's fixes (items #3 and #4, since 04-12 and 04-13 closed the specific defects a prior cold
read found inside them); two are unchanged in substance because neither plan touched their
underlying files (item #1: live install, gated on publish location; item #2: cross-route behavioral
equivalence, gated on Phase 5's benchmark).

## Gaps Summary

**No gap blocks this phase's goal this round.** G-04-3 and G-04-4 — the two live defects the prior
round's human-verification pass surfaced — are both closed, verified independently by this report
rather than accepted from either SUMMARY's word: the repaired text was read directly at HEAD, the
false claims were confirmed absent by grep, the repaired claims were confirmed present and matching
their cited authorities, the new violation code was confirmed registered and listed by `--self-test`,
and the full project gate (plain run, self-test, derivative check) reproduces green with no
regression.

What keeps this phase from `passed` is not a defect but the same four items this project's own
design correctly routes to human judgment rather than a mechanical check, carried forward from prior
rounds and narrowed, not eliminated, by this round's fixes: the live install (blocked on an
unrelated, disclosed placeholder, Phase 6), the cross-route behavioral-equivalence claim (an
explicit `verification: backstop` truth reserved for Phase 5's benchmark), the content-quality
judgment on the worked examples' after-columns (now free of the specific factual defect a cold
reader found, but the general rewrite-vs-restatement judgment is still human), and README's
prose-quality/first-reader-clarity judgment (now free of the specific false install claim, but
whether the prose reads well to a cold reader is still human). None of these are oversights; all
four were disclosed as ceilings in prior rounds and remain so in kind, though two are demonstrably
narrower after this round's work.

**Recommended next step:** route this phase to human verification (the four items above,
specifically the two narrowed ones — re-reading the repaired Control Tower/Feld passages and the
repaired Install section with fresh eyes) rather than another gap-closure plan. There is no
remaining mechanically-closable gap.

---

*Verified: 2026-09-18T08:10:00Z*
*Verifier: Claude (gsd-verifier)*


---

# Round 6 — 2026-09-21: criterion 3 measured

**Plan:** `04-15`, gap-closure round 5. 7 commits, 51 files (45 of them committed measurement
records), 40 live sessions costing $6.34.

**What changed:** Phase 4's one never-measured roadmap success criterion was measured. Criterion 3
asks that a user "can turn the discipline on permanently as an output style, or paste a
system-prompt version in a harness with no skill support, and get equivalent behavior either way."
Rounds 1 through 5 correctly routed this to human/behavioral verification. Round 6 does not route
it — it runs it.

## The five criteria after this round

| # | Criterion | Verdict |
|---|---|---|
| 1 | Before/after pairs per artifact family, after column citing shipped rule numbers | VERIFIED — 4 family sections, 10 distinct allocated tokens, `before-after-family-missing` and `before-after-citation-missing` both enforce it |
| 2 | Install via skills CLI with one command, and as a Claude Code plugin from a manifest in this repo | VERIFIED structurally, live install deferred to Phase 6 (WINDOWS 11) |
| 3 | Output style or pasted system prompt, equivalent behavior either way | **MEASURED AND NOT ESTABLISHED** — see below |
| 4 | A documented re-sync step regenerates both derivatives whenever SKILL.md changes | VERIFIED and exercised this round; DIST-05 moved to complete |
| 5 | README leads with before/after pairs and states an install path for every supported harness | VERIFIED structurally, prose quality deferred (WINDOWS 12) |

## Criterion 3, stated precisely

The comparison ran. It did not find what the criterion's wording asks for, and it did not find the
opposite either.

| route | n | activated | family-line conformant | proxy mean | range |
|---|---|---|---|---|---|
| skill-on | 12 | 9 | 8 | 7.9 | 1-14 |
| style-on | 12 | 11 | 12 | 7.1 | 3-11 |
| prompt-on | 12 | 8 | 9 | 6.3 | 1-10 |

Every pair of arms overlaps on the proxy count, so the measurement did not distinguish the three
routes. The criterion says "equivalent." The records support "not distinguished at n=3." Those are
different claims and only the second one is available, so this verification reports the second one
and marks the criterion addressed rather than satisfied.

Reading the criterion charitably — as asking whether a user choosing route 3 or route 4 is worse
off than a user who installed the skill folder — the answer this run supports is that no penalty
was detected, under caveats the report states in full. Reading it literally, as a positive
equivalence finding, it is not established and cannot be at this sample size.

## What the measurement found that nobody asked for

The activation asymmetry is the round's most useful result and it is not about prose at all. The
installed skill must be triggered and was not in 3 of its 12 sessions; the output style and the
pasted prompt are unconditionally on. For a user deciding between routes, that is a more actionable
fact than any of the proxy means above — and it means skill-on's arm contains unrouted output,
which is why its mean cannot be read as "the skill writes worst."

## Why this round still ends `human_needed`

Not for the reason the previous five rounds did. Criterion 3's mechanical half is now done; what
remains is a different set:

- The `/config` picker (WINDOWS 16, narrowed not closed).
- A published repository (WINDOWS 11, untouched).
- README's prose quality (WINDOWS 12, untouched).
- Round 6's own honest limit: the cold read of the new report was done by the party that wrote it.
  Every prose defect this phase actually caught — G-04-3, G-04-4, G-04-8 — was found by a reader
  who had not written the text, against a gate that was green at the time. That pattern is the best
  evidence in this file about what this round's self-review is worth.
