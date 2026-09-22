---
status: clean
phase: 06-legal-review-gate-launch
reviewed: 2026-09-22
round: gap-closure (06-09)
scope: source files changed by 06-09's gap commits (384b1ae..HEAD) — tools/check_repo.py, evals/trigger/run_trigger_test.py
reviewer: inline (orchestrator) — the gsd-code-reviewer subagent was not dispatched
findings_total: 1
findings_open: 0
findings_fixed: 1
supersedes: 06-REVIEW.md as committed for the 06-08 round (preserved in full below, with its own supersession chain back to 06-05)
---

# Phase 6 Code Review — gap-closure round (06-09)

**Two source files changed. One finding, in the round's own new assertion, fixed before the round
closed: the check was narrower than the sentence it guards.**

Twenty-six commits. The executable surface is one new self-test case in
`evals/trigger/run_trigger_test.py` with two supporting readers (+96 lines); everything in
`tools/check_repo.py` is comment and docstring text, no behaviour change.

## What was reviewed, and how

| File | Executable change | How it was checked |
|---|---|---|
| `evals/trigger/run_trigger_test.py` | `documented_init_key_set()`, `observed_init_key_sets()`, one new `--self-test` case, `EXPECTED_TRANSCRIPT_COUNT` | Three mutation probes on sibling copies outside the repository, each with an unmutated control; every probe asserted on the assertion's own message, not merely on a non-zero exit |
| `tools/check_repo.py` | none — four comment/docstring corrections | `--self-test`, `--mutation-test` (58 codes discrimination-proven) and a live run, all green before and after; claims in the new comments re-derived by AST census and by running `CITATION_RE` over both record paths |

The review deliberately did not stop at "the self-test passes". A self-test that passes is evidence
the code runs, not evidence it discriminates — which is why every new assertion this round shipped
was put under a probe that makes it fail, and a control that keeps it passing.

## Findings

### 1. The new init-event assertion was narrower than the claim it is cited as guarding — FIXED (`c5a5a4f`)

`INIT-EVENTS.md`, as corrected by task 14, says "Every init event in all 140 committed transcripts
carries 24", and points at `run_trigger_test.py --self-test` as the thing that now holds it. The
assertion as first shipped compared the key **set** only. A tarball that lost init events entirely
still yields one distinct key set, so the "every" and the "140" were both unguarded.

Measured rather than reasoned: a probe copy with 40 of the 140 transcripts stripped of their init
event **passed** the check as shipped.

`observed_init_key_sets()` now returns `(sets, scanned, missing)` and the self-test asserts all
three. Re-proven on sibling copies:

| Probe | Result |
|---|---|
| 40 init events stripped | `rc=1` — "40 of 140 transcripts carry no system/init event, so INIT-EVENTS.md's 'every init event' claim does not hold" |
| 10 transcripts dropped | `rc=1` — "the committed tarball holds 130 transcripts, not the 140 INIT-EVENTS.md states" |
| unmutated control | `rc=0`, naming the case |

This is the same class the round spent twenty-one tasks correcting — a claim wider than the check
behind it — committed by the round that was correcting it. That is the third time this phase a
closing round has reproduced the defect class it was closing, and it is the argument for the probe
discipline rather than against it.

## What was checked and found sound

- **`documented_init_key_set()` fails loudly rather than silently.** A missing heading or missing
  fence raises `ValueError`, which the self-test surfaces as a named failure. Verified with a third
  probe (heading renamed): `rc=1` through the loud branch, not a silent empty-set pass.
- **AppleDouble handling is correct and necessary.** The tarball carries `._control` and
  `._treatment` resource forks that are not valid UTF-8; skipping them by basename is what lets the
  reader decode. Without the skip the function raises `UnicodeDecodeError` — observed directly while
  writing it.
- **`extractfile()` can return `None`** for non-regular members; guarded.
- **No `extractall`**, so the Python 3.12 extraction-filter deprecation does not apply.
- **`tools/check_repo.py`'s comment corrections change no behaviour.** `--mutation-test` holds at 58
  codes discrimination-proven before and after, and the live run stays at 0 violations.
- **The new comments' own claims re-derive.** 51 `check_*` functions, 15 calling `strip_fences` and
  36 not, by AST walk; `CITATION_RE` returning 9 matches in `LEGAL-REVIEW.md` and 0 in `README.md`,
  identical before and after `strip_fences()`, re-measured after every later edit in the round.

## Declared ceiling of this review

It is an inline read by the agent that wrote the code, not an independent one. The two things that
make it worth more than a self-assurance are that every assertion was put under a mutation probe
with a control, and that the one finding it produced was found by building a probe that broke the
new check rather than by re-reading it. Neither substitutes for round 6's cold read, which is this
phase's standing closure condition.

## Gate

**Clean.** One finding, fixed in its own commit before the round closed. All ten CI commands green
at `HEAD`.

---

# Superseded: Phase 6 Code Review — gap-closure round (06-08)

The review below was current for the 06-08 round and is preserved verbatim. Its frontmatter, which
this file's own frontmatter has replaced, read:

```yaml
status: clean
phase: 06-legal-review-gate-launch
reviewed: 2026-09-22
round: gap-closure (06-08)
scope: source files changed by 06-08's gap commits (9a2a035..HEAD) — tools/check_repo.py, tools/generate_derivatives.py, evals/benchmark/run_benchmark.py
reviewer: inline (orchestrator) — the gsd-code-reviewer subagent was not dispatched
findings_total: 2
findings_open: 0
findings_fixed: 2
supersedes: 06-REVIEW.md as committed for the 06-06 round (preserved in full below); the 06-07 round produced no review at this path
```

# Phase 6 Code Review — gap-closure round (06-08)

**Three source files changed. Two findings, both in the round's own new check code, both fixed
before the round closed.**

Sixteen commits; the executable surface is one new violation code
(`record-citation-unresolvable`, ~150 lines with fixtures and a mutation), two new self-test
assertions (`caveat-count-matches-constant`, `no-platform-collision`), and prose changes to two
docstrings and one generated preamble.

## What was reviewed, and how

Behavioural, not a read-through. Every claim the new code's docstring makes was put to a probe
against an unmutated sibling control — red for the stated reason, green when unmutated — because
that is the only way to tell a live check from a dead one, and this repository has shipped a dead
check named as covered before (`01-VERIFICATION.md`).

| Change | Probe | Control | Result |
|---|---|---|---|
| `record-citation-unresolvable` overrun | range pushed past EOF in a temp copy | unmutated copy | red with `runs past the end of the file it names (NUMBERING.md has 162 line(s))`; control clean |
| same, missing path | path replaced with `NO-SUCH-FILE.md` | unmutated copy | red with `no file named NO-SUCH-FILE.md exists in the tree`; control clean |
| same, inverted range | `:33-35` → `:35-33` | unmutated copy | red with `whose line range is inverted`; control clean |
| same, production shape | `--mutation-test` entry mutating the real record's first line-range citation | CONTROL step asserts zero violations unmutated | PASS; 58 codes discrimination-proven |
| `caveat-count-matches-constant` | sibling copy whose renderer emits a seventh hardcoded bullet | unmutated sibling copy | red with `emitted 7 caveat bullet(s), expected len(REQUIRED_CAVEATS)=6`; control rc=0 |
| `no-platform-collision` | `Amazon EC2` appended to the real bench brief, then restored | restored brief, byte-identical | red with `reuses shared-deal-brief platforms: ['Amazon EC2']`, exit 1; control exit 0 |

The new code was additionally replayed over all 435 commits of repository history with a control
counting the citation-instances examined, to establish that its zero-firing result is a real
negative and not an empty measurement. 164 instances examined, 14 distinct spellings, zero firings.
That measurement is in the code's own docstring, which is the review's main substantive comment on
it: a check whose value is zero-measured must say so where a reader will meet it.

## Findings

### F-1 — `check_record_citations` did not strip fenced blocks (fixed)

**Severity: low. Real, and a future-CI-breaker rather than a present defect.**

Every other content-scanning code in `check_repo.py` reads `strip_fences(...)` output. This one read
the raw text. Measured impact today: none — `LEGAL-REVIEW.md` contains zero fences and `README.md`'s
seven contain no `path`:N pattern, so the citation set is identical either way.

The defect is prospective and specific: the moment either record documents this very citation format
inside a code fence — which a docstring pointing at `path`:N invites — the gate fires on its own
documentation and fails the build. A gate hostile to its own docs would be discovered by whoever
next tries to explain it.

**Fixed** by reading `strip_fences(...)`, consistent with the file's other codes, plus a seventh
self-test direction (`citation_fenced_root`) carrying the same out-of-range citation as the overrun
fixture but inside a fence, asserted silent. The direction was proven to discriminate: removing
`strip_fences` from a sibling copy fails with `record-citation-unresolvable fired on an out-of-range
citation inside a fenced block, which is documentation`, exit 1; the control passes rc=0. The
behaviour is now declared in the docstring rather than incidental.

### F-2 — stray whitespace inside a path expression (fixed)

`_citation_line_count` read `len(( repo_root / rel)...)`. Cosmetic, no behavioural effect. Fixed.

## What was checked and found sound

- **The index is built once per run, not per citation.** `if index is None` guards it, and the
  lazy build means a record with no citations costs nothing. Measured: the whole check runs in
  42 ms, of which the tree walk over 1,674 paths is 12 ms. No performance concern.
- **The ambiguous-basename branch is not arbitrary.** Where a basename matches more than one file
  the check fires only if the range overruns *every* candidate, and says so in the docstring. That
  is the only sound reading when the check cannot tell which file was meant.
- **`.planning/` is excluded from resolution, not merely from scanning,** and a self-test direction
  pins it: a citation resolvable only inside `.planning/` must report as unresolvable rather than
  silently resolving into the planning archive. A superseded plan is a historical record, not a
  live target.
- **`caveat-count-matches-constant` asserts against `len()`, never a literal.** This is the whole
  point of the finding it closes — a literal above the tuple it counts is what drifted — and the
  new assertion introduces no number of its own.
- **`no-platform-collision` declares the same ceiling as the entity assertion beside it:** a
  substring check over a fixed tuple, proving those six names absent rather than that no platform
  is shared, with the by-hand maintenance obligation stated.
- **`generate_derivatives.py`'s changes are prose only**, and both derivatives were regenerated in
  the same commit as the source change, with `--check` green — so no hand-edit window opened.

## One process observation

This round's own commit broke six line citations in `LEGAL-REVIEW.md` and the new code was silent on
all six. That is not a defect in the code — its docstring says exactly that it cannot catch a line
that exists and says something else — but it is the sharpest available evidence that the citation
class this round tried to mechanize is not mechanically catchable. The structural fix that actually
holds was the convention change, not the gate: cite a Markdown file by heading and quoted string, a
Python file by symbol name. That is recorded in the summary's `patterns-established` and is worth
more than the code shipped alongside it.

---

# Superseded: Phase 6 Code Review — gap-closure round (06-06)

The round-4 review above replaces this one at the same deterministic path. It is preserved in
full below, unchanged, because the path is deterministic and regenerating it would otherwise
erase the record. The 06-07 round produced no review at this path.


# Phase 6 Code Review — gap-closure round (06-06)

**One source file changed in this round: `tools/check_repo.py`. No findings.**

Fourteen commits; thirteen touch documentation only. The single executable change adds one violation
code, `benchmark-run-claim-stale`, with its constants, its check function, its self-test fixtures and
its mutation.

## What was reviewed, and how

The review is behavioural, not a read-through. Every claim the new code's docstring makes about what
it does was put to a probe against an unmutated sibling control — red for the stated reason, green on
the control — rather than accepted from the prose.

| Claim in the docstring | Probe | Control | Mutant |
|---|---|---|---|
| Catches a regression restored **capitalised** | `No benchmark has run.` appended to the skill source | 0 | 1 ✓ |
| Catches a **derivative-only** regression the source-blind sibling would miss | lowercase claim appended to `output-styles/proof-first.md`, source untouched | 0 | 1 ✓ |
| Stays silent when the **evidence file is absent** — the sentence is then true | same capitalised mutant, `evals/benchmark/RESULTS.md` deleted | — | 0 ✓ |

The third row is the one that matters most: it is the two-sided conjunction the sibling code
established, and without it the check would fire on an honest disclosure in a tree where no benchmark
had run.

## Points considered and cleared

- **Placement in `run_derivative_checks`.** The call sits above the `numbering_path.exists()` early
  return, so it runs whether or not `NUMBERING.md` is present. Checked deliberately — the sibling
  call has the same placement and the ordering is load-bearing.
- **`BENCHMARK_CLAIM_PATHS = DERIVATIVE_PATHS + DERIVATIVE_SOURCE_NAMES`.** Both operands are tuples,
  so this concatenates to seven paths rather than doing anything surprising. Each is existence-guarded
  before it is read.
- **False-positive surface of a case-insensitive substring.** Widening the match widens what can trip
  it. The declared ceiling states the check is literal presence and nothing more, matching the
  sibling's disclosed discipline, and the corrected sentence in the tree does not contain the needle
  — `check_repo.py` reports 0 violations, which is the direct evidence.
- **Mutation co-firing.** The mutator appends to a `DERIVATIVE_SOURCE_NAMES` file, so
  `skill-derivative-stale` fires on the same mutant. This does not weaken the result:
  `mutation_test` requires only that the expected code is silent on the control and fires on its own
  mutant, and the control ran clean at 0 violations.

## Deviation from the plan, reviewed on its merits

The plan directed that the literal be added to the existing `check_derivative_comparison_claim`. The
executor made it a sibling code instead. Reviewed and **upheld**: the mutation harness maps one code
to one mutation, so a second literal folded into an existing code would have been registered without
ever being independently discrimination-proven — which is this repository's own named recurring
defect, `.planning/WINDOWS.md` id 10. The deviation serves the plan's stated intent ("prove the
addition discriminates via `--mutation-test`") better than its letter would have. It is recorded in
the commit message rather than left to be discovered.

## Gate

All ten commands from `.github/workflows/ci.yml`, after the final commit: green.
`check_repo.py --mutation-test` reports **57 codes discrimination-proven** with a clean control, up
from 56.

## The caveat, repeated rather than assumed carried over

**This review was not independent.** The agent that wrote the code also reviewed it — the exact
weakness `.planning/WINDOWS.md` id 17 measures, and which this phase's cold reads have now
demonstrated for a fifth consecutive round. The behavioural probes above are worth more than the
read-through precisely because they do not depend on the reviewer's judgement, but a clean
self-review is still weaker evidence than a clean independent one.

The round did run one thing an ordinary self-review does not: it re-read the sentences it had
*added*, not only the ones it fixed, and found two further checkably-false statements — one of its
own making. Both were corrected before the round closed. That is recorded here because the previous
round's failure was precisely this, and catching it once is not evidence the habit holds.

---

# Superseded: Phase 6 Code Review — gap-closure round (06-05)

The round-2 review above replaces this one at the same deterministic path. It is preserved in full
rather than overwritten, because the round it reviewed is the round whose defects round 2 found.

# Phase 6 Code Review — gap-closure round (06-05)

**No source file changed in this round. No findings.**

## Superseded reviews

This file replaces, at the same deterministic path, the **first-round review of 2026-09-21**
recorded in commit `fbcef01`. That round reviewed 1,504 added lines across
`tools/check_repo.py` and `evals/benchmark/run_benchmark.py` — a different file set entirely from
this one — and returned **one low-severity finding, fixed in place, verdict clean**: a dead
`markers` parameter and a redundant identical-branch ternary in `check_repo.py`'s
`_claim_readme()` self-test fixture builder.

Read it in full with:

```
git show fbcef01:.planning/phases/06-legal-review-gate-launch/06-REVIEW.md
```

Nothing in it is re-litigated here. Its finding was fixed and re-verified in that same commit, and
neither of the two files it reviewed is touched by this round.

## Scope

```
git diff --name-only 7e2170d..HEAD
```

| File | Lines | Kind |
|---|---|---|
| `README.md` | +81 / -27 | shipped prose |
| `LEGAL-REVIEW.md` | +314 / -74 | shipped prose |
| `NUMBERING.md` | +15 / -5 | shipped registry prose |
| `.planning/WINDOWS.md` | +51 / -21 | planning artefact |
| `06-05-SUMMARY.md` | +225 | planning artefact |

```
git diff --name-only 7e2170d..HEAD -- . ':!.planning/' ':!*.md'
```

Returns nothing. **No `.py`, no `.json`, no `.yml` changed.** The code-review capability's normal
remit — source files changed in the phase — is empty for this round, and the honest report of that
is this sentence rather than a re-review of code the round did not touch.

## What was reviewed instead

The round's actual risk surface is prose that makes checkable factual claims, which is the class
`.planning/WINDOWS.md` id 17 records as invisible to every check in this repository. Every factual
assertion the diff introduces was re-verified against its own source:

| Assertion introduced | Checked against | Result |
|---|---|---|
| Arm B: 45/45 must-fire, 9/25 must-not-fire, 2026-09-20, `claude-sonnet-5` | `RESULTS-trigger.md`:92-97 Totals block | matches |
| Arm B measures the shipped description | `head -14 skills/proof-first/SKILL.md \| shasum -a 256` == the hash at `RESULTS-trigger.md`:68 | byte-identical |
| Two near-miss phrasings account for all nine over-fires, at 5/5 and 4/5 | `RESULTS-trigger.md`:86-90 | matches (rows 87, 88; rows 86, 89, 90 are 0 of 5) |
| Three measured arms; routes 1 and 2 collapse | `run_routes.py`:113 `ROUTES` tuple; README:54-71 routes 1 and 2 both install the skill folder | matches |
| MOD-04's threshold is "before its first rule marker" | `run_conformance.py`:4-6 | matches |
| `scenarios.json` holds eight prompts, two per family | parsed: 8 entries, `Counter({executive-summary: 2, rfp-rfi: 2, solution-proposal: 2, demo-discovery: 2})` | matches |
| `proxy-sources.md` is the source for `lint.py`'s proxy terms | `proxy-sources.md`:3-7 | matches |
| `ci.yml` runs the checker, its two test modes, every eval self-test, and the derivative check | `ci.yml` names 6 eval scripts; `grep -rln self-test evals/` returns the same 6 | matches |
| `catalog-count-mismatch` and `readme-layout-tree-stale` exist as codes | `tools/check_repo.py` | both present |
| MEDDPPCC, and four letter-ambiguous positions | `NUMBERING.md`:64-77 | M,E,D,D,P,P,C,C; DC/DP both D, Champion/Competition both C |
| The `source-gate-incomplete` ceiling quoted verbatim | `tools/check_repo.py`:484-487 | exact |
| Ledger counts 9 fixed + 2 closed-on-reasoning + 9 waived + 9 open = 29 | `.planning/WINDOWS.md` frontmatter and its 29 JSON entries | matches |

## Findings

None.

## Considered and deliberately not flagged

- **`README.md`:126 still reads "the one canonical fictional deal every worked example cites."**
  Checked rather than assumed: this is the narrow claim the plan explicitly preserved. It is true —
  every worked example cites `examples/deal-brief.md`. The false claim was the *shipping* one at
  :7-8, and that is the one rewritten.
- **The `WINDOWS.md` table regeneration rewrote 51 lines.** Verified as a rendering change, not a
  content change: the fenced JSON is the source of truth, three reasons were reconciled INTO it
  from table-only edits, and the table was then re-rendered with `broken-windows.cjs`'s own
  escaping rule. `gsd-tools windows append` accepting the next write is the mechanical proof the
  two agree.
- **`LEGAL-REVIEW.md` is declared append-only and this round edited earlier sections.** Deliberate
  and bounded: the edits are the register corrections `06-05-PLAN.md` Task 7 commissions by line
  number, plus three heading amendments that mark superseded findings. No earlier finding was
  deleted or reworded into a different finding, and the substantive supersession is an appended
  section 4.

## Verdict

**Clean.** No source file changed, so no code defect is possible from this round; every checkable
prose assertion it introduces was verified against the file it refers to, and all ten commands
`.github/workflows/ci.yml` declares exit 0.

The caveat from the first round applies unchanged and is repeated rather than assumed carried over:
**this review was not independent.** The agent that wrote the text also checked it, which is the
exact weakness `.planning/WINDOWS.md` id 17 measures and which this round's own cold read
demonstrated for a fourth consecutive time. Treat a clean self-review as weaker evidence than a
clean independent one.
