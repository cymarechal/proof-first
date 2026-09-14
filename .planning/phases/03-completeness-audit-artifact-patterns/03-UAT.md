---
status: testing
phase: 03-completeness-audit-artifact-patterns
source: [03-VERIFICATION.md]
started: 2026-09-14T00:00:00Z
updated: 2026-09-14T00:00:00Z
---

## Current Test

number: 1
name: Standalone completeness audit returns its own verdict (AUD-03)
expected: |
  In a live harness session with the skill installed, ask for the completeness
  audit on its own against a sample document. The session returns
  `## Completeness gaps` and its one-line verdict alone — no `## Integrity flags`,
  no `## Prose violations`, no `## Structural ordering`, and no rewritten document.
awaiting: user response

## Tests

### 1. Standalone completeness audit returns its own verdict (AUD-03)
expected: Asking for the completeness audit alone returns `## Completeness gaps` and its verdict only — no other report section, no rewritten document.
result: [pending]

### 2. Skill classifies the artifact family before applying any rules (MOD-04)
expected: Submit one document per family (RFP answer, proposal section, executive summary, demo/discovery note) plus one genuinely ambiguous document, in both Write and Check mode. Every response states the classified family — or the `**No family fits:**` fallback — before any rule is applied or any finding reported.
result: [pending]

### 3. Check mode prints all four report sections in the fixed order (MOD-03)
expected: Run check mode against a document with findings in every category, and against a clean document. All four sections print in order — `## Integrity flags`, `## Prose violations`, `## Completeness gaps`, `## Structural ordering` — each carrying an explicit no-findings line when empty.
result: [pending]

### 4. A live session never fabricates a rule number (MOD-05, live half)
expected: Across several live check-mode and completeness-audit sessions on varied documents, no cited ID falls outside the 31 allocated `PF-` IDs or the 8 allocated `MC-` IDs.
result: [pending]

### 5. Independent human read of the paraphrase boundary
expected: Read all eight MC dimension bodies in `references/completeness-audit.md` and all four family sections in `references/artifact-patterns.md` end to end against `SOURCES.md` lines 11-22. No contiguous run of any framework source's own wording, no source's ordered list in source order, no source-coined term adopted as this repo's own label. Each MC body reads as a question about a document, not a restatement of the underlying methodology concept.
why_human: Plans 03-01, 03-02 and 03-03 each record this `<human-check>` as self-performed by the executing agent because no human was available in the spawned session. It has not yet had an independent human read.
result: [pending]

## Summary

total: 5
passed: 0
issues: 0
pending: 5
skipped: 0
blocked: 0

## Gaps
