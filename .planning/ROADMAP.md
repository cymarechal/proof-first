# Roadmap: Proof First

## Overview

Proof First ships as one dependency-free skill folder plus a reproducible eval harness proving it works. The build starts by freezing the two decisions everything else depends on — the disjoint `PF-`/`MC-` rule-numbering namespaces and the single shared cloud-migration deal brief — alongside the legal scaffolding for three trademarked frameworks. It then authors the rule catalog itself: the persuasion-preserving Command of the Message spine, the deletion test, the integrity section, and the basic draft/check modes, all in one self-contained SKILL.md. The MEDDICC completeness audit and the four artifact-family patterns follow in their own namespace and files, never blended into the prose rules — and it's only once they exist that check mode's three-category reporting, artifact classification, and citation guarantee become real. With the core content frozen, the project fans out into two parallel tracks: multi-channel distribution (plugin, output style, system prompt, README) with worked before/after examples, and a stdlib-only evaluation harness that benchmarks skill-on against skill-off across multiple models with a blind, persuasion-aware judge. The roadmap closes with a dedicated legal review gate — the MEDDIC trademark family carries unresolved litigation risk — and finalized README badges sourced only from the benchmark the prior phase actually ran.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundations — Legal Scaffolding, Numbering, Shared Deal** - Freeze the rule-numbering namespaces, the shared deal brief, and the license/trademark scaffolding before any rule content is drafted. (completed 2026-09-10)
- [x] **Phase 2: Rule Catalog & Integrity — SKILL.md Core** - Author SKILL.md's self-contained rule catalog, integrity section, and basic draft/check modes. (completed 2026-09-20 — closed by explicit project-owner override over CAT-10's disclosed, still-open over-fire residual; see 02-VERIFICATION.md `completion_override`)
- [x] **Phase 3: Completeness Audit & Artifact Patterns** - Add the MEDDICC completeness audit and the four artifact-family patterns, and wire the classification and citation guarantees that depend on them. (completed 2026-09-17)
- [ ] **Phase 4: Distribution & Worked Examples** - Ship the skill through every promised channel with before/after examples citing real rule numbers.
- [x] **Phase 5: Evaluation Harness** - Prove the skill works with a reproducible, multi-model, persuasion-aware benchmark. (completed 2026-09-20)
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

**Plans**: 11/11 plans executed — 6/6 original, plus 5 gap-closure plans added after verification found gaps

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

**Gap closure Wave 3** *(from 02-UAT.md test 2 / gap G-02-2; run with `/gsd-execute-phase 2 --gaps-only`)*

- [x] 02-10-PLAN.md — CAT-10 paired n=5 experiment under a pre-committed six-branch decision rule: the exclusion-clause lever eliminated every over-fire (0/25) but regressed a must-fire row 5/5 → 0/5, selecting Branch 4 — treatment tested live, then reverted; WINDOWS id 24 stays open with measured counts

**Gap closure Wave 4** *(from 02-UAT.md test 4 / gap G-02-4; run with `/gsd-execute-phase 2 --gaps-only`)*

- [x] 02-11-PLAN.md — 02-REVIEW.md CR-01: scope the binding search to `## Scope` and make an absent binding halt, so the trigger instrument's scope-hash guard fails closed instead of open; five self-test cases proven red-then-green by mutation probe

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

**Plans**: 16/16 plans executed (4 original, 1 gap-closure plan added after UAT found gaps, 3 gap-closure plans added after re-verification returned `gaps_found`, 4 gap-closure plans added after the third re-verification returned `gaps_found` with two Critical code-review findings, 3 gap-closure plans added after the fourth re-verification returned `gaps_found` with one Critical and two Warning code-review findings, 1 gap-closure plan added after the fifth re-verification returned `gaps_found` with one Critical verification-integrity defect in the round's own added code)

Plans:

- [x] 03-05-PLAN.md

**Wave 1**

- [x] 03-01-PLAN.md — Tracer: MC-1 end-to-end in a new `references/completeness-audit.md`, registered in NUMBERING.md, indexed in a new `## MC rules` checklist section and pointed at from SKILL.md, with `mc-catalog-id-drift` and `mc-rule-in-skill` proven live; freezes the eight-ID MC map, the four check-mode report sections and their order, and the four artifact-family headings behind a blocking decision checkpoint

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 03-02-PLAN.md — The remaining seven MC dimensions, eight keyed worked pairs in `worked-examples.md`, the standalone-audit section answering AUD-03, and the MC stated-count guard proven live as two more codes

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 03-03-PLAN.md — `references/artifact-patterns.md`: the classification procedure and its no-family fallback, all four artifact families with their conventions and their own expected order, and `artifact-family-section-missing` proven live

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 03-04-PLAN.md — SKILL.md's token budget bought back by trimming restatement, then spent on the check-mode classification line, the third and fourth report sections, the standalone-audit instruction and the second reference pointer; README, the WINDOWS ledger entry routing the MC ordering tension to LEG-04, and the provisional requirement marks

**Wave 5** *(gap closure after `03-VERIFICATION.md` returned `gaps_found`; run with `/gsd-execute-phase 03 --gaps-only`)*

- [x] 03-06-PLAN.md — Tracer: `evals/conformance/` — a stdlib runner that turns `03-UAT.md`'s ad-hoc live-harness recipe into one committed command, five committed fixtures, an offline scorer self-test wired into CI, and one real `claude -p` session driven end to end to prove the instrument before anything is measured with it

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 03-07-PLAN.md — The three content levers: SKILL.md's artifact-family line promoted to an always-printed five-value element with a delivery gate in the self-check (GAP A / WINDOWS 8), the last source-coined dimension label removed from `artifact-patterns.md` (GAP B / WINDOWS 9), `completeness-audit.md`'s standalone-audit shape statement aligned with the AUD-03 criterion (GAP C / WINDOWS 7), and two new violation codes raising the discrimination-proven count from 27 to 29

**Wave 7** *(blocked on Wave 6 completion)*

- [x] 03-08-PLAN.md — The measurement that decides MOD-04: at least 16 scoreable live write-mode sessions across two models and five fixtures against the edited skill, then a disposition applied to WINDOWS entry 8, REQUIREMENTS.md and 03-UAT.md under a decision rule committed before the number is known

**Wave 8** *(gap closure after the third `03-VERIFICATION.md` returned `gaps_found`; run with `/gsd-execute-phase 03 --gaps-only`)*

- [x] 03-09-PLAN.md — Tracer: CR-01, anchor `score_transcript()`'s family search to the prefix window where SKILL.md's write-mode contract places the family line, proven in both directions by two new committed transcript fixtures, plus a standing disclosure that every pre-fix figure is an unrecoverable optimistic ceiling — the hard upstream gate on any MOD-04 remeasurement
- [x] 03-10-PLAN.md — Tracer: CR-02, `readme-results-pointer-missing` (29 → 30 codes) so a README that stops pointing at the committed measurement fails the repo's own gate, then the Status section, layout tree and inventory made true about `evals/conformance/`

**Wave 9** *(blocked on Wave 8 completion)*

- [x] 03-11-PLAN.md — The third MOD-04 lever, different in kind from the two already measured: the self-check's first pass extended from a family-line presence gate to a post-generation ordering re-scan with a stated repair, paid for out of four named restatement clauses to hold 100 tokens of budget headroom, anchored by `skill-family-order-gate-missing` (30 → 31 codes)

**Wave 10** *(blocked on Wave 9 completion)*

- [x] 03-12-PLAN.md — The anchored remeasurement that decides MOD-04: a disposition rule committed to git before any session runs, then two paired sonnet-5 arms (post-`03-11` and a git-materialised pre-`03-11` baseline) at one durable invocation per session, then the branch applied mechanically to WINDOWS entry 8, REQUIREMENTS.md and 03-UAT.md

**Wave 11** *(gap closure after the fourth `03-VERIFICATION.md` returned `gaps_found`; run with `/gsd-execute-phase 03 --gaps-only`)*

- [x] 03-13-PLAN.md — Tracer: the Critical instrument defect, `run_conformance.py`'s whole-run in-memory batching replaced by a per-session write-and-flush through an extracted `run_matrix()`, proven offline by a self-test case that interrupts a matrix part-way through and finds the earlier lines already on disk, plus the Arm A no-family enumeration corrected against the run blocks it claims to be re-derivable from

**Wave 12** *(blocked on Wave 11 completion)*

- [x] 03-14-PLAN.md — Tracer: `results-breakdown-count-mismatch` (31 → 32 codes), the guard that fails the build when a verdict breakdown's stated count disagrees with its own enumeration, discrimination-proven against the real results file by adding `evals` to `MUTATION_SOURCES`; plus the two review consistency findings — the family-line gate made case-insensitive like its sibling, and the stale `skill-token-budget-exceeded` docstring claim corrected

**Wave 13** *(blocked on Wave 12 completion)*

- [x] 03-15-PLAN.md — MOD-04's v1 disposition made an explicit, dated, attributed decision rather than a branch table's arithmetic: route (b) recommended (accept the measured residual, route (a)'s post-generation-repair candidate being architecturally unavailable to an Agent Skill), then the decision and the measured 30.0%/40.0% figures published through RESULTS-mod04.md, WINDOWS entry 8, README, REQUIREMENTS.md and 03-UAT.md

**Wave 14** *(gap closure after the fifth `03-VERIFICATION.md` returned `gaps_found`; run with `/gsd-execute-phase 03 --gaps-only`)*

- [x] 03-16-PLAN.md — Tracer: the verification-integrity defect in this phase's own regression guard — self-test behavior case 11 rewritten to assert write-then-flush call pairing through a `_FlushTrackingHandle` proxy and a pre-close read of the results file, so deleting `_write_result_line()`'s flush call makes CI red instead of green, proven in both directions by a one-time mutation probe; then the two documents that overclaimed what case 11 proved corrected with their provenance recorded, plus the checker's self-contradictory `evals/` comment, README's unnamed decline, and a WINDOWS ledger entry so the defect is tracked rather than untracked

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

**Plans**: 11/11 plans executed, plus 6 gap-closure plans (04-05 .. 04-10) planned from 04-UAT.md's seven gaps, plus 1 gap-closure plan (04-11) planned from 04-VERIFICATION.md's single remaining gap, plus 2 gap-closure plans (04-12, 04-13) planned from 04-UAT.md's two remaining major gaps, plus 1 gap-closure plan (04-14) planned from 04-UAT.md's round-2 re-read, which closed both of those and opened one new major gap, plus 1 plan (04-15) planned 2026-09-21 once Phase 5's completion unblocked 04-UAT.md test 2 — the one roadmap success criterion (#3) never measured

Plans:
**Wave 1**

- [x] 04-01-PLAN.md — Tracer: the Claude Code plugin channel end to end — `.claude-plugin/plugin.json` and `marketplace.json` bound to `SKILL.md`'s frontmatter version, with `plugin-manifest-invalid`, `plugin-manifest-version-mismatch` and `publish-location-drift` proven live (32 → 35 codes); freezes the plugin identifier, the `source: "./"` rooting and the publish-location placeholder behind a blocking decision checkpoint

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 04-02-PLAN.md — `examples/before-after.md`: one document-level before/after pair per artifact family in the frozen order, every after column citing a shipped rule ID, with `before-after-family-missing` and `before-after-citation-missing` proven live (35 → 37)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 04-03-PLAN.md — `tools/generate_derivatives.py` and the two generated, hash-stamped derivatives (`output-styles/proof-first.md`, `prompts/system-prompt.md`), guarded from two directions by `skill-derivative-stale` and the generator's own `--check` mode in CI, plus `derivative-rule-coverage-incomplete` proving all 39 rule headings and four family headings reach each artifact (37 → 39)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 04-04-PLAN.md — README rewritten to lead with a before/after pair and state all four install routes, with the derivative re-sync step documented and the existing measured-figure disclosure preserved; `readme-install-path-missing` and `readme-before-after-order` proven live (39 → 41)

**Gap closure** *(04-UAT.md status `gaps_found`; run with `/gsd-execute-phase 4 --gaps-only`; wave numbers below are internal to this set)*

**Gap wave 1** *(parallel: disjoint files)*

- [x] 04-05-PLAN.md — `examples/before-after.md` prose repair: rule narration out of all four ✓ columns, every ✓ sentence under PF-4.1's 25-word ceiling, the PF-1.9 inversion recast capability-first, both invented counts dropped, the PF-3.3 marker re-attached to a term, and README's reproduced pair kept identical (G-04-1..G-04-5; 41 codes, unchanged)
- [x] 04-06-PLAN.md — `skills/proof-first/references/worked-examples.md` PF-4.1 repair: 8 of 31 ✓ sentences over the ceiling, maximum 37 words, measured during gap planning rather than listed in the UAT; repaired so the sentence-length code can scan both example files honestly (41 codes, unchanged)

**Gap wave 2** *(blocked on gap wave 1)*

- [x] 04-07-PLAN.md — three example-prose violation codes with firing fixtures, silent fixtures and registered mutations: `example-sentence-length`, `before-after-spelled-count`, `example-rule-narration` (G-04-2, G-04-4, G-04-1; 41 → 44)

**Gap wave 3** *(blocked on gap wave 2)*

- [x] 04-08-PLAN.md — README prose repair: lead with the example inside the first screen, state each install route's runnability, move maintainer instruction below Status, narrow the over-broad catalog claim and the model-count caveat, and make the layout legend agree with the tree (G-04-6; 44 codes, unchanged)

**Gap wave 4** *(blocked on gap wave 3)*

- [x] 04-09-PLAN.md — three README violation codes: `readme-example-drift`, `readme-example-lead-distance`, `readme-layout-legend-drift` (G-04-6 mechanised; 44 → 47)

**Gap wave 5** *(blocked on gap wave 4)*

- [x] 04-10-PLAN.md — `04-REVIEW.md`'s three deferred warnings: `_owner_segment` normalised across four GitHub URL forms, `generate_derivatives.py --check` made genuinely byte-comparing with a platform-pinned writer, and both plugin-manifest checks' one-skill assumption disclosed and enforced (G-04-7; 47 codes, unchanged)

**Gap closure, round 2** *(04-VERIFICATION.md status `gaps_found`, one gap; run with `/gsd-execute-phase 4 --gaps-only`)*

- [x] 04-11-PLAN.md — CR-01: `check_plugin_manifest_invalid` enforces `PLUGIN_REQUIRED_KEYS` on `marketplace.json`'s `plugins[0]` entry, proven red-then-green by a second real-file mutation and exhaustively by a nine-key-by-two-position `--self-test` matrix that closes the class rather than the instance; plus the three review fold-ins — duplicated-field equality between the two manifests, MC-31's colon repair inside PF-4.1's ceiling, and the ambiguous spelled-count measurement disambiguated (DIST-02; 47 codes, unchanged)

**Gap closure, round 3** *(04-UAT.md status `diagnosed`, two major gaps; run with `/gsd-execute-phase 4 --gaps-only`)*

**Gap wave 1**

- [x] 04-12-PLAN.md — `examples/before-after.md` factual repair: AWS Control Tower's governance re-scoped from the pre-migration VMware/Oracle estate to the new account structure, agreeing with `deal-brief.md:22`, `worked-examples.md:32` and sentence 1 of its own column, with PF-1.9's capability-first shape and PF-4.1's 25-word ceiling both held; plus Marcus Feld's one recorded utterance quoted once instead of twice and the PF-2.14 marker made actionable (G-04-3; 47 codes, unchanged)

**Gap wave 2** *(blocked on gap wave 1: the new code leaves the repository-wide gate deliberately red between registration and repair)*

- [x] 04-13-PLAN.md — README install truth: route 3's missing copy step and its destination directory stated, the today-runnable claim rewritten to match, and `readme-output-style-destination-missing` registered — a deliberately narrow code proven red on the shipped README and green after, whose declared ceiling refuses the executability claim no code here can make; plus four folded-in credibility defects and one tracked unrun verification (G-04-4; 47 → 48)

**Gap closure, round 4** *(04-UAT.md status `diagnosed`, one major gap opened by round 3's own repair; run with `/gsd-execute-phase 4 --gaps-only`)*

- [x] 04-14-PLAN.md — README self-contradiction: the false universal negative written by 04-13's own fix narrowed to the interactive case it actually describes, the verbatim copy in WINDOWS entry 16 corrected with it, and the mechanisability question answered with a recorded refusal rather than a 49th code — cross-sentence semantic contradiction is not regex-checkable and a code claiming it would be the CR-01 overstatement a third time; plus three folded-in README credibility defects and one unevidenced deliverable claim in the flagship example (G-04-8; 48 codes, unchanged)

**Gap closure, round 5** *(04-UAT.md test 2 unblocked: the Phase 5 dependency it was deferred on is complete; run with `/gsd-execute-phase 4 --gaps-only`)*

- [ ] 04-15-PLAN.md — Route equivalence, measured rather than asserted: `evals/routes/run_routes.py` drives three arms (`skill-on`, `style-on`, `prompt-on`) over the eight committed benchmark scenarios on byte-identical prompts, scores each session with `evals/lint.py`'s `lint()` and `evals/conformance/run_conformance.py`'s `score_transcript()`, and publishes `evals/routes/RESULTS-routes.md` from committed records only; an activation probe against an unrouted control proves each arm is switched on before any matrix spend, and any arm that cannot be proven on is dropped and refused in writing rather than run anyway; then the generated derivative preamble's "No benchmark has compared" claim, the README's route 3/4 paragraphs, COVERAGE.md and the ledger are made true, with a 49th code holding the preamble claim to the results file (G-04-9; DIST-03, DIST-04, DIST-05; 48 -> 49 codes, or 48 with a recorded refusal). Not autonomous: Task 3 is a blocking spend checkpoint (~$10, ~30 min).

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

**Plans**: 3/3 plans executed in 3 sequential waves. The split follows `05-RESEARCH.md`'s recommendation and isolates the one paid, non-reversible step: plans 1 and 2 are entirely offline and free, so a plan-review cycle on either re-triggers no live call; plan 3 owns the judge and the live matrix behind a blocking decision checkpoint. The waves are strictly sequential because the plans share files — 1 and 2 both touch `.github/workflows/ci.yml`, and 2 and 3 both touch `evals/benchmark/run_benchmark.py`.

Plans:
**Wave 1**

- [x] 05-01-PLAN.md — Tracer: one proxy term end to end — `evals/proxy-sources.md` as the external-provenance registry, `evals/lint.py` counting it, `proxy-term-unsourced` making the registry load-bearing, the EVAL-03 disclaimer, and the self-test wired into CI; then the four remaining proxy codes and the provenance allow-list, eight codes each proven in both directions by its own fixture pair (EVAL-01, EVAL-02, EVAL-03)

**Wave 2** *(blocked on Wave 1: shares `.github/workflows/ci.yml`, and imports the linter)*

- [x] 05-02-PLAN.md — The whole free half of the benchmark: a fresh fictional deal sharing no entity with `examples/deal-brief.md`, eight scenarios across the four artifact families, the generation runner with isolated per-session temp dirs and `unscoreable` failure handling, and the offline aggregator and report renderer — every call faked, no `RESULTS.md` committed, and the report path proven never to shell out (EVAL-04, EVAL-05, EVAL-09, EVAL-10, EVAL-11, EVAL-12)

**Wave 3** *(blocked on Wave 2: extends `run_benchmark.py`; not autonomous — carries the spend checkpoint)*

- [x] 05-03-PLAN.md — The blind pairwise judge built and proven offline (labels stripped, both orders averaged, ties kept as ties, schema-invalid replies recorded `unscoreable`), then a blocking decision checkpoint authorising ≈$48 and ≈58 minutes of live calls, then one matrix run, 192 committed raw records, and a `RESULTS.md` whose every figure survives a re-render diff (EVAL-06, EVAL-07, EVAL-08)

### Phase 6: Legal Review Gate & Launch

**Goal**: The repo is legally cleared and honestly marketed before anyone outside the project sees it.
**Depends on**: Phase 4, Phase 5
**Requirements**: LEG-04, LEG-05
**Success Criteria** (what must be TRUE):

  1. A legal review gate passes before public launch, with MEDDIC-family trademark status (including the MEDDPICC genericness ruling) reconfirmed against current sources.
  2. Every claim and badge in README derives only from committed benchmark results in RESULTS.md, stating model versions and date.

**Plans**:

- [x] 06-01-PLAN.md
- [x] 06-02-PLAN.md
- [x] 06-03-PLAN.md
- [x] 06-04-PLAN.md

**Wave 1**

- [x] 06-01 — Tracer: one source row confirmed against a live page, recorded with provenance, and `source-row-unconfirmed` enforcing it

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 06-02 — The legal review gate: five remaining source rows, three rights-holders reconfirmed, `LEGAL-REVIEW.md`, and two more codes

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 06-03 — README states what the benchmark supports: pooled totals rendered, a delimited claim region, four codes

**Wave 4** *(blocked on Wave 3 completion)*

- [ ] 06-04 — Launch gate: the publish decision, the install observations, the human reads, the ledger sweep

Cross-cutting constraints:

- No check this phase adds may make a network call, and no command may be added to `.github/workflows/ci.yml` that does. Lookups happen once at execution time; the committed record is what CI reads.
- Every violation code this phase registers carries a `MUTATIONS` entry in the same commit and is reported discrimination-proven, never merely registered.
- No claim may outrun the evidence — the seven overclaims named in `06-RESEARCH.md` § Decision 6 are prohibited across all four plans.

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 (4 and 5 have no dependency on each other and may run in parallel)

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundations — Legal Scaffolding, Numbering, Shared Deal | 7/7 | Complete    | 2026-09-10 |
| 2. Rule Catalog & Integrity — SKILL.md Core | 10/10 | In Progress|  |
| 3. Completeness Audit & Artifact Patterns | 16/16 | Complete    | 2026-09-17 |
| 4. Distribution & Worked Examples | 11/11 | In Progress|  |
| 5. Evaluation Harness | 3/3 | Complete    | 2026-09-20 |
| 6. Legal Review Gate & Launch | 4/4 | In Progress|  |

---
*Roadmap created: 2026-09-10*
*Granularity: standard (6 phases)*
