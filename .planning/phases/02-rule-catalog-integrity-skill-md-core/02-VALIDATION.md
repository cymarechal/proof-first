---
phase: "2"
slug: "rule-catalog-integrity-skill-md-core"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-11"
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded by `/gsd-plan-phase` from `02-RESEARCH.md` § Validation Architecture.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `tools/check_repo.py` self-test / mutation-test harness — no pytest/jest by design (STACK.md: no test framework beyond the linter's own self-test) |
| **Config file** | none — `tools/check_repo.py` is both the checker and its own test runner |
| **Quick run command** | `python3 tools/check_repo.py --self-test` |
| **Full suite command** | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` |
| **Estimated runtime** | ~5 seconds (stdlib-only Python, single pass over repo Markdown) |

---

## Sampling Rate

- **After every task commit:** Run `python3 tools/check_repo.py --self-test`
- **After every plan wave:** Run `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py`
- **Before `/gsd-verify-work`:** Full suite must be green (same job order as `.github/workflows/ci.yml`)
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

Task IDs are assigned when PLAN.md files are written; this map seeds the
requirement → command binding the planner must honour, and `/gsd-validate-phase`
fills the Task ID / Plan / Wave columns against the real plans.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| TBD | TBD | 0 | CAT-09 (D-33) | T-2-01 | Malformed frontmatter is rejected locally, not silently at distribution time | unit | `python3 tools/check_repo.py --self-test` | ❌ W0 — new parser + fixtures | ⬜ pending |
| TBD | TBD | 0 | CAT-01…CAT-06 ID integrity (D-32) | — | N/A | unit | `python3 tools/check_repo.py --self-test` | ❌ W0 — new extractor + fixtures | ⬜ pending |
| TBD | TBD | 0 | MOD-01/MOD-02 (D-05 sub-block ranges) | — | N/A | unit | `python3 tools/check_repo.py --self-test` | ⚠️ partial — extends existing `check_range_id` | ⬜ pending |
| TBD | TBD | 1 | D-34 — every new check proven live | — | N/A | mutation | `python3 tools/check_repo.py --mutation-test` | ❌ W0 — new `MUTATIONS` entries | ⬜ pending |
| TBD | TBD | 1 | CAT-08 — progressive-disclosure ceiling | — | N/A | scripted count | `wc -l skills/proof-first/SKILL.md` | ❌ — no CI gate exists; see Manual-Only below | ⬜ pending |
| TBD | TBD | — | CAT-02…CAT-06, INT-01…INT-06 rule content | — | Skill refuses fabricated metrics/references/certifications and flags them for a human | manual (UAT) | none — semantic judgment, not mechanically checkable | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Frontmatter parser + `run_frontmatter_checks` + `_bad_frontmatter()` / `_good_frontmatter()` fixtures + one mutation per new code — covers CAT-09 / D-33
- [ ] PF ID-set + stated-count equality parser (rule-defining-heading extractor, checklist-row extractor) + `run_catalog_consistency_checks` + fixtures + mutations — covers D-32
- [ ] `PF-2` sub-block range fixture extending `check_range_id`'s per-section logic to per-sub-block — covers D-05 enforcement (the table itself is a `NUMBERING.md` content edit)
- [ ] Decide and record: whether CI enforces the CAT-08 line ceiling or it stays authoring discipline with a mid-draft checkpoint (no D-3x decision covers this — see Manual-Only)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Deletion test correctly distinguishes a load-bearing technical term from a buzzword | CAT-02, CAT-03 | Semantic judgment; SOURCES.md states no tool in the stated stack performs it | Run the skill on a paragraph containing both a real technical term and a buzzword; confirm the buzzword is replaced with an evidence-attachment instruction and the technical term survives |
| A term appearing verbatim in the customer's own source material is marked, not deleted | CAT-04 | Requires cross-reading `examples/deal-brief.md` source material against skill output | Draft against a deal-brief quote containing customer jargon; confirm the term is marked as customer-sourced |
| Exactly one opening reframe instruction is resolved from three source frameworks | CAT-05 | Requires reading the catalog for conflicting instructions | Read the catalog's opening section; confirm one reframe rule, no reconciliation left to the reader |
| Check-mode returns rule number + offending text + compliant rewrite for each violation | CAT-06 | Output-shape judgment across varied input prose | Run check mode on a seeded-violation paragraph; confirm all three fields per violation |
| Integrity refusals: invented metrics, undisclosed references, competitor comparisons, unverified compliance/export claims | INT-01…INT-06 | Refusal behavior is a model-behavior property, not a file property | Prompt the skill with each of the five fabrication classes; confirm each is flagged for a human rather than invented |
| SKILL.md stays under the progressive-disclosure ceiling | CAT-08 | Depends on whether Wave 0 adds a CI gate; if not, this is authoring discipline | `wc -l skills/proof-first/SKILL.md` at a mid-draft checkpoint and at phase end; baseline for comparison: sibling `simple-english/SKILL.md` = 329 lines |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
