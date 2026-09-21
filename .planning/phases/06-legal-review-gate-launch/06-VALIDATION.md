---
phase: "6"
slug: "legal-review-gate-launch"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-21"
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Derived from `06-RESEARCH.md` § Validation Architecture.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None. House pattern: every script implements its own `--self-test` with inline assertions, and `tools/check_repo.py` additionally implements `--mutation-test`, which injects one named defect per code into a throwaway copy of the real repository files and asserts the matching code fires. |
| **Config file** | `.github/workflows/ci.yml` — 10 commands, all offline, all stdlib-only |
| **Quick run command** | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py` |
| **Full suite command** | the 10 commands in `.github/workflows/ci.yml`, in file order |
| **Estimated runtime** | ~12 s measured 2026-09-21 (`--mutation-test` is 8.1 s of it, up from 1 s before Phase 5 committed `evals/benchmark/raw/`) |

**This phase adds no framework, no dependency, and no network call to CI.** Every network lookup
it performs happens once, at review time, and its *output* — a URL plus a retrieval date — is
committed. The checks read that committed record offline.

---

## Sampling Rate

- **After every task commit:** `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py`
- **After every plan:** all 10 CI commands in order, plus `python3 tools/check_repo.py --mutation-test`
- **Before `/gsd-verify-work`:** all 10 green, and every code this phase adds reported
  discrimination-proven — not merely registered
- **Max feedback latency:** 15 seconds for the quick command, 30 seconds including the mutation pass

**A registered-but-not-discriminating check is this repository's named recurring defect**
(`WINDOWS.md` id 10, and the `01-VERIFICATION.md` finding that created the mutation harness). For
every code this phase adds, the mutation entry is part of the same task as the code, never a
follow-up.

---

## Per-Task Verification Map

**A = `06-01-PLAN.md`** (wave 1, tracer), **B = `06-02-PLAN.md`** (wave 2),
**C = `06-03-PLAN.md`** (wave 3), **D = `06-04-PLAN.md`** (wave 4, launch gate).

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 06-01-01 | A | 1 | LEG-04 | — | A `SOURCES.md` row claiming `verified` without an `https://` URL and an ISO-8601 retrieval date in its `Where` cell is a build failure | unit (offline) | `python3 tools/check_repo.py --self-test` | ✅ | ⬜ pending |
| 06-01-02 | A | 1 | LEG-04 | — | `source-row-unconfirmed` is silent on an unmutated copy of the real `SOURCES.md` and fires on a mutated one | mutation (offline) | `python3 tools/check_repo.py --mutation-test` | ✅ | ⬜ pending |
| 06-02-01 | B | 2 | LEG-04 | — | Every remaining `SOURCES.md` row carries a real URL and retrieval date; no row is left `unverified` | unit (offline) | `python3 tools/check_repo.py` | ✅ | ⬜ pending |
| 06-02-02 | B | 2 | LEG-04 | — | The review record cannot declare the gate passed while any row is `unverified` | unit + mutation (offline) | `python3 tools/check_repo.py --mutation-test` | ✅ | ⬜ pending |
| 06-02-03 | B | 2 | LEG-04 | — | The three `NOTICES.md` framework statements keep their four labelled elements in fixed order after re-dating | unit (offline) | `python3 tools/check_repo.py` | ✅ | ⬜ pending |
| 06-03-01 | C | 3 | LEG-05 | — | Pooled win/tie/loss totals are emitted by `--report-only` from the paired averaging path and the re-rendered file diffs clean | unit (offline) | `python3 evals/benchmark/run_benchmark.py --report-only && git diff --exit-code evals/benchmark/RESULTS.md` | ✅ | ⬜ pending |
| 06-03-02 | C | 3 | LEG-05 | — | A number inside README's claim region that appears in no committed results file is a build failure | unit + mutation (offline) | `python3 tools/check_repo.py --mutation-test` | ✅ | ⬜ pending |
| 06-03-03 | C | 3 | LEG-05 | — | A claim sentence with no model string and no ISO date near it is a build failure | unit + mutation (offline) | `python3 tools/check_repo.py --mutation-test` | ✅ | ⬜ pending |
| 06-03-04 | C | 3 | LEG-05 | — | A badge whose target is not on the stated allow-list is a build failure | unit + mutation (offline) | `python3 tools/check_repo.py --mutation-test` | ✅ | ⬜ pending |
| 06-04-01 | D | 4 | LEG-04 | one-way door | The real publish location replaces `<owner>/<repo>` in all four occurrences and stays mutually consistent | unit (offline) | `python3 tools/check_repo.py` | ✅ | ⬜ pending |
| 06-04-02 | D | 4 | LEG-04 | — | Every `WINDOWS.md` entry is fixed, waived with a stated reason, or routed to v2 with a named owner | manual + ledger query | `node "$GSD_TOOLS" windows list` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. `tools/check_repo.py`,
`evals/benchmark/run_benchmark.py` and `.github/workflows/ci.yml` all exist, all ship self-tests,
and all are already wired into CI. This phase extends them; it builds no new harness.

One structural addition is required in wave 1 and is part of the tracer task rather than a
separate Wave 0 step: `'SOURCES.md'` must be added to `MUTATION_SOURCES` in `tools/check_repo.py`,
because the mutation harness copies exactly that tuple and `SOURCES.md` is not currently in it. The
precedent and its comment discipline are 03-14's addition of `'evals'`.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Each confirmed source actually says what its `SOURCES.md` row claims | LEG-04 | Semantic judgement between a page's content and a row's description. `SOURCES.md` itself states no tool in this stack performs it, and this phase does not build one. | For each row, open the recorded URL and confirm the publisher, kind and subject match the row. Record the outcome in the review record. |
| The inherited MC dimension names and the `MC-1`–`MC-40` ID-range order are paraphrase and not reproduction of a source's own ordered list | LEG-04 (`WINDOWS.md` id 6) | Reproduction-boundary judgement. `SOURCES.md` defines "a source's own ordered list reproduced in its order" as reproduction and states no tool judges it. | Read `skills/proof-first/references/completeness-audit.md` against `NUMBERING.md`'s frozen ranges, and reason explicitly about whether the 2026-04-21 genericness holding changes the analysis. Record the reasoning, not just the verdict. |
| `PF-0.1` / `PF-3.1` framing and the `SOURCES.md` reproduction-boundary read | LEG-04 (`WINDOWS.md` id 3) | Same class. Signed off once at Phase 2 UAT and deliberately kept open for the formal gate. | Re-read both rules against the boundary definition; record the outcome with reasoning in the review record. |
| A Claude Code session lists the copied output style in `/config` and applies it | DIST-03 (`WINDOWS.md` id 16) | Headless `claude -p` sessions have no `/config` picker. Nothing in this repository can drive one. | On a real machine: `mkdir -p ~/.claude/output-styles && cp output-styles/proof-first.md ~/.claude/output-styles/`, start Claude Code, open `/config`, confirm the style is listed and selectable. |
| `npx skills add <owner>/<repo>` and `claude plugin marketplace add <owner>/<repo>` resolve end to end | DIST-01, DIST-02 (`WINDOWS.md` id 11) | Cannot run against an unpublished repository. Blocked on the publish decision, not on tooling. | After publication, run each command in a clean directory and record the observed output. |
| README reads as leading with examples, and no two passages contradict each other | DIST-06 (`WINDOWS.md` ids 12, 17) | Entailment between two independently-phrased passages. Refused as a check on the record, with the refusal's reasoning in `tools/check_repo.py`'s docstring. | A cold read of README end to end by someone who has not just edited it, once per round. |
| No published claim outruns the evidence | LEG-05 | Semantic judgement against `06-RESEARCH.md` § Decision 6's seven named overclaims. | Human read of README's claim region against that list. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or are explicitly listed above as manual-only
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references (none — existing infrastructure)
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] Every check code this phase adds reports discrimination-proven under `--mutation-test`
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
