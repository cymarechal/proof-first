---
phase: "2"
slug: "rule-catalog-integrity-skill-md-core"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: false
wave_0_complete: true
created: "2026-09-11"
validated: "2026-09-11"
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

Filled by `/gsd-validate-phase` against the nine executed plans. Granularity is
per-plan: the PLAN files carry `wave:` frontmatter but no per-task IDs, so the
Plan column is the traceable unit and the Task ID column records that fact
rather than inventing identifiers.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| plan-level | 02-01, 02-06 | 1, 6 | CAT-09 (D-33) | T-2-01 | Malformed frontmatter is rejected locally, not silently at distribution time | unit | `python3 tools/check_repo.py --self-test` | ✅ 4 codes: `frontmatter-unparseable`, `-unknown-key`, `-name-mismatch`, `-description-invalid` | ✅ green |
| plan-level | 02-01, 02-06, 02-07 | 1, 6 | CAT-01, CAT-02, CAT-06 ID/count integrity (D-32) | T-2-19 | A drifted or unstated rule count cannot ship silently | unit | `python3 tools/check_repo.py --self-test` | ✅ 3 codes: `catalog-id-drift`, `catalog-count-unstated`, `catalog-count-mismatch` | ✅ green |
| plan-level | 02-09 (this audit) | — | **CAT-03** | — | A second opening rule cannot be added without the checker firing | unit | `python3 tools/check_repo.py --self-test` | ✅ new code `catalog-opening-rule-count` (`tools/check_repo.py:963`) | ✅ green |
| plan-level | 02-05, 02-06 | 5, 6 | MOD-01/MOD-02 (D-05 sub-block ranges) | T-2-21 | A PF ID landing in a declared sub-block gap is caught, not decorative | unit | `python3 tools/check_repo.py --self-test` | ✅ `range-id` sub-block branch + gapped fixture (`tools/check_repo.py:2175`) | ✅ green |
| plan-level | 02-01…02-09 | all | D-34 — every registered check proven live | T-2-04 | A check named as covered but unable to fire is caught by discrimination testing | mutation | `python3 tools/check_repo.py --mutation-test` | ✅ 22 codes discrimination-proven | ✅ green |
| plan-level | 02-06, 02-08 | 6, 2 | CAT-08 — progressive-disclosure ceiling | T-2-20 | SKILL.md silently outgrowing its budget is caught in CI, not at install time | scripted count | `python3 tools/check_repo.py` | ✅ 2 codes: `skill-too-long` (500 lines), `skill-token-budget-exceeded` | ✅ green |
| plan-level | 02-03, 02-04, 02-05 | 3, 4, 5 | CAT-04, CAT-05, INT-01…INT-06, MOD-01, MOD-02, CAT-10 rule *behavior* | T-2-03, T-2-06…T-2-18 | Skill refuses fabricated metrics/references/certifications and flags them for a human | manual (UAT) | none — model behavior, not a file property | N/A — see Manual-Only | ⬜ manual-only |

*Status: ⬜ pending/manual · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] Frontmatter parser + `run_frontmatter_checks` + fixtures + one mutation per new code — covers CAT-09 / D-33
- [x] PF ID-set + stated-count equality parser + `run_catalog_checks` + fixtures + mutations — covers D-32
- [x] `PF-2` sub-block range fixture extending `check_range_id` to per-sub-block containment — covers D-05 enforcement
- [x] CAT-08 line ceiling decided: CI enforces it. `skill-too-long` (500-line) and `skill-token-budget-exceeded` both ship with mutations, so this is no longer authoring discipline.

---

## Manual-Only Verifications

Nine of the ten gaps this audit examined are model-behavior or live-harness
properties. No test written in this repository's stack can assert them:
`tools/check_repo.py` reads Markdown, and none of these are facts about a file.
Phase 5's eval harness is the designated mechanism for measuring them, not a
test file added here. Recording them as manual-only is the correct permanent
result for Phase 2, not a deferred TODO.

**On the structural proxy.** The seven integrity rules PF-2.11–PF-2.17 carry
INT-01…INT-06, and `catalog-id-drift` does fire if any of those rows is deleted
from the catalog. That proves the *instruction* still ships. It does not prove
the skill *obeys* it. The proxy is recorded here so nobody mistakes a green
checker for verified refusal behavior.

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Deletion test distinguishes a load-bearing technical term from a buzzword | CAT-04 | Semantic judgment; SOURCES.md states no tool in the stated stack performs it | Run the skill on a paragraph containing both a real technical term and a buzzword; confirm the buzzword is replaced with an evidence-attachment instruction and the technical term survives |
| A term appearing verbatim in the customer's own source material is marked, not deleted | CAT-05 | Requires cross-reading `examples/deal-brief.md` source material against skill output | Draft against a deal-brief quote containing customer jargon; confirm PF-3.3 fires and the term is marked as customer-sourced rather than cut |
| Skill refuses to invent metrics, reference customers, benchmark numbers, certifications | INT-01 | Refusal is a model-behavior property, not a file property. Structural proxy: PF-2.11/PF-2.12 allocated, guarded by `catalog-id-drift` | Prompt the skill with a scenario lacking a baseline figure; confirm it emits a GAP marker rather than a plausible number |
| Skill marks an evidence gap for a human instead of filling it | INT-02 | As above. Structural proxy: PF-2.4/PF-2.13 allocated | Prompt with a claim having no attached evidence; confirm a GAP marker appears in place of the claim |
| Skill flags commitment-shaped language | INT-03 | As above. Structural proxy: PF-2.14 allocated | Seed prose with warranty-shaped phrasing ("we will ensure…"); confirm it is flagged for human review |
| Skill flags customer reference details needing disclosure permission | INT-04 | As above. Structural proxy: PF-2.15 allocated | Seed a named customer reference; confirm it is flagged pending disclosure permission |
| Skill flags competitor comparisons | INT-05 | As above. Structural proxy: PF-2.16 allocated | Seed a named-competitor comparison; confirm it is flagged as legal exposure |
| Skill flags compliance, certification, and export claims | INT-06 | As above. Structural proxy: PF-2.17 allocated | Seed a SOC 2 / ISO / export-control claim; confirm it is flagged for human verification |
| Draft mode produces catalog-conformant output | MOD-01 | Model output shape under live invocation | Invoke write mode with a presales scenario; confirm output follows the artifact-family → prose → register structure with no rule-cite list |
| Check mode returns rule number + offending text + compliant rewrite per violation | MOD-02 | Model output shape under live invocation | Invoke check mode on seeded-violation prose; confirm integrity flags and prose violations appear as separately labeled sections and each finding carries rule ID, exact quoted text, and a rewrite |
| `description` triggers the skill reliably on presales writing requests | CAT-10 | Requires driving a live harness session this environment cannot start | Run each of the 14 phrasings in `evals/pressure-tests.md` in a fresh harness session and record Observed/Date/Harness. Hash-bind first: `head -14 skills/proof-first/SKILL.md \| shasum -a 256` must equal `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`. **Do not write observations that were not run.** |

---

## Validation Sign-Off

- [x] All automatable requirements have an automated verify command
- [x] Sampling continuity: the full suite runs in ~5s, well under the 10s latency budget
- [x] Wave 0 covers all MISSING references that a file-reading checker can cover
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [ ] `nyquist_compliant: true` — **not set, and correctly so.** Nine requirements (CAT-04, CAT-05, INT-01…INT-06, MOD-01, MOD-02, CAT-10) describe model behavior or live-harness activation. Full Nyquist compliance is unreachable for this phase by design, not by omission.

**Approval:** validated 2026-09-11 — partial. 22 checker codes green; 9 requirements manual-only.

---

## Validation Audit 2026-09-11

| Metric | Count |
|--------|-------|
| Gaps found | 10 |
| Resolved | 1 |
| Escalated | 9 |

**Resolved.** CAT-03 — added `catalog-opening-rule-count` (`tools/check_repo.py:963`),
wired into `run_catalog_checks`, registered in `CATALOG_CHECK_CODES`, with a silent
good-fixture, a firing bad-fixture, and a `MUTATIONS` entry that adds a second PF-0
rule to both `NUMBERING.md` and `references/checklist.md`. Before this check,
`NUMBERING.md:19` reserved PF-0.1–PF-0.9 with `next: PF-0.2` — a tenth opening rule
could have been added with the whole suite still green, silently breaking CAT-03's
"exactly one opening rule".

**Escalated.** Nine requirements to Manual-Only, listed above with test instructions.

**Suite state, measured 2026-09-11:**

```
self-test PASS - 22 verified violation codes
mutation-test PASS: 22 codes discrimination-proven (CONTROL: 0 violations on the unmutated copy)
check_repo: 0 violations
```

All three commands exit 0, matching `.github/workflows/ci.yml`'s job order.

**One observation, not blocking.** `check_catalog_opening_rule_count` hardcodes
`skills/proof-first/references/checklist.md` rather than reusing the `skills/*/`
glob the sibling checks use. The path is `.exists()`-guarded, so a rename would
silently skip the checklist half while the `NUMBERING.md` half kept firing. Worth
aligning when another check next touches that file; it does not weaken CAT-03
enforcement today.
