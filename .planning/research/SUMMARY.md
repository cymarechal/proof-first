# Project Research Summary

**Project:** Proof First
**Domain:** Public, cross-harness AI agent skill — technical presales writing discipline (rule catalog + linter + benchmark, sibling to SimpleEnglish/ASD-STE100)
**Researched:** 2026-09-10
**Confidence:** MEDIUM-HIGH overall

## Executive Summary

Proof First is a public, MIT-licensed Agent Skill that teaches AI to write persuasive, evidence-backed presales documents (RFP/RFI responses, proposals, executive summaries, demo/discovery material). Experts in this space (per the SimpleEnglish precedent this project deliberately mirrors) build such skills as a four-layer repo — distribution manifests, a progressive-disclosure SKILL.md + references/ content layer, an evidence layer (worked examples + a reproducible eval harness), and a legal layer — shipped as one dependency-free folder consumable natively by Claude Code, Cursor, Codex, Copilot, Gemini CLI, and OpenCode via the Agent Skills standard. The recommended stack is deliberately boring: stdlib-only Python 3.11+ for the linter/benchmark harness, hand-authored JSON/Markdown manifests, no build step, no external NLP dependency (spaCy explicitly rejected).

The single resolved design tension governing everything else: SimpleEnglish "deletes persuasion by design" and Proof First cannot copy that stance, because persuasion is the deliverable. The research converges on one mechanism to resolve this: **every subtractive rule (delete this buzzword, delete this hedge) must be paired with a constructive rule (attach a metric, proof point, or name instead).** Persuasion here is achieved through specificity, not adjectives — and this pairing has to be designed into the rule catalog's first draft, not patched on later, because deletion alone reproduces the flat, STE-flavored prose PROJECT.md names as the project's own worst failure mode. A second convergence, equally load-bearing: Command of the Message's Before scenario, MEDDICC's Identify Pain, and Challenger's Reframe all independently arrive at "state the buyer's problem before the vendor's capability" — this has to resolve into exactly ONE opening rule sourced from three frameworks, not three overlapping ones a writer has to reconcile.

The key risks are asymmetric and some are severe enough to gate release, not just inform phase order. Highest-severity: shipping flat, unpersuasive prose despite passing every mechanical check (mitigated by the pairing rule above and a judge rubric with a dedicated "persuasive force" dimension). Second: trademark exposure is uneven across the three anchor frameworks — a federal court (E.D. Pa., April 2026) found "MEDDPICC" generic and cancelled a registration in a suit alleging enforcement takedowns against community content; MEDDICC/MEDDIC status is separately unresolved; Command of the Message and Challenger show no comparable ruling but are live, actively asserted marks. This requires a dedicated legal-review gate distinct from general repo scaffolding, not a footnote. Third: the eval harness's credibility is structurally weaker here than in the reference project — the deletion test is a semantic judgment no regex can perform, so the linter's buzzword-proxy word list must be independently sourced from the SKILL.md's own worked examples or the benchmark becomes tautological (rewarding the skill for avoiding a list it was told to avoid). Fourth: the deletion test needs a provenance override, or it will strip a customer's own RFP vocabulary from a scored response — a false positive with real business cost, not just a style miss.

## Key Findings

### Recommended Stack

Zero-dependency, hand-authored files throughout: `SKILL.md` + `references/*.md` conforming to the Agent Skills standard (agentskills.io — a hard frontmatter allow-list: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`; nothing else validates), `.claude-plugin/{plugin.json,marketplace.json}` for the Claude Code plugin marketplace, `output-styles/proof-first.md` for an always-on persona, and `prompts/system-prompt.md` as a paste-able fallback for harnesses without skill support. The eval harness is stdlib-only Python (3.11+): `re`-based deterministic linting, a Claude Code CLI (`-p`, headless) benchmark runner, and a blind pairwise LLM judge. `textstat` is an acceptable optional bolt-on metric; spaCy is explicitly rejected (breaks the zero-dependency posture for marginal precision gain on a problem — semantic buzzword judgment — no NLP library solves anyway).

**Core technologies:**
- Agent Skills standard (`SKILL.md` + `scripts/`/`references/`/`assets/`) — the only genuinely cross-harness format in 2026; consumed natively by 7+ major harnesses
- `.claude-plugin/plugin.json` + `marketplace.json` — zero-build Claude Code plugin distribution, proven by SimpleEnglish
- Python 3.11+ stdlib only (`re`, `json`, `argparse`, etc.) — matches the project's own zero-dependency constraint; `python3 script.py` works forever, no lockfile
- Claude Code CLI headless (`-p`, `--bare`, `--model` exact string, `--effort` pinned, `--disallowedTools`) — the benchmark driver; `--bare` should be added even though the reference implementation predates it, to guarantee a clean baseline
- `skills-ref` validator — run before every release to catch frontmatter/schema errors that silently break distribution

Notable stack caveat: claude.ai's upload help center states a 200-char `description` cap versus the general spec's 1024 — unreconciled; write descriptions ≤200 chars to be safe everywhere (LOW confidence on the exact number, worth a manual smoke test).

### Expected Features

The skill is best understood not as a ban-list tool but as an **evidence-attachment enforcement tool**: every rule is checkable as "does this claim have a metric, proof point, capability, or name attached — yes/no."

**Must have (table stakes):**
- Command of the Message rule spine, numbered — Before/After scenarios, Required Capabilities, Metrics, Proof Points, Differentiators, PBOs, each mapped to a checkable writing rule
- The deletion test as the buzzword rule, stated with positive evidence-attachment framing, not deletion alone
- Integrity/anti-fabrication section — refuses to invent metrics, references, benchmarks, certifications; marks gaps instead
- MEDDICC-derived completeness audit, kept structurally and namespace-separate from prose rules (document-level checklist, not sentence-level rules)
- Challenger opening rule — resolved into ONE instruction alongside the CotM Before-scenario/MEDDICC Identify-Pain overlap
- Self-contained prose mechanics (no simple-english dependency) — a compact, presales-tuned subset (sentence length, active voice, modal discipline, one-claim-per-sentence), deliberately smaller and less rigid than STE's
- Write mode + check mode (rule number / offending text / compliant rewrite), with check mode reporting three distinct categories (prose violations, MEDDICC completeness gaps, integrity flags) plus a structural/ordering pass
- Per-artifact conventions for all four families (RFP/RFI, proposal, exec summary, demo/discovery) — genuinely different structures, not one rule set with light variation
- One shared fictional deal (a cloud migration) anchoring every example
- Trademark/non-affiliation disclosure for all three frameworks

**Should have (differentiators):**
- Persuasion-preserving self-check — checks for presence of evidence, not just absence of violations (a genuinely novel step relative to SimpleEnglish's model)
- Deterministic linter with regex proxies for the qualitative rules, enabling the benchmark claim
- Multi-model, blind-pairwise benchmark, published and reproducible

**Defer (v2+):**
- Additional artifact families (SOW narrative sections, security questionnaires)
- Localization/non-English rule catalogs
- Any Challenger "Tailor"/"Take Control" conversational expansion — explicitly out of scope, would need full re-scoping

Confidence caveat carried forward explicitly: "AI slop in presales specifically" as a documented literature is thin (LOW) — presales-specific failure patterns here are inferred from general AI-slop writing plus the three frameworks, not sourced from presales-specific case studies. Likewise, exact RFP scoring weight percentages are aggregated from vendor-blog content, not a standards body — directional only, not to be encoded as literal rules. The MEDDICC-as-document-completeness-checklist translation is this research's own synthesis; no public precedent was found, and it should be validated with actual presales practitioners rather than treated as settled convention.

### Architecture Approach

Four-layer separation (distribution / content / evidence / legal), directly modeled on SimpleEnglish, with progressive disclosure enforced by a ~5,000-token / <500-line ceiling on SKILL.md itself — pushing the MEDDICC checklist, artifact patterns, and the deletion-test worked-pairs table into four `references/*.md` files, one per orthogonal audit dimension (never mixed). Two disjoint rule-numbering namespaces are required, decided before drafting: `PF-<section>.<n>` for the prose catalog (with reserved numeric headroom per section) and `MC-<n>` for the MEDDICC completeness audit — this is what lets a check-mode report cite two catalogs at once without ambiguity, and it is a Phase 0/1 design decision, not a cleanup task; retrofitting reserved ranges after organic numbering forces the exact renumbering the scheme exists to prevent. The mode axis is write vs. check (matching PROJECT.md exactly) — strictness and artifact-type were both explicitly considered and rejected as competing axes (artifact type is a classification step, not a third mode; strictness has no legitimate "relaxable" version of a binary requirement like anti-fabrication).

**Major components:**
1. `skills/proof-first/SKILL.md` — frontmatter, two-mode framing, artifact classification step, the compact numbered rule catalog, pointers to references
2. `references/{checklist.md, meddicc-checklist.md, artifact-patterns.md, deletion-test.md}` — one file per audit dimension, exhaustive within its own dimension only
3. `examples/deal-brief.md` (new — no SimpleEnglish analog) — the single fictional deal's canonical facts, required because this domain's shared example carries far more moving facts (dollar figures, roles, timeline, competitors) than SimpleEnglish's `sqlpipe`
4. `evals/{proof_lint.py, run_bench.py, scenarios.json, results/}` — the closed, auditable benchmark loop: fixed prompts → generation → deterministic proxy scoring → committed raw JSON → generated/regenerable summary + RESULTS.md
5. `NOTICES.md` (new) — single canonical trademark/non-affiliation statement for all three rights-holders, pointed to (not repeated) from every framework-touching file

Real build-order finding: apparent dependencies are often looser than they look. Scenarios and the deal brief can start in parallel with SKILL.md drafting (they need rule *concepts*, not final wording); MEDDICC has zero content dependency on the prose catalog and can be drafted in any order; but README badges have a hard, non-negotiable dependency on the benchmark having actually run — this is the single most likely place the repo could accidentally violate its own "measured claims or no claims" constraint.

### Critical Pitfalls

1. **Flat, unpersuasive output despite passing every check** — the project's central, unavoidable risk. Avoid by pairing every subtractive rule with a constructive one from the first draft, and by scoring a dedicated "persuasive force" dimension in the blind judge, independent of clarity/evidence-density, so a flat-but-clean draft can't hide behind a high aggregate score.
2. **The deletion test breaks on customer/RFP-sourced vocabulary and compound terms** — apply the test per-token (not per-phrase) and add a provenance override: a term appearing verbatim in the customer's own RFP/requirements is retained and marked, never silently deleted. Must be exercised in the pressure-test suite with an actual RFP-excerpt scenario.
3. **Trademark exposure, worst in the MEDDIC/MEDDICC/MEDDPICC family** — a federal court ruling found "MEDDPICC" generic in a suit alleging enforcement takedowns against community content (posts, videos, book listings); MEDDICC/MEDDIC status is separately unresolved. Command of the Message and Challenger show no comparable ruling but are live marks. Requires a dedicated legal-review phase gate before public launch, with per-framework, individually named non-affiliation disclaimers (not one blended footnote) — not legal advice, flag for counsel review.
4. **Benchmark self-serving failure modes, worse here than the reference project** — judge position bias (counter-balance both orders, mandatory), self-preference/family bias (disclose judge-vs-generator family relationship per row), and critically: **linter tautology** — if the buzzword-proxy word list is drawn from the same examples as SKILL.md's worked illustrations, "improvement" is circular. The proxy list must be independently sourced from an external corpus, never derived from the rule catalog's own examples.
5. **The linter cannot check the rule it's built around** — unlike SimpleEnglish's mostly-syntactic rules, the deletion test is a semantic judgment; caveat language copied verbatim from SimpleEnglish ("it undercounts") would understate this. Must state explicitly that the deletion test is not machine-checkable at all, and report mechanical-proxy and judged-persuasion numbers as two separately labeled figures, never blended.

Additional pitfalls carried into phase mapping below: skill-triggering failures (description field as an explicit trigger list, "should"/soft-language audit, hallucinated rule-number citations across three numbering systems); domain-specific legal hazards beyond fabrication (commitment-shaped "will" language, unauthorized reference disclosure, competitor comparisons, compliance/export claims — each needs its own flag category in the Integrity section, not deferral to v2); and post-launch decay (multi-channel artifacts drifting from a single source of truth, stale dated benchmark numbers).

## Implications for Roadmap

Based on combined research, suggested phase structure:

### Phase 1: Foundations — legal scaffolding, numbering scheme, shared deal
**Rationale:** Zero content dependencies, fully parallelizable, and everything downstream depends on the numbering namespaces and the deal brief being frozen before real drafting starts (Architecture's Phase 0/1 finding: numbering is a design decision, not a cleanup task).
**Delivers:** `LICENSE`, `NOTICES.md` skeleton, `.claude-plugin/*.json` skeletons, `examples/deal-brief.md`, the `PF-#`/`MC-#` namespace with reserved ranges per section.
**Addresses:** Trademark/non-affiliation requirement (Active requirements list); shared fictional deal requirement.
**Avoids:** Pitfall 3 (trademark exposure — start the disclaimer/namespace discipline here, before frameworks are named repeatedly) and the numbering-retrofit trap.

### Phase 2: Rule catalog — SKILL.md core (CotM spine, deletion test, integrity, Challenger opening)
**Rationale:** This is the whole point of the skill; nothing else (references, linter, benchmark) can be written correctly before the rule spine's section skeleton is frozen.
**Delivers:** `skills/proof-first/SKILL.md` with the numbered catalog, evidence-attachment framing built in from the first draft, the resolved single opening rule (CotM Before + MEDDICC Identify Pain + Challenger Reframe converged into one instruction), the integrity section including the four flag categories (commitments, reference disclosure, competitor claims, compliance/export — per Pitfall 7, not deferrable to v2).
**Uses:** Agent Skills frontmatter schema, the ~5,000-token/500-line ceiling discipline.
**Implements:** `skills/proof-first/SKILL.md` component; the persuasion-preservation pairing (subtract + replace) as a structural requirement, not a polish pass.

### Phase 3: Reference files — MEDDICC checklist, artifact patterns, deletion-test worked pairs, prose mechanics checklist
**Rationale:** Depends on Phase 2's section skeleton and numbering being frozen; MEDDICC itself has no content dependency on the prose catalog and can proceed largely in parallel once its `MC-#` namespace is agreed.
**Delivers:** `references/{meddicc-checklist.md, artifact-patterns.md, deletion-test.md, checklist.md}` — one file per orthogonal audit dimension, never blended (Pitfall/Anti-Pattern: blending MEDDICC into prose rules is explicitly ruled out).
**Addresses:** Per-artifact conventions (RFP/RFI, proposal, exec summary, demo/discovery), MEDDICC completeness audit, deletion-test provenance override for customer/RFP-sourced terms.
**Avoids:** Pitfall 2 (deletion test edge cases) — the worked-pairs file must include at least one RFP-excerpt/customer-language pressure-test case.

### Phase 4: Multi-channel distribution + worked examples
**Rationale:** Output style and system prompt are lossy compressions of SKILL.md and can only be authored once its rule content is stable; before/after examples need the deal brief plus the stabilized rule catalog to reference real rule numbers.
**Delivers:** `output-styles/proof-first.md`, `prompts/system-prompt.md`, `examples/before-after.md`, finalized `.claude-plugin/*.json`.
**Uses:** Claude Code output-styles spec, plugin marketplace schema.
**Implements:** The "synced-derivative pair" pattern — treat these as generated from one source of truth, with a re-sync step scheduled on every future SKILL.md revision (Pitfall 8).

### Phase 5: Eval harness — linter, scenarios, benchmark, judge
**Rationale:** Genuinely sequenced last per both Architecture and Features research — the linter needs rule *concepts* frozen, and a linter built against rules still changing is wasted work; the benchmark needs the linter, per-artifact conventions, and the shared deal all in place.
**Delivers:** `evals/proof_lint.py` (independently-sourced proxy word list, explicit "deletion test is not machine-checkable" docstring), `evals/scenarios.json`, `evals/run_bench.py`, committed `results/raw/*.json`, `results.json`, `RESULTS.md` with a mandatory "honest number warnings" section covering position bias, family bias, baseline-prompt parity, linter-proxy provenance, and sample size.
**Addresses:** Multi-model benchmark and blind pairwise judge (Active requirements); persuasion-force judge dimension.
**Avoids:** Pitfall 4 (benchmark self-serving failure modes) and Pitfall 5 (linter/semantic-gap honesty) — both require explicit, named mitigations before the first published number, not retrofits.

### Phase 6: Legal review gate + public launch
**Rationale:** Distinct from general repo scaffolding per Pitfalls research — the MEDDIC/MEDDICC/MEDDPICC litigation history specifically warrants a dedicated review step, not a footnote task, and README badges have a hard dependency on Phase 5's benchmark having actually run.
**Delivers:** Reviewed, per-framework non-affiliation disclaimers; finalized `README.md` with badges sourced only from committed `RESULTS.md`; a stated (even modest) re-benchmark maintenance cadence.
**Avoids:** Pitfall 3 (trademark) and Pitfall 8 (post-launch decay) — dated, model-version-pinned benchmark claims from day one.

### Phase Ordering Rationale

- Numbering scheme and the shared fictional deal must be frozen before real content drafting (Architecture's explicit "Phase 0/1 design decision, not cleanup" finding) — hence Phase 1 first.
- The rule catalog (Phase 2) is the load-bearing dependency for every reference file, every worked example, and the linter itself — nothing legitimately parallelizes ahead of its section-skeleton freeze, only after it.
- MEDDICC is deliberately kept in a separate namespace and separate file (Phase 3) to avoid the "mushy catalog" category error PROJECT.md and Pitfalls both flag as an anti-pattern.
- The eval harness (Phase 5) is sequenced last, mirroring the reference repo's own evolution (`ste_lint.py` and `scenarios.json` post-date the rule catalog) and avoiding wasted work against a still-moving rule set.
- Legal review is broken out as its own late-stage gate (Phase 6) rather than folded into general scaffolding, specifically because of the documented MEDDIC-family litigation risk — this is the one place research recommends deviating from a "scaffolding happens whenever" default.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2 (rule catalog):** the persuasion-preservation pairing mechanism and the single-resolved-opening-rule are novel design work with no external prior art — needs careful phase-level research/discussion, not just execution.
- **Phase 3 (MEDDICC checklist / artifact patterns):** no public "MEDDICC-for-documents" precedent exists; this is original synthesis that should be pressure-tested, ideally against practitioner feedback, during planning.
- **Phase 5 (eval harness):** LLM-judge bias mitigation and linter-tautology avoidance are subtle, easy to get wrong, and directly determine whether the project's headline claim is credible — worth a research pass at plan time even though the mechanics (regex counting, headless CLI calls) are otherwise standard.
- **Phase 6 (legal gate):** explicitly flagged as needing input beyond this research — trademark status of MEDDICC/MEDDIC specifically should be reconfirmed with current sources or counsel before the phase closes.

Phases with standard patterns (skip research-phase):
- **Phase 1 (foundations):** directly copies proven SimpleEnglish scaffolding patterns (LICENSE, plugin manifests) — mechanically well-documented.
- **Phase 4 (distribution/worked examples):** output-styles and plugin manifest formats are documented, stable Claude Code specs; the "synced-derivative" discipline is a process pattern, not a research question.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Official specs (agentskills.io, code.claude.com docs) fetched directly for every load-bearing schema; only the claude.ai description-length figure and spaCy-vs-regex tradeoff are engineering judgment, flagged inline |
| Features | MEDIUM | Framework mechanics (CotM, MEDDICC, Challenger) cross-checked across official and multiple independent secondary sources; "AI slop in presales" specifically and MEDDICC-as-document-checklist translation are this research's own synthesis, explicitly flagged LOW |
| Architecture | HIGH for repo layout/eval-harness shape (direct byte-for-byte inspection of the reference repo); MEDIUM-HIGH for the numbering scheme and mode-axis recommendations (novel design work, no external prior art for this project's specific catalog shape) |
| Pitfalls | MEDIUM-HIGH | Design/process and LLM-eval pitfalls backed by cited peer-reviewed/preprint research (position bias, self-preference bias, instruction-decay); trademark specifics are MEDIUM confidence — sourced via secondary press reporting on a court ruling, explicitly flagged as not legal advice |

**Overall confidence:** MEDIUM-HIGH

### Gaps to Address

- **"AI slop in presales writing" as a distinctly documented failure pattern is thin (LOW).** Treat the exact wording of before/after slop examples as something to build and validate empirically via the benchmark scenario set, not as an established literature.
- **RFP scoring weight percentages are directional only**, aggregated from vendor-blog content, not a standards body — do not encode literal percentages as rules.
- **No public "MEDDICC-for-written-documents" precedent exists** — the completeness-checklist translation is original synthesis; validate with actual presales practitioners during requirements/planning rather than treating as settled convention.
- **MEDDICC/MEDDIC trademark status beyond the "MEDDPICC ruled generic" ruling is unresolved** — do not assume the whole acronym family is safe by extension; get current legal confirmation before publishing, especially before Phase 6.
- **claude.ai upload description-length limit (200 vs. 1024 chars)** is an unreconciled discrepancy between two official-ish sources — write ≤200 chars to be safe, confirm with a manual smoke test before shipping.
- **The exact list of Agent-Skills-standard-compatible harnesses (claimed 78+)** is aggregated from a non-canonical source; only Claude Code, Cursor, Codex, Copilot, Gemini CLI, OpenCode, and Goose are independently cross-confirmed — do not overstate compatibility claims in marketing copy.

## Sources

### Primary (HIGH confidence)
- agentskills.io/specification — Agent Skills frontmatter schema, progressive disclosure token/line budget
- code.claude.com/docs/en/{plugin-marketplaces, output-styles, headless, cli-reference, skills} — plugin manifest schema, output-style format, headless CLI flags
- Direct inspection of the local SimpleEnglish reference repo (`AminBlg/SimpleEnglish` v1.3.0) — repo layout, eval harness shape, linter docstring conventions, trademark posture, all read in full
- meddicc.com, forcemanagement.com, challengerinc.com — official framework sources (definitional content, not proprietary training material)
- ACL Anthology / arXiv position-bias and self-preference-bias papers — LLM-as-judge failure mode measurements
- IPWatchdog / meddicc.com / PR Newswire reporting on the E.D. Pa. MEDDPICC genericness ruling (Civil Action No. 24-1836, April 2026)

### Secondary (MEDIUM confidence)
- Cross-checked secondary breakdowns of Command of the Message, MEDDICC, and Challenger (Qwilr, Fullcast, Oliv.ai, Zapier, HubSpot, Anaplan PDF, Forbes, pitchmonster)
- hesreallyhim/claude-code-json-schema — long tail of optional plugin manifest fields
- Legal-practice sources on RFP contractual exposure, comparative-advertising law, "shall/will/should" contract-formation language

### Tertiary (LOW confidence)
- General AI-slop/business-writing content (Merritt Group, Spike AI, seo.com) — thin, general-purpose, not presales-specific
- RFP scoring weight bands (Inventive.ai, RocketDocs) — vendor/consultancy blog aggregates, directional only
- `textstat` maintenance activity — search-synthesis, not directly verified against PyPI

---
*Research completed: 2026-09-10*
*Ready for roadmap: yes*
