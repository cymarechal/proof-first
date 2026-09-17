---
phase: "04"
slug: "distribution-worked-examples"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-17"
---

# Phase 04 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
>
> Derived from `04-RESEARCH.md` § Validation Architecture. The baseline figures below
> were re-measured at planning time (2026-09-17) against the current working tree, not
> copied from research prose.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `tools/check_repo.py`'s own `--self-test` / `--mutation-test` harness (no pytest/jest, by design — stdlib only) |
| **Config file** | none |
| **Quick run command** | `python3 tools/check_repo.py --self-test` |
| **Full suite command** | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` |
| **Estimated runtime** | ~1 second (all three commands; self-test measured at 0.13s wall) |

**Baseline this phase must not regress** (measured 2026-09-17 at planning time):

```
python3 tools/check_repo.py --self-test      → self-test PASS, 32 violation codes verified   (exit 0)
python3 tools/check_repo.py --mutation-test  → mutation-test PASS: 32 codes discrimination-proven,
                                                CONTROL 0 violations / 0 unexpected           (exit 0)
python3 tools/check_repo.py                  → check_repo: 0 violations                       (exit 0)
```

Phase 4 is expected to raise the discrimination-proven count to roughly 36–38 and must
never lower it. The CONTROL line must still read `0 unexpected`.

---

## Sampling Rate

- **After every task commit:** `python3 tools/check_repo.py --self-test`
- **After every plan wave:** `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py`
- **Before `/gsd-verify-work`:** full suite green, plus a UAT pass covering the model-behavior half of DIST-03/DIST-04
- **Max feedback latency:** ~1 second

---

## Per-Task Verification Map

Task IDs are assigned by the planner; this map is keyed by requirement and is the
contract each plan's `<verify>` blocks must satisfy.

| Requirement | Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|
| EX-02 | `examples/before-after.md` carries all four frozen artifact-family headings | unit (new code `before-after-family-missing`) | `python3 tools/check_repo.py --self-test` | ❌ W0 | ⬜ pending |
| EX-02 | Every "after" cell cites at least one rule ID that exists in NUMBERING.md | unit (new code `before-after-citation-missing`) | `python3 tools/check_repo.py --self-test` | ❌ W0 | ⬜ pending |
| EX-02 | The before/after prose is genuinely illustrative, not a restatement of rule text | manual | UAT / conversational verification | N/A | ⬜ pending |
| DIST-01 | `npx skills add <owner>/<repo>` installs the skill in a real harness | manual | manual smoke test once the repo is public | N/A | ⬜ pending |
| DIST-02 | `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` are valid JSON with required keys | unit (new well-formedness check) | `python3 tools/check_repo.py --self-test` | ❌ W0 | ⬜ pending |
| DIST-02 | Plugin manifest `version` matches the skill frontmatter version NUMBERING.md already obligates | unit (new code `plugin-manifest-version-mismatch`) | `python3 tools/check_repo.py --self-test` | ❌ W0 | ⬜ pending |
| DIST-02 | `claude plugin marketplace add` / `install` actually works | manual | manual smoke test against the local working tree | N/A | ⬜ pending |
| DIST-03 | `output-styles/proof-first.md` exists with valid frontmatter and toggles via `/config` | unit (file/frontmatter half) + manual (session-behavior half) | `python3 tools/check_repo.py --self-test`; `/config` smoke test | ❌ W0 | ⬜ pending |
| DIST-04 | A pasted system prompt produces comparable behavior in a skill-less harness | manual only — explicitly unmeasured | UAT, disclosed as unmeasured | N/A | ⬜ pending |
| DIST-05 | Derivatives are regenerated from SKILL.md and staleness is mechanically detectable | unit (new code `skill-derivative-stale`) | `python3 tools/check_repo.py --self-test`; `python3 tools/generate_derivatives.py --check` | ❌ W0 | ⬜ pending |
| DIST-06 | README leads with before/after pairs and states an install path per harness | manual (prose/ordering) + existing regression gate | UAT; `readme-results-pointer-missing` must keep passing | ✅ existing | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

These files and codes do not exist yet; the first wave must create them before any
later wave can verify against them.

- [ ] `.claude-plugin/plugin.json` — does not exist
- [ ] `.claude-plugin/marketplace.json` — does not exist
- [ ] `output-styles/proof-first.md` — does not exist
- [ ] `prompts/system-prompt.md` — does not exist
- [ ] `tools/generate_derivatives.py` — does not exist
- [ ] `examples/before-after.md` — does not exist
- [ ] New `check_repo.py` codes plus their self-test fixtures and mutation entries:
      `plugin-manifest-version-mismatch`, `skill-derivative-stale`,
      `before-after-family-missing`, `before-after-citation-missing`
- [ ] README's before/after and Install sections (the existing Status and measured-figure
      sections must be preserved, not overwritten)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|---|---|---|---|
| Skills-CLI install actually resolves and installs | DIST-01 | Needs a published public GitHub repo; no git remote is configured in this working tree | Once published: `npx skills add <owner>/<repo>` in a clean directory, confirm the skill appears in the harness's skill list |
| Plugin marketplace add/install flow | DIST-02 | Requires a live Claude Code session and a reachable marketplace source | `claude plugin marketplace add ./` against the local tree, then `claude plugin install proof-first@<marketplace>` |
| Output style changes session behavior | DIST-03 | Model/UI behavior; no file-reading checker can observe a future session | Select the style in `/config`, then ask for a paragraph of presales prose and confirm the discipline is applied |
| Pasted system prompt gives comparable behavior | DIST-04 | Model behavior across harnesses; asserting equivalence as fact is forbidden until Phase 5's benchmark runs | Paste `prompts/system-prompt.md` into a skill-less harness, run one fixture from `evals/conformance/fixtures/`, compare qualitatively and record as unmeasured |
| Before/after prose is illustrative, not restatement | EX-02 | Content quality is a semantic judgment | Read each pair; the "after" must show the rewrite, not repeat the rule's wording |
| README ordering and claim discipline | DIST-06 | Prose ordering and the absence of unmeasured claims | Read top-to-bottom; confirm before/after pairs precede install instructions and that no performance figure appears |

---

## Known Nyquist Ceiling

The model-behavior half of DIST-03 and DIST-04 will remain
`nyquist_compliant: false` at the end of this phase, exactly as the equivalent
content-quality findings did in Phases 2 and 3. No file-reading checker can observe
how a live session behaves, and this project's evidence discipline forbids asserting
"equivalent behavior" as a measured fact before Phase 5's benchmark exists. This is a
disclosed ceiling, not a gap to be closed inside Phase 4 — the plans' Definition of
Done must state it rather than quietly claim coverage.

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or a Wave 0 dependency
- [ ] Sampling continuity: no 3 consecutive tasks without an automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] Discrimination-proven code count ≥ 32 and rising; CONTROL still 0 unexpected
- [ ] `nyquist_compliant: true` set in frontmatter — **not expected this phase**; see Known Nyquist Ceiling

**Approval:** pending
