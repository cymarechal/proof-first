---
status: complete
phase: 02-rule-catalog-integrity-skill-md-core
source: [02-VERIFICATION.md]
started: 2026-09-11T13:45:00Z
updated: 2026-09-11T13:25:00Z
---

## Current Test

[testing complete]

## Tests

### 1. SOURCES.md paraphrase-boundary read across SKILL.md and both reference files

expected: No contiguous-reproduction or coined-term-adoption violations found. PF-0.1 and PF-3.1 framing clears assumptions A-03/A-04.
why_human: SOURCES.md states this is a semantic judgement no tool in this project's stack performs. Phase 6's LEG-04 is the formal gate. Tracked as WINDOWS.md id 3 (open).
scope_note: The 02-07 trim moved 20 worked ✗/✓ pairs into `references/worked-examples.md` and tightened 16 rule statements. Statements are in scope for this read; the frontmatter is not (byte-identical, sha256 `d5dd651a…`).
result: pass

### 2. Trigger pressure-test — run all 14 phrasings in a real harness session

expected: Every Must-fire row activates the skill; every Must-not-fire row does not. Observed/Date/Harness recorded for each.
why_human: Skill activation requires driving a live harness session this environment cannot start. Every row still reads "not yet observed". Tracked as WINDOWS.md id 4 (open). This is also the sole blocker on requirement CAT-10.
scope_note: `evals/pressure-tests.md`'s `## Scope` section binds these 14 phrasings to the SKILL.md frontmatter `description` whose first 14 lines hash to sha256 `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`. Confirm that hash still matches before recording observations; if it does not, the rows must be re-authored, not filled in.
hash_check: confirmed matching at UAT time (2026-09-11) — `head -14 skills/proof-first/SKILL.md | shasum -a 256` = `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`.
result: pass

## Summary

total: 2
passed: 2
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none]
