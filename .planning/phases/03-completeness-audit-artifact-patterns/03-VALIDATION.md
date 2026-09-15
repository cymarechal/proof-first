---
phase: "03"
slug: "completeness-audit-artifact-patterns"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: true
created: "2026-09-15"
---

# Phase 03 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
>
> **Seeded at gap-closure planning time (2026-09-15), after plans 03-01..03-05 had
> already executed.** Its scope is the gap-closure work that follows, not a
> retrospective contract over the five plans already shipped. Baseline figures below
> are the *current* post-execution numbers (27 discrimination-proven codes), not the
> 22-code pre-phase baseline recorded in `03-RESEARCH.md`'s Validation Architecture.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `tools/check_repo.py`'s own `--self-test` / `--mutation-test` harness (no pytest/jest, by design) |
| **Config file** | none |
| **Quick run command** | `python3 tools/check_repo.py --self-test` |
| **Full suite command** | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` |
| **Estimated runtime** | ~5 seconds (all three commands) |

**Baseline this gap-closure run must not regress** (re-measured in `03-VERIFICATION.md`,
2026-09-15T01:56:13Z):

```
python3 tools/check_repo.py --self-test      → self-test PASS, 27 violation codes verified   (exit 0)
python3 tools/check_repo.py --mutation-test  → mutation-test PASS: 27 codes discrimination-proven,
                                                CONTROL 0 unexpected                          (exit 0)
python3 tools/check_repo.py                  → check_repo: 0 violations                       (exit 0)
```

Any new check must raise the discrimination-proven count above 27, never lower it, and the
CONTROL line must keep reading `0 unexpected`.

**Hard constraint carried into this run:** `skills/proof-first/SKILL.md` sits at 3700 words /
4810 estimated tokens against the 5000-token ceiling `skill-token-budget-exceeded` enforces —
a **190-token margin**. Any SKILL.md edit must fit inside it or pay for itself by trimming
restatement. `python3 tools/check_repo.py` is the gate that catches an overrun.

---

## Sampling Rate

- **After every task commit:** `python3 tools/check_repo.py --self-test`
- **After every plan wave:** `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py`
- **Before `/gsd-verify-work`:** full suite green, plus a live-harness conformance run for any
  model-behaviour truth the gap-closure plans claim to close
- **Max feedback latency:** ~5 seconds for the static suite; a live-harness conformance run is
  minutes, not seconds, and is a phase-gate activity rather than a per-commit one

---

## Per-Task Verification Map

Filled by the gap-closure plans themselves — each task's `<verify><automated>` command plus its
`<fails_when>` statement is the authoritative row. This table is populated by
`/gsd-validate-phase` after the plans land.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| — | 03-06+ | 1 | MOD-04 | — | N/A | static + live | `python3 tools/check_repo.py` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all gap-closure requirements. `tools/check_repo.py` exists with
27 discrimination-proven codes; no new test scaffolding is needed to verify a SKILL.md or
`references/*.md` content edit.

The live-harness conformance runner is **not** committed infrastructure — it is the ad-hoc
recipe recorded in `03-UAT.md`'s `## Method` (isolated dir outside the repo, skill copied to
`.claude/skills/proof-first/`, fresh `claude -p` per session with
`--disallowedTools Write Edit Bash NotebookEdit`, no `--bare`, one writer per output file).
A plan that claims to close MOD-04 must re-run that recipe, not assert conformance.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| A live write-mode session names the artifact family before applying any rule, in **every** session | MOD-04 | No file-reading checker can observe what a future live model session does. `check_repo.py` can assert the instruction text is present (already ✓ at `SKILL.md:261` and `SKILL.md:275`); it cannot assert the session obeys it. | Re-run `03-UAT.md`'s `## Method` recipe in write mode across ≥16 scoreable sessions, ≥2 models, ≥5 fixtures. Score: did the response name a family (or the `**No family fits:**` fallback) before the first applied rule marker? Current measured rate is 14/16. |
| A standalone completeness audit returns `## Completeness gaps` **and nothing more** | AUD-03 | Same class — live-session output shape. | Standalone-audit sessions per `03-UAT.md` test 1. Current record: 9/9 met the stated criterion; 1 of the 9 additionally printed an extra `## Artifact family` heading (`WINDOWS.md` entry 7). |
| No source-coined term is adopted as this repository's own unattributed label | AUD-01, ART-01..04 | `SOURCES.md` states the paraphrase boundary is a semantic judgement no tool in this stack performs. Two independent **subagent** reads are the closest available proxy, not a substitute. | An actual human reads the eight MC bodies and four family sections against `SOURCES.md` lines 11-22. Owned by **Phase 6 LEG-04** (`WINDOWS.md` entries 3, 6, 9) — not closable in Phase 3. |

**Expect the model-behaviour half of MOD-03, MOD-04, MOD-05, AUD-01 and AUD-03 to remain
`nyquist_compliant: false` permanently.** That is a property of the deliverable (a prompt-time
skill), not a shortfall in this phase's test discipline. Say so in the plan's Definition of
Done rather than promising verification the phase cannot deliver.

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references — existing `check_repo.py` suffices
- [x] No watch-mode flags
- [x] Feedback latency < 10s for the static suite
- [ ] `nyquist_compliant: true` set in frontmatter — will stay `false`; MOD-04's remaining half is model behaviour

**Approval:** pending
