---
phase: 04-distribution-worked-examples
reviewed: 2026-09-18T00:00:00Z
depth: standard
files_reviewed: 10
files_reviewed_list:
  - .claude-plugin/marketplace.json
  - .claude-plugin/plugin.json
  - .github/workflows/ci.yml
  - examples/before-after.md
  - output-styles/proof-first.md
  - prompts/system-prompt.md
  - README.md
  - skills/proof-first/references/worked-examples.md
  - tools/check_repo.py
  - tools/generate_derivatives.py
findings:
  critical: 0
  warning: 0
  info: 0
  total: 0
status: clean
---

# Phase 4: Code Review Report

**Reviewed:** 2026-09-18
**Depth:** standard
**Files Reviewed:** 10
**Status:** clean

## Summary

This is a re-review of the 04-11 gap-closure round that followed my predecessor's report
(CR-01 critical, WR-01/WR-02 warnings, IN-01 info). Only two files changed in the four commits
under review — `tools/check_repo.py` and `skills/proof-first/references/worked-examples.md` — so
I scoped adversarial effort there and re-examined the other eight files only for whether the
change could have invalidated the prior "sound" verdict (it could not: nothing else in this
diff touches manifests, README, output-styles, system-prompt, or `generate_derivatives.py`).

I did not accept the orchestrator's green-gate reproduction (`--self-test`, `--mutation-test`,
plain run, `generate_derivatives.py --check`) as sufficient on its own — per this project's own
standard, a green gate proves the gate passes, not that its coverage matches what its docstring
claims, which is precisely the class of defect CR-01 was. I independently re-derived each of the
five specific claims flagged for audit by loading `check_repo.py` as a module and exercising its
own fixture-builder functions and constants directly, rather than trusting the self-test's own
PASS/FAIL narration:

1. **CR-01 docstring/implementation match.** Read `check_plugin_manifest_invalid`'s full
   docstring (`tools/check_repo.py:2645-2683`) against its body (`2684-2818`) line by line,
   including the module-level "Violation codes implemented in this file" contract
   (`tools/check_repo.py:389-427`). Both now state exactly what the code does: `PLUGIN_REQUIRED_KEYS`
   enforced at two positions (plugin.json top-level, marketplace.json's `plugins[0]`), and
   `MARKETPLACE_ENTRY_EQUAL_KEYS` enforced once both objects parse. No claim in either docstring
   exceeds what I could trace in the implementation.

2. **`MARKETPLACE_ENTRY_EQUAL_KEYS` exclusion of `homepage`/`repository`.** The exclusion is
   disclosed in both docstrings, with the stated reason (`check_publish_location_drift` already
   owns owner-segment equivalence across four URL syntaxes, so an exact-string check on these two
   fields would misfire on `_mixed_url_form_manifests`). I confirmed this is literally true of the
   code: that fixture writes `plugin.json`'s `repository` as an SSH remote
   (`git@github.com:acme/proof-first.git`) and `marketplace.json`'s plugin-entry `repository` as
   an HTTPS URL naming the same owner — two different strings. Running the real
   `check_plugin_manifest_invalid` against that fixture root confirms it stays silent (matching
   the self-test's own `plugin_mixed_url_codes` assertion), and I traced by hand that including
   `repository` in the equality set would have made these two literal strings compare unequal and
   misfire, exactly as claimed.

3. **The 18-cell required-key matrix.** `PLUGIN_REQUIRED_KEYS` has 9 members; the matrix iterates
   it against the same two literal position strings the production docstring names. I instantiated
   `_required_key_matrix_root` directly for all 9×2=18 combinations and ran `run_all_checks`
   against each: all 18 cells fired `plugin-manifest-invalid`, zero misses, and the loop iterates
   the actual `PLUGIN_REQUIRED_KEYS` constant rather than a hand-copied duplicate list, so there is
   no drift risk between the matrix and the production check it's proving.

4. **The 47-code total and set-vs-list semantics.** `MUTATIONS` is a 48-row list containing two
   rows for `plugin-manifest-invalid` (one deleting a key from `plugin.json`, the new one deleting
   a key from `marketplace.json`'s entry) — 47 unique codes. `discrimination_proven` is
   constructed as a Python `set`, so both rows firing the same code collapse to one membership,
   preserving 47 for the reason claimed (set semantics), not because a row was silently dropped
   from `ALL_CHECK_CODES` or `MUTATIONS`.

5. **MC-31's repair.** The new two-sentence form ("...said in discovery: '...govern'. He added:
   'Right now every VM is a snowflake'.") splits under `check_example_sentence_length`'s own
   `SENTENCE_SPLIT_RE` into a 20-word and a 9-word sentence — both well inside PF-4.1's 25-word
   ceiling, confirmed by running the check's actual regex constants against the line rather than
   counting by eye. The repair also isn't an isolated stylistic choice: `examples/before-after.md`
   already uses the identical "said in discovery: '...'. He added: '...'." construction for the
   same Marcus Feld quote, so `worked-examples.md` now matches the established in-repo pattern
   rather than inventing a new one.

I also directly reproduced the mutation this round added
(`_mutate_marketplace_entry_required_key_missing`, deleting `license` from the real
`marketplace.json`'s entry) against a scratch copy of the actual repository and confirmed it
fires exactly one `plugin-manifest-invalid` line, with no double-report from the new equality
guard (the guard's `key in entry` condition correctly excludes an already-missing key from also
being compared for equality). I did the same for the WR-02 drift fixture
(`_marketplace_entry_field_drift_manifests`): it fires exactly the one expected
`plugin-manifest-invalid ... 'keywords' differs ...` line, plus the pre-existing incidental noise
that minimal fixture roots already carry (missing LICENSE, missing NOTICES.md subsections) — no
new unexpected code.

All four prior findings (CR-01, WR-01, WR-02, IN-01) are genuinely closed, not merely
gate-green: I found no gap between what the round's docstrings now claim and what the code does,
no new coverage hole in the mutation/self-test matrices this round added, and no factual error in
the newly-stated numbers (the "5 raw matches / 4 would-be violations" split in
`check_before_after_spelled_count`'s docstring reproduces exactly against the real
`skills/proof-first/references/` tree). I found nothing new to report in this round's diff.

## Critical Issues

None.

## Warnings

None.

## Info

None.

---

_Reviewed: 2026-09-18_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
