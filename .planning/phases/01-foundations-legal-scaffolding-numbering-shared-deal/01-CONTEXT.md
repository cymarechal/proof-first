# Phase 1: Foundations — Legal Scaffolding, Numbering, Shared Deal - Context

**Gathered:** 2026-09-10
**Status:** Ready for planning

<domain>
## Phase Boundary

Freeze the three foundations every later phase is forced to inherit, before any rule content is drafted:

1. **Rule ID namespaces** — `PF-<section>.<n>` and `MC-<n>`, with numeric ranges reserved per section (CAT-07).
2. **The shared fictional deal** — one canonical cloud-migration brief supplying every fact any example, scenario, or benchmark prompt ever cites (EX-01).
3. **Legal posture** — MIT license, a canonical `NOTICES.md` naming all three frameworks individually, and an auditable paraphrase boundary (LEG-01, LEG-02, LEG-03).

**Not in this phase:** any prose rule text, the completeness-audit items themselves, artifact patterns, SKILL.md, distribution manifests, the eval harness, or the legal review gate (Phase 6 / LEG-04).

</domain>

<decisions>
## Implementation Decisions

### Rule Numbering (CAT-07)

- **D-01:** PF namespace uses **six sections**, per `.planning/research/ARCHITECTURE.md:166`: `PF-0.x` Opening/Reframe, `PF-1.x` Structure (Command of the Message spine), `PF-2.x` Proof & Integrity, `PF-3.x` Specificity & Buzzwords, `PF-4.x` Prose Mechanics, `PF-5.x` Consistency & Voice. **`PF-1`'s reserved range is carved into seven named sub-blocks, one per Command of the Message element** (Before scenario, After scenario, Required Capabilities, Metrics, Proof Points, Differentiators, Positive Business Outcomes). This resolves the conflict between CAT-01 ("sections follow the CotM elements") and the research table (CotM as one section): CAT-01 is satisfied inside `PF-1`, while orthogonal concerns keep their own sections. A rule added later to Metrics cannot land next to a Differentiators rule. — **Reversibility:** one-way — every published citation, saved check-mode report, issue, and blog post resolves against these IDs; renumbering is the exact failure the reserved-range scheme exists to prevent.
- **D-02:** MC namespace reserves **blocks of five per MEDDICC dimension**: `MC-1`–`5` Metric, `6`–`10` Economic Buyer, `11`–`15` Decision Criteria, `16`–`20` Decision Process, `21`–`25` Paper Process, `26`–`30` Pain, `31`–`35` Champion, `36`–`40` Competition. Ceiling `MC-40`. Granular enough that check mode can cite "no baseline stated" separately from "no target stated". Phase 3 fills the blocks; it does not choose them. — **Reversibility:** one-way — same citation-stability contract as D-01.
- **D-03:** `NUMBERING.md` at repo root is the **authoritative ID registry**: the range table, every allocated ID, and the deprecated-never-reused table. It is a contributor artifact and costs zero inference tokens. SKILL.md carries only the one-line stated total ("N rules across 6 sections"), which is what lets an out-of-range citation be spotted.
- **D-04:** Deprecation, never deletion — a retired ID is recorded in `NUMBERING.md`'s deprecated table with the version it was retired in and what absorbed it, and is never reassigned. — **Reversibility:** one-way — the guarantee only holds if it has always held.
- **D-05:** Phase 1 ships a **stdlib-only Python ID-integrity checker** wired into CI. It fails on: an ID defined twice, an ID outside its section's reserved range, an ID reused after deprecation, and an ID cited but never defined. It ships with fixture-based self-tests so CI is meaningful before any rule file exists, and it must tolerate the absence of SKILL.md and the reference files. This turns MOD-05 ("never cites a rule number that doesn't exist") from an aspiration into something checkable.

### Shared Deal Brief (EX-01)

- **D-06:** `examples/deal-brief.md` carries **canonical facts plus a customer-source-material section** — a handful of RFP questions with their scoring weights, discovery-call quotes, the economic buyer's stated priorities, the decision criteria, and the paper process. CAT-05 ("a term appearing verbatim in the customer's own source material is marked, not deleted"), ART-01's criteria-mirroring, AUD-01's audit dimensions, and EVAL-04's scenarios all need facts that live *outside* the sentence being written. — **Reversibility:** costly — every later example, scenario, and committed benchmark generation is anchored to these facts.
- **D-07:** **Fictional parties, real platforms.** The buyer, the proposing integrator, and its rival bidders are all invented. The migration source and target are real named platforms, so vendor-specific product nouns are available where the deletion test and ART-02's architecture narrative genuinely need them. No comparative claim about any real company appears anywhere in the repo — which is what INT-05 tells users to do, applied to the repo's own output. — **Reversibility:** costly — changing the cast means rewriting every worked example and re-running the benchmark.
- **D-08:** The brief **deliberately includes facts inconvenient for the vendor**: a pain point with no measured baseline, a compliance certification the integrator does not yet hold, a technical evaluator who openly prefers the incumbent, and a buyer timeline the vendor cannot honestly commit to. This gives INT-01–INT-06 real material to fire on instead of invented demonstrations, and pre-empts the cherry-picked-scenario critique in `.planning/research/PITFALLS.md:108` before the benchmark runs.
- **D-09:** Deal scale is a **regulated mid-enterprise opportunity**: roughly $4–8M over three years, financial services or healthcare, a formal scored RFP, CFO as economic buyer, VP Infrastructure as champion, a security + procurement + legal paper process, three bidders. Formal scoring gives ART-01 something real to mirror; the regulated setting gives INT-06's compliance and certification flags genuine material; the fact set still fits on one page. — **Reversibility:** costly — the magnitude of every number in every example derives from this.
- **D-10:** The brief carries a **"Canonical figures" table** — every dollar amount, date, percentage, and count with a short stable key. The Phase 1 checker extracts numeric literals from `examples/` and the eval scenarios and fails on any figure absent from that table. Regex handles numbers reliably where it cannot handle entities, and numbers are what drifts (`.planning/research/PITFALLS.md:257`). Prose facts — roles, competitor names, pain points — stay ordinary prose under clear headings.

### Legal Posture (LEG-01, LEG-02, LEG-03)

- **D-11:** **Generic filenames and headings; marks in body text only.** The completeness-audit reference is `references/completeness-audit.md`, not `meddicc-checklist.md`, and its headings read "Completeness Audit". The MEDDIC-family name appears only in body prose where it is needed to identify what the concepts derive from — the nominative-fair-use standard of using no more of the mark than necessary — plus one factual attribution in `NOTICES.md`. Filenames get forked, scraped, and search-indexed in ways body text does not, and `.planning/research/PITFALLS.md:71-82` names this family as the highest-risk of the three, with a documented history of enforcement against community content. **This overrides the `meddicc-checklist.md` filename proposed in `.planning/research/ARCHITECTURE.md:69` and its structure diagram.** — **Reversibility:** costly — published paths appear in install docs, forks, and search indexes.
- **D-12:** `SOURCES.md` at repo root lists the **approved public secondary sources per framework** (the frameworks' creators' own books and public posts, encyclopedia-level descriptions) and states the rule: every framework-derived concept must trace to a listed source, and vendor training-portal material is out of bounds regardless of how readily a model reproduces it. Authorable now with zero rule content, and it gives Phase 6's legal gate something concrete to review.
- **D-13:** `NOTICES.md` carries **three separate, individually named statements**. Force Management is named for Command of the Message; Challenger Inc./its successors for Challenger. For the MEDDIC family, state that the marks are **claimed by multiple parties and ownership is contested** rather than attributing them to one holder — this research could not support a single-owner claim, and getting it wrong in a public notices file is worse than not saying it. Each statement carries its own non-affiliation line and paraphrase boundary, plus a `Last reviewed:` date. **No claims about mark validity or litigation** — the repo does not adjudicate trademark status.
- **D-14:** `NOTICES.md` defines the **exact one-line attribution pointer verbatim** and names the files required to carry it (SKILL.md header, the completeness-audit reference, the artifact-patterns reference, README). The Phase 1 checker asserts each listed file carries that exact string once it exists, so the disclaimer cannot drift or be silently dropped in a later edit. One canonical string with N pointers, not N restatements.

### Scaffolding Scope

- **D-15:** Phase 1 creates **requirement-scoped files only**: `LICENSE` (MIT), `NOTICES.md`, `SOURCES.md`, `NUMBERING.md`, `examples/deal-brief.md`, the checker script with its fixture-based self-tests, the CI workflow, and a `README.md` stating what the repo is — **with no claims and no badges** (LEG-05 forbids any number not sourced from a benchmark that has run). The target layout is documented, not pre-created; empty placeholder files age badly and blur the phase boundary the roadmap draws at "before any rule content is drafted".
- **D-16:** The skill lives at **`skills/proof-first/`**. `NOTICES.md`, `SOURCES.md`, `NUMBERING.md`, `examples/`, and `evals/` stay at repo root and never ship to an installed user. Folder name equals the frontmatter `name`, as the Agent Skills spec requires. A claude.ai ZIP upload is that one folder zipped with the folder as its root. — **Reversibility:** one-way — the path is baked into published install commands, the plugin manifest, and the marketplace entry.
- **D-17:** **Semver**, in the skill's frontmatter metadata and the plugin manifest, matched by a git tag. `NUMBERING.md` states what each bump means: patch for wording, minor for a rule added inside a reserved range, major for a rule deprecated or a section restructured. D-04's deprecation entries and DIST-05's derivative re-sync step both cite these versions. — **Reversibility:** costly — published version history cannot be restated.

### Claude's Discretion

- Exact per-section PF ceilings within the research's proposed shape (`PF-0` to `0.9`, `PF-1` to `1.20`, `PF-2` to `2.20`, `PF-3` to `3.10`, `PF-4` to `4.20`, `PF-5` to `5.10`) — adopt as proposed unless planning surfaces a reason to widen a block.
- Which regulated sector (financial services vs. healthcare), the invented company and integrator names, the specific real platforms named as migration source and target, and how many RFP questions the source-material section carries.
- The checker script's filename and location, and the CI provider job shape (a single GitHub Actions job, per `.planning/research/STACK.md:250`).
- Whether the brief also carries a `Last reviewed:` marker for vocabulary staleness (`.planning/research/PITFALLS.md:227` recommends it).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project decisions and scope
- `.planning/PROJECT.md` — core value, the three-framework split (Command of the Message = rule spine, MEDDICC = completeness audit, Challenger = opening rule), deletion test rationale, the five constraints.
- `.planning/REQUIREMENTS.md` — CAT-07, EX-01, LEG-01, LEG-02, LEG-03 are this phase's requirements; the full v1 set shows what these foundations must serve.
- `.planning/ROADMAP.md` — Phase 1 goal and its four success criteria; Phase 6 owns the legal review gate.
- `.planning/STATE.md` — standing blockers, including the unresolved MEDDIC-family trademark status.

### Repo layout, numbering, and legal structure
- `.planning/research/ARCHITECTURE.md:155-185` — the rule-numbering scheme: two disjoint namespaces, the proposed per-section reserved ranges, deprecation-not-deletion, and why numbering is Phase 1 design work rather than later cleanup.
- `.planning/research/ARCHITECTURE.md:46-56` — what a three-rights-holder repo needs that the sibling project does not: canonical `NOTICES.md`, the separate completeness-audit file, per-file attribution pointers.
- `.planning/research/ARCHITECTURE.md:88-126` — the recommended directory tree and its rationale. **Note: D-11 overrides the `meddicc-checklist.md` filename shown there.**
- `.planning/research/ARCHITECTURE.md:60-72` — component responsibilities, including what `examples/deal-brief.md` owns and must not own.

### Legal risk
- `.planning/research/PITFALLS.md:66-93` — Pitfall 3, the trademark analysis: three live marks, the MEDDIC-family inter-vendor litigation and the April 2026 E.D. Pa. genericness ruling, the nominative-fair-use boundary, and why the legal gate is a phase and not a footnote.
- `.planning/research/PITFALLS.md:259-266` — the security/legal mistakes table, including why "MEDDPICC ruled generic" must not be read as covering MEDDIC or MEDDICC.
- `.planning/research/PITFALLS.md:188-205` — Pitfall 7: how the skill's own specificity-over-adjectives mechanism creates the four legal exposure categories the deal brief must give INT-01–06 material for.

### Deal brief and example integrity
- `.planning/research/PITFALLS.md:104-110` — the cherry-picked-scenario risk that D-08 answers.
- `.planning/research/PITFALLS.md:219-233, :255-258` — fact drift between examples and vocabulary staleness; the one-canonical-file mitigation D-10 implements.
- `.planning/research/SUMMARY.md:84-90` — the research's own Phase 1 recommendation and what it expected the phase to deliver.

### Standards and precedent
- `.planning/research/STACK.md:1-60` — Agent Skills frontmatter schema (`name` must match the parent directory), the six documented frontmatter keys, and why `compatibility` is omitted.
- `.planning/research/STACK.md:250-266` — repo hygiene: MIT `LICENSE` at root, the single-job CI surface, the non-affiliation posture, and what the sibling project deliberately does not have.
- `~/devoteam/.claude/plugins/marketplaces/simple-english/` — the SimpleEnglish reference implementation, read directly during research. Inspect `LICENSE`, `README.md` (its footer disclaimer), and the `skills/` layout for the precedent this phase mirrors. Do not copy its text.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

None. The repository is greenfield — `git ls-files` returns only `.claude/CLAUDE.md` and `.planning/**`. Phase 1 writes the first product files in the repo.

### Established Patterns

- No `.planning/codebase/` maps exist, and none are needed yet — there is no code to map.
- The nearest thing to a house pattern is the SimpleEnglish reference checkout at `~/devoteam/.claude/plugins/marketplaces/simple-english/`, which this project deliberately mirrors in layout, distribution model, and honesty posture. Its four-layer split (distribution / content / evidence / legal) is the structure Phase 1 begins laying down.

### Integration Points

- `.planning/config.json` sets `commit_docs: true`, `parallelization: true`, and `granularity: standard`. CI is the only automation surface Phase 1 introduces.
- Phase 1's checker script is the seam every later phase plugs into: Phase 2 and 3 rule files, Phase 4 examples and manifests, and Phase 5 scenarios all get validated by it.

</code_context>

<specifics>
## Specific Ideas

- The `PF-1` sub-block layout should be written into `NUMBERING.md` as a table with the CotM element names spelled out, so a contributor adding a Metrics rule reads the element name rather than inferring it from a number.
- `NOTICES.md`'s attribution pointer should be quoted verbatim in a fenced block inside `NOTICES.md` itself, so the checker and a human contributor read the same source string.
- The deal brief's "Canonical figures" table is the interface the checker validates against — treat its format as an API, not prose formatting.
- The checker must run green on a repo that contains none of the files it will eventually validate; absence is not failure, only contradiction is.
- `README.md` at this phase says what the repo is and states that no measured claims exist yet. It gets its numbers in Phase 6, sourced only from `RESULTS.md`.

</specifics>

<deferred>
## Deferred Ideas

- **Plugin and marketplace manifests** (`.claude-plugin/plugin.json`, `marketplace.json`) — `.planning/research/SUMMARY.md:88` suggested scaffolding these in Phase 1, but DIST-02 belongs to Phase 4 and their description text cannot be written honestly before the catalog exists. Phase 1 freezes the path they will point at (D-16) and the version scheme they will carry (D-17); that is the whole dependency.
- **Adversarial / objection-handling scenarios** — `.planning/research/PITFALLS.md:108` recommends stress-testing with a scenario type the catalog was not designed around. D-08 puts the inconvenient *facts* in the brief; building an adversarial scenario on top of them belongs with the Phase 5 scenario set.
- **A "last reviewed" freshness cadence across the repo** — `.planning/research/PITFALLS.md:227` wants vocabulary staleness visible. D-13 puts a review date on `NOTICES.md`; extending the convention repo-wide is a launch-readiness concern for Phase 6.
- **Textual anti-plagiarism checking** against framework material — Phase 6's legal review gate (LEG-04) covers this. Phase 1 makes it auditable via `SOURCES.md` (D-12); it does not attempt to verify it mechanically, which no tool in the stated stack can do.
- **A second, non-Anthropic benchmark runner** — `.planning/research/STACK.md` names it; XPRV-01/02 are v2 requirements.

</deferred>

---

*Phase: 1-Foundations — Legal Scaffolding, Numbering, Shared Deal*
*Context gathered: 2026-09-10*
