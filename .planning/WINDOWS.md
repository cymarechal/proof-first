---
schema_version: 1
open_count: 12
waived_count: 1
fixed_count: 6
total_count: 19
last_updated: 2026-09-18T09:36:24.007Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 01 | unrun-verify | examples/deal-brief.md |  | T-01-04 name-collision web search for 4 invented parties + 5 invented persons not run (no live network access in this environment) — human must confirm via web search before repo goes public | fixed |  | 2026-09-10T06:46:57.541Z | 2026-09-10T11:02:49.274Z |
| 2 | 01 | unrun-verify | examples/deal-brief.md |  | D-07/P-05 boundary check (no sentence compares two real products or companies) reviewed by executor via re-read, not confirmed by an independent human reviewer as the plan's <manual> verify step specifies | fixed |  | 2026-09-10T06:46:57.653Z | 2026-09-10T11:02:55.089Z |
| 3 | 02 | unrun-verify | skills/proof-first/SKILL.md |  | Tracer feedback human-check (02-01 Task 1): SOURCES.md reproduction-boundary read plus PF-0.1/PF-3.1 framing judgment (CAT-03/CAT-04 flagged assumptions A-03/A-04) - signed off at end-of-phase UAT 2026-09-11 (02-UAT.md test 1, result pass); stays open because the formal reproduction-boundary gate is Phase 6 LEG-04 | open |  | 2026-09-11T00:38:23.292Z |  |
| 4 | 02 | unrun-verify | evals/pressure-tests.md |  | D-31 trigger pressure-test: must-fire/must-not-fire phrasings recorded with method only — this environment cannot drive a fresh harness session to install the skill and observe activation, so every Observed cell reads 'not yet observed'; a human must run each phrasing in a real harness session and fill in Observed/Date/Harness before this is fixed | open |  | 2026-09-11T01:22:59.066Z |  |
| 5 | 02 | unmet-truth | skills/proof-first/SKILL.md |  | CAT-08 token half: skill-token-budget-exceeded fires against the real SKILL.md (estimated 6207 tokens, words x 1.3, against the 5000-token ceiling) -- content-volume finding, not a formatting artifact (368 lines, well under the line ceiling). Needs catalog trimming or content restructuring in a future plan; do not resolve by re-wrapping or raising the ceiling. | fixed |  | 2026-09-11T01:48:55.000Z | 2026-09-11T04:32:38.278Z |
| 6 | 03 | unrun-verify | skills/proof-first/references/completeness-audit.md |  | The eight MC dimension names (Metric, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Pain, Champion, Competition) and their MC-1 through MC-40 ID-range order were frozen in NUMBERING.md and .planning/REQUIREMENTS.md before Phase 3 began, and that order matches the MEDDICC acronym's own canonical sequence. SOURCES.md states that a source's own ordered list reproduced in its order is reproduction, not paraphrase, and that no tool in this stack performs that judgment. Phase 3 used content levers only: every dimension's audit question is written in this repository's own words, grounded entirely in examples/deal-brief.md's facts, and Phase 3 deliberately did not reorder or rename any dimension. The paraphrase-boundary judgment on the inherited ID-range order itself is routed to Phase 6's LEG-04 gate, which is this entry's closure condition. | open |  | 2026-09-14T08:17:27.877Z |  |
| 7 | 03 | unmet-truth | skills/proof-first/references/completeness-audit.md |  | 03-05's single standalone-audit re-check (docs/B-proposal-section.md) printed an unrequested ## Artifact family section before ## Completeness gaps, diverging from 'Running the audit on its own's stated shape ('returns...and nothing more') and from 03-UAT.md test 1's 6/6 clean result. One-sample variance, not reproduced across multiple runs; AUD-03 was still marked Complete in this plan on the strength of the 6/6 Phase 3 UAT evidence, but this single later sample is recorded so it isn't silently lost. | fixed |  | 2026-09-14T12:38:38.005Z | 2026-09-15T03:04:40.278Z |
| 8 | 03 | unmet-truth | skills/proof-first/SKILL.md |  | MOD-04 anchored remeasurement (03-12), the first measurement of this residual produced entirely under 03-09's anchored scorer (FAMILY_LINE_WINDOW_CHARS=400) rather than the unbounded pre-fix search -- every figure below is a precise measurement, not an optimistic ceiling. Prior figures retained for the record: 03-05's unanchored UAT recipe measured 5/6 then 14/16; 03-08's same-instrument unanchored measurement of 03-07's levers measured 16/20 (both models) with a 5/11 sonnet-5-only paired baseline (6/10 vs 5/11 same-model, 45.5%->60.0%). None of those four are directly comparable to this round's figures (different scorer, or different recipe entirely). This round: Arm A -- post-03-11 skill (blob fadc48613f71fb29d55b42f70805225f9087a2b9), the ordering-gate lever under test -- scored 3 of 10 scoreable claude-sonnet-5 sessions conformant (30.0%). Arm B -- the paired same-instrument baseline, pre-03-11 skill materialised from commit c7c1df45e5042636565747f31d4eb5c38513dbac (blob 9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a) -- scored 4 of 10 (40.0%). The delta (N_A/M_A - N_B/M_B = -10.0 percentage points) is below the pre-committed rule's 0.10 improvement threshold, selecting Branch 4: the honest finding is a decline, not merely flat movement, though at n=10 per arm this is within plausible sampling noise for a true rate difference of zero. Every non-conformant session this round scored no-family (no family phrase within the anchored 400-character window at all); zero sessions scored rule-before-family, a different residual shape from every earlier, unanchored measurement of this entry. Three levers have now each been measured and none reached the 87.5% closure bar: 03-05's restatement, 03-07's five-value family line plus presence gate, and 03-11's self-check ordering re-scan. This residual is accepted and disclosed as a known, measured limitation -- not hidden, and not claimed satisfied. Full run-by-run evidence, exclusions, and the reproduction command: evals/conformance/RESULTS-mod04.md, section '## Anchored remeasurement result (03-12)'. | waived | Anchored remeasurement (03-12): Arm A (post-03-11, ordering-gate lever) 3/10 (30.0%) conformant vs. Arm B (pre-03-11, paired same-instrument baseline) 4/10 (40.0%) -- a -10.0 percentage-point delta, selecting the pre-committed rule's Branch 4 (delta < 0.10). Three levers now measured (03-05 restatement, 03-07 family line plus presence gate, 03-11 ordering re-scan) and none reached the 87.5% bar. This is the first anchored (non-optimistic-ceiling) MOD-04 measurement; the residual is accepted and disclosed, not satisfied. Full evidence: evals/conformance/RESULTS-mod04.md, section Anchored remeasurement result (03-12). Explicit v1 disposition decided 2026-09-16 by the project owner (human, in an interactive /gsd-execute-phase 03 --gaps-only session, not the executing agent on the project's behalf): Option A, accept and disclose. See evals/conformance/RESULTS-mod04.md, section '## v1 disposition decision (03-15)'. | 2026-09-15T01:50:32.188Z | 2026-09-16T09:15:30.640Z |
| 9 | 03 | unmet-truth | skills/proof-first/references/artifact-patterns.md |  | Residual source label outside 03-05's scope: artifact-patterns.md line 103 still reads 'Diane Osoria, the economic buyer'. Plan 03-05 scoped the G-03-5 fix to the six affected MC bodies in completeness-audit.md, so this one occurrence in the Executive summary family section was not covered and is the last remaining instance of a frozen NUMBERING.md registry label used as this repository's own unattributed noun in shipped skill content. One-word fix ('the person who signs'); left unmade rather than silently widening a verified plan's scope. Closure: fold into the next content plan or into Phase 6 LEG-04 alongside entries 3 and 6. | fixed |  | 2026-09-15T01:50:41.248Z | 2026-09-15T03:04:40.161Z |
| 10 | 03 | unmet-truth | evals/conformance/run_conformance.py |  | Self-test behavior case 11 in evals/conformance/run_conformance.py, added by 03-13 to prove that _write_result_line()'s flush call makes each scored session durable against a process interruption, did not discriminate the flush call's presence from its absence, because the interrupting exception was caught inside the same block whose own close-on-exit flushed the file regardless. A future silent deletion of that one line would have reintroduced the exact data-loss bug that has already destroyed two real measurement runs, shipping with a green self-test and a green CI -- the failure mode this repository's own mutation-testing preamble exists to prevent. Two independent reproductions: 03-REVIEW.md's round-5 CR-01 and 03-VERIFICATION.md's verifier, each by copying the script to a sibling path inside evals/conformance/, removing the flush call and observing a clean self-test PASS. The fix: 03-16 rewrote case 11 to assert the recorded write-then-flush call sequence through a proxy handle and to read the results file before the underlying handle is closed, proven in both directions by a one-time mutation probe. The residual and its route: run_conformance.py still ships no committed mutation harness of its own, unlike tools/check_repo.py --mutation-test, so this discrimination is proven once rather than continuously; that narrower guarantee is disclosed in the module docstring, in RESULTS-mod04.md's Self-test discrimination correction (03-16) section and here, and is routed to Phase 5's eval-harness work rather than claimed closed. | fixed |  | 2026-09-17T04:10:16.975Z | 2026-09-17T04:10:23.158Z |
| 11 | 04 | unrun-verify | .claude-plugin/plugin.json |  | Publish location frozen as the placeholder <owner>/<repo> (P4-03): .claude-plugin/plugin.json's homepage/repository, .claude-plugin/marketplace.json's homepage/repository/owner.url all state https://github.com/<owner>/<repo> or https://github.com/<owner>, enforced consistent by publish-location-drift. This is a disclosed, non-resolving placeholder pending the real GitHub owner/repo (no git remote is configured); closes when the real value is substituted and verified, routed to Phase 6's LEG-04 launch gate. | open |  | 2026-09-17T06:22:03.471Z |  |
| 12 | 04 | unrun-verify | README.md |  | DIST-06's prose-quality half (does the lead-in genuinely read as leading with examples, is the Install section clear to a first-time reader) is unverified by any check in this repository -- only the structural half (four anchors present, Before-and-after precedes Install and Status) is CI-enforced by readme-install-path-missing/readme-before-after-order. Provisional pending end-of-phase UAT per workflow.human_verify_mode: end-of-phase. | open |  | 2026-09-17T07:58:46.362Z |  |
| 13 | 04 | deviation | README.md |  | 04-04-PLAN.md's own acceptance criteria and <verification> expect grep -cF 'evals/conformance/RESULTS-mod04.md' README.md to print 3, describing a third occurrence 'in the layout tree at line 104' pre-rewrite. Direct inspection (both live and via git show HEAD before this plan) confirms the pre-rewrite count was 2: the tree only ever contained the bare filename 'RESULTS-mod04.md' nested under 'conformance/', never the literal concatenated path string. The guarded literal is preserved byte-identical at its original 2 occurrences (readme-results-pointer-missing passes); no third occurrence was fabricated to force the miscounted script to pass, matching the 03-04/04-01/04-03 precedent for documenting plan-authored verification-script errors rather than force-fitting shipped content to them. | open |  | 2026-09-17T07:58:46.489Z |  |
| 14 | 04 | deviation | tools/check_repo.py |  | 04-07-PLAN.md's own interfaces block stated 12 word-spelled cardinals measured in examples/deal-brief.md's prose and 3 such occurrences in skills/proof-first/references/worked-examples.md. Direct measurement with the exact SPELLED_CARDINAL_RE the shipped code uses (\\b(two\|three\|four\|five\|six\|seven\|eight\|nine\|ten\|eleven\|twelve)\\b, case-insensitive) found 13 and 5 respectively. The shipped before-after-spelled-count docstring states the corrected figures (13, 5), not the plan's stated ones, matching the 03-04/04-01/04-04/04-04(id-13) precedent of documenting plan-authored measurement errors rather than force-fitting shipped content to them. No behavior or scope decision changes -- both files remain out of this code's scan (BEFORE_AFTER_PATH only). | open |  | 2026-09-17T09:56:36.048Z |  |
| 15 | 04 | deviation | tools/generate_derivatives.py |  | 04-10-PLAN.md's own import-set verify probe (regex `^\\\\s*(?:import\|from)\\\\s+...`) matches the module docstring's prose line 'from the Python standard library;' (pre-existing text, unedited by this plan) in addition to the five real import statements, printing ['argparse','hashlib','pathlib','re','sys','the'] instead of the five-element list the acceptance criterion names. Direct inspection confirms the real import set (grep '^import \\\\\|^from ' restricted to the five actual statement lines at the file's end) is exactly argparse/hashlib/pathlib/re/sys, unchanged by this plan. Matching the 03-04/04-01/04-03/04-04/WINDOWS-13 precedent for documenting a plan-authored verify-script false positive rather than rewording shipped docstring prose to dodge it. | open |  | 2026-09-17T10:46:40.096Z |  |
| 16 | 04 | unrun-verify | README.md |  | README's output-style route now states the copy step (mkdir -p ~/.claude/output-styles, cp output-styles/proof-first.md ~/.claude/output-styles/) and its destination directory; readme-output-style-destination-missing mechanically enforces that at least one destination directory is named. What remains unobserved is the last link in the chain: a live Claude Code session listing the copied style in /config and applying it — this repository's live sessions are headless claude -p runs (evals/conformance/run_conformance.py), which have no /config picker to observe. The two destination paths (~/.claude/output-styles/ and a project's .claude/output-styles/) are recorded from 04-UAT.md test 4's orchestrator-verified finding, not from a documentation source this environment can fetch. Closure condition: a human runs the stated copy on a real machine and confirms the style appears in /config, routed alongside entries 11 and 12 to Phase 6's LEG-04 launch gate. | open |  | 2026-09-18T06:45:50.382Z |  |
| 17 | 04 | unrun-verify | README.md |  | No code in this repository compares two factual assertions in the same document for consistency. Measured evidence: three consecutive rounds (G-04-3, G-04-4, G-04-8) where check_repo.py reported 0 violations while a cold human read found a false sentence on first pass -- the class is invisible to every existing check, not just the ones that fired green here. This is a decision, not an oversight: the defect is entailment between two independently-phrased passages, which pattern matching over one file at a time cannot perform; a blocklist of the exact removed phrasings would prove only that those specific sentences did not come back; and a broad negative-existential regex over README prose would be a fuzzy-proxy hard-fail gate on every future legitimate disclosure sentence. A narrow presence code (require README.md to name the headless mechanism) was measured and would be red-then-green across this plan, meeting the repository's own evidence bar, but is still refused: unlike 04-13's readme-output-style-destination-missing, whose string has independent reader value (a route missing its destination directory is unexecutable), this token's only function would be to gesture at this specific correction and cannot distinguish a correctly scoped disclosure from an over-broad one that happens to mention the mechanism elsewhere on the page. Recorded in tools/check_repo.py's module docstring alongside the existing paraphrase-judgement limit. Closure condition: a cold human read each round, routed to end-of-phase UAT rather than to CI -- the same method that caught all three instances of this defect class. | open |  | 2026-09-18T07:42:37.964Z |  |
| 18 | 05 | unrun-verify | evals/benchmark/bench-deal-brief.md |  | Name-collision web search for bench-deal-brief.md's invented company/people names could not be run in this environment (no live network access), mirroring Phase 1's disclosed unrun-verify posture for examples/deal-brief.md. | open |  | 2026-09-18T09:36:23.879Z |  |
| 19 | 05 | unrun-verify | evals/benchmark/scenarios.json |  | Whether the eight scenario prompts are realistic presales tasks a bid team would actually receive (vs. shaped to favor one condition) is a verification:backstop truth per 05-02-PLAN.md, not mechanically checked. | open |  | 2026-09-18T09:36:24.007Z |  |

````json
[
  {
    "id": 1,
    "kind": "unrun-verify",
    "phase": "01",
    "file": "examples/deal-brief.md",
    "line": null,
    "description": "T-01-04 name-collision web search for 4 invented parties + 5 invented persons not run (no live network access in this environment) — human must confirm via web search before repo goes public",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-10T06:46:57.541Z",
    "resolved_at": "2026-09-10T11:02:49.274Z"
  },
  {
    "id": 2,
    "kind": "unrun-verify",
    "phase": "01",
    "file": "examples/deal-brief.md",
    "line": null,
    "description": "D-07/P-05 boundary check (no sentence compares two real products or companies) reviewed by executor via re-read, not confirmed by an independent human reviewer as the plan's <manual> verify step specifies",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-10T06:46:57.653Z",
    "resolved_at": "2026-09-10T11:02:55.089Z"
  },
  {
    "id": 3,
    "kind": "unrun-verify",
    "phase": "02",
    "file": "skills/proof-first/SKILL.md",
    "line": null,
    "description": "Tracer feedback human-check (02-01 Task 1): SOURCES.md reproduction-boundary read plus PF-0.1/PF-3.1 framing judgment (CAT-03/CAT-04 flagged assumptions A-03/A-04) - signed off at end-of-phase UAT 2026-09-11 (02-UAT.md test 1, result pass); stays open because the formal reproduction-boundary gate is Phase 6 LEG-04",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-11T00:38:23.292Z",
    "resolved_at": null
  },
  {
    "id": 4,
    "kind": "unrun-verify",
    "phase": "02",
    "file": "evals/pressure-tests.md",
    "line": null,
    "description": "D-31 trigger pressure-test: must-fire/must-not-fire phrasings recorded with method only — this environment cannot drive a fresh harness session to install the skill and observe activation, so every Observed cell reads 'not yet observed'; a human must run each phrasing in a real harness session and fill in Observed/Date/Harness before this is fixed",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-11T01:22:59.066Z",
    "resolved_at": null
  },
  {
    "id": 5,
    "kind": "unmet-truth",
    "phase": "02",
    "file": "skills/proof-first/SKILL.md",
    "line": null,
    "description": "CAT-08 token half: skill-token-budget-exceeded fires against the real SKILL.md (estimated 6207 tokens, words x 1.3, against the 5000-token ceiling) -- content-volume finding, not a formatting artifact (368 lines, well under the line ceiling). Needs catalog trimming or content restructuring in a future plan; do not resolve by re-wrapping or raising the ceiling.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-11T01:48:55.000Z",
    "resolved_at": "2026-09-11T04:32:38.278Z"
  },
  {
    "id": 6,
    "kind": "unrun-verify",
    "phase": "03",
    "file": "skills/proof-first/references/completeness-audit.md",
    "line": null,
    "description": "The eight MC dimension names (Metric, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Pain, Champion, Competition) and their MC-1 through MC-40 ID-range order were frozen in NUMBERING.md and .planning/REQUIREMENTS.md before Phase 3 began, and that order matches the MEDDICC acronym's own canonical sequence. SOURCES.md states that a source's own ordered list reproduced in its order is reproduction, not paraphrase, and that no tool in this stack performs that judgment. Phase 3 used content levers only: every dimension's audit question is written in this repository's own words, grounded entirely in examples/deal-brief.md's facts, and Phase 3 deliberately did not reorder or rename any dimension. The paraphrase-boundary judgment on the inherited ID-range order itself is routed to Phase 6's LEG-04 gate, which is this entry's closure condition.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-14T08:17:27.877Z",
    "resolved_at": null
  },
  {
    "id": 7,
    "kind": "unmet-truth",
    "phase": "03",
    "file": "skills/proof-first/references/completeness-audit.md",
    "line": null,
    "description": "03-05's single standalone-audit re-check (docs/B-proposal-section.md) printed an unrequested ## Artifact family section before ## Completeness gaps, diverging from 'Running the audit on its own's stated shape ('returns...and nothing more') and from 03-UAT.md test 1's 6/6 clean result. One-sample variance, not reproduced across multiple runs; AUD-03 was still marked Complete in this plan on the strength of the 6/6 Phase 3 UAT evidence, but this single later sample is recorded so it isn't silently lost.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-14T12:38:38.005Z",
    "resolved_at": "2026-09-15T03:04:40.278Z"
  },
  {
    "id": 8,
    "kind": "unmet-truth",
    "phase": "03",
    "file": "skills/proof-first/SKILL.md",
    "line": null,
    "description": "MOD-04 anchored remeasurement (03-12), the first measurement of this residual produced entirely under 03-09's anchored scorer (FAMILY_LINE_WINDOW_CHARS=400) rather than the unbounded pre-fix search -- every figure below is a precise measurement, not an optimistic ceiling. Prior figures retained for the record: 03-05's unanchored UAT recipe measured 5/6 then 14/16; 03-08's same-instrument unanchored measurement of 03-07's levers measured 16/20 (both models) with a 5/11 sonnet-5-only paired baseline (6/10 vs 5/11 same-model, 45.5%->60.0%). None of those four are directly comparable to this round's figures (different scorer, or different recipe entirely). This round: Arm A -- post-03-11 skill (blob fadc48613f71fb29d55b42f70805225f9087a2b9), the ordering-gate lever under test -- scored 3 of 10 scoreable claude-sonnet-5 sessions conformant (30.0%). Arm B -- the paired same-instrument baseline, pre-03-11 skill materialised from commit c7c1df45e5042636565747f31d4eb5c38513dbac (blob 9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a) -- scored 4 of 10 (40.0%). The delta (N_A/M_A - N_B/M_B = -10.0 percentage points) is below the pre-committed rule's 0.10 improvement threshold, selecting Branch 4: the honest finding is a decline, not merely flat movement, though at n=10 per arm this is within plausible sampling noise for a true rate difference of zero. Every non-conformant session this round scored no-family (no family phrase within the anchored 400-character window at all); zero sessions scored rule-before-family, a different residual shape from every earlier, unanchored measurement of this entry. Three levers have now each been measured and none reached the 87.5% closure bar: 03-05's restatement, 03-07's five-value family line plus presence gate, and 03-11's self-check ordering re-scan. This residual is accepted and disclosed as a known, measured limitation -- not hidden, and not claimed satisfied. Full run-by-run evidence, exclusions, and the reproduction command: evals/conformance/RESULTS-mod04.md, section '## Anchored remeasurement result (03-12)'.",
    "status": "waived",
    "reason": "Anchored remeasurement (03-12): Arm A (post-03-11, ordering-gate lever) 3/10 (30.0%) conformant vs. Arm B (pre-03-11, paired same-instrument baseline) 4/10 (40.0%) -- a -10.0 percentage-point delta, selecting the pre-committed rule's Branch 4 (delta < 0.10). Three levers now measured (03-05 restatement, 03-07 family line plus presence gate, 03-11 ordering re-scan) and none reached the 87.5% bar. This is the first anchored (non-optimistic-ceiling) MOD-04 measurement; the residual is accepted and disclosed, not satisfied. Full evidence: evals/conformance/RESULTS-mod04.md, section Anchored remeasurement result (03-12). Explicit v1 disposition decided 2026-09-16 by the project owner (human, in an interactive /gsd-execute-phase 03 --gaps-only session, not the executing agent on the project's behalf): Option A, accept and disclose. See evals/conformance/RESULTS-mod04.md, section '## v1 disposition decision (03-15)'.",
    "recorded_at": "2026-09-15T01:50:32.188Z",
    "resolved_at": "2026-09-16T09:15:30.640Z"
  },
  {
    "id": 9,
    "kind": "unmet-truth",
    "phase": "03",
    "file": "skills/proof-first/references/artifact-patterns.md",
    "line": null,
    "description": "Residual source label outside 03-05's scope: artifact-patterns.md line 103 still reads 'Diane Osoria, the economic buyer'. Plan 03-05 scoped the G-03-5 fix to the six affected MC bodies in completeness-audit.md, so this one occurrence in the Executive summary family section was not covered and is the last remaining instance of a frozen NUMBERING.md registry label used as this repository's own unattributed noun in shipped skill content. One-word fix ('the person who signs'); left unmade rather than silently widening a verified plan's scope. Closure: fold into the next content plan or into Phase 6 LEG-04 alongside entries 3 and 6.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-15T01:50:41.248Z",
    "resolved_at": "2026-09-15T03:04:40.161Z"
  },
  {
    "id": 10,
    "kind": "unmet-truth",
    "phase": "03",
    "file": "evals/conformance/run_conformance.py",
    "line": null,
    "description": "Self-test behavior case 11 in evals/conformance/run_conformance.py, added by 03-13 to prove that _write_result_line()'s flush call makes each scored session durable against a process interruption, did not discriminate the flush call's presence from its absence, because the interrupting exception was caught inside the same block whose own close-on-exit flushed the file regardless. A future silent deletion of that one line would have reintroduced the exact data-loss bug that has already destroyed two real measurement runs, shipping with a green self-test and a green CI -- the failure mode this repository's own mutation-testing preamble exists to prevent. Two independent reproductions: 03-REVIEW.md's round-5 CR-01 and 03-VERIFICATION.md's verifier, each by copying the script to a sibling path inside evals/conformance/, removing the flush call and observing a clean self-test PASS. The fix: 03-16 rewrote case 11 to assert the recorded write-then-flush call sequence through a proxy handle and to read the results file before the underlying handle is closed, proven in both directions by a one-time mutation probe. The residual and its route: run_conformance.py still ships no committed mutation harness of its own, unlike tools/check_repo.py --mutation-test, so this discrimination is proven once rather than continuously; that narrower guarantee is disclosed in the module docstring, in RESULTS-mod04.md's Self-test discrimination correction (03-16) section and here, and is routed to Phase 5's eval-harness work rather than claimed closed.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-17T04:10:16.975Z",
    "resolved_at": "2026-09-17T04:10:23.158Z"
  },
  {
    "id": 11,
    "kind": "unrun-verify",
    "phase": "04",
    "file": ".claude-plugin/plugin.json",
    "line": null,
    "description": "Publish location frozen as the placeholder <owner>/<repo> (P4-03): .claude-plugin/plugin.json's homepage/repository, .claude-plugin/marketplace.json's homepage/repository/owner.url all state https://github.com/<owner>/<repo> or https://github.com/<owner>, enforced consistent by publish-location-drift. This is a disclosed, non-resolving placeholder pending the real GitHub owner/repo (no git remote is configured); closes when the real value is substituted and verified, routed to Phase 6's LEG-04 launch gate.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-17T06:22:03.471Z",
    "resolved_at": null
  },
  {
    "id": 12,
    "kind": "unrun-verify",
    "phase": "04",
    "file": "README.md",
    "line": null,
    "description": "DIST-06's prose-quality half (does the lead-in genuinely read as leading with examples, is the Install section clear to a first-time reader) is unverified by any check in this repository -- only the structural half (four anchors present, Before-and-after precedes Install and Status) is CI-enforced by readme-install-path-missing/readme-before-after-order. Provisional pending end-of-phase UAT per workflow.human_verify_mode: end-of-phase.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-17T07:58:46.362Z",
    "resolved_at": null
  },
  {
    "id": 13,
    "kind": "deviation",
    "phase": "04",
    "file": "README.md",
    "line": null,
    "description": "04-04-PLAN.md's own acceptance criteria and <verification> expect grep -cF 'evals/conformance/RESULTS-mod04.md' README.md to print 3, describing a third occurrence 'in the layout tree at line 104' pre-rewrite. Direct inspection (both live and via git show HEAD before this plan) confirms the pre-rewrite count was 2: the tree only ever contained the bare filename 'RESULTS-mod04.md' nested under 'conformance/', never the literal concatenated path string. The guarded literal is preserved byte-identical at its original 2 occurrences (readme-results-pointer-missing passes); no third occurrence was fabricated to force the miscounted script to pass, matching the 03-04/04-01/04-03 precedent for documenting plan-authored verification-script errors rather than force-fitting shipped content to them.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-17T07:58:46.489Z",
    "resolved_at": null
  },
  {
    "id": 14,
    "kind": "deviation",
    "phase": "04",
    "file": "tools/check_repo.py",
    "line": null,
    "description": "04-07-PLAN.md's own interfaces block stated 12 word-spelled cardinals measured in examples/deal-brief.md's prose and 3 such occurrences in skills/proof-first/references/worked-examples.md. Direct measurement with the exact SPELLED_CARDINAL_RE the shipped code uses (\\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\\b, case-insensitive) found 13 and 5 respectively. The shipped before-after-spelled-count docstring states the corrected figures (13, 5), not the plan's stated ones, matching the 03-04/04-01/04-04/04-04(id-13) precedent of documenting plan-authored measurement errors rather than force-fitting shipped content to them. No behavior or scope decision changes -- both files remain out of this code's scan (BEFORE_AFTER_PATH only).",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-17T09:56:36.048Z",
    "resolved_at": null
  },
  {
    "id": 15,
    "kind": "deviation",
    "phase": "04",
    "file": "tools/generate_derivatives.py",
    "line": null,
    "description": "04-10-PLAN.md's own import-set verify probe (regex `^\\\\s*(?:import|from)\\\\s+...`) matches the module docstring's prose line 'from the Python standard library;' (pre-existing text, unedited by this plan) in addition to the five real import statements, printing ['argparse','hashlib','pathlib','re','sys','the'] instead of the five-element list the acceptance criterion names. Direct inspection confirms the real import set (grep '^import \\\\|^from ' restricted to the five actual statement lines at the file's end) is exactly argparse/hashlib/pathlib/re/sys, unchanged by this plan. Matching the 03-04/04-01/04-03/04-04/WINDOWS-13 precedent for documenting a plan-authored verify-script false positive rather than rewording shipped docstring prose to dodge it.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-17T10:46:40.096Z",
    "resolved_at": null
  },
  {
    "id": 16,
    "kind": "unrun-verify",
    "phase": "04",
    "file": "README.md",
    "line": null,
    "description": "README's output-style route now states the copy step (mkdir -p ~/.claude/output-styles, cp output-styles/proof-first.md ~/.claude/output-styles/) and its destination directory; readme-output-style-destination-missing mechanically enforces that at least one destination directory is named. What remains unobserved is the last link in the chain: a live Claude Code session listing the copied style in /config and applying it — this repository's live sessions are headless claude -p runs (evals/conformance/run_conformance.py), which have no /config picker to observe. The two destination paths (~/.claude/output-styles/ and a project's .claude/output-styles/) are recorded from 04-UAT.md test 4's orchestrator-verified finding, not from a documentation source this environment can fetch. Closure condition: a human runs the stated copy on a real machine and confirms the style appears in /config, routed alongside entries 11 and 12 to Phase 6's LEG-04 launch gate.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-18T06:45:50.382Z",
    "resolved_at": null
  },
  {
    "id": 17,
    "kind": "unrun-verify",
    "phase": "04",
    "file": "README.md",
    "line": null,
    "description": "No code in this repository compares two factual assertions in the same document for consistency. Measured evidence: three consecutive rounds (G-04-3, G-04-4, G-04-8) where check_repo.py reported 0 violations while a cold human read found a false sentence on first pass -- the class is invisible to every existing check, not just the ones that fired green here. This is a decision, not an oversight: the defect is entailment between two independently-phrased passages, which pattern matching over one file at a time cannot perform; a blocklist of the exact removed phrasings would prove only that those specific sentences did not come back; and a broad negative-existential regex over README prose would be a fuzzy-proxy hard-fail gate on every future legitimate disclosure sentence. A narrow presence code (require README.md to name the headless mechanism) was measured and would be red-then-green across this plan, meeting the repository's own evidence bar, but is still refused: unlike 04-13's readme-output-style-destination-missing, whose string has independent reader value (a route missing its destination directory is unexecutable), this token's only function would be to gesture at this specific correction and cannot distinguish a correctly scoped disclosure from an over-broad one that happens to mention the mechanism elsewhere on the page. Recorded in tools/check_repo.py's module docstring alongside the existing paraphrase-judgement limit. Closure condition: a cold human read each round, routed to end-of-phase UAT rather than to CI -- the same method that caught all three instances of this defect class.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-18T07:42:37.964Z",
    "resolved_at": null
  },
  {
    "id": 18,
    "kind": "unrun-verify",
    "phase": "05",
    "file": "evals/benchmark/bench-deal-brief.md",
    "line": null,
    "description": "Name-collision web search for bench-deal-brief.md's invented company/people names could not be run in this environment (no live network access), mirroring Phase 1's disclosed unrun-verify posture for examples/deal-brief.md.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-18T09:36:23.879Z",
    "resolved_at": null
  },
  {
    "id": 19,
    "kind": "unrun-verify",
    "phase": "05",
    "file": "evals/benchmark/scenarios.json",
    "line": null,
    "description": "Whether the eight scenario prompts are realistic presales tasks a bid team would actually receive (vs. shaped to favor one condition) is a verification:backstop truth per 05-02-PLAN.md, not mechanically checked.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-18T09:36:24.007Z",
    "resolved_at": null
  }
]
````
