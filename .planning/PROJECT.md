# Proof First

## What This Is

Proof First is a public, MIT-licensed agent skill that makes AI write technical presales documents a buyer will actually believe. It covers RFP/RFI responses, solution proposals, executive summaries, and demo/discovery material — writing that has to be commercially persuasive without reading like a brochure or an LLM.

It occupies the territory that [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) explicitly refuses. That skill's closing section says STE "deletes persuasion by design" and sends marketing writing away. Proof First is the sibling that takes those documents and makes them persuasive the only way that survives a technical evaluator: through specificity and evidence instead of adjectives.

It is for presales engineers, solution architects, and bid teams — vendor-neutral, usable by anyone, distributed the same way SimpleEnglish is (skills CLI, Claude Code plugin marketplace, output style, and a paste-able system prompt).

## Core Value

**A technical evaluator finishes the document believing the author genuinely understands their problem — because complex things were made simple without being made wrong.**

Everything yields to this. Simplification that costs technical accuracy fails. Accuracy that the reader cannot follow fails. Persuasion that a competent engineer can smell as marketing fails hardest of all, because it destroys the trust the rest of the document was spending.

The secondary job, downstream of trust: make the decision easy — remove the buyer's reasons to hesitate about risk, cost, effort, and whether the vendor can actually do it.

## Business Context

- **Customer**: Presales engineers, solution architects, and bid teams writing customer-facing technical documents. Free and public.
- **Revenue model**: None. Open source, MIT. The return is reputation and adoption, in the way SimpleEnglish's return is.
- **Success metric**: Measured reduction in violations per 100 words, skill-on versus skill-off, across multiple models — the same evidence standard the skill itself demands of its users.
- **Strategy notes**: Distribution mirrors SimpleEnglish because that path is proven for this artifact class: one folder, no dependencies, Agent Skills standard, plugin marketplace, and a README that leads with before/after pairs.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] A numbered, self-contained rule catalog for presales writing, structured on Command of the Message
- [ ] The deletion test as the buzzword rule — no maintained blocklist governs the skill itself
- [ ] An integrity section that refuses to fabricate metrics, references, benchmarks, or certifications
- [ ] A MEDDICC-derived completeness audit, kept separate from the prose rules
- [ ] The Challenger opening rule: reframe the customer's problem before listing capabilities
- [ ] Self-contained prose mechanics tuned for presales — no dependency on simple-english
- [ ] Per-artifact patterns for RFP/RFI responses, solution proposals, executive summaries, demo and discovery material
- [ ] Both write mode and check mode (report violations with rule number, offending text, compliant rewrite)
- [ ] A deterministic linter that counts observable proxies for the rules
- [ ] A multi-model baseline-versus-skill benchmark with published, reproducible results
- [ ] A blind pairwise judge run to measure quality, not just violation counts
- [ ] Public repo scaffolding: README with before/after pairs, plugin manifests, output style, system prompt, MIT license
- [ ] All worked examples running on one fictional cloud migration deal

### Out of Scope

- **Slide decks and visual design** — this is a text skill; deck structure is a different problem with different tooling
- **Pricing calculation, sizing, or commercial modelling** — the skill writes about numbers, it does not produce them
- **CRM, proposal-automation, or bid-management integration** — one folder, no dependencies, matching SimpleEnglish's distribution model
- **Reproducing proprietary framework material** — concepts are paraphrased; no Force Management, Challenger Inc., or MEDDIC training content is copied
- **Verifying that the writer's inputs are true** — the skill refuses to invent facts and marks gaps, but it cannot fact-check what it is given
- **Marketing copy, brand writing, launch posts** — the same boundary SimpleEnglish draws, drawn from the other side

## Context

**The parent project.** SimpleEnglish (AminBlg/SimpleEnglish, v1.3.0, MIT) grounds itself in ASD-STE100 Simplified Technical English — 53 numbered rules across 9 sections, paraphrased with software examples, reproducing zero spec or dictionary text. Its structure is: `SKILL.md` (rule catalog, two modes, self-check), plus three references (`checklist.md` for the audit pass, `word-swaps.md` for slop substitutions, `use-cases.md` for per-artifact adaptations). Around it sits a README built on before/after pairs, a plugin marketplace manifest, an output style, a paste-able system prompt, and `evals/` with a deterministic regex linter (`ste_lint.py`), a scenario set (`scenarios.json`), and benchmark runners. Its headline claim is 74.6% fewer violations per 100 words across 7 models and 8 tasks, plus a blind pairwise judge preferring skill output in 45 of 56 pairs.

**Why the anchor problem is different here.** SimpleEnglish's authority is borrowed from an external, maintained, numbered standard — "it is not vibes." Presales writing has no ASD-STE100. The decision taken during questioning is to anchor in three established commercial frameworks, each with a distinct job rather than blended into one catalog:

- **Command of the Message is the rule spine.** It is the only one of the three that is about articulation rather than qualification or conversation. Its elements — Before scenario, After scenario, Required Capabilities, Metrics, Proof Points, Differentiators — map close to 1:1 onto the sections of a proposal, which makes them writable and checkable.
- **MEDDICC is the completeness audit, not the prose rules.** It is a qualification framework; making it govern sentences would be a category error. As a checklist it is excellent: does this document name a metric, speak to the economic buyer, mirror their stated decision criteria, respect the paper process, arm the champion for a meeting the author will not attend? A document can be well written and fail every one of those.
- **Challenger contributes one rule, and it is the opening.** Lead with a reframe of the customer's problem, not a list of capabilities. That is roughly its whole useful contribution to a writing skill, and it is the highest-leverage structural rule for an executive summary.

This mirrors SimpleEnglish's own three-part shape: rule catalog, checklist, use-cases.

**The buzzword line is the hardest design problem.** Some cloud terms are technical nouns doing real work — landing zone, zero trust, VPC Service Controls, FinOps. Some are pure air — synergy, best-of-breed, next-generation, holistic. A blocklist gets this wrong in both directions and needs endless maintenance. The chosen rule is a **deletion test**: a term is legal if deleting it changes the technical meaning, and a buzzword if the sentence survives deletion intact. This mirrors SimpleEnglish's "if the word carries no fact, delete it," and it is one rule with no vocabulary to maintain.

**Known consequence of that choice.** The deletion test is a semantic judgment, so a regex linter cannot check it directly. This is not a contradiction; it is the same split SimpleEnglish lives with. Its own linter docstring states plainly that it is "a regex pass, not a grammar parser," that it "undercounts," and that its numbers "are not a compliance verdict." Proof First takes the same position: the SKILL.md teaches the deletion test as *the rule*, and the linter counts observable proxies — unquantified superlatives, claims with no adjacent number, hedges, sentence length, passive voice. The linter measures correlates for benchmarking. It is not the standard.

**Why integrity is a first-class section.** A presales writing assistant is under constant pressure to invent proof — a plausible metric, a reference customer, a benchmark number, a certification. Every one of those is a trust-destroying event if a buyer checks it, and models produce them readily because they are exactly what the surrounding text implies. Making refusal explicit turns the honest path into the default, and it is a genuine differentiator for a commercial writing skill.

## Constraints

- **Legal**: All three anchor frameworks are proprietary and trademarked (Force Management, Challenger Inc., and the MEDDIC training vendors). Adopt the SimpleEnglish posture exactly — name them, paraphrase concepts only, reproduce zero proprietary text, state non-affiliation and trademark ownership explicitly, MIT license the repo.
- **Dependencies**: Zero. One folder, no install step, no dependency on simple-english even though it is the sibling skill. The prose mechanics must be restated self-contained.
- **Compatibility**: Agent Skills standard, so it works across Claude Code, Cursor, Codex, Copilot, Gemini CLI, OpenCode and the rest. Plus a paste-able system prompt for harnesses with no skill support.
- **Evidence**: The repo makes measured claims or no claims. Any headline number must be reproducible from a committed script, with honest caveats stated — the same standard the skill demands of its users. Anything less would be the exact failure the skill exists to prevent.
- **Voice**: The skill must stay commercially attractive while banning buzzwords. Flat, STE-style prose is a failure mode here, not a goal — persuasion has to survive.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Name it Proof First | States the operative rule in the name: no claim ships without evidence attached. Reads as a discipline rather than a genre. | — Pending |
| Anchor in sales methodology rather than inventing rules | Borrowed authority from frameworks practitioners already respect, matching how SimpleEnglish borrows from ASD-STE100 | — Pending |
| Three frameworks, three distinct jobs | Command of the Message governs articulation, MEDDICC audits completeness, Challenger sets the opening. Blending them would produce a mushy catalog. | — Pending |
| Deletion test over blocklist | One rule, no vocabulary to maintain, and it keeps real technical nouns legal while killing air | — Pending |
| Fully self-contained prose mechanics | Zero dependency on simple-english; a second required install would kill adoption | — Pending |
| Integrity as its own catalog section | Fabricated proof is the highest-cost failure in presales and the one models produce most readily | — Pending |
| Full eval harness in v1 | Measured benchmarks are what separate this from a prompt repo, and the repo cannot demand evidence it does not itself provide | — Pending |
| One fictional cloud migration deal for all examples | Keeps the repo vendor-neutral and the examples mutually reinforcing, exactly as sqlpipe does for SimpleEnglish | — Pending |
| SimpleEnglish trademark posture | Proven approach to the same legal problem, applied to three rights-holders instead of one | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-09-10 after initialization*
