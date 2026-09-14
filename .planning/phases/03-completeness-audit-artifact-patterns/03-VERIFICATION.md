---
phase: 03-completeness-audit-artifact-patterns
verified: 2026-09-14T00:00:00Z
status: human_needed
score: "4/8 truths verified, 4 present-behavior-unverified (17 requirement IDs mapped: 10 satisfied mechanically, 7 needing a live harness session)"
behavior_unverified: 4
overrides_applied: 0
behavior_unverified_items:
  - truth: "AUD-03 — writer can run the completeness audit independently of the prose rules and get a separate verdict"
    test: "In a live harness session with the skill installed, ask for the completeness audit on its own against a sample document (e.g. examples/deal-brief.md-derived text)."
    expected: "The session returns `## Completeness gaps` and its one-line verdict alone — no `## Integrity flags`, no `## Prose violations`, no `## Structural ordering`, and no rewritten document."
    why_human: "This is model runtime behaviour. `SKILL.md` and `references/completeness-audit.md` carry the instruction text (grep-verified), but no file-reading checker in this repository can observe whether a live session actually obeys it."
  - truth: "MOD-04 — the skill classifies the artifact family before applying any rules, and says which one"
    test: "In a live harness session, submit one document per artifact family (RFP answer, proposal section, executive summary, demo/discovery note) plus one genuinely ambiguous document, in both Write mode and Check mode."
    expected: "Every response states the classified family (or the `**No family fits:**` fallback) before any rule is applied or any finding is reported."
    why_human: "Model runtime behaviour. The classification sentence exists in both Write mode (pre-existing) and the new Check-mode sentence this phase added, and `references/artifact-patterns.md`'s classification procedure and fallback are grep-verified present — but whether a live session actually follows the stated order is unobservable by any check in this repository."
  - truth: "MOD-03 — check mode reports prose violations, completeness gaps, and integrity flags as three separately labeled categories, plus a structural ordering pass"
    test: "Run check mode in a live session against a document with findings in every category, and against a clean document."
    expected: "All four sections (`## Integrity flags`, `## Prose violations`, `## Completeness gaps`, `## Structural ordering`) print in that fixed order every time, each carrying an explicit no-findings line when empty."
    why_human: "Model runtime behaviour, permanently unobservable by a file-reading checker. Additionally flagged: `SKILL.md`'s Check-mode section contains a residual sentence reading \"Findings are grouped under two labelled sections in this fixed order\" immediately before describing all four sections by name — see Anti-Patterns Found. This is a concrete, human-fixable wording defect that a live session may or may not be robust against; a human should judge whether it needs fixing before this truth is trusted."
  - truth: "MOD-05 (live-session half) — check mode never cites a rule number in a live conversation that isn't in the shipped catalog or checklist files"
    test: "Run several live check-mode and completeness-audit sessions across varied documents and inspect every cited rule ID."
    expected: "No cited ID falls outside the 31 allocated `PF-` IDs or the 8 allocated `MC-` IDs."
    why_human: "The shipped-file half of this guarantee is fully and mechanically enforced today (`undefined-id`, `mc-catalog-id-drift`, `mc-count-unstated`/`mc-count-mismatch`, all mutation-proven). The live-session half — that a fresh conversation never fabricates a number — is permanently manual per `.planning/REQUIREMENTS.md`'s own annotation and cannot be closed by any check in this repository."
human_verification:
  - test: "Run the four live-session checks above (AUD-03 standalone run, MOD-04 classification-before-rules, MOD-03 four-section report, MOD-05 live no-invented-citation) in a real installed-skill harness session."
    expected: "See each item's expected column above."
    why_human: "Model runtime behaviour no file-reading checker can observe."
  - test: "Read all eight MC dimension bodies in `skills/proof-first/references/completeness-audit.md` and all four artifact-family sections in `skills/proof-first/references/artifact-patterns.md` end to end against `SOURCES.md`'s reproduction boundary (lines 11-22)."
    expected: "No contiguous run of any framework source's own wording, no source's ordered list reproduced in source order, and no source-coined term adopted as this repository's own label. Confirm each MC body and each family convention reads as a question/instruction about a document rather than a restatement of what the underlying methodology concept means."
    why_human: "Every one of `03-01`, `03-02`, and `03-03`'s SUMMARY files record this exact `<human-check>` as self-performed by the executing agent, not an independent human, because no human was available to respond in the spawned session. The plans explicitly require this be treated as provisional pending end-of-phase UAT — it has not yet had an independent human read."
  - test: "Decide whether `AUD-01`, `ART-01` through `ART-04`, and `MOD-05` should keep their `[x]` Complete checkbox in `.planning/REQUIREMENTS.md` given each carries an italic annotation stating its content-quality or live-session half is UNVERIFIED."
    expected: "A deliberate human decision — either accept `[x]` as \"structurally complete, content/live half tracked separately in the annotation\" (consistent across all six), or revert to `[ ]` to match `AUD-03`/`MOD-04`'s treatment and this repo's own precedent of reverting premature Complete marks (commits `24e7d22`, `80cc1cb`)."
    why_human: "See Gaps Summary and Anti-Patterns Found below — this is a policy call about the project's own completion-tracking discipline, not something this verifier should silently resolve either way."
---

# Phase 3: Completeness Audit & Artifact Patterns Verification Report

**Phase Goal:** A writer can classify a document by artifact family, apply that family's conventions, and get a document-level completeness verdict and trustworthy rule citations — independent of the prose rules.
**Verified:** 2026-09-14
**Status:** human_needed
**Re-verification:** No — initial verification

## Project Gate (independently re-run, not taken on trust)

```
python3 tools/check_repo.py --self-test      -> self-test PASS - 27 verified violation codes
python3 tools/check_repo.py --mutation-test  -> mutation-test PASS: 27 codes discrimination-proven
python3 tools/check_repo.py                  -> check_repo: 0 violations
```

All three confirmed independently in this session, matching the orchestrator's reported figures exactly (27 codes discrimination-proven, control copy clean, no code fire-only).

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | **(SC1, structural half)** Document-level completeness audit derived from MEDDICC, covering all 8 dimensions (metric, economic buyer, decision criteria, decision process, paper process, pain, champion, competition), living in its own `MC-` namespace and reference file, never blended into the prose rules | ✓ VERIFIED | `MC-1, MC-6, MC-11, MC-16, MC-21, MC-26, MC-31, MC-36` present identically across `completeness-audit.md` rule headings, `NUMBERING.md`'s Allocated IDs table, and `checklist.md`'s `## MC rules` table (grep-confirmed, all three sets equal). `mc-rule-in-skill` fails the build if any `SKILL.md` defines an MC heading — confirmed present in `--self-test`'s verified-code list and in `--mutation-test`'s discrimination-proven set. |
| 2 | **(SC1, live half / AUD-03)** Writer can run the completeness audit independently and get a separate verdict | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | `## Running the audit on its own` section exists in `completeness-audit.md` (grep `1`), and `SKILL.md`'s Check mode carries a parallel standalone-run sentence pointing at it. No live session was run in this verification to confirm the behaviour. Routed to human verification. |
| 3 | **(SC2)** Each of the four artifact families (RFP/RFI response, solution proposal, executive summary, demo/discovery material) gets its own conventions and its own expected order | ✓ VERIFIED | All four frozen headings present exactly once in `artifact-patterns.md`; each carries a distinct `**Order:**` line (4 total, verified distinct by direct read — answer-first / architecture-then-capability-then-risk / reframe-then-case-then-list / discovery-then-script-then-criteria-then-follow-up); all 15 frozen element labels (one per ART-01..04 requirement clause) present exactly once. `artifact-family-section-missing` is CI-enforced and mutation-proven. Direct read of all four sections found no verbatim source reproduction in this spot check. |
| 4 | **(SC3, structural half / MOD-04)** Skill states which artifact family it classified the document as before applying any rules | ✓ VERIFIED (text present) | Write mode's pre-existing assumed-family sentence and the new Check-mode classification sentence (`SKILL.md:276`) both exist and both point at `references/artifact-patterns.md`'s classification procedure, which itself carries a `**No family fits:**` fallback (grep-confirmed, present exactly once). |
| 5 | **(SC3, live half / MOD-04)** A live session actually classifies a real document and states the family before applying any rule | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | No live session was run. Routed to human verification. |
| 6 | **(SC4, structural half / MOD-03)** Check mode's report text names four labeled sections (Integrity flags, Prose violations, Completeness gaps, structural ordering pass) in a fixed order | ✓ VERIFIED (text present, with a caveat) | All four section names present in `SKILL.md` in the frozen order, each described distinctly; `## ` heading count unchanged at 13 (none written as a real heading — confirmed by direct grep, matching the plan's own invariant). **Caveat:** the paragraph introducing the sections still reads "Findings are grouped under **two** labelled sections in this fixed order" immediately before naming all four — see Anti-Patterns Found. This is a genuine, human-fixable wording defect this verification located that no acceptance criterion in any of the four plans caught. |
| 7 | **(SC4, live half / MOD-03)** A live check-mode session actually prints all four labeled sections, in that order, each with a no-findings line when empty | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | No live session was run. Routed to human verification. |
| 8 | **(SC5, shipped-file half / MOD-05)** Check mode never cites a rule number that doesn't exist in the shipped catalog or checklist files | ✓ VERIFIED | `undefined-id` scans all of `skills/`, `examples/`, and `README.md` for `PF-#.#`/`MC-#` tokens and fails the build on any unallocated one; `mc-catalog-id-drift` and the two `mc-count-*` codes independently guard the MC registry/definition/checklist three-way agreement. All mutation-proven (part of the 27 discrimination-proven codes), all confirmed live in this session's re-run of `--mutation-test`. |
| 9 | **(SC5, live-session half / MOD-05)** A live check-mode conversation in a fresh session never fabricates a rule number | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | Permanently manual — no file-reading checker in this repository can observe this. `.planning/REQUIREMENTS.md`'s own MOD-05 annotation states the same. Routed to human verification (permanent closure condition: a live harness session recorded at UAT). |

**Score:** 4/8 truths fully verified (5 VERIFIED counting truth 4's text-presence, but 4 of the 8 rows above are present-and-wired with behaviour not exercised). Restated for the frontmatter contract: **4 VERIFIED, 4 PRESENT_BEHAVIOR_UNVERIFIED**, 0 FAILED.

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `skills/proof-first/references/completeness-audit.md` | 8 MC checks, stated-count sentence, standalone-run section, attribution pointer | ✓ VERIFIED | All present; `grep -c '^### MC-'` → 8; `## Running the audit on its own` → 1; `Not affiliated...` pointer → 1 (all directly re-confirmed). |
| `skills/proof-first/references/artifact-patterns.md` | Classification procedure, no-family fallback, 4 family sections with conventions and order | ✓ VERIFIED | All present and directly read; no numbered rule heading minted (`### PF-`/`### MC-` search returns none). |
| `skills/proof-first/references/checklist.md` | `## MC rules` table with all 8 MC IDs | ✓ VERIFIED | All 8 rows present, ascending. |
| `NUMBERING.md` | 8 MC Allocated IDs rows | ✓ VERIFIED | All 8 rows present, ascending, matching the reference file's headings. |
| `tools/check_repo.py` | 5 new violation codes (mc-catalog-id-drift, mc-rule-in-skill, mc-count-unstated, mc-count-mismatch, artifact-family-section-missing) | ✓ VERIFIED | All 5 present in `--self-test`'s verified-code list and `--mutation-test`'s 27 discrimination-proven codes, re-run independently this session. |
| `skills/proof-first/SKILL.md` | Check-mode classification line, 4-section report order, standalone-audit instruction, both new reference pointers, all 31 PF rules intact, token margin ≥150 | ✓ VERIFIED (with the "two labelled sections" wording caveat noted above) | 31/31 rule/`**Replace with:**` parity; 236-token margin (≥150 gate); both pointer bullets present; 13 real headings unchanged. |
| `README.md` | Reflects the two new reference files as existing, correct worked-pair count | ✓ VERIFIED | 28 worked pairs stated and matches actual file section count; `(planned)` count is 4 (down from 6); no leftover "does not exist yet" claim for the Phase 3 files. |
| `.planning/WINDOWS.md` | Open ledger entry routing the MC dimension-order tension to Phase 6 LEG-04 | ✓ VERIFIED | Entry id 6, phase 03, status `open`, present in both the table and the JSON block. |
| `.planning/REQUIREMENTS.md` | Provisional annotations on every Phase 3 requirement whose closure needs a live session | ✓ VERIFIED (annotation text present) — ⚠️ WARNING (checkbox state) | All 9 requirements needing a live/content-quality half carry the "records implementation, not verification" annotation. **However**, 5 of those 9 (`AUD-01`, `ART-01`, `ART-02`, `ART-03`, `ART-04`) plus `MOD-05` are still checked `[x]` Complete in the same file despite the annotation on the same line stating the opposite ("UNVERIFIED"). See Anti-Patterns Found. |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `completeness-audit.md` rule headings | `NUMBERING.md` Allocated IDs | `### MC-\d+ — ` | ✓ WIRED | 8/8 match, `mc-catalog-id-drift` build-enforced. |
| `checklist.md` `## MC rules` | `NUMBERING.md` Allocated IDs | `\| MC-\d+ \|` | ✓ WIRED | 8/8 match. |
| `tools/check_repo.py` | `completeness-audit.md` | `run_catalog_checks` reads MC headings | ✓ WIRED | Confirmed via `--self-test`/`--mutation-test` exercising `check_mc_catalog_id_drift`. |
| `artifact-patterns.md` | `NOTICES.md` | attribution pointer carried once | ✓ WIRED | `grep -c` → 1. |
| `tools/check_repo.py` | `artifact-patterns.md` | `check_artifact_family_sections` reads the 4 required headings | ✓ WIRED | Mutation deletes `## Solution proposal` from the real file and is discrimination-proven. |
| `SKILL.md` | `completeness-audit.md` / `artifact-patterns.md` | reference pointers + inline Check-mode sentences | ✓ WIRED | Both files referenced ≥1 time each in the Reference files list, plus inline in the Check-mode section. |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
| AUD-01 | 03-01, 03-02 | 8-dimension MEDDICC completeness checklist | ✓ SATISFIED (structural) / ? NEEDS HUMAN (content-quality) | 8/8 IDs registered and enforced; content-quality read is self-performed by the executor, not an independent human — REQUIREMENTS.md's own annotation says so. |
| AUD-02 | 03-01 | Own reference file, own `MC-` namespace, never blended | ✓ SATISFIED | `mc-rule-in-skill` + physically separate file; no caveat needed, mechanically closed. |
| AUD-03 | 03-02, 03-04 | Standalone audit run with separate verdict | ? NEEDS HUMAN | Instruction text shipped; live behaviour unobserved. Correctly `[ ]` Pending in REQUIREMENTS.md. |
| ART-01 | 03-03 | RFP/RFI response pattern | ✓ SATISFIED (structural) / ? NEEDS HUMAN (content-quality) | Section + `**Order:**` + all element labels present; content read directly in this session with no reproduction found in spot check, but no independent human paraphrase-boundary read has occurred. |
| ART-02 | 03-03 | Solution proposal pattern | ✓ SATISFIED (structural) / ? NEEDS HUMAN (content-quality) | Same evidence class as ART-01. |
| ART-03 | 03-03 | Executive summary pattern | ✓ SATISFIED (structural) / ? NEEDS HUMAN (content-quality) | Same evidence class as ART-01. |
| ART-04 | 03-03 | Demo/discovery pattern | ✓ SATISFIED (structural) / ? NEEDS HUMAN (content-quality) | Same evidence class as ART-01. |
| MOD-03 | 03-04 | 4-section check-mode report | ✓ SATISFIED (text present) / ? NEEDS HUMAN (live behaviour) | Text present with the "two labelled sections" wording caveat noted above. |
| MOD-04 | 03-03, 03-04 | Classify family before applying rules | ✓ SATISFIED (text present) / ? NEEDS HUMAN (live behaviour) | Both modes' classification sentences and the fallback exist. |
| MOD-05 | 03-01, 03-02, 03-04 | Never cite an undefined rule number | ✓ SATISFIED (shipped-file half) / ? NEEDS HUMAN (live-session half, permanent) | Fully mechanically enforced and mutation-proven for the shipped-file half; live-session half permanently manual. |

No requirement ID is ORPHANED — all 10 of this phase's requirement IDs (`AUD-01..03`, `ART-01..04`, `MOD-03..05`) appear in at least one plan's `requirements:` frontmatter and are cross-referenced in `.planning/REQUIREMENTS.md`.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| `skills/proof-first/SKILL.md` | 282 | Residual wording: "Findings are grouped under **two** labelled sections in this fixed order" — immediately followed by descriptions of all **four** sections (Integrity flags, Prose violations, Completeness gaps, Structural ordering), and by a later sentence correctly saying "All four section headings always print." | ⚠️ Warning | This is a genuine, objectively-verifiable self-contradiction in the primary instruction file a model reads at runtime, introduced when Phase 3 extended the report from 2 to 4 sections but missed updating this specific lead-in sentence (only the later "always print" sentence was updated, per `03-04-SUMMARY.md`'s own account of what it edited). Not caught by any of the four plans' acceptance criteria, none of which grepped for the literal word "two" in this context, nor by the code review (which reviewed `check_repo.py`'s mechanics, not this prose). Low risk of actually breaking live behaviour (the four names and their descriptions immediately follow and are reinforced later), but it is a one-line, unambiguous, trivially fixable defect that should be corrected — change "two" to "four" at `SKILL.md:282`. |
| `.planning/REQUIREMENTS.md` | 34, 40-43, 51 | `AUD-01`, `ART-01` through `ART-04`, and `MOD-05` are checked `[x]` Complete while carrying an italic annotation on the same line stating "content-quality reliability UNVERIFIED" / "live-session reliability UNVERIFIED" | ⚠️ Warning | This is the exact "false Complete" pattern the project's own provisional-annotation mechanism exists to prevent (per every Phase 3 plan's `<output>` instructions, referencing a prior propagated false CAT-10 Complete). Git history confirms the mechanism: each checkbox was mechanically flipped `[ ]` → `[x]` in the same commit that landed the plan's `requirements-completed:` frontmatter field (`952c3c5` for `AUD-01`+`MOD-05`, `ef177fe` for `MOD-05`'s earlier flip, `bcac0c6`'s parent commit for `ART-01..04`), even though those very SUMMARY files explicitly instruct "this must be recorded as provisional pending end-of-phase UAT, not auto-passed off a self-check alone." This repository has reverted this exact mistake twice before (commits `24e7d22` and `80cc1cb`, both titled "revert premature Complete requirements after gaps found"), and `AUD-03`/`MOD-04` in this same phase correctly stayed `[ ]` Pending — showing the more careful treatment was available and applied inconsistently. This is a repo-hygiene defect, not a functional one: none of the underlying artifacts are broken, but the tracking file itself makes an unearned claim, which is squarely against this project's own "measured claims or no claims" constraint. Flagged for a human decision (see `human_verification` above) rather than silently resolved either way by this verifier. |

No debt markers (`TBD`/`FIXME`/`XXX`) found in any file this phase touched. No stub patterns, empty implementations, or hardcoded-empty-data patterns found in the new reference files (`completeness-audit.md`, `artifact-patterns.md`) or in `tools/check_repo.py`'s new code.

### Deferred Items

None. No Phase 3 gap matches a later phase's stated goal or success criteria closely enough to defer (Phase 4 covers distribution/before-after examples, Phase 5 covers the eval harness, Phase 6 covers the LEG-04 legal gate that the MC dimension-order tension is *already* correctly routed to via the open `WINDOWS.md` entry — that routing is itself part of this phase's own completed work, not a deferred gap).

## Human Verification Required

See the `human_verification` list in the frontmatter above for the full, structured set. In summary, three classes of item need a person:

1. **Four live-session behaviour checks** (AUD-03 standalone run, MOD-04 classify-before-rules, MOD-03 four-section report, MOD-05 live no-invented-citation) — none of these can be observed by a file-reading checker, by design; this matches every one of the four plans' own "Honest verification statement" sections.
2. **An independent human paraphrase-boundary read** of all 8 MC dimension bodies and all 4 artifact-family sections against `SOURCES.md`'s reproduction boundary — the plans' own `<human-check>` blocks were self-performed by the executing agent in each case (documented explicitly in every SUMMARY as "no human available to respond in this spawned session"), which is a reasonable stopgap but is not the independent human read the plans themselves call for.
3. **A policy decision** on the six `.planning/REQUIREMENTS.md` checkboxes (`AUD-01`, `ART-01..04`, `MOD-05`) that are marked `[x]` Complete while their own annotation says UNVERIFIED — see Anti-Patterns Found.

## Gaps Summary

No must-have truth FAILED and no required artifact is MISSING or STUB — every mechanical, CI-enforceable half of this phase's five roadmap success criteria is genuinely, independently re-verified in this session (self-test 27/27 codes, mutation-test 27 discrimination-proven with a clean control, bare run 0 violations, all re-run live rather than trusted from the SUMMARY). The phase's own honest-verification discipline (present in every plan's `<verification>` block) already correctly identifies which halves of AUD-03, MOD-03, MOD-04, and MOD-05 are permanently unobservable by any check in this repository, and those are the items routed to human verification here.

Two things this verification located that the phase's own acceptance criteria and code review did not catch, both fixable and neither blocking the phase's structural achievement:

1. A one-line wording defect in `SKILL.md`'s Check-mode section ("two labelled sections" where it should read "four").
2. A tracking-discipline inconsistency in `.planning/REQUIREMENTS.md` — six requirements marked Complete despite carrying UNVERIFIED annotations, reproducing (for the third time in this repository's history) the exact false-Complete pattern its own process exists to prevent.

Neither of these breaks the shipped mechanism the phase built (the CI gate, the MC namespace, the artifact-family conventions are all genuinely present, wired, and mutation-proven), so this report does not mark any roadmap success criterion FAILED. It marks the phase `human_needed` because that is the honest status once the live-session halves and the two located defects are accounted for — a `passed` verdict here would overclaim in exactly the way this project's own "measured claims or no claims" standard forbids.

---

*Verified: 2026-09-14*
*Verifier: Claude (gsd-verifier)*

---

## Post-Verification Resolutions (orchestrator, after this report was written)

Both human-decision items this report raised were resolved by the execute-phase orchestrator
immediately after verification returned. The findings above are left as written — this section
records what changed, not a retraction of what was found.

| Finding | Resolution | Commit |
|---|---|---|
| `SKILL.md` Check-mode paragraph read "grouped under **two** labelled sections" immediately before naming all four | Corrected to "four". Word count unchanged at 3665; estimated tokens 4764; margin 236. No CI code guards this count (`catalog-count-mismatch` covers PF, `mc-count-mismatch` covers MC), which is why all 27 codes passed over it. | `8c41abe` |
| `AUD-01`, `ART-01`-`ART-04`, `MOD-05` carried `[x]` Complete while their own annotations read UNVERIFIED | Reverted to `[ ]` and traceability-table status to `Pending`, matching `AUD-03`/`MOD-04`'s treatment and this repo's precedent (`24e7d22`, `80cc1cb`). `AUD-02` keeps `[x]`: it carries no UNVERIFIED annotation and is mechanically enforced by `mc-rule-in-skill`. | `a30dbd6` |

**Decision rationale for the checkbox call.** The report correctly declined to resolve this
silently and routed it to a human. The orchestrator resolved it toward `[ ]` because the repo's
stated constraint is *measured claims or no claims*: a `[x]` beside an annotation reading
UNVERIFIED is an unmeasured claim in the project's own tracking file, and the two prior reverts
establish the precedent. This was an orchestrator decision, not a human one — a human may
reverse it.

**Gate state after both fixes**, re-run in full: `--self-test` PASS, `--mutation-test` PASS at
27 codes discrimination-proven with control `0 violations`, bare run `0 violations`.

The four PRESENT_BEHAVIOR_UNVERIFIED items are unaffected by these fixes and still require a
live harness session. Phase status remains `human_needed`.
