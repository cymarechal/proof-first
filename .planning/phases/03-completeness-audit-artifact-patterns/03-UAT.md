---
status: diagnosed
phase: 03-completeness-audit-artifact-patterns
source: [03-VERIFICATION.md]
started: 2026-09-14T00:00:00Z
updated: 2026-09-14T12:00:00Z
---

## Current Test

[testing complete]

## Method

Tests 1-4 were run as genuine live harness sessions, not simulated in the orchestrator
context. An isolated project directory outside this repository received a copy of
`skills/proof-first/` at `.claude/skills/proof-first/` and seven fixture documents
(one per artifact family, one deliberately ambiguous, one carrying findings in every
category, one near-clean). Each session was a fresh `claude -p` invocation with
`--disallowedTools Write Edit Bash NotebookEdit`, no `--bare` (so skill auto-discovery
stayed on), started from that directory. The skill activated on its own description in
every run — it was never named in a system prompt.

18 sessions in total: 6 standalone-audit, 9 check-mode, 6 write-mode (3 of the 6
write-mode runs are reruns after two sessions hit a usage limit and one was retried).
Models: `claude-sonnet-5` and `claude-opus-5`.

Caveat on model coverage: two models, both Anthropic. This says nothing about the
skill's behaviour on a non-Anthropic harness, which the project's own stack notes
call for and which no run here covers.

Caveat on an earlier false finding: a first pass showed duplicated report sections in
4 of 8 runs. That was a defect in this test harness — two batches wrote to the same
output paths concurrently — not in the skill. Every result below comes from the clean
rerun, where each output file had exactly one writer.

Test 5 was performed by two independent subagents, not by a human. See its entry.

## Tests

### 1. Standalone completeness audit returns its own verdict (AUD-03)
expected: Asking for the completeness audit alone returns `## Completeness gaps` and its verdict only — no other report section, no rewritten document.
result: pass
evidence: 6 sessions (4 sonnet-5, 2 opus-5) across 3 documents. Every run emitted `## Completeness gaps` as its only report heading, zero `PF-` citations, no rewritten document, and a verdict line naming how many of the eight dimensions were satisfied and which were not. No run emitted `## Integrity flags`, `## Prose violations`, or `## Structural ordering`.

### 2. Skill classifies the artifact family before applying any rules (MOD-04)
expected: Submit one document per family (RFP answer, proposal section, executive summary, demo/discovery note) plus one genuinely ambiguous document, in both Write and Check mode. Every response states the classified family — or the `**No family fits:**` fallback — before any rule is applied or any finding reported.
result: issue
reported: "14 of 15 sessions conformed. One write-mode session on the solution-proposal fixture cited PF-2.17, PF-2.15 and PF-1.17 as findings without ever stating an artifact family, and stopped to await a 'proceed' reply instead of drafting."
severity: major
post_fix: "Partially closed by 03-05. The turn-ending behaviour is fixed; family-line omission persists in 2 of 16 post-fix write-mode sessions. See gap G-03-2 and WINDOWS.md entry 8."
detail: |
  Check mode: 9/9 conformant. Every run named the family in its first line or first
  heading, before any finding. The ambiguous fixture was correctly reported as spanning
  Demo-and-discovery and Solution-proposal rather than forced into one, in both modes.
  Write mode: 5/6 conformant. The failing run opened with the customer-source-material
  question `SKILL.md` requires, then listed three rule findings, then asked the user to
  reply "proceed". It never classified the document and never drafted.
  Two shipped instructions were broken in that one run: Write mode's "ask for it once,
  proceeding either way" (it did not proceed), and MOD-04's classify-before-rules order
  (it cited three rule IDs first). A retry of the same prompt on the same fixture
  conformed, so this is variance, not a deterministic failure.

### 3. Check mode prints all four report sections in the fixed order (MOD-03)
expected: Run check mode against a document with findings in every category, and against a clean document. All four sections print in order — `## Integrity flags`, `## Prose violations`, `## Completeness gaps`, `## Structural ordering` — each carrying an explicit no-findings line when empty.
result: pass
evidence: 9 check-mode sessions (7 sonnet-5, 2 opus-5) across 7 documents. All four headings printed in the fixed order in 9/9, with no extra, missing, reordered or duplicated section. The one empty section observed across the whole set — `## Integrity flags` on the near-clean fixture — carried an explicit "No findings." line rather than disappearing. Two runs additionally printed a trailing `## Unresolved before this document is sent` register, which the shipped instructions permit.

### 4. A live session never fabricates a rule number (MOD-05, live half)
expected: Across several live check-mode and completeness-audit sessions on varied documents, no cited ID falls outside the 31 allocated `PF-` IDs or the 8 allocated `MC-` IDs.
result: pass
evidence: Every `PF-#.#` and `MC-#` token was extracted from all 18 session transcripts and differenced against the 39 allocated IDs (31 `PF-` headings in `SKILL.md`, 8 `MC-` headings in `references/completeness-audit.md`; `references/checklist.md` matches that set exactly). 224 distinct cited IDs across the 18 files. Zero unallocated IDs in zero files.

### 5. Independent human read of the paraphrase boundary
expected: Read all eight MC dimension bodies in `references/completeness-audit.md` and all four family sections in `references/artifact-patterns.md` end to end against `SOURCES.md` lines 11-22. No contiguous run of any framework source's own wording, no source's ordered list in source order, no source-coined term adopted as this repo's own label. Each MC body reads as a question about a document, not a restatement of the underlying methodology concept.
why_human: Plans 03-01, 03-02 and 03-03 each record this `<human-check>` as self-performed by the executing agent because no human was available in the spawned session. It has not yet had an independent human read.
result: issue
reported: "Two independent readers, run blind to `.planning/` and to each other, both returned ISSUES FOUND. They converge on source dimension labels used as this repository's own working nouns inside six of the eight MC bodies."
severity: major
post_fix: "Closed by 03-05 for `completeness-audit.md`, verified mechanically. One residual occurrence remains in `artifact-patterns.md` line 103 — see gap G-03-5 and WINDOWS.md entry 9. The provenance half (an actual human read) is still open and owned by Phase 6 LEG-04."
performed_by: two independent subagents (opus and sonnet), NOT a human. The provenance half of this test is still open; Phase 6 LEG-04 remains the owner per SOURCES.md.
detail: |
  Verified directly against the file, not taken from the readers' report:
  `completeness-audit.md` uses "economic buyer" (5 times), "champion" (3), "pain" (4),
  "the paper process" (1) and "the buyer's decision process" (1) as this repository's
  own unattributed labels — including in `**Replace with:**` lines, which are
  instruction text a live session repeats. The control holds: "decision criteria" and
  "competition" appear zero times, because MC-11 and MC-36 deliberately route around
  their source labels ("evaluation criteria", "alternatives"). Six of eight bodies do
  not do what two of eight demonstrably can.
  Strongest single instance, both readers independent: MC-21 line 76, "has not stated
  the paper process honestly." "Paper process" is not ordinary business English outside
  the MEDDIC family, and MC-21's own heading already avoids it.
  Weaker instances the readers themselves argued both ways: "economic buyer" and
  "champion" predate the listed sources (Miller Heiman 1985 and general usage), so they
  arguably fail SOURCES.md's "coined by a source" test. "Problem reframe" as a bold
  label in `artifact-patterns.md` was flagged against The Challenger Sale's named
  Reframe step, with the counter-argument that the content underneath is the opposite
  move (deference to the buyer's framing, not an overturning insight).
  Already tracked, not a new finding: both readers independently identified that the
  eight MC blocks reproduce the MEDDICC letter sequence in order. `WINDOWS.md` entry 6
  records exactly this, status `open`, routed to Phase 6 LEG-04. It is not counted as
  part of this gap.

## Summary

total: 5
passed: 3
issues: 2
pending: 0
skipped: 0
blocked: 0

## Gaps

- gap_id: G-03-2
  truth: "The skill states the classified artifact family before applying any rule or reporting any finding, in both modes"
  status: partially_resolved
  resolved_by: 03-05-PLAN.md
  resolved_at: 2026-09-15
  post_fix_evidence: |
    Re-checked independently of the fixing agent: 16 scoreable live write-mode sessions
    against the EDITED skill (sonnet-5 and opus-5, 5 fixtures, fresh isolated dirs,
    skill auto-discovered). 14 named the artifact family before the first applied
    marker; 2 named no family at all (A fixture on opus-5, E fixture on sonnet-5).
    The targeted defect IS fixed: the B fixture, which pre-fix ended its turn on the
    source-material ask without classifying, now names the family first and drafts in
    the same response, on both models.
    The residual is not fixed: roughly 1 in 8 write-mode sessions still omits the
    family line. Pre-fix conformance was 5/6, post-fix 14/16 — the difference is not
    a measurable improvement in the overall rate.
    Ruled out as a cause: a control of 4 runs under the identical write-blocked
    condition conformed 4/4, so the omission is sampling variance rather than an
    artifact of the harness preamble both failures happened to open with.
    Recorded as WINDOWS.md entry 8. MOD-04 stays `[ ]`.

    03-08-PLAN.md measurement (2026-09-15/16), a DIFFERENT recipe from the two figures
    above -- 03-06's committed instrument (evals/conformance/run_conformance.py), its
    own fixture set and prompt, not directly comparable to the 5/6 or 14/16 figures.
    Post-03-07 (family line made unconditional, self-check gate added): 16 of 20
    scoreable write-mode sessions conformant across claude-sonnet-5 and claude-opus-5,
    five fixtures, two repeats (measured SKILL.md blob
    9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a). A same-instrument, same-model paired
    baseline against the pre-03-07 skill (blob 1fc1e1092941157191268a8294ab4e1edc65cdac,
    commit 6f62385) measured 5 of 11 scoreable sonnet-5-only sessions conformant.
    Restricted to sonnet-5 on both sides for a like-for-like comparison: 6 of 10 (60.0%)
    post-03-07 versus 5 of 11 (45.5%) pre-03-07 -- a real, measured improvement from
    03-07's levers, still short of the 87.5% bar the pre-committed decision rule uses.
    Zero sessions in either arm omitted the family line entirely (no genuine no-family
    verdict); every non-conformant session cited a rule marker before naming the family
    (rule-before-family), the actual residual failure mode. Instruction-text changes
    (03-05, 03-07) have now been tried and measured twice under two different recipes;
    both times the rate stayed under the closure bar this rule uses. MOD-04 stays `[ ]`.
    Full run-by-run evidence: evals/conformance/RESULTS-mod04.md.

    03-12-PLAN.md anchored remeasurement (2026-09-16), the first MOD-04 measurement
    produced entirely under 03-09's anchoring fix (FAMILY_LINE_WINDOW_CHARS=400) --
    every figure here is a precise measurement, not an optimistic ceiling like the
    03-06/03-08 figures immediately above. Arm A -- post-03-11 skill (the ordering-gate
    lever under test, blob fadc48613f71fb29d55b42f70805225f9087a2b9): 3 of 10 scoreable
    claude-sonnet-5 sessions conformant (30.0%). Arm B -- paired same-instrument
    baseline, pre-03-11 skill materialised from commit
    c7c1df45e5042636565747f31d4eb5c38513dbac (blob
    9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a): 4 of 10 (40.0%). Delta =
    (N_A/M_A) - (N_B/M_B) = -10.0 percentage points, below the pre-committed rule's
    0.10 improvement threshold, selecting Branch 4 ("did not move"): the honest
    finding is a decline, not flat movement, though at n=10 per arm this sits within
    plausible sampling noise for a true rate difference of zero. Every non-conformant
    session this round scored no-family (no family phrase within the anchored
    400-character window at all); zero scored rule-before-family, a different residual
    shape from every earlier, unanchored measurement of this gap. Three levers have
    now each been measured (03-05 restatement, 03-07 family line plus presence gate,
    03-11 ordering re-scan) and none reached the 87.5% bar. Per Branch 4, WINDOWS.md
    entry 8 is waived (accepted and disclosed, not fixed); MOD-04 stays `[ ]`.
    Full run-by-run evidence and reproduction command: evals/conformance/RESULTS-mod04.md,
    section '## Anchored remeasurement result (03-12)'.
  reason: "User reported: 14 of 15 live sessions conformed; one write-mode session cited PF-2.17, PF-2.15 and PF-1.17 before stating any family, and stopped to await a 'proceed' reply instead of drafting"
  severity: major
  test: 2
  root_cause: "`skills/proof-first/SKILL.md`'s `## Write mode` section states two requirements in two separate paragraphs and never relates them. Paragraph 1 fixes the output as 'exactly three parts, in order', family line first. Paragraph 2 tells the session to name what counts as customer source material and 'ask for it once, proceeding either way'. Nothing states that the ask precedes the family line, nothing forbids emitting a rule finding before the family line, and 'proceeding either way' is the fifth clause of a 34-word sentence rather than its own instruction. A session that takes the ask as a turn-ending question satisfies every sentence it read."
  artifacts:
    - path: "skills/proof-first/SKILL.md"
      issue: "`## Write mode` paragraph 2 buries 'proceeding either way' and never forbids reporting a finding before the family line"
  missing:
    - "State in `## Write mode` that the source-material ask never ends the turn — the draft follows in the same response whether or not material is supplied."
    - "State that no rule ID is cited before the family line, in either mode, so MOD-04's ordering is an instruction rather than an inference from the three-part output shape."
  budget_constraint: "`SKILL.md` carries a 236-token margin under the 5000-token ceiling `skill-token-budget-exceeded` enforces. Both edits must fit inside it or trim restatement to pay for themselves."

- gap_id: G-03-5
  truth: "No source-coined term is adopted as this repository's own label in the MC dimension bodies or the artifact-family sections"
  status: resolved
  resolved_by: 03-05-PLAN.md
  resolved_at: 2026-09-15
  post_fix_evidence: |
    Verified mechanically, not taken from the fixing agent's report: `grep -iE
    'economic buyer|paper process|champion|decision process|pains?'` over
    `references/completeness-audit.md` returns zero hits. All 8 MC headings, all 8 IDs,
    the stated 8-check count and `NUMBERING.md` are unchanged; `check_repo.py`
    self-test, mutation-test and bare run all pass.
    Two further standalone-audit sessions (sonnet-5 and opus-5) confirmed the edited
    MC bodies still cite correctly and the audit output shape is unchanged.
    One residual outside this gap's stated scope: `references/artifact-patterns.md`
    line 103 still reads "Diane Osoria, the economic buyer". The gap scoped the fix to
    the six MC bodies, so this was not covered. Recorded as WINDOWS.md entry 9 rather
    than fixed by widening a verified plan's scope.
  reason: "User reported: two independent readers both returned ISSUES FOUND; six of eight MC bodies use the source's own dimension label as this repository's unattributed working noun, while MC-11 and MC-36 demonstrate the file can avoid them"
  severity: major
  test: 5
  root_cause: "`skills/proof-first/references/completeness-audit.md` was authored dimension by dimension against the frozen `NUMBERING.md` reserved-block labels (Metric, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Pain, Champion, Competition). Six of the eight bodies carried their block label straight into running prose as an unattributed noun; MC-11 and MC-36 substituted a document-facing phrase instead. No acceptance criterion in 03-01 or 03-02 checked for the label appearing in a body, and no `check_repo.py` code can — `SOURCES.md` states the boundary is a semantic judgement no tool in this stack performs."
  artifacts:
    - path: "skills/proof-first/references/completeness-audit.md"
      issue: "lines 22, 23, 38, 41, 43 use 'economic buyer'; 64 'the buyer's decision process'; 76 'the paper process'; 85, 88, 92 'pain'; 99, 102, 104 'champion' — as this repository's own labels, including inside `**Replace with:**` instruction text"
  missing:
    - "Replace each source dimension label in the six affected MC bodies with the document-facing phrase the heading already uses, following MC-11's and MC-36's pattern. MC-21's 'the paper process' is the clearest and should be treated as the minimum fix."
    - "Leave `NUMBERING.md`'s reserved-block labels alone — they are frozen registry structure and are already covered by `WINDOWS.md` entry 6."
    - "Decide whether `artifact-patterns.md`'s `**Problem reframe:**` label needs the same treatment, or whether PF-0.1's existing 'opening reframe' title makes it repo vocabulary already settled in Phase 2 (WINDOWS.md entry 3)."
  not_in_scope: "The MC block ordering matching the MEDDICC letter sequence. `WINDOWS.md` entry 6 already records it, status open, routed to Phase 6 LEG-04."
