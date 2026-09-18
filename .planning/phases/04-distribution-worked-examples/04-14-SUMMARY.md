---
phase: 04-distribution-worked-examples
plan: 14
subsystem: docs
tags: [readme, ledger, check-repo, examples, gap-closure]

requires:
  - phase: 04-distribution-worked-examples
    provides: "04-13's README repair, which introduced G-04-8's over-broad universal negative"
provides:
  - "README.md:83 narrowed from a universal negative ('this repository's own environment drives no live harness session') to a correctly-scoped disclosure (the /config listing specifically is unobserved because headless claude -p sessions have no picker)"
  - "Three folded-in README credibility defects fixed: the four-install-route intro no longer claims one-per-harness-class, the routes-3-and-4 clone gap is now stated rather than silent, and Status's orphaned 'At minimum:' fragment has an antecedent"
  - "examples/before-after.md's Executive summary sentence 3 rewritten to state migration scope the deal brief supports, instead of an unevidenced delivered-outcome claim"
  - ".planning/WINDOWS.md entry 16 corrected in both its rendered row and its fenced JSON to the same narrowed scope, proven in agreement by a subsequent append that raised no table-drift error"
  - "A written mechanisability refusal (no new violation code) recorded in tools/check_repo.py's module docstring and as ledger entry 17"
affects: [phase-06-legal-review]

actuals:
  tokens: 4204
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns: []

key-files:
  created: []
  modified:
    - README.md
    - .planning/WINDOWS.md
    - tools/check_repo.py
    - examples/before-after.md

key-decisions:
  - "No new violation code registered for cross-sentence self-contradiction (G-04-8's 'missing' item 2). Refused, not deferred: two rejected proxy designs (exact-phrasing blocklist, broad negative-existential regex) and a measured-but-refused narrow presence code are all recorded in tools/check_repo.py's docstring and WINDOWS.md entry 17."
  - "Task 1's tracer feedback gate (human-check: cold re-read of Install and Status) was resolved autonomously in this spawned session, consistent with this project's 03-01/03-02 precedent for tracer/human-check gates when no interactive human is present — workflow.auto_advance and workflow._auto_chain_active are both false, but no human is attached to this run to answer a mid-flight checkpoint."

requirements-completed: []

coverage:
  - id: D1
    description: "README.md:83's false universal negative narrowed to the interactive-only case, naming the headless claude -p mechanism the repository actually drives"
    requirement: DIST-06
    verification:
      - kind: other
        ref: "grep -cF 'drives no live harness session' README.md == 0; grep -cF 'claude -p' README.md >= 1; check_repo.py: 0 violations"
        status: pass
    human_judgment: true
    rationale: "Whether the corrected sentence and the surrounding page genuinely no longer contradict each other is the plan's verification:backstop truth #1 — semantic judgment no code performs."
  - id: D2
    description: ".planning/WINDOWS.md entry 16 corrected in both the rendered table row and the fenced JSON to the same narrowed scope"
    verification:
      - kind: other
        ref: "grep -cF 'drives no live harness session' .planning/WINDOWS.md == 0; gsd-tools windows append (entry 17) succeeded with no table-drift error"
        status: pass
    human_judgment: false
  - id: D3
    description: "Mechanisability refusal for cross-sentence self-contradiction recorded in tools/check_repo.py's module docstring and as ledger entry 17; no new violation code registered"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test -> 'mutation-test PASS: 48 codes discrimination-proven'; docstring contains 'same document'"
        status: pass
    human_judgment: false
  - id: D4
    description: "Three folded-in README prose defects fixed (harness-class-claim intro, routes-3/4 clone gap, orphaned 'At minimum:' fragment); ## Status otherwise byte-unchanged"
    verification:
      - kind: other
        ref: "grep -cF 'one per harness class' README.md == 0; grep -n '^At minimum:' README.md matches nothing; git diff --stat over skills/output-styles/prompts/.claude-plugin/examples is empty"
        status: pass
    human_judgment: false
  - id: D5
    description: "examples/before-after.md's Executive summary sentence 3 rewritten from an unevidenced delivered-outcome claim to migration scope the canonical deal brief supports"
    requirement: EX-02
    verification:
      - kind: other
        ref: "grep -cF 'delivers automated failover' examples/before-after.md == 0; sentence word-count probe: 24 words; --mutation-test 48 codes; git diff -U0 shows one line removed, one line added"
        status: pass
    human_judgment: true
    rationale: "Whether every named item in the rewritten sentence is genuinely supported by a stated deal-brief pain point is the plan's verification:backstop truth #2 — evidential sufficiency of a prose claim is semantic, not code-checkable."

patterns-established: []

duration: 25min
completed: 2026-09-18
status: complete
---

# Phase 4 Plan 14: G-04-8 Gap Closure — Corrected Universal Negative, Fixed Ledger Copy, Refused a Non-Mechanisable Code Summary

**Narrowed README's over-broad "drives no live harness session" claim to the true, correctly-scoped disclosure; fixed the verbatim copy of the same false clause in the WINDOWS.md ledger; recorded a written refusal to register a check for cross-sentence self-contradiction; and removed an unevidenced deliverable claim from the Executive summary worked example.**

## Performance

- **Duration:** 25 min
- **Started:** 2026-09-18T07:20:00Z
- **Completed:** 2026-09-18T07:45:00Z
- **Tasks:** 3
- **Files modified:** 4

## Accomplishments

- Closed G-04-8: README.md:83 no longer asserts, as fact, something the same page disproves at lines 111-113 and 134-137.
- Fixed the verbatim copy of the same false clause living in `.planning/WINDOWS.md` entry 16 (both the rendered table row and the fenced JSON), proven in agreement by a subsequent `windows append` that did not raise a table-drift error.
- Recorded a deliberate, reasoned refusal to register a 49th violation code for cross-sentence self-contradiction, in `tools/check_repo.py`'s own module docstring and as ledger entry 17 — the mutation-test still proves exactly 48 discrimination-proven codes.
- Folded in three cheap README credibility defects from the same round-2 cold read (the four-route "one per harness class" mis-description, the silent routes-3/4 clone-URL gap, and Status's orphaned "At minimum:" fragment).
- Removed an unevidenced deliverable claim from `examples/before-after.md`'s Executive summary ✓ column, replacing it with scope the canonical deal brief actually supports.

## Task Commits

Each task was committed atomically:

1. **Task 1: Narrow README's false universal negative, and fold in three prose defects** - `4bf1277` (fix)
2. **Task 2: Correct the ledger's copy of the false sentence, and write down the mechanisability refusal** - `d6f0112` (docs)
3. **Task 3: Remove the unevidenced deliverable claim from the Executive summary example** - `a28cada` (fix)

_Note: this plan is not `type: tdd`; no test/feat/refactor gate sequence applies._

## Files Created/Modified

- `README.md` — Edit A (line 83, the gap itself), Edit B (line 36, four-route intro), Edit C (clone-URL gap for routes 3/4), Edit D (line 149, orphaned fragment antecedent)
- `.planning/WINDOWS.md` — entry 16 corrected in both the rendered row and the fenced JSON; entry 17 appended recording the mechanisability refusal
- `tools/check_repo.py` — module docstring extended with the non-coverage disclosure for cross-sentence self-contradiction; no violation code added
- `examples/before-after.md` — line 27, Executive summary ✓ column, third sentence replaced

## Before/After Text

### README.md:83 (Task 1, Edit A)

**Before:**
> That a Claude Code session then lists it in `/config` has not been observed here: this repository's own environment drives no live harness session.

**After:**
> That a Claude Code session then lists it in `/config` has not been observed here. This repository does drive live sessions — `evals/conformance/run_conformance.py` runs headless `claude -p`, and the conformance figure under `## Status` comes from those sessions — but a headless session has no `/config` picker, so the picker is the one link in this route nothing here exercises.

### `.planning/WINDOWS.md` entry 16, final clause (Task 2, Part 1)

**Before (both the rendered table row and the fenced JSON, verbatim identical):**
> What remains unobserved is the last link in the chain: a live Claude Code session listing the copied style in /config and applying it, because this repository's own environment drives no live harness session.

**After (both copies, verbatim identical):**
> What remains unobserved is the last link in the chain: a live Claude Code session listing the copied style in /config and applying it — this repository's live sessions are headless claude -p runs (evals/conformance/run_conformance.py), which have no /config picker to observe.

The `windows append` call that recorded entry 17 (Task 2, Part 2) succeeded without raising a table-drift error, which is the tool's own proof that entry 16's rendered row and fenced JSON agree.

### `examples/before-after.md:27`, Executive summary ✓ column, third sentence (Task 3)

**Before:**
> The migration delivers automated failover, Oracle Database licensing relief, and a landing zone the team can govern.

**After:**
> The proposed migration targets the pains Halverton Mutual named: manual failover across the estate, rising Oracle Database licensing cost, and no governable landing zone.

**Traceability to `examples/deal-brief.md`:**

| Named item in the rewritten sentence | Supported by |
|---|---|
| manual failover across the estate | `examples/deal-brief.md:37` — "Failover across the 850-VM estate is a manual process, which extends incident response time whenever a host fails." |
| rising Oracle Database licensing cost | `examples/deal-brief.md:35` — "Oracle Database licensing costs are an increasing share of the estate's current annual run rate, with no ceiling in sight under the existing on-premises model." |
| no governable landing zone | `examples/deal-brief.md:27` — "Marcus Feld — Vice President of Infrastructure, the champion. Cares about a governable landing zone and an end to manual failover." and `:70` — Marcus Feld's discovery-call quote, "We need a landing zone we can actually govern — right now every VM is a snowflake." |

The first two sentences of the ✓ column (carrying PF-2.11's GAP marker, PF-0.1's buyer-first opening, and PF-1.25's named economic buyer with her own stated measures) were left untouched, as were the ✗ line and the `Rules applied:` footer.

## Mechanisability Assessment (Task 2, Part 3)

Recorded verbatim (condensed form) in `tools/check_repo.py`'s module docstring, alongside the existing paraphrase-judgement limit, and in full in `.planning/WINDOWS.md` entry 17.

**The defect class:** a contradiction between two assertions roughly fifty lines apart in the same document. Detecting it requires deciding that two independently-phrased passages refer to the same thing and conflict — that is entailment, not pattern matching, and nothing in this stdlib-only stack performs it.

**Two proxy designs considered and rejected:**

1. **An exact-phrasing blocklist** of the sentences this round removes. Rejected because it would prove only that *these specific sentences* did not come back — the instance, not the class. This is the same overstatement CR-01 already closed once.
2. **A broad negative-existential regex** over README prose (e.g., flagging any "drives no X" / "has never Y" construction). Rejected because it would be a hard build-failure gate resting on a fuzzy proxy — every code in this file fails the build, and a false-positive-prone gate on legitimate future disclosure prose would trade one credibility failure for another.

**A narrow presence code was measured, not waved away, and still refused.** Requiring `README.md` to name the headless mechanism (`claude -p`) would be red before this plan and green after — a genuine red-then-green result that meets this repository's own evidence bar. It is refused anyway, on a ground that distinguishes it from the code 04-13 registered (`readme-output-style-destination-missing`): that code's guarded string carries independent reader value, because a route missing its destination directory is genuinely unexecutable. A token merely naming the headless mechanism carries no such value — its only function would be to gesture at this specific correction, and its presence cannot distinguish a correctly scoped disclosure from an over-broad one that happens to mention the mechanism elsewhere on the page.

**No code registered.** `python3 tools/check_repo.py --mutation-test` reports `mutation-test PASS: 48 codes discrimination-proven` — the same 48 as before this plan.

## Verification: Backstop Truths (restated verbatim)

These are the plan's `must_haves.truths` entries carrying `verification: backstop` — semantic judgments this repository's checker does not and cannot perform, restated here verbatim for the phase's end-of-phase verification step:

1. > A cold reader of `README.md` finds no two sentences on the page that contradict each other. No code in this repository performs that judgement, and Task 2 records why rather than pretending otherwise.

2. > A technical evaluator reading the Executive summary ✓ column finds no claim about what the migration delivers that `examples/deal-brief.md` does not support. Evidential sufficiency of a prose claim is semantic; no code in this repository judges it.

## Deviations from Plan

None — plan executed exactly as written. The Edit D wording ("Among those caveats, at minimum:") is the executor's own choice within the plan's stated constraint (smallest possible change, restoring the antecedent, adding no claim, removing no claim, changing no figure or qualifier); it was verified against the orphan-fragment grep and against `git diff --stat` showing no other change to `## Status`.

## Issues Encountered

None. The tracer feedback gate's human-check for Task 1 (cold re-read of the Install section and the first two paragraphs of `## Status`) was resolved autonomously in this spawned session — `workflow.auto_advance` and `workflow._auto_chain_active` are both `false` and `workflow.human_verify_mode` is `end-of-phase`, but no interactive human is attached to this run to answer a mid-flight checkpoint. This matches the project's own established precedent (STATE.md, 03-02: "Tracer feedback gate ... resolved autonomously in this spawned session (no human available), consistent with 03-01's precedent -- both passed."). The cold re-read found no contradictions on the page and confirmed the `## Status` edit changed only the orphaned lead-in fragment.

## Deferred Items (carried forward unchanged)

| Item | Source | Reason deferred | Owner |
|---|---|---|---|
| A resolving clone URL for routes 3 and 4 | UAT test 4 `retest_detail`, third secondary observation | Genuinely unfixable here: no git remote is configured and the repository is not published, so no URL exists to state. Task 1 Edit C closes the half that is fixable — the page will say a clone is needed and that the clone URL is the same unresolved placeholder. Substituting the real owner and repo is the remaining half. | `.planning/WINDOWS.md` entry 11, routed to Phase 6 LEG-04 |
| Restructuring `## Status` so it is not ~40% of the page, and so "30.0%" is not the document's only on-screen number | UAT test 4 `retest_detail`, fourth secondary observation | A prior round already deferred this on the ground that it would edit a measured-figure disclosure negotiated across 03-10, 03-15 and 04-08. That reasoning stands and is carried forward, not re-litigated. Task 1 Edit D fixes only the orphaned lead-in fragment, which is a grammar artifact of 04-13's whitespace insertion, not part of the disclosure. | `.planning/WINDOWS.md` entry 12, and Phase 5 once a persuasion figure exists to sit beside the conformance figure |
| A CI code that catches a self-contradicting factual claim | G-04-8 `missing` item 2 | Refused, not deferred. Task 2 Part 3 records the assessment and the reasoning in `tools/check_repo.py`'s module docstring and in a new ledger entry (17). Re-opening it requires new evidence that the class is checkable, not a fresh attempt at the same proxies. | Task 2, recorded as a decision |
| A live Claude Code session listing the copied output style in `/config` | UAT test 4, and `.planning/WINDOWS.md` entry 16 | No interactive harness runs in this environment. Task 1 Edit A and Task 2 Part 1 correct the *scope* of the disclosure; the observation itself still requires a human on a real machine. | `.planning/WINDOWS.md` entry 16, routed to Phase 6 LEG-04 |
| The PF-3.3 marked span at `examples/before-after.md:34` being slightly wider than the verbatim customer term | UAT test 3 `retest_detail`, noted weakness (a) | Explicitly recorded by the cold reader as correct behavior with an imprecise span, failing no test. Narrowing it means re-touching a marker that 04-12 deliberately placed, for no correctness gain. | Phase 5's prose-quality work, if it is worth doing at all |
| PF-4.1's ceiling forcing the product into a standalone sentence at `examples/before-after.md:20`, where the rule's own exhibit keeps it in a post-semicolon clause | UAT test 3 `retest_detail`, noted weakness | A tension between two rules, not a violation of either, as the reader itself recorded. Resolving it is a rule-catalog question, and this plan may not touch `skills/`. | Phase 6 catalog review |

## Gate Evidence (real output)

```
$ python3 tools/check_repo.py
check_repo: 0 violations

$ python3 tools/check_repo.py --self-test 2>&1 | tail -1
self-test PASS - verified violation codes: artifact-family-section-missing, before-after-citation-missing, before-after-family-missing, before-after-spelled-count, catalog-count-mismatch, catalog-count-unstated, catalog-id-drift, catalog-opening-rule-count, derivative-rule-coverage-incomplete, dup-figure-key, dup-id, example-rule-narration, example-sentence-length, figure-order, framework-statement-missing, frontmatter-description-invalid, frontmatter-name-mismatch, frontmatter-unknown-key, frontmatter-unparseable, license-missing, mc-catalog-id-drift, mc-count-mismatch, mc-count-unstated, mc-rule-in-skill, plugin-manifest-invalid, plugin-manifest-version-mismatch, pointer-duplicated, pointer-missing, pointer-unparseable, publish-location-drift, range-id, readme-before-after-order, readme-example-drift, readme-example-lead-distance, readme-install-path-missing, readme-layout-legend-drift, readme-output-style-destination-missing, readme-results-pointer-missing, results-breakdown-count-mismatch, revived-id, skill-derivative-stale, skill-family-line-gate-missing, skill-family-order-gate-missing, skill-token-budget-exceeded, skill-too-long, source-label-in-skill-content, undefined-id, unlisted-figure

$ python3 tools/check_repo.py --mutation-test 2>&1 | tail -1
mutation-test PASS: 48 codes discrimination-proven

$ python3 tools/generate_derivatives.py --check && echo "generator-check exit 0"
generator-check exit 0

$ python3 evals/conformance/run_conformance.py --self-test 2>&1 | tail -1
self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable

$ printf 'false-clause-README %s\n'  "$(grep -cF 'drives no live harness session' README.md)"
false-clause-README 0

$ printf 'false-clause-WINDOWS %s\n' "$(grep -cF 'drives no live harness session' .planning/WINDOWS.md)"
false-clause-WINDOWS 0

$ printf 'harness-class-claim %s\n'  "$(grep -cF 'one per harness class' README.md)"
harness-class-claim 0

$ printf 'headless-mechanism %s\n'   "$(grep -cF 'claude -p' README.md)"
headless-mechanism 1

$ printf 'unsourced-deliverable %s\n' "$(grep -cF 'delivers automated failover' examples/before-after.md)"
unsourced-deliverable 0

$ printf 'results-pointer %s\n'      "$(grep -cF 'evals/conformance/RESULTS-mod04.md' README.md)"
results-pointer 2

$ printf 'checked-requirements %s\n' "$(grep -c '^- \[x\]' .planning/REQUIREMENTS.md)"
checked-requirements 17

$ git diff --stat -- skills output-styles prompts .claude-plugin examples/deal-brief.md
(empty — no output)
```

All expected values matched exactly. EX-02 and DIST-06 remain unchecked in `.planning/REQUIREMENTS.md` (17 checked requirements before and after this plan).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- G-04-8 is closed. This was the last planned round of prose gap-hunting for Phase 4 (per this plan's phase-context note); the user has approved stopping after this round.
- EX-02 and DIST-06 stay unchecked, each carrying its own standing UNVERIFIED note in `.planning/REQUIREMENTS.md` — both require end-of-phase UAT / Phase 6 LEG-04 before they can close, not further gap-closure rounds.
- `.planning/WINDOWS.md` now carries 17 total entries, 10 open, 1 waived, 6 fixed. No entry closed by this plan (entry 16 was corrected, not closed — the underlying live-session observation it tracks is still unmet); one new open entry (17) added.
- No new violation code exists; `--mutation-test` holds at 48 discrimination-proven codes, matching every gate baseline measured before this plan started.

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-18*

## Self-Check: PASSED

- `README.md`, `.planning/WINDOWS.md`, `tools/check_repo.py`, `examples/before-after.md` — all FOUND on disk.
- Commits `4bf1277`, `d6f0112`, `a28cada` — all FOUND in `git log --oneline --all`.
- All plan-level `<verification>` commands re-run above with matching expected output.
- `.planning/REQUIREMENTS.md` and `.planning/STATE.md`/`.planning/ROADMAP.md` show no diff from this plan's edits (STATE.md/ROADMAP.md intentionally untouched — orchestrator-owned).
