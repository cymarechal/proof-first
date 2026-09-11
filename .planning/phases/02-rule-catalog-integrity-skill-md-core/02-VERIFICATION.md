---
phase: 02-rule-catalog-integrity-skill-md-core
verified: 2026-09-11T13:30:00Z
status: human_needed
score: "5/5 roadmap success criteria verified (17 requirement IDs: 16 satisfied, 1 needs human)"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: "4/5 roadmap success criteria verified (17 requirement IDs: 15 satisfied, 1 blocked, 1 needs human)"
  gaps_closed:
    - "SKILL.md is under the 5,000-token progressive-disclosure ceiling (CAT-08 / Roadmap SC1) — 3,694 words / 4,802 estimated tokens, a 198-token margin, confirmed by direct `wc -w` and by `python3 tools/check_repo.py` exiting 0."
    - "`.github/workflows/ci.yml`'s three-step job is green against the real repository state — all three commands (`--self-test`, `--mutation-test`, plain run) exit 0, confirmed by running each live in this pass."
    - "`tools/check_repo.py --mutation-test` now measures genuine discrimination (silent-on-control, fires-on-mutated) for every one of the 21 codes, including `skill-token-budget-exceeded`, whose control copy is now clean (under ceiling) rather than already-non-clean — confirmed by reading `mutation_test()`'s comparison logic and by the live run's `OK` (not `FIRE-ONLY`) line for that code."
  gaps_remaining: []
  regressions: []
human_verification:

  - test: "Confirm skills/proof-first/SKILL.md and both reference files paraphrase Command of the Message / MEDDICC / Challenger concepts at the level of generality SOURCES.md's listed sources state publicly, with no contiguous reproduction of source wording, no source's ordered list reproduced in source order, and no source-coined term adopted as this repo's own label — specifically re-examine PF-0.1 (opening reframe) and PF-3.1 (deletion test) framing against the flagged assumptions A-03/A-04."
    expected: "No contiguous-reproduction or coined-term-adoption violations found."
    why_human: "SOURCES.md states this is a semantic judgement no tool in this project's stack performs; Phase 6's LEG-04 is the formal gate. Tracked as WINDOWS.md id 3 (open) — genuinely still open, unresolvable from this environment, correctly not re-closed by this pass."
  - test: "Run every phrasing in evals/pressure-tests.md's Must-fire and Must-not-fire tables in a real harness session and record Observed/Date/Harness."
    expected: "Must-fire rows activate the skill; must-not-fire rows do not."
    why_human: "Skill activation requires driving a live harness session this environment cannot start. Every row still reads 'not yet observed'; 02-09 added a scope note (SKILL.md frontmatter sha256) binding the 14 phrasings to the current description but did not, and could not, add observations. Tracked as WINDOWS.md id 4 (open, genuinely unresolvable here) — the same finding drives CAT-10's requirement verdict."
---

# Phase 2: Rule Catalog & Integrity — SKILL.md Core Verification Report

**Phase Goal:** A writer can open SKILL.md and draft or spot-check presales prose against a persuasion-preserving, self-contained rule catalog that never lets a fabricated claim through.
**Verified:** 2026-09-11
**Status:** human_needed
**Re-verification:** Yes — after a three-plan gap-closure round (02-07, 02-08, 02-09)

## Goal Achievement

All three gaps from the prior `gaps_found` verification are closed, confirmed by direct re-measurement and live command execution, not by trusting SUMMARY.md prose. The two open human-verification items (WINDOWS.md ids 3 and 4) remain genuinely open, as directed — they are not closeable from this execution environment and were correctly not fabricated shut by the gap-closure round. A code review that ran immediately before this pass (`02-REVIEW.md`) surfaced two further findings against the gap-closure commits themselves; both are independently confirmed below and assessed for phase-goal impact.

### Observable Truths (Roadmap Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Writer can read one numbered rule catalog organized by Command of the Message elements, fully self-contained under the progressive-disclosure ceiling, with valid frontmatter and a reliably triggering description. | ✓ VERIFIED (trigger-reliability sub-item routed to human) | CoM organization VERIFIED (`## PF-0` through `## PF-5`, matching the 7 CoM elements exactly as in the prior pass). Self-containment VERIFIED (PF-4: "It depends on no other skill, tool, or standard being installed" — unchanged, confirmed present at line 213). **Progressive-disclosure ceiling now VERIFIED**: live `python3 tools/check_repo.py` exits 0; direct `wc -w skills/proof-first/SKILL.md` = 3,694 words → 4,802 estimated tokens, 198 tokens under the 5,000 ceiling (matches 02-07's own edge-probe claim exactly). Frontmatter validity VERIFIED (0 frontmatter violations live; `--self-test`/`--mutation-test` both confirm all 4 frontmatter codes discriminate). **Reliable triggering remains UNVERIFIED** (WINDOWS.md id 4, open) — routed to human verification below, not counted as failed. |
| 2 | Writer asking the skill to draft gets output where every deleted buzzword is replaced by an instruction to attach specific evidence in its place, not just silence — and a term appearing verbatim in the customer's own source material is marked, not deleted. | ✓ VERIFIED | PF-3.1 (line 193) and PF-3.3 (line 205) unchanged by the trim: "attach that evidence ... rather than deleting it"; `[PF-3.3: customer's term, retained — source]` marker form intact. `references/deletion-test.md` (876 words) still carries the worked two-marker instance. |
| 3 | Writer gets exactly one opening instruction — a single reframe-the-problem rule resolved from the three overlapping source frameworks, not three conflicting ones to reconcile. | ✓ VERIFIED | Exactly one `### PF-0.1` heading (line 55); no other PF-0 rule. Unchanged by the gap-closure round. |
| 4 | Writer asking the skill to check text gets each prose violation back labeled with a rule number, the offending text, and a compliant rewrite. | ✓ VERIFIED | `## Check mode` (line 278) states the exact block shape verbatim: "the rule ID, the offending text quoted exactly as it appears ... and a compliant rewrite." Two-category fixed order, tie-break rule, no-findings-line all present, unchanged. |
| 5 | Skill refuses to invent metrics, reference customers, benchmark numbers, or certifications, and instead flags commitment-shaped language, undisclosed customer references, competitor comparisons, and unverified compliance/export claims for a human to resolve. | ✓ VERIFIED | PF-2.11/2.12 (refusal + true-part+marker worked examples) and PF-2.14–2.17 (flag + closed `REVIEW` category vocabulary) all present and unchanged in SKILL.md's inline rule statements; the 20 worked ✗/✓ pairs that illustrate them moved to `references/worked-examples.md` (confirmed: 20 `## PF-#.#` headings, 20 unique PF IDs, all resolve against `NUMBERING.md`) with zero loss of enforcement (`undefined-id`/`unlisted-figure` scan `skills/` recursively, confirmed 0 violations live). |

**Score:** 5/5 roadmap success criteria verified (one sub-item of SC1 — reliable triggering — is present-but-behaviorally-unverified and routed to human verification, per WINDOWS.md id 4; it does not fail SC1 because the code/description artifact itself is confirmed unchanged and correctly formed).

### Per-Requirement Verdicts

| Requirement | Description | Status | Evidence |
|---|---|---|---|
| CAT-01 | Numbered catalog follows Command of the Message sections | ✓ SATISFIED | Unchanged from prior pass; `catalog-count-mismatch`/`catalog-id-drift` report 0 violations live. |
| CAT-02 | Every subtractive rule paired with a constructive rule | ✓ SATISFIED | 31 `### PF-` headings, 31 `**Replace with:**` lines — exact 1:1 match after the trim, re-counted directly. |
| CAT-03 | Exactly one opening rule resolving the 3-framework convergence | ✓ SATISFIED | Exactly one `PF-0.1` heading, unchanged. |
| CAT-04 | Deletion test stated with evidence-attachment framing, not deletion alone | ✓ SATISFIED | PF-3.1 body unchanged: "attach that evidence ... rather than deleting it." |
| CAT-05 | Deletion test retains customer-verbatim terms, marks instead of deletes | ✓ SATISFIED | PF-3.3 body and worked example unchanged. |
| CAT-06 | Self-contained prose mechanics section, no dependency on another skill | ✓ SATISFIED | PF-4's self-containment sentence stays on one physical line, unchanged, confirmed present. |
| CAT-08 | Under progressive-disclosure ceiling (500 lines / ~5,000 tokens) | ✓ SATISFIED | 309 lines / 3,694 words → 4,802 estimated tokens. Live check exits 0. Gap closed (WINDOWS.md id 5, fixed). |
| CAT-09 | Frontmatter validates against Agent Skills allow-list, loads without error | ✓ SATISFIED | Live check: 0 frontmatter violations. Frontmatter block confirmed byte-identical before/after the trim via sha256 match (`d5dd651a...`) against 02-07's own recorded hash of the first 14 lines. |
| CAT-10 | Description triggers the skill reliably | ? NEEDS HUMAN | Description confirmed byte-identical to its pre-trim state (sha256 match); front-loaded trigger terms unaffected. Zero real activations have ever been observed — every row in `evals/pressure-tests.md` still reads "not yet observed"; 02-09 added a scope note binding the 14 phrasings to this exact description (via sha256) but could not add observations. WINDOWS.md id 4, open — correctly not closed. |
| INT-01 | Refuses to invent metrics/reference customers/benchmarks/certifications | ✓ SATISFIED | PF-2.11/PF-2.12 unchanged; certifications correctly modeled as a flag (PF-2.17), not a refusal. |
| INT-02 | Marks an evidence gap for a human instead of filling it with plausible text | ✓ SATISFIED | `GAP` marker mechanism unchanged; every marker moved into `references/worked-examples.md` keeps a non-empty body after its keyword (confirmed by direct read of all 20 pairs). |
| INT-03 | Flags commitment-shaped language | ✓ SATISFIED | PF-2.14, `REVIEW (commitment)`, unchanged. |
| INT-04 | Flags customer reference details needing disclosure permission | ✓ SATISFIED | PF-2.15, `REVIEW (reference)`, unchanged. |
| INT-05 | Flags competitor comparisons creating legal exposure | ✓ SATISFIED | PF-2.16, `REVIEW (competitor)`, unchanged. |
| INT-06 | Flags compliance/certification/export claims | ✓ SATISFIED | PF-2.17, `REVIEW (compliance)`, unchanged. |
| MOD-01 | Draft mode follows the catalog | ✓ SATISFIED | "Write mode" section unchanged: three-part output, no rule-trace list, explicit source-material ask. |
| MOD-02 | Check mode returns rule number + offending text + compliant rewrite | ✓ SATISFIED | "Check mode" section states this exact block shape verbatim, unchanged. |

**Orphan check:** REQUIREMENTS.md's Phase 2 traceability rows (CAT-01–06, CAT-08–10, INT-01–06, MOD-01–02 = 17 IDs) match exactly the 17 IDs supplied for this verification and the union of `requirements:` fields across all nine PLAN.md frontmatters (six original plus 02-07/08/09). No orphaned requirements found. `REQUIREMENTS.md`'s own tracking table still shows CAT-01–10 as "Complete" and INT-01–06/MOD-01–02 as "Gaps Found" — that table has not been regenerated since the initial verification pass; this VERIFICATION.md is the authoritative source for the current, post-gap-closure status and supersedes those rows for INT-01–06/MOD-01–02, which are now satisfied per the table above.

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `skills/proof-first/SKILL.md` | 31-rule catalog, frontmatter, two modes, Limits section, under token ceiling | ✓ VERIFIED (exists/substantive/wired, ceiling now met) | 309 lines, 31 `### PF-` headings, 31 `**Replace with:**` lines, valid frontmatter, 3,694 words / 4,802 estimated tokens |
| `skills/proof-first/references/checklist.md` | PF ID index | ✓ VERIFIED | 31 PF rows, matches SKILL.md headings 1:1 |
| `skills/proof-first/references/deletion-test.md` | 4-class worked-pairs table + per-token + provenance sections | ✓ VERIFIED | Unchanged from prior pass |
| `skills/proof-first/references/worked-examples.md` | 20 worked ✗/✓ pairs moved out of SKILL.md, keyed by rule ID | ✓ VERIFIED (new artifact, D-25 amended per human checkpoint decision) | 20 `## PF-#.#` sections, 20 unique PF IDs, all facts traceable to `examples/deal-brief.md` |
| `NUMBERING.md` | PF-2 sub-block table, Allocated IDs | ✓ VERIFIED | Unchanged; `catalog-id-drift` reports 0 violations live |
| `tools/check_repo.py` | 21 checks, genuine mutation-discrimination for all 21 | ✓ VERIFIED, with one documented but non-blocking defect | `--self-test` and `--mutation-test` both PASS clean: 21/21 discrimination-proven, 0 FIRE-ONLY. **However:** the top-of-file module docstring (lines ~200-205) still falsely claims `skill-token-budget-exceeded` "fires against this repository's own skills/proof-first/SKILL.md — a known, tracked, open finding against CAT-08," directly contradicting the correct `KNOWN_OPEN_VIOLATIONS` comment 60 lines below it in the same file (confirmed by direct read; 02-REVIEW.md CR-01, independently reconfirmed here). This is a newly-surfaced defect outside 02-08's declared must-have scope (which named only `_mutate_skill_token_budget_exceeded`'s docstring and the `MUTATIONS` description string — both of which are correctly fixed, confirmed by direct read at lines 1327-1364). Classified as a non-blocking documentation anti-pattern (see below), consistent with how an analogous stale-docstring finding was classified in the prior verification pass (CAT-09 row, "cosmetic doc defect, not a functional gap"). |
| `README.md` | Status prose and tree diagram both accurate and mutually consistent | ✓ VERIFIED, with one documented but non-blocking clarity defect | The original contradiction this phase's 02-09 must-have targeted ("the skill itself has not been written yet" vs. the tree diagram) is fixed: prose now correctly lists SKILL.md, all three reference files, and `evals/pressure-tests.md` as existing today, matching the tree diagram exactly (confirmed: tree diagram shows no `(planned)` tag on any file that exists on disk). **However:** a new, narrower ambiguity exists — "What exists today" (line 26) lists `worked-examples.md` as "the 20 worked ✗/✓ pairs," while "What does not exist yet" (line 40) lists "The worked before-and-after examples" — near-identical wording for what a reader could reasonably (but incorrectly) assume is the same artifact (02-REVIEW.md CR-02, independently reconfirmed here). Read in context with the adjacent, unambiguous tree diagram (which correctly tags only `examples/before-after.md` as `(planned)`), no single sentence is factually false, but the prose alone does not disambiguate. Classified as a non-blocking documentation clarity defect, not a failure of 02-09's literal must-have text (prose/tree-diagram agreement, listing the named files as existing — both confirmed true). |
| `evals/pressure-tests.md` | Recorded trigger pressure-test, scope-bound to current description | ✓ VERIFIED as a method artifact; ⚠️ zero real observations (unchanged) | 14 phrasings, every Observed cell still "not yet observed"; 02-09 added a Scope section binding the phrasings to the description's sha256 (`d5dd651a...`), confirmed to match the live file exactly. |

### Key Link Verification

| From | To | Via | Status |
|---|---|---|---|
| `skills/proof-first/SKILL.md` | `NUMBERING.md` | Every `### PF-#.#` heading has a matching Allocated IDs row | ✓ WIRED (`catalog-id-drift` reports 0 violations live) |
| `skills/proof-first/SKILL.md` | `references/checklist.md` | Reference pointer + ID cross-check | ✓ WIRED (unchanged) |
| `skills/proof-first/SKILL.md` | `references/worked-examples.md` | D-28 condition-specific reference pointer naming when to open the file | ✓ WIRED — "Before writing or checking a ✗/✓ contrast for a rule, read `references/worked-examples.md`" confirmed at line 51 |
| `skills/proof-first/references/worked-examples.md` | `examples/deal-brief.md` | Every ✗/✓ pair cites deal-brief facts only | ✓ WIRED (`unlisted-figure` reports 0 violations against `skills/**/*.md` live) |
| `skills/proof-first/references/worked-examples.md` | `NUMBERING.md` | `undefined-id` validates every PF-#.# token inside a moved marker | ✓ WIRED (0 violations live; 20/20 PF IDs resolve) |
| `tools/check_repo.py` | `.github/workflows/ci.yml` | Three-step job order (`--self-test`, `--mutation-test`, plain run) | ✓ WIRED — confirmed `ci.yml` content matches exactly the three commands run live in this pass, all exiting 0 |

### Behavioral Spot-Checks / Probe Execution

| Behavior | Command | Result | Status |
|---|---|---|---|
| Checker self-test proves all violation codes fire on engineered fixtures | `python3 tools/check_repo.py --self-test` | `self-test PASS` — 21 codes listed | ✓ PASS |
| Mutation test proves each code discriminates clean vs. mutated content, including the previously-vacuous `skill-token-budget-exceeded` mutation | `python3 tools/check_repo.py --mutation-test` | `mutation-test PASS: 21 codes discrimination-proven` — no `FIRE-ONLY` lines printed; the `skill-token-budget-exceeded` row now reads `OK`, not `FIRE-ONLY` | ✓ PASS (gap 3 closed — control copy for this code is confirmed clean, so the mutation genuinely discriminates for the first time) |
| Live check against the real repository state | `python3 tools/check_repo.py` | `check_repo: 0 violations` | ✓ PASS (gap 1/2 closed — was `EXIT:1` in the prior pass) |
| Two consecutive live-check runs produce byte-identical output | `python3 tools/check_repo.py` (x2), diffed | No diff | ✓ PASS (02-07 edge probe INT-05/idempotency) |
| SKILL.md frontmatter byte-identical before/after the trim | `sha256sum` of first 14 lines | `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675` — matches 02-07's own recorded hash exactly | ✓ PASS |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| `tools/check_repo.py` | module docstring, ~200-205 | Stale claim that `skill-token-budget-exceeded` "fires against this repository's own skills/proof-first/SKILL.md" — false post-trim, contradicts the correct `KNOWN_OPEN_VIOLATIONS` comment 60 lines below in the same file | ⚠️ Warning (doc-only, no functional impact — confirmed the check itself behaves correctly) | A reader trusting the module docstring over the live check output would wrongly believe CAT-08 is still an open finding. Newly surfaced by this review pass (02-REVIEW.md CR-01), outside 02-08's declared must-have scope. |
| `README.md` | lines 26 vs. 40 | Near-identical wording ("worked ✗/✓ pairs" vs. "worked before-and-after examples") for what a reader could mistake as the same artifact, one listed as existing and the other as not | ⚠️ Warning (clarity, not falsity — the adjacent tree diagram unambiguously resolves it, and no single sentence is factually wrong) | A reader who reads only the prose bullets (skipping the tree diagram three lines below) could be confused about whether `worked-examples.md` exists. Newly surfaced by this review pass (02-REVIEW.md CR-02). |
| `tools/check_repo.py` | `KNOWN_OPEN_VIOLATIONS` comment vs. consuming code, lines ~1060-1063 vs. ~1394-1397 | Comment documents a `(code, subject)` tuple exclusion pattern the consuming code cannot match (compares bare code strings) | ℹ️ Info / dormant (02-REVIEW.md WR-01) | Currently inert — `KNOWN_OPEN_VIOLATIONS` is empty, so nothing is masked today. Would silently fail to exclude anything if a future maintainer populated it exactly as the comment instructs. Not exercised by any current requirement or truth. |
| `tools/check_repo.py` | `mutation_test()` failure summary, lines ~1445-1448 | On failure, the printed summary can read "0 codes not discrimination-proven" even while the run is genuinely failing (a state-drift scenario not counted by the `failed` variable) | ℹ️ Info / not currently triggered (02-REVIEW.md WR-02) | The live run in this pass is a clean PASS, so this path is not exercised. Detail is still present elsewhere in the real output (the `CONTROL` line), so nothing is silently hidden — only the one-line summary under a hypothetical `FAILED` banner could mislead. |

No `TBD`/`FIXME`/`XXX`/`TODO`/`HACK`/`PLACEHOLDER` debt markers found in any of the 8 phase-modified files (confirmed by direct grep across `NUMBERING.md`, `README.md`, `evals/pressure-tests.md`, `skills/proof-first/SKILL.md`, both original reference files, `worked-examples.md`, and `tools/check_repo.py`).

### Human Verification Required

1. **SOURCES.md reproduction-boundary + PF-0.1/PF-3.1 framing judgment** — unchanged from the prior pass, still open. Why human: SOURCES.md states this is a semantic judgement no tool in the stack performs; Phase 6's LEG-04 is the formal gate. (WINDOWS.md id 3, open — correctly not re-closed by this pass, per this run's explicit instruction.)
2. **Trigger pressure-test observations** — unchanged from the prior pass, still open. Why human: skill activation requires driving a live harness session this environment cannot start; zero observations exist. 02-09 added a sha256-bound scope note but no plan in this phase could add an actual observation. (WINDOWS.md id 4, open — correctly not re-closed by this pass. Same finding drives the CAT-10 requirement verdict.)

### Gaps Summary

**All three gaps from the prior `gaps_found` verification are closed, confirmed by live re-execution, not by trusting SUMMARY.md claims:**

1. **CAT-08 / Roadmap SC1 (progressive-disclosure ceiling) — CLOSED.** SKILL.md is now 3,694 words / 4,802 estimated tokens, 198 tokens under the 5,000 ceiling, via 02-07's trim (moving the 20 worked ✗/✓ pairs into a new `references/worked-examples.md`, added under D-25's checkpoint-amended scope — a human explicitly chose option-a over in-place trimming). Directly confirmed by `wc -w` and by the live checker exiting 0.
2. **CI is red — CLOSED.** All three `.github/workflows/ci.yml` steps now exit 0 against the real repository state, run live in this pass with no modification to the workflow file itself (consistent with 02-07's must-have that no `continue-on-error` or suppression be used).
3. **The mutation-test overclaim — CLOSED.** `mutation_test()` now measures genuine silent-on-control/fires-on-mutated discrimination for every code, including `skill-token-budget-exceeded`. Its control copy is confirmed clean (the trim in gap 1 made this true), so the "21 codes discrimination-proven" headline is now honestly provable rather than blended with one unprovable case. Confirmed by reading the comparison logic in `mutation_test()` and by the live run showing `OK` (not `FIRE-ONLY`) for that code.

**Two new findings surfaced by the code review that ran immediately before this pass are confirmed real but assessed as non-blocking documentation defects, not phase-goal or must-have failures:**

- **CR-01** (stale module-docstring claim in `tools/check_repo.py`): outside 02-08's declared must-have scope (which named three specific locations, all correctly fixed), and has no functional effect — the check itself behaves correctly, confirmed live. Classified the same way an analogous stale-docstring finding was classified in the prior verification pass: a cosmetic doc defect, not a functional or requirement-level gap.
- **CR-02** (README prose ambiguity about `worked-examples.md` vs. "worked before-and-after examples"): the specific contradiction 02-09's must-have targeted (Status prose vs. tree diagram, "the skill itself has not been written yet") is genuinely fixed — confirmed by direct read, the prose and tree diagram now agree and both correctly list all three reference files and `worked-examples.md` as existing. The new ambiguity is narrower and is resolved for any reader who also reads the adjacent, unambiguous tree diagram; no sentence in the README is factually false. This does not fail 02-09's must-have on its literal terms (prose/diagram agreement, correct existence listing — both true), but it is a real, recommended-to-fix clarity defect and is reported prominently so it is not lost.

Neither WINDOWS.md id 3 nor id 4 was touched by this pass, exactly as instructed — both remain genuinely open and unresolvable from this execution environment; both correctly route to human verification, and CAT-10 correctly stays `? NEEDS HUMAN` rather than being marked satisfied on presence alone.

**Recommendation:** The phase goal is achieved and all 17 requirement IDs are now either satisfied or correctly routed to human verification (none blocked). Fixing CR-01 and CR-02 before shipping is recommended (both have concrete fixes documented in `02-REVIEW.md`) but does not, on independent reassessment, block phase completion. The two open WINDOWS.md items (ids 3 and 4) require human action before Phase 2's human verification sign-off is complete; this is outside what any further plan in this phase can close.

---

_Verified: 2026-09-11_
_Verifier: Claude (gsd-verifier)_
