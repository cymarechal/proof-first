---
phase: 03-completeness-audit-artifact-patterns
verified: 2026-09-16T09:37:32Z
status: gaps_found
score: "8/10 truths verified, 2 failed, 0 present-behavior-unverified"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: "8/9 truths verified, 1 failed, 0 present-behavior-unverified"
  gaps_closed:
    - "CR-01 (unanchored scorer): score_transcript()'s family search is now bounded to the transcript's opening 400 characters (FAMILY_LINE_WINDOW_CHARS), both offsets computed against the same `stripped` string. Independently confirmed by direct source read and by re-running the two discrimination probes (no-family / conformant) in this session — both match the fix's intended direction."
    - "WR-01 (old, timeout data loss on a single transcript): run_session() now catches TimeoutExpired, normalises bytes/str/None streams, writes a decoded partial transcript, and re-raises unchanged. Confirmed present in source."
    - "CR-02 (README false claim): README.md's Status section no longer states 'no measured claim is published.' It names evals/conformance/RESULTS-mod04.md, carries four caveats, states no percentage, and correctly attributes the still-unrun persuasion benchmark to Phase 5. A new discrimination-proven check (`readme-results-pointer-missing`, 30th->31st-adjacent code) guards this from silently regressing. Confirmed by direct read and independent check_repo.py --mutation-test re-run in this session."
    - "MOD-04 was remeasured a fourth time (03-12), this time entirely under the anchored (CR-01-fixed) scorer, with a mechanically pre-committed disposition rule committed to git before any session ran. Independently re-derived: Arm A (post-03-11 ordering-gate lever) 3/10 = 30.0%; Arm B (paired pre-03-11 baseline) 4/10 = 40.0%; delta -10.0pp, correctly selecting Branch 4. All four MOD-04 trackers (RESULTS-mod04.md, WINDOWS.md entry 8, REQUIREMENTS.md, 03-UAT.md G-03-2) carry identical figures. WINDOWS.md entry 8 correctly moved from `open` to `waived` (accepted, disclosed residual, explicitly not `fixed`), and MOD-04's checkbox correctly stays `[ ]`."
  gaps_remaining:
    - "MOD-04 (SC3, live-session half) — still FAILED, and by the honest anchored measurement, WORSE than the prior optimistic-ceiling figures suggested: 30.0% (3/10) for the post-03-11 skill, actually below the 40.0% (4/10) pre-03-11 paired baseline. Three levers (03-05 restatement, 03-07 five-value family line + presence gate, 03-11 mechanical self-check ordering re-scan) have now each been measured and none reached the 87.5% bar; the anchored figures are markedly lower than every unanchored figure for this residual, consistent with CR-01's documented optimistic-ceiling bias. The project's own disposition (WINDOWS.md entry 8 `waived`) is an honest acceptance of an unresolved residual, not a claim of satisfaction — this verification agrees with that self-assessment and does not soften it further in either direction."
  regressions: []
gaps:
  - truth: "The skill states which artifact family it classified the document as before applying any rules, in every live write-mode session (SC3, live half / MOD-04)"
    status: failed
    reason: "03-12's anchored remeasurement — the first MOD-04 figure produced under a scorer proven not to inflate the rate (03-09's FAMILY_LINE_WINDOW_CHARS=400 fix) — measured the current shipped skill (post-03-11, blob fadc48613f71fb29d55b42f70805225f9087a2b9) at 3/10 = 30.0% scoreable claude-sonnet-5 sessions conformant. A same-instrument, same-model paired baseline of the pre-03-11 skill (blob 9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a) measured 4/10 = 40.0% — i.e. the newest, most targeted lever measured WORSE than its own immediate predecessor once the scorer's optimistic bias was removed, a 10.0-percentage-point decline (disclosed by the project itself as within plausible sampling noise at n=10 per arm, not proof the lever actively hurts). Independently re-derived in this session directly from the 23 committed run blocks (12 Arm A lines including 2 retried timeouts, 11 Arm B lines including 1 retried timeout): counts match exactly (N_A=3/M_A=10, N_B=4/M_B=10). This is the same truth that failed in the prior verification round; four measurement rounds across four different levers and two scorer generations have now all landed under the 87.5% closure bar, three of them clustered well below it and none close."
    artifacts:
      - path: "skills/proof-first/SKILL.md"
        issue: "The self-check's first pass (`## Self-check before delivering`) now gates on ordering, not merely presence — 're-scan the drafted response... confirm no PF-/MC- marker stands before the artifact-family line... move the family line to the top' — and is mechanically anchored by `skill-family-order-gate-missing` (discrimination-proven). The instruction is present, worded correctly, and cannot be silently deleted. It still does not reliably change model behavior: every non-conformant session this round scored `no-family` (the family phrase never appeared at all within the first 400 characters), not `rule-before-family` (the failure mode 03-11 specifically targeted) — meaning the ordering re-scan lever addressed a residual that, under the anchored scorer, was apparently much smaller or differently shaped than 03-08's unanchored measurement suggested."
    missing:
      - "A lever that does not depend on the model correctly following either a restated instruction or a self-check it performs on its own output — 03-12's own Next Phase Readiness section names the candidate direction: a post-generation mechanical repair (not just detection) applied by the skill or a wrapping tool before the response reaches the user, rather than trusting the model's own re-scan."
      - "Alternatively, an explicit, human-made decision (this verifier is not making it) that the write-mode classify-before-rules ordering is acceptable at a ~30-40% observed rate for v1, given three distinct lever types have now been tried and measured without reaching the bar."
  - truth: "The project's own 'measured claims or no claims' reproducibility constraint holds for the instrument that produced this phase's headline MOD-04 measurement (CLAUDE.md's evidence constraint, applied to the phase's own committed script)"
    status: failed
    reason: "03-REVIEW.md's fresh code review (completed 2026-09-16, after 03-12 landed) found a new, currently unresolved Critical finding (CR-01 in that review — a different CR-01 from the one 03-09 fixed): `run_conformance.py`'s live-mode `main()` loop accumulates every session's result line into an in-memory `lines` list and writes it to `RESULTS-mod04.md` in a single deferred `f.writelines(lines)` call only after the ENTIRE model x fixture x repeat loop finishes. Confirmed by direct source read in this session: `lines = []` still exists at line 687, and the single deferred `with open(out_path, 'a') as f: f.writelines(lines)` still exists at lines 761-762 — the review's exact fix (write-and-flush per session) has not been applied. `RESULTS-mod04.md` itself documents this exact failure mode having already destroyed two entire prior measurement attempts (a Claude Code session-usage-limit interruption, then a session teardown) — the project's response was operational (drive the matrix as many single-invocation-per-session calls) rather than a code fix, and the tool's own documented default usage in its module docstring (`python3 evals/conformance/run_conformance.py [--fixtures A,B,C] [--models M,...] [--repeats N]`) is still the vulnerable multi-session single-invocation pattern. This is a genuine, reproducible data-loss defect in a script this project holds up as the reproducible backing for its one committed measurement, discovered by this phase's own review and not yet addressed by any commit."
    artifacts:
      - path: "evals/conformance/run_conformance.py"
        issue: "Lines ~687 (`lines = []` in-memory accumulator) through ~761-762 (single deferred `f.writelines(lines)` after the full loop) — confirmed present at HEAD by direct read in this session. An ordinary interruption between sessions (not just mid-session, which WR-01/old-CR-01 already cover) silently discards every already-scored session in that invocation."
      - path: "evals/conformance/RESULTS-mod04.md"
        issue: "03-REVIEW.md's WR-01 (this round's — a different WR-01 from 03-09's fixed one): the Arm A `no-family` breakdown at lines ~756-757 states 'no-family: 7 (...)' but its own parenthetical names only 6 sessions (2+2+1+1), omitting the `B-proposal-section` first-attempt no-family verdict recorded at line ~596 of the same file. Confirmed present by direct read in this session — the aggregate N_A/M_A figures are unaffected (correctly 3/10), but the file explicitly claims to be 're-derivable by anyone... without re-running anything' and a manual check of this specific enumeration does not add up."
    missing:
      - "The review's suggested fix: write each session's result line to `out_path` immediately after it is scored (with `f.flush()`), rather than batching into an in-memory list, so an interruption between sessions loses at most the in-flight one."
      - "Correct the Arm A no-family enumeration in RESULTS-mod04.md to name all 7 sessions, including the omitted `B-proposal-section` first attempt."
      - "Two lower-severity, also-unresolved review findings, not rising to gap level but worth folding into the same fix pass: WR-02 (`check_skill_family_line_gate()` matches its two anchors case-sensitively while its 03-11 sibling `check_skill_family_order_gate()` matches case-insensitively — a real, disclosed-as-deliberate inconsistency per 03-11's own SUMMARY, but the review correctly notes it leaves the older check needlessly brittle against an unremarkable future capitalization edit) and IN-01 (`tools/check_repo.py`'s module docstring still describes `skill-token-budget-exceeded` as an open, currently-firing finding against the real SKILL.md; it has been silent since Phase 2 per WINDOWS.md entry 5, `status: fixed`, and the docstring is stale)."
deferred:
  - truth: "AUD-01 — independent human (not subagent) paraphrase-boundary read of the MC dimension bodies against SOURCES.md"
    addressed_in: "Phase 6"
    evidence: "ROADMAP.md Phase 6 goal: 'The repo is legally cleared and honestly marketed before anyone outside the project sees it', Success Criterion 1 names MEDDIC-family trademark status reconfirmation against current sources; WINDOWS.md entries 3 and 6 both state the same class of reproduction-boundary judgment is routed to Phase 6 LEG-04. Re-confirmed untouched this round: 03-12 Task 3 explicitly re-asserted AUD-01 stays `[ ]` with its Phase-6 annotation intact, verified by direct read in this session."
  - truth: "ART-01 through ART-04 — independent human paraphrase-boundary read of the four artifact-family sections"
    addressed_in: "Phase 6"
    evidence: "WINDOWS.md entry 9 (mechanically fixed in 03-07): 'Closure: fold into the next content plan or into Phase 6 LEG-04 alongside entries 3 and 6' — the human-provenance judgment itself remains Phase 6 LEG-04's to close. Re-confirmed untouched this round: all four checkboxes still `[ ]`, verified by direct grep in this session (`grep -cE '^\\- \\[ \\] \\*\\*(AUD-01|ART-01|ART-02|ART-03|ART-04)\\*\\*'` returns 5)."
human_verification:
  - test: "Read all eight MC dimension bodies and all four artifact-family sections end to end against SOURCES.md's reproduction boundary, with a real human, not a subagent."
    expected: "Confirm the six relabeled MC bodies and the one relabeled artifact-patterns.md appositive read as document-facing prose, not source restatement, and make the final call on the MEDDICC letter-order tension (WINDOWS entries 3, 6, 9)."
    why_human: "SOURCES.md itself states this paraphrase-boundary judgment is semantic; no tool in this stack performs it. Explicitly deferred to Phase 6 LEG-04, unchanged this round."
  - test: "Decide whether the project should invest a further, structurally-different lever at MOD-04 (a post-generation mechanical repair applied outside the model's own self-check, per 03-12's own Next Phase Readiness note) or formally accept the ~30-40% observed anchored rate as a disclosed v1 limitation and move on."
    expected: "A team decision on MOD-04's disposition beyond 'WINDOWS.md entry 8 stays waived, no further lever scheduled.' Three structurally distinct levers (restatement, presence gate, self-check ordering re-scan) have now been tried and none reached the bar; the anchored figures are markedly lower than every earlier unanchored figure for this exact residual, so continuing to iterate on prompt/self-check wording specifically has a weakening evidence base for success."
    why_human: "This is a project-prioritization and risk-acceptance decision, not a mechanical check. The measurement is now honest and reproducible (once CR-01/new is fixed); what to do about the residual is a judgment call this verifier is not making on the project's behalf."
---

# Phase 3: Completeness Audit & Artifact Patterns Verification Report

**Phase Goal:** A writer can classify a document by artifact family, apply that family's conventions, and get a document-level completeness verdict and trustworthy rule citations — independent of the prose rules.
**Verified:** 2026-09-16T09:37:32Z
**Status:** gaps_found
**Re-verification:** Yes — fourth round. Plans 03-09 through 03-12 (a gap-closure wave targeting the prior round's two open gaps — MOD-04/WINDOWS entry 8, and the CR-01/CR-02 code-review findings from the prior round) plus a fresh code review (03-REVIEW.md) that verified all three prior findings genuinely fixed and surfaced one new Critical and two new Warnings, none yet addressed by any commit.

## Project Gate (independently re-run, not taken on trust)

```
$ python3 tools/check_repo.py --self-test
self-test PASS - verified violation codes: artifact-family-section-missing, catalog-count-mismatch,
catalog-count-unstated, catalog-id-drift, catalog-opening-rule-count, dup-figure-key, dup-id,
figure-order, framework-statement-missing, frontmatter-description-invalid, frontmatter-name-mismatch,
frontmatter-unknown-key, frontmatter-unparseable, license-missing, mc-catalog-id-drift,
mc-count-mismatch, mc-count-unstated, mc-rule-in-skill, pointer-duplicated, pointer-missing,
pointer-unparseable, range-id, readme-results-pointer-missing, revived-id,
skill-family-line-gate-missing, skill-family-order-gate-missing, skill-token-budget-exceeded,
skill-too-long, source-label-in-skill-content, undefined-id, unlisted-figure
(31 codes)

$ python3 tools/check_repo.py --mutation-test
mutation-test PASS: 31 codes discrimination-proven
(exit 0)

$ python3 tools/check_repo.py
check_repo: 0 violations
(exit 0)

$ python3 evals/conformance/run_conformance.py --self-test
self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable
(exit 0)
```

All four commands re-run fresh in this session. All exit 0, and the code count (31, up from 29 in the
prior verification round: `readme-results-pointer-missing` from 03-10, `skill-family-order-gate-missing`
from 03-11) matches every claim in 03-09/03-10/03-11/03-12's SUMMARYs exactly.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | (SC1, structural) MC namespace/registry never blended into prose rules | ✓ VERIFIED | Regression-confirmed: 8 `### MC-` headings in `completeness-audit.md`; `mc-rule-in-skill` still discrimination-proven in this session's mutation-test re-run. Unchanged this round. |
| 2 | (SC1, live half / AUD-03) Standalone audit returns a separate verdict, independent of prose rules | ✓ VERIFIED (with a disclosed caveat, carried forward) | Unchanged this round: 6/6 clean UAT sessions, `[x]` checkbox re-confirmed untouched by 03-12 Task 3's own drift check and by direct read in this session. |
| 3 | (SC2, structural) Four artifact families each get distinct conventions and expected order | ✓ VERIFIED | Regression-confirmed: 4 family `## ` headings, distinct `**Order:**` lines, `artifact-family-section-missing` still discrimination-proven. Content-quality half (ART-01..04) remains open — see Deferred. |
| 4 | (SC3, structural / MOD-04) Classification instruction exists in both modes, states the ordering explicitly, and is mechanically gated on BOTH presence and ordering | ✓ VERIFIED (strengthened this round) | `SKILL.md`'s self-check first pass (confirmed by direct read) now reads: re-scan the drafted response, confirm no `PF-`/`MC-` marker stands before the artifact-family line, move the line to the top and re-check if one does. Two sibling checks, `skill-family-line-gate-missing` (presence) and `skill-family-order-gate-missing` (ordering, new in 03-11), are both discrimination-proven in this session's mutation-test re-run (31/31). Token budget confirmed at 4,823 estimated tokens, 177 headroom (>= 100 floor). |
| 5 | (SC3, live half) A live session actually classifies before applying any rule, in every session | ✗ **FAILED** | 03-12's anchored remeasurement (the first MOD-04 figure produced under a scorer proven not to inflate the rate): Arm A (current shipped skill) 3/10 = 30.0% conformant; Arm B (immediately prior skill, paired baseline) 4/10 = 40.0%. Independently re-derived from the 23 committed run blocks in this session — arithmetic matches exactly. The newest, most targeted lever (03-11's mechanical self-check ordering re-scan) measured WORSE than its own predecessor once the scorer's optimistic bias was removed. WINDOWS.md entry 8 correctly moved to `waived` (accepted, disclosed residual — explicitly not a satisfied requirement), and `MOD-04` correctly stays `[ ]`. |
| 6 | (SC4, structural / MOD-03) Four labeled sections in fixed order, correct lead-in wording | ✓ VERIFIED | Unchanged this round: `SKILL.md`'s four-section wording directly re-confirmed present by read in this session. |
| 7 | (SC4, live half / MOD-03) A live check-mode session prints all four sections, in order, with no-findings lines | ✓ VERIFIED | Unchanged this round: 03-UAT.md test 3, 9/9 live sessions. No new session run against this truth this round (03-09..12 targeted MOD-04's instrument and measurement, not MOD-03); no regression evidence found. |
| 8 | (SC5, shipped-file half / MOD-05) Check mode never cites an unallocated rule number | ✓ VERIFIED | Regression-confirmed: `undefined-id`, `mc-catalog-id-drift`, `mc-count-unstated`/`mc-count-mismatch` all still discrimination-proven in this session's mutation-test re-run (31/31). |
| 9 | (SC5, live-session half / MOD-05) A live conversation never fabricates a rule number | ✓ VERIFIED | Unchanged this round: 03-UAT.md test 4, 18/18 sessions, 224 distinct citations, zero unallocated IDs. |
| 10 | (New this round) The project's own "measured claims or no claims" reproducibility constraint holds for the instrument backing this phase's one committed measurement | ✗ **FAILED** | 03-REVIEW.md's fresh review (2026-09-16) found a new, unresolved Critical (CR-01 in that review): `run_conformance.py`'s live-mode loop batches every session result into an in-memory list and writes it in one deferred call after the full loop finishes — confirmed present at HEAD by direct source read in this session (`lines = []` at line 687, single deferred `f.writelines(lines)` at lines 761-762). `RESULTS-mod04.md` itself documents this exact failure mode having already destroyed two prior measurement attempts, worked around operationally (one invocation per session) rather than fixed in code. This did not corrupt 03-12's own measurement (which used the one-invocation-per-session workaround throughout, independently confirmed via the 23 individually-committed run-block commits), but the shipped script remains genuinely vulnerable under its own documented default usage. A related itemization error (this round's WR-01: Arm A's `no-family` breakdown names 6 sessions where it states 7) is also unresolved, confirmed present by direct read. |

**Score:** 8/10 truths verified, 2 FAILED, 0 present-behavior-unverified. Truth 5 is the same truth that
failed in every prior verification round of this phase; this round adds the first anchored (non-inflated)
measurement of it, and the honest reading is that the residual is not shrinking with more instruction-wording
and self-check levers — it may be worse than the unanchored measurements suggested. Truth 10 is new this
round: this phase's own code review found a genuine, currently-unfixed defect in the very instrument this
phase committed as its evidentiary backing, which is exactly the class of gap this project's "measured
claims or no claims" standard exists to catch.

### Deferred Items

| # | Item | Addressed In | Evidence |
|---|------|-------------|----------|
| 1 | AUD-01 — independent human paraphrase-boundary read of the MC dimension bodies | Phase 6 | ROADMAP.md Phase 6 Success Criterion 1 (MEDDIC-family trademark reconfirmation); WINDOWS.md entries 3, 6 |
| 2 | ART-01..04 — independent human paraphrase-boundary read of the four artifact-family sections | Phase 6 | WINDOWS.md entry 9's closure note routes the human-provenance judgment to Phase 6 LEG-04 |

### Required Artifacts (regression + new-this-round check)

| Artifact | Status | Details |
|---|---|---|
| `skills/proof-first/references/completeness-audit.md` | ✓ VERIFIED | Unchanged this round; 8 MC headings confirmed. |
| `skills/proof-first/references/artifact-patterns.md` | ✓ VERIFIED | Unchanged this round; 4 family headings confirmed, no frozen source label. |
| `skills/proof-first/SKILL.md` | ✓ VERIFIED | 31/31 PF rules intact; self-check now carries both the presence pass and the new ordering pass (`re-scan`, `before any rule marker`, confirmed by direct read); token budget 4,823/5,000 (177 headroom). |
| `tools/check_repo.py` | ✓ VERIFIED | 31/31 codes discrimination-proven (up from 29), confirmed by independent `--mutation-test` re-run in this session. `readme-results-pointer-missing` and `skill-family-order-gate-missing` both confirmed newly present and firing correctly on their registered mutations. |
| `evals/conformance/run_conformance.py` | ⚠️ VERIFIED-WITH-DEFECT | `--self-test` passes (10 inline cases + 5 fixture cross-checks, confirmed by independent re-run). The prior round's CR-01 (unbounded family search) and WR-01 (single-transcript timeout data loss) are both genuinely fixed, confirmed by direct source read. A NEW, currently-unresolved defect (this round's review CR-01: whole-run in-memory batching, data loss on inter-session interruption) was found by 03-REVIEW.md and confirmed still present in this session — not yet fixed by any commit. |
| `evals/conformance/RESULTS-mod04.md` | ⚠️ VERIFIED-WITH-DEFECT | `## Scorer anchoring correction (CR-01)`, `## Pre-committed disposition rule (03-12)`, and `## Anchored remeasurement result (03-12)` all present in the correct order (confirmed by grep offsets); the 03-12 arithmetic (N_A=3/M_A=10, N_B=4/M_B=10) independently re-derived from the raw run blocks in this session and correct. One itemization defect (this round's review WR-01, distinct from a same-named finding fixed earlier) remains unresolved: the Arm A `no-family` parenthetical names 6 sessions where the line states 7 — confirmed by direct read; does not affect the correct aggregate figures. |
| `.planning/REQUIREMENTS.md` | ✓ VERIFIED | Checkbox states correct: AUD-02/AUD-03/MOD-03/MOD-05 `[x]`; AUD-01/ART-01..04/MOD-04 `[ ]`. `grep -c "^- \[x\].*UNVERIFIED"` returns 0, independently re-run in this session. MOD-04's annotation now carries all four measurement rounds (5/6, 14/16, 16/20+5/11, 3/10+4/10 anchored) with model ids, blob SHAs, and reproduction commands. |
| `.planning/WINDOWS.md` | ✓ VERIFIED | Entries 3, 6 remain `open` (correctly, Phase 6-owned). Entries 5, 7, 9 remain `fixed`. Entry 8 now `waived` (was `open`), description and reason replaced with the anchored figures — confirmed by direct JSON parse in this session, parses cleanly. |
| `README.md` | ✓ VERIFIED (CR-02 closed) | Status section confirmed by direct read: no longer states "no measured claim is published"; names `evals/conformance/RESULTS-mod04.md`, four caveats, no percentage, correctly attributes the still-unrun persuasion benchmark to Phase 5. Repository-layout tree and what-exists-today list both now list `evals/conformance/`. `readme-results-pointer-missing` guards this from silently regressing. |

### Requirements Coverage

| Requirement | Status | Evidence |
|---|---|---|
| AUD-01 | ? NEEDS HUMAN — correctly `[ ]` | Unchanged this round; deferred to Phase 6 LEG-04; 03-12 explicitly re-verified untouched. |
| AUD-02 | ✓ SATISFIED — `[x]` | Mechanically enforced, unchanged. |
| AUD-03 | ✓ SATISFIED (with caveat) — `[x]` | Unchanged this round. |
| ART-01..04 | ? NEEDS HUMAN — correctly `[ ]` | Structurally implemented and mechanically enforced; content-quality/paraphrase read still deferred to Phase 6 LEG-04. |
| MOD-03 | ✓ SATISFIED — `[x]` | Unchanged this round. |
| MOD-04 | ✗ **BLOCKED** — correctly `[ ]` | Now measured four times under three recipes and two scorer generations (5/6, 14/16, 16/20+5/11, and this round's anchored 3/10 vs 4/10), all below the closure bar. The anchored figure is the most trustworthy one produced so far and shows no improvement — arguably a decline — versus the immediately prior skill version. `WINDOWS.md` entry 8 is `waived`: an honest, disclosed acceptance of the residual, not a claim that the requirement is satisfied. |
| MOD-05 | ✓ SATISFIED — `[x]` | Unchanged this round. |

No requirement is ORPHANED. All ten requirement IDs (AUD-01..03, ART-01..04, MOD-03..05) declared across
the phase's 12 plans' frontmatter are accounted for above.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| `evals/conformance/run_conformance.py` | ~687, ~761-762 | Whole-run in-memory result batching (this round's review CR-01, unresolved, confirmed present in this session) — an interruption between sessions (process kill, uncaught exception type, external termination) silently discards every already-scored session in that invocation. | 🛑 Blocker (data-integrity defect in the instrument backing this phase's one committed, "reproducible from a committed script" measurement) | `RESULTS-mod04.md` itself documents two prior total losses from this exact class of failure, worked around operationally rather than fixed. Does not invalidate 03-12's own 30.0%/40.0% figures (which used the one-invocation-per-session workaround throughout, independently confirmed via 23 individually committed run blocks), but the shipped tool's documented default usage remains vulnerable to a class of loss this project's own WR-01 fix already solved for the single-transcript case. |
| `evals/conformance/RESULTS-mod04.md` | ~756-757 | Arm A `no-family` breakdown states "7" but its own parenthetical enumerates only 6 sessions, omitting the `B-proposal-section` first-attempt no-family verdict (this round's review WR-01, unresolved, confirmed present). | ⚠️ Warning | Aggregate N_A/M_A figures (3/10, 30.0%) are correct and unaffected — this is an itemization gap in a file that explicitly claims full manual re-derivability. |
| `tools/check_repo.py` | ~1413-1466 | `check_skill_family_line_gate()` matches its two anchors case-sensitively while its 03-11 sibling `check_skill_family_order_gate()` matches case-insensitively (this round's review WR-02, unresolved, confirmed present; a deliberate, disclosed asymmetry per 03-11's own SUMMARY, but the review's point about differential brittleness against a plausible future capitalization edit stands). | ⚠️ Warning | Leaves the older presence-gate check needlessly brittle relative to its newer sibling; not a correctness defect against the current tree (`check_repo.py` reports 0 violations). |
| `tools/check_repo.py` | ~322-328 | Module docstring still describes `skill-token-budget-exceeded` as an open, currently-firing finding against the real `SKILL.md`; it has been silent since Phase 2 (WINDOWS.md entry 5, `status: fixed`). Stale prose, confirmed present. | ℹ️ Info | Prose-only, no CI/behavior impact; flagged by 03-REVIEW.md as IN-01, unresolved. |

No debt markers (`TBD`/`FIXME`/`XXX`) found in any file this round's plans touched. Beyond the four
review-sourced findings above (all independently confirmed still present in this session), no new stub
patterns or hardcoded-empty-data patterns found in the modified reference/skill files.

**Carried forward from the prior VERIFICATION.md (now resolved, kept for history):**
- CR-01 (unanchored `score_transcript()` family search) — fixed in 03-09, confirmed by direct read and re-run of both discrimination probes in this session.
- CR-02 (README's false "no measured claim" statement) — fixed in 03-10, confirmed by direct read in this session; guarded by the new `readme-results-pointer-missing` check.
- WR-01/old (a single timed-out session losing its own transcript) — fixed in 03-09, confirmed by direct read in this session (folded into the same commit that fixed CR-01/old).

## Human Verification Required

See the `human_verification` list in the frontmatter. In summary:

1. **An actual human** (not a subagent) still needs to perform the `SOURCES.md` paraphrase-boundary read for the MC bodies and the four artifact-family sections — explicitly deferred to Phase 6 LEG-04, not blocking this phase's status, unchanged this round.
2. **A policy call** on MOD-04's disposition beyond "waived, no further lever scheduled": three structurally distinct levers have now been tried and none reached the bar, and the anchored figures are markedly lower than every earlier unanchored figure for the same residual — meaning the earlier apparent progress (45.5% -> 60.0%) may have been largely or entirely a measurement artifact rather than real behavior change.

## Gaps Summary

**Gap 1 (carried forward, re-measured under an honest scorer for the first time, still open): MOD-04's live-session classify-before-rules ordering.** This round's four plans did real, disciplined work: 03-09 fixed the scorer bias that made every prior figure an optimistic ceiling; 03-10 fixed a false claim in README that this phase's own work had introduced; 03-11 built a genuinely different-in-kind lever (a mechanical self-check ordering re-scan, not another instruction restatement); 03-12 measured that lever under the fixed scorer with a disposition rule committed to git before any session ran, and applied it mechanically and honestly (naming a decline as a decline, not softening it to match the branch template's "did not move" label). The honest result is that the residual has not closed and shows no clear improvement — the anchored figures are the lowest and most trustworthy this phase has produced. This is not a deferred item: WINDOWS.md entry 8 has no later-phase owner, and it is now `waived` rather than `open`, which correctly documents that the project has looked at the number and chosen to stop spending live-session budget on this specific class of lever, not that the requirement is met.

**Gap 2 (new this round): this phase's own code review found a genuine, currently-unresolved Critical defect in the measurement instrument that backs this phase's headline claim** — `run_conformance.py` can silently lose an entire batch of already-scored sessions on an ordinary interruption between sessions, a failure mode the project's own file already documents having happened twice and worked around operationally rather than in code. Two lower-severity, also-unresolved findings (an itemization arithmetic mismatch in `RESULTS-mod04.md`'s own prose, and a case-sensitivity inconsistency between two sibling checker functions) round out the review. None of these three findings invalidate the specific 30.0%/40.0% figures 03-12 produced (which used the durable one-invocation-per-session workaround throughout, verified via 23 individually committed run blocks), but they are real, disclosed-by-review, currently-unaddressed defects in artifacts this phase committed, and the project's own "measured claims or no claims" standard applies to its own instruments, not only to its headline prose.

The phase is **not** ready for `passed`. Requirement MOD-04's one remaining truth (live-session classify-before-rules ordering) has now been measured honestly and clearly fails the bar, with no evidence the residual is shrinking — if anything the most trustworthy measurement to date is the lowest one recorded. Separately, this phase's own most recent code review surfaced one Critical and two Warning findings against artifacts this phase committed, none yet fixed. The path forward is either: (a) a genuinely different class of lever for MOD-04 (03-12's own SUMMARY names a post-generation mechanical repair as the next candidate, distinct from both instruction restatement and a model-performed self-check) plus a small gap-closure plan fixing the review's three new findings, or (b) an explicit, disclosed human decision that both residuals (the MOD-04 rate, and the instrument's inter-session data-loss exposure) are acceptable for v1 as currently documented.

---

*Verified: 2026-09-16T09:37:32Z*
*Verifier: Claude (gsd-verifier)*
