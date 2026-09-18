---
phase: 05-evaluation-harness
plan: 01
subsystem: testing
tags: [linter, provenance, regex, stdlib, ci]

requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: skills/proof-first/SKILL.md's frozen PF-2.1, PF-3.1/PF-3.2, PF-4.1, PF-4.3 rule
      text that this linter's proxy codes cite in their docstrings
provides:
  - A stdlib-only deterministic proxy linter (evals/lint.py) with eight discrimination-proven
    violation codes and a self-test
  - An externally-sourced, mechanically-checked provenance registry (evals/proxy-sources.md)
    binding every counted term to Wikipedia MOS:WTW or GSA plain-language guidance
  - A CI gate running the linter's self-test on every push/PR
affects: [05-02-benchmark-scenarios, 05-03-benchmark-runner-and-judge, 06-legal-review]

actuals:
  tokens: 11500
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns:
    - "Longest-first term alternation for word-boundary proxy matching (mirrors
      tools/check_repo.py's declared-ceiling docstring convention)"
    - "One dedicated firing/clean fixture pair per violation code inside self_test(),
      never a fixture that trips two codes at once"
    - "Registry provenance validated via an allow-list of (label, URL-prefix) pairs,
      never a deny-list"

key-files:
  created:
    - evals/lint.py
    - evals/proxy-sources.md
  modified:
    - .github/workflows/ci.yml

key-decisions:
  - "SUPERLATIVE_TERMS and HEDGE_TERMS are deliberately disjoint from PROXY_TERMS (five new
    Wikipedia-sourced superlatives; may/might/could for hedge/modal) so a sentence exercising
    unquantified-superlative or unbounded-modal never also, as a side effect, trips
    buzzword-term -- required by the plan's own one-fixture-one-code discipline."
  - "HEDGE_TERMS (may, might, could) traces to PF-4.3's own named possibility-modal vocabulary
    and to the same Wikipedia Words-to-watch page's hedging-language concern, sourced label A."
  - "Resolved a Task 1 plan self-contradiction (the <behavior> block says 'class is also a
    registry row', <acceptance_criteria> says 'class is not itself a registry row in this
    task') by following acceptance_criteria -- 'class' was never added to the shipped
    registry; the longest-match-wins mechanism is instead proven directly against a local
    ('class', 'best-in-class') probe pair inside self_test()."
  - "Kept check_provenance() and lint() as two separate entry points: lint(text) returns only
    text-based violations for a document; check_provenance(terms, rows) validates the registry
    itself and is exercised directly in self_test(), not folded into every lint() call, since
    registry provenance is a property of the registry file, not of any one document."

patterns-established:
  - "Every registry-sourced term list (PROXY_TERMS, SUPERLATIVE_TERMS, HEDGE_TERMS) is unioned
    into ALL_COUNTED_TERMS and checked against the registry by one shared check_provenance()
    call, so a future fourth list needs no new checker function."

requirements-completed: [EVAL-01, EVAL-02, EVAL-03]

coverage:
  - id: D1
    description: "evals/lint.py counts buzzword-term violations from an externally-sourced
      registry, with a self-test proving both directions and the longest-match rule"
    requirement: EVAL-01
    verification:
      - kind: unit
        ref: "evals/lint.py#self_test (buzzword-term + longest-match-wins cases)"
        status: pass
      - kind: other
        ref: "python3 evals/lint.py --self-test"
        status: pass
    human_judgment: false
  - id: D2
    description: "evals/proxy-sources.md binds every counted term to Wikipedia MOS:WTW or GSA
      plain-language guidance; proxy-term-unsourced/-invalid/-is-internal make the binding a
      CI-enforced allow-list rather than a promise"
    requirement: EVAL-02
    verification:
      - kind: unit
        ref: "evals/lint.py#self_test (proxy-term-unsourced/-invalid/-is-internal cases)"
        status: pass
    human_judgment: true
    rationale: "The mechanical check proves every shipped term traces outward to one of the
      two named external lists; it cannot prove a human never looked at
      worked-examples.md while curating which external-list entries to ship, and the
      docstring says so explicitly. Whether the curation was in fact blind is a
      verification:backstop truth (05-01-PLAN.md), not something this code can attest to."
  - id: D3
    description: "The DISCLAIMER constant states the deletion-test ceiling and the
      not-a-compliance-verdict ceiling in every lint() result and every printed invocation"
    requirement: EVAL-03
    verification:
      - kind: unit
        ref: "evals/lint.py#self_test (disclaimer-sentence assertions)"
        status: pass
    human_judgment: false

duration: ~35min
completed: 2026-09-18
status: complete
---

# Phase 5 Plan 1: Deterministic Proxy Linter Summary

**A stdlib-only proxy linter with eight discrimination-proven violation codes, wired to a
two-source external provenance registry so the benchmark's buzzword list cannot be circular.**

## Performance

- **Duration:** ~35 min (exact start timestamp not captured; estimated from session length)
- **Completed:** 2026-09-18
- **Tasks:** 3
- **Files modified:** 3 (2 created, 1 modified)

## Accomplishments

- `evals/proxy-sources.md` ships as the single authoritative registry: 22 buzzword/jargon terms
  (12 Wikipedia MOS:WTW puffery terms, 10 GSA plain-language jargon terms), 5 dedicated
  superlative terms, and 3 hedge/modal terms (`may`, `might`, `could`), every row labeled `A` or
  `B` with a URL under an allow-listed external prefix.
- `evals/lint.py` implements all eight frozen violation codes (`buzzword-term`,
  `unquantified-superlative`, `claim-without-adjacent-number`, `sentence-over-ceiling`,
  `unbounded-modal`, `proxy-term-unsourced`, `proxy-term-source-invalid`,
  `proxy-term-source-is-internal`), each proven in both directions by its own dedicated fixture
  pair inside `self_test()` — no fixture trips two codes at once.
- The module docstring names all eight codes plus three non-negotiable ceilings (the deletion
  test is a semantic judgment this file cannot perform; provenance is proven outward, not blind
  curation; sentence segmentation is naive), in `tools/check_repo.py`'s own sentence class.
- `.github/workflows/ci.yml` runs `python3 evals/lint.py --self-test` on every push/PR, added as
  one new line inside the existing single `run: |` block with no new job, step, or live-model call.
- All five pre-existing CI gate commands still pass unchanged, and `--mutation-test` still
  reports 48 codes discrimination-proven — this plan added no code to `tools/check_repo.py`.

## Task Commits

Each task was committed atomically:

1. **Task 1: One proxy term, end to end** — `9b0c6d2` (feat) — buzzword-term +
   proxy-term-unsourced, tracer feedback gate re-verified before expansion
2. **Task 2: Four remaining proxy codes** — `d262fee` (feat) — unquantified-superlative,
   claim-without-adjacent-number, sentence-over-ceiling, unbounded-modal
3. **Task 3: Close the provenance allow-list** — `da0bd98` (feat) —
   proxy-term-source-invalid, proxy-term-source-is-internal, full docstring ceilings

_Note: tasks carried `tdd="true"`; test assertions and implementation were built and verified
together per task rather than as separate RED/GREEN commits — see Deviations below._

## Files Created/Modified

- `evals/proxy-sources.md` — the two-source, mechanically-checked provenance registry (93 lines)
- `evals/lint.py` — the stdlib-only linter, self-test, and eight violation codes (674 lines)
- `.github/workflows/ci.yml` — one new line, `python3 evals/lint.py --self-test`

## Decisions Made

See `key-decisions` in frontmatter. The two decisions with the most downstream consequence for
05-02/05-03: (1) `HEDGE_TERMS`/`SUPERLATIVE_TERMS` are disjoint from `PROXY_TERMS` by design, so
future term additions to the buzzword table should not silently reuse a superlative/hedge word
without checking for accidental fixture co-firing; (2) registry provenance (`check_provenance`)
is a separate call from `lint()`, so a future runner script wanting registry-drift detection in
a live run must call `check_provenance()` explicitly, not assume `lint()` already covers it.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Plan self-contradiction] Task 1's `<behavior>` and `<acceptance_criteria>`
disagree on whether `class` is a registry row**
- **Found during:** Task 1
- **Issue:** The `<behavior>` block states "`class` is also a registry row"; the
  `<acceptance_criteria>` block states "`class` is not itself a registry row in this task —
  the longest-match rule is asserted by a self-test case, not merely intended." These are
  literal opposites.
- **Fix:** Followed `<acceptance_criteria>` (the testable, authoritative contract). `class` was
  never added to `PROXY_TERMS` or the registry — adding a bare, non-puffery English word to a
  shipped buzzword list to satisfy a self-test artifact would itself have been a Rule-2-adjacent
  correctness problem (false-positive risk on ordinary technical prose) and would have violated
  the plan's own prohibition against sourcing a term from anywhere but the two named external
  lists. The longest-match-wins mechanism is instead proven directly: `self_test()` builds a
  local `('class', 'best-in-class')` pattern via the same `_build_term_pattern()` the shipped
  code uses, and asserts it produces exactly one match on `"This best-in-class platform ships
  today."` This exercises the identical code path `lint()` uses for the real registry, without
  shipping an invented term.
- **Files modified:** evals/lint.py (`self_test()`)
- **Verification:** `python3 evals/lint.py --self-test` passes; the probe assertion is one of
  the eight self-test blocks.
- **Committed in:** `9b0c6d2` (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 plan self-contradiction, Rule 1 class).
**Impact on plan:** No scope creep — the fix kept the registry's honesty guarantee (every term
traces outward to one of the two named external lists) intact while still literally satisfying
the acceptance criterion's own wording.

## Issues Encountered

- The plan's Task 2 instruction to add a "Superlative terms" table as "the label-A subset the
  buzzword list draws on" would, if read as reusing the same 12 buzzword terms verbatim, make
  every `unquantified-superlative` fixture also trip `buzzword-term` — directly contradicting
  the same task's explicit "never let a fixture trip two codes at once" discipline. Resolved by
  reading "subset" as "additional label-A-sourced terms, not identical to the buzzword table's
  rows" and sourcing five distinct Wikipedia-puffery-style terms (`exceptional`,
  `extraordinary`, `outstanding`, `unbeatable`, `unrivaled`) for the superlative table instead.
  Documented as a design decision (see `key-decisions`), not a deviation, since both readings
  are defensible and this one is the internally consistent one.

## User Setup Required

None — no external service configuration required.

## Known Stubs

None. `evals/lint.py`'s live-run mode (`python3 evals/lint.py <path>`) is fully implemented,
not a placeholder; it is simply not yet invoked by any other script in this repository (05-02/
05-03 will call it against generated benchmark text).

## Threat Flags

None beyond what 05-01-PLAN.md's own threat model already names and mitigates (T-05-01 through
T-05-05, T-05-SC) — no new network endpoint, auth path, or schema change was introduced.

## Next Phase Readiness

- `evals/lint.py` and `evals/proxy-sources.md` are ready for 05-02/05-03 to import and call
  `lint()` against live-model-generated benchmark text.
- No blockers. `evals/lint.py`'s live-run `--json` mode gives 05-02/05-03 a machine-readable
  shape (`violations`, `violations_total`, `by_code`, `disclaimer`) to aggregate directly.

---
*Phase: 05-evaluation-harness*
*Completed: 2026-09-18*

## Self-Check: PASSED
