---
phase: 01-foundations-legal-scaffolding-numbering-shared-deal
verified: 2026-09-10T11:15:00Z
status: human_needed
score: 14/14 must-haves verified
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: "7/9 must-haves verified"
  gaps_closed:
    - "BLOCKER: parse_notices() could not match production NOTICES.md's shape (prose between heading and fence); pointer resolved to None and check_pointer() short-circuited to []. Closed by 01-05: parse_notices() now uses split_sections() to read the Attribution pointer section body, then searches for a fenced block inside that body only."
    - "check_repo.py exited 0 when a named carrier existed and lacked the pointer, and when it contained the pointer twice — the pointer family was dead code. Closed by 01-05: independently reproduced deleting/duplicating the pointer line in README.md now produces pointer-missing/pointer-duplicated and exit 1."
    - "--self-test's inline NOTICES.md fixture used a fence-under-heading shape production NOTICES.md never has, so the self-test certified an unreachable shape. Closed by 01-05: _bad_notices()/_good_notices() rewritten to the production shape (heading, prose paragraph, fence); new _unparseable_notices()/_escaping_notices() fixtures added; self-test now names pointer-unparseable among 10 covered codes."
    - "README.md as the first real carrier was not actually enforced — 01-04's key link was falsified. Closed by 01-05, independently re-reproduced this round: deleting the pointer line from README.md now yields pointer-missing and exit 1."
    - "WARNING: check_unlisted_figure()'s in_canonical flag never reset when '## Canonical figures' was a file's last heading, so content appended after the table was never scanned. Closed by 01-06 Task 1: the exempt region is now bounded by table shape (blank or pipe-prefixed lines), not only by a following heading. Independently reproduced this round: a stray figure appended after the table at end-of-file is now reported."
    - "WARNING (WR-01, 01-REVIEW.md): MC IDs validated against one aggregate (min,max) across all 8 dimension blocks instead of each block's own range. Closed by 01-06 Task 2: parse_numbering() now returns a per-dimension mc_ranges dict; check_range_id() requires membership in some declared block. Independently reproduced this round: an ID landing in a deliberately opened gap between two blocks is reported range-id; the real MC-40 ceiling is still accepted."
    - "WARNING (WR-02, 01-REVIEW.md): unlisted-figure's value-collision blind spot was undisclosed. Closed by 01-06 Task 3 as a disclosure-only fix (the stronger key-binding fix is deliberately deferred — implementing it would rewrite the frozen '## Canonical figures' interface D-10 designates as an API): the module docstring now states the ceiling and _good_deal_brief() pins two rows sharing one value as an accepted, documented case."
    - "Structural gap: a check that exists, is named as covered, runs in CI, and cannot fire had no regression class closing it. Closed by 01-07: a --mutation-test mode injects one named defect per violation code into a throwaway copy of the real repository files and asserts the code fires; wired into CI between --self-test and the live check."
  gaps_remaining: []
  regressions: []
gaps: []
human_verification:
  - test: "Search the web for the 9 invented deal-brief names: Halverton Mutual, Kestrel Systems Group, Ardent Digital, Vantage Nine Consulting, Diane Osoria, Marcus Feld, Priya Raghunathan, Tom Weatherly, Gina Almeida."
    expected: "None matches an existing company or a real identifiable person in insurance, retirement services, or systems integration."
    why_human: "Requires live network access this verifier lacks. Logged as .planning/WINDOWS.md item 1 (open), scoped to 'before the repository goes public' / LEG-04, not a Phase-1 success-criterion blocker."
  - test: "An independent reviewer (not the executor who authored the content) reads examples/deal-brief.md end to end."
    expected: "No sentence compares two real companies or two real products; VMware vSphere/Oracle Database/AWS products appear only as migration source/target."
    why_human: "The originating plan requires an independent reviewer distinct from the author; the self-review already performed is a substitute, not the specified check. Logged as .planning/WINDOWS.md item 2 (open), scoped to LEG-04, not a Phase-1 success-criterion blocker."
  - test: "Read tools/check_repo.py's module docstring's ten violation-code entries end to end and confirm each declared ceiling matches what the code actually does, with no entry promising a guarantee the function does not deliver."
    expected: "Every docstring entry is an honest, accurate description of current code behavior — this is the honesty contract the phase's original BLOCKER violated."
    why_human: "Harvested from 01-06-PLAN.md Task 3's <verify><human-check> block (type=auto task, human-check deferred to end-of-phase per workflow.human_verify_mode). The task's own text states this is 'a judgment a grep cannot make.' This verifier independently read all ten entries against the current code (lines 23-75, 193-210, 307-342, 407-420) and found no discrepancy, but the plan's own design requires human sign-off rather than the executor's or verifier's self-assessment."
---

# Phase 1: Foundations — Legal Scaffolding, Numbering, Shared Deal Verification Report

**Phase Goal:** The project's foundational scaffolding — rule numbering, shared example data, and legal posture — is frozen before any rule content is drafted, so nothing downstream forces a renumbering or a retrofit.
**Verified:** 2026-09-10T11:15:00Z
**Status:** human_needed
**Re-verification:** Yes — after gap closure (plans 01-05, 01-06, 01-07)

## Goal Achievement

Every truth from the 2026-09-10T07:21:30Z verification (commit `9af9999`) is re-stated below by number so the prior report's findings are accounted for by name, not superseded silently. All truths were re-verified by direct reproduction in this session (fresh scratch-copy mutations run independently of the plans' own `<verify>` blocks and independently of the SUMMARY.md/01-REVIEW.md claims), not by re-reading prior claims.

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A contributor can look up the next free ID in either the `PF-<section>.<n>` or `MC-<n>` namespace without guessing (ROADMAP SC1) | ✓ VERIFIED | Regression-checked: `NUMBERING.md` structure unchanged (9 `## ` headings). `dup-id`/`range-id`/`revived-id`/`undefined-id` independently re-verified to fire on production-shaped mutations this round (see Behavioral Spot-Checks). |
| 2 | Every worked example can cite facts from one canonical fictional deal brief (ROADMAP SC2) | ✓ VERIFIED | Regression-checked: `examples/deal-brief.md` structure unchanged (10 `## ` headings). The end-of-file blind spot that partially undermined this truth previously (see #10 below) is now closed and independently reproduced. |
| 3 | `LICENSE` and `NOTICES.md` individually name all three frameworks with non-affiliation and trademark language (ROADMAP SC3) | ✓ VERIFIED | Regression-checked: `LICENSE` unmodified MIT text (21 lines); `NOTICES.md` still carries `## Scope of this file` and 3 fixed-order `###` framework subsections, byte-for-byte consistent with the prior verification's description. |
| 4 | Nothing in the repo reproduces proprietary framework text; framework concepts are paraphrased and sources are cited, **and this is mechanically enforced** (ROADMAP SC4) | ✓ VERIFIED | **Previously FAILED (enforcement gap).** Independently re-reproduced this round: deleting the pointer line from `README.md` in a scratch copy now produces `pointer-missing README.md does not contain the attribution pointer string`, exit 1 — the exact reproduction that previously produced `check_repo: 0 violations` now fails loud. `SOURCES.md` content unchanged and still honest about LEG-04 deferral. |
| 5 | `check_repo.py` exits 0 when a carrier is absent, non-zero with `pointer-missing`/`pointer-duplicated` when a named carrier exists and the pointer is absent/duplicated (01-01/01-05 must-have, LEG-03/empty edge) | ✓ VERIFIED | Independently reproduced: absent-carrier and present-carrier cases both produce the documented behavior (see Behavioral Spot-Checks #1, #2). |
| 6 | `check_repo.py --self-test` proves every check family fires on a production-shaped fixture, not merely its own historically-unreachable shape (01-01/01-05 must-have) | ✓ VERIFIED | `--self-test` exits 0 and names all **10** codes as covered, including `pointer-unparseable`. `_bad_notices()`/`_good_notices()` fixtures now carry the heading→prose→fence shape that matches production `NOTICES.md` (confirmed by direct file read, lines 757-788). |
| 7 | `README.md` is a real, enforced attribution-pointer carrier — `pointer-missing` fires against shipped content, not only against a fixture (01-04 key link, previously falsified) | ✓ VERIFIED | Same empirical reproduction as #4: deleting the pointer line from the real `README.md` (copied to a scratch dir) now yields `pointer-missing README.md ...`, exit 1. The key link now holds. |
| 8 | `.github/workflows/ci.yml` runs the checker's self-test, mutation-test, and live check on every push, in that order, before any rule content exists, with zero `pip install` lines | ✓ VERIFIED | Direct file read: single `check` job, `ubuntu-latest`, checkout + setup-python 3.11, one run block with the three `python3 tools/check_repo.py` invocations in `--self-test`, `--mutation-test`, then bare order. `grep -c 'pip install'` → 0. (Scope of this truth expanded by 01-07 to include the new mutation-test step; original self-test+live ordering preserved.) |
| 9 | No empty placeholder file was created for any documented-but-unbuilt path (D-15) | ✓ VERIFIED | `find . -type f -empty -not -path './.git/*' -not -path './.gsd/*'` → 0 files. |
| 10 | `unlisted-figure` has no positional blind spot at end of file when `## Canonical figures` is a file's last heading (01-06 must-have, closing the prior WARNING) | ✓ VERIFIED | Independently reproduced: appending `A stray figure of $999,999,999 appears here at end of file.` after the real Canonical figures table's last row (heading is last in the real file) now produces `unlisted-figure $999,999,999 in examples/deal-brief.md has no matching Canonical figures row`, exit 1. Pre-existing mid-file detection (inside `## Timeline`) still works — no regression. Live run against the repo as shipped stays at 0 violations, so no false positive was introduced against real trailing table rows. |
| 11 | MC IDs are validated per declared dimension block, not against one aggregate range spanning all 8 blocks (01-06 must-have, closing WR-01) | ✓ VERIFIED | Independently reproduced with two adversarial mutations: (a) deleting the `Economic Buyer` block row and allocating `MC-8` (which falls in the resulting gap) produces `range-id MC-8 belongs to no declared MC dimension block`, exit 1; (b) allocating `MC-40` (the real, declared Competition-block ceiling) produces `check_repo: 0 violations`, exit 0 — the boundary ID is correctly accepted by its own block, not merely by an aggregate ceiling. |
| 12 | `unlisted-figure`'s value-collision ceiling is disclosed in the module docstring and pinned by a fixture rather than left silent (01-06 must-have, closing WR-02 as a disclosure-only fix) | ✓ VERIFIED | Docstring (lines 45-58) states both the pre-existing bare-count ceiling and the new "Declared ceiling (value collision): matching is by formatted value string with no binding to a canonical key" clause. `_good_deal_brief()` (lines 743-754) carries two distinct keys (`audit-fee-rate`, `escrow-fee-rate`) sharing the value `5%`, and `--self-test` stays green on that fixture, confirming the collision is accepted-and-documented rather than accidental. The stronger key-binding fix is explicitly and reasonably deferred (would rewrite the frozen `## Canonical figures` interface D-10 designates as an API) — this is a disclosure claim, and disclosure is what was verified, not a claim that the underlying limitation was removed. |
| 13 | `--mutation-test` proves every one of the 10 violation codes fires against a deliberately mutated copy of the real repository's documents, with a clean control run first (01-07 must-have) | ✓ VERIFIED | Ran independently: `mutation-test CONTROL: 0 violations on the unmutated copy`, followed by 10 `mutation-test OK: <code>` lines (one per code in `ALL_CHECK_CODES`), then `mutation-test PASS: 10 codes proven live`, exit 0. Independently confirmed `{code for code, _, _ in MUTATIONS} == set(ALL_CHECK_CODES)` in both directions via a standalone Python check — the harness cannot silently omit a future code. |
| 14 | The mutation harness itself is fail-first, not merely green by construction (01-07 must-have) | ✓ VERIFIED | Independently reproduced the exact adversarial test the plan specifies: injected `return []` at the top of `check_pointer()` in a scratch copy and re-ran `--mutation-test`. Result: `mutation-test FAIL: pointer-missing ...`, `mutation-test FAIL: pointer-duplicated ...`, `mutation-test FAILED: 2 codes not proven live`, exit 1 — matches the verbatim output recorded in 01-07-SUMMARY.md exactly. This is the specific property the phase's original BLOCKER lacked: the harness can distinguish "check disabled" from "check never ran." |

**Score:** 14/14 truths verified by independent reproduction. `behavior_unverified: 0` — every truth above that concerned runtime behavior (state-transition-shaped: "exits non-zero when X", "fires when Y", "the harness proves Z") was exercised by an actual command run in this session, not inferred from symbol presence.

One additional item — docstring-honesty of the ten violation-code entries — is a planner-deferred human-check (01-06-PLAN.md Task 3's `<verify><human-check>`), not a truth this verifier can certify unilaterally; it is listed under Human Verification Required, not counted in the 14/14 score.

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `NUMBERING.md` | 9-section ID registry, PF/MC ranges, empty Allocated/Deprecated tables | ✓ VERIFIED | Unchanged from prior verification; wired into `check_repo.py`'s now-per-block MC enforcement. |
| `tools/check_repo.py` | Stdlib-only checker, 10 violation codes, fixture self-test, mutation-test harness | ✓ VERIFIED | All 10 codes (`dup-id`, `range-id`, `revived-id`, `undefined-id`, `dup-figure-key`, `figure-order`, `unlisted-figure`, `pointer-missing`, `pointer-duplicated`, `pointer-unparseable`) independently proven to fire against production-shaped mutations. AST-based import scan confirms `{argparse, re, tempfile, pathlib, sys, shutil}` — stdlib only, `shutil` is the only import 01-07 added. 907 lines. |
| `.github/workflows/ci.yml` | Single job, self-test + mutation-test + live check in that order, no `pip install` | ✓ VERIFIED | Confirmed on disk; 3 `python3 tools/check_repo.py` invocations in the documented order; one `check:` job; 0 `pip install` lines. |
| `examples/deal-brief.md` | Complete fictional deal, Canonical figures table, no end-of-file scanning blind spot | ✓ VERIFIED | Structure unchanged; the previously-noted positional gap is closed and independently re-verified. |
| `NOTICES.md` | Scope section, attribution pointer, 3 framework statements, now actually parseable | ✓ VERIFIED | Content unchanged from prior verification (still has the prose paragraph between heading and fence); the parser now handles that shape correctly. |
| `LICENSE` | Unmodified MIT | ✓ VERIFIED | Unchanged. |
| `SOURCES.md` | Rule, reproduction boundary, 3 source tables, out-of-bounds list | ✓ VERIFIED | Unchanged from prior verification (not touched by any gap-closure plan; correctly not claimed by 01-05/06/07 per the phase's own Source Coverage Audit). |
| `README.md` | Claim-free entry point, first real pointer carrier, now actually enforced | ✓ VERIFIED | Content unchanged; carries exactly one occurrence of the pointer string (`grep -c` → 1); now demonstrably inspected by the checker. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|-----|-----|--------|---------|
| `NUMBERING.md` reserved-range tables | `tools/check_repo.py` per-dimension `mc_ranges` / `pf_ranges` | reads ranges from the registry, per block | ✓ WIRED | Independently re-verified against a gap-mutated copy and a boundary-mutated copy (Truth #11). |
| `examples/deal-brief.md` `## Canonical figures` table | `tools/check_repo.py` figure scanner | table-shape-bounded exempt region | ✓ WIRED | Independently re-verified against an end-of-file mutation (Truth #10); no longer position-dependent. |
| `NOTICES.md` attribution-pointer block + carriers list | `tools/check_repo.py` pointer assertion, via `split_sections()` | one canonical string, N pointers, section-scoped extraction | ✓ WIRED | **Previously NOT WIRED.** Independently re-verified against three separate mutations (missing, duplicated, unparseable) — all three fire against production content (Truths #5, #7). |
| `.github/workflows/ci.yml` | `tools/check_repo.py` (3 modes) | CI runs self-test, mutation-test, live check on every push | ✓ WIRED | Workflow steps and commands verified on disk. |
| `ALL_CHECK_CODES` | `MUTATIONS` registry | set equality enforced at runtime and by acceptance criterion | ✓ WIRED | Independently confirmed via a standalone Python equality check; a future code with no mutation would be a reported harness failure, not a silent gap. |

### Data-Flow Trace (Level 4)

Not applicable in the conventional sense — this phase ships no UI or API surface with rendered dynamic data. The equivalent trace for a repository-integrity checker is "does the violation reported at the end of the pipeline trace back to a real parse of a real file," which is exactly what the Behavioral Spot-Checks and Key Link Verification sections above establish by direct mutation rather than by reading the code's intent.

### Behavioral Spot-Checks

All checks below were run independently by this verifier in this session, on fresh scratch copies, not reused from any plan's own `<verify>` block or SUMMARY.md's recorded output (except where noted as a cross-check).

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Live run on repo as shipped | `python3 tools/check_repo.py` | `check_repo: 0 violations`, exit 0 | ✓ PASS |
| `--self-test` | `python3 tools/check_repo.py --self-test` | `self-test PASS - verified violation codes: dup-figure-key, dup-id, figure-order, pointer-duplicated, pointer-missing, pointer-unparseable, range-id, revived-id, undefined-id, unlisted-figure` (10 codes), exit 0 | ✓ PASS |
| `--mutation-test` | `python3 tools/check_repo.py --mutation-test` | `mutation-test CONTROL: 0 violations`, 10× `mutation-test OK: <code>`, `mutation-test PASS: 10 codes proven live`, exit 0 | ✓ PASS |
| **Mutation 1 — pointer deleted from README.md** | scratch copy, `grep -v` the pointer line, run checker | `pointer-missing README.md does not contain the attribution pointer string`, exit 1 | ✓ PASS (BLOCKER closure confirmed) |
| **Mutation 2 — pointer duplicated in README.md** | scratch copy, append a second copy of the pointer line, run checker | `pointer-duplicated README.md contains the attribution pointer string 2 times`, exit 1 | ✓ PASS |
| **Mutation 3 — `## Attribution pointer` heading removed from NOTICES.md** | scratch copy, `sed` delete the heading line, run checker | `pointer-unparseable NOTICES.md's Attribution pointer section yields no usable pointer definition`, exit 1 | ✓ PASS |
| **Mutation 4 — stray `$` figure appended after Canonical figures table, end of file** | scratch copy, append a prose line with `$999,999,999` after the real table's last row | `unlisted-figure $999,999,999 in examples/deal-brief.md has no matching Canonical figures row`, exit 1 | ✓ PASS (end-of-file blind spot closure confirmed) |
| **MC gap test** | scratch `NUMBERING.md` with `Economic Buyer` block row deleted, `MC-8` allocated | `range-id MC-8 belongs to no declared MC dimension block`, exit 1 | ✓ PASS |
| **MC boundary test** | scratch `NUMBERING.md` with `MC-40` (real declared ceiling) allocated | `check_repo: 0 violations`, exit 0 | ✓ PASS (real ceiling still accepted) |
| **Mutation-harness fail-first proof** | scratch copy with `return []` injected at the top of `check_pointer()`, run `--mutation-test` | `mutation-test FAIL: pointer-missing ...`, `mutation-test FAIL: pointer-duplicated ...`, `mutation-test FAILED: 2 codes not proven live`, exit 1 | ✓ PASS (matches 01-07-SUMMARY.md's recorded output verbatim) |
| Two consecutive live runs byte-identical | `diff -q` on two runs | identical | ✓ PASS |
| Stdlib-only imports | `ast`-based import scan | `{argparse, re, tempfile, pathlib, sys, shutil}`, exit 0 | ✓ PASS |
| `ALL_CHECK_CODES` == `MUTATIONS` codes, both directions | standalone Python equality check | `True` / `True` | ✓ PASS |
| No `pip install` in CI | `grep -c 'pip install' .github/workflows/ci.yml` | `0` | ✓ PASS |
| Working tree unaffected by any mode | `git status --porcelain` before/after all runs | unchanged (only pre-existing, unrelated `.planning/config.json` / GSD state entries) | ✓ PASS |
| **Independent WR-01 (review) reproduction — directory carrier crashes the checker** | scratch `NOTICES.md` with a carrier entry rewritten to `examples` (a directory), run checker | Unhandled `IsADirectoryError`, traceback, exit 1 | ✓ PASS (confirms WR-01 is real; fails loud/non-zero, not silently — see Anti-Patterns) |

### Probe Execution

No `scripts/*/tests/probe-*.sh` convention applies to this phase; `tools/check_repo.py --self-test`, `--mutation-test`, and the live run serve this role and are covered above.

### Requirements Coverage

| Requirement | Source Plan(s) | Description | Status | Evidence |
|---|---|---|---|---|
| CAT-07 | 01-01, 01-06, 01-07 | Citable IDs in two disjoint namespaces, ranges reserved per section | ✓ SATISFIED | `NUMBERING.md` + per-block MC enforcement (Truth #11) + mutation-proven ID checks (Truth #13). |
| EX-01 | 01-01, 01-02, 01-06, 01-07 | Single fictional deal brief supplies canonical facts | ✓ SATISFIED | `examples/deal-brief.md` complete; end-of-file blind spot closed (Truth #10); value-collision ceiling disclosed (Truth #12); mutation-proven (Truth #13). |
| LEG-01 | 01-03 | MIT license covering all original content | ✓ SATISFIED | Unchanged since prior verification; correctly not re-claimed by any gap-closure plan (no gap existed here). |
| LEG-02 | 01-03 | Individually named non-affiliation/trademark statement per framework | ✓ SATISFIED | Unchanged since prior verification; correctly not re-claimed by any gap-closure plan (no gap existed here). |
| LEG-03 | 01-01, 01-03, 01-04, 01-05, 01-07 | Zero proprietary text reproduced; concepts paraphrased, sources cited, mechanically enforced | ✓ SATISFIED | **Previously ENFORCEMENT BLOCKED.** Content unchanged and clean; the no-drift enforcement mechanism now fires against production content and is mutation-proven (Truths #4, #5, #7, #13). |
| LEG-04 | Phase 6 | Legal review gate, MEDDIC-family status reconfirmed | Correctly deferred | Not in scope for Phase 1; `SOURCES.md` names it as owner; the two open WINDOWS.md items are explicitly scoped here. |
| LEG-05 | Phase 6 | README claims/badges sourced only from committed benchmarks | Correctly deferred | Unchanged. |

No orphaned requirements: the union of `requirements:` fields across all seven plans (`CAT-07, EX-01, LEG-01, LEG-02, LEG-03`) exactly matches REQUIREMENTS.md's Phase 1 mapping. LEG-01 and LEG-02 are correctly absent from 01-05/01-06/01-07's `requirements:` fields — they had no open gap, and claiming them there would be manufactured coverage, exactly as the phase's own Source Coverage Audit states.

**Note on `.planning/REQUIREMENTS.md`'s current on-disk state:** the checkboxes and traceability table for `CAT-07`, `EX-01`, `LEG-01`, `LEG-02`, `LEG-03` still read `[ ]` / `Gaps Found` (set by commit `80cc1cb`, a blanket revert made when the BLOCKER was found). That revert predates this round's gap-closure work and has not been re-applied since. This verification's finding is that all five are now SATISFIED; updating `REQUIREMENTS.md` to reflect that is expected to follow from this report, not a gap this report itself needs to hold open.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `tools/check_repo.py` | `check_pointer()` (~412-414) | A carrier entry that resolves to an existing directory (e.g. `.`, or an entry like `examples`) is not rejected by `_carrier_is_repo_relative()` and is not filtered by `p.exists()` (directories exist too); `p.read_text()` then raises an unhandled `IsADirectoryError`, crashing the checker instead of reporting a violation. **Independently reproduced by this verifier** (not merely re-stated from 01-REVIEW.md's WR-01): a scratch `NOTICES.md` naming `examples` as a carrier produces a full traceback and exit 1. | ⚠️ WARNING | Fails **loud and non-zero** — a documentation-editing mistake in `NOTICES.md`'s carrier list turns CI red with a traceback rather than silently passing, which is the opposite failure mode from the phase's original BLOCKER (silent green). Not currently exploited — today's `NOTICES.md` carrier list names only files. Reasonable to leave open per 01-REVIEW.md's own severity classification; a future carrier-list edit that names a directory would need a code fix (`is_file()` check), not a content fix. |
| `tools/check_repo.py` | `_carrier_is_repo_relative()` (~367-379) | The containment guard is lexical only (rejects absolute paths, drive letters, `..` segments) and does not call `.resolve()`, so a committed symlink pointing outside the repository, named as a carrier, would be followed by `check_pointer()`. | ⚠️ WARNING | Theoretical and low-impact per 01-REVIEW.md's own analysis (bounded to a DoS/crash risk on a hostile symlink target, not data exfiltration, since matched content is never echoed back); requires a coordinated two-file change (new symlink + matching NOTICES.md entry) that would be visible in the same diff/PR review. Not currently exploited. |
| `tools/check_repo.py` | `check_pointer()` (~408-410) | Dead defensive branch: `if pointer is None: return violations` is unreachable because the only caller (`run_notices_checks`) already short-circuits to a `pointer-unparseable` violation before ever calling `check_pointer` with a `None` pointer. | ℹ️ INFO | No functional impact today; a latent false-green surface only if a future call site forgot the precondition. Not a phase-1 blocker. |
| `tools/check_repo.py` | `mutation_test()` / `self_test()` | `_mutate_pointer_unparseable` exercises only one of `pointer-unparseable`'s two trigger conditions (missing fenced block); the second trigger (an escaping carrier path) is proven live only by `self_test()`'s `_escaping_notices()` fixture, not by the mutation harness against production content. | ℹ️ INFO | The code itself is proven live by the combination of both harnesses — no violation code is unproven overall. An asymmetry in which harness proves which branch, not a coverage gap in the sense the phase was closing. Optional follow-up, not required. |

No `TBD`/`FIXME`/`XXX` debt markers found in any phase-1 file (the one `grep` hit for "placeholder" in `README.md` is the phrase "this repository does not ship empty placeholder files," a false positive on the keyword, not a debt marker).

## Assessment of the prior BLOCKER (CR-01) and its closure

The prior verification's BLOCKER is closed and independently re-confirmed in this session, not accepted on the strength of 01-05-SUMMARY.md's own claims. The specific empirical reproduction that previously produced `check_repo: 0 violations` after deleting the pointer line from `README.md` now produces `pointer-missing README.md does not contain the attribution pointer string`, exit 1 — re-run fresh in this session against the current `tools/check_repo.py` and the current `README.md`, not copied from any prior report. The fix mechanism matches what the plan and both prior reports describe: `parse_notices()` now scopes extraction to the `Attribution pointer` section body via `split_sections()` (the house idiom `parse_deal_brief()`/`parse_numbering()` already used), rather than a regex anchored directly to the heading line, and a `pointer-unparseable` code now fails loud on any unusable pointer definition instead of silently returning `[]`.

## Assessment of the three prior WARNINGs

- **`in_canonical` end-of-file blind spot** — closed and independently re-confirmed (Truth #10, Mutation 4). The exempt region is now bounded by the table's own row shape (blank or pipe-prefixed lines), with a heading match still an additional exit — matching 01-06's stated action precisely.
- **WR-01 (MC aggregate range)** — closed and independently re-confirmed (Truth #11, MC gap/boundary tests). `mc_ranges` is a per-dimension dict; the aggregate `mc_range` key no longer exists in the parsed data.
- **WR-02 (unlisted-figure value collision)** — deliberately and reasonably deferred as disclosure-only, per the plan's own explicit rationale (implementing the stronger key-binding fix would rewrite the frozen `## Canonical figures` interface D-10 designates as an API, and would rewrite content 01-02 shipped and the original verifier confirmed). The disclosure itself is verified: the docstring states the ceiling, and a fixture pins the accepted-collision behavior. This is not scored as a closed gap in the sense of "the underlying limitation was removed" — it was never claimed to be — but as "the limitation is now honestly declared," which is exactly what was asked for.

## Assessment of two new WARNINGs surfaced by 01-REVIEW.md's gap-closure re-review

Both are independently reproduced by this verifier in this session (see Behavioral Spot-Checks and Anti-Patterns above), not merely re-stated from 01-REVIEW.md. Neither undermines a Phase-1 success criterion: both fail loud (non-zero exit, in one case a traceback) rather than silently passing, which is the structurally different — and structurally safer — failure mode from the class of defect this entire gap-closure round exists to eliminate (a check that is present, named as covered, and produces zero signal). Correctly left open as WARNINGs rather than escalated, consistent with 01-REVIEW.md's own severity classification, and correctly not assigned to any of 01-05/01-06/01-07 since they are new findings from the gap-closure code itself, discovered only after that code shipped.

## Human Verification Required

### 1. Name-collision web search over the 9 invented names

**Test:** Search the web for `Halverton Mutual`, `Kestrel Systems Group`, `Ardent Digital`, `Vantage Nine Consulting`, `Diane Osoria`, `Marcus Feld`, `Priya Raghunathan`, `Tom Weatherly`, `Gina Almeida`.
**Expected:** None matches an existing company or a real identifiable person in insurance, retirement services, or systems integration.
**Why human:** Requires live network access this verifier lacks. Carried forward unchanged from the prior verification and from `.planning/WINDOWS.md` item 1 (`open`). Not a Phase-1 success-criterion blocker; scoped to "before the repository goes public" / LEG-04.

### 2. Independent comparison read-through of `examples/deal-brief.md`

**Test:** An independent reviewer (not the executor who wrote the text) reads the brief end to end.
**Expected:** No sentence compares two real companies or two real products; VMware vSphere/Oracle Database/AWS products appear only as migration source/target.
**Why human:** The originating plan requires an independent reviewer distinct from the author; the self-review already performed is a substitute, not the specified check. Carried forward unchanged from the prior verification and from `.planning/WINDOWS.md` item 2 (`open`). Not a Phase-1 success-criterion blocker; scoped to LEG-04.

### 3. Docstring-honesty read-through of `tools/check_repo.py`'s ten violation-code entries

**Test:** Read the module docstring's ten violation-code entries (lines 23-75) end to end and confirm each declared ceiling and behavior description matches what the code currently does.
**Expected:** No entry promises a guarantee the code does not deliver; both declared blind spots (bare-count, value-collision) and the code-point-equality/no-normalization rule read as accurate.
**Why human:** Newly harvested from 01-06-PLAN.md Task 3's `<verify><human-check>` block, which explicitly states this is "a judgment a grep cannot make" and was deferred from an in-task human checkpoint to end-of-phase. This verifier independently cross-read all ten entries against the corresponding functions (`check_dup_id`, `check_range_id`, `check_revived_id`, `check_undefined_id`, `check_dup_figure_key`, `check_figure_order`, `check_unlisted_figure`, `check_pointer`, `run_notices_checks`) and found each entry consistent with current behavior — but the plan's own design calls for independent human sign-off on this specific judgment, not the executor's or this verifier's self-assessment, given that a docstring/code mismatch is exactly the class of unenforced, prose-only claim the phase's original BLOCKER was built from.

## Gaps Summary

No gaps remain. The prior BLOCKER and both prior WARNINGs are closed and independently re-confirmed by fresh adversarial reproduction in this session (not by re-reading the plans' or summaries' own claims). A new regression class — a `--mutation-test` harness that injects one named defect per violation code into a copy of the real repository and is itself proven fail-first — is now wired into CI, closing the structural failure mode (a check that exists, is named as covered, runs in CI, and cannot fire) rather than only today's instances of it.

Two new WARNINGs surfaced by the gap-closure re-review (a directory-carrier crash, a lexical-only symlink-containment check) were independently reproduced and correctly assessed as non-blocking: both fail loud and non-zero rather than silently passing, neither is exploited by current repository content, and both require either a documentation-editing mistake or a coordinated two-file PR to trigger.

Overall status is `human_needed`, not `passed`, solely because three legitimate human-verification items remain open: two pre-existing items already logged in `.planning/WINDOWS.md` (name-collision search, independent comparison read-through — both explicitly scoped to pre-launch/LEG-04, not Phase-1 success criteria) and one newly harvested planner-deferred human-check (docstring honesty read-through, from 01-06-PLAN.md Task 3). Per the verification decision tree, any non-empty human-verification list routes the phase to `human_needed` even when every other truth is independently verified — which is the case here.

---

_Verified: 2026-09-10T11:15:00Z_
_Verifier: Claude (gsd-verifier)_
