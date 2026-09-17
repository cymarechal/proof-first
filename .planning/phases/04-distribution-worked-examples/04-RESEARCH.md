# Phase 4: Distribution & Worked Examples - Research

**Researched:** 2026-09-17
**Domain:** Shipping an already-complete, near-token-ceiling Agent Skill (`skills/proof-first/SKILL.md`, 308 lines / 3,710 words / ~4,823 estimated tokens, 177-token margin) through the four distribution channels the project promises (skills CLI, Claude Code plugin marketplace, output style, paste-able system prompt), plus family-level worked before/after examples and a rewritten claim-free README. No new runtime code paradigm: new Markdown/JSON artifact files, a new stdlib-only generator script, and `tools/check_repo.py` extensions — the same shape every prior phase used.
**Confidence:** HIGH for everything read directly this session (repo files, the SimpleEnglish reference implementation on disk, `tools/check_repo.py`'s live-run baseline, official Claude Code docs fetched directly). MEDIUM for the two genuinely novel design decisions this phase must make that no precedent in this repo or in SimpleEnglish resolves (the DIST-05 sync mechanism, and what "equivalent behavior" can honestly mean for a skill this much larger than SimpleEnglish's). LOW/flagged wherever the research surfaces a real open question (the repo's own GitHub owner/repo string, which does not exist yet — no git remote is configured).

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EX-02 | Before/after pairs covering each artifact family, citing real rule numbers | Q4 below — the four frozen family names and all 39 citable IDs are enumerated; recommends `examples/before-after.md`, already anticipated in README's own target tree, plus two new checker codes |
| DIST-01 | Install via the skills CLI with one command | Q6 below — exact verified command from the `vercel-labs/skills` README, cross-checked against the real SimpleEnglish README's own usage |
| DIST-02 | Install as a Claude Code plugin from a marketplace manifest in this repo | Q1/Q6 below — exact schema fetched from official docs, cross-checked against the real, working SimpleEnglish `.claude-plugin/plugin.json` and `marketplace.json` read directly this session |
| DIST-03 | Turn the discipline on permanently as a Claude Code output style | Q1/Q3 below — schema is prior research in `./.claude/CLAUDE.md`; this research adds the concrete content-scope problem specific to this skill's much larger reference-file footprint |
| DIST-04 | Paste a system-prompt version in a harness with no skill support | Q3 below — same content-scope problem, sized precisely against this skill's real word counts |
| DIST-05 | Derivative artifacts regenerated from SKILL.md whenever it changes, documented re-sync step | Q2 below — the hard question; SimpleEnglish has **no** mechanism for this at all (verified by direct inspection), so this phase must build something genuinely new |
| DIST-06 | README leads with before/after pairs, states an install path per harness | Q7 below — exact claims-discipline boundary stated, given README already carries the committed MOD-04 figure and the `readme-results-pointer-missing` gate that must not regress |

</phase_requirements>

## Summary

This phase inherits a skill that is functionally complete and content-frozen at 308 lines / 3,710 words / an estimated 4,823 tokens against `check_skill_token_budget`'s 5,000-token ceiling — a margin of 177 estimated tokens `[VERIFIED: wc -l -w -c skills/proof-first/SKILL.md, run this session: "308 3710 23174"]`. Unlike Phase 3, this phase does not need to add rule content to `SKILL.md`, so this tight margin is a background constraint (any incidental edit must be re-measured), not the load-bearing risk it was for Phase 3. The load-bearing risk here is different and new: **this skill has five reference files totaling 6,192 words on top of SKILL.md's 3,710** `[VERIFIED: wc -w skills/proof-first/references/*.md, run this session: artifact-patterns.md 1378, checklist.md 588, completeness-audit.md 1484, deletion-test.md 876, worked-examples.md 1316; sum 4642 excluding worked-examples' overlap with SKILL.md's own catalog — see Q3]`. SimpleEnglish, the reference implementation this project's own `PROJECT.md` and `CLAUDE.md` are explicitly modeled on, has **no reference files at all in its main SKILL.md's progressive-disclosure sense** beyond three small files (`checklist.md`, `word-swaps.md`, `use-cases.md`) and a single 3,664-word `SKILL.md` `[VERIFIED: wc -l -w ~/devoteam/.claude/plugins/marketplaces/simple-english/skills/simple-english/SKILL.md, run this session: "329 3664"]`. Proof First's rule catalog is comparably sized to SimpleEnglish's own core file, but Proof First carries roughly 60% more total instructional content once its reference files are counted, split across five files instead of three. This directly affects how big a faithful, no-skill-support system prompt or output style must be to honestly claim it delivers "the same behavior" (DIST-03/04) — a problem SimpleEnglish's own repo does not have to the same degree and did not have to solve rigorously (see Q2/Q3).

The second load-bearing finding: **direct inspection of the real, working SimpleEnglish repository on disk (`~/devoteam/.claude/plugins/marketplaces/simple-english/`) shows it has built no mechanism at all for DIST-05.** `output-styles/simple-english.md` (361 words) and `prompts/system-prompt.md` (467 words) are both hand-written, independently-worded condensations of the 3,664-word `SKILL.md` — there is no generator script anywhere in the repo, no version stamp, no content hash, and no documented re-sync step in the README `[VERIFIED: find ~/devoteam/.claude/plugins/marketplaces/simple-english -iname "*generat*" -o -iname "*sync*", run this session — zero results; README.md and SKILL.md grepped for "regenerat|re-sync|resync|generate", run this session — zero relevant matches]`. This means Proof First's DIST-05 requirement is not "do what SimpleEnglish does" — it is new engineering scope this research must design from scratch, using this project's own already-established idioms (a stdlib-only generator in `tools/`, a stated-value-vs-registry drift check in `check_repo.py`, exactly the shape Phase 2/3 already used for the PF/MC catalog counts).

**Primary recommendation:** Treat this phase as four small, mostly-independent tracks. Track A (worked examples, EX-02): a new `examples/before-after.md` carrying one full before/after pair per artifact family, each after-column citing at least one of the 39 real allocated IDs, gated by two new checker codes mirroring `artifact-family-section-missing`'s shape. Track B (plugin scaffolding, DIST-01/02): `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, both hand-written JSON with `source: "./"`, mirroring the real, working SimpleEnglish manifests field-for-field, plus a new checker code enforcing NUMBERING.md's own already-stated rule that the plugin manifest's version matches SKILL.md's frontmatter version. Track C (derivatives, DIST-03/04/05 — the hard one): a new stdlib-only `tools/generate_derivatives.py` that mechanically emits `output-styles/proof-first.md` and `prompts/system-prompt.md` from SKILL.md plus its reference files, each derivative stamped with a content hash of its inputs, checked for staleness by a new `check_repo.py` code — never hand-maintained prose that can silently drift. Track D (README, DIST-06): rewrite lead-in and Install sections only, preserving the existing Status/measured-figure sections and the `readme-results-pointer-missing` gate untouched. Sequence Track B and the plugin-version check first (cheapest, fully precedented), then Track A, then Track C last (it depends on nothing else being done, but is the most novel and should not block the cheaper wins if time runs short) — Track D closes the phase once A-C exist to point at.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Skill content (rule catalog, reference files) | Content Layer (`skills/proof-first/`, frozen by Phases 2-3) | — | Phase 4 reads this content, never edits its rule bodies — DIST-03/04/05 are about *derivation*, not new rules |
| Plugin distribution manifest | Distribution Layer (`.claude-plugin/*.json`, new) | Enforcement Layer (`tools/check_repo.py`, new version-match check) | A hand-written, harness-specific manifest format distinct from the Agent Skills spec itself; NUMBERING.md already anticipates a version-matching obligation between the skill's frontmatter and "the plugin manifest" |
| Output style / system prompt derivatives | Distribution Layer (`output-styles/`, `prompts/`, new, generated) | Tooling Layer (`tools/generate_derivatives.py`, new) + Enforcement Layer (staleness check) | These are compiled artifacts of SKILL.md + references, not independently authored content — the generator is the single source of truth for how they are produced, mirroring the project's existing "one grammar, one validation path" discipline (Phase 3's `_three_way_id_diff` helper) |
| Worked before/after examples per artifact family | Content Layer (`examples/before-after.md`, new) | Enforcement Layer (two new checker codes: family-heading presence, citation presence) | Distinct from `references/worked-examples.md`'s per-rule pairs (Phase 2/3 content); this is a new, family-level example set EX-02 specifically asks for |
| README | Distribution Layer (top-level entry point) | Enforcement Layer (existing `readme-results-pointer-missing`, unchanged) | Must lead with before/after pairs and install paths per DIST-06, while never regressing the existing measured-figure disclosure Phase 3 already gated |

## Package Legitimacy Audit

This phase's only external-facing dependency is the `skills` npm package, invoked transiently via `npx` in a documented README command — **no package is added to this repository's own dependency tree** (the project remains zero-dependency; `npx` does not modify any committed manifest).

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|--------------|---------|-------------|
| `skills` | npm | Actively maintained, current version `1.6.0` `[VERIFIED: npm view skills version, run this session]` | Not independently checked this session (see below) | `github.com/vercel-labs/skills` `[VERIFIED: npm view skills repository.url, run this session: "git+https://github.com/vercel-labs/skills.git"]` | OK | Approved |

**Legitimacy note:** the package name `skills` was already a locked stack decision in `./.claude/CLAUDE.md` before this research session (the CLAUDE.md STACK section names `vercel-labs/skills` and its `npx skills` CLI explicitly, citing `https://github.com/vercel-labs/skills` as a fetched, HIGH-confidence source). This research independently re-confirmed the package's existence, current version, and repository URL against the live npm registry this session `[VERIFIED: npm registry, npm view skills description, run this session: "The open agent skills ecosystem"]`, and cross-checked its exact invocation syntax against a live web fetch of its own README (see Q6). Per this project's own provenance rule, the package **name** itself was originally surfaced via the CLAUDE.md's own prior WebSearch-and-fetch research (not independently re-discovered from scratch this session), so it is tagged `[CITED: CLAUDE.md STACK section, itself citing https://github.com/vercel-labs/skills]` for provenance purposes even though its registry existence and current version are freshly `[VERIFIED]` this session. **Packages removed due to `[SLOP]` verdict:** none. **Packages flagged as suspicious `[SUS]`:** none.

**No new package will ever appear in this repository's own `package.json`, `requirements.txt`, or equivalent** — there is no such file in this repo and this phase does not introduce one. `tools/generate_derivatives.py` (recommended below) must be stdlib-only Python, exactly like `tools/check_repo.py` and `evals/conformance/run_conformance.py`.

## Project Constraints (from CLAUDE.md)

`./.claude/CLAUDE.md` (reproduced in this agent's system context) carries repo-wide directives binding this phase, all cross-checked against this session's own findings:

- **Zero dependencies. Stdlib Python 3 only.** Any new tooling this phase adds (a derivative generator, new checker codes) must import only the standard library, exactly like `tools/check_repo.py`'s own stated posture (`tools/check_repo.py:8-9`, read this session).
- **Agent Skills standard is the distribution backbone.** `SKILL.md` + `references/` is untouched by this phase's rule content; the four distribution channels wrap around it, they do not modify it.
- **`.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`, current schema, additive/backward-compatible.** This session fetched the current official schema directly (Q1) and cross-checked it against the real, working SimpleEnglish manifests (also read directly this session) — both agree.
- **`output-styles/*.md`, Claude Code v2.1+ format.** `keep-coding-instructions` and `force-for-plugin` are documented fields; CLAUDE.md itself already states Proof First "likely wants neither `true`" since it is a writing persona, not a coding-instruction layer, and users should opt in — this research finds no reason to revisit that framing (see Q1).
- **A second, harness-agnostic CLI for cross-provider benchmarking (Pi/OpenCode/Claude Agent SDK)** — out of scope for this phase; belongs to Phase 5.
- **Evidence: measured claims or no claims.** README must not assert "equivalent behavior" as a measured fact (see Q3/Q7) — this is the single most consequential constraint this phase must respect.
- **GSD workflow enforcement.** File-changing tool calls happen through a GSD command, not ad hoc.
- **Every check_repo.py check must be proven live by mutation test.** Any new check this phase's plan adds must ship with a self-test fixture pair and a `MUTATIONS` entry, following the exact D-34 three-part contract Phase 1-3 already established (self-test fixture, live-repo mutation, discrimination proof) — the baseline this phase must not regress is **32 codes discrimination-proven, 0 unexpected control violations** `[VERIFIED: python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py, run this session — "self-test PASS", "mutation-test PASS: 32 codes discrimination-proven", "check_repo: 0 violations"]`.
- **No emojis** in shipped content unless explicitly requested.

## Standard Stack

### Core

| Component | Version/Spec | Purpose | Why Standard |
|---|---|---|---|
| Python 3 standard library only (`re`, `json`, `hashlib`, `argparse`, `pathlib`) | 3.13.13 confirmed present `[VERIFIED: python3 --version, run this session]` | `tools/generate_derivatives.py` (new) and `tools/check_repo.py` extensions | Matches this project's zero-dependency posture exactly; `hashlib` (stdlib) is the one new stdlib module this phase needs beyond what Phase 1-3 already imported, for the DIST-05 content-hash mechanism |
| Agent Skills frontmatter schema | Current spec, unchanged since Phase 2's research | `SKILL.md`'s frontmatter (`name`, `description`, `license`, `metadata.version: "0.1.0"`) is read, never edited, by this phase's tooling | Already locked; Phase 4 only reads `metadata.version` as an input to the plugin-version-match check |
| Claude Code plugin manifest schema (`plugin.json`/`marketplace.json`) | Current, additive/backward-compatible, no version pin `[CITED: https://code.claude.com/docs/en/plugin-marketplaces, fetched directly this session]` | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (new) | Official schema; this session fetched it directly and cross-checked field-for-field against the real, working SimpleEnglish manifests (also read directly) — see Q1 |
| `vercel-labs/skills` CLI (invoked via `npx skills ...`, no local install) | `1.6.0` on npm as of this session `[VERIFIED: npm view skills version, run this session]` | DIST-01's one-command install path | Already a locked stack decision in `./.claude/CLAUDE.md`; this session re-confirmed registry existence/version and fetched exact command syntax (Q6) |
| `git` | 2.54.0 confirmed present `[VERIFIED: git --version, run this session]` | Commit, phase workflow | Standard |
| Claude Code CLI | `2.1.236` confirmed present `[VERIFIED: claude --version, run this session]` | Manual smoke-testing the plugin/output-style install paths (see Validation Architecture) | `./.claude/CLAUDE.md`'s own Version Compatibility table notes `--permission-prompts none` needs v2.1.259+; this environment's `2.1.236` is below that floor — irrelevant to this phase (no scripted permission-prompt handling is needed for a manual smoke test) but worth recording |

### Supporting

None. This phase adds no new package to any ecosystem; `npx skills` is invoked by end users from README instructions, never by this repository's own tooling.

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| A generator script that mechanically produces `output-styles/proof-first.md` and `prompts/system-prompt.md` from SKILL.md + references | Hand-maintaining both derivatives independently, exactly as SimpleEnglish does | SimpleEnglish's own repo demonstrates the cost of this choice: zero drift protection, no way to know if the hand-written condensation still matches the source after an edit. This project's own DIST-05 requirement explicitly asks for more than SimpleEnglish delivers, so the hand-maintained path does not satisfy the requirement as written, only a superficially similar one |
| A content-hash drift check (`hashlib.sha256`) recorded in each derivative's header | A stated-version-number check (mirroring `catalog-count-mismatch`'s "stated N vs registry N" pattern, using SKILL.md's `metadata.version` field) | A hash is precise (catches every byte-level change) but requires no separate contributor discipline; a version-number check is simpler to read but only as good as contributors remembering to bump `metadata.version` on every substantive edit, which nothing today enforces. Recommend the hash for the derivative-staleness check specifically (Q2), and *additionally* enforce the already-existing NUMBERING.md obligation that the plugin manifest's version tracks SKILL.md's version (a separate, complementary check, not a substitute) |
| A single reference file for both artifact-family before/after pairs and the existing per-rule worked pairs | Reusing `references/worked-examples.md` for the new family-level pairs | `references/worked-examples.md`'s own header states its scope precisely: "the worked ✗/✓ contrast for each catalog rule that has one," keyed by rule ID `[VERIFIED: skills/proof-first/references/worked-examples.md:1-7, read this session, quoted verbatim: "This file carries the worked ✗/✓ contrast for each catalog rule that has one... this file supplies the contrast only, keyed by the ID of the rule it belongs to."]`. EX-02 asks for family-level pairs, a different unit of organization; blending the two would violate the file's own stated scope and the project's established "each new organizing concept gets its own file" discipline (mirrored by AUD-02's completeness-audit/prose-rule separation) |

**Installation:** None — no `npm install`/`pip install` for this repository's own tree. End users run `npx skills add ...` per README (see Q6).

## Architecture Patterns

### System Architecture Diagram

```
                     SKILL.md + references/*.md
                     (frozen content, Phases 2-3)
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
          ▼                   ▼                    ▼
   ┌─────────────┐   ┌────────────────────┐  ┌──────────────────┐
   │ .claude-     │   │ tools/generate_    │  │ examples/         │
   │ plugin/      │   │ derivatives.py     │  │ before-after.md   │  ← NEW, Track A
   │ plugin.json  │   │ (NEW, stdlib-only) │  │ (family-level     │    (EX-02)
   │ marketplace  │   │                    │  │ pairs, real IDs)  │
   │ .json        │   │ reads SKILL.md +   │  └─────────┬─────────┘
   │ (NEW)        │   │ references/, hashes│            │
   └──────┬───────┘   │ the input, writes: │            ▼
          │            │                    │   ┌──────────────────┐
   Track B│            ▼                    │   │ check_repo.py:    │
   (DIST- │   ┌──────────────────┐          │   │ before-after-      │
   01/02) │   │ output-styles/    │◄─────────┘   │ family-missing     │
          │   │ proof-first.md    │              │ before-after-       │
          │   │ (NEW, generated,  │              │ citation-missing    │
          │   │  hash-stamped)    │              │ (NEW codes)          │
          │   └──────────────────┘              └──────────────────────┘
          │            │
          │            ▼
          │   ┌──────────────────┐
          │   │ prompts/          │
          │   │ system-prompt.md   │
   Track C│   │ (NEW, generated,  │
   (DIST- │   │  hash-stamped)    │
   03/04/ │   └──────────────────┘
   05)    │            │
          │            ▼
          │   ┌───────────────────────────┐
          │   │ check_repo.py:             │
          │   │ skill-derivative-stale     │  ← recomputes hash of
          │   │ (NEW code, compares        │    SKILL.md + references/,
          │   │  recorded vs live hash)    │    compares to each
          │   └───────────────────────────┘    derivative's stamp
          │
          ▼
   ┌──────────────────┐
   │ check_repo.py:     │
   │ plugin-version-    │  ← enforces NUMBERING.md's own
   │ mismatch (NEW)     │    already-stated rule: plugin
   └──────────────────┘    manifest version == SKILL.md
                            frontmatter metadata.version

                              │
                              ▼
                     ┌──────────────────┐
                     │ README.md         │  ← Track D (DIST-06), last:
                     │ rewritten lead-in │    leads with before/after
                     │ + Install section │    pairs, states install path
                     │ (existing Status/ │    per harness; existing
                     │ measured-figure   │    readme-results-pointer-
                     │ sections kept)    │    missing gate untouched
                     └──────────────────┘
```

### Recommended Project Structure

```
.claude-plugin/
├── plugin.json                          # NEW — Track B
└── marketplace.json                      # NEW — Track B
output-styles/
└── proof-first.md                        # NEW — generated, Track C
prompts/
└── system-prompt.md                      # NEW — generated, Track C
examples/
├── deal-brief.md                         # unchanged
└── before-after.md                       # NEW — Track A (EX-02)
tools/
├── check_repo.py                         # EXTENDED — 4-5 new codes
└── generate_derivatives.py               # NEW — Track C generator
README.md                                 # REWRITTEN lead-in + Install — Track D
```

This exact tree is already anticipated by README.md's own "target layout" diagram, written in Phase 1/2/3 and never contradicted since `[VERIFIED: README.md:80-116, quoted verbatim: "output-styles/\n│   └── proof-first.md                  (planned)\n├── prompts/\n│   └── system-prompt.md                (planned)\n├── examples/\n│   ├── deal-brief.md                   (exists)\n│   └── before-after.md                 (planned)\n... ├── .claude-plugin/                     (planned)"]`. This phase turns five "(planned)" entries into "(exists)."

### Pattern 1: The Real Working Reference — SimpleEnglish's Actual Manifests, Read Directly, Not Recalled

`[VERIFIED: cat ~/devoteam/.claude/plugins/marketplaces/simple-english/.claude-plugin/plugin.json, run this session, quoted verbatim]`:
```json
{
  "name": "simple-english",
  "displayName": "Simple English",
  "description": "Write or rewrite technical text with ASD-STE100 Simplified Technical English: short sentences, one word one meaning, active voice, condition before command.",
  "version": "1.3.0",
  "author": { "name": "AminBlg" },
  "homepage": "https://github.com/AminBlg/SimpleEnglish",
  "repository": "https://github.com/AminBlg/SimpleEnglish",
  "license": "MIT",
  "keywords": ["technical-writing", "documentation", "ste", "asd-ste100"]
}
```

`[VERIFIED: cat ~/devoteam/.claude/plugins/marketplaces/simple-english/.claude-plugin/marketplace.json, run this session, quoted verbatim]`:
```json
{
  "name": "simple-english",
  "owner": { "name": "AminBlg", "url": "https://github.com/AminBlg" },
  "description": "ASD-STE100 Simplified Technical English skill for clear, unambiguous technical writing.",
  "plugins": [
    {
      "name": "simple-english",
      "source": "./",
      "displayName": "Simple English",
      "description": "Write or rewrite technical text with ASD-STE100 Simplified Technical English: short sentences, one word one meaning, active voice, condition before command.",
      "version": "1.3.0",
      "author": { "name": "AminBlg" },
      "homepage": "https://github.com/AminBlg/SimpleEnglish",
      "repository": "https://github.com/AminBlg/SimpleEnglish",
      "license": "MIT",
      "keywords": ["technical-writing", "documentation", "ste", "asd-ste100"]
    }
  ]
}
```

Both are hand-written JSON at the repository root under `.claude-plugin/`. Note `source: "./"` — the plugin's root **is the repository root itself**, not a subdirectory; Claude Code auto-discovers `skills/*/`, `output-styles/*.md`, and (if present) `commands/`, `agents/`, `hooks/` beneath whatever directory `source` points to, with no explicit `skills`/`output-styles` field needed in either manifest `[CITED: https://code.claude.com/docs/en/plugin-marketplaces, fetched directly this session — "skills, commands, agents, hooks, mcpServers, lspServers - Component configuration" listed as optional overrides, implying default auto-discovery from the plugin root's conventional folders]`.

**Recommendation for Proof First:** mirror this shape exactly. `name: "proof-first"` in both files (matching the skill folder name, though the plugin manifest's `name` key is a separate namespace from the Agent Skills `name` field and is not enforced to match by any existing check), `source: "./"` in the marketplace entry, `version` set to whatever `skills/proof-first/SKILL.md`'s frontmatter `metadata.version` currently states (`"0.1.0"` as of this session `[VERIFIED: skills/proof-first/SKILL.md:13, read this session: 'version: "0.1.0"']`).

### Pattern 2: NUMBERING.md Already Anticipates a Version-Match Obligation — This Is Not a New Decision

`[VERIFIED: NUMBERING.md:143-149, quoted verbatim]`:
> "Semantic versioning is carried in the skill's frontmatter `metadata` and in the plugin manifest, matched by a git tag."

This sentence was written in Phase 1, before any plugin manifest existed. It is a frozen, already-locked obligation this phase must satisfy, not a new design choice: `skills/proof-first/SKILL.md`'s frontmatter `metadata.version` and `.claude-plugin/plugin.json`'s (and `marketplace.json`'s plugin-entry) `version` field must agree, and both should be matched by a git tag at release. **Recommendation:** a new `check_repo.py` code, `plugin-manifest-version-mismatch`, comparing `SKILL.md`'s frontmatter `metadata.version` (already parsed by the existing `parse_frontmatter()`, which keeps nested-map values as opaque strings — the `metadata:` block's `version:` sub-key will need a small, targeted extraction, not a general YAML parser, matching this file's own established D-33 discipline) against `plugin.json`'s and `marketplace.json`'s `version` fields (parsed with stdlib `json.loads`, since these are genuine JSON files, unlike the hand-rolled Markdown-adjacent frontmatter parser). Fires once per mismatched file, naming both values.

### Pattern 3: The Content-Scope Problem — Why "Equivalent Behavior" Is Materially Harder for Proof First Than for SimpleEnglish

**What SimpleEnglish actually ships as its derivatives, measured directly this session:**

| File | Words | Relationship to SKILL.md |
|---|---|---|
| `skills/simple-english/SKILL.md` | 3,664 `[VERIFIED: wc -l -w, run this session]` | Source |
| `output-styles/simple-english.md` | 361 `[VERIFIED: wc -w, run this session]` | ~10% of SKILL.md's length — a heavily condensed persona restatement |
| `prompts/system-prompt.md` | 467 `[VERIFIED: wc -w, run this session]` | ~13% of SKILL.md's length, plus a documented "~60-token" ultra-condensed variant at the file's own end |

SimpleEnglish's SKILL.md has **no reference files it depends on for correct behavior** beyond `checklist.md` (an ID index, analogous to Proof First's own `checklist.md`), `word-swaps.md`, and `use-cases.md` — none of which carry rule bodies the skill's core behavior depends on to function; the rule catalog itself is fully self-contained in the one 3,664-word file. This is why a ~360-word condensation can plausibly claim to capture "the same rules" — the source itself is small and self-contained.

**Proof First's SKILL.md is not self-contained in the same way.** Two of its own instructions explicitly require reading a reference file to perform a rule correctly:
`[VERIFIED: skills/proof-first/SKILL.md:47-51, quoted verbatim]`:
> "Before applying the deletion test to a compound term, or to any term appearing in the customer's own supplied source material, read `references/deletion-test.md`.
> Before emitting any rule citation in check mode, read `references/checklist.md`.
> Before writing or checking a ✗/✓ contrast for a rule, read `references/worked-examples.md`.
> Before running a document-level completeness audit, or before reporting a completeness gap in check mode, read `references/completeness-audit.md`.
> Before classifying a document into an artifact family, or before applying that family's conventions, read `references/artifact-patterns.md`."

Every one of these reference files carries content this project's own architecture explicitly refuses to duplicate into SKILL.md (AUD-02: "never blended into the prose rules"; Phase 3's own token-budget finding: there was no room left to inline them even if the project wanted to). Measured this session: `completeness-audit.md` (1,484 words, the 8 MC dimensions), `artifact-patterns.md` (1,378 words, the 4 artifact families), `deletion-test.md` (876 words, edge cases), `checklist.md` (588 words, the ID index) — **4,326 words of instructional content that a genuinely faithful system prompt or output style cannot honestly omit**, on top of SKILL.md's own 3,710. (`worked-examples.md`, 1,316 words, is example material rather than instruction and is the one file this research recommends treating as optional/abridged in a condensed derivative — see below.)

**Why this matters concretely for DIST-03/04:** a derivative that inlines only SKILL.md's own body (as SimpleEnglish's condensations do, because that is all their source needs) would silently drop the completeness audit's 8 dimensions and all 4 artifact-family conventions — a materially different, less capable tool, not "the same behavior." **Recommendation:** the system prompt (DIST-04, pasted into contexts with generous length budgets — a system prompt field, `AGENTS.md`, `.cursorrules`) should inline SKILL.md's full body plus `deletion-test.md`, `completeness-audit.md`, and `artifact-patterns.md` in full — an estimated ~7,450 words (SKILL.md's 3,710 + those three files' combined 3,738), roughly ~9,700 estimated tokens at the same `words × 1.3` proxy this project already uses. This is large but not unreasonable for a system-prompt/AGENTS.md context in 2026-era harnesses with substantial context windows; it is the only version of this artifact that can honestly claim structural completeness. The output style (DIST-03) faces a harder tension: Claude Code output styles are typically much shorter persona layers (SimpleEnglish's is 361 words), and if a user selects the output style alone, without the skill folder also installed or readable, none of the reference-file detail is available to the model at all. **This is a genuine, unresolved design tension this research flags rather than resolves** (see Open Questions) — the two defensible options are (a) ship a condensed output style with an explicit, disclosed limitation that it covers the prose catalog and integrity flags only, deferring completeness-audit/artifact-family depth to "install the full skill for that," or (b) ship a longer output style that inlines everything the system prompt does, accepting that output styles are not typically this long. This research recommends (a), condensed-with-disclosure, because it is the only option that does not silently misrepresent what the artifact covers, but flags it explicitly as **Claude's Discretion pending a discuss-phase pass**, not a locked recommendation.

### Pattern 4: DIST-05's Sync Mechanism — Generator Plus Hash-Drift Check, Following This Project's Own "Stated Value vs. Registry" Idiom

**The concrete new-code shape**, following exactly the pattern `catalog-count-mismatch`/`mc-count-mismatch` already established (a stated value in a file, checked against a freshly recomputed value from the source of truth):

1. `tools/generate_derivatives.py` (new, stdlib-only): reads `skills/proof-first/SKILL.md` and the reference files named in Pattern 3, computes `hashlib.sha256(...).hexdigest()` over their concatenated bytes (a single, stated, documented hashing recipe — never "whichever bytes happen to produce a favorable number," mirroring `skill-token-budget-exceeded`'s own declared-ceiling discipline of using one stated estimator consistently), and writes `output-styles/proof-first.md` and `prompts/system-prompt.md` with a leading HTML comment recording that hash, e.g. `<!-- generated from skills/proof-first/SKILL.md + references/{deletion-test,completeness-audit,artifact-patterns}.md, sha256:ab12...ff -->`.
2. A new `check_repo.py` code, `skill-derivative-stale`: for each derivative file that carries this header comment, recompute the same hash over the same current source files and compare; fire if the recorded hash does not match the live one, or if the header comment is missing entirely from a file that exists.
3. **The documented re-sync step (DIST-05's explicit requirement):** a `## Keeping derivatives in sync` section in README (or a short `tools/generate_derivatives.py --help`-style docstring), stating plainly: "after any edit to `SKILL.md` or its `references/` files, run `python3 tools/generate_derivatives.py` before committing; `check_repo.py`'s `skill-derivative-stale` code fails the build if this step was skipped."

**Failure modes to disclose (this project's own "declared ceiling" convention, applied to the new check):** (a) the hash only proves the derivative was regenerated from *some* version of the source — it does not itself prove the generator's own logic is correct, i.e., a bug in `generate_derivatives.py` that silently drops a rule would still produce a matching hash as long as the same buggy generator produced it; (b) this mechanism proves *structural* freshness (the derivative was produced from the current source), not *behavioral* equivalence (whether a live model session using the derivative behaves the same as one using the skill) — that second claim is out of scope for a static hash check and belongs to Q3/Q7's discussion below; (c) a contributor could still hand-edit a derivative file after generation and leave the stale header comment in place with matching hash by coincidence — astronomically unlikely for a real SHA-256 collision, but the check only verifies the hash tag agrees with a recomputation, not that no one tampered with the body between generation and commit; state this as a known, accepted ceiling, following the exact rhetorical pattern every other "Declared ceiling" note in `tools/check_repo.py`'s own docstring already uses.

### Pattern 5: EX-02's Concrete Content — Real Family Names and All 39 Citable IDs, So the Planner Invents None

**The four frozen artifact-family names**, already enforced as a build-checkable interface (`ARTIFACT_FAMILY_SECTIONS`, `tools/check_repo.py:1487-1496`) and already used verbatim throughout `references/artifact-patterns.md` `[VERIFIED: skills/proof-first/references/artifact-patterns.md, headings read this session]`:
- `RFP and RFI response`
- `Solution proposal`
- `Executive summary`
- `Demo and discovery material`

**All 31 allocated `PF-` IDs and all 8 allocated `MC-` IDs** `[VERIFIED: NUMBERING.md's Allocated IDs table, lines 79-124, read this session]` — the complete, closed set any before/after "after" column may cite:

`PF-0.1, PF-1.1, PF-1.2, PF-1.5, PF-1.9, PF-1.13, PF-1.14, PF-1.17, PF-1.21, PF-1.25, PF-2.1, PF-2.2, PF-2.3, PF-2.4, PF-2.11, PF-2.12, PF-2.13, PF-2.14, PF-2.15, PF-2.16, PF-2.17, PF-3.1, PF-3.2, PF-3.3, PF-4.1, PF-4.2, PF-4.3, PF-4.4, PF-5.1, PF-5.2, PF-5.3` (31 PF rules) and `MC-1, MC-6, MC-11, MC-16, MC-21, MC-26, MC-31, MC-36` (8 MC rules) — 39 total. Citing any other number is `undefined-id`, already a live, proven CI gate.

**Where family-level worked examples should live:** a new `examples/before-after.md`, already named "(planned)" in README's own target tree (`README.md:97`). This is distinct from `references/worked-examples.md`, which is per-rule (see Alternatives Considered above) — EX-02 asks for per-**family** pairs, a document-level before/after (e.g., a full non-compliant RFP answer paragraph next to a compliant rewrite citing several rule IDs together), not a single-sentence contrast.

**What makes a before/after pair mechanically checkable — two new codes, mirroring existing patterns exactly:**
1. `before-after-family-missing` — mirrors `artifact-family-section-missing`'s exact shape: `examples/before-after.md`, if it exists, must contain all four frozen family headings (reuse `ARTIFACT_FAMILY_SECTIONS` as the shared constant — do not redeclare a second copy of this frozen list, per this project's own "one grammar, one validation path" discipline).
2. `before-after-citation-missing` — new shape, but small: for each family section in `examples/before-after.md`, the section's body must contain at least one `PF-\d+\.\d+` or `MC-\d+` token (reusing the same regex `check_undefined_id` already uses). This directly operationalizes EX-02's own wording ("citing real, shipped rule numbers") as a build failure, not a convention. Declared ceiling to state in the docstring: this check only asserts *a* citation exists somewhere in the section, not that the citation is textually adjacent to the specific sentence it is meant to justify, nor that the cited rule is the *correct* one for that sentence — content-quality correctness remains a manual/UAT concern, exactly as Phase 2/3's own Validation Architecture sections already disclose for every content-quality half of a requirement.

### Recommended `examples/before-after.md` Structure

```markdown
# Before and After

One family-level before/after pair per artifact family this skill classifies. Every fact traces
to `examples/deal-brief.md`. Every after column cites at least one rule ID allocated in
`NUMBERING.md`.

## RFP and RFI response

✗ [non-compliant paragraph — vague, no evidence, buried answer]
✓ [compliant rewrite — answer-first, evidenced, citing e.g. PF-2.1, MC-11]

## Solution proposal
...

## Executive summary
...

## Demo and discovery material
...
```

(The bracketed placeholders above are illustrative structure only — the plan should draft real prose sourced from `examples/deal-brief.md`'s facts, following the exact tone and construction already proven in `references/worked-examples.md`'s existing ✗/✓ pairs.)

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| A hand-maintained output style / system prompt kept in sync "by discipline" | Two independently-worded condensations, updated by a contributor remembering to edit both whenever SKILL.md changes | `tools/generate_derivatives.py`, a single stdlib-only generator, plus a hash-drift `check_repo.py` code | Directly demonstrated by SimpleEnglish's own repo: this is exactly the path that produces zero drift protection. This project's own DIST-05 requirement exists specifically because "by discipline" is not good enough — the same reasoning this project already applied to buzzword lists and paraphrase judgments (never a maintained list where a mechanism is possible) |
| A second, differently-shaped JSON parser for `.claude-plugin/*.json` | A bespoke line-by-line JSON reader, mirroring `parse_frontmatter`'s targeted-extractor style | Python's stdlib `json` module | Unlike SKILL.md's frontmatter (a YAML-adjacent, hand-parsed format with no general-purpose stdlib parser available, D-33's stated reason for a targeted extractor), `.claude-plugin/*.json` files are genuine, well-formed JSON — `json.loads()` is the correct, zero-risk stdlib tool, and reaching for a hand-rolled parser here would be solving an already-solved problem the D-33 rationale does not apply to |
| A third copy of the four frozen artifact-family name strings | Redeclaring `['RFP and RFI response', 'Solution proposal', ...]` inside a new before-after check | Import/reuse `ARTIFACT_FAMILY_SECTIONS`, already defined once in `tools/check_repo.py:1487-1496` | This exact list is already flagged in its own source as a frozen interface multiple other files bind to ("do not reword, re-case, pluralise, or reorder these four strings") — a second, independently-typed copy is exactly the drift risk that comment exists to prevent |

**Key insight:** every new piece of tooling this phase needs is either (a) a same-shaped sibling of a check Phase 1-3 already built and proved, or (b) a small, clearly-scoped new script solving a problem (mechanical derivation with drift detection) that this project's own reference implementation never had to solve and does not model. The risk in this phase is design judgment on the two genuinely novel questions (DIST-05's mechanism, DIST-03/04's content scope), not engineering novelty once those judgments are made.

## Common Pitfalls

### Pitfall 1: Treating SimpleEnglish's output-style/system-prompt files as a template to copy wording from

**What goes wrong:** A plan drafts Proof First's `output-styles/proof-first.md` by adapting SimpleEnglish's own 361-word file's structure and phrasing patterns, since it is the nearest working example.
**Why it happens:** It is the only real, working example on disk, and it is natural to reach for it.
**How to avoid:** SimpleEnglish's condensation works because its source has no reference-file dependency (Pattern 3). Proof First's derivatives must be *generated from* SKILL.md + references, not hand-styled after SimpleEnglish's prose — the generator's job is mechanical extraction/concatenation, not creative condensation. Structural conventions (frontmatter shape, `keep-coding-instructions` field) may be borrowed; prose content may not.
**Warning signs:** A hand-written (not generated) `output-styles/proof-first.md` with no accompanying `tools/generate_derivatives.py` and no hash-drift check.

### Pitfall 2: Asserting "equivalent behavior" as a fact in README or in the derivative files themselves

**What goes wrong:** README's Install/Distribution section states something like "the output style and system prompt give you the same behavior as the skill" as a flat claim.
**Why it happens:** DIST-03/04's success criterion literally uses the phrase "equivalent behavior either way," and it is tempting to restate the requirement as an accomplished fact once the artifacts exist.
**How to avoid:** Per this project's own "measured claims or no claims" constraint (already stated in `PROJECT.md` and `CLAUDE.md`), this is a behavioral claim about live model sessions that has not been measured — Phase 5 is where a benchmark could measure it, and even then only comparatively, never as a proven identity. Phase 4 can only discharge this **structurally**: state that the derivatives are mechanically generated from the same source content and pass a content-hash freshness check, and stop there. See Q3/Q7.
**Warning signs:** Any sentence in README, `output-styles/proof-first.md`, or `prompts/system-prompt.md` asserting sameness of outcome rather than sameness of source.

### Pitfall 3: Assuming the plugin manifest's `version` field is free-standing and forgetting NUMBERING.md's existing obligation

**What goes wrong:** `.claude-plugin/plugin.json` ships with an arbitrary version string (e.g., `"1.0.0"`) uncoordinated with `SKILL.md`'s frontmatter `metadata.version` (`"0.1.0"`), and no check catches the mismatch until a human notices.
**Why it happens:** The two files live in different directories and are edited by different plan tasks; nothing forces a contributor to cross-reference them.
**How to avoid:** Build `plugin-manifest-version-mismatch` (Pattern 2) as part of this phase's own deliverables, not as an assumed side effect of "we'll remember." This is exactly the "check that cannot fire" defect class Phase 1 spent three gap-closure plans closing for the PF namespace — do not reintroduce it here for the plugin/skill version pair.
**Warning signs:** A plan that creates `.claude-plugin/plugin.json` with a hardcoded version string not read from `SKILL.md`'s own frontmatter, and no new check verifying the two agree.

### Pitfall 4: Inventing the GitHub `owner/repo` string for install commands without flagging it as unresolved

**What goes wrong:** README ships with a placeholder or guessed `owner/repo` (e.g., `devoteam/technical-presales` or a personal GitHub handle) baked into `npx skills add owner/repo` and `claude plugin marketplace add owner/repo`, presented as if it were a confirmed fact.
**Why it happens:** Every other part of this research is groundable in a file or a fetched URL; this one fact is not, because **no git remote is configured in this repository as of this session** `[VERIFIED: git remote -v, run this session — zero output]`.
**How to avoid:** State plainly in the plan and in README (e.g., an HTML comment or a clearly marked TODO) that the install commands use a placeholder `owner/repo` pending the actual publish location, and route confirmation of the real value to a `checkpoint:human-verify` task, exactly as the Package Legitimacy Protocol requires for any unverified external fact.
**Warning signs:** A plan or a committed README with a confident-sounding `owner/repo` string and no accompanying note that it is unconfirmed.

## Code Examples

### Existing per-rule worked-pair format (the pattern EX-02's family-level pairs should visually echo, at a different unit of granularity)

```
# Source: skills/proof-first/references/worked-examples.md:9-13, read this session, quoted verbatim
## PF-0.1

✗ "Kestrel Systems Group offers a comprehensive, best-in-class cloud migration solution."
✓ "Halverton Mutual's 850-VM estate is at capacity, and its nightly settlement batch regularly
overruns its required window. This proposal describes an estate the team can govern, not one it
has to manage VM by VM."
```

### Existing artifact-family section-presence check (the exact shape `before-after-family-missing` should mirror)

```python
# Source: tools/check_repo.py:1487-1544, read in full this session
ARTIFACT_FAMILY_SECTIONS = (
    'RFP and RFI response', 'Solution proposal',
    'Executive summary', 'Demo and discovery material',
)

def check_artifact_family_sections(repo_root):
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        patterns_path = skill_path.parent / 'references' / 'artifact-patterns.md'
        if not patterns_path.exists():
            continue
        text = strip_fences(patterns_path.read_text(encoding='utf-8'))
        sections = split_sections(text)
        for heading in ARTIFACT_FAMILY_SECTIONS:
            if heading not in sections:
                ...  # violation, naming file + missing heading + owning requirement
```

### Existing stated-value-vs-registry check (the exact shape `plugin-manifest-version-mismatch` and `skill-derivative-stale` should mirror)

```python
# Source: tools/check_repo.py:1400-1428, read in full this session (catalog-count, PF-specific)
COUNT_SENTENCE_RE = re.compile(r'^This catalog contains (\d+) rules in (\d+) numbered sections\.$')

def check_catalog_count(allocated, repo_root):
    # ... stated = parsed from SKILL.md's own text ...
    # ... registry = derived from NUMBERING.md's Allocated IDs table ...
    if stated_rules != registry_rule_count or stated_sections != registry_section_count:
        violations.append(...)  # "states X, but the registry has Y"
```

### Real, verified skills-CLI and plugin-marketplace install commands (SimpleEnglish's own README, live and working)

```
# Source: ~/devoteam/.claude/plugins/marketplaces/simple-english/README.md, read this session, quoted verbatim
npx skills add AminBlg/SimpleEnglish

claude plugin marketplace add AminBlg/SimpleEnglish && claude plugin install simple-english@simple-english

# Or inside Claude Code:
/plugin marketplace add AminBlg/SimpleEnglish
/plugin install simple-english@simple-english
```

### Official Claude Code plugin manifest minimal shapes (fetched directly this session)

```json
// plugin.json minimal valid example
// Source: https://code.claude.com/docs/en/plugin-marketplaces, fetched this session
{ "name": "my-plugin" }
```

```json
// marketplace.json minimal valid example
// Source: https://code.claude.com/docs/en/plugin-marketplaces, fetched this session
{
  "name": "my-plugins",
  "owner": { "name": "Your Name" },
  "plugins": [ { "name": "my-plugin", "source": "./plugins/my-plugin" } ]
}
```

## State of the Art

| Old Approach (SimpleEnglish's shipped state, this project's own explicit model) | Current Approach (this phase must build) | When Changed | Impact |
|---|---|---|---|
| Output style / system prompt hand-condensed once, no drift protection, no documented re-sync step | Generated from source + hash-stamped, with a `check_repo.py` staleness gate | This phase (DIST-05) | Proof First's DIST-05 requirement is stricter than what its own named reference implementation actually does — this is new engineering scope, not a port |
| A single self-contained SKILL.md with no reference-file dependency for core behavior | A SKILL.md that explicitly delegates 4,326 words of instructional content to `references/` (deletion test, completeness audit, artifact patterns, checklist) | Established in Phases 2-3, consequential now | A faithful no-skill-support system prompt must inline substantially more content than SimpleEnglish's own condensation needed to; a short output style faces a genuine, disclosed content-scope tension SimpleEnglish never had to resolve |
| README with no before/after section, no install section (claim-free, Phase 1-3 state) | README leading with before/after pairs and a per-harness install section, while keeping the existing MOD-04 measured-figure disclosure and its CI gate intact | This phase (DIST-06) | The rewrite is additive to the existing Status section, not a replacement of it — `readme-results-pointer-missing` must keep passing |

**Deprecated/outdated for this phase's purposes:** None.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | A faithful system prompt should inline SKILL.md + `deletion-test.md` + `completeness-audit.md` + `artifact-patterns.md` in full (~7,450 words, ~9,700 estimated tokens), while `worked-examples.md` and `checklist.md` may be abridged or omitted from the condensed derivatives | Pattern 3 | If a target harness's system-prompt field has a hard length ceiling well below ~10k tokens (some chat-product "custom instructions" boxes do), this design does not fit as-is and needs a further-condensed variant — flagged, not verified against every possible harness's exact limit |
| A2 | The output style should be a condensed, disclosed-limitation artifact (option (a) in Pattern 3), not a full inline of everything the system prompt carries | Pattern 3 | This is explicitly flagged as Claude's Discretion pending a discuss-phase pass; if a future `04-CONTEXT.md` locks the fuller-inline option (b) instead, this recommendation should be discarded |
| A3 | `hashlib.sha256` over the concatenated bytes of SKILL.md + the three depended-on reference files is an adequate, sufficient DIST-05 mechanism | Pattern 4 | If the planner determines a coarser granularity (e.g., a single hash covering the whole `skills/proof-first/` tree, or a per-file hash set rather than one combined hash) is more useful for pinpointing *which* file changed, that is a legitimate refinement — the combined-hash version is simpler to implement first and sufficient to detect *that* something changed, which is DIST-05's actual requirement |
| A4 | The repository's eventual GitHub `owner/repo` string is unknown and must be treated as a placeholder pending human confirmation | Pitfall 4 | If this is silently guessed and shipped, the README's install commands could be wrong at publish time — this is exactly the class of unverifiable external fact the Package Legitimacy Protocol's `checkpoint:human-verify` gate exists for |

## Open Questions

1. **Should the output style inline the full derivative content (matching the system prompt) or ship a condensed, explicitly-limited version?**
   - What we know: SimpleEnglish's own output style is a short (361-word) condensation, but its source skill has no reference-file dependency to omit; Proof First's does.
   - What's unclear: whether a long output style (thousands of words) is a reasonable user experience for a Claude Code output style, versus whether a short one that silently under-delivers on completeness-audit/artifact-family depth is an acceptable, disclosed limitation.
   - Recommendation: ship the condensed version with an explicit, visible disclosure of what it omits (Pattern 3, option (a)); treat as Claude's Discretion pending a discuss-phase pass, not a locked interface.

2. **Does `references/worked-examples.md` need to be inlined into the system prompt derivative, or is it acceptable to omit example material from a no-skill-support paste?**
   - What we know: `worked-examples.md` (1,316 words) supplies illustrative ✗/✓ contrasts, not new rule content — every rule it illustrates is already stated in full in SKILL.md itself.
   - What's unclear: whether omitting worked examples materially degrades a model's ability to apply the rules correctly in a no-skill-support harness, versus whether the rule statements alone (each of which already carries a **Replace with:** instruction) are sufficient.
   - Recommendation: omit from the system prompt derivative by default (keeps the artifact smaller, and every rule's own **Replace with:** line already carries the operational instruction); flag as Claude's Discretion, easy to reverse if UAT surfaces a real quality gap.

3. **What is the actual GitHub `owner/repo` this repository will be published under?**
   - What we know: no git remote is configured as of this session.
   - What's unclear: the final public location, which the exact README install commands depend on verbatim.
   - Recommendation: use a clearly marked placeholder, route to a `checkpoint:human-verify` task before this repository goes public, per Pitfall 4.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | `tools/generate_derivatives.py`, `check_repo.py` extensions | ✓ | 3.13.13 `[VERIFIED: python3 --version, run this session]` | — |
| git | Committing plan output, phase workflow | ✓ | 2.54.0 `[VERIFIED: git --version, run this session]` | — |
| Node.js / npm (for `npx skills`) | Manually smoke-testing DIST-01's install command | ✓ | Node v22.22.3, npm 10.9.8 `[VERIFIED: node --version, npm --version, run this session]` | — |
| Claude Code CLI | Manually smoke-testing DIST-02/03's plugin/output-style install flow | ✓ | 2.1.236 `[VERIFIED: claude --version, run this session]` | Below the `2.1.259+` floor `./.claude/CLAUDE.md` notes for `--permission-prompts none`; irrelevant here since no scripted permission handling is needed for a manual smoke test |
| A public GitHub remote for this repository | The exact install commands DIST-01/02/06 must state verbatim | ✗ | — | No fallback — this is a genuine blocker for the *exact final string*, not for building the mechanism; use a placeholder and route to `checkpoint:human-verify` (see Pitfall 4) |

**Missing dependencies with no fallback:** the repository's own public location (owner/repo) — blocks only the literal string in README's install commands, not the mechanism build-out.
**Missing dependencies with fallback:** none beyond the above.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `tools/check_repo.py`'s own `--self-test`/`--mutation-test` harness (unchanged from Phase 1-3; no pytest/jest, by design) |
| Config file | none |
| Quick run command | `python3 tools/check_repo.py --self-test` |
| Full suite command | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` |

**Baseline recorded this session `[VERIFIED: all three commands run this session against the current repo]`:**
```
$ python3 tools/check_repo.py --self-test
self-test PASS - verified violation codes: [32 codes listed]

$ python3 tools/check_repo.py --mutation-test
mutation-test CONTROL: 0 violations on the unmutated copy (0 known-open per KNOWN_OPEN_VIOLATIONS, 0 unexpected)
[... 32 "mutation-test OK" lines ...]
mutation-test PASS: 32 codes discrimination-proven

$ python3 tools/check_repo.py
check_repo: 0 violations
```

This phase should raise the discrimination-proven count above 32 (expect 4-6 new codes: `plugin-manifest-version-mismatch`, `skill-derivative-stale`, `before-after-family-missing`, `before-after-citation-missing`, and optionally a plugin-manifest-well-formedness check), never leave it lower, with the CONTROL line still reading "0 unexpected."

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| EX-02 | `examples/before-after.md` exists, has all four frozen family headings, each with at least one real rule citation | unit (new) | `python3 tools/check_repo.py --self-test` (after new fixtures for `before-after-family-missing`/`before-after-citation-missing`) | ❌ Wave 0 — new checks + file |
| EX-02 (content quality) | The before/after prose is genuinely illustrative, not a restatement of the rule text | manual (same class as Phase 2/3's content-quality findings) | UAT / conversational verification | N/A |
| DIST-01 | `npx skills add <owner>/<repo>` actually installs the skill in a real harness | manual (this environment cannot run `npx` against a not-yet-published GitHub repo) | manual smoke test once the repo is public | N/A — permanently manual for *this* environment; see Environment Availability |
| DIST-02 | `.claude-plugin/plugin.json` + `marketplace.json` are well-formed, and `claude plugin marketplace add`/`install` actually works | unit (well-formedness: new, optional) + manual (actual install flow) | `python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))"`-style check inside `check_repo.py`, plus a manual `claude plugin marketplace add ./` smoke test against the local working tree (Claude Code supports a local-path source) | ❌ Wave 0 for the unit half; manual for the install-flow half |
| DIST-03 | Output style toggles on via `/config` and changes response style for the whole session | manual (model/UI behavior) | UAT / conversational verification, plus a manual `/config` smoke test in a real Claude Code session | N/A |
| DIST-04 | A pasted system prompt produces comparable behavior in a harness with no skill support | manual (model behavior; this is the "equivalent behavior" claim Pitfall 2 says must never be asserted as measured fact) | UAT / conversational verification only, explicitly disclosed as unmeasured | N/A |
| DIST-05 | Derivative files are regenerated from SKILL.md whenever it changes; staleness is mechanically detectable | unit (new) | `python3 tools/check_repo.py --self-test` (new `skill-derivative-stale` fixtures) + `python3 tools/generate_derivatives.py` itself, exercised in CI as a "does it run without error" smoke step | ❌ Wave 0 — new script + check |
| DIST-06 | README leads with before/after pairs and states an install path per harness | manual (prose-quality, ordering) | UAT / conversational verification for prose quality; `readme-results-pointer-missing` (existing) must keep passing as a regression guard | ✅ existing gate must not regress; ❌ new ordering/content is manual |

**As with Phases 2-3, expect the model-behavior half of DIST-03/04 (does a live session actually behave the same) to remain permanently `nyquist_compliant: false`** — no file-reading checker can observe a future live session's behavior, and this project's own evidence discipline forbids asserting it as measured without Phase 5's benchmark. State this plainly in the plan's Definition of Done.

### Sampling Rate

- **Per task commit:** `python3 tools/check_repo.py --self-test`
- **Per wave merge:** `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py`
- **Phase gate:** full suite green before `/gsd-verify-work`, plus a UAT pass covering DIST-03/04's model-behavior half and a manual smoke test of the plugin/skills-CLI install flow once network/publish access allows it.

### Wave 0 Gaps

- [ ] `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` — do not exist yet
- [ ] `output-styles/proof-first.md`, `prompts/system-prompt.md` — do not exist yet
- [ ] `tools/generate_derivatives.py` — does not exist yet
- [ ] `examples/before-after.md` — does not exist yet
- [ ] New `check_repo.py` codes and their self-test fixtures/mutations: `plugin-manifest-version-mismatch`, `skill-derivative-stale`, `before-after-family-missing`, `before-after-citation-missing` (and optionally a JSON well-formedness check for the two manifests)
- [ ] README's before/after + Install sections — do not exist yet (Status/measured-figure sections already exist and must be preserved)
- [ ] The actual GitHub `owner/repo` string — genuinely unknown, no git remote configured; route to `checkpoint:human-verify`

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No authentication surface |
| V3 Session Management | No | Not applicable |
| V4 Access Control | No | Not applicable — public MIT-licensed content |
| V5 Input Validation | Yes, narrowly | The new JSON parsing (`.claude-plugin/*.json`) reads locally-authored, repo-owned files via stdlib `json.loads`, not untrusted external input — no injection surface. The generator script reads only repo-relative paths it is pointed at |
| V6 Cryptography | Yes, narrowly | `hashlib.sha256` is used here for **content-drift detection**, not for any security guarantee (integrity against a malicious actor, signing, etc.) — this must be stated plainly in the code/docstring so a future reader does not mistake it for a security control |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A derivative file (`output-styles/proof-first.md`, `prompts/system-prompt.md`) silently drifting out of sync with `SKILL.md` after an edit, the "check that cannot fire" class | Tampering (of the project's own claimed DIST-05 guarantee) | The new `skill-derivative-stale` check, self-test-and-mutation-proven exactly like every other code in this file |
| A plugin manifest shipping with an uncoordinated version string, contradicting NUMBERING.md's own stated versioning rule | Tampering (of the registry's own claimed cross-file guarantee) | The new `plugin-manifest-version-mismatch` check |
| An unresolved `owner/repo` placeholder shipping to a public README as if it were confirmed, sending users to a nonexistent or wrong repository | Tampering / Information Disclosure risk to end users, not to this repo | Explicit `checkpoint:human-verify` gate before publish, per Pitfall 4 |
| A README asserting "equivalent behavior" as measured fact when no benchmark has run | Repudiation (of the project's own evidence-discipline commitment) | Pitfall 2's explicit ban; state structural completeness only, never behavioral sameness, until Phase 5 |

## Sources

### Primary (HIGH confidence — read or fetched directly this session)

- `skills/proof-first/SKILL.md`, all five `references/*.md` files, `checklist.md`, `worked-examples.md` — full files read, word counts measured via `wc`
- `NUMBERING.md`, `NOTICES.md`, `README.md`, `examples/deal-brief.md` — full files read
- `tools/check_repo.py` — full 3,787-line file read across two passes; every relevant check function, parser, fixture, and mutation examined for reusable patterns
- `.github/workflows/ci.yml` — read in full
- `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/WINDOWS.md`, `.planning/PROJECT.md` (grepped) — read for phase scope, decision history, and open ledger items
- `.planning/phases/03-completeness-audit-artifact-patterns/03-RESEARCH.md` — read in full (546 lines) for methodological precedent and to confirm no conventions needed re-deriving
- `~/devoteam/.claude/plugins/marketplaces/simple-english/` — the entire reference-implementation repository read directly: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `output-styles/simple-english.md`, `prompts/system-prompt.md`, `README.md` (in full), `skills/simple-english/SKILL.md` (word count only), directory listing confirming no generator/sync script exists anywhere
- `https://code.claude.com/docs/en/plugin-marketplaces` — fetched directly this session for the exact `plugin.json`/`marketplace.json` required/optional field lists and minimal valid examples
- `python3 --version` (3.13.13), `git --version` (2.54.0), `node --version` (v22.22.3), `npm --version` (10.9.8), `claude --version` (2.1.236), `git remote -v` (empty) — all run directly this session
- `npm view skills version/repository.url/description` — run directly this session against the live npm registry
- `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py && python3 evals/conformance/run_conformance.py --self-test` — run directly this session, full output recorded above

### Secondary (MEDIUM confidence)

- `https://github.com/vercel-labs/skills` (via WebFetch) — exact `npx skills add`/`--skill`/`-a`/`--all` flag syntax; cross-checked against SimpleEnglish's own real, working README usage (`npx skills add AminBlg/SimpleEnglish`), which agrees with the simpler no-flag form for a single-skill repository

### Tertiary (LOW confidence)

- None — every claim in this research is either read/fetched directly this session or explicitly flagged in the Assumptions Log / Open Questions as a design judgment pending confirmation.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new packages beyond the already-locked, freshly-reverified `skills` CLI; all new tooling is stdlib-only, matching every prior phase's posture
- Architecture: HIGH for file layout, manifest schema, and CI-extension patterns (all read or fetched directly this session, cross-checked against a real working reference implementation and official docs); MEDIUM for the two genuinely novel design calls (DIST-05's mechanism, DIST-03's content-scope tradeoff) since these are judgment, not fact
- Pitfalls: HIGH — grounded directly in this session's own measurements (word counts, the empty git remote, SimpleEnglish's absent sync mechanism) and in Phase 1-3's own documented near-misses (the "check that cannot fire" class), not speculation
- Security: MEDIUM — small, honestly-scoped surface, matching Phase 2/3's own ASVS mapping precedent; the one genuinely new element (a hash used for drift detection, not security) is flagged explicitly to prevent future misreading

**Research date:** 2026-09-17
**Valid until:** Effectively the life of this phase's plan. Two facts are time-sensitive and should be re-checked if plan execution is delayed: (1) `SKILL.md`'s measured token margin (177 estimated tokens) — re-measure if any other phase or hotfix touches `SKILL.md` first; (2) whether a git remote has since been configured for this repository — if so, the actual `owner/repo` string replaces the placeholder this research explicitly could not resolve.
