---
phase: 03-completeness-audit-artifact-patterns
reviewed: 2026-09-14T00:00:00Z
depth: standard
files_reviewed: 8
files_reviewed_list:
  - NUMBERING.md
  - README.md
  - skills/proof-first/SKILL.md
  - skills/proof-first/references/artifact-patterns.md
  - skills/proof-first/references/checklist.md
  - skills/proof-first/references/completeness-audit.md
  - skills/proof-first/references/worked-examples.md
  - tools/check_repo.py
findings:
  critical: 0
  warning: 1
  info: 1
  total: 2
status: issues_found
---

# Phase 3: Code Review Report

**Reviewed:** 2026-09-14
**Depth:** standard
**Files Reviewed:** 8
**Status:** issues_found

## Summary

Reviewed the five new/changed Markdown documents (NUMBERING.md, README.md, SKILL.md,
artifact-patterns.md, checklist.md, completeness-audit.md, worked-examples.md) and the one code
file, `tools/check_repo.py`, at standard depth, with targeted deep-dive verification on the
review's stated priority target: the `_three_way_id_diff` shared helper backing both
`check_catalog_id_drift` (PF) and the new `check_mc_catalog_id_drift` (MC), the parameterized
`parse_checklist`, and the five new violation codes (`mc-catalog-id-drift`, `mc-rule-in-skill`,
`mc-count-unstated`, `mc-count-mismatch`, `artifact-family-section-missing`).

Verification performed beyond static reading:
- Ran `python3 tools/check_repo.py --self-test`, `--mutation-test`, and a bare live run. All three
  pass exactly as claimed: self-test covers all 27 codes, mutation-test reports "27 codes
  discrimination-proven" with a clean (0-violation) control copy and no fire-only codes, and the
  live run reports `0 violations`.
- Diffed the PF-path refactor (`git show 79e9613`) to confirm `check_catalog_id_drift`'s message
  text and comparison logic are byte-for-byte unchanged after being extracted into
  `_three_way_id_diff` — the commit message's "byte-identical message text and behavior" claim
  holds up under inspection.
- Confirmed the `PF-` and `MC-` ID regexes (`PF_ID_RE`, `MC_ID_RE`) and the heading regexes
  (`RULE_HEADING_RE`, `MC_HEADING_RE`) cannot alias each other (disjoint prefixes, anchored
  patterns), and that the heading regexes' em dash (`\xe2\x80\x94`, U+2014) matches the actual
  byte sequence used in `SKILL.md` and `completeness-audit.md`'s headings — a plausible failure
  mode (en dash/hyphen substitution silently defeating heading detection) that is not present.
- Manually cross-footed every count NUMBERING.md states against its own Allocated IDs table (PF
  section counts/next-free values, MC dimension-block counts) and against the frozen
  stated-count sentences in `SKILL.md` ("31 rules in 6 numbered sections") and
  `completeness-audit.md` ("8 checks across 8 dimensions") — all agree.
- Confirmed `parse_checklist`'s new `section_name` parameter is additive-only: both pre-existing
  PF call sites still pass no argument and get the same `'PF rules'` default, and the one new MC
  call site passes `'MC rules'` explicitly; there is no code path where a PF call site could read
  the MC table or vice versa (they key off distinct heading strings via `split_sections`).
- Confirmed empty/absent-set handling: an MC namespace with no `completeness-audit.md` for a
  skill folder returns early before computing any set (required precisely because the majority of
  self-test fixture roots allocate MC rows in `NUMBERING.md` with no MC reference file present),
  and a `checklist.md` missing the `'## MC rules'` section degrades to an empty set rather than
  raising, which the three-way diff still handles correctly (reports every allocated/defined ID as
  missing from the checklist).

No blockers were found. Two non-blocking issues are reported below: one internal-consistency
defect in `tools/check_repo.py`'s own top-of-file documentation (a stale claim contradicted by
the file's own `KNOWN_OPEN_VIOLATIONS` comment and confirmed stale by the live run), and one
minor formatting inconsistency in `README.md`'s repository-layout tree.

## Warnings

### WR-01: Stale, self-contradictory claim in check_repo.py's own violation-code docstring

**File:** `tools/check_repo.py:260-267`
**Issue:** The module docstring's entry for `skill-token-budget-exceeded` states: "As of this
writing this code fires against this repository's own skills/proof-first/SKILL.md — a known,
tracked, open finding against CAT-08 (see .planning/WINDOWS.md), not a defect in this check."
This is no longer true and contradicts two other places in the same file:

1. The `KNOWN_OPEN_VIOLATIONS` comment block (`tools/check_repo.py:1380-1399`) explicitly says
   this finding "is now closed -- 02-07's trim brought the file under the 5,000-token ceiling,"
   and `KNOWN_OPEN_VIOLATIONS` itself is an empty `frozenset()`.
2. The `_mutate_skill_token_budget_exceeded` mutation's own docstring
   (`tools/check_repo.py:1707-1714`) says "The control copy is under the ceiling (3,694 words /
   4,802 estimated tokens as of 02-07's trim, a 198-token margin below the 5,000-token ceiling)."

A live run confirms the docstring is the stale one: `skills/proof-first/SKILL.md` is currently
3,665 words / an estimated 4,764 tokens (236-token margin under the 5,000 ceiling), and
`python3 tools/check_repo.py` reports `0 violations` — `skill-token-budget-exceeded` does not
fire against the real repository today. This predates Phase 3 (the docstring text was not
touched by any of the three Phase 3 commits), but it is a real, currently-shipping inconsistency
in a file this phase modified extensively, and it will mislead a future contributor who reads the
top-of-file catalog as the source of truth for "which checks are currently failing against this
repo."
**Fix:** Delete or rewrite the stale sentence to match the `KNOWN_OPEN_VIOLATIONS` block's
account, e.g.:
```python
#   ... never the more favourable of several. This check previously fired
#   against this repository's own skills/proof-first/SKILL.md; that finding
#   was closed by 02-07's trim (see KNOWN_OPEN_VIOLATIONS above) and the
#   check is silent against the current file.
```

## Info

### IN-01: Inconsistent (exists)/(planned) tagging in README.md's repository-layout tree

**File:** `README.md:56-84`
**Issue:** The repository-layout tree is introduced with "Entries marked 'planned' are
documented here but not yet created," implying tagged vs. untagged carries meaning. Most rows
follow that convention (`examples/deal-brief.md (exists)`, `.claude-plugin/ (planned)`,
`tools/check_repo.py (exists)`, `LICENSE (exists)`, etc.), but several rows that indisputably
exist today carry no tag at all: `SKILL.md`, all five files under `references/` (including the
two this phase added, `completeness-audit.md` and `artifact-patterns.md`, which lost their
`(planned)` tag in this phase's diff but did not gain an `(exists)` one), and
`evals/pressure-tests.md`. The "What exists today" bullet list two paragraphs above resolves the
ambiguity for a careful reader, but the tree itself is not internally self-consistent about its
own tagging convention.
**Fix:** Either tag every existing entry with `(exists)` for consistency with the rows that
already carry it, or drop the tag from every existing entry (relying solely on the absence of
`(planned)`) and state that convention explicitly in the paragraph above the tree.

---

_Reviewed: 2026-09-14_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
