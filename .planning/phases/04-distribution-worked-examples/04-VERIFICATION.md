---
phase: 04-distribution-worked-examples
verified: 2026-09-18T08:10:00Z
status: human_needed
score: "4/5 roadmap success criteria VERIFIED (structural); 1/5 (#3) correctly routes to human/behavioral verification by explicit project design"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: human_needed
  previous_score: "4/5 roadmap success criteria VERIFIED (structural); 1/5 (#3) correctly routes to human/behavioral verification by explicit project design"
  gaps_closed:
    - "G-04-3 — examples/before-after.md:20's Solution proposal column no longer claims AWS Control Tower governs Halverton Mutual's on-premises VMware/Oracle estate (Control Tower governs AWS accounts, not on-premises VMs). Re-scoped to 'the new account structure', now agreeing with deal-brief.md:22 and worked-examples.md:32. The Demo column's fabricated two-attribution Feld quotation is collapsed to one attribution, one quotation, verbatim against deal-brief.md:70 including the em dash; the misdirected PF-2.14 'delivery date' marker now names the commitment the sentence actually makes. Both PF-1.9 capability-first shape and PF-3.3 term-level marking — the two things this test was originally written to check — had already passed; the defect fixed here was a third, unanticipated one introduced by the earlier PF-1.9 recast (f8ebf78)."
    - "G-04-4 — README.md no longer claims routes 3 and 4 both 'work today, from a local clone'. Route 3 (output style) is repaired to state its missing copy step (`mkdir -p ~/.claude/output-styles && cp output-styles/proof-first.md ~/.claude/output-styles/`) and destination, distinguished from route 4 (system prompt paste), which needs no step. A new discrimination-proven code, readme-output-style-destination-missing (48th), fails the build if that destination disappears again. Four of five secondary defects (lead-in layout mismatch, opaque rule-namespace pointer, duplicate placeholder disclosure, unbroken Status paragraph) folded in; the fifth (Status section's position/density) is explicitly deferred with a stated reason, not dropped."
  gaps_remaining: []
  regressions: []
overrides: []
gaps: []
deferred:
  - truth: "A live install (npx skills add / claude plugin marketplace add) succeeds against the published repository"
    addressed_in: "Phase 6 (LEG-04 launch gate)"
    evidence: "WINDOWS.md entry 11 (open, unchanged): publish location is frozen as the disclosed <owner>/<repo> placeholder; no git remote exists."
  - truth: "A live Claude Code session actually lists and applies the copied output style through /config"
    addressed_in: "Phase 6 (LEG-04 launch gate)"
    evidence: "WINDOWS.md entry 16 (new this round, unrun-verify): readme-output-style-destination-missing proves README names the correct destination directory; it does not and cannot observe a live harness session listing or applying the style. This repository's own environment drives no live Claude Code session."
human_verification:
  - test: "Once a real repository/owner exists: run `npx skills add <real-owner>/<real-repo>` and `claude plugin marketplace add <real-owner>/<real-repo> && claude plugin install proof-first@proof-first`."
    expected: "Both commands resolve and install the skill/plugin, including a marketplace.json whose plugin entry is mechanically known-complete (CR-01, closed round 3)."
    why_human: "No git remote is configured; a live install is a network-and-harness behavior no file-reading checker can observe. Unchanged this round — 04-12/04-13 did not touch either manifest."
  - test: "Drive a live Claude Code session with `output-styles/proof-first.md` copied to `~/.claude/output-styles/` (per README's now-stated route 3) and selected, and a second live session in a harness with `prompts/system-prompt.md` pasted as the system prompt. Compare both against a session with the skill folder installed on the same task."
    expected: "All three routes apply the same rule text, the same completeness audit, and the same artifact-family conventions, producing comparably disciplined output. Separately, confirm the copied style actually appears in `/config` and applies — the one link WINDOWS entry 16 tracks as unobserved in this environment."
    why_human: "Authored as a `verification: backstop` truth in 04-03-PLAN.md precisely so no automated check marks it passed before Phase 5's benchmark runs. Unchanged in substance; WINDOWS entry 16 is new bookkeeping for a residual this item already covered, not a new requirement."
  - test: "Have a person unfamiliar with this project re-read examples/before-after.md's four after-columns, focused on the two columns 04-12 repaired: the Solution proposal column's AWS Control Tower governance claim (line 20) and the Demo column's Marcus Feld quotation and PF-2.14 marker (line 34)."
    expected: "The Control Tower claim is now true of the product and consistent with deal-brief.md:22 / worked-examples.md:32 (governs the new account structure, not the on-premises estate); the Feld quotation reads as one recorded utterance, not a reconstructed two-part transcript; each after column overall still reads as an applied rewrite grounded in the deal brief, not a paraphrase of the rule text."
    why_human: "Authored as a `verification: backstop` truth in 04-02-PLAN.md — product-scope truth and quotation-fidelity-as-experienced-by-a-reader are semantic judgments no regex in this stack performs. G-04-3's specific defect is fixed and independently reproduced by this verifier (grep-level: 'on-premises estate' governance phrasing now absent, 'governance across the new account structure' present once, Feld's utterance appears once verbatim); the broader backstop truth (does the rewrite genuinely read as applied, not restated) still requires a cold human read."
  - test: "Have a first-time reader open README.md cold, follow route 3's now-stated copy step (`mkdir -p ~/.claude/output-styles && cp output-styles/proof-first.md ~/.claude/output-styles/`), and report whether the Install section is now actionable without cross-referencing other files, and whether the lead-in genuinely reads as leading with a real example."
    expected: "A prospective evaluator understands what the skill does and how to install it within the first screen or two, with no confusion about which of the four routes to pick, and can now execute route 3 to completion using only what README states (up to the point this repository can observe: the file lands in the scanned directory)."
    why_human: "DIST-06's prose-quality half — WINDOWS.md entry 12 (open, narrowed this round: the false 'works today' claim and missing copy step, G-04-4's primary defect, are fixed; what remains open is whether the prose reads well to a cold reader, not whether the steps are complete). Independently reproduced by this verifier: 'work today, from a local clone' no longer appears; the destination directory appears twice; readme-output-style-destination-missing (48th code) now fails the build if the destination is removed again."
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
