---
phase: 04-distribution-worked-examples
reviewed: 2026-09-17T00:00:00Z
depth: standard
files_reviewed: 10
files_reviewed_list:
  - .claude-plugin/marketplace.json
  - .claude-plugin/plugin.json
  - .github/workflows/ci.yml
  - README.md
  - examples/before-after.md
  - output-styles/proof-first.md
  - prompts/system-prompt.md
  - skills/proof-first/references/worked-examples.md
  - tools/check_repo.py
  - tools/generate_derivatives.py
findings:
  critical: 1
  warning: 2
  info: 1
  total: 4
status: issues_found
---

# Phase 4: Code Review Report

**Reviewed:** 2026-09-17
**Depth:** standard
**Files Reviewed:** 10
**Status:** issues_found

## Summary

This phase closed seven UAT gaps: three example-prose codes (04-07), three README codes
(04-09), and three repair items (04-10) — `_owner_segment` URL normalisation, byte-level
comparison in `generate_derivatives.py --check`, and two plugin-manifest ceiling disclosures.

I re-ran `check_repo.py --self-test`, `--mutation-test`, a plain run, and
`generate_derivatives.py --check` against the working tree: all four pass exactly as CI
expects (47 codes discrimination-proven, 0 violations, both derivatives byte-identical to a
fresh render). That is real evidence the shipped gate is green, but it is not evidence the
gate's own coverage is complete — the self-test and mutation-test only prove each check fires
on the one mutation its own fixture applies, not that the check's scope matches what its
docstring or its caller-facing name claims.

Working from that distinction, I found one place where `check_plugin_manifest_invalid`'s
implementation covers meaningfully less than its docstring and its own violation-code name
promise — a marketplace.json plugin entry can be missing most of its required distribution
metadata (`name`, `displayName`, `author`, `license`, `keywords`, `description`) and the
checker reports zero violations, which I reproduced directly against a scratch copy of the
repository. Given this project's own stated bar ("a check whose docstring promises more than
its implementation delivers is a real defect of the same class as an unmeasured marketing
claim"), I am treating this as a blocker rather than a nitpick. I also found one shipped
worked-example (`MC-31` in `worked-examples.md`) with a punctuation defect that makes its
"after" sentence read as two disconnected fragments, inconsistent with the correctly-punctuated
analogous instance in `examples/before-after.md`.

Everything else I checked — `_owner_segment`'s four-URL-form normalisation, the byte-comparison
fix in `generate_derivatives.py --check`, the new example-prose checks
(`example-sentence-length`, `before-after-spelled-count`, `example-rule-narration`), and the
three new README structural checks — held up under adversarial reading: edge cases I traced by
hand (SSH remote form, scheme-less form, trailing `.git`, proper-noun exemption in the
spelled-cardinal check, zero-line-difference truncation in the byte-diff reporter) all resolved
the way the docstrings claim, and the declared ceilings in those docstrings are, as far as I
could verify, honestly stated.

## Critical Issues

### CR-01: `check_plugin_manifest_invalid` does not validate marketplace.json's plugin-entry required fields

**File:** `tools/check_repo.py:2617-2702` (the `plugins[0]` handling at lines 2687-2700, and
`PLUGIN_REQUIRED_KEYS` at lines 2610-2613)

**Issue:** `PLUGIN_REQUIRED_KEYS = ('name', 'displayName', 'description', 'version', 'author', 'homepage', 'repository', 'license', 'keywords')` is enforced only against the top-level `.claude-plugin/plugin.json` object (line 2643: `for key in PLUGIN_REQUIRED_KEYS:` iterates `plugin_data`). For `.claude-plugin/marketplace.json`'s nested plugin entry (`marketplace_data['plugins'][0]`), the only field ever inspected is `source` (line 2695-2700); `name`, `displayName`, `author`, `license`, `keywords`, and `description` on that same object are never checked for presence at all. `check_plugin_manifest_version` separately checks `version`, and `check_publish_location_drift` separately checks `homepage`/`repository`'s *owner segment* — but nothing checks that those two fields, or the six named above, are even present on the marketplace entry.

The function's own docstring says it asserts "both plugin manifests are well-formed: valid JSON, every required key present" — that claim is false for marketplace.json's plugin entry. I reproduced this directly: in a scratch copy of the repository, deleting `license`, `keywords`, `author`, and `displayName` from `.claude-plugin/marketplace.json`'s `plugins[0]` object and re-running `python3 tools/check_repo.py` reports `0 violations`. A marketplace.json in this state would very likely fail a real `claude plugin marketplace add` / `claude plugin install` call (per the Claude Code plugin manifest schema this project's own `plugin.json` already conforms to), yet the project's sole automated gate for manifest validity is silent about it. This is exactly the class of defect the project's own review brief calls out: a check whose docstring promises more than its implementation delivers.

**Fix:** Enforce the same required-key set (or a `MARKETPLACE_PLUGIN_ENTRY_REQUIRED_KEYS` subset, if some fields are intentionally marketplace-entry-optional — but that intent isn't stated anywhere today) against `plugins[0]`, the same way `PLUGIN_REQUIRED_KEYS` is enforced against `plugin_data`:

```python
        if 'plugins' in marketplace_data:
            plugins = marketplace_data['plugins']
            if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
                violations.append((MARKETPLACE_MANIFEST_PATH, (
                    f"plugin-manifest-invalid {MARKETPLACE_MANIFEST_PATH} 'plugins' must be a "
                    f"list of exactly one object"
                )))
            else:
                entry = plugins[0]
                for key in PLUGIN_REQUIRED_KEYS:
                    if key not in entry:
                        violations.append((MARKETPLACE_MANIFEST_PATH, (
                            f"plugin-manifest-invalid {MARKETPLACE_MANIFEST_PATH}'s plugin "
                            f"entry is missing required key '{key}'"
                        )))
                source = entry.get('source')
                if source != './':
                    ...
```
Add a mutation-test fixture (e.g. `_mutate_plugin_manifest_invalid` variant deleting `license` from `marketplace.json`'s entry rather than from `plugin.json`) so the new coverage is discrimination-proven, matching this project's own stated CI bar rather than just fixing the code silently.

## Warnings

### WR-01: Worked example MC-31 has a broken attribution sentence

**File:** `skills/proof-first/references/worked-examples.md:141-142`
**Issue:** The ✓ column reads: `"Marcus Feld, Halverton Mutual's Vice President of Infrastructure, said in discovery. 'We need a landing zone we can actually govern — right now every VM is a snowflake.'"` — the period after "discovery" instead of a colon leaves the quoted material unintroduced, reading as two disconnected sentences rather than an attributed quote. The analogous instance in `examples/before-after.md:34` gets this right: `"Marcus Feld, Vice President of Infrastructure, said in discovery: 'We need a landing zone we can actually govern'."` This file is cited from `SKILL.md`'s own "Reference files" section ("Before writing or checking a ✗/✓ contrast for a rule, read `references/worked-examples.md`") and from the derived `output-styles/proof-first.md`/`prompts/system-prompt.md` bundles are *not* built from it (it's the one deliberately-omitted source) — but a live skill session, or a human contributor, reading this file directly inherits the malformed sentence as a model for how to write the rule.
**Fix:** Replace the period with a colon: `"...said in discovery: 'We need a landing zone we can actually govern — right now every VM is a snowflake.'"`

### WR-02: marketplace.json/plugin.json field duplication has no drift guard beyond version and homepage/repository

**File:** `tools/check_repo.py:2617-2702`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
**Issue:** `plugin.json` and `marketplace.json`'s plugin entry both carry hand-duplicated copies of `description`, `displayName`, `author`, `license`, and `keywords` today, and they currently agree. Nothing in `check_repo.py` asserts they *stay* agreeing — only `version` (via `check_plugin_manifest_version`) and the owner segment of `homepage`/`repository` (via `check_publish_location_drift`) are cross-checked between the two files. A future edit to one manifest's `description` or `keywords` without the matching edit to the other would ship silently. This is a narrower, related instance of CR-01 — even after CR-01 is fixed (which would restore *presence* checking on marketplace.json's entry), nothing enforces *equality* between the two files' duplicated content.
**Fix:** Either (a) after fixing CR-01, add an explicit `plugin-manifest-invalid` (or a new code) equality check comparing `plugin_data`'s `description`/`displayName`/`author`/`license`/`keywords` against `marketplace_data['plugins'][0]`'s same fields, firing once per disagreeing field; or (b), if this asymmetry is intentional (e.g., a marketplace listing is allowed to state its own description), disclose that explicitly in the docstring as a declared ceiling, matching this file's own convention everywhere else.

## Info

### IN-01: `check_before_after_spelled_count`'s docstring measurement is ambiguous about pre- vs. post-exemption counting

**File:** `tools/check_repo.py:2409-2432`
**Issue:** The docstring states "a per-rule illustrative pair reads naturally with a spelled count -- 5 such occurrences were measured" to justify excluding `skills/**` from this check's scope. I reproduced this by hand: running the check's own regex and proper-noun exemption logic against every ✗/✓ line under `skills/proof-first/references/`, the *raw* match count is 5 (`five`, `Three`, `five`, `three`, `Nine` — the last of these is `Vantage Nine Consulting`, a proper noun the check's own exemption logic would not flag as a violation if the check applied there). The *post-exemption* violation count is 4. The docstring's "5" is defensible under a raw-match reading but is not disambiguated, and a reader auditing this specific number (as the project's own stated standard for headline numbers asks for) cannot tell from the docstring alone which of the two methodologies produced it.
**Fix:** State explicitly whether "5" counts raw regex matches or would-be violations after the proper-noun exemption, e.g. "5 raw regex matches were measured, one of which (`Nine`, in `Vantage Nine Consulting`) the proper-noun exemption would also excuse if this check applied there."

---

_Reviewed: 2026-09-17_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
