---
phase: "01"
slug: "foundations-legal-scaffolding-numbering-shared-deal"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: false
wave_0_complete: true
created: "2026-09-10"
---

# Phase 01 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Reconstructed from phase artifacts (State B — no VALIDATION.md existed; 7 SUMMARYs present).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None — `tools/check_repo.py` is a stdlib-only, self-contained checker that *is* the test harness. Zero pip dependencies, per the project's zero-dependency constraint. |
| **Config file** | none — no pytest.ini / pyproject.toml / tox.ini exists, and none is wanted |
| **Quick run command** | `python3 tools/check_repo.py` |
| **Full suite command** | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` |
| **Estimated runtime** | ~1 second (all three modes) |
| **CI** | `.github/workflows/ci.yml` runs all three commands in that order on every push and pull request |

The harness has three modes, and the distinction matters for what each proves:

- `--self-test` — fixture-based. Asserts each violation code fires on a hand-built known-bad
  fixture and stays silent on a known-good one.
- `--mutation-test` — injects one named defect per violation code into a throwaway copy of the
  **real** repository documents and asserts that code fires. This closes the "a check exists,
  is named as covered, runs in CI, and cannot fire" class that produced this phase's original
  BLOCKER.
- live run — must print `check_repo: 0 violations` and exit 0 against the shipped repo.

---

## Sampling Rate

- **After every task commit:** Run `python3 tools/check_repo.py`
- **After every plan wave:** Run the full suite (all three modes)
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** ~1 second

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01 | 01 | 1 | CAT-07 | — | N/A | unit | `python3 tools/check_repo.py --self-test` | ✅ | ✅ green |
| 01-01 | 01 | 1 | CAT-07 | — | N/A | mutation | `python3 tools/check_repo.py --mutation-test` | ✅ | ✅ green |
| 01-02 | 02 | 2 | EX-01 | — | N/A | unit | `python3 tools/check_repo.py --self-test` | ✅ | ✅ green |
| 01-02 | 02 | 2 | EX-01 | — | N/A | mutation | `python3 tools/check_repo.py --mutation-test` | ✅ | ✅ green |
| 01-03 | 03 | 2 | LEG-01 | — | N/A | unit + mutation | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test` | ✅ | ✅ green |
| 01-03 | 03 | 2 | LEG-02 | — | N/A | unit + mutation | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test` | ✅ | ✅ green |
| 01-03 | 03 | 2 | LEG-03 | — | N/A | manual | — | ❌ | ⬜ manual-only (see below) |
| 01-04 | 04 | 3 | CAT-07, EX-01 | — | N/A | integration | `python3 tools/check_repo.py` | ✅ | ✅ green |
| 01-05 | 05 | gap | CAT-07, EX-01 | — | N/A | unit + mutation | full suite | ✅ | ✅ green |
| 01-06 | 06 | gap | CAT-07, EX-01 | — | N/A | unit + mutation | full suite | ✅ | ✅ green |
| 01-07 | 07 | gap | CAT-07, EX-01 | — | N/A | mutation | `python3 tools/check_repo.py --mutation-test` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

### Requirement → violation-code coverage

| Requirement | Violation codes enforcing it | Verdict |
|---|---|---|
| **CAT-07** — stable citable IDs in two disjoint namespaces, ranges reserved per section | `dup-id`, `range-id`, `revived-id`, `undefined-id` | COVERED |
| **EX-01** — one canonical deal brief supplies every example's facts | `dup-figure-key`, `figure-order`, `unlisted-figure` | COVERED (two declared ceilings) |
| **LEG-01** — repo ships an MIT license | `license-missing` | COVERED (declared ceiling) |
| **LEG-02** — NOTICES.md individually names all three frameworks with non-affiliation and trademark language | `framework-statement-missing` | COVERED |
| **LEG-03** — zero proprietary framework text reproduced | *none, by design* | MANUAL-ONLY |

---

## Wave 0 Requirements

Existing infrastructure covers all automatable phase requirements. No framework install is
needed or wanted — introducing one would violate the project's zero-dependency constraint.

---

## Validation Audit 2026-09-10

| Metric | Count |
|--------|-------|
| Gaps found | 2 |
| Resolved | 2 |
| Escalated | 0 |

Two Phase-1 requirements were true on disk but had zero automated verification: nothing in CI
fired if `LICENSE` was replaced or if a framework statement was deleted from `NOTICES.md`. That
is the same "named as covered but cannot fire" defect class 01-05 and 01-07 were written to
close, so both were closed rather than recorded as accepted risk.

**Codes added to `tools/check_repo.py` (10 → 12):**

| Code | Requirement | Fires when | Declared ceiling |
|---|---|---|---|
| `license-missing` | LEG-01 | `LICENSE` is absent from the repo root, is empty, or does not **begin with** the string `MIT License` | Only the first line is inspected; the body is never compared against the full MIT text, so a file carrying `MIT License` as its first line over a different license body is accepted |
| `framework-statement-missing` | LEG-02 | `NOTICES.md` is absent, or its `## Framework statements` section is missing any of the three required subsections, or a subsection is present but lacks its non-affiliation or trademark-rights language. Fires **per missing framework**, naming which one; when `NOTICES.md` is absent all three are reported | Matches on heading text plus the `Non-affiliation` / `not affiliated` / `Rights-holder` markers; does not validate subsection ordering or assert the count is exactly three |

Per-framework (not aggregate) reporting was required deliberately: LEG-02 says *individually
named*, so one aggregate boolean would repeat the exact defect 01-06 Task 2 fixed for MC ranges.

**Orchestrator verification of the auditor's work.** The auditor's first result was returned
with all three CI commands green, and was rejected. Independent reproduction found three
defects, two of them violations of the docstring-honesty contract this phase's original BLOCKER
was built from and which UAT checkpoint 3 signs off:

1. **Docstring/code mismatch.** The docstring described a substring predicate (`does not
   contain … in its first line`) while the code implemented `startswith`. A `LICENSE` beginning
   `The MIT License` satisfies the documented predicate but fails the implemented one.
   *Fixed:* docstring now reads "does not begin with", matching the code.
2. **Undeclared ceiling.** A `LICENSE` whose first line is `MIT License` over an Apache-2.0 body
   passed silently, with no ceiling declared. *Fixed:* ceiling now stated in the docstring, in
   the same plain style as the `unlisted-figure` and `pointer-missing` entries.
3. **A check that could not fire.** `check_framework_statements()` returned empty when
   `NOTICES.md` was absent, so deleting the file produced `check_repo: 0 violations`, exit 0 —
   LEG-02 maximally violated with CI green. *Fixed:* all three frameworks are now reported when
   the file is absent, and the mutation entry deletes the whole file.

All three fixes were re-verified by independent reproduction, not by accepting the report.

**Coverage note.** The `framework-statement-missing` mutation entry was changed to delete
`NOTICES.md` wholesale, so the missing-*subsection* path is no longer mutation-proven. It
remains covered by the `--self-test` fixture `_bad_notices_frameworks()`, which ships a present
`NOTICES.md` lacking only `### Command of the Message`. Both paths are therefore covered, but
across two harnesses rather than one. Independently reproduced: removing only `### Challenger`
from the real file yields `framework-statement-missing Challenger subsection is missing`, exit 1.

**Out of scope, left unchanged (pre-existing, not introduced here):** `run_notices_checks()`
carries the same early return when `NOTICES.md` is absent, so the `pointer-*` family still
cannot fire on a deleted `NOTICES.md`. This was deliberately not touched — it belongs to the
pointer family, not to either gap under audit. Worth a future ticket.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| No proprietary framework text is reproduced anywhere in the repo; concepts are paraphrased and sources cited | LEG-03 | Not mechanically decidable. `check_repo.py`'s own module docstring states it "does not read framework source material and it cannot judge whether a paraphrase reproduces proprietary text — that judgement is Phase 6's legal review gate (LEG-04)." No linter settles it either. | Phase 6 legal review gate (LEG-04): read framework-derived prose against the approved sources listed in `SOURCES.md` and confirm the reproduction boundary holds. |
| The 9 invented deal-brief names collide with no real company or identifiable person | LEG-04 (scoped) | Requires live network access. | Web-search each of the 9 names. Recorded in `01-UAT.md` test 1 — **passed 2026-09-10**. |
| `examples/deal-brief.md` contains no sentence comparing two real companies or products | LEG-04 (scoped) | The originating plan requires a reviewer distinct from the author; author self-review is a substitute, not the specified check. | Independent end-to-end read. Recorded in `01-UAT.md` test 2 — **passed 2026-09-10**. |
| Every `check_repo.py` docstring violation-code entry honestly describes what the code does | CAT-07 (harness integrity) | A judgment a grep cannot make. | Read all violation-code entries against their functions. Recorded in `01-UAT.md` test 3 — **passed 2026-09-10**. Re-confirmed this session for the two new entries after the docstring/code mismatch above was fixed. |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies — except LEG-03, manual by design
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references — no Wave 0 needed
- [x] No watch-mode flags
- [x] Feedback latency < 5s (~1s measured)
- [ ] `nyquist_compliant: true` — **not set.** LEG-03 has no automated verification and cannot
      have one; it is deferred to the Phase 6 LEG-04 legal gate. The phase is validated-PARTIAL:
      4 of 5 requirements automated, 1 manual-only by design.

**Approval:** approved 2026-09-10
