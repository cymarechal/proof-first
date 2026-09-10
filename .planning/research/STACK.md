# Stack Research

**Domain:** Public, cross-harness AI agent skill (technical presales writing) — authoring, packaging, distributing, and benchmarking, modeled on SimpleEnglish (AminBlg/SimpleEnglish)
**Researched:** 2026-09-10
**Confidence:** HIGH overall (official specs and official docs fetched directly for every load-bearing schema); MEDIUM/LOW called out inline where only community sources exist

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Agent Skills standard (agentskills.io) | Current spec, no version number published — treat as a living spec | Portable skill format: `SKILL.md` + optional `scripts/`, `references/`, `assets/` | This is the only format that is genuinely cross-harness in 2026. It is consumed natively by Claude Code, Cursor, Codex, GitHub Copilot, Gemini CLI, OpenCode, Goose, and dozens more via the `skills` CLI ecosystem. Building anything harness-specific (e.g. a Cursor-only rules file) forfeits the reach the project explicitly wants. |
| `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` | Current Claude Code plugin schema (no version pin; schema is additive, backward compatible) | Distribution through the Claude Code plugin marketplace mechanism | Second distribution channel, proven by SimpleEnglish. Zero build step: the files are hand-written JSON, no compiler, no publish pipeline. |
| `output-styles/*.md` | Claude Code v2.1+ output style format | A "persona" mode that changes how Claude Code talks for an entire session, not just one skill invocation | Gives users a way to force Proof First's voice by default rather than relying on the model to decide the skill is relevant. Zero-dependency, one Markdown file. |
| Python 3 (stdlib only: `re`, `json`, `sys`, `argparse`, `pathlib`, `subprocess`, `time`, `itertools`, `datetime`) | 3.11+ (3.13 current stable as of 2026; anything 3.9+ will run this code unchanged) | The eval harness: linter + benchmark runner + judge runner | Matches the project's own "zero dependencies" constraint and SimpleEnglish's precedent exactly. A `pip install` step is one more thing that can silently break reproducibility for someone trying to reproduce the headline number two years from now; stdlib-only means `python3 script.py` works forever with no lockfile. |
| Claude Code CLI (logged-in, subscription auth) | Whatever is on the user's PATH; no version pin needed for `-p` mode itself, but note flags below have version floors | Headless model driver for the primary benchmark matrix | No API key needed (uses the CLI's own OAuth login), so the benchmark is runnable by anyone with a Claude subscription — the same bar SimpleEnglish set. |
| A second, harness-agnostic CLI (the reference implementation uses **Pi**; **OpenCode** or the **Claude Agent SDK** in Python/TS are equally valid substitutes) | N/A | Cross-provider benchmark runner, so the headline number isn't "only tested on Claude" | The project's `PITFALLS.md`/`FEATURES.md` should flag this, but for STACK purposes: pick one non-Anthropic-hosted runner that can disable ambient skills/tools/context (`--no-tools --no-skills --no-context-files` in Pi's case) so the baseline condition is genuinely a clean baseline. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| None (stdlib `re`) | — | Deterministic violation counting | Default choice — see the dedicated linting analysis below. |
| `textstat` | latest on PyPI (actively maintained; last commit Feb 2026 per repo activity) | Optional supplementary readability metrics (Flesch Reading Ease, sentence-length distributions) reported alongside the custom linter | Only if you want a second, externally-recognized number in `RESULTS.md` for readers who trust a named library more than a bespoke regex. Not a replacement for the custom linter — it does not detect superlatives, buzzwords, or claim/number adjacency, which are this project's actual targets. |
| `spaCy` | N/A — **not recommended**, see analysis below | POS-tagged superlative detection, numeric entity detection | Only if a future phase needs true grammatical disambiguation (e.g., distinguishing "the fastest car" as a fact vs. "the best solution" as an unquantified claim) and the team accepts a ~500MB model download breaking the zero-dependency posture for the eval harness specifically (not the skill itself, which stays dependency-free regardless). |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| GitHub Actions | CI for `ste`-style `--self-test` linter mode | One job, no matrix needed: `python3 evals/lint.py --self-test`. Runs on every push/PR. This is the entire CI surface for a zero-dependency repo — no package manager, no build, nothing else to test in CI. |
| `skills-ref` (agentskills/agentskills reference library) | Validates `SKILL.md` frontmatter against the spec (`skills-ref validate ./skill-dir`) | Run this locally (or add as a second CI job if the runner environment can fetch it) before every release. It is the closest thing to an official conformance check and catches the exact class of error that silently breaks distribution: name/description length, hyphen rules, frontmatter key allow-list. |
| MIT `LICENSE` file at repo root | Legal | Matches SimpleEnglish and the project's own stated constraint. |

## Installation

```bash
# Core: nothing to install for the skill itself (zero dependencies, by design)

# Eval harness: nothing to install either (stdlib-only Python 3.11+)
python3 --version   # confirm 3.9+ is on PATH; no venv, no requirements.txt needed

# Optional, only if you add the supplementary readability metric
pip install textstat   # optional, evals/ only, never required to reproduce headline numbers

# CI
# .github/workflows/ci.yml — no install step, just:
python3 evals/lint.py --self-test
```

---

## 1. The Agent Skills standard — canonical spec and schema

**Canonical spec location:** `https://agentskills.io/specification` (fetched directly; HIGH confidence). There is also a documentation index at `https://agentskills.io/llms.txt` for machine consumption, and a reference validator at `github.com/agentskills/agentskills` (`skills-ref` package).

**Directory shape:**
```
skill-name/
├── SKILL.md          # required
├── scripts/           # optional — executable code
├── references/        # optional — progressive-disclosure docs, loaded on demand
├── assets/            # optional — templates, static resources
```

**Frontmatter schema (verified against the live spec page):**

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | 1–64 chars. Lowercase unicode alphanumerics and hyphens only. No leading/trailing hyphen, no `--`. **Must match the parent directory name.** |
| `description` | Yes | 1–1024 chars, non-empty. Must describe *what* it does and *when* to use it — this is the only field an idle agent reads at startup, so keyword density matters for activation. |
| `license` | No | License name or a pointer to a bundled license file. |
| `compatibility` | No | 1–500 chars. Free text describing environment requirements ("Requires git, docker, jq..."). Most skills should omit it. |
| `metadata` | No | Free-form string→string map (author, version, etc.). Clients may use it; the spec itself ignores it. |
| `allowed-tools` | No | Space-separated string of pre-approved tools. Marked **experimental** — support varies by harness. |

Any other top-level key **fails validation** — this is a hard allow-list, not "extra keys are ignored."

**Note on the reference implementation's `compatibility` field:** SimpleEnglish's `SKILL.md` sets `compatibility: claude-code cursor codex gemini-cli opencode` — a bare space-separated harness list. The spec's own examples show `compatibility` as a *prose sentence* ("Designed for Claude Code (or similar products)", "Requires git, docker, jq..."), not a token list. Both forms are legal free text under the 500-char limit, so this isn't a validator error, but it's not the documented convention either. **Recommendation for Proof First: omit `compatibility` entirely** (the spec explicitly says "most skills do not need" it), and instead put the harness-compatibility claim in the README/marketplace description where humans read it — that's a stronger signal than a field the agent itself never surfaces to the user.

**Progressive disclosure — the exact token budget the spec sets:**
1. **Metadata (~100 tokens):** `name` + `description` only, loaded at startup for every installed skill, whether or not it's relevant to the current task.
2. **Instructions (< 5,000 tokens recommended):** the full `SKILL.md` body, loaded only once the skill activates. Spec also says: **keep `SKILL.md` under 500 lines**; push detail into `references/`.
3. **Resources (as needed):** files under `scripts/`, `references/`, `assets/` load only when the agent actually opens them.

For a project with three anchor frameworks (Command of the Message, MEDDICC, Challenger) plus an integrity section and per-artifact patterns, hitting the 500-line/5,000-token ceiling on `SKILL.md` itself is a real risk — SimpleEnglish's own `SKILL.md` is already dense at 53 rules across 9 sections and it still pushes the full dictionary, checklist, and per-artifact adaptations out to three `references/*.md` files loaded on demand. **Do the same split from the start**: rule catalog + self-check in `SKILL.md`; MEDDICC checklist, per-artifact patterns (RFP/RFI, proposal, exec summary, demo/discovery), and the integrity/fabrication-refusal detail in `references/`.

**Which harnesses consume it (verified across multiple 2026 ecosystem sources, MEDIUM-HIGH — no single authoritative harness-support matrix exists, but corroborated across independent write-ups):** Claude Code, Cursor, OpenAI Codex, GitHub Copilot, Gemini CLI, OpenCode, Goose, and dozens of smaller clients all read the same `SKILL.md` format without modification. This is the actual basis for calling it "the standard" rather than "Anthropic's format" — Anthropic originated it but it's now multi-vendor. Confidence on the *exact* list of 78+ supported agents is MEDIUM (aggregated from vercel-labs/skills' own claims and third-party registries, not one canonical list); confidence that Claude Code, Cursor, Codex, Copilot, Gemini CLI, OpenCode, and Goose specifically are supported is HIGH (each cross-confirmed independently).

## 2. Distribution channels — exact schemas

### `skills` CLI (vercel-labs/skills, `npx skills`)

Verified directly from the repo (HIGH confidence for command syntax, MEDIUM for the exact discovery-path list since it came from a fetch summary rather than the raw source file):

```bash
npx skills add <owner/repo>                       # install from a GitHub shorthand
npx skills add <owner/repo> --list                # list skills in a repo without installing
npx skills add <owner/repo> --skill <name>         # install one named skill
npx skills add <owner/repo> --all                  # install every skill in the repo
npx skills init [name]                             # scaffold a new skill
npx skills list                                    # list locally installed skills
npx skills find                                    # interactive search across registries
npx skills remove <name>                           # remove an installed skill
```

**No manifest file is required at the repo root** for `skills` CLI discovery — it walks the tree (root, `skills/<name>/`, `skills/<category>/<name>/`, up to 3 levels) looking for any `SKILL.md`. It separately recognizes `.claude-plugin/marketplace.json`/`plugin.json` for Claude-plugin-ecosystem compatibility, but that's additive, not required. **Implication for Proof First:** put the skill at `skills/proof-first/SKILL.md` (flat layout) — this satisfies both the `skills` CLI's default discovery path *and* the Claude Code plugin convention (`skills/<name>/SKILL.md` relative to plugin root) in one layout, exactly what SimpleEnglish does.

### Claude Code plugin marketplace — `plugin.json` and `marketplace.json`

Verified directly against `code.claude.com/docs/en/plugin-marketplaces` (HIGH confidence for required fields; the fuller optional-field list below is corroborated by the unofficial-but-actively-maintained `hesreallyhim/claude-code-json-schema` repo, MEDIUM confidence for the long tail of optional fields).

**`.claude-plugin/plugin.json` — plugin manifest, one per plugin:**

```json
{
  "name": "proof-first",
  "displayName": "Proof First",
  "description": "Write persuasive, evidence-backed technical presales documents — RFP/RFI responses, proposals, executive summaries, demo/discovery material — that survive a technical evaluator's scrutiny.",
  "version": "1.0.0",
  "author": { "name": "Cyril Marechal" },
  "homepage": "https://github.com/<org>/proof-first",
  "repository": "https://github.com/<org>/proof-first",
  "license": "MIT",
  "keywords": ["presales", "rfp", "proposal-writing", "sales-engineering", "technical-writing"]
}
```
Required: `name`, `description`, `version` (kebab-case name). Everything else in the example above is optional but standard practice (SimpleEnglish's own `plugin.json` sets exactly this set). Additional optional keys exist for `commands`, `agents`, `hooks`, `mcpServers`, `lspServers`, `defaultEnabled` — none needed for a pure writing skill.

**`.claude-plugin/marketplace.json` — one per marketplace (repo), lists one or more plugins:**

```json
{
  "name": "proof-first",
  "owner": { "name": "<Author>", "url": "https://github.com/<org>" },
  "description": "Vendor-neutral technical presales writing skill — evidence-backed, not persuasion-as-adjectives.",
  "plugins": [
    {
      "name": "proof-first",
      "source": "./",
      "displayName": "Proof First",
      "description": "Write persuasive, evidence-backed technical presales documents.",
      "version": "1.0.0",
      "author": { "name": "<Author>" },
      "homepage": "https://github.com/<org>/proof-first",
      "repository": "https://github.com/<org>/proof-first",
      "license": "MIT",
      "keywords": ["presales", "rfp", "proposal-writing"]
    }
  ]
}
```
Required: `name`, `owner.name`, and a `plugins` array where each entry needs at minimum `name` + `source`. `source: "./"` means "this repo is itself the plugin" — the pattern SimpleEnglish uses and the correct one here since Proof First is a single-plugin repo. Do **not** invent a `skills` key in either manifest unless you need a non-default skill path — Claude Code auto-discovers `skills/<name>/SKILL.md` under the plugin root without it.

### Claude Code output styles

Verified directly from `code.claude.com/docs/en/output-styles` (HIGH confidence).

- **Location for a plugin-shipped style:** `output-styles/` at the plugin root (SimpleEnglish ships `output-styles/simple-english.md`; Proof First should mirror this at `output-styles/proof-first.md`).
- **Format:** Markdown file, YAML frontmatter + instruction body.
- **Frontmatter fields:**

| Field | Purpose | Default |
|---|---|---|
| `name` | Style name if different from filename | filename |
| `description` | Shown in the `/config` picker | none |
| `keep-coding-instructions` | Keep Claude Code's built-in software-engineering system prompt underneath your style | `false` |
| `force-for-plugin` | Auto-apply this style whenever the plugin is enabled, no user selection needed (plugin output styles only) | `false` |

For Proof First, `keep-coding-instructions` should be **omitted/false** (a presales-writing persona has nothing to do with software engineering defaults) — mirrors SimpleEnglish's own output style, which also omits it.

### claude.ai skill upload

Verified against `support.claude.com` help center (MEDIUM-HIGH confidence — official source, but reached via search-result synthesis for one datapoint, directly fetched for the rest).

- Path: **Customize → Skills → + → Upload** (web, desktop, and mobile apps).
- The ZIP must have the **skill folder as its root** — not the bare `SKILL.md`, not a nested wrapper folder.
- **Requires "Code execution" enabled** under Settings → Capabilities (Free/Pro/Max/Team/Enterprise).
- One official help article states a stricter **200-character cap on `description`** for claude.ai uploads, versus 1024 in the general agentskills.io spec. This is a real discrepancy between two official-ish sources and I could not fully reconcile it — **treat 200 chars as the safe ceiling** if claude.ai upload matters to the project, even though the general spec and Claude Code itself will accept up to 1024. (Confidence: LOW on the exact number, MEDIUM that *some* tighter description limit applies on claude.ai specifically — worth a manual smoke test before shipping v1.)

## 3. Eval harness tooling — reproducible baseline-vs-skill benchmark

### Headless invocation (Claude Code CLI)

Verified directly against `code.claude.com/docs/en/headless` and `code.claude.com/docs/en/cli-reference` (HIGH confidence).

Minimal reproducible call shape, updated from the reference implementation's pattern:

```bash
claude -p "<prompt>" \
  --model claude-sonnet-5 \
  --effort low \
  --output-format json \
  --disallowedTools "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch" \
  --bare
```

Key points not in the reference implementation, worth adopting:

- **`--bare` is the flag to add for benchmark determinism** and didn't exist when SimpleEnglish's `run_bench.py` was written (it only sets `cwd="/tmp"` and disallows tools). `--bare` skips auto-discovery of hooks, skills, custom commands, subagents, plugins, MCP servers, auto memory, and `CLAUDE.md` — i.e. it guarantees the benchmark isn't accidentally picking up a hook or a stray project-level skill from wherever the harness runs. Docs explicitly say **this is becoming the default for `-p` in a future release** and is "the recommended mode for scripted and SDK calls." Because `--bare` skips OAuth/keychain reading, pair it with `ANTHROPIC_API_KEY` set in the environment rather than relying on subscription login — this is a tradeoff against the reference implementation's "no API key needed" claim, and should be stated as a caveat if adopted.
- **Effort levels confirmed:** `low`, `medium`, `high`, `xhigh`, `max` (the reference implementation's own `RESULTS.md` text cites measured numbers at `low` and `xhigh`, corroborating both exist). One source additionally mentioned an `ultracode` level; I could not independently corroborate this and **do not recommend relying on it** — treat it as unverified.
- **`--json-schema`** (added since the reference implementation was written) can enforce that the model's output actually matches an expected shape, e.g. forcing structured `{"text": "..."}` output instead of parsing free text out of `result`. Not required, but reduces one class of parsing failure in the benchmark runner.
- **`--disallowedTools`** as SimpleEnglish uses it is still correct syntax and still the right call for a pure-writing benchmark (baseline and skill conditions should not be allowed to shell out or read files — that would contaminate the comparison with tool-use variance unrelated to the skill).

### Determinism — what you can and cannot pin

Claude's API/CLI **exposes no `temperature` or `seed` flag** in `-p` mode (confirmed absent from the CLI reference; this is a stable fact across Claude Code versions, not new in 2026). This means true bit-for-bit determinism is not achievable. What *is* achievable, and what the reference implementation already does correctly:

1. **Pin `--model` to an exact model string**, not an alias (`claude-sonnet-5`, not `sonnet`) — aliases can silently move underneath you as Anthropic ships updates.
2. **Pin `--effort`** explicitly and **record it in every raw result file** — SimpleEnglish's own `RESULTS.md` shows effort alone moves the headline number from 85.0% to 90.2% on the same model/scenarios. This is the single most important reproducibility control in the whole harness.
3. **Run more than one generation per cell** if variance matters — the reference implementation is explicit that it does *not* do this ("One generation per cell... re-run the matrix for variance") and states that honestly as a caveat. Proof First's harness should either do the same (cheap, single-shot, disclosed limitation) or budget for N≥3 repeats and report a spread — a stronger claim, but 3-8x the cost. Given the project's evidence standard ("measured claims or no claims"), N≥3 with a reported range is the more defensible default if budget allows; single-shot-with-disclosed-limitation is the acceptable fallback, matching precedent.
4. Use `--bare` (see above) so ambient project state can't leak nondeterminism in.

### Raw-result JSON structure

The reference implementation's shape is sound and should be kept close to verbatim — one JSON file per (model, condition, scenario) cell, resumable (skip if the file exists), containing: `text`, token/cost fields, `effort`, `duration_ms`, plus the harness's own metadata (`model`, `condition`, `scenario`, `type`, and the linter's `lint` object nested inline). This makes every number in `RESULTS.md` traceable to one committed file — that traceability *is* the reproducibility story, more than any specific tool choice. Recommended additions for Proof First specifically, given the extra scrutiny a "no fabricated evidence" skill invites:
- Record the **exact scenario prompt text** inline in the raw file (not just a scenario ID), so a reader auditing a specific number doesn't have to cross-reference a separate `scenarios.json` that could drift.
- Record a **git commit SHA** of the `SKILL.md` used, since presales skills are more likely to be actively iterated post-launch than a stable linguistic standard — a violations number is meaningless without knowing which `SKILL.md` revision produced it.

## 4. Deterministic linting — stdlib regex vs. spaCy/textstat

**Recommendation: stay stdlib-only regex for the linter itself. Confidence: MEDIUM-HIGH** (this is an engineering judgment call, not a fact I can verify against a spec — flagging accordingly).

**Why stdlib regex still wins for this project, even though its targets are harder:**

- **The project's own constraints already decided this.** PROJECT.md states "Dependencies: Zero... no install step" and lists "A deterministic linter that counts observable proxies for the rules" as a v1 requirement modeled explicitly on SimpleEnglish's own linter, which states in its docstring that it is "a regex pass, not a grammar parser" and that this is a known, disclosed ceiling rather than a defect. Reproducibility of the benchmark two years from now depends on `python3 evals/lint.py --self-test` working with nothing but a system Python — that property is worth more to a credibility-first repo than a few points of linter recall.
- **spaCy would break that property for the eval harness.** A `pip install spacy` plus `python -m spacy download en_core_web_sm` is a ~15-50MB+ dependency and model download before the linter runs at all — turning "clone and run" into "clone, install, download a model, then run." For a repo whose entire pitch is "one folder, no dependencies," this is a real cost, not a style preference, even if scoped to `evals/` and not the skill itself.
- **The two specific targets called out in the question — unquantified superlatives and claims with no adjacent number — are both approximable with regex at acceptable precision for a *comparative* (not absolute) benchmark:**
  - *Unquantified superlatives*: a hand-built list of superlative forms (`\b\w+est\b` for morphological superlatives, plus an explicit list for irregular/periphrastic ones: `best|worst|most|least|fastest|leading|premier|unmatched|unrivaled|world-class|industry-leading|cutting-edge|state-of-the-art|next-generation`) catches the overwhelming majority of presales puffery. This is exactly the same tactic SimpleEnglish's `SLOP` regex already uses for a different word list, just extended for a different violation class.
  - *Claims with no adjacent number*: approximate with a regex that flags sentences matching a "claim pattern" (a superlative, a comparative, or one of a small set of claim verbs — `reduce|improve|increase|accelerate|save|cut|eliminate`) **and** checks whether a numeral, percent sign, or unit token (`\d`) appears within the same sentence. This is a token-window heuristic, not true semantic claim extraction, but — critically — **the linter's job here is to produce a comparable proxy number for baseline-vs-skill, not a compliance verdict.** Both conditions get run through the identical regex, so systematic undercounting cancels out in the comparison, exactly the argument SimpleEnglish's own `RESULTS.md` makes ("it counts the same way for both conditions, so the comparison is fair even where the absolute numbers are low").
- **Where spaCy would actually help — and where it wouldn't be worth it even so:** a POS tagger reliably distinguishes an adjective's superlative morphology (`JJS`/`RBS` tags) from a proper noun or an -est word that isn't a superlative at all, and named-entity/numeric typing (`like_num`, `ent_type_ in {CARDINAL, PERCENT, MONEY, QUANTITY}`) is strictly more precise than a bare `\d` regex for "is there a number here." But the actual hard part of this project's anchor rule — the **deletion test** ("is this term legal because deleting it changes technical meaning, or a buzzword because the sentence survives deletion intact") — is a semantic judgment no off-the-shelf NLP library performs either. Since the linter was never going to check the deletion test directly (the project's own Context section states this explicitly, mirroring SimpleEnglish's own linter/standard split), the marginal precision spaCy buys on superlative/number detection doesn't change what the linter can actually claim. You'd be paying the dependency cost to slightly better-approximate something you're already treating as a proxy, not a verdict.
- **Where the honest ceiling should be disclosed** (again, following the SimpleEnglish precedent of a docstring stating limits plainly): this linter undercounts semantic buzzwords with no morphological or listable signature (a truly novel piece of jargon has no regex to catch it), and it will false-positive on legitimate superlatives that *are* backed by an adjacent number three sentences later rather than in the same sentence. State this in the linter's own header, exactly as SimpleEnglish does.
- **`textstat` as a bolt-on, not a replacement:** if the team wants an externally-recognized number in `RESULTS.md` (Flesch Reading Ease, average sentence length) alongside the custom violation count, `textstat` is actively maintained (repo activity as recently as Feb 2026) and adds one well-known `pip install textstat` — a smaller, more justifiable dependency than spaCy because it's a pure-Python metrics library with no model download. Still: make it optional/additive in `evals/`, never a hard dependency for reproducing the headline number, and never anywhere near the skill itself.

**What NOT to use:** a maintained buzzword blocklist as the *linter's* source of truth for "is this a violation" — this repeats the exact mistake the project's own design section (PROJECT.md) already rejected for the *skill's* rule (a blocklist needs endless maintenance and gets real technical nouns wrong in both directions). The linter's word lists should be understood as a narrow, disclosed proxy for benchmarking, never advertised as the deletion-test itself.

## 5. Blind pairwise LLM-judge methodology

Corroborated across multiple 2026 academic and practitioner sources on LLM-as-judge position bias (MEDIUM-HIGH confidence — consistent findings across arXiv survey papers and independent practitioner write-ups, no single canonical "best practice" doc, but strong convergence).

**Position bias is real and large.** Documented bias magnitude in the literature: judges can favor whichever response is shown in a given position by 10-15 percentage points, with position-consistency issues reported in 60-75% of cases across studied setups. Any single-order pairwise judge run is not trustworthy on its own — this validates SimpleEnglish's `run_bench.py` design (`order1_base_first` / `order2_skill_first`, averaged) rather than being a gap in it.

**Recommended judge protocol for Proof First, keeping SimpleEnglish's core design and adding two refinements the literature calls out:**

1. **Run every pair in both orders** and average per-item scores (score-based swap augmentation) — already correct in the reference implementation. Keep this.
2. **Strip labels/identity before judging.** The reference implementation already does this correctly by sending bare `TEXT A` / `TEXT B` with no model name, condition name, or ordering hint in the prompt — preserve this. Do not let the judge prompt leak which text came from the skill condition.
3. **Add explicit calibration language to the rubric prompt** — the literature specifically recommends telling the judge directly not to let position influence its score (e.g., "Your evaluation must not be influenced by the order in which the texts are presented"). SimpleEnglish's rubric prompt doesn't currently include this instruction; it's a one-line addition worth making.
4. **Force a rationale before the verdict** (chain-of-thought before score) reduces reliance on superficial positional or stylistic cues, per multiple surveyed mitigation techniques. SimpleEnglish's rubric asks for JSON-only scores with no rationale field — consider adding a short `"rationale"` string to the judge's required JSON output. This costs a few output tokens per call but gives you an auditable trail for every score in the raw judge files, which matters more for Proof First than for SimpleEnglish: a persuasion-quality judge call is inherently softer/more contestable than an STE mechanical-clarity judge call, so a visible rationale is what lets a skeptical reader trust the number instead of just the score.
5. **Rubric design for Proof First specifically:** SimpleEnglish's rubric asks 3 yes/no-flavored questions tuned to STE (misreadability, executability, slop). Proof First's rubric should be built the same way — a small, fixed set of criteria mapped 1:1 to the skill's actual claims, not a generic "which is better written" question (a generic question reintroduces exactly the vibes-based judgment the project is trying to avoid). Suggested axes, each scored independently and summed or averaged: (a) does the opening reframe the buyer's problem rather than list capabilities (Challenger), (b) is every claim of value tied to a metric or proof point rather than an adjective (Command of the Message / integrity), (c) would a technical evaluator read this and believe the author understands their environment. Keep the rubric small — 3-4 axes, same order of magnitude as SimpleEnglish's 3 — a long rubric list re-introduces subjective aggregation problems the pairwise-average design is meant to avoid.
6. **Report ties honestly and report the caveats block SimpleEnglish already models well:** one judge model (family bias against/for its own outputs is a known confound when judge and generator share a vendor — flag this explicitly, as the reference implementation already does), N=1 judgment per order (no variance measurement across repeated judge calls), and effort-level consistency across judge calls (the reference implementation flags historical judge files that predate effort-pinning as a known inconsistency — carry the same discipline forward from day one instead of retrofitting it).
7. **Consider one additional judge model for a cross-check**, if budget allows — using a judge from a different vendor family than the models being benchmarked reduces (does not eliminate) family-bias risk, and the literature's "ensemble judging across orderings/judges" recommendation applies here. This is a nice-to-have, not a blocker for v1; SimpleEnglish ships without it and states the limitation instead, which is an acceptable, honest v1 posture.

## 6. Repo hygiene

Confirmed by direct inspection of the SimpleEnglish reference repo (HIGH confidence — this is the working precedent, not a claim from search):

- **MIT `LICENSE`** at repo root — matches PROJECT.md's stated legal posture and the trademark-neutrality requirement for the three proprietary frameworks it paraphrases (Command of the Message, MEDDICC, Challenger).
- **CI: a single self-test job.** SimpleEnglish's linter ships a `--self-test` mode with fixture text engineered to trip every violation category plus a clean fixture that must score zero (`assert ... == 0`). The entire CI surface for a zero-dependency repo is one GitHub Actions job running `python3 evals/lint.py --self-test` on every push/PR — no build matrix, no package manager, nothing else needed. Proof First should do exactly this for its own linter, sized to whatever violation categories it ends up counting (superlatives, unquantified claims, hedges, sentence length, passive voice, etc.).
- **README built on before/after pairs** — this is SimpleEnglish's actual marketing mechanism (a reader decides whether to install a skill from the README's examples, not from reading `SKILL.md`), and PROJECT.md already states this is the intended strategy for Proof First.
- **A committed, reproducible `RESULTS.md`** generated by the benchmark runner, with the "Honest number warnings" section as a first-class, permanent part of the file rather than something that gets trimmed once results look good — this is what makes the "measured claims or no claims" constraint self-enforcing rather than aspirational.
- **Non-affiliation / trademark disclaimer,** stated once, plainly, near wherever Command of the Message / MEDDICC / Challenger are first named — the same posture SimpleEnglish takes toward ASD-STE100 and asd-ste100.org, applied to three rights-holders instead of one, per PROJECT.md's own constraint.
- **What SimpleEnglish does *not* have, and Proof First likely doesn't need either:** a `package.json`/build step, a test framework beyond the linter's own self-test, a `CONTRIBUTING.md`, or a versioning/release-automation pipeline. Adding any of these would be scope creep relative to the "one folder, no dependencies" model this project is explicitly copying.

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| A separate build/publish pipeline (npm package, PyPI package, compiled binary) for the skill itself | Contradicts the explicit "one folder, no install step" constraint and the entire distribution model this project is copying | Plain files: `SKILL.md`, `references/*.md`, `output-styles/*.md`, `.claude-plugin/*.json` — all hand-authored, no tooling |
| A maintained buzzword blocklist as the skill's core anti-slop mechanism | The project's own design already rejected this (endless maintenance, wrong in both directions); repeating it in the linter just moves the same mistake into eval tooling | The deletion test (skill) + a small, explicitly-labeled regex proxy list (linter only, disclosed as a proxy, not the standard) |
| spaCy (or any model-download NLP dependency) inside the shipped skill or as a hard dependency of the eval harness | Breaks reproducibility/zero-dependency posture for marginal precision gain on a problem (semantic buzzword detection) that no library solves anyway | stdlib `re`, with `textstat` as a fully optional bolt-on metric only |
| Single-order LLM judging (only one of A-vs-B or B-vs-A) | Position bias in pairwise LLM judging is well-documented at 10-15 point magnitude; a single order is not a reliable signal | Both-orders swap + averaging, exactly as the reference implementation already does |
| `temperature`/`seed` flags on Claude Code CLI for "determinism" | These flags do not exist in `-p` mode — attempting to rely on them will simply fail or be silently ignored depending on version | Pin `--model` (exact string) + `--effort` (recorded per raw file) + `--bare`; accept and disclose that true determinism isn't available, and increase N if variance matters |
| Inventing a `compatibility:` value shaped like a harness list (e.g. `claude-code cursor codex...`) as if it were a structured field | The agentskills.io spec treats `compatibility` as free-text prose about environment requirements, not a structured harness-compatibility list; there is no field the agent itself reads to advertise "works on these harnesses" | State cross-harness compatibility in the README/marketplace description for humans; omit `compatibility` from frontmatter entirely per the spec's own guidance that most skills don't need it |

## Version Compatibility

| Package/Tool | Compatible With | Notes |
|-----------|-----------------|-------|
| Agent Skills spec frontmatter | Claude Code, Cursor, Codex, Copilot, Gemini CLI, OpenCode, Goose, and dozens more via `skills` CLI | No version pin on the spec itself; it's additive/backward-compatible by design (unknown optional keys are the only thing that breaks — stick to the six documented frontmatter keys) |
| `--bare` flag | Claude Code CLI v2.1.x line (exact floor not stated in docs; assume any 2026-era release) | Not present in the SimpleEnglish reference implementation's `run_bench.py` — an intentional deviation recommended above, not a bug in the reference |
| `--permission-prompts none` | Requires Claude Code v2.1.259+ | Only relevant if the benchmark runner needs unattended permission handling beyond `--disallowedTools` |
| `keep-coding-instructions` / `force-for-plugin` output-style fields | Documented in current output-styles page; `force-for-plugin` is plugin-scoped only | Proof First likely wants neither `true` (it's a writing persona, not a coding-instruction layer, and users should opt in rather than have it forced) |
| claude.ai upload description length | 200 chars (help center) vs. 1024 chars (agentskills.io spec) | Unreconciled discrepancy between two official-ish sources — write descriptions ≤200 chars to be safe everywhere; LOW confidence on the exact claude.ai number, worth a manual smoke test |

## Sources

- `https://agentskills.io/specification` — fetched directly. Full frontmatter schema, progressive disclosure token/line budget, `references/`/`scripts/`/`assets/` conventions, validation via `skills-ref`. HIGH confidence.
- `https://github.com/vercel-labs/skills` — fetched directly. CLI command syntax, discovery paths, agent installation mapping. HIGH confidence on syntax, MEDIUM on the full discovery-path list.
- `https://code.claude.com/docs/en/plugin-marketplaces` — fetched directly. `marketplace.json`/`plugin.json` required fields and example. HIGH confidence.
- `https://github.com/hesreallyhim/claude-code-json-schema` — unofficial but actively maintained JSON Schema project, used to corroborate the long tail of optional plugin/marketplace fields. MEDIUM confidence (community source).
- `https://code.claude.com/docs/en/output-styles` — fetched directly. Output style file format, frontmatter fields, load-order rules. HIGH confidence.
- `https://code.claude.com/docs/en/headless` — fetched directly. `-p`/`--print` mode, `--bare`, streaming, structured output, permission flags. HIGH confidence.
- `https://code.claude.com/docs/en/cli-reference` (via targeted fetch) — `--model`, `--effort` levels, `--disallowedTools`, `--json-schema`, system-prompt flags. HIGH confidence on documented flags; the `ultracode` effort level mentioned in one synthesis pass is UNVERIFIED and excluded from recommendations.
- `https://support.claude.com/en/articles/12512198-how-to-create-custom-skills` — fetched directly. claude.ai ZIP upload structure and the 200-char description figure. MEDIUM-HIGH confidence (official help center, but conflicts with the agentskills.io 1024-char figure — flagged, not resolved).
- Web search corroboration (Anthropic news posts, cometapi.com) confirming `claude-sonnet-5` (released 2026-06-30) and `claude-opus-5` (released 2026-07-24) are real, current model identifiers matching the reference implementation's `run_bench.py` model list. MEDIUM-HIGH confidence.
- arXiv survey/position-bias literature (`arxiv.org/html/2602.02219v2` and related 2025-2026 LLM-as-judge surveys) — position bias magnitude, swap-augmentation and calibration-prompt mitigations. MEDIUM-HIGH confidence (converging findings, no single canonical source).
- Direct inspection of the local SimpleEnglish checkout (`~/devoteam/.claude/plugins/marketplaces/simple-english/`) — used as the working baseline throughout, per the task's reference-implementation instructions. HIGH confidence (primary source, read directly).
- `textstat` PyPI/GitHub activity — actively maintained as of Feb 2026. MEDIUM confidence (search-synthesis, not directly fetched from PyPI).
- No canonical, single-source comparison of stdlib regex vs. spaCy/textstat specifically for superlative/claim-number detection exists in the literature; the recommendation in Section 4 is this agent's engineering judgment applied to the project's stated constraints, not a verified external claim. Flagged as such inline.

---
*Stack research for: Public cross-harness AI agent skill (technical presales writing) — Proof First*
*Researched: 2026-09-10*
