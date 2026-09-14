# Roadmap: Proof First

## Overview

Proof First ships as one dependency-free skill folder plus a reproducible eval harness proving it works. The build starts by freezing the two decisions everything else depends on — the disjoint `PF-`/`MC-` rule-numbering namespaces and the single shared cloud-migration deal brief — alongside the legal scaffolding for three trademarked frameworks. It then authors the rule catalog itself: the persuasion-preserving Command of the Message spine, the deletion test, the integrity section, and the basic draft/check modes, all in one self-contained SKILL.md. The MEDDICC completeness audit and the four artifact-family patterns follow in their own namespace and files, never blended into the prose rules — and it's only once they exist that check mode's three-category reporting, artifact classification, and citation guarantee become real. With the core content frozen, the project fans out into two parallel tracks: multi-channel distribution (plugin, output style, system prompt, README) with worked before/after examples, and a stdlib-only evaluation harness that benchmarks skill-on against skill-off across multiple models with a blind, persuasion-aware judge. The roadmap closes with a dedicated legal review gate — the MEDDIC trademark family carries unresolved litigation risk — and finalized README badges sourced only from the benchmark the prior phase actually ran.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundations — Legal Scaffolding, Numbering, Shared Deal** - Freeze the rule-numbering namespaces, the shared deal brief, and the license/trademark scaffolding before any rule content is drafted. (completed 2026-09-10)
- [ ] **Phase 2: Rule Catalog & Integrity — SKILL.md Core** - Author SKILL.md's self-contained rule catalog, integrity section, and basic draft/check modes.
- [ ] **Phase 3: Completeness Audit & Artifact Patterns** - Add the MEDDICC completeness audit and the four artifact-family patterns, and wire the classification and citation guarantees that depend on them.
- [ ] **Phase 4: Distribution & Worked Examples** - Ship the skill through every promised channel with before/after examples citing real rule numbers.
- [ ] **Phase 5: Evaluation Harness** - Prove the skill works with a reproducible, multi-model, persuasion-aware benchmark.
- [ ] **Phase 6: Legal Review Gate & Launch** - Clear trademark risk and publish a README whose claims are sourced only from the benchmark that actually ran.

## Phase Details

### Phase 1: Foundations — Legal Scaffolding, Numbering, Shared Deal

**Goal**: The project's foundational scaffolding — rule numbering, shared example data, and legal posture — is frozen before any rule content is drafted, so nothing downstream forces a renumbering or a retrofit.
**Depends on**: Nothing (first phase)
**Requirements**: CAT-07, EX-01, LEG-01, LEG-02, LEG-03
**Success Criteria** (what must be TRUE):

  1. A contributor drafting a new rule can look up the next free ID in either the `PF-<section>.<n>` or `MC-<n>` namespace without guessing, because ranges are reserved per section before drafting starts.
  2. Every worked example anywhere in the repo can cite facts (dollar figures, roles, timeline, competitors) from one canonical fictional cloud-migration deal brief.
  3. The repo's LICENSE and NOTICES.md individually name all three frameworks (Command of the Message, MEDDICC, Challenger) with non-affiliation and trademark language, before any framework-derived content ships.
  4. Nothing in the repo reproduces proprietary framework text — framework concepts are paraphrased and sources are cited wherever they appear.

**Plans**: 7/7 plans executed (4 executed, 3 gap-closure plans pending)

Plans:
**Wave 1**

- [x] 01-01-PLAN.md — Tracer: freeze all three registry formats and prove them end-to-end with a stdlib-only checker in CI (NUMBERING.md, tools/check_repo.py, .github/workflows/ci.yml, plus the Canonical figures table and the attribution pointer block)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 01-02-PLAN.md — Fill examples/deal-brief.md with the one canonical fictional deal, its customer source material, and the facts that are awkward for the vendor
- [x] 01-03-PLAN.md — Legal posture: MIT LICENSE, three individually named framework statements in NOTICES.md, and the approved-source list plus reproduction boundary in SOURCES.md

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 01-04-PLAN.md — Claim-free README documenting the target layout, plus the full-repository integrity sweep and phase-closing legal read

**Gap closure** *(from 01-VERIFICATION.md and 01-REVIEW.md; run with `/gsd-execute-phase 1 --gaps-only`)*

- [x] 01-05-PLAN.md — BLOCKER: parse the real NOTICES.md shape, fail loud on an unusable pointer definition, and prove `pointer-missing` fires against the shipped README.md (wave 1)
- [x] 01-06-PLAN.md — WARNINGs: bound the Canonical figures exemption to the table, enforce MC reserved blocks per dimension, and declare the checker's real ceilings (wave 2)
- [x] 01-07-PLAN.md — Add a `--mutation-test` mode proving every check fires against mutated production content, and wire it into CI (wave 3)

### Phase 2: Rule Catalog & Integrity — SKILL.md Core

**Goal**: A writer can open SKILL.md and draft or spot-check presales prose against a persuasion-preserving, self-contained rule catalog that never lets a fabricated claim through.
**Depends on**: Phase 1
**Requirements**: CAT-01, CAT-02, CAT-03, CAT-04, CAT-05, CAT-06, CAT-08, CAT-09, CAT-10, INT-01, INT-02, INT-03, INT-04, INT-05, INT-06, MOD-01, MOD-02
**Success Criteria** (what must be TRUE):

  1. Writer can read one numbered rule catalog organized by Command of the Message elements, fully self-contained under the progressive-disclosure ceiling, with valid frontmatter and a reliably triggering description.
  2. Writer asking the skill to draft gets output where every deleted buzzword is replaced by an instruction to attach specific evidence in its place, not just silence — and a term appearing verbatim in the customer's own source material is marked, not deleted.
  3. Writer gets exactly one opening instruction — a single reframe-the-problem rule resolved from the three overlapping source frameworks, not three conflicting ones to reconcile.
  4. Writer asking the skill to check text gets each prose violation back labeled with a rule number, the offending text, and a compliant rewrite.
  5. Skill refuses to invent metrics, reference customers, benchmark numbers, or certifications, and instead flags commitment-shaped language, undisclosed customer references, competitor comparisons, and unverified compliance/export claims for a human to resolve.

**Plans**: 9/9 plans executed — 6/6 original, plus 3 gap-closure plans added after verification found gaps

Plans:
**Wave 1**

- [x] 02-01-PLAN.md — Tracer: three rules (PF-0.1, PF-2.11, PF-3.1) end-to-end in a real skill folder, registered in NUMBERING.md and indexed in checklist.md, with `catalog-id-drift` proven live and the mutation control copy widened to include `skills/`

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 02-02-PLAN.md — PF-1: the Command of the Message spine, nine rules across the seven frozen sub-blocks, plus the mid-draft line-count checkpoint

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 02-03-PLAN.md — PF-2: four Proof rules and seven Integrity rules, with each of the four presales hazards as its own numbered, citable rule

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 02-04-PLAN.md — PF-3.2/PF-3.3 and the deletion-test reference table's four documented classes, PF-4's self-contained prose mechanics, PF-5's protective rules, and the final line measurement

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 02-05-PLAN.md — Write mode, check mode, the two-pass self-check, the register and Limits sections, the recorded trigger pressure-test, and the README layout correction

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 02-06-PLAN.md — Enforcement: four frontmatter codes, the stated-count and line-ceiling codes, PF sub-block containment, and twenty violation codes proven live

**Gap closure Wave 1** *(from 02-VERIFICATION.md; run with `/gsd-execute-phase 2 --gaps-only`)*

- [x] 02-07-PLAN.md — CAT-08's token ceiling met by moving the 20 worked ✗/✓ pairs into `references/` and tightening prose, leaving every rule, every constructive half and every enforcement path intact; closes the red CI step by construction

**Gap closure Wave 2** *(blocked on gap closure Wave 1)*

- [x] 02-08-PLAN.md — `--mutation-test` asserts discrimination instead of firing, reports any fire-only code separately, empties the stale known-open allowance, and corrects both overclaiming docstrings
- [x] 02-09-PLAN.md — README's Status prose reconciled with its own tree and the repository, the pending trigger observations made attributable, and WINDOWS ids 3 and 4 routed to human checks rather than machine-closed

### Phase 3: Completeness Audit & Artifact Patterns

**Goal**: A writer can classify a document by artifact family, apply that family's conventions, and get a document-level completeness verdict and trustworthy rule citations — independent of the prose rules.
**Depends on**: Phase 2
**Requirements**: AUD-01, AUD-02, AUD-03, ART-01, ART-02, ART-03, ART-04, MOD-03, MOD-04, MOD-05
**Success Criteria** (what must be TRUE):

  1. Writer can run a document-level completeness audit derived from MEDDICC — covering metric, economic buyer, decision criteria, decision process, paper process, pain, champion, and competition — and get a verdict in its own `MC-` namespace and reference file, never blended into the prose rules.
  2. Writer drafting an RFP/RFI response, a solution proposal, an executive summary, or demo/discovery material each gets that family's own conventions (answer-first ordering and criteria-mirroring; architecture narrative and risk treatment; problem-reframe-then-business-case; discovery-to-follow-up structure, respectively).
  3. Skill states which artifact family it classified the document as before applying any rules.
  4. Check mode reports prose violations, completeness gaps, and integrity flags as three separately labeled categories, plus a structural ordering pass.
  5. Check mode never cites a rule number that doesn't exist in the shipped catalog or checklist files.

**Plans**: 4 plans

Plans:
**Wave 1**

- [ ] 03-01-PLAN.md — Tracer: MC-1 end-to-end in a new `references/completeness-audit.md`, registered in NUMBERING.md, indexed in a new `## MC rules` checklist section and pointed at from SKILL.md, with `mc-catalog-id-drift` and `mc-rule-in-skill` proven live; freezes the eight-ID MC map, the four check-mode report sections and their order, and the four artifact-family headings behind a blocking decision checkpoint

**Wave 2** *(blocked on Wave 1 completion)*

- [ ] 03-02-PLAN.md — The remaining seven MC dimensions, eight keyed worked pairs in `worked-examples.md`, the standalone-audit section answering AUD-03, and the MC stated-count guard proven live as two more codes

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] 03-03-PLAN.md — `references/artifact-patterns.md`: the classification procedure and its no-family fallback, all four artifact families with their conventions and their own expected order, and `artifact-family-section-missing` proven live

**Wave 4** *(blocked on Wave 3 completion)*

- [ ] 03-04-PLAN.md — SKILL.md's token budget bought back by trimming restatement, then spent on the check-mode classification line, the third and fourth report sections, the standalone-audit instruction and the second reference pointer; README, the WINDOWS ledger entry routing the MC ordering tension to LEG-04, and the provisional requirement marks

### Phase 4: Distribution & Worked Examples

**Goal**: The finished rule catalog reaches a writer through every distribution channel the project promises, backed by real worked examples.
**Depends on**: Phase 2, Phase 3
**Requirements**: EX-02, DIST-01, DIST-02, DIST-03, DIST-04, DIST-05, DIST-06
**Success Criteria** (what must be TRUE):

  1. Reader sees before/after pairs covering each of the four artifact families, with the after column citing real, shipped rule numbers.
  2. User can install the skill via the skills CLI with one command, and separately as a Claude Code plugin from a marketplace manifest in this repo.
  3. User can turn the discipline on permanently as an output style, or paste a system-prompt version in a harness with no skill support, and get equivalent behavior either way.
  4. A documented re-sync step exists that regenerates the output style and system prompt whenever SKILL.md changes.
  5. Reader opens a README that leads with before/after pairs and states an install path for every supported harness.

**Plans**: TBD

### Phase 5: Evaluation Harness

**Goal**: Anyone can reproduce a credible, honestly-caveated measurement of the skill's effect using only committed scripts and data.
**Depends on**: Phase 2, Phase 3
**Requirements**: EVAL-01, EVAL-02, EVAL-03, EVAL-04, EVAL-05, EVAL-06, EVAL-07, EVAL-08, EVAL-09, EVAL-10, EVAL-11, EVAL-12
**Success Criteria** (what must be TRUE):

  1. A deterministic linter counts rule-proxy violations using only the Python standard library, passes its own self-test, and states plainly that the deletion test is a semantic judgment it cannot perform.
  2. The linter's buzzword proxy list is sourced independently of the skill's own worked examples, so a reviewer can confirm the measured improvement isn't circular.
  3. A committed scenario set drives generations across all four artifact families, run headlessly across multiple pinned Claude models, at least three times per cell.
  4. A blind pairwise judge scores skill-on against skill-off with labels stripped and both text orders run, scoring persuasive force as its own dimension so a flat-but-clean draft can't pass on clarity alone.
  5. Published results report mechanical-proxy counts and judged persuasion as two separately labeled figures with variance alongside the mean, name honest caveats (position bias, judge-family bias, baseline prompt parity, proxy provenance, sample size), and every raw generation and judgement is committed so any number can be recomputed with one documented command.

**Plans**: TBD — likely splits across the linter, the scenario/benchmark runner, and the judge; EVAL-06's mandatory 3x-per-cell repetition raises benchmark runtime meaningfully and may warrant its own plan separate from the linter.

### Phase 6: Legal Review Gate & Launch

**Goal**: The repo is legally cleared and honestly marketed before anyone outside the project sees it.
**Depends on**: Phase 4, Phase 5
**Requirements**: LEG-04, LEG-05
**Success Criteria** (what must be TRUE):

  1. A legal review gate passes before public launch, with MEDDIC-family trademark status (including the MEDDPICC genericness ruling) reconfirmed against current sources.
  2. Every claim and badge in README derives only from committed benchmark results in RESULTS.md, stating model versions and date.

**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 (4 and 5 have no dependency on each other and may run in parallel)

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundations — Legal Scaffolding, Numbering, Shared Deal | 7/7 | Complete    | 2026-09-10 |
| 2. Rule Catalog & Integrity — SKILL.md Core | 9/9 | In Progress|  |
| 3. Completeness Audit & Artifact Patterns | 0/TBD | Not started | - |
| 4. Distribution & Worked Examples | 0/TBD | Not started | - |
| 5. Evaluation Harness | 0/TBD | Not started | - |
| 6. Legal Review Gate & Launch | 0/TBD | Not started | - |

---
*Roadmap created: 2026-09-10*
*Granularity: standard (6 phases)*
