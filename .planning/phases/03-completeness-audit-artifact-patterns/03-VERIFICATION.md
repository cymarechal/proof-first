---
phase: 03-completeness-audit-artifact-patterns
verified: 2026-09-16T20:15:00Z
status: gaps_found
score: "9/10 truths verified, 1 failed, 0 present-behavior-unverified"
behavior_unverified: 0
overrides_applied: 1
overrides:
  - must_have: "(SC3, live half) A live write-mode session actually classifies the artifact family before applying any rule, in every session"
    reason: "Four measurement rounds across three structurally distinct levers (03-05 instruction restatement, 03-07 unconditional family line + presence gate, 03-11 self-check ordering re-scan) all landed under the pre-committed 87.5% closure bar. The only anchored (non-inflated) measurement is the lowest recorded (30.0%, 3/10) and a 10-point decline against its own paired same-instrument baseline (40.0%, 4/10). The project owner — a human, not the executing agent — was shown all three disposition options with full pros/cons in an interactive /gsd-execute-phase 03 --gaps-only session and explicitly chose Option A: accept the measured residual for v1 and publish it rather than pursue a fourth lever or re-scope the project to permit a harness-specific runtime component (architecturally foreclosed for an Agent Skill under the zero-dependency and cross-harness-portability constraints). The decision is dated, attributed, evidenced, and reversible (recorded in evals/conformance/RESULTS-mod04.md '## v1 disposition decision (03-15)', WINDOWS.md entry 8 (waived, not fixed), REQUIREMENTS.md's MOD-04 annotation, and 03-UAT.md gap G-03-2 — all five records agree). MOD-04's requirement checkbox correctly stays unchecked and README publishes the unfavorable number in its own prose, not merely a pointer, satisfying this project's own 'measured claims or no claims' standard applied honestly to an unflattering result. This is publication of a disclosed limitation, not a claim of satisfaction."
    accepted_by: "project owner (human), in an interactive /gsd-execute-phase 03 --gaps-only session — per the documented provenance in evals/conformance/RESULTS-mod04.md section '## v1 disposition decision (03-15)'"
    accepted_at: "2026-09-16"
re_verification:
  previous_status: gaps_found
  previous_score: "8/10 truths verified, 2 failed, 0 present-behavior-unverified"
  gaps_closed:
    - "Gap 1 (MOD-04 live-session residual) — disposed, not fixed, via an explicit human decision (03-15). The prior verification's second `missing` item ('an explicit, human-made decision... that the write-mode classify-before-rules ordering is acceptable at a ~30-40% observed rate for v1') is exactly what 03-15's checkpoint:decision task produced: dated, attributed to the actual project owner (not the executing agent), evidenced against the four-round measurement history, with named rejected alternatives and a stated reopening condition. Verified present and consistent across all five tracking records (RESULTS-mod04.md, WINDOWS.md entry 8, README.md, REQUIREMENTS.md, 03-UAT.md G-03-2) by direct read in this session. Recorded as an accepted override rather than a satisfied requirement — MOD-04 stays unchecked."
    - "Gap 2, first half (whole-run in-memory batching / data-loss-on-interruption) — genuinely closed. Direct read of evals/conformance/run_conformance.py confirms `run_matrix()`/`_write_result_line()` write and flush every session's result line to disk the moment it is scored; no in-memory `lines` accumulator remains in `main()` or `run_matrix()`. `git diff 5346c19..HEAD -- evals/conformance/run_conformance.py` (re-run in this session) confirms the refactor is scoped exactly as claimed, touching neither `score_transcript()` nor `run_session()`'s TimeoutExpired handling."
    - "Gap 2, second half (Arm A no-family enumeration naming 6 sessions against a stated count of 7) — genuinely closed. RESULTS-mod04.md's Arm A no-family bullet now enumerates all 7 sessions including the previously-omitted B-proposal-section first attempt; independently summed against the parenthetical in this session, matches. A new discrimination-proven check_repo.py code (`results-breakdown-count-mismatch`, the 32nd code) now holds this defect class mechanically."
    - "Two lower-severity findings from the fresh 03-REVIEW.md (WR-02: case-sensitivity asymmetry between the two family-gate checks; IN-01: stale skill-token-budget-exceeded docstring) — both genuinely closed by 03-14, confirmed by direct read and by the mutation-test's new `family_capitalized_root` fixture."
  gaps_remaining: []
  regressions: []
gaps:
  - truth: "The project's own 'measured claims or no claims' reproducibility constraint holds for the instrument that produced this phase's headline MOD-04 measurement — including the instrument's own regression guard against the exact data-loss defect this phase already found and fixed once"
    status: failed
    reason: "03-REVIEW.md's fresh review (completed after 03-15 landed, the newest commit at HEAD) found a new, previously-undiscovered Critical defect in this round's own added code, and I independently reproduced it in this session rather than taking the review's word for it. Self-test behavior case 11 (evals/conformance/run_conformance.py:612-668) is supposed to prove offline that `_write_result_line()`'s `handle.flush()` call makes each scored session durable against a process interruption between sessions. It does not: the test's `try/except KeyboardInterrupt` sits INSIDE the `with open(fake_results_path_11, 'a') as fake_handle_11:` block, so the KeyboardInterrupt is fully handled before the `with` block exits, and the `with` block's own normal-exit `close()` flushes the file regardless of whether `_write_result_line()` ever calls `.flush()` itself. I verified this empirically in this session: copying `run_conformance.py` to a sibling path inside `evals/conformance/` (to preserve `REPO_ROOT` resolution), removing the `handle.flush()` line from `_write_result_line()`, and re-running `--self-test` still printed `self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable` with no FAIL line — reproducing the review's exact finding independently. The production code is correct today (`.flush()` is present at evals/conformance/run_conformance.py:729), and the underlying data-loss defect this phase already suffered twice is genuinely fixed in the shipped script. What is false is the verification-integrity claim: the module docstring (line 36) states the durability guarantee is 'proved offline by `--self-test` behavior case 11', and evals/conformance/RESULTS-mod04.md's own '## Instrument durability fix (03-13)' section repeats the same claim ('A new offline self-test behavior case (case 11) proves this'). Neither statement is true — case 11 would pass identically with the flush call deleted, meaning a future silent regression of the exact bug that has already destroyed two real measurement runs would ship with a green self-test and a green CI. This is precisely the failure mode this project's own mutation-testing preamble in tools/check_repo.py names as the thing it exists to prevent ('a dead check ship[ping] named as covered'), reproduced here in the sibling instrument's self-test rather than in check_repo.py itself. No commit at HEAD (d144f91) addresses this — 03-REVIEW.md discovered it after 03-13/03-14 landed, and 03-15 was scoped only to MOD-04's disposition decision, not to this finding."
    artifacts:
      - path: "evals/conformance/run_conformance.py"
        issue: "Lines 612-668 (self-test case 11) do not discriminate the presence of `_write_result_line()`'s `.flush()` call from its absence, because the interrupting `KeyboardInterrupt` is caught inside the `with open(...) as fake_handle_11:` block rather than propagating past it. Lines 34-37 (module docstring) assert the durability guarantee is 'proved offline by --self-test behavior case 11', which is not true of the current test."
      - path: "evals/conformance/RESULTS-mod04.md"
        issue: "Lines ~840-861 ('## Instrument durability fix (03-13)') repeat the same overclaim — 'A new offline self-test behavior case (case 11) proves this' — about a test that does not prove it."
    missing:
      - "Rewrite case 11 to assert the actual write/flush discipline against a call-recording stub (e.g. a thin handle proxy that records write()/flush() call order), independent of whatever the `with` block's own close()-on-exit does — so the test fails the moment `.flush()` is removed from `_write_result_line()`, regardless of which exception type interrupts the run. 03-REVIEW.md's Fix section gives a concrete `_FlushTrackingHandle` implementation."
      - "Correct the two overclaiming statements (run_conformance.py's module docstring line 36, and RESULTS-mod04.md's '## Instrument durability fix (03-13)' section) once the test genuinely discriminates the property, or soften them in the interim to state what case 11 actually proves (that the interrupted portion of a matrix is not silently lost when the interrupting exception unwinds through the open file's own context manager) rather than what it does not (that the explicit .flush() call itself is load-bearing)."
human_verification: []
---

# Phase 3: Completeness Audit & Artifact Patterns Verification Report

**Phase Goal:** A writer can classify a document by artifact family, apply that family's conventions, and get a document-level completeness verdict and trustworthy rule citations — independent of the prose rules.
**Verified:** 2026-09-16T20:15:00Z
**Status:** gaps_found
**Re-verification:** Yes — fifth round. Plans 03-13, 03-14, 03-15 closed the prior round's two gaps: the instrument's whole-run data-loss defect and enumeration error (03-13/03-14), and MOD-04's disposition, elevated from a branch-table default to an explicit, dated, human-attributed decision (03-15). A fresh code review (03-REVIEW.md, the latest commit at HEAD) confirmed all four prior review findings genuinely closed but surfaced one new, previously-undiscovered Critical in this round's own added code — independently reproduced in this session, not taken on the review's word.

## Project Gate (independently re-run, not taken on trust)

```
$ python3 tools/check_repo.py --self-test
self-test PASS - verified violation codes: artifact-family-section-missing, catalog-count-mismatch,
catalog-count-unstated, catalog-id-drift, catalog-opening-rule-count, dup-figure-key, dup-id,
figure-order, framework-statement-missing, frontmatter-description-invalid, frontmatter-name-mismatch,
frontmatter-unknown-key, frontmatter-unparseable, license-missing, mc-catalog-id-drift,
mc-count-mismatch, mc-count-unstated, mc-rule-in-skill, pointer-duplicated, pointer-missing,
pointer-unparseable, range-id, readme-results-pointer-missing, results-breakdown-count-mismatch,
revived-id, skill-family-line-gate-missing, skill-family-order-gate-missing,
skill-token-budget-exceeded, skill-too-long, source-label-in-skill-content, undefined-id,
unlisted-figure
(32 codes)

$ python3 tools/check_repo.py --mutation-test
mutation-test PASS: 32 codes discrimination-proven
(exit 0)

$ python3 tools/check_repo.py
check_repo: 0 violations
(exit 0)

$ python3 evals/conformance/run_conformance.py --self-test
self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable
(exit 0)
```

All four commands re-run fresh in this session. All exit 0, and the code count (32, unchanged from
the prior round, which already reflected `results-breakdown-count-mismatch` added by 03-14) matches
every claim in 03-13/03-14/03-15's SUMMARYs exactly.

**Independent reproduction of 03-REVIEW.md's new Critical.** Copied `run_conformance.py` to a sibling
path inside `evals/conformance/` (preserving `REPO_ROOT = Path(__file__).resolve().parents[2]`
resolution), removed the `handle.flush()` line from `_write_result_line()`, and re-ran `--self-test`:

```
$ python3 evals/conformance/_noflush_test.py --self-test
self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable
```

No FAIL line, including for case 11 — confirming the review's finding that case 11 does not
discriminate the presence of `.flush()` from its absence. Test file deleted after the probe (never
committed).

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | (SC1, structural) MC namespace/registry never blended into prose rules | ✓ VERIFIED | Regression-confirmed: 8 `### MC-` headings in `completeness-audit.md`; `mc-rule-in-skill` still discrimination-proven in this session's mutation-test re-run. Unchanged this round — no plan in this round touched `completeness-audit.md`. |
| 2 | (SC1, live half / AUD-03) Standalone audit returns a separate verdict, independent of prose rules | ✓ VERIFIED (with a disclosed caveat, carried forward) | Unchanged this round: 6/6 clean UAT sessions (03-UAT.md test 1), untouched by 03-13/14/15. |
| 3 | (SC2, structural) Four artifact families each get distinct conventions and expected order | ✓ VERIFIED | Regression-confirmed: 4 family `## ` headings, distinct `**Order:**` lines, `artifact-family-section-missing` still discrimination-proven. Content-quality half (ART-01..04) remains open — see Deferred. |
| 4 | (SC3, structural / MOD-04) Classification instruction exists in both modes, states the ordering explicitly, and is mechanically gated on BOTH presence and ordering | ✓ VERIFIED | Unchanged this round: `SKILL.md`'s self-check first pass, `skill-family-line-gate-missing` and `skill-family-order-gate-missing` both discrimination-proven in this session's mutation-test re-run (32/32). No plan this round touched `SKILL.md`. |
| 5 | (SC3, live half) A live session actually classifies before applying any rule, in every session | **PASSED (override)** | See `overrides` in frontmatter. Measured four times across three structurally distinct levers; the only anchored measurement is 3/10 (30.0%), a decline against its paired 4/10 (40.0%) baseline. 03-15 elevated this from an unowned branch-table default to an explicit, dated (2026-09-16), human-attributed (the project owner, not the executing agent) accept-and-disclose decision, evidenced against the full measurement history and propagated identically across five tracking records — independently confirmed consistent in this session by direct read of all five. `MOD-04` correctly stays `[ ]`; `README.md` publishes 30.0%/40.0% in its own prose, not merely a pointer. |
| 6 | (SC4, structural / MOD-03) Four labeled sections in fixed order, correct lead-in wording | ✓ VERIFIED | Unchanged this round: `SKILL.md`'s four-section wording untouched by any plan this round. |
| 7 | (SC4, live half / MOD-03) A live check-mode session prints all four sections, in order, with no-findings lines | ✓ VERIFIED | Unchanged this round: 03-UAT.md test 3, 9/9 live sessions. No regression evidence found. |
| 8 | (SC5, shipped-file half / MOD-05) Check mode never cites an unallocated rule number | ✓ VERIFIED | Regression-confirmed: `undefined-id`, `mc-catalog-id-drift`, `mc-count-unstated`/`mc-count-mismatch` all still discrimination-proven (32/32). |
| 9 | (SC5, live-session half / MOD-05) A live conversation never fabricates a rule number | ✓ VERIFIED | Unchanged this round: 03-UAT.md test 4, 18/18 sessions, 224 distinct citations, zero unallocated IDs. |
| 10 | The project's own "measured claims or no claims" reproducibility constraint holds for the instrument backing this phase's headline measurement, including its own regression guard against the data-loss defect this same instrument already suffered twice | ✗ **FAILED** | The prior round's specific failure (whole-run in-memory batching) is genuinely fixed and verified by direct code read — `run_matrix()`/`_write_result_line()` write-and-flush per session, no accumulator remains. But 03-REVIEW.md's fresh review found, and I independently reproduced in this session, that the offline self-test case (case 11) written specifically to prove this durability property does not actually discriminate it: removing the `.flush()` call from a copy of `_write_result_line()` still produces a clean `--self-test PASS`, because the test's `KeyboardInterrupt` is caught inside the same `with` block whose own close()-on-exit would flush the file regardless. The module docstring's claim ("proved offline by `--self-test` behavior case 11") and `RESULTS-mod04.md`'s identical claim in its `## Instrument durability fix (03-13)` section are both currently false. Not addressed by any commit at HEAD. |

**Score:** 9/10 truths verified (including 1 accepted override), 1 FAILED, 0 present-behavior-unverified.
Truth 5, which failed in the prior three verification rounds, is now disposed via an explicit,
evidenced, reversible human decision rather than left as an open branch-table consequence — this
verifier treats that disposition as satisfying the phase's evidentiary bar for this truth, without
treating it as a satisfied requirement (`MOD-04` stays unchecked; see the override entry for the full
reasoning). Truth 10 is a narrower but genuine reopening of the same class of concern the prior round's
Truth 10 raised: the specific data-loss defect is fixed, but the new regression guard built to prove it
does not prove it, and two shipped documents currently overclaim that it does. This is a new,
previously-undiscovered defect in this round's own added code (case 11 did not exist before 03-13),
not a recurrence of the closed CR-01.

### Deferred Items

| # | Item | Addressed In | Evidence |
|---|------|-------------|----------|
| 1 | AUD-01 — independent human paraphrase-boundary read of the MC dimension bodies | Phase 6 | ROADMAP.md Phase 6 Success Criterion 1 (MEDDIC-family trademark reconfirmation); WINDOWS.md entries 3, 6. Untouched this round (confirmed by direct grep: still `[ ]`, unchanged since prior round). |
| 2 | ART-01..04 — independent human paraphrase-boundary read of the four artifact-family sections | Phase 6 | WINDOWS.md entry 9's closure note routes the human-provenance judgment to Phase 6 LEG-04. Untouched this round. |

### Required Artifacts (regression + new-this-round check)

| Artifact | Status | Details |
|---|---|---|
| `skills/proof-first/references/completeness-audit.md` | ✓ VERIFIED | Unchanged this round; 8 MC headings confirmed, untouched by any of 03-13/14/15. |
| `skills/proof-first/references/artifact-patterns.md` | ✓ VERIFIED | Unchanged this round; 4 family headings confirmed, no frozen source label. |
| `skills/proof-first/SKILL.md` | ✓ VERIFIED | Unchanged this round; 32/32 checks intact, self-check carries both presence and ordering passes. |
| `tools/check_repo.py` | ✓ VERIFIED | 32/32 codes discrimination-proven, confirmed by independent `--mutation-test` re-run. `results-breakdown-count-mismatch` (new in 03-14) confirmed firing correctly on its registered mutation. |
| `evals/conformance/run_conformance.py` | ⚠️ VERIFIED-WITH-DEFECT | `--self-test` passes; the prior round's whole-run batching defect (CR-01, from the fresh review) is genuinely fixed, confirmed by direct source read. A NEW, currently-unresolved defect found by this round's own 03-REVIEW.md and independently reproduced in this session: self-test case 11, added specifically to prove the durability fix, does not discriminate `.flush()`'s presence from its absence, and the module docstring overclaims that it does. |
| `evals/conformance/RESULTS-mod04.md` | ⚠️ VERIFIED-WITH-DEFECT | `## Instrument durability fix (03-13)` and `## v1 disposition decision (03-15)` both present and correctly ordered after `## Anchored remeasurement result (03-12)`. Arm A `no-family` enumeration now correctly names all 7 sessions (confirmed by direct read). The durability-fix section repeats the same "proves this" overclaim found in the source file's docstring. |
| `.planning/REQUIREMENTS.md` | ✓ VERIFIED | Checkbox states correct: `AUD-01`, `ART-01..04`, `MOD-03..05`, `AUD-02`, `AUD-03` all `[ ]` — unchanged by this round's plans by design (03-15's own prohibitions forbid touching them; re-marking clean-verified requirements is this verifier's task only when the whole phase verifies clean, which it does not this round because of Truth 10). `grep -c "^- \[x\].*UNVERIFIED"` returns 0. `MOD-04`'s annotation now carries the 03-15 decision, its provenance, and a pointer to the new results-file section. |
| `.planning/WINDOWS.md` | ✓ VERIFIED | Entries 3, 6 remain `open` (correctly, Phase 6-owned). Entries 5, 7, 9 remain `fixed`. Entry 8 remains `waived`, its `reason` field extended with the 03-15 decision and its provenance — confirmed by direct JSON parse in this session, parses cleanly. No WINDOWS.md entry exists yet for the new self-test non-discrimination defect (Truth 10) — it is untracked in the ledger and unaddressed by any commit. |
| `README.md` | ✓ VERIFIED | Status section confirmed by direct read: publishes `3 of 10 scoreable claude-sonnet-5 sessions (30.0%)` against the paired `4 of 10 (40.0%)` baseline in its own prose, dated, framed as a disclosed v1 limitation, keeps the literal `evals/conformance/RESULTS-mod04.md` pointer and all three prescribed caveats. |

### Requirements Coverage

| Requirement | Status | Evidence |
|---|---|---|
| AUD-01 | ? NEEDS HUMAN — correctly `[ ]` | Unchanged this round; deferred to Phase 6 LEG-04. |
| AUD-02 | ✓ SATISFIED — `[ ]` (checkbox re-marking withheld this round; see below) | Mechanically enforced, unchanged. |
| AUD-03 | ✓ SATISFIED (with caveat) — `[ ]` (checkbox re-marking withheld this round; see below) | Unchanged this round. |
| ART-01..04 | ? NEEDS HUMAN — correctly `[ ]` | Structurally implemented and mechanically enforced; content-quality/paraphrase read still deferred to Phase 6 LEG-04. |
| MOD-03 | ✓ SATISFIED — `[ ]` (checkbox re-marking withheld this round; see below) | Unchanged this round. |
| MOD-04 | ✗ **BLOCKED (accepted v1 residual, override applied to phase Truth 5)** — correctly `[ ]` | Now explicitly disposed as of 2026-09-16: an evidenced, attributed, reversible human decision to accept the measured residual and disclose it. Not a satisfied requirement — the checkbox correctly stays unchecked and the unfavorable figure is published in README. |
| MOD-05 | ✓ SATISFIED — `[ ]` (checkbox re-marking withheld this round; see below) | Unchanged this round. |

No requirement is ORPHANED. All ten requirement IDs (AUD-01..03, ART-01..04, MOD-03..05) declared
across the phase's 15 plans' frontmatter are accounted for above.

**On checkbox re-marking:** 03-15-PLAN.md's own must-haves state that AUD-02, AUD-03, MOD-03 and
MOD-05's re-marking to `[x]` "is the verifier's to do when the phase verifies clean." This phase does
not verify clean this round — Truth 10 is FAILED — so per that plan's own design, this verifier is
not re-marking any checkbox in this round. They remain individually SATISFIED in substance (see the
table above) but unchecked in `.planning/REQUIREMENTS.md` pending a round with no gaps.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| `evals/conformance/run_conformance.py` | 612-668, 34-37 | Self-test case 11 does not discriminate `_write_result_line()`'s `.flush()` call from its absence (confirmed by independent reproduction in this session); the module docstring overclaims that it does. | 🛑 Blocker (verification-integrity defect: a future silent regression of the exact data-loss bug that has already destroyed two real measurement runs would ship with a green self-test and green CI) | Does not affect the correctness of the currently-shipped `.flush()` call or any published figure (all of which used the durable, one-invocation-per-session workaround). Affects only the trustworthiness of the regression guard going forward. |
| `evals/conformance/RESULTS-mod04.md` | ~849-851 | `## Instrument durability fix (03-13)` repeats the same "case 11 proves this" overclaim found in the source docstring. | ⚠️ Warning | A committed, reader-facing measurement file stating an unproven verification claim as proven — the exact class of overclaim this project's "measured claims or no claims" standard exists to prevent, though narrower in stakes than a false headline number. |
| `README.md` | 53-56 | (Carried forward from 03-REVIEW.md IN-02, still present, not blocking) The 10-point decline is stated in full numeric form but the word "decline" itself never appears in this file's prose, unlike `RESULTS-mod04.md` and `WINDOWS.md` entry 8, which both use it. | ℹ️ Info | Both numbers (30.0%, 40.0%) are present and correctly attributed; a reader who does the arithmetic reaches the same conclusion. Purely a clarity nit, not a false or omitted claim. |

No debt markers (`TBD`/`FIXME`/`XXX`) found in any file this round's plans touched (checked directly
in this session: `run_conformance.py`, `RESULTS-mod04.md`, `WINDOWS.md`, `README.md`,
`REQUIREMENTS.md`, `check_repo.py`, `03-UAT.md`). Beyond the two findings above (independently
confirmed present in this session), no new stub patterns or hardcoded-empty-data patterns found.

**Carried forward from the prior VERIFICATION.md (now resolved, kept for history):**
- Whole-run in-memory batching (03-REVIEW.md's round-4 CR-01) — fixed in 03-13, confirmed by direct
  source read in this session (`run_matrix()`/`_write_result_line()` write-and-flush per session, no
  accumulator remains).
- Arm A `no-family` enumeration naming 6 sessions against a stated count of 7 (round-4 WR-01) — fixed
  in 03-13, confirmed by direct read; now mechanically held by `results-breakdown-count-mismatch`
  (03-14).
- Case-sensitivity asymmetry between the two family-gate checks (round-4 WR-02) — fixed in 03-14,
  confirmed by the new `family_capitalized_root` self-test fixture.
- Stale `skill-token-budget-exceeded` docstring (round-4 IN-01) — fixed in 03-14, confirmed by direct
  read (`grep -c 'silent against the current tree'` returns 1).
- MOD-04's disposition as an unowned branch-table consequence (round-4's second gap's `missing` item)
  — resolved in 03-15 via an explicit, dated, human-attributed decision; recorded above as an accepted
  override on phase Truth 5.

## Human Verification Required

None new this round. The two Phase-6-deferred items (AUD-01, ART-01..04's paraphrase-boundary reads)
remain open and unchanged; see Deferred Items above. Truth 10's gap is a mechanically confirmed code
defect (independently reproduced in this session), not a judgment call requiring a human — it routes
to `gaps_found`, not `human_needed`.

## Gaps Summary

**The prior round's two gaps are both genuinely closed, in different ways.** Gap 1 (MOD-04's
unowned disposition) is now an explicit, dated, evidenced, reversible human decision — this verifier
records it as an accepted override on phase Truth 5 rather than as an unresolved failure, because the
project's own escalation path (a `checkpoint:decision` task, not the executing agent) was followed
correctly and the outcome is honestly disclosed rather than hidden or softened. Gap 2's headline defect
(whole-run in-memory batching, silently losing every already-scored session on an inter-session
interruption) is genuinely fixed, verified by direct code read: `run_matrix()`/`_write_result_line()`
write and flush every session's result line the instant it is scored.

**A new gap opened by this round's own added code.** 03-REVIEW.md's fresh review — the newest commit
at HEAD, run after 03-13/03-14/03-15 all landed — found, and I independently reproduced in this
session (removing the `.flush()` call from a copy of `_write_result_line()` and confirming
`--self-test` still passes cleanly), that self-test behavior case 11 does not actually discriminate
the durability property it was written to prove: the interrupting `KeyboardInterrupt` is caught inside
the same `with` block whose own close()-on-exit flushes the file regardless of whether
`_write_result_line()`'s explicit `.flush()` call exists at all. Two committed documents
(`run_conformance.py`'s module docstring and `RESULTS-mod04.md`'s `## Instrument durability fix
(03-13)` section) currently state, incorrectly, that case 11 proves this. The production code is not
defective — the `.flush()` call is present and does genuine work against a real process kill, which I
did not need to re-verify given 03-REVIEW.md's own direct SIGKILL test — but the regression guard
protecting it is not real, meaning a future silent deletion of that one line would ship with a green
CI, reproducing the exact class of loss this project has already suffered twice. This is a
verification-integrity defect of the kind this project's own mutation-testing preamble names as the
thing it exists to prevent, found here in a sibling instrument's self-test rather than in
`check_repo.py` itself.

**This gap is narrow in scope and does not touch the writer-facing artifacts this phase's goal is
about** (`SKILL.md`, `completeness-audit.md`, `artifact-patterns.md` are all untouched this round and
remain fully verified). It is, however, a live, currently-shipped false claim in a committed file this
project holds up as the reproducible evidentiary backing for its one measured MOD-04 figure, and this
project's own governing constraint treats an overstated claim as a first-class defect regardless of
where it appears. The path forward is narrow: rewrite case 11 against a call-recording stub (a concrete
implementation is already given in `03-REVIEW.md`'s own Fix section) so it fails the moment `.flush()`
is removed, and correct or soften the two overclaiming sentences once it does.

---

*Verified: 2026-09-16T20:15:00Z*
*Verifier: Claude (gsd-verifier)*
