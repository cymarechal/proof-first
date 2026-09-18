---
phase: 04-distribution-worked-examples
plan: 11
subsystem: infra
tags: [check_repo.py, plugin-manifest, marketplace.json, self-test, mutation-test, worked-examples]

# Dependency graph
requires:
  - phase: 04-distribution-worked-examples
    provides: "plugin.json/marketplace.json manifests, plugin-manifest-invalid check (04-01), the CR-01 defect the 04-VERIFICATION.md gap-closure round found in 04-10's fix pass"
provides:
  - "Required-key presence on marketplace.json's plugins[0] entry, enforced and exhaustively self-tested"
  - "A second real-file plugin-manifest-invalid mutation proving discrimination against the actual repository manifest"
  - "Cross-manifest equality guard (MARKETPLACE_ENTRY_EQUAL_KEYS) for the five hand-duplicated distribution fields, with the homepage/repository exclusion proven silent rather than merely asserted"
  - "MC-31 punctuation repair (colon-introduced quotation) in skills/proof-first/references/worked-examples.md"
  - "Disambiguated 'raw regex matches' wording for the spelled-cardinal measurement in both docstring copies (IN-01)"
affects: [04-VERIFICATION, phase-06-legal-review]

# Actuals (#2632)
actuals:
  tokens: 6610
  tasks: 3
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns: ["fire-and-clear proof pattern for CI checkers: register a real-file mutation, capture the RED state before the fix, then GREEN after", "exhaustive self-test coverage matrix (key x position) instead of one hand-built sample fixture"]

key-files:
  created: []
  modified:
    - tools/check_repo.py
    - skills/proof-first/references/worked-examples.md

key-decisions:
  - "Reused PLUGIN_REQUIRED_KEYS for the marketplace entry rather than defining a narrower marketplace-entry-optional subset -- both real manifests carry all nine keys today, so a subset constant would describe a field this repository does not actually treat as optional."
  - "Equality set (MARKETPLACE_ENTRY_EQUAL_KEYS) deliberately excludes homepage/repository (owned by publish-location-drift's owner-segment normalisation across four GitHub URL syntaxes), name (owned by the folder-name equality check), and version (owned by plugin-manifest-version-mismatch) -- proven silent on the mixed-URL-form self-test fixture, not merely asserted."
  - "WR-01's literal reviewer suggestion (period-to-colon substitution) was not applied verbatim because it produces a single 28-word sentence tripping example-sentence-length; the two-sentence split matching examples/before-after.md:34's construction was used instead, measuring 20 and 9 words."

requirements-completed: [DIST-02]

coverage:
  - id: D1
    description: "Deleting any one of the nine PLUGIN_REQUIRED_KEYS from marketplace.json's plugins[0] entry fails check_repo.py, naming that key and file"
    requirement: "DIST-02"
    verification:
      - kind: unit
        ref: "tools/check_repo.py --self-test (required-key coverage matrix, 18 cells)"
        status: pass
      - kind: unit
        ref: "tools/check_repo.py --mutation-test (second plugin-manifest-invalid mutation against the real marketplace.json)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Cross-manifest equality guard for the five hand-duplicated distribution fields, with homepage/repository exclusion proven"
    requirement: "DIST-02"
    verification:
      - kind: unit
        ref: "tools/check_repo.py --self-test (plugin_marketplace_entry_drift_root fires; plugin_good_codes and plugin_mixed_url_codes stay silent)"
        status: pass
    human_judgment: false
  - id: D3
    description: "MC-31 punctuation repair and IN-01 measurement disambiguation in worked-examples.md and check_repo.py docstrings"
    verification:
      - kind: unit
        ref: "tools/check_repo.py plain run: check_repo: 0 violations; grep -cF checks on 'said in discovery:' and 'raw regex matches'"
        status: pass
    human_judgment: false

# Metrics
duration: 35min
completed: 2026-09-18
status: complete
---

# Phase 04 Plan 11: Marketplace-Entry Required-Key Enforcement (CR-01 Gap Closure) Summary

**Closed CR-01 by enforcing PLUGIN_REQUIRED_KEYS on marketplace.json's plugins[0] entry, proving it exhaustively (18-cell key x position self-test matrix) and against the real file (a second registered mutation), then folded in WR-01/WR-02/IN-01 from 04-REVIEW.md without registering any new violation code.**

## Performance

- **Duration:** 35 min
- **Started:** 2026-09-18T04:48:00Z (approx, per STATE.md pre-plan session)
- **Completed:** 2026-09-18T05:23:01Z
- **Tasks:** 3
- **Files modified:** 2 (`tools/check_repo.py`, `skills/proof-first/references/worked-examples.md`)

## Accomplishments

- **Task 1 (tracer, tdd="true"):** `check_plugin_manifest_invalid` now enforces `PLUGIN_REQUIRED_KEYS` against `marketplace.json`'s `plugins[0]` entry — the object `claude plugin marketplace add` actually reads — not just `plugin.json`'s top-level object. A second real-file `plugin-manifest-invalid` mutation (`_mutate_marketplace_entry_required_key_missing`) was registered against the real `marketplace.json`. Red-then-green proven per the plan's own TDD instruction (see below).
- **Task 2:** An 18-cell self-test matrix (`_required_key_matrix_root`, 9 keys x 2 positions) proves the required-key claim exhaustively rather than by one sample, closing the exact defect class that let CR-01 ship in 04-10 (a fixture/mutation pair both targeting `plugin.json` only).
- **Task 3:** Folded in three 04-REVIEW.md findings — WR-02 (cross-manifest equality guard `MARKETPLACE_ENTRY_EQUAL_KEYS`), WR-01 (MC-31 colon-introduced quotation, matching `examples/before-after.md:34`'s construction), and IN-01 (disambiguated "raw regex matches" wording in both docstring copies of the spelled-cardinal measurement).
- No new violation code registered anywhere in this plan. `--mutation-test` reports 47 codes discrimination-proven throughout, matching the pre-plan baseline exactly.

## Task Commits

Each task was committed atomically:

1. **Task 1: Enforce required-key presence on marketplace.json's plugin entry, proven red-then-green on the real file** — `6af26bd` (fix)
2. **Task 2: Close the class — assert every required key at every enforced position, exhaustively** — `19715ce` (test)
3. **Task 3: Fold in the three review warnings — duplicated-field equality, the MC-31 punctuation repair, and the ambiguous measurement** — `44b256b` (fix)

_Note: Task 1 carried `tdd="true"` as a per-task attribute (the plan's own red-then-green instruction on the mutation-registry row), not the project-wide TDD gate — `workflow.tdd_mode` is false for this project._

## Discrimination Proof (recorded per the plan's `<output>` spec)

**1. Red state, Task 1, before the fix — verbatim:**

```
mutation-test CONTROL: 0 violations on the unmutated copy (0 known-open per KNOWN_OPEN_VIOLATIONS, 0 unexpected)
mutation-test FAIL: plugin-manifest-invalid delete the required 'license' key from the real .claude-plugin/marketplace.json's plugin entry
mutation-test FAILED: 0 codes not discrimination-proven
```
Exit code: 1 (non-zero, confirmed via `echo $?`).

**2. Green state, final run — verbatim:**

```
mutation-test CONTROL: 0 violations on the unmutated copy (0 known-open per KNOWN_OPEN_VIOLATIONS, 0 unexpected)
mutation-test PASS: 47 codes discrimination-proven
```
Exit code: 0. `mutation-test OK: plugin-manifest-invalid` count: **2** (confirmed via `grep -c`).

**3. Fire direction, all nine keys (scratch copy, Task 1):** deleting each of `name`, `displayName`, `description`, `version`, `author`, `homepage`, `repository`, `license`, `keywords` one at a time from `.claude-plugin/marketplace.json`'s `plugins[0]` made `check_repo.py` fire `plugin-manifest-invalid`, naming that key and `.claude-plugin/marketplace.json` — 9/9, matching the plan's expected outcome (0/9 fired before this plan).

**4. Four-together, one violation per key:** removing `license`, `keywords`, `author`, `displayName` together in a scratch copy produced exactly 4 separate `plugin-manifest-invalid` lines, each naming a different key.

**5. Exhaustive-matrix discrimination pair (Task 2), measured in both directions:**
- With Task 1's marketplace-entry loop removed in a scratch copy: **9** failing matrix cells, all at the marketplace-entry position (`FAIL: plugin-manifest-invalid did not fire for key '<key>' missing from marketplace.json's plugin entry` for all nine keys).
- With the loop present: **0** failing matrix cells.
- Both numbers match the plan's planning-time measurement exactly (9 and 0).

**6. MC-31 repaired sentence word counts (Task 3, WR-01):** the repaired check column splits into two sentences under the shipped `SENTENCE_SPLIT_RE`/`MARKER_SPAN_RE`/`PF41_WORD_CEILING` — measured **20** and **9** words respectively, both inside the 25-word ceiling, matching the plan's stated expected values exactly.

**7. WR-02 fire/clear/no-double-report, all verified in scratch copies:**
- Changing `marketplace.json`'s `plugins[0].keywords` to disagree with `plugin.json`'s fired `plugin-manifest-invalid` naming `keywords` and both manifest paths; restoring cleared it.
- `--self-test` confirms `_mixed_url_form_manifests` (four GitHub URL syntaxes, same owner) stays silent on `plugin-manifest-invalid`, proving the `homepage`/`repository` exclusion.
- Deleting `license` from the marketplace entry produced exactly **1** `plugin-manifest-invalid` line for that key, not two (the required-key loop and the equality guard do not double-report an absence).

**8. WINDOWS.md deviations filed:** None. Every count this plan's `<interfaces>` block stated (baseline 47 codes, 9/9 fire, 9-and-0 matrix discrimination, 20-and-9 word counts, 5 raw regex matches with 4 would-be violations after the proper-noun exemption, 147-line file count) matched the working tree exactly on measurement. No 13/14/15-precedent deviation entry was needed.

## Files Created/Modified

- `tools/check_repo.py` — `check_plugin_manifest_invalid` now enforces `PLUGIN_REQUIRED_KEYS` at both positions and `MARKETPLACE_ENTRY_EQUAL_KEYS` cross-manifest equality; new fixture builders `_mutate_marketplace_entry_required_key_missing`, `_marketplace_entry_missing_key_manifests`, `_required_key_matrix_root`, `_marketplace_entry_field_drift_manifests`; new self-test matrix (18 cells) and coverage assertions; both docstrings (function and module-contract entry) reconciled to state exactly what is enforced; IN-01's ambiguous "5 such occurrences were measured" phrase disambiguated in both copies to name raw regex matches and the proper-noun exemption's effect.
- `skills/proof-first/references/worked-examples.md` — MC-31's check column line 142 repaired: introduces its quotation with a colon and splits the attribution into two sentences (20 and 9 words), matching `examples/before-after.md:34`'s construction. One line changed (`git diff --numstat` confirms 1 insertion, 1 deletion); total line count unchanged at 147.

## Decisions Made

See `key-decisions` in frontmatter.

## Deviations from Plan

None - plan executed exactly as written. One self-correction during Task 1 authoring: the equality-check code was initially written inline while implementing Task 1's required-key loop, then backed out before verification/commit once it became clear `MARKETPLACE_ENTRY_EQUAL_KEYS` (a Task 3 deliverable) did not exist yet — this was caught and corrected before any verification or commit ran, so it produced no incorrect commit and is not logged as a Rule 1-3 deviation (no broken state was ever committed).

**Total deviations:** 0.
**Impact on plan:** None — plan executed exactly as written across all three tasks.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- CR-01 (the sole `failed` gap in `04-VERIFICATION.md`) is mechanically closed: the marketplace-entry required-key hole is enforced, exhaustively self-tested, and proven against the real repository file in both directions.
- WR-01, WR-02, and IN-01 from `04-REVIEW.md` are also closed in this same pass, per the plan's fold-in disposition table.
- `DIST-02`'s checkbox correctly stays `[ ]` — its live-install half remains unverified for the disclosed, unrelated reason in WINDOWS.md entry 11 (no git remote). `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` still returns `0`.
- Out-of-scope items (G-04-3, G-04-5, DIST-06's prose-quality half, the live-install flow, cross-route behavioral equivalence) were not touched, as instructed.
- Ready for `/gsd-verify-work 04` to re-run phase-level verification and confirm CR-01's closure against a fresh `04-VERIFICATION.md` pass.

## Self-Check: PASSED

- `tools/check_repo.py` and `skills/proof-first/references/worked-examples.md` exist and carry the expected changes (confirmed via `git diff --stat` against the pre-plan commit).
- All three task commits (`6af26bd`, `19715ce`, `44b256b`) found in `git log --oneline --all`.
- Full project gate green at time of writing: `--self-test` PASS, `--mutation-test` PASS (47 codes discrimination-proven, 0 unexpected, 2 `plugin-manifest-invalid` OK lines), plain run `check_repo: 0 violations`, `evals/conformance/run_conformance.py --self-test` PASS, `generate_derivatives.py --check` exit 0.
- `git status --porcelain` shows only `.planning/` bookkeeping files and the two plan-scoped source files as modified — no scope breach.

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-18*
