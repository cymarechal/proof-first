# Phase 1: Foundations — Legal Scaffolding, Numbering, Shared Deal - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-10
**Phase:** 1-Foundations — Legal Scaffolding, Numbering, Shared Deal
**Areas discussed:** PF/MC numbering taxonomy & ranges, Deal brief shape & competitors, Trademark surface in the repo, Phase 1 scaffolding scope

---

## PF/MC Numbering Taxonomy & Ranges

### Q1 — How should the PF section taxonomy resolve the CAT-01 vs. research-table conflict?

| Option | Description | Selected |
|--------|-------------|----------|
| 6 sections, CotM sub-blocks | Keep research's six PF sections; carve PF-1's reserved range into seven named sub-blocks, one per Command of the Message element. Satisfies CAT-01 literally, keeps orthogonal concerns out of the spine. | ✓ |
| 6 sections, flat PF-1 | Research's table verbatim; CotM elements are sub-headings only, numbers run sequentially across PF-1. | |
| One section per CotM element | Seven top-level CotM sections plus opening, buzzwords, integrity, mechanics, voice — ~12 sections. | |

**User's choice:** 6 sections, CotM sub-blocks
**Notes:** CAT-01 and `.planning/research/ARCHITECTURE.md:166` genuinely conflicted — CAT-01 says sections follow the seven CotM elements, the research table makes the whole spine one section. The sub-block carve resolves both without inflating the section count.

### Q2 — Where does the authoritative ID registry live?

| Option | Description | Selected |
|--------|-------------|----------|
| NUMBERING.md at repo root | Range table, allocated IDs, deprecated-never-reused table. Zero inference tokens; SKILL.md carries only the stated totals line. | ✓ |
| Inside SKILL.md | Model sees ranges on every activation, but burns CAT-08's ~500-line budget on contributor process. | |
| references/numbering.md | Ships with the skill for runtime citation checks — mostly duplicates Phase 3's checklist files. | |

**User's choice:** NUMBERING.md at repo root

### Q3 — How should the MC- namespace reserve its ranges?

| Option | Description | Selected |
|--------|-------------|----------|
| Blocks of 5 per dimension | MC-1–5 Metric through MC-36–40 Competition. Ceiling MC-40. Granular enough for actionable check-mode citations. | ✓ |
| One ID per dimension | MC-1–8, sub-questions as unnumbered bullets. Cleanest mapping to AUD-01 but no granularity in citations. | |
| Defer to Phase 3 | Freeze the prefix only — fails Phase 1's own success criterion 1. | |

**User's choice:** Blocks of 5 per dimension

### Q4 — Should Phase 1 ship a mechanical ID-integrity check?

| Option | Description | Selected |
|--------|-------------|----------|
| Policy + stdlib checker in CI | NUMBERING.md states the contract; a stdlib-only script fails on duplicate, out-of-range, reused-after-deprecation, and cited-but-undefined IDs. Runs vacuously green until Phase 2. | ✓ |
| Written policy only | No code in a scaffolding phase; risk is that the guarantee the citation scheme rests on is verified by nothing. | |
| Policy now, checker in Phase 5 | One Python entry point in the repo, but Phases 2–3 author every rule unchecked. | |

**User's choice:** Policy + stdlib checker in CI
**Notes:** Makes MOD-05's "never cites a nonexistent rule number" checkable rather than aspirational.

---

## Deal Brief Shape & Competitors

### Q1 — How much should examples/deal-brief.md carry?

| Option | Description | Selected |
|--------|-------------|----------|
| Facts + customer source material | Canonical facts plus RFP questions with scoring weights, discovery quotes, economic buyer priorities, decision criteria, paper process. | ✓ |
| Facts only | One compact page of profile, figures, roles, timeline, competitors — leaves CAT-05 with no source material to point at. | |
| Facts + source material + bad drafts | Also ships slop-ridden "before" drafts per artifact family — pulls Phase 4/5 work forward before the catalog exists. | |

**User's choice:** Facts + customer source material
**Notes:** CAT-05, ART-01, AUD-01 and EVAL-04 all need facts external to the sentence being written.

### Q2 — Who are the parties in the fictional deal?

| Option | Description | Selected |
|--------|-------------|----------|
| Fictional parties, real platforms | Buyer, integrator and rivals invented; migration source/target are real named platforms so vendor-specific product nouns work. | ✓ |
| Everything fictional | Maximum neutrality, but guts the deletion test and the architecture narrative. | |
| Fictional buyer, real vendors | Most realistic — but publishes comparative positioning against real companies, which is exactly what INT-05 flags. | |

**User's choice:** Fictional parties, real platforms

### Q3 — Should the deal brief deliberately include facts inconvenient for the vendor?

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, bake in the hard facts | Unmeasured baseline, a certification not held, an evaluator favouring the incumbent, an uncommittable timeline. | ✓ |
| Clean deal, adversarial scenarios later | Simpler brief, but Phase 2 must invent evidence gaps ad hoc — the drift EX-01 exists to stop. | |
| Two briefs — clean and hostile | Broadest coverage but contradicts EX-01's single brief and doubles the fact surface. | |

**User's choice:** Yes, bake in the hard facts
**Notes:** Directly answers the cherry-picked-scenario risk in `.planning/research/PITFALLS.md:108`.

### Q4 — What scale and sector is the deal?

| Option | Description | Selected |
|--------|-------------|----------|
| Regulated mid-enterprise | ~$4–8M / 3 years, regulated sector, formal scored RFP, CFO economic buyer, VP Infrastructure champion, three bidders. | ✓ |
| Large enterprise, board-level | $20M+, regulator in the loop, five bidders — heavier fact surface, less representative reader. | |
| Mid-market commercial | ~$1.5M, light process — leaves several MEDDICC dimensions and INT-06 with nothing to bite on. | |

**User's choice:** Regulated mid-enterprise

---

## Trademark Surface in the Repo

### Q1 — How much trademark surface in filenames and headings?

| Option | Description | Selected |
|--------|-------------|----------|
| Generic names, marks in body text only | references/completeness-audit.md; the family name appears only in body prose where needed to identify the source concepts. | ✓ |
| Name it directly | meddicc-checklist.md with MEDDICC headings — best discoverability, worst fork-and-index surface. | |
| Generic filename, mark in the heading | Splits the difference; slightly harder to defend than body-text-only. | |

**User's choice:** Generic names, marks in body text only
**Notes:** Overrides the `meddicc-checklist.md` filename proposed in `.planning/research/ARCHITECTURE.md:69`. Driven by `.planning/research/PITFALLS.md:71-82` — the MEDDIC family has documented enforcement history against community content of exactly this kind.

### Q2 — How does Phase 1 make the paraphrase boundary auditable?

| Option | Description | Selected |
|--------|-------------|----------|
| SOURCES.md with an approved-source rule | Lists public secondary sources per framework; every framework-derived concept must trace to one, vendor training-portal material out of bounds. | ✓ |
| Prose statement in NOTICES.md | One less file, but Phase 6 verification becomes re-derivation. | |
| Per-rule inline provenance | Strongest trail, but spends CAT-08's budget and turns a runtime artifact into a legal document. | |

**User's choice:** SOURCES.md with an approved-source rule

### Q3 — How should NOTICES.md state ownership and status?

| Option | Description | Selected |
|--------|-------------|----------|
| Named owners, contested family flagged | Force Management and Challenger Inc. named; MEDDIC family stated as contested with multiple claimants. Last-reviewed date. No validity or litigation claims. | ✓ |
| Add a dated litigation note | More transparent, but puts the repo on record about live litigation and needs constant re-checking. | |
| One named owner each, symmetric | Cleanest to read, but attributing the MEDDIC marks to one party is unsupported by the research. | |

**User's choice:** Named owners, contested family flagged

### Q4 — How is the per-file attribution pointer handled?

| Option | Description | Selected |
|--------|-------------|----------|
| Canonical string + CI enforcement | NOTICES.md defines the exact one-liner and the file list; the checker asserts each listed file carries it once it exists. | ✓ |
| Canonical string, review-only | No extra code, but the pointer is the kind of line that gets dropped in a refactor unnoticed. | |
| NOTICES.md only, no per-file pointers | Zero duplication, but a reader auditing one framework-derived file sees no posture. | |

**User's choice:** Canonical string + CI enforcement

---

## Phase 1 Scaffolding Scope

### Q1 — What does Phase 1 actually create on disk?

| Option | Description | Selected |
|--------|-------------|----------|
| Requirement-scoped files only | LICENSE, NOTICES.md, SOURCES.md, NUMBERING.md, examples/deal-brief.md, checker + self-tests, CI workflow, claim-free README. Layout documented, not pre-created. | ✓ |
| Full skeleton with placeholders | Every directory and stub created — but empty stubs age badly and manifest text cannot be written honestly yet. | |
| Add a frozen minimal SKILL.md | Locks CAT-09 early and gives CI a real file — but SKILL.md is Phase 2's deliverable and a live stub is a hazard. | |

**User's choice:** Requirement-scoped files only

### Q2 — Where does the skill folder live in the repo?

| Option | Description | Selected |
|--------|-------------|----------|
| skills/proof-first/ | Repo-root artifacts never ship to an installed user; folder name equals frontmatter name; ZIP upload is that one folder. | ✓ |
| Repo root is the skill | Shortest paths, but evals/, examples/, NOTICES.md and CI config all ride along on install. | |
| skills/proof-first/ with a root copy | Broadest compatibility, but two copies of the catalog is the drift problem the single-source rule prevents. | |

**User's choice:** skills/proof-first/

### Q3 — How does the repo stop later examples from contradicting the deal brief?

| Option | Description | Selected |
|--------|-------------|----------|
| Canonical figures table + numeric check | Every figure keyed in a table; the checker fails on any numeric literal in examples/ or scenarios absent from it. Prose facts stay prose. | ✓ |
| Stable keys on every fact | Fullest traceability, but turns a narrative brief into a database and still cannot verify surrounding prose. | |
| Prose only, consistency by review | Readable, but EX-01's one guarantee is then enforced by attention alone. | |

**User's choice:** Canonical figures table + numeric check

### Q4 — What version scheme does Phase 1 freeze?

| Option | Description | Selected |
|--------|-------------|----------|
| Semver with stated change classes | Patch = wording, minor = rule added in range, major = rule deprecated or section restructured. Cited by deprecation entries and DIST-05's re-sync. | ✓ |
| Date-based versions | Signals freshness, says nothing about citation stability. | |
| Commit SHA and date only | Precise and ceremony-free, but a plugin manifest needs a version string. | |

**User's choice:** Semver with stated change classes
**Notes:** Needed because the deprecation policy locked in Q4 of the numbering area cites version numbers.

---

## Claude's Discretion

- Exact per-section PF ceilings within the research's proposed shape.
- Which regulated sector, the invented company/integrator names, the specific real platforms, and how many RFP questions the source-material section carries.
- The checker script's filename and location, and the CI job shape.
- Whether the deal brief also carries a `Last reviewed:` vocabulary-staleness marker.

## Deferred Ideas

- Plugin and marketplace manifests — Phase 4 (DIST-02). Phase 1 freezes only the path and version scheme they depend on.
- Adversarial / objection-handling scenarios — Phase 5 scenario set. Phase 1 provides the inconvenient facts they build on.
- A repo-wide "last reviewed" freshness cadence — Phase 6 launch readiness.
- Textual anti-plagiarism verification against framework material — Phase 6 legal review gate (LEG-04).
- A second, non-Anthropic benchmark runner — v2 (XPRV-01/02).
