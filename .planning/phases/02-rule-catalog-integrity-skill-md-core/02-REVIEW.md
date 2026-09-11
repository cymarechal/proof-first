---
phase: 02-rule-catalog-integrity-skill-md-core
reviewed: 2026-09-11T00:00:00Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - tools/check_repo.py
  - skills/proof-first/SKILL.md
  - skills/proof-first/references/checklist.md
  - skills/proof-first/references/deletion-test.md
  - NUMBERING.md
  - README.md
  - evals/pressure-tests.md
findings:
  critical: 3
  warning: 3
  info: 2
  total: 8
status: issues_found
---

# Phase 02: Code Review Report

**Reviewed:** 2026-09-11T00:00:00Z
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Summary

`tools/check_repo.py`'s 8 new checks (`parse_frontmatter`/`check_frontmatter`, `check_catalog_count`,
`check_skill_too_long`, `check_skill_token_budget`, and the `parse_pf_subblocks` extension to
`check_range_id`) are, on direct inspection and by execution (`--self-test`, `--mutation-test`, and
a bare live run — all run against this checkout), functionally correct at their stated boundaries:
the description-length check is silent at exactly 200 and exactly 1024 characters and fires one
character past either bound; `skill-too-long` is silent at exactly 500 lines and fires at 501; a
repeated top-level frontmatter key is reported as a violation rather than silently last-value-wins
merged; the sub-block containment extension to `range-id` correctly fires when an ID lands in a
declared gap. `NUMBERING.md`'s Allocated-IDs counts, `SKILL.md`'s 31 rule headings, and
`references/checklist.md`'s 31 rows are all mutually consistent (verified by grep cross-check and
by the live `catalog-id-drift`/`catalog-count-mismatch` checks both reporting zero violations).

Three problems earn BLOCKER status. First, the orchestrator's suspicion about
`_mutate_skill_token_budget_exceeded` is confirmed by direct experiment (see CR-01): the mutation
is provably vacuous for this one code, so the tool's own printed claim `mutation-test PASS: 21 codes
proven live` is false for that code — the exact class of overclaim this project's "measured claims
or no claims" constraint exists to prevent, coming from the project's own integrity-checking tool.
Second, the new `frontmatter-description-invalid` check's docstring claims coverage (the case where
`description` is entirely absent) that the code does not actually implement — demonstrated by a
direct test, this is the same class of defect Phase 1's verification caught (a check named as
covered that cannot fire for part of what it claims). Third, `README.md`'s prose "Status" section
was left uncorrected by this same diff even though the diff rewrote the adjacent tree diagram to
mark `skills/proof-first/` and `evals/pressure-tests.md` as existing — the file is now internally
self-contradictory about whether the skill has been written.

Three WARNING-level and two INFO-level findings follow below.

## Critical Issues

### CR-01: `mutation-test`'s proof for `skill-token-budget-exceeded` is vacuous — the printed "21 codes proven live" claim is false for this code

**File:** `tools/check_repo.py:1320-1332` (mutation function), `:1356` (registration), `:1372-1410` (`mutation_test`, including the `PASS` print at `:1404-1405`)

**Issue:** Every other mutation follows clean-control → mutated-copy → fires, which genuinely
demonstrates the check can distinguish good data from bad. `skill-token-budget-exceeded` cannot
follow that shape because the real `skills/proof-first/SKILL.md` already exceeds the 5,000-token
estimate before any mutation runs (confirmed live: `skill-token-budget-exceeded ... is estimated at
6207 tokens ... exceeding the 5000-token ceiling`; `mutation-test CONTROL: 1 violations on the
unmutated copy (1 known-open ...)`). The mutation function's own docstring acknowledges this and
asserts the test still "registers a named, independent defect so the code is proven to react to a
fresh injected change, not merely to already-present content" — but `mutation_test`'s actual
assertion (`fired = any(... code ...)`) only checks whether the code fires on the mutated copy at
all, which it already does regardless of whether the mutation ran. Direct proof, run against this
checkout, with the mutation function replaced by a no-op:

```
fired with NO mutation applied at all: True
```

So `mutation-test OK: skill-token-budget-exceeded ...` — and therefore the final
`mutation-test PASS: 21 codes proven live` — asserts something the test did not actually establish
for this one code. This is not a cosmetic nit: this repository's stated governing constraint is
"any headline number must be reproducible ... with honest caveats stated," and this tool is the
thing enforcing that constraint elsewhere in the repo. Its own "21 codes proven live" headline
number is inaccurate for this code.

**Fix:** Make the control state for this one mutation genuinely clean before mutating, so the test
regains discriminating power, e.g. trim the scratch copy's `SKILL.md` under the ceiling first (or
swap in a synthetic under-ceiling fixture, the same technique `_token_budget_good_skill`/
`_token_budget_bad_skill` already use in `self_test`) before appending filler:

```python
def _mutate_skill_token_budget_exceeded(root):
    """Force the control state under the ceiling first, then push it back over --
    so this mutation is clean -> fires like every other mutation, instead of
    fire -> fire against a file that already violates this check."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    # ... trim body content to a synthetic under-ceiling word count here ...
    if not text.endswith('\n'):
        text += '\n'
    text += '\n' + ' '.join(['filler'] * 2000) + '\n'
    path.write_text(text, encoding='utf-8')
```

At minimum, if trimming is judged out of scope for this phase, do not let the tool claim more than
it proved: exclude this code from the "N codes proven live" count and print it as a separately
labelled, honest caveat (e.g. `"20 codes discrimination-proven; 1 code (skill-token-budget-exceeded)
confirmed to fire but not discrimination-proven — see KNOWN_OPEN_VIOLATIONS"`).

### CR-02: `frontmatter-description-invalid`'s docstring claims a coverage case ("absent") the code does not implement

**File:** `tools/check_repo.py:144-151` (docstring) vs. `:811-825` (`check_frontmatter`'s description block)

**Issue:** The module docstring states:

```
frontmatter-description-invalid - a skills/*/SKILL.md's frontmatter
                    `description` is absent, empty after whitespace
                    collapse, shorter than 200 characters, or longer
                    than 1024 characters, ...
```

But the code only evaluates description length inside `if 'description' in keys:` — when the key
is truly absent from the frontmatter (not merely empty), this block never runs, and the file's
missing-required-key defect is instead reported under a *different* code,
`frontmatter-unparseable`. Verified directly against this checkout with a fixture SKILL.md that has
a valid `---`-delimited block with `name`/`license` but no `description` key at all:

```
('skills/no-desc/SKILL.md', 'frontmatter-unparseable skills/no-desc/SKILL.md missing required key(s): description')
```

No `frontmatter-description-invalid` violation is ever produced for the "absent" case the docstring
claims this code covers. This is exactly the defect class Phase 1's verification caught: a check
documented as covering a case it cannot actually fire for.

**Fix:** Correct the docstring to state the true boundary — this code fires on present-but-invalid
descriptions only; a fully absent `description` key is `frontmatter-unparseable`'s job:

```
frontmatter-description-invalid - a skills/*/SKILL.md's frontmatter
                    `description` key is present but, after whitespace
                    collapse, is empty, shorter than 200 characters, or
                    longer than 1024 characters, naming the measured
                    length and the bound it broke. A frontmatter with no
                    `description` key at all is frontmatter-unparseable's
                    missing-required-key case, not this code's.
```

### CR-03: `README.md`'s "Status" section is left stale by this same diff and now contradicts its own tree diagram

**File:** `README.md:14-36` (Status / "What exists today" / "What does not exist yet") vs.
`README.md:47-77` (the tree diagram this phase's diff itself edited)

**Issue:** This phase's diff to `README.md` removed the `(planned)` tag from `skills/proof-first/`
in the tree and added `evals/\n│   └── pressure-tests.md` as existing (see the diff: `-│   └──
proof-first/                    (planned)` → `+│   └── proof-first/`, and `-├── evals/
(planned)` → `+├── evals/\n+│   └── pressure-tests.md`). But the prose two sections above it was not
touched and still reads:

> This repository is in early construction. The foundational scaffolding is in place; **the skill
> itself has not been written yet.**
>
> What exists today: `NUMBERING.md`, `examples/deal-brief.md`, `LICENSE`, `NOTICES.md`,
> `SOURCES.md`, `tools/check_repo.py`. [no mention of `skills/proof-first/SKILL.md`, its
> `references/`, or `evals/pressure-tests.md`]
>
> What does not exist yet: **The skill itself.** Its reference files. ... The evaluation harness.

This is now false and self-contradictory within the same file: `skills/proof-first/SKILL.md` is a
368-line, 31-rule catalog this very phase wrote (and `check_repo.py`'s own new
`catalog-count-unstated`/`catalog-id-drift` checks depend on it existing); `references/checklist.md`
and `references/deletion-test.md` exist; `evals/pressure-tests.md` exists. A reader trusting the
prose over the tree three lines below it would conclude the opposite of reality for the exact
deliverable this phase produced.

**Fix:** Update the Status section in the same commit that updates the tree:

```markdown
## Status

This repository is under active construction. `NUMBERING.md`'s rule-ID registry, the
`skills/proof-first/` rule catalog (`SKILL.md`, `references/checklist.md`,
`references/deletion-test.md`), and the integrity checker are in place.

What exists today:

- `NUMBERING.md` — the frozen rule-ID registry.
- `skills/proof-first/SKILL.md` — the 31-rule prose catalog.
- `skills/proof-first/references/checklist.md` — the rule-ID index.
- `skills/proof-first/references/deletion-test.md` — deletion-test edge cases.
- `examples/deal-brief.md` — the one canonical fictional deal every worked example cites.
- `evals/pressure-tests.md` — the trigger-pressure-test method (not yet run; see the file itself).
- `LICENSE`, `NOTICES.md`, `SOURCES.md`.
- `tools/check_repo.py` — a stdlib-only checker enforcing all of the above, wired into CI.

What does not exist yet:

- The distribution manifests (`.claude-plugin/`).
- The output style.
- The paste-able system prompt.
- The worked before-and-after examples.
- A run evaluation benchmark (the pressure-test method exists; no observations are recorded yet).
```

## Warnings

### WR-01: `KNOWN_OPEN_VIOLATIONS` is scoped by violation code only, not by subject — it can mask an unrelated future regression of the same code

**File:** `tools/check_repo.py:1046-1063` (constant and its justifying comment), `:1373-1376`
(control filter)

**Issue:** The comment above `KNOWN_OPEN_VIOLATIONS` calls it "this narrow, named allowance" and
frames it as covering exactly one known fact about one file
(`skills/proof-first/SKILL.md`'s current token estimate). But the actual filter operates purely on
the violation *code*:

```python
unexpected_control_violations = [
    v for v in control_violations
    if v[1].split(' ', 1)[0] not in KNOWN_OPEN_VIOLATIONS
]
```

If a second skill folder is ever added under `skills/*/SKILL.md` and it independently exceeds the
token ceiling for a genuinely new, unrelated reason, `mutation-test`'s control step would silently
swallow that new violation into the "known-open" bucket rather than flagging it as an unexpected
regression — exactly the failure mode the surrounding comment says this allowance is narrow enough
to avoid. There is currently only one skill folder, so the blast radius is latent, not active.

**Fix:** Scope the allowance to the specific `(code, subject)` pair it actually excuses, not the bare
code:

```python
KNOWN_OPEN_VIOLATIONS = frozenset({
    ('skill-token-budget-exceeded', 'skills/proof-first/SKILL.md'),
})
...
unexpected_control_violations = [
    v for v in control_violations
    if (v[1].split(' ', 1)[0], v[0]) not in KNOWN_OPEN_VIOLATIONS
]
```

### WR-02: The live-check CI step exits non-zero on this commit, with no accommodation for the disclosed known-open finding

**File:** `.github/workflows/ci.yml` (third step: `python3 tools/check_repo.py`), caused by
`tools/check_repo.py`'s live run against the state this phase ships

**Issue:** Running the live check against this checkout exits 1:

```
skill-token-budget-exceeded skills/proof-first/SKILL.md is estimated at 6207 tokens (4775 words x 1.3), exceeding the 5000-token ceiling
EXIT:1
```

This is a real, disclosed, tracked finding (`.planning/WINDOWS.md` item 5), not a surprise — but the
CI workflow's third step has no accommodation for it (no `continue-on-error`, no separate
non-gating job, no comment explaining the expected-red state). Every push/PR on this branch will
show a red check from this commit forward until the catalog is trimmed, which is easy to mistake
for an unrelated regression in an unrelated PR.

**Fix:** Either resolve the token-budget finding before merging this phase's output past CI-gating
branches, or make the known-open state explicit in CI (e.g. a comment in `ci.yml` pointing at
`.planning/WINDOWS.md` item 5, or a documented `continue-on-error: true` scoped to this one check
until the trim lands).

### WR-03: `evals/pressure-tests.md`'s blanket justification for its "must not fire" rows overstates what `SKILL.md`'s Limits section actually names

**File:** `evals/pressure-tests.md:34-36` (justification), `:40-44` (the five rows)

**Issue:** The section header claims every near-miss row "sits just outside the skill's stated
scope — PROJECT.md's Out of Scope list **and SKILL.md's own Limits section**." `SKILL.md`'s Limits
section (its final paragraph) names exactly: slide decks and visual design, pricing/sizing/commercial
modelling, CRM or bid-management integration, and marketing or brand writing. Two of the five rows —
"Write the API reference docs for the /migrations endpoint" and "Rewrite this paragraph in plain
English for a general reader" — are not covered by anything in that Limits section; they're
reasonable non-fires because they fall outside the frontmatter's positive scope description, not
because Limits names them.

**Fix:** Either narrow the claim ("sits outside the skill's stated positive scope, and in three of
five cases is also named in SKILL.md's Limits section") or add the two missing exclusions to
`SKILL.md`'s Limits section if they are meant to be enforced there.

## Info

### IN-01: `_collapse_whitespace` folds intentional blank-line paragraph breaks before measuring description length

**File:** `tools/check_repo.py:794-795` (`_collapse_whitespace`), `:817-825` (its use in the
description-length check)

**Issue:** `_collapse_whitespace` does `' '.join(text.split())`, which reduces any run of
whitespace — including a deliberate blank line separating two paragraphs inside a `|` block-scalar
description — to a single space. A description written as two paragraphs therefore measures
several characters shorter than its literal on-disk length, purely as an artifact of how many blank
lines it used. This is a minor approximation and currently affects no real fixture (the shipped
description is one paragraph), but it is not mentioned in the check's "Declared ceiling" note.

**Fix:** Either note this fold explicitly in the docstring's declared-ceiling paragraph, or (if
literal length is intended) preserve a single boundary character per blank line before collapsing
runs of ordinary whitespace.

### IN-02: Defensive `f.name == 'NUMBERING.md'` guards are unreachable for their current scan roots

**File:** `tools/check_repo.py:397-399` (`check_undefined_id`), `:484-486` (`check_unlisted_figure`)

**Issue:** Both scans skip a file named `NUMBERING.md`, but their scan roots (`skills/`,
`examples/`, `README.md`) never contain a file by that name in this repository — `NUMBERING.md`
lives only at the repository root, outside both scan roots. The guard is currently dead code (not a
correctness problem — it costs nothing and protects against a future misplacement — but worth
noting since it's the kind of statement a docstring audit should double check against reality).

**Fix:** No action required; consider a one-line comment noting this is forward-defensive rather
than currently reachable, so a future reader doesn't waste time looking for the case it should
guard against.

---

_Reviewed: 2026-09-11T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
