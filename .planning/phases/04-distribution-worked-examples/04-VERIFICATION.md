---
phase: 04-distribution-worked-examples
verified: 2026-09-17T09:40:00Z
status: gaps_found
score: "2/5 roadmap success criteria structurally verified outright; 1/5 blocked by a newly-reproduced tooling defect (CR-01); 2/5 correctly route to human/behavioral verification by design"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: human_needed
  previous_score: "3/5 roadmap success criteria structurally verified (2 correctly route to human/behavioral verification by design)"
  gaps_closed:
    - "G-04-1 (rule narration in ✓ columns) — mechanized: example-rule-narration"
    - "G-04-2 (PF-4.1 sentence-length overruns in before-after.md and worked-examples.md) — mechanized: example-sentence-length, 0/17 and 0/31 over the 25-word ceiling"
    - "G-04-4 (invented spelled-out counts) — mechanized: before-after-spelled-count"
    - "G-04-6 (six README defects) — structural half repaired and mechanized (readme-example-drift, readme-example-lead-distance, readme-layout-legend-drift); prose-quality half stays open (WINDOWS.md 12, unchanged from prior round)"
    - "G-04-7 (three deferred 04-REVIEW warnings, WR-01/02/03 from the prior round) — WR-01 (_owner_segment URL forms) and WR-02 (byte-level --check comparison) genuinely fixed; WR-03 (plugin-manifest zero/multi-skill ambiguity) fixed for that specific ambiguity, but code review this round (04-REVIEW.md CR-01) found a distinct, more severe gap in the same function that G-04-7's own stated purpose was to close: marketplace.json's plugin-entry required fields are never checked for presence at all"
  gaps_remaining:
    - "G-04-3 (before-after.md line 20 PF-1.9 inversion) — recast, but 'does this now lead with capability' is an explicit verification:backstop truth, not mechanically closable. Carried forward as human_verification item #3."
    - "G-04-5 (PF-3.3 marker on a whole quotation, not a term) — re-attached, but this is also a semantic verdict, not mechanically closable. Carried forward inside human_verification item #3."
    - "DIST-06 prose-quality half (WINDOWS.md 12) — still open, unchanged. Carried forward as human_verification item #4."
  regressions: []
overrides: []
gaps:
  - truth: "User can install as a Claude Code plugin from a marketplace manifest in this repo, and that manifest's validity is mechanically guaranteed the same way plugin.json's is"
    status: failed
    reason: "check_plugin_manifest_invalid (tools/check_repo.py) enforces PLUGIN_REQUIRED_KEYS only against .claude-plugin/plugin.json's top-level object. marketplace.json's nested plugins[0] entry is checked for its 'source' field alone -- name, displayName, author, license, keywords, and description on that same entry are never checked for presence. This directly contradicts the function's own docstring ('assert both plugin manifests are well-formed... every required key present'). 04-REVIEW.md (this round) reproduced it directly: deleting license/keywords/author/displayName from a scratch copy of marketplace.json's plugin entry still yields 'check_repo: 0 violations'. This matters more than an ordinary latent gap because plan 04-10's stated purpose this round was closing exactly this class of defect (a tool overstating what it checks, G-04-7/WR-03) and it edited this very function without catching CR-01. DIST-02's structural evidence rests on this checker; the checker does not deliver what it claims."
    artifacts:
      - path: "tools/check_repo.py:2617-2702 (check_plugin_manifest_invalid, PLUGIN_REQUIRED_KEYS at 2610-2613)"
        issue: "Required-key presence check runs against plugin_data (plugin.json) only; marketplace_data['plugins'][0] is never iterated against PLUGIN_REQUIRED_KEYS, only its 'source' field is inspected"
    missing:
      - "Enforce PLUGIN_REQUIRED_KEYS (or an explicitly documented, narrower MARKETPLACE_PLUGIN_ENTRY_REQUIRED_KEYS subset if some fields are meant to be marketplace-entry-optional) against marketplace.json's plugins[0] entry, the same way it is enforced against plugin.json"
      - "Add a mutation-test fixture that deletes a required key from marketplace.json's plugin entry specifically (not plugin.json's), so this coverage becomes discrimination-proven rather than assumed"
deferred:
  - truth: "A live install (npx skills add / claude plugin marketplace add) succeeds against the published repository"
    addressed_in: "Phase 6 (LEG-04 launch gate)"
    evidence: "WINDOWS.md entry 11 (open): publish location is frozen as the disclosed <owner>/<repo> placeholder; no git remote exists. Routed to Phase 6's LEG-04 launch gate in both the prior verification round and REQUIREMENTS.md's own DIST-01/DIST-02 closure-condition annotations."
human_verification:
  - test: "Once CR-01 is fixed and re-verified: run `npx skills add <real-owner>/<real-repo>` and `claude plugin marketplace add <real-owner>/<real-repo> && claude plugin install proof-first@proof-first` against the published repository once it exists."
    expected: "Both commands resolve and install the skill/plugin from this repository, including a marketplace.json whose plugin entry is now mechanically known-complete."
    why_human: "No git remote is configured; a live install is a network-and-harness behavior no file-reading checker can observe. Carried forward from the prior round's item #1 (unchanged fact pattern), now additionally gated on CR-01's fix."
  - test: "Drive a live Claude Code session with `output-styles/proof-first.md` selected, and a second live session in a harness with `prompts/system-prompt.md` pasted as the system prompt. Compare both against a session with the skill folder installed on the same task."
    expected: "All three routes apply the same rule text, the same completeness audit, and the same artifact-family conventions, producing comparably disciplined output."
    why_human: "This is model behavior, authored as a verification:backstop truth in 04-03-PLAN.md precisely so no automated check marks it passed before Phase 5's benchmark runs. Carried forward unchanged from the prior round's item #2."
  - test: "Have a person unfamiliar with this project read examples/before-after.md's four after-columns and judge whether each genuinely demonstrates the rewrite its cited rule asks for (including the PF-1.9 recast at line 20 and the PF-3.3 re-attachment, G-04-3/G-04-5), rather than restating the rule's own wording, or marking a whole quotation instead of a term."
    expected: "Each after column reads as an applied rewrite grounded in the deal brief, not a paraphrase of the rule text; PF-1.9 genuinely leads with capability; PF-3.3 marks a term, not a full quotation."
    why_human: "Authored in 04-02-PLAN.md as a verification:backstop truth. Carried forward from the prior round's item #3, now explicitly covering the two gap-closure recasts (G-04-3, G-04-5) that this round's mechanical checks cannot see."
  - test: "Have a first-time reader open README.md cold and report whether the lead-in genuinely reads as leading with a real example, and whether the Install section is clear enough to act on without cross-referencing other files."
    expected: "A prospective evaluator understands what the skill does and how to install it within the first screen or two, with no confusion about which of the four routes to pick."
    why_human: "DIST-06's prose-quality half — WINDOWS.md entry 12 (still open, unchanged). Only the structural half is CI-enforced. Carried forward unchanged from the prior round's item #4."
---

# Phase 4: Distribution & Worked Examples Verification Report

**Phase Goal:** The finished rule catalog reaches a writer through every distribution channel the project promises, backed by real worked examples.
**Verified:** 2026-09-17T09:40:00Z
**Status:** gaps_found
**Re-verification:** Yes — after gap closure

## Project Gate (evidence gathered and independently reproduced by the orchestrator this round)

```
python3 tools/check_repo.py --self-test       -> self-test PASS, 47 verified violation codes
python3 tools/check_repo.py --mutation-test   -> mutation-test PASS: 47 codes discrimination-proven,
                                                  0 unexpected CONTROL, no FIRE-ONLY line
python3 tools/check_repo.py                   -> check_repo: 0 violations
python3 tools/generate_derivatives.py --check -> exit 0
```

Prior round measured 41 discrimination-proven codes; this round measures 47 (+3 from plan 04-07's
example-prose codes, +3 from plan 04-09's README structural codes). All four commands pass green.
This is real evidence the shipped gate is green — it is not, on its own, evidence the gate's own
coverage is complete. See CR-01 below for exactly where that distinction bites.

## Goal Achievement

### Observable Truths (roadmap Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Reader sees before/after pairs covering each of the four artifact families, after column citing real, shipped rule numbers | ✓ VERIFIED (structural) | Unchanged from prior round's structural finding, now further strengthened: G-04-1 (rule narration), G-04-2 (PF-4.1 sentence-length overruns), and G-04-4 (invented spelled-out counts) are now all mechanized and green (`example-rule-narration`, `example-sentence-length`, `before-after-spelled-count`). `examples/before-after.md` now has 0 of 17 ✓-column sentences over the 25-word ceiling (was 8, max 88, mean 45); `worked-examples.md` has 0 of 31 (was 8, max 37), all 28 ✗ columns byte-identical. Content-quality (does the rewrite genuinely apply the rule) and the two remaining semantic recasts (G-04-3 PF-1.9 lead-with-capability, G-04-5 PF-3.3 marker-not-quotation) stay explicit `verification: backstop` truths — routed to human verification, not silently passed. |
| 2 | User can install via the skills CLI with one command, and separately as a Claude Code plugin from a marketplace manifest in this repo | ✗ FAILED (plugin-manifest half) | The skills-CLI half (DIST-01) is unaffected and still structurally sound (README anchor, `publish-location-drift` clean). The plugin-manifest half (DIST-02) is not: this round's code review (04-REVIEW.md CR-01) reproduced that `check_plugin_manifest_invalid` never checks marketplace.json's plugin entry for `name`/`displayName`/`author`/`license`/`keywords`/`description` presence — only `source` is inspected there. Deleting those fields from a scratch marketplace.json still yields `check_repo: 0 violations`, directly contradicting the checker's own docstring. This is the phase's sole automated proof that the manifest driving `claude plugin marketplace add` is well-formed; that proof does not currently hold for the fields it claims to hold. Live install remains additionally unverifiable for the unrelated, previously-disclosed reason (no git remote) — that half is unchanged and still correctly deferred to Phase 6. |
| 3 | User can turn the discipline on permanently as an output style, or paste a system-prompt version, and get equivalent behavior either way | ⚠️ Structural only — routes to human, by design (unchanged) | No change from prior round: both derivatives still exist, reproduce byte-for-byte, carry the identical sha256 stamp, and cover all 39 rule + 4 family headings. The "equivalent behavior" clause remains a deliberate `verification: backstop` truth pending Phase 5's benchmark. |
| 4 | A documented re-sync step exists that regenerates the output style and system prompt whenever SKILL.md changes | ✓ VERIFIED (strengthened) | Unchanged core finding, now stronger: WR-02 (byte-level `--check` comparison, `newline='\n'` pinned on write) is fixed this round, closing the docstring/implementation gap the prior round's Anti-Patterns section flagged as dormant. Reproduced in both directions by the orchestrator: mutating `output-styles/proof-first.md` to CRLF makes `--check` exit 1; restoring it exits 0 — a distinction the prior text-mode comparison could not see. |
| 5 | Reader opens a README that leads with before/after pairs and states an install path for every supported harness | ✓ VERIFIED (structural) | G-04-6's structural half is now fully repaired and mechanized: README's first ✗ line moved to line 14 (was 23), 0 `(exists)` markers remain (was 19), 0 occurrences of the unused `planned` legend term, and cross-file identity between README's and `examples/before-after.md`'s ✗/✓ lines is discrimination-proven (`readme-example-drift`, confirmed to fire and clear in both directions). Heading order (`readme-before-after-order`) and all four install anchors (`readme-install-path-missing`) remain enforced as before. Prose-quality (WINDOWS.md entry 12) stays open, unchanged, routed to human verification. |

**Score:** 2/5 truths (#1, #5) structurally VERIFIED outright, plus #4 fully VERIFIED and strengthened —
3/5 pass cleanly. 1/5 (#2) is FAILED on its plugin-manifest half by a newly-reproduced tooling defect
(CR-01), independent of and more severe than the previously-disclosed live-install ceiling. 1/5 (#3)
is correctly left unverified by explicit project design (measured-claims-or-none discipline). Because
rule 1 of the status decision tree fires on any FAILED truth, this round's status is `gaps_found`,
not `human_needed` — even though four of five truths hold and the human-verification items from the
prior round remain valid and unchanged in substance.

### Gap Detail — CR-01 (the one blocking finding this round)

`check_plugin_manifest_invalid` (`tools/check_repo.py:2617-2702`) enforces `PLUGIN_REQUIRED_KEYS`
against `.claude-plugin/plugin.json`'s top-level object only. `.claude-plugin/marketplace.json`'s
nested `plugins[0]` entry is inspected for its `source` field alone; `name`, `displayName`, `author`,
`license`, `keywords`, and `description` on that same object are never checked for presence at all.
`check_plugin_manifest_version` separately checks `version`, and `check_publish_location_drift`
separately checks the *owner segment* of `homepage`/`repository` — but nothing checks that those two
fields, or the six named above, are even present on the marketplace entry. The function's own
docstring claims it asserts "both plugin manifests are well-formed... every required key present";
that claim is false for marketplace.json's plugin entry, and the code reviewer reproduced this
directly against a scratch copy of the repository (deleting `license`, `keywords`, `author`, and
`displayName` from `marketplace.json`'s entry: `check_repo.py` still reports 0 violations).

This is weighed as a blocker rather than a dormant/latent warning (unlike WR-01/02/03 from the prior
round) for three reasons: (1) it is rated **critical**, not warning, by this round's own code review;
(2) it directly undermines the mechanical evidence this verification chain relies on for DIST-02 — a
marketplace.json missing required distribution metadata would very likely fail a real
`claude plugin marketplace add`/`claude plugin install` call, and the project's sole gate for that is
silent about it; (3) plan 04-10's own stated purpose this round was closing exactly this class of
defect (G-04-7, "a tool overstating what it checks") in this exact function, and it did not catch
this instance. A gap-closure round that edits the very function responsible for a defect class and
still leaves an instance of that class live is not a closed gap — it is an incompletely-closed one.

**This does not retroactively undo G-04-7's genuine fixes.** WR-01 (`_owner_segment` four-URL-form
normalisation) and WR-02 (byte-level `--check` comparison) are independently verified fixed, and the
specific zero-skill/multi-skill ambiguity WR-03 targeted is also fixed. CR-01 is a distinct,
previously-undetected gap in the same area, found by this round's own code review — not a regression
of anything the prior round certified.

### Required Artifacts (unchanged findings from prior round, re-affirmed at 47-code gate; CR-01 delta noted)

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `.claude-plugin/plugin.json` | Plugin manifest DIST-02 install resolves | ✓ VERIFIED | Exists, parses, all required keys present on this file specifically |
| `.claude-plugin/marketplace.json` | Marketplace manifest, one entry rooted at repo root | ⚠️ INCOMPLETE COVERAGE | Exists, parses, `source: "./"` checked — but required-key presence on the nested `plugins[0]` entry is unchecked (CR-01) |
| `tools/check_repo.py` (plugin checks) | 3 codes with 3-part contract, now including the zero/multi-skill disambiguation (WR-03 fix) | ⚠️ PARTIAL | `plugin-manifest-invalid`, `plugin-manifest-version-mismatch`, `publish-location-drift` all still discrimination-proven for what they do check; `plugin-manifest-invalid`'s docstring-vs-implementation gap on marketplace.json is CR-01 |
| `examples/before-after.md` | 4 document-level pairs, real citations, no sentence-length/rule-narration/spelled-count violations | ✓ VERIFIED | 4/4 families, 0/17 ✓ sentences over 25 words, 0 rule-narration hits, 0 spelled cardinals |
| `skills/proof-first/references/worked-examples.md` | Same sentence-length discipline as before-after.md | ✓ VERIFIED (mechanical) | 0/31 ✓ sentences over 25 words (was 8, max 37); MC-31's punctuation defect (WR-01, code review this round) is a disclosed, non-blocking Warning, not a mechanically-checked property |
| `tools/generate_derivatives.py` | stdlib-only generator with byte-level `--check` | ✓ VERIFIED (strengthened) | `newline='\n'` now pinned on write; `--check` compares bytes, not text-mode-translated strings; CRLF-mutation test fires and clears in both directions |
| `output-styles/proof-first.md`, `prompts/system-prompt.md` | DIST-03/DIST-04 derivatives | ✓ VERIFIED | Unchanged from prior round; still hash-stamped, still cover all headings |
| `README.md` | Before/after lead-in, 4 install routes, re-sync step, no cross-file drift | ✓ VERIFIED | First ✗ line now at line 14 (was 23); 0 `(exists)` markers (was 19); cross-file identity with `examples/before-after.md` discrimination-proven in both directions |
| `tools/check_repo.py` (README checks) | 3 new codes this round | ✓ VERIFIED | `readme-example-drift`, `readme-example-lead-distance`, `readme-layout-legend-drift` all discrimination-proven |

### Requirements Coverage

| Requirement | Status | Evidence |
|-------------|--------|----------|
| EX-02 | Structural: SATISFIED (strengthened). Content-quality: NEEDS HUMAN | Sentence-length/rule-narration/spelled-count mechanized this round; PF-1.9/PF-3.3 recasts (G-04-3/G-04-5) and general rewrite-vs-restatement judgment remain backstop truths |
| DIST-01 | Structural: SATISFIED. Live flow: NEEDS HUMAN (unchanged, Phase 6) | Unaffected by CR-01; README anchor and `publish-location-drift` clean |
| DIST-02 | Structural: **BLOCKED (CR-01)**. Live flow: NEEDS HUMAN (unchanged, Phase 6) | `check_plugin_manifest_invalid` does not check marketplace.json's plugin-entry required fields; the mechanical proof this requirement rests on is incomplete |
| DIST-03 | Structural: SATISFIED. Behavioral: NEEDS HUMAN (by design) | Unchanged |
| DIST-04 | Structural: SATISFIED. Behavioral: NEEDS HUMAN (by design) | Unchanged |
| DIST-05 | SATISFIED (strengthened) | WR-02 byte-comparison fix closes the docstring/implementation gap the prior round flagged as dormant |
| DIST-06 | Structural: SATISFIED (strengthened). Prose-quality: NEEDS HUMAN (WINDOWS.md 12, unchanged) | Six README defects (G-04-6) structurally repaired and mechanized; prose-quality half remains open |

No orphaned requirements — unchanged from prior round.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `tools/check_repo.py:2617-2702` (`check_plugin_manifest_invalid`) | 2687-2700 | Marketplace.json's plugin-entry required fields (`name`, `displayName`, `author`, `license`, `keywords`, `description`) are never checked for presence — CR-01 | 🛑 Blocker | Undermines the mechanical proof this phase offers for DIST-02; see Gap Detail above. Not a debt marker (no TBD/FIXME/XXX), but a critical, reproduced code-review finding — treated as a blocker per this report's own adversarial-verification standard. |
| `skills/proof-first/references/worked-examples.md:141-142` | 141-142 | MC-31's ✓ column uses a period instead of a colon before quoted material ("...said in discovery. 'We need...'"), unlike the analogous, correctly-punctuated line in `examples/before-after.md:34` (WR-01, code review this round) | ⚠️ Warning | Non-blocking prose defect in a cited reference file; disclosed, not mechanically enforced, does not fail any requirement's structural half |
| `tools/check_repo.py:2617-2702` | — | Nothing enforces that `plugin.json` and `marketplace.json`'s hand-duplicated fields (`description`, `displayName`, `author`, `license`, `keywords`) stay equal after CR-01 is fixed — only `version` and the owner segment are cross-checked (WR-02 in this round's review, distinct from the WR-02 of the prior round) | ⚠️ Warning | Dormant today (both files currently agree); a narrower, related instance of CR-01's coverage gap; correctly logged as an open review finding, not blocking on its own |
| `tools/check_repo.py:2409-2432` (`check_before_after_spelled_count` docstring) | — | Docstring's "5 such occurrences were measured" is ambiguous between raw regex matches (5) and post-exemption violations (4) (IN-01, code review this round) | ℹ️ Info | Documentation-precision issue only; does not affect the check's actual behavior |
| Plan 04-09's executor session | — | Used `git stash` for a baseline comparison, which #3542 forbids executors from doing | ℹ️ Info | Harmless in this instance — isolation was `none`, no worktrees exist, `git stash list` is empty on inspection — but recorded as a protocol deviation for the project's own tracking |

Zero `TBD`/`FIXME`/`XXX` debt markers and zero `TODO`/`HACK`/`PLACEHOLDER` occurrences found across
the files this phase's gap-closure plans modified. WR-01, WR-02 (marketplace-equality), and IN-01
above are disclosed, dormant, non-blocking code-review findings tracked in `04-REVIEW.md` — correctly
left as follow-up rather than in-phase scope creep. CR-01 is the sole finding elevated to blocker
status this round, for the reasons stated in the Gap Detail section above.

### REQUIREMENTS.md checkbox defect — fixed this round

The prior verification round flagged (as a non-blocking WARNING) that `EX-02`, `DIST-01`, `DIST-02`,
and `DIST-06` were checked `[x]` in `REQUIREMENTS.md` despite each having an explicit unverified
residual stated in its own italic annotation on the same line — a defect this project's memory log
already tracks as recurring (prior fixes in commits `24e7d22` and `80cc1cb`). A repository-wide
re-scan this round found the same pattern on **9** rows, not 4: the prior round's own report only
sampled Phase 4's rows; Phase 3's `AUD-01`, `ART-01`, `ART-02`, `ART-03`, `ART-04`, and `MOD-04` carried
the identical defect. All 9 have been corrected as part of this verification: each checkbox is now
`[ ]` and its Traceability table row is now `Pending`, with every italic evidence annotation left
untouched. `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` now returns `0` (was 9).

This gap-closure round did not cause the defect: the only checkbox flip between the prior commit range
and this round was `DIST-05` (now `[x]`, traceability `Complete`), and that line carries no `UNVERIFIED`
annotation — 04-10 shipped the documented re-sync step with `--check` genuinely byte-comparing, so
that checkbox is earned and was left unchanged.

### Open WINDOWS.md entries touching this phase

- **11** (open) — publish location frozen as `<owner>/<repo>` placeholder; no git remote. Routed to
  Phase 6 LEG-04. Unchanged.
- **12** (open) — DIST-06's prose-quality half unverified by any check. Unchanged.
- **13, 14, 15** (open, `deviation` kind) — three plan-authored verification-script errors documented
  rather than force-fitted; 14 and 15 filed by 04-07 and 04-10 this round. Disclosed, not blocking.

## Human Verification Required

See the `human_verification` list in this file's frontmatter — 4 items, all carried forward from the
prior round with updates where the gap-closure work changed the facts: the live skills-CLI/plugin
install (now additionally gated on CR-01's fix, not just the publish-location placeholder), the
behavioral-equivalence claim across the three distribution routes (unchanged, deferred to Phase 5),
the content-quality judgment on `examples/before-after.md`'s four after-columns (now explicitly
covering the PF-1.9/PF-3.3 recasts, G-04-3/G-04-5), and README's prose-quality/first-reader-clarity
judgment (unchanged, WINDOWS.md 12).

## Gaps Summary

**One gap blocks this phase's goal this round: CR-01.** Five of the seven UAT gaps from the prior
round (`G-04-1`, `G-04-2`, `G-04-4`, and the structural halves of `G-04-6`/`G-04-7`) are genuinely,
mechanically closed — reproduced independently by the orchestrator this round, not taken on
SUMMARY.md's word. The project gate is green at 47 discrimination-proven codes (up from 41), CONTROL
is clean, and no code is FIRE-ONLY.

What blocks `passed` is that this round's own code review (`04-REVIEW.md`) found a critical,
reproduced defect in the tool that was supposed to have exactly this class of defect closed this
round: `check_plugin_manifest_invalid` does not check marketplace.json's plugin-entry required fields
for presence at all, despite its docstring's claim to the contrary. This directly weakens DIST-02's
mechanical evidence and is not the same finding as the previously-disclosed, correctly-deferred
live-install ceiling (WINDOWS.md entry 11) — it is a gap in the *proof*, not merely in the
*demonstration*, and it surfaced only because this round's gap-closure plan (04-10) edited the exact
function responsible without catching it.

Two truths remain correctly routed to human verification by explicit project design (the behavioral-
equivalence claim, and the two remaining semantic backstop truths in the worked examples), and one
remains open for prose-quality reasons (README, WINDOWS.md 12) — none of these three block the phase
goal; they are disclosed ceilings, not oversights, consistent with the prior round's disposition.

Separately, and now fixed as part of this verification: 9 `REQUIREMENTS.md` checkboxes across
Phases 3 and 4 were marked `[x]` without the caveat-annotation convention this project otherwise uses
consistently — corrected to `[ ]`/`Pending` in this pass, with all evidence annotations preserved.

**Recommended next step:** a focused gap-closure plan for CR-01 alone — extend
`check_plugin_manifest_invalid` to enforce `PLUGIN_REQUIRED_KEYS` (or an explicitly documented subset)
against `marketplace.json`'s `plugins[0]` entry, add a mutation-test fixture proving the new coverage
discrimination-proven, and re-verify. WR-01 (worked-examples.md punctuation), the marketplace-equality
warning, and IN-01 (docstring ambiguity) can be folded into the same plan or deferred at the
maintainer's discretion — none of them independently blocks the phase goal.

---

*Verified: 2026-09-17T09:40:00Z*
*Verifier: Claude (gsd-verifier)*
