---
schema_version: 1
open_count: 8
waived_count: 9
fixed_count: 11
total_count: 28
last_updated: 2026-09-21T10:14:38.246Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 01 | unrun-verify | examples/deal-brief.md |  | T-01-04 name-collision web search for 4 invented parties + 5 invented persons not run (no live network access in this environment) — human must confirm via web search before repo goes public | fixed |  | 2026-09-10T06:46:57.541Z | 2026-09-10T11:02:49.274Z |
| 2 | 01 | unrun-verify | examples/deal-brief.md |  | D-07/P-05 boundary check (no sentence compares two real products or companies) reviewed by executor via re-read, not confirmed by an independent human reviewer as the plan's <manual> verify step specifies | fixed |  | 2026-09-10T06:46:57.653Z | 2026-09-10T11:02:55.089Z |
| 3 | 02 | unrun-verify | skills/proof-first/SKILL.md |  | Tracer feedback human-check (02-01 Task 1): SOURCES.md reproduction-boundary read plus PF-0.1/PF-3.1 framing judgment (CAT-03/CAT-04 flagged assumptions A-03/A-04) - signed off at end-of-phase UAT 2026-09-11 (02-UAT.md test 1, result pass); stays open because the formal reproduction-boundary gate is Phase 6 LEG-04 | fixed |  | 2026-09-11T00:38:23.292Z | 2026-09-21T10:14:36.928Z |
| 4 | 02 | unrun-verify | evals/pressure-tests.md |  | D-31 trigger pressure-test: must-fire/must-not-fire phrasings recorded with method only — this environment cannot drive a fresh harness session to install the skill and observe activation, so every Observed cell reads 'not yet observed'; a human must run each phrasing in a real harness session and fill in Observed/Date/Harness before this is fixed | fixed |  | 2026-09-11T01:22:59.066Z | 2026-09-20T02:20:51.557Z |
| 5 | 02 | unmet-truth | skills/proof-first/SKILL.md |  | CAT-08 token half: skill-token-budget-exceeded fires against the real SKILL.md (estimated 6207 tokens, words x 1.3, against the 5000-token ceiling) -- content-volume finding, not a formatting artifact (368 lines, well under the line ceiling). Needs catalog trimming or content restructuring in a future plan; do not resolve by re-wrapping or raising the ceiling. | fixed |  | 2026-09-11T01:48:55.000Z | 2026-09-11T04:32:38.278Z |
| 6 | 03 | unrun-verify | skills/proof-first/references/completeness-audit.md |  | The eight MC dimension names (Metric, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Pain, Champion, Competition) and their MC-1 through MC-40 ID-range order were frozen in NUMBERING.md and .planning/REQUIREMENTS.md before Phase 3 began, and that order matches the MEDDICC acronym's own canonical sequence. SOURCES.md states that a source's own ordered list reproduced in its order is reproduction, not paraphrase, and that no tool in this stack performs that judgment. Phase 3 used content levers only: every dimension's audit question is written in this repository's own words, grounded entirely in examples/deal-brief.md's facts, and Phase 3 deliberately did not reorder or rename any dimension. The paraphrase-boundary judgment on the inherited ID-range order itself is routed to Phase 6's LEG-04 gate, which is this entry's closure condition. | fixed |  | 2026-09-14T08:17:27.877Z | 2026-09-21T10:14:37.056Z |
| 7 | 03 | unmet-truth | skills/proof-first/references/completeness-audit.md |  | 03-05's single standalone-audit re-check (docs/B-proposal-section.md) printed an unrequested ## Artifact family section before ## Completeness gaps, diverging from 'Running the audit on its own's stated shape ('returns...and nothing more') and from 03-UAT.md test 1's 6/6 clean result. One-sample variance, not reproduced across multiple runs; AUD-03 was still marked Complete in this plan on the strength of the 6/6 Phase 3 UAT evidence, but this single later sample is recorded so it isn't silently lost. | fixed |  | 2026-09-14T12:38:38.005Z | 2026-09-15T03:04:40.278Z |
| 8 | 03 | unmet-truth | skills/proof-first/SKILL.md |  | MOD-04 anchored remeasurement (03-12), the first measurement of this residual produced entirely under 03-09's anchored scorer (FAMILY_LINE_WINDOW_CHARS=400) rather than the unbounded pre-fix search -- every figure below is a precise measurement, not an optimistic ceiling. Prior figures retained for the record: 03-05's unanchored UAT recipe measured 5/6 then 14/16; 03-08's same-instrument unanchored measurement of 03-07's levers measured 16/20 (both models) with a 5/11 sonnet-5-only paired baseline (6/10 vs 5/11 same-model, 45.5%->60.0%). None of those four are directly comparable to this round's figures (different scorer, or different recipe entirely). This round: Arm A -- post-03-11 skill (blob fadc48613f71fb29d55b42f70805225f9087a2b9), the ordering-gate lever under test -- scored 3 of 10 scoreable claude-sonnet-5 sessions conformant (30.0%). Arm B -- the paired same-instrument baseline, pre-03-11 skill materialised from commit c7c1df45e5042636565747f31d4eb5c38513dbac (blob 9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a) -- scored 4 of 10 (40.0%). The delta (N_A/M_A - N_B/M_B = -10.0 percentage points) is below the pre-committed rule's 0.10 improvement threshold, selecting Branch 4: the honest finding is a decline, not merely flat movement, though at n=10 per arm this is within plausible sampling noise for a true rate difference of zero. Every non-conformant session this round scored no-family (no family phrase within the anchored 400-character window at all); zero sessions scored rule-before-family, a different residual shape from every earlier, unanchored measurement of this entry. Three levers have now each been measured and none reached the 87.5% closure bar: 03-05's restatement, 03-07's five-value family line plus presence gate, and 03-11's self-check ordering re-scan. This residual is accepted and disclosed as a known, measured limitation -- not hidden, and not claimed satisfied. Full run-by-run evidence, exclusions, and the reproduction command: evals/conformance/RESULTS-mod04.md, section '## Anchored remeasurement result (03-12)'. | waived | Anchored remeasurement (03-12): Arm A (post-03-11, ordering-gate lever) 3/10 (30.0%) conformant vs. Arm B (pre-03-11, paired same-instrument baseline) 4/10 (40.0%) -- a -10.0 percentage-point delta, selecting the pre-committed rule's Branch 4 (delta < 0.10). Three levers now measured (03-05 restatement, 03-07 family line plus presence gate, 03-11 ordering re-scan) and none reached the 87.5% bar. This is the first anchored (non-optimistic-ceiling) MOD-04 measurement; the residual is accepted and disclosed, not satisfied. Full evidence: evals/conformance/RESULTS-mod04.md, section Anchored remeasurement result (03-12). Explicit v1 disposition decided 2026-09-16 by the project owner (human, in an interactive /gsd-execute-phase 03 --gaps-only session, not the executing agent on the project's behalf): Option A, accept and disclose. See evals/conformance/RESULTS-mod04.md, section '## v1 disposition decision (03-15)'. | 2026-09-15T01:50:32.188Z | 2026-09-16T09:15:30.640Z |
| 9 | 03 | unmet-truth | skills/proof-first/references/artifact-patterns.md |  | Residual source label outside 03-05's scope: artifact-patterns.md line 103 still reads 'Diane Osoria, the economic buyer'. Plan 03-05 scoped the G-03-5 fix to the six affected MC bodies in completeness-audit.md, so this one occurrence in the Executive summary family section was not covered and is the last remaining instance of a frozen NUMBERING.md registry label used as this repository's own unattributed noun in shipped skill content. One-word fix ('the person who signs'); left unmade rather than silently widening a verified plan's scope. Closure: fold into the next content plan or into Phase 6 LEG-04 alongside entries 3 and 6. | fixed |  | 2026-09-15T01:50:41.248Z | 2026-09-15T03:04:40.161Z |
| 10 | 03 | unmet-truth | evals/conformance/run_conformance.py |  | Self-test behavior case 11 in evals/conformance/run_conformance.py, added by 03-13 to prove that _write_result_line()'s flush call makes each scored session durable against a process interruption, did not discriminate the flush call's presence from its absence, because the interrupting exception was caught inside the same block whose own close-on-exit flushed the file regardless. A future silent deletion of that one line would have reintroduced the exact data-loss bug that has already destroyed two real measurement runs, shipping with a green self-test and a green CI -- the failure mode this repository's own mutation-testing preamble exists to prevent. Two independent reproductions: 03-REVIEW.md's round-5 CR-01 and 03-VERIFICATION.md's verifier, each by copying the script to a sibling path inside evals/conformance/, removing the flush call and observing a clean self-test PASS. The fix: 03-16 rewrote case 11 to assert the recorded write-then-flush call sequence through a proxy handle and to read the results file before the underlying handle is closed, proven in both directions by a one-time mutation probe. The residual and its route: run_conformance.py still ships no committed mutation harness of its own, unlike tools/check_repo.py --mutation-test, so this discrimination is proven once rather than continuously; that narrower guarantee is disclosed in the module docstring, in RESULTS-mod04.md's Self-test discrimination correction (03-16) section and here, and is routed to Phase 5's eval-harness work rather than claimed closed. | fixed |  | 2026-09-17T04:10:16.975Z | 2026-09-17T04:10:23.158Z |
| 11 | 04 | unrun-verify | .claude-plugin/plugin.json |  | Publish location frozen as the placeholder <owner>/<repo> (P4-03): .claude-plugin/plugin.json's homepage/repository, .claude-plugin/marketplace.json's homepage/repository/owner.url all state https://github.com/<owner>/<repo> or https://github.com/<owner>, enforced consistent by publish-location-drift. This is a disclosed, non-resolving placeholder pending the real GitHub owner/repo (no git remote is configured); closes when the real value is substituted and verified, routed to Phase 6's LEG-04 launch gate. | open | Publication DEFERRED at the 06-04 launch checkpoint on 2026-09-21 by explicit operator decision, recorded in LEGAL-REVIEW.md's ## Launch section. No remote was created and no placeholder was substituted; all four occurrences still read <owner>/<repo> and still agree with each other, so publish-location-drift stays silent. Owner: the operator. Closes when a real owner/repo is substituted in all four guarded locations AND at least one install route is observed resolving against it — substitution alone does not close this entry, because publish-location-drift proves the four agree and can never prove they resolve. | 2026-09-17T06:22:03.471Z |  |
| 12 | 04 | unrun-verify | README.md |  | DIST-06's prose-quality half (does the lead-in genuinely read as leading with examples, is the Install section clear to a first-time reader) is unverified by any check in this repository -- only the structural half (four anchors present, Before-and-after precedes Install and Status) is CI-enforced by readme-install-path-missing/readme-before-after-order. Provisional pending end-of-phase UAT per workflow.human_verify_mode: end-of-phase. | open | Cold read PERFORMED 2026-09-21 by /gsd-verify-work 06 -- the 'no reader available' premise is cleared and must not be reused. Two independent headless readers, neither of which wrote the text, read README in a scratch directory on a neutral brief. On the specific question this entry carried (does the new claim region read as an honest report of a mixed result or a defensive one): PASS -- the reader's verdict was 'honest report of a mixed result, not a burial, and not close to one', noting the loss is pre-announced at :163, stated subject-verb-number at :181, given MORE sentence-level prominence than the two wins, and has its cheapest excuse foreclosed at :183. The entry stays OPEN on a different finding: the same readers surfaced three checkably-false README statements, recorded as gap G-06-6 in 06-UAT.md and planned in 06-05-PLAN.md. Closes when those three are corrected. | 2026-09-17T07:58:46.362Z |  |
| 13 | 04 | deviation | README.md |  | 04-04-PLAN.md's own acceptance criteria and <verification> expect grep -cF 'evals/conformance/RESULTS-mod04.md' README.md to print 3, describing a third occurrence 'in the layout tree at line 104' pre-rewrite. Direct inspection (both live and via git show HEAD before this plan) confirms the pre-rewrite count was 2: the tree only ever contained the bare filename 'RESULTS-mod04.md' nested under 'conformance/', never the literal concatenated path string. The guarded literal is preserved byte-identical at its original 2 occurrences (readme-results-pointer-missing passes); no third occurrence was fabricated to force the miscounted script to pass, matching the 03-04/04-01/04-03 precedent for documenting plan-authored verification-script errors rather than force-fitting shipped content to them. | waived | Plan-authored verify-script error, not a content defect: 04-04-PLAN.md expected 3 occurrences of the results-pointer path in README.md and described a third 'in the layout tree at line 104'. Direct inspection of the pre-rewrite file, live and via git show, confirms that third occurrence never existed; the shipped README carries the pointer the count needs and readme-results-pointer-missing enforces it. Nothing in shipped content is wrong, so there is nothing to fix. | 2026-09-17T07:58:46.489Z | 2026-09-21T10:14:37.421Z |
| 14 | 04 | deviation | tools/check_repo.py |  | 04-07-PLAN.md's own interfaces block stated 12 word-spelled cardinals measured in examples/deal-brief.md's prose and 3 such occurrences in skills/proof-first/references/worked-examples.md. Direct measurement with the exact SPELLED_CARDINAL_RE the shipped code uses (\b(two\|three\|four\|five\|six\|seven\|eight\|nine\|ten\|eleven\|twelve)\b, case-insensitive) found 13 and 5 respectively. The shipped before-after-spelled-count docstring states the corrected figures (13, 5), not the plan's stated ones, matching the 03-04/04-01/04-04/04-04(id-13) precedent of documenting plan-authored measurement errors rather than force-fitting shipped content to them. No behavior or scope decision changes -- both files remain out of this code's scan (BEFORE_AFTER_PATH only). | waived | Plan-authored measurement error, not a content defect: 04-07-PLAN.md's interfaces block stated 12 word-spelled cardinals in examples/deal-brief.md and 3 in worked-examples.md. Measuring with the exact SPELLED_CARDINAL_RE the shipped code uses returns different figures, and the shipped docstring already states the corrected ones. before-after-spelled-count is discrimination-proven against the real file. | 2026-09-17T09:56:36.048Z | 2026-09-21T10:14:37.540Z |
| 15 | 04 | deviation | tools/generate_derivatives.py |  | 04-10-PLAN.md's own import-set verify probe (regex `^\\s*(?:import\|from)\\s+...`) matches the module docstring's prose line 'from the Python standard library;' (pre-existing text, unedited by this plan) in addition to the five real import statements, printing ['argparse','hashlib','pathlib','re','sys','the'] instead of the five-element list the acceptance criterion names. Direct inspection confirms the real import set (grep '^import \\\|^from ' restricted to the five actual statement lines at the file's end) is exactly argparse/hashlib/pathlib/re/sys, unchanged by this plan. Matching the 03-04/04-01/04-03/04-04/WINDOWS-13 precedent for documenting a plan-authored verify-script false positive rather than rewording shipped docstring prose to dodge it. | waived | Plan-authored probe error, not a content defect: 04-10-PLAN.md's import-set probe regex also matched the prose phrase 'from the Python standard library;' in the module docstring, inflating the import set by one. The real import set is the five statements the probe otherwise found, and tools/generate_derivatives.py imports only stdlib modules — re-asserted this phase by the AST-based stdlib check, which reads ast.Import/ast.ImportFrom nodes rather than regex over text and reports EXTRA []. | 2026-09-17T10:46:40.096Z | 2026-09-21T10:14:37.657Z |
| 16 | 04 | unrun-verify | README.md |  | README's output-style route now states the copy step (mkdir -p ~/.claude/output-styles, cp output-styles/proof-first.md ~/.claude/output-styles/) and its destination directory; readme-output-style-destination-missing mechanically enforces that at least one destination directory is named. What remains unobserved is the last link in the chain: a live Claude Code session listing the copied style in /config and applying it — this repository's live sessions are headless claude -p runs (evals/conformance/run_conformance.py), which have no /config picker to observe. The two destination paths (~/.claude/output-styles/ and a project's .claude/output-styles/) are recorded from 04-UAT.md test 4's orchestrator-verified finding, not from a documentation source this environment can fetch. Closure condition: a human runs the stated copy on a real machine and confirms the style appears in /config, routed alongside entries 11 and 12 to Phase 6's LEG-04 launch gate. | open | UAT 2026-09-21 observed it. /gsd-verify-work 06 drove an interactive Claude Code 2.1.267 session in a pty on Darwin 25.6.0 and captured the rendered /config panel: the output-style picker lists `proof-first` as entry 7 with its description frontmatter rendered. Selecting it set the row to proof-first, the value survived closing and reopening /config, and it was written to disk as .claude/settings.local.json -> {"outputStyle": "proof-first"} -- so it outlives the session, which README:75-76 understates rather than overstates. Two controls: Esc without confirming left the row `default` and wrote nothing; a run that landed on Explanatory confirmed Explanatory. Caveat this entry turns on: the observation was made by automation reading a terminal, not by a human eye, on one platform, against a project-scoped .claude/output-styles/ rather than ~/.claude/output-styles/. The owner decides whether a captured render of the real picker meets a closure condition written as a human observation. | 2026-09-18T06:45:50.382Z |  |
| 17 | 04 | unrun-verify | README.md |  | No code in this repository compares two factual assertions in the same document for consistency. Measured evidence: three consecutive rounds (G-04-3, G-04-4, G-04-8) where check_repo.py reported 0 violations while a cold human read found a false sentence on first pass -- the class is invisible to every existing check, not just the ones that fired green here. This is a decision, not an oversight: the defect is entailment between two independently-phrased passages, which pattern matching over one file at a time cannot perform; a blocklist of the exact removed phrasings would prove only that those specific sentences did not come back; and a broad negative-existential regex over README prose would be a fuzzy-proxy hard-fail gate on every future legitimate disclosure sentence. A narrow presence code (require README.md to name the headless mechanism) was measured and would be red-then-green across this plan, meeting the repository's own evidence bar, but is still refused: unlike 04-13's readme-output-style-destination-missing, whose string has independent reader value (a route missing its destination directory is unexecutable), this token's only function would be to gesture at this specific correction and cannot distinguish a correctly scoped disclosure from an over-broad one that happens to mention the mechanism elsewhere on the page. Recorded in tools/check_repo.py's module docstring alongside the existing paraphrase-judgement limit. Closure condition: a cold human read each round, routed to end-of-phase UAT rather than to CI -- the same method that caught all three instances of this defect class. | open | Fourth consecutive round of the same pattern, now measured rather than asserted. 2026-09-21: all ten CI commands green (check_repo.py 0 violations, --mutation-test 56 codes discrimination-proven, seven self-tests rc=0) while two independent cold readers found three checkably-false README statements -- README:231-233's universal evidence-discipline claim, contradicted by tools/check_repo.py:405-415's own docstring; README:139-140's 'four install routes', contradicted by run_routes.py:2 and its ROUTES tuple; and README:131-133's superseded n=1 trigger figures, against RESULTS-trigger.md:166's Arm B n=5 measurement of the shipped description. The 06-04 self-read reached the third and dismissed it as Arm A, the reverted treatment -- the superseding figure is Arm B, the control that ships. That is this entry's thesis demonstrated, and it is the argument against a fuzzy-proxy gate, not for one. The proxy-gate refusal stands. Closes with G-06-6. | 2026-09-18T07:42:37.964Z |  |
| 18 | 05 | unrun-verify | evals/benchmark/bench-deal-brief.md |  | Name-collision web search for bench-deal-brief.md's invented company/people names could not be run in this environment (no live network access), mirroring Phase 1's disclosed unrun-verify posture for examples/deal-brief.md. | fixed |  | 2026-09-18T09:36:23.879Z | 2026-09-21T10:14:37.171Z |
| 19 | 05 | unrun-verify | evals/benchmark/scenarios.json |  | Whether the eight scenario prompts are realistic presales tasks a bid team would actually receive (vs. shaped to favor one condition) is a verification:backstop truth per 05-02-PLAN.md, not mechanically checked. | waived | Backstop truth, accepted with its reason stated: whether the eight scenario prompts in evals/benchmark/scenarios.json are realistic presales tasks is a judgement 05-02-PLAN.md classified verification:backstop, and no tool in this stack performs it. The scenarios are committed and readable, so a reader can judge them directly; the figures they produce are published with that limitation rather than behind it. | 2026-09-18T09:36:24.007Z | 2026-09-21T10:14:37.778Z |
| 20 | 05 | unmet-truth | evals/benchmark/run_benchmark.py |  | 05-REVIEW.md CR-02: aggregate()'s 'Judged persuasion' mean/range table pools individual per-order judgement records (n=6 per cell) instead of averaging each pair's two orders first, the way judge_summary()/average_orders() does for the win/tie/loss table. With a complete matrix (0 unscoreable, 0 excluded pairs) the published means are unaffected, which is why no committed figure is wrong today. But if one order of a pair were ever unscoreable, an un-paired, position-bias-uncorrected score would leak into the mean while RESULTS.md's own position-bias caveat still asserts orders are averaged before the report reads them. Non-blocking now, latent falsehood later. | open | Routed to v2. aggregate()'s 'Judged persuasion' mean/range table pools per-order judgement records instead of averaging each pair's two orders first, so those means are partly an artifact of judge position. NOT fixed here, by explicit decision: the fix changes the means that evals/benchmark/RESULTS.md already publishes, which makes it a figure-moving change rather than a cheap one, and 06-04's own rule routes a figure-moving fix to v2. 06-03 did not inherit the defect — pooled_summary() consumes judge_summary()'s paired output and a self-test fixture is constructed so the paired and per-order answers differ, so the pooled totals README quotes are provably on the paired path. Owner: v2 benchmark maintainer. Closes when aggregate() averages orders before pooling and RESULTS.md is re-rendered with the corrected means and a note saying they changed and why. | 2026-09-20T02:01:52.821Z |  |
| 21 | 05 | unmet-truth | evals/benchmark/run_benchmark.py |  | 05-REVIEW.md CR-03: raw-record filenames and aggregate()'s grouping key omit effort, judge_model and judge_effort. Re-running against a populated evals/benchmark/raw/ with a different --effort or --judge-model silently reuses stale-configuration records (skip-if-exists matches on the shorter key) with no diagnostic, and RESULTS.md never states which effort or judge model produced its numbers. The committed run is internally consistent (single effort, single judge model), so no published figure is wrong; the gap is that nothing prevents or discloses a mixed-configuration run. | open | Routed to v2. Raw-record filenames and aggregate()'s grouping key omit effort, judge_model and judge_effort, so re-running against a populated evals/benchmark/raw/ with a different --effort or --judge-model silently reuses stale-configuration records via skip-if-exists. No v1 requirement depends on a re-run at a different configuration, and the committed run is internally consistent at one configuration. Owner: v2 benchmark maintainer. Closes when the record key includes effort, judge_model and judge_effort, and a re-run at a changed configuration is observed writing new records rather than reusing old ones. | 2026-09-20T02:01:52.940Z |  |
| 22 | 05 | unmet-truth | evals/benchmark/run_benchmark.py |  | 05-REVIEW.md CR-04: a (model, scenario, condition) cell whose every generation attempt failed is silently absent from the 'Mechanical proxy counts' table, with no 'Unscoreable generations: N' line -- asymmetric with the judgement side, which does print 'Unscoreable judgements: N' and 'Excluded pairs: N'. The committed run has zero unscoreable generations so nothing is hidden today, but a future partial run could publish a table that silently covers fewer cells than it appears to. | open | Routed to v2. A (model, scenario, condition) cell whose every generation attempt failed is silently absent from the Mechanical proxy counts table, with no 'Unscoreable generations: N' line — asymmetric with the judgement side, which prints both 'Unscoreable judgements' and 'Excluded pairs'. The committed run has no such cell, so no published figure is affected today; the defect is that a future run could lose a cell without saying so. Owner: v2 benchmark maintainer. Closes when build_results_md() emits an unscoreable-generation count alongside the mechanical table, with a self-test fixture in which a wholly-failed cell is reported rather than dropped. | 2026-09-20T02:01:53.066Z |  |
| 23 | 05 | deviation | evals/benchmark/run_benchmark.py |  | 05-REVIEW.md W-02: DISALLOWED_TOOLS = ['Write','Edit','Bash','NotebookEdit'] omits WebSearch and WebFetch, so generations run with web access available. MEASURED, NOT HYPOTHETICAL: summing usage.server_tool_use across all 96 committed generation records gives web_search_requests=0 and web_fetch_requests=0, so the committed measurement is uncontaminated. Recorded as a hardening gap for any future run, not as a defect in the published numbers. | waived | Measured, not hypothetical: DISALLOWED_TOOLS omits WebSearch and WebFetch, so generations ran with web access nominally available. Summing usage.server_tool_use across all 96 committed generation records gives web_search_requests=0 and web_fetch_requests=0 — no generation used either tool, so no published figure is contaminated. The omission is real and the exposure it created was measured to be zero. | 2026-09-20T02:01:53.185Z | 2026-09-21T10:14:37.893Z |
| 24 | 02 | unmet-truth | skills/proof-first/SKILL.md |  | CAT-10 over-broad description. The 2026-09-20 n=1 observation (9/9 must-fire, 2/5 must-not-fire over-fires) was superseded by the CAT-10 gap-closure round's paired n=5 measurement (02-10-PLAN.md, evals/trigger/DECISION-RULE-cat10.md, evals/trigger/RESULTS-trigger.md): Arm B (control, unchanged 439-char description) measured OF_B/SN_B=9/25 over-fires and MH_B/SM_B=45/45 must-fire hits. Arm A (treatment, 551-char description with an appended exclusion clause) measured OF_A/SN_A=0/25 (every must-not-fire row clean) but MH_A/SM_A=40/45 -- the must-fire row 'We're putting together our bid response -- write the commercial section.' regressed from 5/5 to 0/5, a genuine must-fire regression the pre-committed decision rule's Branch 4 catches ahead of Branch 1's clean over-fire elimination (Fisher exact p_attr=0.0016 on the over-fire delta alone -- real, and still insufficient because it cost a legitimate must-fire request). The treatment was tested live and REVERTED; the shipped description is unchanged from the original 439-char text, still measuring 9/25 must-not-fire hits at n=5. This entry stays open: the exclusion-clause lever is now a tested and refuted first candidate, not an unfunded one -- the next lever (most likely H1's audience-clause removal, deliberately not bundled into this round) remains unattempted. | open | Routed to v2, with the next lever named. CAT-10's description is over-broad: the shipped 439-character text measures 9 of 25 must-not-fire over-fires at n=5. The first candidate lever — an appended exclusion clause, 551 characters — was tested live under the pre-committed decision rule and REFUTED, not merely untried: it eliminated every must-not-fire over-fire (Fisher exact p_attr=0.0016) but regressed a legitimate must-fire row from 5/5 to 0/5, selecting Branch 4, and it was reverted. The shipped description is unchanged. Owner: v2 skill maintainer. Closes when the next lever — most likely H1's audience-clause removal, deliberately not bundled into the 02-10 round — is measured under the same paired protocol and either kept or refuted on the record. | 2026-09-20T02:20:51.680Z |  |
| 25 | 05 | unmet-truth | README.md |  | Phase 5 closeout left README.md asserting its own benchmark 'has not run' and listing it under 'What does not exist yet', while evals/benchmark/RESULTS.md records a 2026-09-18 run of 96 generations across claude-opus-5 and claude-sonnet-5 with both-orders judge scoring. The false negative claims were corrected during Phase 2's closeout to point at the committed results file; what remains for Phase 6 (LEG/README claims) is deciding what, if anything, this README states on the strength of that run -- its mechanical proxy counts do not move in one direction, so no clean headline number falls out of it. | fixed |  | 2026-09-20T02:20:59.504Z | 2026-09-21T10:14:37.294Z |
| 26 | 02 | deviation | evals/trigger/DECISION-RULE-cat10.md |  | 02-10-PLAN.md's own git-diff removed-lines probes (Tasks 3, 5, 6, and the plan-level <verification> block) always print >=1 because git diff's '--- a/file' header line starts with '-', independent of any real content removal; the substantive check (grep -E '^-' \| grep -v '^--- ') printed empty throughout, proving zero real removed lines across the round. | waived | Plan-authored probe artifact, settled by the substantive check: 02-10-PLAN.md's git-diff removed-lines probes always print at least 1 because git diff's '--- a/file' header itself starts with '-'. The substantive form, grep -E '^-' filtered through grep -v '^--- ', printed empty throughout the round, proving zero real removed lines. Shipped content was never wrong. | 2026-09-20T09:08:30.444Z | 2026-09-21T10:14:38.013Z |
| 27 | 02 | deviation | evals/pressure-tests.md |  | 02-10-PLAN.md Task 4's 'not yet observed' whole-file count probe expects 14 but this file's own pre-existing intro paragraph (unrelated to this task, present since 02-05) already contains that literal phrase once as descriptive prose, so the naive count is 15; the table-scoped count (grep -cE '^\\| .* \\| not yet observed \\| - \\| - \\|$') correctly printed 14. | waived | Plan-authored probe artifact, settled by the table-scoped count: 02-10-PLAN.md Task 4's whole-file count of 'not yet observed' returned 15 against an expected 14 because evals/pressure-tests.md's own intro paragraph, present since 02-05 and unrelated to that task, carries the phrase once as descriptive prose. The table-scoped count returned 14, which is the figure that was ever in question. | 2026-09-20T09:08:30.560Z | 2026-09-21T10:14:38.130Z |
| 28 | 04 | unrun-verify | evals/routes/RESULTS-routes.md |  | 04-15 measured route equivalence and did not distinguish the three distribution routes: 36 headless claude-sonnet-5 sessions at --effort low, 3 routes x 4 scenarios x 3 repeats, every pair of arms overlapping on the mechanical proxy count (skill-on 7.9 [1-14], style-on 7.1 [3-11], prompt-on 6.3 [1-10]). What stays UNOBSERVED after this run, and is what this entry tracks: (a) the arms are not a level playing field -- skill-on must be triggered and was not in 3 of 12 sessions, while style-on and prompt-on are unconditionally on, so a null result between them is partly a statement about trigger behaviour (CAT-10, entry 24) rather than about rule delivery; (b) the reduced matrix authorised at the spend checkpoint carries one scenario per family, so a family-general effect cannot be separated from that scenario's quirks and no cross-check against Phase 5's eight-scenario arm is available; (c) prompt-on is a headless --append-system-prompt-file proxy, and no harness other than Claude Code was driven; (d) n=3 per cell on one model at one effort cannot distinguish a small real difference from run-to-run variance. Closing any of these needs more spend, not more code. Entries 11, 12, 16 and 17 are untouched by this run and stay open where they are routed. | waived | Measured null result, published with its four named limits: 04-15 ran 36 headless claude-sonnet-5 sessions at --effort low across 3 routes x 4 scenarios x 3 repeats, and every pair of arms overlapped on the mechanical proxy count. The limits are stated in evals/routes/RESULTS-routes.md itself — the arms are not a level playing field because skill-on must be triggered while style-on and prompt-on are unconditionally live; the reduced matrix carries one scenario per family; n=3 per cell; and one model at one effort. Accepted as a disclosed null result rather than restated as equivalence. | 2026-09-21T00:00:00.000Z | 2026-09-21T10:14:38.246Z |

````json
[
  {
    "id": 1,
    "kind": "unrun-verify",
    "phase": "01",
    "file": "examples/deal-brief.md",
    "line": null,
    "description": "T-01-04 name-collision web search for 4 invented parties + 5 invented persons not run (no live network access in this environment) \u2014 human must confirm via web search before repo goes public",
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
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-11T00:38:23.292Z",
    "resolved_at": "2026-09-21T10:14:36.928Z"
  },
  {
    "id": 4,
    "kind": "unrun-verify",
    "phase": "02",
    "file": "evals/pressure-tests.md",
    "line": null,
    "description": "D-31 trigger pressure-test: must-fire/must-not-fire phrasings recorded with method only \u2014 this environment cannot drive a fresh harness session to install the skill and observe activation, so every Observed cell reads 'not yet observed'; a human must run each phrasing in a real harness session and fill in Observed/Date/Harness before this is fixed",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-11T01:22:59.066Z",
    "resolved_at": "2026-09-20T02:20:51.557Z"
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
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-14T08:17:27.877Z",
    "resolved_at": "2026-09-21T10:14:37.056Z"
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
    "reason": "Publication DEFERRED at the 06-04 launch checkpoint on 2026-09-21 by explicit operator decision, recorded in LEGAL-REVIEW.md's ## Launch section. No remote was created and no placeholder was substituted; all four occurrences still read <owner>/<repo> and still agree with each other, so publish-location-drift stays silent. Owner: the operator. Closes when a real owner/repo is substituted in all four guarded locations AND at least one install route is observed resolving against it \u2014 substitution alone does not close this entry, because publish-location-drift proves the four agree and can never prove they resolve.",
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
    "reason": "DIST-06's prose-quality half. Not closed this round: the cold read it turns on requires a reader who did not write the text, and this round's README edits and their re-read would have been the same agent, with no independent reader available to the session. An author's self-read was performed and recorded in LEGAL-REVIEW.md's ## Human observations section 3; it found the lead-with-examples structure intact and the Install section truthful after the deferral. Owner: whoever performs the cold read. Closes on that read answering one specific question this record cannot answer about itself \u2014 whether the new claim region reads as an honest report of a mixed result or as a defensive one.",
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
    "status": "waived",
    "reason": "Plan-authored verify-script error, not a content defect: 04-04-PLAN.md expected 3 occurrences of the results-pointer path in README.md and described a third 'in the layout tree at line 104'. Direct inspection of the pre-rewrite file, live and via git show, confirms that third occurrence never existed; the shipped README carries the pointer the count needs and readme-results-pointer-missing enforces it. Nothing in shipped content is wrong, so there is nothing to fix.",
    "recorded_at": "2026-09-17T07:58:46.489Z",
    "resolved_at": "2026-09-21T10:14:37.421Z"
  },
  {
    "id": 14,
    "kind": "deviation",
    "phase": "04",
    "file": "tools/check_repo.py",
    "line": null,
    "description": "04-07-PLAN.md's own interfaces block stated 12 word-spelled cardinals measured in examples/deal-brief.md's prose and 3 such occurrences in skills/proof-first/references/worked-examples.md. Direct measurement with the exact SPELLED_CARDINAL_RE the shipped code uses (\\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\\b, case-insensitive) found 13 and 5 respectively. The shipped before-after-spelled-count docstring states the corrected figures (13, 5), not the plan's stated ones, matching the 03-04/04-01/04-04/04-04(id-13) precedent of documenting plan-authored measurement errors rather than force-fitting shipped content to them. No behavior or scope decision changes -- both files remain out of this code's scan (BEFORE_AFTER_PATH only).",
    "status": "waived",
    "reason": "Plan-authored measurement error, not a content defect: 04-07-PLAN.md's interfaces block stated 12 word-spelled cardinals in examples/deal-brief.md and 3 in worked-examples.md. Measuring with the exact SPELLED_CARDINAL_RE the shipped code uses returns different figures, and the shipped docstring already states the corrected ones. before-after-spelled-count is discrimination-proven against the real file.",
    "recorded_at": "2026-09-17T09:56:36.048Z",
    "resolved_at": "2026-09-21T10:14:37.540Z"
  },
  {
    "id": 15,
    "kind": "deviation",
    "phase": "04",
    "file": "tools/generate_derivatives.py",
    "line": null,
    "description": "04-10-PLAN.md's own import-set verify probe (regex `^\\\\s*(?:import|from)\\\\s+...`) matches the module docstring's prose line 'from the Python standard library;' (pre-existing text, unedited by this plan) in addition to the five real import statements, printing ['argparse','hashlib','pathlib','re','sys','the'] instead of the five-element list the acceptance criterion names. Direct inspection confirms the real import set (grep '^import \\\\|^from ' restricted to the five actual statement lines at the file's end) is exactly argparse/hashlib/pathlib/re/sys, unchanged by this plan. Matching the 03-04/04-01/04-03/04-04/WINDOWS-13 precedent for documenting a plan-authored verify-script false positive rather than rewording shipped docstring prose to dodge it.",
    "status": "waived",
    "reason": "Plan-authored probe error, not a content defect: 04-10-PLAN.md's import-set probe regex also matched the prose phrase 'from the Python standard library;' in the module docstring, inflating the import set by one. The real import set is the five statements the probe otherwise found, and tools/generate_derivatives.py imports only stdlib modules \u2014 re-asserted this phase by the AST-based stdlib check, which reads ast.Import/ast.ImportFrom nodes rather than regex over text and reports EXTRA [].",
    "recorded_at": "2026-09-17T10:46:40.096Z",
    "resolved_at": "2026-09-21T10:14:37.657Z"
  },
  {
    "id": 16,
    "kind": "unrun-verify",
    "phase": "04",
    "file": "README.md",
    "line": null,
    "description": "README's output-style route now states the copy step (mkdir -p ~/.claude/output-styles, cp output-styles/proof-first.md ~/.claude/output-styles/) and its destination directory; readme-output-style-destination-missing mechanically enforces that at least one destination directory is named. What remains unobserved is the last link in the chain: a live Claude Code session listing the copied style in /config and applying it \u2014 this repository's live sessions are headless claude -p runs (evals/conformance/run_conformance.py), which have no /config picker to observe. The two destination paths (~/.claude/output-styles/ and a project's .claude/output-styles/) are recorded from 04-UAT.md test 4's orchestrator-verified finding, not from a documentation source this environment can fetch. Closure condition: a human runs the stated copy on a real machine and confirms the style appears in /config, routed alongside entries 11 and 12 to Phase 6's LEG-04 launch gate.",
    "status": "open",
    "reason": "DIST-03's /config half. Not closed this round: the session executing Phase 6 is non-interactive and has no picker to open, and copying output-styles/proof-first.md into ~/.claude/output-styles/ would have produced the setup without the observation while changing the operator's own configuration directory for no verification gain, so it was not done. 04-15 already measured the half a script can reach \u2014 the style's content does arrive in a live session and an unrouted control cited none of this project's rule markers. Owner: a human on a machine with a /config picker. Closes when that human records the style listed and selectable; platform and destination directory are pre-recorded in LEGAL-REVIEW.md ## Human observations section 1.",
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
    "reason": "The entailment class: no code here compares two factual assertions in one document for consistency, and the refusal to build a fuzzy-proxy gate for it stands, on the reasoning already recorded in this entry. Not closed this round, for the same reason as id 12: no cold reader was available. What WAS done, recorded in LEGAL-REVIEW.md ## Human observations section 2, is a mechanical cross-reference of twelve checkable README claims against the shipped files \u2014 rule count, worked-pair count, every layout-tree and 'What exists today' path, all nine pooled tallies and the direction count against RESULTS.md's rendered tables, the trigger summary against RESULTS-trigger.md's totals, and the absence of the two sentences 06-03 superseded. No checkably-false statement was found; all four apparent findings were defects in the checking script, which is itself this ledger's 13/14/15/26/27 class and is exactly why a self-read is not accepted as a substitute. Owner: whoever performs the cold read. Closes on that read.",
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
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-18T09:36:23.879Z",
    "resolved_at": "2026-09-21T10:14:37.171Z"
  },
  {
    "id": 19,
    "kind": "unrun-verify",
    "phase": "05",
    "file": "evals/benchmark/scenarios.json",
    "line": null,
    "description": "Whether the eight scenario prompts are realistic presales tasks a bid team would actually receive (vs. shaped to favor one condition) is a verification:backstop truth per 05-02-PLAN.md, not mechanically checked.",
    "status": "waived",
    "reason": "Backstop truth, accepted with its reason stated: whether the eight scenario prompts in evals/benchmark/scenarios.json are realistic presales tasks is a judgement 05-02-PLAN.md classified verification:backstop, and no tool in this stack performs it. The scenarios are committed and readable, so a reader can judge them directly; the figures they produce are published with that limitation rather than behind it.",
    "recorded_at": "2026-09-18T09:36:24.007Z",
    "resolved_at": "2026-09-21T10:14:37.778Z"
  },
  {
    "id": 20,
    "kind": "unmet-truth",
    "phase": "05",
    "file": "evals/benchmark/run_benchmark.py",
    "line": null,
    "description": "05-REVIEW.md CR-02: aggregate()'s 'Judged persuasion' mean/range table pools individual per-order judgement records (n=6 per cell) instead of averaging each pair's two orders first, the way judge_summary()/average_orders() does for the win/tie/loss table. With a complete matrix (0 unscoreable, 0 excluded pairs) the published means are unaffected, which is why no committed figure is wrong today. But if one order of a pair were ever unscoreable, an un-paired, position-bias-uncorrected score would leak into the mean while RESULTS.md's own position-bias caveat still asserts orders are averaged before the report reads them. Non-blocking now, latent falsehood later.",
    "status": "open",
    "reason": "Routed to v2. aggregate()'s 'Judged persuasion' mean/range table pools per-order judgement records instead of averaging each pair's two orders first, so those means are partly an artifact of judge position. NOT fixed here, by explicit decision: the fix changes the means that evals/benchmark/RESULTS.md already publishes, which makes it a figure-moving change rather than a cheap one, and 06-04's own rule routes a figure-moving fix to v2. 06-03 did not inherit the defect \u2014 pooled_summary() consumes judge_summary()'s paired output and a self-test fixture is constructed so the paired and per-order answers differ, so the pooled totals README quotes are provably on the paired path. Owner: v2 benchmark maintainer. Closes when aggregate() averages orders before pooling and RESULTS.md is re-rendered with the corrected means and a note saying they changed and why.",
    "recorded_at": "2026-09-20T02:01:52.821Z",
    "resolved_at": null
  },
  {
    "id": 21,
    "kind": "unmet-truth",
    "phase": "05",
    "file": "evals/benchmark/run_benchmark.py",
    "line": null,
    "description": "05-REVIEW.md CR-03: raw-record filenames and aggregate()'s grouping key omit effort, judge_model and judge_effort. Re-running against a populated evals/benchmark/raw/ with a different --effort or --judge-model silently reuses stale-configuration records (skip-if-exists matches on the shorter key) with no diagnostic, and RESULTS.md never states which effort or judge model produced its numbers. The committed run is internally consistent (single effort, single judge model), so no published figure is wrong; the gap is that nothing prevents or discloses a mixed-configuration run.",
    "status": "open",
    "reason": "Routed to v2. Raw-record filenames and aggregate()'s grouping key omit effort, judge_model and judge_effort, so re-running against a populated evals/benchmark/raw/ with a different --effort or --judge-model silently reuses stale-configuration records via skip-if-exists. No v1 requirement depends on a re-run at a different configuration, and the committed run is internally consistent at one configuration. Owner: v2 benchmark maintainer. Closes when the record key includes effort, judge_model and judge_effort, and a re-run at a changed configuration is observed writing new records rather than reusing old ones.",
    "recorded_at": "2026-09-20T02:01:52.940Z",
    "resolved_at": null
  },
  {
    "id": 22,
    "kind": "unmet-truth",
    "phase": "05",
    "file": "evals/benchmark/run_benchmark.py",
    "line": null,
    "description": "05-REVIEW.md CR-04: a (model, scenario, condition) cell whose every generation attempt failed is silently absent from the 'Mechanical proxy counts' table, with no 'Unscoreable generations: N' line -- asymmetric with the judgement side, which does print 'Unscoreable judgements: N' and 'Excluded pairs: N'. The committed run has zero unscoreable generations so nothing is hidden today, but a future partial run could publish a table that silently covers fewer cells than it appears to.",
    "status": "open",
    "reason": "Routed to v2. A (model, scenario, condition) cell whose every generation attempt failed is silently absent from the Mechanical proxy counts table, with no 'Unscoreable generations: N' line \u2014 asymmetric with the judgement side, which prints both 'Unscoreable judgements' and 'Excluded pairs'. The committed run has no such cell, so no published figure is affected today; the defect is that a future run could lose a cell without saying so. Owner: v2 benchmark maintainer. Closes when build_results_md() emits an unscoreable-generation count alongside the mechanical table, with a self-test fixture in which a wholly-failed cell is reported rather than dropped.",
    "recorded_at": "2026-09-20T02:01:53.066Z",
    "resolved_at": null
  },
  {
    "id": 23,
    "kind": "deviation",
    "phase": "05",
    "file": "evals/benchmark/run_benchmark.py",
    "line": null,
    "description": "05-REVIEW.md W-02: DISALLOWED_TOOLS = ['Write','Edit','Bash','NotebookEdit'] omits WebSearch and WebFetch, so generations run with web access available. MEASURED, NOT HYPOTHETICAL: summing usage.server_tool_use across all 96 committed generation records gives web_search_requests=0 and web_fetch_requests=0, so the committed measurement is uncontaminated. Recorded as a hardening gap for any future run, not as a defect in the published numbers.",
    "status": "waived",
    "reason": "Measured, not hypothetical: DISALLOWED_TOOLS omits WebSearch and WebFetch, so generations ran with web access nominally available. Summing usage.server_tool_use across all 96 committed generation records gives web_search_requests=0 and web_fetch_requests=0 \u2014 no generation used either tool, so no published figure is contaminated. The omission is real and the exposure it created was measured to be zero.",
    "recorded_at": "2026-09-20T02:01:53.185Z",
    "resolved_at": "2026-09-21T10:14:37.893Z"
  },
  {
    "id": 24,
    "kind": "unmet-truth",
    "phase": "02",
    "file": "skills/proof-first/SKILL.md",
    "line": null,
    "description": "CAT-10 over-broad description. The 2026-09-20 n=1 observation (9/9 must-fire, 2/5 must-not-fire over-fires) was superseded by the CAT-10 gap-closure round's paired n=5 measurement (02-10-PLAN.md, evals/trigger/DECISION-RULE-cat10.md, evals/trigger/RESULTS-trigger.md): Arm B (control, unchanged 439-char description) measured OF_B/SN_B=9/25 over-fires and MH_B/SM_B=45/45 must-fire hits. Arm A (treatment, 551-char description with an appended exclusion clause) measured OF_A/SN_A=0/25 (every must-not-fire row clean) but MH_A/SM_A=40/45 -- the must-fire row 'We're putting together our bid response -- write the commercial section.' regressed from 5/5 to 0/5, a genuine must-fire regression the pre-committed decision rule's Branch 4 catches ahead of Branch 1's clean over-fire elimination (Fisher exact p_attr=0.0016 on the over-fire delta alone -- real, and still insufficient because it cost a legitimate must-fire request). The treatment was tested live and REVERTED; the shipped description is unchanged from the original 439-char text, still measuring 9/25 must-not-fire hits at n=5. This entry stays open: the exclusion-clause lever is now a tested and refuted first candidate, not an unfunded one -- the next lever (most likely H1's audience-clause removal, deliberately not bundled into this round) remains unattempted.",
    "status": "open",
    "reason": "Routed to v2, with the next lever named. CAT-10's description is over-broad: the shipped 439-character text measures 9 of 25 must-not-fire over-fires at n=5. The first candidate lever \u2014 an appended exclusion clause, 551 characters \u2014 was tested live under the pre-committed decision rule and REFUTED, not merely untried: it eliminated every must-not-fire over-fire (Fisher exact p_attr=0.0016) but regressed a legitimate must-fire row from 5/5 to 0/5, selecting Branch 4, and it was reverted. The shipped description is unchanged. Owner: v2 skill maintainer. Closes when the next lever \u2014 most likely H1's audience-clause removal, deliberately not bundled into the 02-10 round \u2014 is measured under the same paired protocol and either kept or refuted on the record.",
    "recorded_at": "2026-09-20T02:20:51.680Z",
    "resolved_at": null
  },
  {
    "id": 25,
    "kind": "unmet-truth",
    "phase": "05",
    "file": "README.md",
    "line": null,
    "description": "Phase 5 closeout left README.md asserting its own benchmark 'has not run' and listing it under 'What does not exist yet', while evals/benchmark/RESULTS.md records a 2026-09-18 run of 96 generations across claude-opus-5 and claude-sonnet-5 with both-orders judge scoring. The false negative claims were corrected during Phase 2's closeout to point at the committed results file; what remains for Phase 6 (LEG/README claims) is deciding what, if anything, this README states on the strength of that run -- its mechanical proxy counts do not move in one direction, so no clean headline number falls out of it.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-20T02:20:59.504Z",
    "resolved_at": "2026-09-21T10:14:37.294Z"
  },
  {
    "id": 26,
    "kind": "deviation",
    "phase": "02",
    "file": "evals/trigger/DECISION-RULE-cat10.md",
    "line": null,
    "description": "02-10-PLAN.md's own git-diff removed-lines probes (Tasks 3, 5, 6, and the plan-level <verification> block) always print >=1 because git diff's '--- a/file' header line starts with '-', independent of any real content removal; the substantive check (grep -E '^-' | grep -v '^--- ') printed empty throughout, proving zero real removed lines across the round.",
    "status": "waived",
    "reason": "Plan-authored probe artifact, settled by the substantive check: 02-10-PLAN.md's git-diff removed-lines probes always print at least 1 because git diff's '--- a/file' header itself starts with '-'. The substantive form, grep -E '^-' filtered through grep -v '^--- ', printed empty throughout the round, proving zero real removed lines. Shipped content was never wrong.",
    "recorded_at": "2026-09-20T09:08:30.444Z",
    "resolved_at": "2026-09-21T10:14:38.013Z"
  },
  {
    "id": 27,
    "kind": "deviation",
    "phase": "02",
    "file": "evals/pressure-tests.md",
    "line": null,
    "description": "02-10-PLAN.md Task 4's 'not yet observed' whole-file count probe expects 14 but this file's own pre-existing intro paragraph (unrelated to this task, present since 02-05) already contains that literal phrase once as descriptive prose, so the naive count is 15; the table-scoped count (grep -cE '^\\| .* \\| not yet observed \\| - \\| - \\|$') correctly printed 14.",
    "status": "waived",
    "reason": "Plan-authored probe artifact, settled by the table-scoped count: 02-10-PLAN.md Task 4's whole-file count of 'not yet observed' returned 15 against an expected 14 because evals/pressure-tests.md's own intro paragraph, present since 02-05 and unrelated to that task, carries the phrase once as descriptive prose. The table-scoped count returned 14, which is the figure that was ever in question.",
    "recorded_at": "2026-09-20T09:08:30.560Z",
    "resolved_at": "2026-09-21T10:14:38.130Z"
  },
  {
    "id": 28,
    "kind": "unrun-verify",
    "phase": "04",
    "file": "evals/routes/RESULTS-routes.md",
    "line": null,
    "description": "04-15 measured route equivalence and did not distinguish the three distribution routes: 36 headless claude-sonnet-5 sessions at --effort low, 3 routes x 4 scenarios x 3 repeats, every pair of arms overlapping on the mechanical proxy count (skill-on 7.9 [1-14], style-on 7.1 [3-11], prompt-on 6.3 [1-10]). What stays UNOBSERVED after this run, and is what this entry tracks: (a) the arms are not a level playing field -- skill-on must be triggered and was not in 3 of 12 sessions, while style-on and prompt-on are unconditionally on, so a null result between them is partly a statement about trigger behaviour (CAT-10, entry 24) rather than about rule delivery; (b) the reduced matrix authorised at the spend checkpoint carries one scenario per family, so a family-general effect cannot be separated from that scenario's quirks and no cross-check against Phase 5's eight-scenario arm is available; (c) prompt-on is a headless --append-system-prompt-file proxy, and no harness other than Claude Code was driven; (d) n=3 per cell on one model at one effort cannot distinguish a small real difference from run-to-run variance. Closing any of these needs more spend, not more code. Entries 11, 12, 16 and 17 are untouched by this run and stay open where they are routed.",
    "status": "waived",
    "reason": "Measured null result, published with its four named limits: 04-15 ran 36 headless claude-sonnet-5 sessions at --effort low across 3 routes x 4 scenarios x 3 repeats, and every pair of arms overlapped on the mechanical proxy count. The limits are stated in evals/routes/RESULTS-routes.md itself \u2014 the arms are not a level playing field because skill-on must be triggered while style-on and prompt-on are unconditionally live; the reduced matrix carries one scenario per family; n=3 per cell; and one model at one effort. Accepted as a disclosed null result rather than restated as equivalence.",
    "recorded_at": "2026-09-21T00:00:00.000Z",
    "resolved_at": "2026-09-21T10:14:38.246Z"
  }
]
````
