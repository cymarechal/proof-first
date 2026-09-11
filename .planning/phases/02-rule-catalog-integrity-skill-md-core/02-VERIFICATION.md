---
phase: 02-rule-catalog-integrity-skill-md-core
verified: 2026-09-11T00:00:00Z
status: gaps_found
score: 4/5 roadmap success criteria verified (17 requirement IDs: 15 satisfied, 1 blocked, 1 needs human)
behavior_unverified: 1
overrides_applied: 0
gaps:
  - truth: "Writer can read one numbered rule catalog ... fully self-contained under the progressive-disclosure ceiling ... (Roadmap SC1 / CAT-08)"
    status: failed
    reason: "SKILL.md is 368 lines (under the 500-line half of the ceiling) but is estimated at 6,207 tokens (4,775 words x 1.3) against the 5,000-token ceiling — 24% over. `python3 tools/check_repo.py` (live, no flags) exits 1 on this exact finding. This is a content-volume problem, not a formatting artifact, and is tracked as WINDOWS.md id 5 (open)."
    artifacts:
      - path: "skills/proof-first/SKILL.md"
        issue: "Exceeds the 5,000-token progressive-disclosure ceiling CAT-08 requires"
    missing:
      - "Catalog trimming or content restructuring (not re-wrapping, not raising the ceiling — WINDOWS.md id 5 explicitly rules those out) to bring the token estimate under 5,000."
  - truth: "`.github/workflows/ci.yml` is green for this phase's shipped content"
    status: failed
    reason: "Direct consequence of the token-budget breach above. The CI job's third step (`python3 tools/check_repo.py`, no flags) exits 1 against the current repository state. Every push/PR shows red from this commit forward with no `continue-on-error` or explanatory comment in ci.yml (REVIEW.md WR-02)."
    artifacts:
      - path: ".github/workflows/ci.yml"
        issue: "No accommodation for the known-open token-budget finding; live check step fails"
    missing:
      - "Either resolve the token-budget finding, or make the known-open state explicit in CI per REVIEW.md WR-02's suggested fix."
  - truth: "The phase's own enforcement tooling makes only claims it can prove (this repo's own governing 'measured claims or no claims' constraint, applied reflexively to tools/check_repo.py's mutation-test output)"
    status: failed
    reason: "Live `python3 tools/check_repo.py --mutation-test` prints 'mutation-test PASS: 21 codes proven live'. Per REVIEW.md CR-01 (confirmed independently in this verification pass by re-running self-test and mutation-test), `_mutate_skill_token_budget_exceeded`'s control state is already non-clean — the real SKILL.md already exceeds the ceiling before any mutation runs — so that one code's mutation cannot demonstrate discrimination between good and bad content. The true, honestly-provable figure is 20 discrimination-proven codes, not 21. This is exactly the class of overclaim the project exists to prevent, coming from the project's own integrity tool."
    artifacts:
      - path: "tools/check_repo.py"
        issue: "mutation_test() counts skill-token-budget-exceeded as proven live when its control state was never clean"
    missing:
      - "Either make the control state clean before mutating (REVIEW.md CR-01's suggested fix), or print '20 codes discrimination-proven; 1 code confirmed-fire-only' instead of a single blended count."
deferred: []
behavior_unverified_items:
  - truth: "The frontmatter `description` field triggers the skill reliably on presales writing requests (CAT-10; part of Roadmap SC1)"
    test: "Install skills/proof-first/ into a real harness (Claude Code, Cursor, etc.) and run each phrasing in evals/pressure-tests.md's 'Must fire' and 'Must not fire' tables in a fresh session."
    expected: "Every 'Must fire' phrasing activates the skill; every 'Must not fire' phrasing does not."
    why_human: "Skill activation is a per-session harness decision this execution environment cannot drive (no ability to launch a separate harness session, install a skill into it, and read back activation). Every row in evals/pressure-tests.md reads 'not yet observed' — zero real observations exist. Presence of a well-front-loaded, keyword-dense description (verified: 6+ distinct artifact-type terms in the first 200 characters) is necessary but not sufficient to claim 'reliably triggers' under this project's own 'measured claims or no claims' constraint. Tracked as WINDOWS.md id 4 (open)."
human_verification:
  - test: "Confirm skills/proof-first/SKILL.md and both reference files paraphrase Command of the Message / MEDDICC / Challenger concepts at the level of generality SOURCES.md's listed sources state publicly, with no contiguous reproduction of source wording, no source's ordered list reproduced in source order, and no source-coined term adopted as this repo's own label — specifically re-examine PF-0.1 (opening reframe) and PF-3.1 (deletion test) framing against the flagged assumptions A-03/A-04."
    expected: "No contiguous-reproduction or coined-term-adoption violations found."
    why_human: "SOURCES.md states this is a semantic judgement no tool in this project's stack performs, with Phase 6's LEG-04 as the formal gate. Tracked as WINDOWS.md id 3 (open, harvested from 02-01's tracer feedback human-check per workflow.human_verify_mode=end-of-phase)."
  - test: "Run every phrasing in evals/pressure-tests.md's Must-fire and Must-not-fire tables in a real harness session and record Observed/Date/Harness."
    expected: "Must-fire rows activate the skill; must-not-fire rows do not."
    why_human: "Same finding as behavior_unverified_items above (WINDOWS.md id 4, open) — this is the mechanism by which CAT-10 would move from unverified to verified or falsified."
---

# Phase 2: Rule Catalog & Integrity — SKILL.md Core Verification Report

**Phase Goal:** A writer can open SKILL.md and draft or spot-check presales prose against a persuasion-preserving, self-contained rule catalog that never lets a fabricated claim through.
**Verified:** 2026-09-11
**Status:** gaps_found
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths (Roadmap Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Writer can read one numbered rule catalog organized by Command of the Message elements, fully self-contained under the progressive-disclosure ceiling, with valid frontmatter and a reliably triggering description. | ✗ FAILED | CoM organization VERIFIED (PF-1's 7 sub-blocks — Before/After/Capabilities/Metrics/Proof Points/Differentiators/Outcomes — map exactly to PF-1.1/1.2, PF-1.5, PF-1.9, PF-1.13/1.14, PF-1.17, PF-1.21, PF-1.25). Self-containment VERIFIED (`grep -i "install\|load\|other skill"` finds nothing pointing outside `skills/proof-first/`; PF-4 states explicitly "It depends on no other skill, tool, or standard being installed"). Frontmatter validity VERIFIED (live check: 0 frontmatter violations against the real file; `--self-test` and `--mutation-test` both confirm all 4 frontmatter codes discriminate correctly). **Progressive-disclosure ceiling FAILED**: live `python3 tools/check_repo.py` (no flags) exits 1 with `skill-token-budget-exceeded skills/proof-first/SKILL.md is estimated at 6207 tokens (4775 words x 1.3), exceeding the 5000-token ceiling` — confirmed by direct `wc -w` (4775 words). Line count (368) is fine; token estimate is not. **Reliable triggering is UNVERIFIED**, not merely unproven-but-probably-fine — see behavior_unverified_items. |
| 2 | Writer asking the skill to draft gets output where every deleted buzzword is replaced by an instruction to attach specific evidence in its place, not just silence — and a term appearing verbatim in the customer's own source material is marked, not deleted. | ✓ VERIFIED | PF-3.1 (deletion test) states: "If deleting the term changes what the sentence claims, attach that evidence ... in the same sentence rather than deleting it" — evidence-attachment framing, not deletion-only. PF-3.3 states a customer-verbatim term "is retained and marked, not deleted" with the exact marker form `[PF-3.3: customer's term, retained — source]`. `references/deletion-test.md` carries a worked instance showing both a retention marker and a REVIEW marker on one phrase (D-11 compliance). |
| 3 | Writer gets exactly one opening instruction — a single reframe-the-problem rule resolved from the three overlapping source frameworks, not three conflicting ones to reconcile. | ✓ VERIFIED | `## PF-0 — Opening and reframe` contains exactly one rule, `PF-0.1 — The opening reframe`. `references/checklist.md` lists exactly one PF-0 row. NUMBERING.md reserves 8 further PF-0 slots as intentional headroom, not additional rules. |
| 4 | Writer asking the skill to check text gets each prose violation back labeled with a rule number, the offending text, and a compliant rewrite. | ✓ VERIFIED | Check mode section: "Each finding is a block: the rule ID, the offending text quoted exactly as it appears ... and a compliant rewrite." Fixed two-category order (`## Integrity flags` then `## Prose violations`), document-order-then-ascending-ID tie-break, no-findings-line, and verbatim-quote/no-truncation rules are all stated explicitly. |
| 5 | Skill refuses to invent metrics, reference customers, benchmark numbers, or certifications, and instead flags commitment-shaped language, undisclosed customer references, competitor comparisons, and unverified compliance/export claims for a human to resolve. | ✓ VERIFIED | PF-2.11 ("Never invent a metric, a baseline, or a benchmark number") and PF-2.12 ("Never invent a reference customer, a logo, or a named account") are both stated as refusals, each with a worked ✗/✓ pair showing the true part of the sentence shipping with a `GAP` marker in place of the fabrication — matching D-10's "true part + marker" behavior exactly. PF-2.14/2.15/2.16/2.17 flag commitment, reference, competitor, and compliance respectively via the closed `REVIEW (category)` vocabulary, each with a worked example. |

**Score:** 4/5 roadmap success criteria verified (1 present-but-unverified sub-item folded into SC1's failure); see requirement-level table below for granularity.

### Per-Requirement Verdicts

| Requirement | Description | Status | Evidence |
|---|---|---|---|
| CAT-01 | Numbered catalog follows Command of the Message sections | ✓ SATISFIED | PF-1's 7 sub-blocks match the 7 CoM elements; `catalog-count-mismatch`/`catalog-id-drift` report 0 violations live. |
| CAT-02 | Every subtractive rule paired with a constructive rule | ✓ SATISFIED | 31 `### PF-` headings, 31 `**Replace with:**` lines — exact 1:1 match, confirmed by grep count. |
| CAT-03 | Exactly one opening rule resolving the 3-framework convergence | ✓ SATISFIED | Exactly one `PF-0.1` heading; no other PF-0 rule. |
| CAT-04 | Deletion test stated with evidence-attachment framing, not deletion alone | ✓ SATISFIED | PF-3.1 body: "attach that evidence ... rather than deleting it." |
| CAT-05 | Deletion test retains customer-verbatim terms, marks instead of deletes | ✓ SATISFIED | PF-3.3 body and worked example; `references/deletion-test.md`'s "Customer-first terms" row. |
| CAT-06 | Self-contained prose mechanics section, no dependency on another skill | ✓ SATISFIED | PF-4 states "depends on no other skill, tool, or standard being installed"; no external-skill references found anywhere in SKILL.md. |
| CAT-08 | Under progressive-disclosure ceiling (500 lines / ~5,000 tokens) | ✗ BLOCKED | 368 lines (pass) / 6,207 tokens (fail, 24% over). Live check exits 1. WINDOWS.md id 5, open. |
| CAT-09 | Frontmatter validates against Agent Skills allow-list, loads without error | ✓ SATISFIED | Live check: 0 frontmatter violations. `--self-test`/`--mutation-test` both confirm `frontmatter-unparseable`, `frontmatter-unknown-key`, `frontmatter-name-mismatch`, `frontmatter-description-invalid` all discriminate correctly. (Minor: REVIEW.md CR-02 found the description-invalid code's docstring overclaims an "absent" coverage case the code doesn't implement — cosmetic doc defect, not a functional gap for the real file.) |
| CAT-10 | Description triggers the skill reliably | ? NEEDS HUMAN | Description is front-loaded (6+ distinct artifact-type trigger terms inside its first 200 characters, verified). But zero real activations have ever been observed — every row in `evals/pressure-tests.md` reads "not yet observed." Under this project's own "measured claims or no claims" doctrine, "reliably" cannot be honestly asserted on unobserved evidence. WINDOWS.md id 4, open. |
| INT-01 | Refuses to invent metrics/reference customers/benchmarks/certifications | ✓ SATISFIED | PF-2.11 (metrics/baseline/benchmark) and PF-2.12 (reference customer) each stated as an explicit refusal with true-part+marker worked examples. Certifications covered by PF-2.17 (flag, since certification status is externally verifiable, not fabricable by the skill — correctly modeled as a flag, not a refusal). |
| INT-02 | Marks an evidence gap for a human instead of filling it with plausible text | ✓ SATISFIED | PF-2.4 ("cut the claim and mark the gap in its place"), PF-2.11, PF-2.12, PF-2.13 (additive-sweep absences) all route to the same `GAP` marker mechanism. |
| INT-03 | Flags commitment-shaped language | ✓ SATISFIED | PF-2.14, `REVIEW (commitment)`. |
| INT-04 | Flags customer reference details needing disclosure permission | ✓ SATISFIED | PF-2.15, `REVIEW (reference)`. |
| INT-05 | Flags competitor comparisons creating legal exposure | ✓ SATISFIED | PF-2.16, `REVIEW (competitor)`. |
| INT-06 | Flags compliance/certification/export claims | ✓ SATISFIED | PF-2.17, `REVIEW (compliance)`. |
| MOD-01 | Draft mode follows the catalog | ✓ SATISFIED | "Write mode" section: three-part output (family line, prose, register), no rule-trace list, explicit source-material ask per D-23/D-24. |
| MOD-02 | Check mode returns rule number + offending text + compliant rewrite | ✓ SATISFIED | "Check mode" section states this exact block shape verbatim. |

**Orphan check:** REQUIREMENTS.md's Phase 2 traceability rows (CAT-01–06, CAT-08–10, INT-01–06, MOD-01–02 = 17 IDs) match exactly the 17 IDs supplied for this verification and the union of `requirements:` fields across all six PLAN.md frontmatters. No orphaned requirements found. (CAT-07 is correctly attributed to Phase 1 and out of scope here.)

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `skills/proof-first/SKILL.md` | 31-rule catalog, frontmatter, two modes, Limits section | ✓ VERIFIED (exists/substantive/wired) — flagged for token-budget breach, see Truths #1 | 368 lines, 31 `### PF-` headings, 31 `**Replace with:**` lines, valid frontmatter |
| `skills/proof-first/references/checklist.md` | PF ID index | ✓ VERIFIED | 31 PF rows, ascending, matches SKILL.md headings 1:1 |
| `skills/proof-first/references/deletion-test.md` | 4-class worked-pairs table + per-token + provenance sections | ✓ VERIFIED | All 4 classes present with worked pairs; two-marker composed instance present |
| `NUMBERING.md` | PF-2 sub-block table, Allocated IDs | ✓ VERIFIED | PF-2 Proof (2.1-2.10) / Integrity (2.11-2.20) sub-block table present; no rule crosses the boundary |
| `tools/check_repo.py` | 8 new checks (frontmatter x4, catalog-count x2, skill-too-long, sub-block containment) | ✓ VERIFIED, with the CR-01 mutation-proof caveat noted above | `--self-test` and `--mutation-test` both run clean except for the vacuous mutation on `skill-token-budget-exceeded` |
| `README.md` | Layout updated, three shipped skill files no longer "(planned)" | ⚠️ ORPHANED CONTENT (self-contradictory) | Tree diagram correctly updated; Status prose section (lines 14-36) untouched and still asserts "the skill itself has not been written yet" — REVIEW.md CR-03, confirmed by direct read |
| `evals/pressure-tests.md` | Recorded trigger pressure-test | ✓ VERIFIED as a method artifact; ⚠️ zero real observations | 14 phrasings (9 must-fire, 5 must-not-fire), every Observed cell reads "not yet observed" — honestly disclosed, not silently claimed |

### Key Link Verification

| From | To | Via | Status |
|---|---|---|---|
| `skills/proof-first/SKILL.md` | `NUMBERING.md` | Every `### PF-#.#` heading has a matching Allocated IDs row | ✓ WIRED (`catalog-id-drift` reports 0 violations live) |
| `skills/proof-first/SKILL.md` | `references/checklist.md` | Reference pointer + ID cross-check | ✓ WIRED (checklist rows match SKILL.md headings 1:1) |
| `skills/proof-first/SKILL.md` | `references/deletion-test.md` | Reference pointer names the condition requiring the file | ✓ WIRED (pointer text present, condition-specific per D-28) |
| `skills/proof-first/SKILL.md` and reference files | `examples/deal-brief.md` | Every ✗/✓ pair cites deal-brief facts only | ✓ WIRED (`unlisted-figure` reports 0 violations against `skills/**/*.md` live; Halverton/Kestrel/Marcus Feld/Diane Osoria names consistent throughout) |

### Behavioral Spot-Checks / Probe Execution

| Behavior | Command | Result | Status |
|---|---|---|---|
| Checker self-test proves all violation codes fire on engineered fixtures | `python3 tools/check_repo.py --self-test` | `self-test PASS` — 21 codes listed | ✓ PASS |
| Mutation test proves each code discriminates clean vs. mutated content | `python3 tools/check_repo.py --mutation-test` | `mutation-test PASS: 21 codes proven live` | ⚠️ PASS-WITH-CAVEAT — the printed "21" is one higher than the honestly provable "20" (REVIEW.md CR-01, independently reconfirmed here) |
| Live check against the real repository state | `python3 tools/check_repo.py` | `skill-token-budget-exceeded ... EXIT:1` | ✗ FAIL (this is the CAT-08 gap, not a new finding) |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| README.md | 14-36 vs 47-77 | Status prose contradicts its own tree diagram | 🛑 Blocker-adjacent (documentation integrity, not code) | A reader trusting the prose over the tree concludes the opposite of reality for this phase's own deliverable (REVIEW.md CR-03) |
| tools/check_repo.py | mutation_test() / print at :1404-1405 | Overclaimed "21 codes proven live" when 1 code's mutation is vacuous | 🛑 Blocker-adjacent (reflexive integrity failure in the project's own enforcement tool) | Undermines the "measured claims or no claims" doctrine the tool exists to enforce elsewhere (REVIEW.md CR-01) |
| tools/check_repo.py | docstring :144-151 vs code :811-825 | `frontmatter-description-invalid` docstring claims an "absent" coverage case the code routes to a different code | ⚠️ Warning (doc-only) | Minor; functional behavior for the real file is unaffected (REVIEW.md CR-02) |

No `TBD`/`FIXME`/`XXX`/`TODO`/`HACK`/`PLACEHOLDER` debt markers found in any of the 7 phase-modified files (checked directly via grep).

### Human Verification Required

1. **SOURCES.md reproduction-boundary + PF-0.1/PF-3.1 framing judgment** — Confirm no contiguous reproduction of framework source wording and no source-coined term adopted as this repo's own label, specifically for the opening reframe and deletion-test framing. Why human: SOURCES.md states this is a semantic judgement no tool in the stack performs; Phase 6's LEG-04 is the formal gate. (WINDOWS.md id 3, open.)
2. **Trigger pressure-test observations** — Run all 14 phrasings in `evals/pressure-tests.md` in a real harness session and record Observed/Date/Harness. Why human: skill activation requires driving a live harness session this environment cannot start; zero observations currently exist, so CAT-10 cannot honestly be marked verified. (WINDOWS.md id 4, open — same finding drives the CAT-10 requirement verdict and the behavior_unverified_items entry above.)

### Gaps Summary

Three concrete gaps block a clean pass, none of them cosmetic:

1. **CAT-08 / Roadmap SC1 (progressive-disclosure ceiling):** SKILL.md is 24% over its 5,000-token budget. This is disclosed and tracked (WINDOWS.md id 5) but unresolved — the live checker fails on exactly this finding.
2. **CI is red:** the direct, undisclosed-in-CI consequence of (1) — every push/PR shows a failing check with no explanation in `ci.yml` itself.
3. **The project's own integrity tool overclaims by one code:** `mutation-test`'s "21 codes proven live" headline is inaccurate for `skill-token-budget-exceeded`, whose control state was never clean before mutation. This is a small absolute number but a category-defining failure for a project whose entire premise is that claims must be provable — and it is the tool responsible for proving everyone else's claims.

Additionally, two items are correctly disclosed as open rather than silently passed: the SOURCES.md paraphrase-boundary judgment (WINDOWS id 3) and the trigger-reliability observations behind CAT-10 (WINDOWS id 4). Neither is a newly discovered gap — both were already honestly tracked by the phase's own artifacts — but neither is resolved either, so CAT-10 cannot be marked satisfied and both route to human verification rather than a silent pass.

None of the identified gaps are deferred to a later phase; Phase 3's scope (completeness audit, artifact patterns, MOD-03/04/05, distribution manifests) does not cover token-budget trimming, CI accommodation, or the mutation-test count — these are Phase 2's own unresolved obligations.

Everything else — the rule catalog's structure, the integrity refusals and flags (with true-part+marker behavior confirmed by reading the rule bodies), the deletion test and its provenance override, the two modes' output contracts, self-containment, and the checker's frontmatter/count/ID-drift enforcement — is genuinely present, internally consistent, and wired, confirmed by direct reading and by live execution of the checker rather than by trusting SUMMARY.md's narrative.

---

_Verified: 2026-09-11_
_Verifier: Claude (gsd-verifier)_
