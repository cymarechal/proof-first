# Requirements: Proof First

**Defined:** 2026-09-10
**Core Value:** A technical evaluator finishes the document believing the author genuinely understands their problem — because complex things were made simple without being made wrong.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Rule Catalog

- [x] **CAT-01**: Writer gets a numbered rule catalog whose sections follow the Command of the Message elements (Before scenario, After scenario, Required Capabilities, Metrics, Proof Points, Differentiators, Positive Business Outcomes)
- [x] **CAT-02**: Every subtractive rule is paired with a constructive rule that names what evidence to attach in place of the deleted text
- [x] **CAT-03**: Writer gets exactly one opening rule, resolving the Before-scenario / Identify-Pain / Reframe convergence into a single instruction
- [x] **CAT-04**: Writer gets the deletion test as the buzzword rule, stated with evidence-attachment framing rather than deletion alone
- [x] **CAT-05**: The deletion test retains a term that appears verbatim in the customer's own source material and marks it, instead of deleting it
- [x] **CAT-06**: Writer gets a self-contained prose mechanics section (sentence length, active voice, modal discipline, one claim per sentence) with no dependency on another skill
- [x] **CAT-07**: Rules carry stable citable IDs in two disjoint namespaces — `PF-<section>.<n>` for prose rules and `MC-<n>` for the completeness audit — with numeric ranges reserved per section before drafting
- [x] **CAT-08**: SKILL.md stays under the progressive-disclosure ceiling (under 500 lines, approximately 5,000 tokens) with detail pushed into `references/`
- [x] **CAT-09**: SKILL.md frontmatter validates against the Agent Skills allow-list and loads without error in every target harness
- [ ] **CAT-10**: The `description` field triggers the skill reliably on presales writing requests, acting as an explicit trigger list

### Integrity

- [ ] **INT-01**: Skill refuses to invent metrics, reference customers, benchmark numbers, or certifications
- [ ] **INT-02**: Skill marks an evidence gap for a human to fill instead of filling it with plausible text
- [ ] **INT-03**: Skill flags commitment-shaped language that could become a contractual warranty
- [ ] **INT-04**: Skill flags customer reference details that need disclosure permission before use
- [ ] **INT-05**: Skill flags competitor comparisons that create legal exposure
- [ ] **INT-06**: Skill flags compliance, certification, and export claims for human verification

### Completeness Audit

- [ ] **AUD-01**: Writer gets a document-level completeness checklist derived from MEDDICC, covering metric, economic buyer, decision criteria, decision process, paper process, pain, champion, and competition as questions asked of a document
- [ ] **AUD-02**: The checklist lives in its own reference file and its own `MC-` namespace, never blended into the prose rules
- [ ] **AUD-03**: Writer can run the completeness audit independently of the prose rules and get a separate verdict

### Artifact Patterns

- [ ] **ART-01**: Writer gets an RFP/RFI response pattern covering answer-first ordering, compliance-versus-value separation, and mirroring the buyer's stated evaluation criteria
- [ ] **ART-02**: Writer gets a solution proposal pattern covering architecture narrative, required-capability mapping, and risk treatment
- [ ] **ART-03**: Writer gets an executive summary pattern that opens with the problem reframe and states the business case before the capability list
- [ ] **ART-04**: Writer gets a demo and discovery pattern covering discovery notes, demo scripts, POC success criteria, and follow-up

### Modes

- [ ] **MOD-01**: Writer can ask the skill to draft a presales document and get output that follows the catalog
- [ ] **MOD-02**: Writer can ask the skill to check existing text and get each violation as rule number, offending text, and a compliant rewrite
- [ ] **MOD-03**: Check mode reports prose violations, completeness gaps, and integrity flags as three separately labeled categories, plus a structural ordering pass
- [ ] **MOD-04**: Skill classifies the artifact family before applying rules, and says which one it chose
- [ ] **MOD-05**: Check mode cites only rule numbers that exist in the shipped files, and never invents one

### Examples

- [x] **EX-01**: A single fictional cloud migration deal brief supplies the canonical facts that every example in the repo reuses
- [ ] **EX-02**: Reader gets before/after pairs covering each artifact family, with the after column citing real rule numbers

### Distribution

- [ ] **DIST-01**: User can install via the skills CLI with one command
- [ ] **DIST-02**: User can install as a Claude Code plugin from a marketplace manifest in this repo
- [ ] **DIST-03**: User can turn the discipline on permanently as a Claude Code output style
- [ ] **DIST-04**: User with no skill support can paste a system prompt version and get the same behavior
- [ ] **DIST-05**: Derivative artifacts (output style, system prompt) are regenerated from SKILL.md whenever it changes, and a documented re-sync step exists
- [ ] **DIST-06**: Reader gets a README that leads with before/after pairs and states install paths for each harness

### Evaluation

- [ ] **EVAL-01**: A deterministic linter counts rule-proxy violations using only the Python standard library, and passes its own self-test
- [ ] **EVAL-02**: The linter's buzzword proxy list is sourced independently of the skill's own worked examples, so measured improvement is not circular
- [ ] **EVAL-03**: The linter states plainly that the deletion test is a semantic judgment it cannot perform, and that its numbers are not a compliance verdict
- [ ] **EVAL-04**: A committed scenario set drives generations across all four artifact families
- [ ] **EVAL-05**: A benchmark runner drives multiple Claude models headlessly with the model string and reasoning effort pinned and recorded per result
- [ ] **EVAL-06**: Each benchmark cell runs at least three times, and published results report variance alongside the mean
- [ ] **EVAL-07**: A blind pairwise judge scores skill-on against skill-off with labels stripped and both text orders run
- [ ] **EVAL-08**: The judge rubric scores persuasive force as its own dimension, so a flat but clean draft cannot pass on clarity alone
- [ ] **EVAL-09**: Published results report mechanical-proxy counts and judged persuasion as two separately labeled figures, never blended into one number
- [ ] **EVAL-10**: RESULTS.md carries an honest-caveats section naming position bias, judge family bias, baseline prompt parity, proxy provenance, and sample size
- [ ] **EVAL-11**: Every raw generation and judgement is committed as JSON so any published number can be recomputed from the repo
- [ ] **EVAL-12**: A reader can reproduce the benchmark with one documented command

### Legal

- [x] **LEG-01**: The repo ships an MIT license covering all original content
- [x] **LEG-02**: NOTICES.md carries a separate, individually named non-affiliation and trademark statement for each of the three frameworks
- [x] **LEG-03**: The repo reproduces zero proprietary framework text — concepts are paraphrased and sources are cited
- [ ] **LEG-04**: A legal review gate passes before public launch, with the MEDDIC-family trademark status reconfirmed against current sources
- [ ] **LEG-05**: README claims and badges derive only from committed benchmark results, with the model versions and date stated

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Cross-Provider Validation

- **XPRV-01**: Benchmark runs against non-Claude models so the claim is demonstrably a property of the skill, not of one model family
- **XPRV-02**: Published cross-provider results table with its own method and caveats

### Additional Artifacts

- **ART2-01**: Statement of work narrative sections
- **ART2-02**: Security and compliance questionnaires
- **ART2-03**: Bid/no-bid qualification memos

### Reach

- **REACH-01**: Non-English rule catalogs for localized bid teams
- **REACH-02**: Optional readability metric (for example `textstat`) reported alongside the proxy counts

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Slide decks and visual design | This is a text skill; deck structure is a different problem needing different tooling |
| Pricing calculation, sizing, commercial modelling | The skill writes about numbers, it does not produce them |
| CRM or bid-management integration | One folder, no dependencies — the distribution model that makes the sibling skill adoptable |
| Reproducing proprietary framework material | Legal exposure, and paraphrase is sufficient to teach the mechanics |
| Fact-checking the writer's inputs | The skill refuses to invent facts and marks gaps, but cannot verify what it is given |
| Marketing copy, brand writing, launch posts | The same boundary SimpleEnglish draws, drawn from the other side |
| Challenger "Tailor" and "Take Control" stages | Conversational, not written. Only the opening reframe is in scope; the rest would need full re-scoping |
| spaCy or other NLP dependency in the linter | Breaks the zero-dependency posture for marginal precision on a problem no NLP library solves |
| Strictness modes | Considered and rejected — there is no legitimately relaxable version of a binary requirement like anti-fabrication |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| CAT-01 | Phase 2 | Complete |
| CAT-02 | Phase 2 | Complete |
| CAT-03 | Phase 2 | Complete |
| CAT-04 | Phase 2 | Complete |
| CAT-05 | Phase 2 | Complete |
| CAT-06 | Phase 2 | Complete |
| CAT-07 | Phase 1 | Complete |
| CAT-08 | Phase 2 | Complete |
| CAT-09 | Phase 2 | Complete |
| CAT-10 | Phase 2 | Gaps Found |
| INT-01 | Phase 2 | Gaps Found |
| INT-02 | Phase 2 | Gaps Found |
| INT-03 | Phase 2 | Gaps Found |
| INT-04 | Phase 2 | Gaps Found |
| INT-05 | Phase 2 | Gaps Found |
| INT-06 | Phase 2 | Gaps Found |
| AUD-01 | Phase 3 | Pending |
| AUD-02 | Phase 3 | Pending |
| AUD-03 | Phase 3 | Pending |
| ART-01 | Phase 3 | Pending |
| ART-02 | Phase 3 | Pending |
| ART-03 | Phase 3 | Pending |
| ART-04 | Phase 3 | Pending |
| MOD-01 | Phase 2 | Gaps Found |
| MOD-02 | Phase 2 | Gaps Found |
| MOD-03 | Phase 3 | Pending |
| MOD-04 | Phase 3 | Pending |
| MOD-05 | Phase 3 | Pending |
| EX-01 | Phase 1 | Complete |
| EX-02 | Phase 4 | Pending |
| DIST-01 | Phase 4 | Pending |
| DIST-02 | Phase 4 | Pending |
| DIST-03 | Phase 4 | Pending |
| DIST-04 | Phase 4 | Pending |
| DIST-05 | Phase 4 | Pending |
| DIST-06 | Phase 4 | Pending |
| EVAL-01 | Phase 5 | Pending |
| EVAL-02 | Phase 5 | Pending |
| EVAL-03 | Phase 5 | Pending |
| EVAL-04 | Phase 5 | Pending |
| EVAL-05 | Phase 5 | Pending |
| EVAL-06 | Phase 5 | Pending |
| EVAL-07 | Phase 5 | Pending |
| EVAL-08 | Phase 5 | Pending |
| EVAL-09 | Phase 5 | Pending |
| EVAL-10 | Phase 5 | Pending |
| EVAL-11 | Phase 5 | Pending |
| EVAL-12 | Phase 5 | Pending |
| LEG-01 | Phase 1 | Complete |
| LEG-02 | Phase 1 | Complete |
| LEG-03 | Phase 1 | Complete |
| LEG-04 | Phase 6 | Pending |
| LEG-05 | Phase 6 | Pending |

**Coverage:**

- v1 requirements: 53 total
- Mapped to phases: 53
- Unmapped: 0 ✓

---
*Requirements defined: 2026-09-10*
*Last updated: 2026-09-10 after roadmap creation — 53/53 requirements mapped across 6 phases*
