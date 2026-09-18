---
phase: 04-distribution-worked-examples
verified: 2026-09-18T06:00:00Z
status: human_needed
score: "4/5 roadmap success criteria VERIFIED (structural); 1/5 (#3) correctly routes to human/behavioral verification by explicit project design"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: "2/5 roadmap success criteria structurally verified outright; 1/5 blocked by a newly-reproduced tooling defect (CR-01); 2/5 correctly route to human/behavioral verification by design"
  gaps_closed:
    - "CR-01 — check_plugin_manifest_invalid now enforces PLUGIN_REQUIRED_KEYS against marketplace.json's plugins[0] entry (previously checked for 'source' alone), proven both against the real repository file (a second registered --mutation-test row, red-then-green observed) and exhaustively (an 18-cell key-by-position --self-test matrix that fails 9/18 when the new loop is removed and 0/18 with it present, independently reproduced by this verifier)."
  gaps_remaining: []
  regressions: []
overrides: []
gaps: []
deferred:
  - truth: "A live install (npx skills add / claude plugin marketplace add) succeeds against the published repository"
    addressed_in: "Phase 6 (LEG-04 launch gate)"
    evidence: "WINDOWS.md entry 11 (open, unchanged): publish location is frozen as the disclosed <owner>/<repo> placeholder; no git remote exists."
human_verification:
  - test: "Once a real repository/owner exists: run `npx skills add <real-owner>/<real-repo>` and `claude plugin marketplace add <real-owner>/<real-repo> && claude plugin install proof-first@proof-first`."
    expected: "Both commands resolve and install the skill/plugin, including a marketplace.json whose plugin entry is now mechanically known-complete (CR-01 closed this round removes the prior additional gating reason)."
    why_human: "No git remote is configured; a live install is a network-and-harness behavior no file-reading checker can observe. Carried forward from prior rounds' item #1, now only gated on the disclosed publish-location ceiling (WINDOWS.md 11), not on CR-01."
  - test: "Drive a live Claude Code session with `output-styles/proof-first.md` selected, and a second live session in a harness with `prompts/system-prompt.md` pasted as the system prompt. Compare both against a session with the skill folder installed on the same task."
    expected: "All three routes apply the same rule text, the same completeness audit, and the same artifact-family conventions, producing comparably disciplined output."
    why_human: "Authored as a `verification: backstop` truth in 04-03-PLAN.md precisely so no automated check marks it passed before Phase 5's benchmark runs. Unchanged from prior rounds' item #2."
  - test: "Have a person unfamiliar with this project read examples/before-after.md's four after-columns and judge whether each genuinely demonstrates the rewrite its cited rule asks for (including the PF-1.9 recast at line 20 and the PF-3.3 re-attachment, G-04-3/G-04-5), rather than restating the rule's own wording or marking a whole quotation instead of a term."
    expected: "Each after column reads as an applied rewrite grounded in the deal brief, not a paraphrase of the rule text; PF-1.9 genuinely leads with capability; PF-3.3 marks a term, not a full quotation."
    why_human: "Authored as a `verification: backstop` truth in 04-02-PLAN.md. Unchanged from prior rounds' item #3 — 04-11 did not touch examples/before-after.md."
  - test: "Have a first-time reader open README.md cold and report whether the lead-in genuinely reads as leading with a real example, and whether the Install section is clear enough to act on without cross-referencing other files."
    expected: "A prospective evaluator understands what the skill does and how to install it within the first screen or two, with no confusion about which of the four routes to pick."
    why_human: "DIST-06's prose-quality half — WINDOWS.md entry 12 (still open, unchanged). Only the structural half is CI-enforced. Unchanged from prior rounds' item #4 — 04-11 did not touch README.md."
---

# Phase 4: Distribution & Worked Examples Verification Report

**Phase Goal:** The finished rule catalog reaches a writer through every distribution channel the project promises, backed by real worked examples.
**Verified:** 2026-09-18T06:00:00Z
**Status:** human_needed
**Re-verification:** Yes — third round, closing the single gap (CR-01) carried by the prior report

This report focuses on what changed since `04-VERIFICATION.md`'s prior round (`gaps_found`, CR-01 the
sole blocker). For the full history of rounds one and two — the seven original UAT gaps, their
mechanization across plans 04-05..04-10, and the 47-code gate's build-up from 41 — see that prior
report's content, superseded here rather than restated. This round's changes are exactly 4 commits,
2 files (`tools/check_repo.py`, `skills/proof-first/references/worked-examples.md`), all from plan
04-11.

## What This Round Closed

**CR-01 is genuinely closed — verified independently, not taken on the SUMMARY's word.** The prior
round's finding was that `check_plugin_manifest_invalid` enforced `PLUGIN_REQUIRED_KEYS` against
`.claude-plugin/plugin.json` only; `marketplace.json`'s nested `plugins[0]` entry — the object
`claude plugin marketplace add` actually reads — was checked for `source` alone. This verifier:

1. **Read the fixed function** (`tools/check_repo.py:2642-2762`) directly and confirmed the
   marketplace `else:` branch now contains `for key in PLUGIN_REQUIRED_KEYS: if key not in entry:`
   immediately before the pre-existing `source` inspection, and a new
   `for key in MARKETPLACE_ENTRY_EQUAL_KEYS:` cross-manifest equality loop guarded on
   `key in entry and key in plugin_data` (no double-reporting an absence as two defects).
2. **Reproduced the fix firing, independently, in a scratch copy of HEAD** — not the orchestrator's
   copy. Deleting `license`, `keywords`, `author`, `displayName` from `.claude-plugin/marketplace.json`'s
   `plugins[0]` produced exactly the four expected `plugin-manifest-invalid ... is missing required
   key '<key>'` lines; restoring the file returned `check_repo: 0 violations`.
3. **Reproduced the new equality guard firing**, independently: changing only `keywords` on the
   marketplace entry produced `plugin-manifest-invalid .claude-plugin/marketplace.json's plugin entry
   'keywords' differs from .claude-plugin/plugin.json's 'keywords'`.
4. **Verified the fix closes the class, not just the instance.** Read the 18-cell self-test matrix
   (`tools/check_repo.py:6636-6650`) and confirmed it iterates the real `PLUGIN_REQUIRED_KEYS`
   constant (not a hand-copied duplicate) against both enforced positions, asserting presence only
   (never exclusivity, so the legitimate co-firing of `plugin-manifest-version-mismatch` on a
   deleted `version` key is correctly not treated as a miss). Then, in a separate scratch copy, this
   verifier removed the Task-1 marketplace-entry loop and re-ran `--self-test`: it produced exactly
   **9** `FAIL: plugin-manifest-invalid did not fire for key '<key>' missing from marketplace.json's
   plugin entry` lines (all 9 keys, all at the marketplace position) plus one additional fixture-level
   FAIL — 10 total — matching the plan's stated discrimination pair (9 matrix misses without the fix,
   0 with it) exactly. This is the evidence that the matrix would have caught CR-01 had it existed
   before 04-10, closing the actual defect class ("a docstring claim sampled at one position, not
   proven at both") rather than only patching the one reported instance.
5. **Confirmed no regression.** `MUTATIONS` is a 48-row list (one new row registered for
   `plugin-manifest-invalid` against the real `marketplace.json`); `discrimination_proven` is
   accumulated as a Python set, so two rows sharing a code correctly collapse to one membership —
   47 unique codes, unchanged, for the documented reason. Reproduced directly:
   `python3 tools/check_repo.py --mutation-test` → `mutation-test PASS: 47 codes discrimination-proven`,
   with two `mutation-test OK: plugin-manifest-invalid` lines (one per manifest position) rather than
   one.
6. **Full project gate reproduced green, independently, at HEAD:** `check_repo.py` → `check_repo: 0
   violations`; `--self-test` → PASS, 47 verified codes, zero `FAIL:` lines; `--mutation-test` → PASS,
   47 codes discrimination-proven, CONTROL 0 unexpected, no FIRE-ONLY line;
   `generate_derivatives.py --check` → exit 0.
7. **WR-01 (MC-31 punctuation), WR-02 (equality guard, folded above), and IN-01 (ambiguous
   measurement wording)** are also folded in per 04-11's plan. Read `worked-examples.md:142` directly:
   it now reads `"Marcus Feld, Halverton Mutual's Vice President of Infrastructure, said in discovery:
   'We need a landing zone we can actually govern'. He added: 'Right now every VM is a snowflake'."` —
   matching `examples/before-after.md:34`'s established two-sentence, colon-introduced construction,
   both sentences (20 and 9 words) inside PF-4.1's 25-word ceiling, and the plain gate confirms 0
   violations with this line in place.
8. **This round's code review** (`04-REVIEW.md`, committed `89bcf34`) independently re-derived all
   five audit claims by loading `check_repo.py` as a module and exercising its fixture builders
   directly rather than trusting the self-test's own narration, and found **0 findings** (critical,
   warning, info all 0) — a genuinely clean re-review, not a rubber stamp, since it explicitly
   re-checked the exact three prior findings (CR-01, WR-01/02, IN-01) it was scoped to confirm closed.

**No anti-patterns found.** `grep -n -E "TBD|FIXME|XXX|TODO|HACK|PLACEHOLDER"` across both files
modified this round returns nothing. No new violation code was registered (`ALL_CHECK_CODES` /
`PLUGIN_CHECK_CODES` unchanged; `KNOWN_OPEN_VIOLATIONS` stays `frozenset()`).

## Goal Achievement

### Observable Truths (roadmap Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Reader sees before/after pairs covering each of the four artifact families, after column citing real, shipped rule numbers | ✓ VERIFIED (structural, unchanged) | 04-11 did not touch `examples/before-after.md`. Prior round's mechanized findings (`example-rule-narration`, `example-sentence-length`, `before-after-spelled-count`, all 0 violations) stand; content-quality judgment on the two semantic recasts (G-04-3, G-04-5) remains an explicit `verification: backstop` truth, routed to human verification #3. |
| 2 | User can install via the skills CLI with one command, and separately as a Claude Code plugin from a marketplace manifest in this repo | ✓ VERIFIED (structural — CR-01 closed this round) | The skills-CLI half (DIST-01) was unaffected throughout. The plugin-manifest half (DIST-02), FAILED last round on CR-01, is now structurally sound: `check_plugin_manifest_invalid` enforces required-key presence on marketplace.json's plugin entry, proven exhaustively (18-cell matrix, independently reproduced discriminating 9/18 → 0/18) and against the real file (a second registered mutation, red-then-green independently reproduced). Live install stays gated on the pre-existing, unrelated, disclosed ceiling (no git remote) — routed to human verification #1 and Phase 6's LEG-04, unchanged in substance. |
| 3 | User can turn the discipline on permanently as an output style, or paste a system-prompt version, and get equivalent behavior either way | ⚠️ Structural only — routes to human, by design (unchanged) | 04-11 touched neither derivative nor the generator. Both derivatives still exist, reproduce byte-for-byte, and cover all rule + family headings. "Equivalent behavior" remains a deliberate `verification: backstop` truth pending Phase 5's benchmark — this verifier abstains rather than inferring a pass from presence, per the non-inferable-truth rule. |
| 4 | A documented re-sync step exists that regenerates the output style and system prompt whenever SKILL.md changes | ✓ VERIFIED (unchanged) | 04-11 did not touch `tools/generate_derivatives.py`. `generate_derivatives.py --check` reproduced exit 0 at HEAD; WR-02 (byte-level comparison, fixed in the prior round) is unaffected by this round's changes. |
| 5 | Reader opens a README that leads with before/after pairs and states an install path for every supported harness | ✓ VERIFIED (structural, unchanged) | 04-11 did not touch `README.md`. Prior round's mechanized findings (`readme-example-drift`, `readme-example-lead-distance`, `readme-layout-legend-drift`, `readme-before-after-order`, `readme-install-path-missing`) stand, reproduced green at HEAD. Prose-quality (WINDOWS.md entry 12) stays open, routed to human verification #4. |

**Score:** 4/5 truths (#1, #2, #4, #5) structurally VERIFIED — up from 3/5 last round now that CR-01's
closure resolves truth #2's FAILED status. 1/5 (#3) is correctly left unverified by explicit project
design (measured-claims-or-none discipline; a `backstop` truth is never inferred VERIFIED from
presence alone). Because no truth is now FAILED, rule 1 of the status decision tree no longer fires.
Rule 2 fires instead: four human-verification items remain open (three carried forward unchanged
because 04-11 never touched their underlying files, one updated to reflect CR-01's closure) — so this
round's status is `human_needed`, not `passed`.

### Required Artifacts (delta from prior round)

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `.claude-plugin/marketplace.json` | Marketplace manifest, plugin entry required-key presence mechanically guaranteed | ✓ VERIFIED (was ⚠️ INCOMPLETE COVERAGE) | Required-key presence now enforced on `plugins[0]`, independently reproduced firing (4/4 deleted keys) and clearing (restored file, 0 violations). |
| `tools/check_repo.py` (plugin checks) | 3 codes, marketplace-entry coverage matching the docstring's claim | ✓ VERIFIED (was ⚠️ PARTIAL) | `plugin-manifest-invalid` now enforces `PLUGIN_REQUIRED_KEYS` at both positions plus `MARKETPLACE_ENTRY_EQUAL_KEYS`; both docstrings (function and module-contract entry) state exactly the two positions covered — read directly, no overstated claim remains. |
| `skills/proof-first/references/worked-examples.md` | MC-31 colon-introduced quotation, PF-4.1 compliant | ✓ VERIFIED | Line 142 reproduces the exact repair claimed (20-word + 9-word sentences), matching `examples/before-after.md:34`'s construction; file line count unchanged (147). |

All other artifacts (`plugin.json`, `before-after.md`, the two derivatives, `README.md`, the README
checker codes) are unchanged from the prior round's ✓ VERIFIED findings — 04-11 did not touch them —
and this verifier's own gate re-run (Step 7) confirms nothing regressed.

### Requirements Coverage

| Requirement | Status | Evidence |
|-------------|--------|----------|
| EX-02 | Structural: SATISFIED (unchanged). Content-quality: NEEDS HUMAN | Unaffected by 04-11; PF-1.9/PF-3.3 recasts and general rewrite-vs-restatement judgment remain backstop truths (human verification #3) |
| DIST-01 | Structural: SATISFIED (unchanged). Live flow: NEEDS HUMAN (Phase 6) | Unaffected by 04-11 or CR-01 |
| DIST-02 | Structural: **SATISFIED (CR-01 closed this round)**. Live flow: NEEDS HUMAN (Phase 6, unrelated disclosed ceiling) | `check_plugin_manifest_invalid` now enforces required-key presence on marketplace.json's plugin entry, independently reproduced firing and clearing |
| DIST-03 | Structural: SATISFIED (unchanged). Behavioral: NEEDS HUMAN (by design) | Unaffected by 04-11 |
| DIST-04 | Structural: SATISFIED (unchanged). Behavioral: NEEDS HUMAN (by design) | Unaffected by 04-11 |
| DIST-05 | SATISFIED (unchanged) | Unaffected by 04-11; `generate_derivatives.py --check` still exit 0 |
| DIST-06 | Structural: SATISFIED (unchanged). Prose-quality: NEEDS HUMAN (WINDOWS.md 12) | Unaffected by 04-11 |

No orphaned requirements. All seven IDs declared across the phase's plans are accounted for above.

**REQUIREMENTS.md checkbox guard:** `grep -c '^- \[x\].*UNVERIFIED' .planning/REQUIREMENTS.md` returns
`0` at HEAD. `DIST-02`'s row is `- [ ]` / Traceability `Pending`, correctly left unchecked — its
live-install half is still unverified for the disclosed, unrelated reason (WINDOWS.md 11). Per the
04-11-PLAN.md prohibition and the SUMMARY's own note, this round's executor deliberately did not run
`requirements.mark-complete`; this verifier did not flip it either. Note: `DIST-05`'s row also reads
`- [ ]` / `Pending` — this is the designed effect of `gaps_found` reverting every checkbox in the phase
during the prior round (per this project's own tracked pattern, not a regression this round introduced
and not something this verifier corrects; a subsequent `passed` status is what re-marks earned
checkboxes complete).

### Anti-Patterns Found

None in the two files this round modified. `grep -n -E "TBD|FIXME|XXX|TODO|HACK|PLACEHOLDER"` across
`tools/check_repo.py` and `skills/proof-first/references/worked-examples.md` returns no matches. No
new violation code registered; `KNOWN_OPEN_VIOLATIONS` stays `frozenset()`.

### Open WINDOWS.md entries touching this phase (unchanged)

- **11** (open) — publish location frozen as `<owner>/<repo>` placeholder; no git remote. Routed to
  Phase 6 LEG-04.
- **12** (open) — DIST-06's prose-quality half unverified by any check.
- **13, 14, 15** (open, `deviation` kind) — disclosed, non-blocking plan-authored verification-script
  errors from prior rounds. No new entry filed this round.

## Human Verification Required

See the `human_verification` list in this file's frontmatter — 4 items. Three are unchanged from the
prior round's substance (04-11 never touched `examples/before-after.md`, `README.md`, or the
derivative generator); the live-install item is updated to drop the additional CR-01 gating clause,
since that gate is now closed — it is gated only on the pre-existing, disclosed publish-location
placeholder (WINDOWS.md 11, Phase 6).

## Gaps Summary

**No gap blocks this phase's goal this round.** CR-01 — the sole `failed` truth carried by the prior
round — is closed, verified independently by this report rather than accepted from `04-11-SUMMARY.md`
or `04-REVIEW.md`'s word: the fix was read directly, the fire/clear behavior was reproduced against a
fresh scratch copy of HEAD in both directions, the exhaustive 18-cell matrix's own discrimination
(9 misses without the fix, 0 with it) was independently reproduced rather than merely re-read, and the
full project gate (self-test, mutation-test, plain run, derivative check) reproduces green with no
regression to the 47-code discrimination-proven total.

What keeps this phase from `passed` is not a defect but four items this project's own design correctly
routes to human judgment rather than a mechanical check: the live install (blocked on an unrelated,
disclosed placeholder, Phase 6), the cross-route behavioral-equivalence claim (an explicit
`verification: backstop` truth reserved for Phase 5's benchmark), the content-quality judgment on the
worked examples' after-columns, and README's prose-quality/first-reader-clarity judgment. None of
these are oversights; all four were disclosed as ceilings in prior rounds and remain so, unmoved by
this round's change set.

**Recommended next step:** route this phase to human verification (the four items above) rather than
another gap-closure plan. There is no remaining mechanically-closable gap.

---

*Verified: 2026-09-18T06:00:00Z*
*Verifier: Claude (gsd-verifier)*
