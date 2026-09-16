---
phase: 03-completeness-audit-artifact-patterns
reviewed: 2026-09-16T00:00:00Z
depth: standard
files_reviewed: 18
files_reviewed_list:
  - .github/workflows/ci.yml
  - NUMBERING.md
  - README.md
  - evals/conformance/RESULTS-mod04.md
  - evals/conformance/fixtures/A-rfp-answer.md
  - evals/conformance/fixtures/B-proposal-section.md
  - evals/conformance/fixtures/C-exec-summary.md
  - evals/conformance/fixtures/D-demo-discovery.md
  - evals/conformance/fixtures/E-ambiguous.md
  - evals/conformance/run_conformance.py
  - evals/conformance/transcripts/conformant-family-first.txt
  - evals/conformance/transcripts/nonconformant-no-family.txt
  - evals/conformance/transcripts/nonconformant-rule-before-family.txt
  - skills/proof-first/SKILL.md
  - skills/proof-first/references/artifact-patterns.md
  - skills/proof-first/references/checklist.md
  - skills/proof-first/references/completeness-audit.md
  - skills/proof-first/references/worked-examples.md
  - tools/check_repo.py
findings:
  critical: 2
  warning: 5
  info: 1
  total: 8
status: issues_found
---

# Phase 03: Code Review Report

**Reviewed:** 2026-09-16T00:00:00Z
**Depth:** standard
**Files Reviewed:** 18
**Status:** issues_found

## Summary

This phase's four project gates (`check_repo.py --self-test`, `--mutation-test`, the live run, and
`run_conformance.py --self-test`) were re-run during this review and all four currently pass, as
claimed. `tools/check_repo.py`'s two new codes (`skill-family-line-gate-missing`,
`source-label-in-skill-content`) are genuinely discrimination-proven: both fire only after the
targeted mutation and stay silent on the control copy. The hand-computed arithmetic in
`RESULTS-mod04.md`'s "Combined result" section was independently re-derived from every underlying
run block in this file and checks out exactly (16/20 = 80.0% for Arm 1, 5/11 = 45.5% for Arm 2);
the `INVALIDATED` block is unambiguously labelled and excluded correctly from that arithmetic.

The review did find a real defect class in `run_conformance.py`'s scorer that is the same shape as
the two bugs this phase already found and fixed: `score_transcript()` treats a family-name phrase
match found *anywhere* in the transcript as proof the family line was declared, with no requirement
that the match sit at the start of the output where `SKILL.md`'s write-mode contract places it. A
transcript that genuinely omits the family line (a true violation) but later contains the same
common English phrase as ordinary prose — "executive summary," "solution proposal" — would be
mis-scored `conformant` (or `rule-before-family`) instead of the correct `no-family`, silently
inflating MOD-04's measured conformance rate. This is a plausible, not merely theoretical, risk:
"executive summary" and "solution proposal" are exactly the words a real presales document is
likely to use as an ordinary heading or descriptive phrase, independent of whether the mandatory
opening family-line was ever written.

Separately, `README.md`'s "no measured claim is published in this repository yet" section is now
factually false: this phase committed `evals/conformance/RESULTS-mod04.md` with two real,
percentage-bearing measurement arms. In a project whose stated evidence constraint is "measured
claims or no claims," a stale claim that inverts to a false "no claims exist" is a meaningful
finding, not a nit.

## Critical Issues

### CR-01: `score_transcript()` accepts an unanchored family-phrase match anywhere in the transcript, risking a silently inflated conformance rate

**File:** `evals/conformance/run_conformance.py:46-59, 97-139`
**Issue:** `SKILL.md`'s write-mode contract (`SKILL.md:261`) requires the artifact-family line to
be the *first* of "exactly three parts, in order": the family line, the prose, then the register.
`score_transcript()` does not enforce or even check this position. It scans the *entire* transcript
text for the leftmost match of any `FAMILY_PATTERNS` entry — several of which are short, ordinary
English phrases ("executive summary", "solution proposal") that are highly likely to recur later in
a real drafted document (e.g., as a section heading, or in a sentence like "this solution proposal
covers…") regardless of whether the mandatory opening family line was ever written.

Concretely: if a live session violates the rule by never naming a family up front (a genuine
`no-family` case), but the drafted body text it goes on to produce happens to contain the phrase
"executive summary" or "solution proposal" anywhere — extremely plausible content for these
document types — `score_transcript()` will find that occurrence, treat it as `family_at`, and score
the session `conformant` (or `rule-before-family` if a marker also appears somewhere before that
incidental occurrence). This converts a true violation into a false pass, in exactly the direction
that inflates the headline MOD-04 rate this instrument exists to produce honestly. It is the same
defect class already found and fixed twice this phase (nonzero-exit sessions scored `no-family`;
`_git_blob_sha()` reporting the wrong revision) — a signal being trusted as proof of a behavior it
does not actually establish.

The docstring's own disclosed ceiling ("it cannot tell a family named in a heading from one named in
a sentence") covers a narrower case than this: it does not disclose that the family match can come
from content structurally unrelated to the required opening declaration at all, including from a
document that never satisfies the family-line requirement.

**Fix:** Anchor the family-line search to the start of the transcript (the way the actual rule is
written — the "first line"/first part of the output), rather than searching without bound:

```python
# The family line is contractually the transcript's first part (SKILL.md's
# write-mode section). Bound the family search to a generous prefix window
# so a coincidental later occurrence of the same phrase cannot stand in for
# an omitted opening declaration.
FAMILY_LINE_WINDOW_CHARS = 400

def score_transcript(text):
    stripped = text.strip()
    if not stripped:
        return 'unscoreable', 'empty transcript'

    window = stripped[:FAMILY_LINE_WINDOW_CHARS]
    family_match = None
    family_at = None
    for pattern in FAMILY_PATTERNS:
        m = pattern.search(window)
        if m and (family_at is None or m.start() < family_at):
            family_at = m.start()
            family_match = m.group(0)
    ...
```
Add a `self_test()` case that proves a transcript with no family line at all, but the phrase
"executive summary" appearing only in the drafted body well past the window, is scored `no-family`
— not `conformant` — to close the gap the way the two prior fixes were each closed with a dedicated
case.

### CR-02: `README.md` states no measured claim exists in the repository; this is now false

**File:** `README.md:45-47`
**Issue:** `README.md` reads: "No measured claim is published in this repository yet. The
benchmark has not run." This phase committed `evals/conformance/RESULTS-mod04.md`, which contains
two fully-computed measurement arms with published percentages ("conformant 16 of 20 scoreable
sessions... Rate: 16/20 = 80.0%" and "conformant 5 of 11 scoreable sessions... Rate: 5/11 = 45.5%"),
each with named caveats. The README's claim is not merely stale wording — it is a factually
incorrect statement about the repository's current contents, in a project whose stated constraint
is explicitly "measured claims or no claims" (project CLAUDE.md) and whose own skill exists to catch
exactly this class of unearned-or-inaccurate claim in someone else's document. `README.md`'s
"Repository layout" tree (lines 49-91) and "What exists today" list (lines 20-35) also do not
mention `evals/conformance/` at all, so a reader has no way to discover the measurement that
contradicts the "no measured claim" sentence two paragraphs later.
**Fix:** Update the "Status" section to either (a) state the MOD-04 conformance measurement exists,
point to `evals/conformance/RESULTS-mod04.md`, and carry its own caveats forward (unequal-sample-size
comparison, non-determinism, Anthropic-only models), or (b) if this measurement is not meant to be
treated as a "published" headline number yet, say precisely why (e.g., "an instrument-proving run,
not yet a final MOD-04 measurement") rather than asserting no measured claim exists at all. Add
`evals/conformance/` (fixtures, transcripts, `run_conformance.py`, `RESULTS-mod04.md`) to the
repository layout tree and the "What exists today" list.

## Warnings

### WR-01: A timed-out session leaves no diagnostic artifact, unlike every other failure path

**File:** `evals/conformance/run_conformance.py:169-194`
**Issue:** `run_session()`'s docstring and inline comment ("Write both streams for audit") commit to
preserving stdout/stderr for every failure mode, and the nonzero-exit path (`SessionFailedError`)
does write `out_path` before raising. But `subprocess.run(..., timeout=timeout_s)` raises
`subprocess.TimeoutExpired` directly from line 169, before any of the `out_path.write_text(...)`
logic below it ever runs, and the exception is not caught inside `run_session()` at all — it
propagates straight to `main()`'s `except subprocess.TimeoutExpired` clause, which never touches
`session_out_path`. Every timeout in `RESULTS-mod04.md` (there are several) has zero on-disk
transcript, including any partial stdout the process had already produced — the one failure mode
this project has already been burned by twice is precisely the one this script cannot audit after
the fact.
**Fix:** Catch `subprocess.TimeoutExpired` inside `run_session()`, and write whatever partial
`stdout`/`stderr` the exception object carries (`exc.stdout`, `exc.stderr` — populated by
`subprocess.run` when `capture_output=True` even on timeout) to `out_path` before re-raising, the
same way the nonzero-exit path already does.

### WR-02: A zero exit code is trusted as proof of a valid transcript with no content sanity check

**File:** `evals/conformance/run_conformance.py:176-192`
**Issue:** The fix for the nonzero-exit bug assumes `result.returncode == 0` reliably distinguishes
a genuine transcript from an error string. This is an assumption about the `claude` CLI's own
behavior that is not verified anywhere in this codebase (no test exercises "exit 0, error-shaped
stdout"). If any class of harness/environment failure ever surfaces as an exit-0 invocation with a
short error string in stdout (a quota message printed to stdout rather than stderr, for instance),
that text would flow straight into `score_transcript()` and most likely be scored `no-family` — the
exact false verdict `SessionFailedError` was introduced to eliminate, just reached through a
different door.
**Fix:** Add a minimal sanity check before scoring — e.g., a stdout under some small character
floor, or one that fails to include any recognizable structure — and record it as `unscoreable` with
a distinct reason rather than passing it straight to `score_transcript()`. At minimum, document the
assumption explicitly in `run_session()`'s docstring as a known, accepted gap rather than an
implicit one.

### WR-03: `--repeats 0` silently produces no output and no diagnostic for the skipped cell

**File:** `evals/conformance/run_conformance.py:502-506`
**Issue:** `for repeat in range(args.repeats):` with `args.repeats == 0` (a value `argparse` accepts
without validation) causes the model×fixture cell to run zero times, appending nothing to `lines`
and incrementing neither `scoreable_count` nor `unscoreable_sessions`. A user who mistypes
`--repeats 0` gets a `RESULTS-mod04.md` block that is silently missing that cell's data entirely,
with no diagnostic distinguishing "ran and produced no rows" from "requested zero repeats."
**Fix:** Reject `args.repeats < 1` in argument validation (`parser.error(...)`) rather than silently
accepting it.

### WR-04: `skill-family-line-gate-missing`'s anchor text is matched case-sensitively

**File:** `tools/check_repo.py:1294-1331`
**Issue:** `check_skill_family_line_gate()` requires the exact case-sensitive substrings
`'artifact family'` and `'No family fits'` inside the self-check section body. A future wording
change that preserves the gate's meaning but changes casing — e.g. "confirm the Artifact Family is
named" — would falsely fire `skill-family-line-gate-missing` even though the instruction the check
exists to protect is semantically intact. This is not covered by the check's own declared ceiling
("this check asserts the instruction text is present... cannot assert a live session obeys it"),
which speaks to a different limitation.
**Fix:** Either explicitly document the case-sensitivity as a declared ceiling (consistent with this
file's convention of stating every check's known limits), or match case-insensitively for the
anchor-phrase checks specifically, since case carries no semantic weight here (unlike, say, the
`'No family fits'` value's exact-spelling requirement in `FAMILY_PATTERNS`, which is a frozen
interface with `run_conformance.py` and should stay exact).

### WR-05: `SOURCE_COINED_LABELS` pluralization handling is inconsistent across labels

**File:** `tools/check_repo.py:1334-1356`
**Issue:** Only `'pain'` is marked pluralizable (`_SOURCE_LABEL_PLURALIZABLE = frozenset({'pain'})`).
`'champion'` and `'competition'` — both realistic in plural or near-plural form ("champions",
"competitions") — are not, so `\bchampion\b`/`\bcompetition\b` will not match those forms even
though they carry the same unattributed-source-label risk this check exists to catch. This is
consistent with the check's own declared ceiling ("a novel one has no string to match") but the
asymmetry (why `pain` and not the other two) is not explained anywhere.
**Fix:** Either extend `_SOURCE_LABEL_PLURALIZABLE` to cover `champion`/`competition`, or add a
one-line comment explaining why `pain` alone needed plural handling (its singular/plural forms are
both common) while the others were judged not to need it.

## Info

### IN-01: `run_conformance.py`'s `FAMILY_PATTERNS` list duplicates a comment claim about being "byte-identical" to `check_repo.py`'s constant without any check enforcing that claim

**File:** `evals/conformance/run_conformance.py:43-45`
**Issue:** The comment states this list must stay "byte-identical to tools/check_repo.py's
ARTIFACT_FAMILY_SECTIONS," but nothing enforces that at test time — a future edit to one file's
four canonical strings (`ARTIFACT_FAMILY_SECTIONS` in `check_repo.py`) will not fail
`run_conformance.py --self-test` or `check_repo.py --self-test` if the other file drifts out of
sync. `run_conformance.py`'s list is also a superset (it adds `SKILL.md`'s write-mode phrasings and
the "No family fits" value on top of the four `check_repo.py` section headings), so "byte-identical"
somewhat overstates the actual relationship — it is byte-identical only for the shared four-string
subset.
**Fix:** Either add a shared self-test assertion (in one of the two `--self-test` modes) that the
four `check_repo.py` section-heading strings are literally present as a subset of
`run_conformance.py`'s `FAMILY_PATTERNS` source strings, or soften the comment's "byte-identical"
claim to describe the actual subset relationship.

---

_Reviewed: 2026-09-16T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
