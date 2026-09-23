<!-- GSD:project-start source:PROJECT.md -->

## Project

**Proof First**

Proof First is a public, MIT-licensed agent skill that makes AI write technical presales documents a buyer will actually believe. It covers RFP/RFI responses, solution proposals, executive summaries, and demo/discovery material: writing that has to be commercially persuasive without reading like a brochure or an LLM.

It occupies the territory that [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) explicitly refuses. That skill's closing section says STE "deletes persuasion by design" and sends marketing writing away. Proof First is the sibling that takes those documents and makes them persuasive the only way that survives a technical evaluator: through specificity and evidence instead of adjectives.

It is for presales engineers, solution architects, and bid teams: vendor-neutral, usable by anyone, distributed the same way SimpleEnglish is (skills CLI, Claude Code plugin marketplace, output style, and a paste-able system prompt).

**Core Value:** **A technical evaluator finishes the document believing the author genuinely understands their problem: because complex things were made simple without being made wrong.**

Everything yields to this. Simplification that costs technical accuracy fails. Accuracy that the reader cannot follow fails. Persuasion that a competent engineer can smell as marketing fails hardest of all, because it destroys the trust the rest of the document was spending.

The secondary job, downstream of trust: make the decision easy: remove the buyer's reasons to hesitate about risk, cost, effort, and whether the vendor can actually do it.

### Constraints

- **Legal**: All three anchor frameworks are proprietary and trademarked (Force Management, Challenger Inc., and the MEDDIC training vendors). Adopt the SimpleEnglish posture exactly: name them, paraphrase concepts only, reproduce zero proprietary text, state non-affiliation and trademark ownership explicitly, MIT license the repo.
- **Dependencies**: Zero. One folder, no install step, no dependency on simple-english even though it is the sibling skill. The prose mechanics must be restated self-contained.
- **Compatibility**: Agent Skills standard, so it works across Claude Code, Cursor, Codex, Copilot, Gemini CLI, OpenCode and the rest. Plus a paste-able system prompt for harnesses with no skill support.
- **Evidence**: The repo makes measured claims or no claims. Any headline number must be reproducible from a committed script, with honest caveats stated: the same standard the skill demands of its users. Anything less would be the exact failure the skill exists to prevent.
- **Voice**: The skill must stay commercially attractive while banning buzzwords. Flat, STE-style prose is a failure mode here, not a goal: persuasion has to survive.

<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->

## Technology Stack

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Agent Skills standard (agentskills.io) | Current spec, no version number published: treat as a living spec | Portable skill format: `SKILL.md` + optional `scripts/`, `references/`, `assets/` | This is the only format that is genuinely cross-harness in 2026. It is consumed natively by Claude Code, Cursor, Codex, GitHub Copilot, Gemini CLI, OpenCode, Goose, and dozens more via the `skills` CLI ecosystem. Building anything harness-specific (e.g. a Cursor-only rules file) forfeits the reach the project explicitly wants. |
| `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` | Current Claude Code plugin schema (no version pin; schema is additive, backward compatible) | Distribution through the Claude Code plugin marketplace mechanism | Second distribution channel, proven by SimpleEnglish. Zero build step: the files are hand-written JSON, no compiler, no publish pipeline. |
| `output-styles/*.md` | Claude Code v2.1+ output style format | A "persona" mode that changes how Claude Code talks for an entire session, not just one skill invocation | Gives users a way to force Proof First's voice by default rather than relying on the model to decide the skill is relevant. Zero-dependency, one Markdown file. |
| Python 3 (stdlib only: `re`, `json`, `sys`, `argparse`, `pathlib`, `subprocess`, `time`, `itertools`, `datetime`) | 3.11+ (3.13 current stable as of 2026; anything 3.9+ will run this code unchanged) | The eval harness: linter + benchmark runner + judge runner | Matches the project's own "zero dependencies" constraint and SimpleEnglish's precedent exactly. A `pip install` step is one more thing that can silently break reproducibility for someone trying to reproduce the headline number two years from now; stdlib-only means `python3 script.py` works forever with no lockfile. |
| Claude Code CLI (logged-in, subscription auth) | Whatever is on the user's PATH; no version pin needed for `-p` mode itself, but note flags below have version floors | Headless model driver for the primary benchmark matrix | No API key needed (uses the CLI's own OAuth login), so the benchmark is runnable by anyone with a Claude subscription: the same bar SimpleEnglish set. |
| A second, harness-agnostic CLI (the reference implementation uses **Pi**; **OpenCode** or the **Claude Agent SDK** in Python/TS are equally valid substitutes) | N/A | Cross-provider benchmark runner, so the headline number isn't "only tested on Claude" | The project's `PITFALLS.md`/`FEATURES.md` should flag this, but for STACK purposes: pick one non-Anthropic-hosted runner that can disable ambient skills/tools/context (`--no-tools --no-skills --no-context-files` in Pi's case) so the baseline condition is genuinely a clean baseline. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| None (stdlib `re`) |: | Deterministic violation counting | Default choice: see the dedicated linting analysis below. |
| `textstat` | latest on PyPI (actively maintained; last commit Feb 2026 per repo activity) | Optional supplementary readability metrics (Flesch Reading Ease, sentence-length distributions) reported alongside the custom linter | Only if you want a second, externally-recognized number in `RESULTS.md` for readers who trust a named library more than a bespoke regex. Not a replacement for the custom linter: it does not detect superlatives, buzzwords, or claim/number adjacency, which are this project's actual targets. |
| `spaCy` | N/A: **not recommended**, see analysis below | POS-tagged superlative detection, numeric entity detection | Only if a future phase needs true grammatical disambiguation (e.g., distinguishing "the fastest car" as a fact vs. "the best solution" as an unquantified claim) and the team accepts a ~500MB model download breaking the zero-dependency posture for the eval harness specifically (not the skill itself, which stays dependency-free regardless). |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| GitHub Actions | CI for `ste`-style `--self-test` linter mode | One job, no matrix needed: `python3 evals/lint.py --self-test`. Runs on every push/PR. This is the entire CI surface for a zero-dependency repo: no package manager, no build, nothing else to test in CI. |
| `skills-ref` (agentskills/agentskills reference library) | Validates `SKILL.md` frontmatter against the spec (`skills-ref validate ./skill-dir`) | Run this locally (or add as a second CI job if the runner environment can fetch it) before every release. It is the closest thing to an official conformance check and catches the exact class of error that silently breaks distribution: name/description length, hyphen rules, frontmatter key allow-list. |
| MIT `LICENSE` file at repo root | Legal | Matches SimpleEnglish and the project's own stated constraint. |

## Installation

# Core: nothing to install for the skill itself (zero dependencies, by design)

# Eval harness: nothing to install either (stdlib-only Python 3.11+)

# Optional, only if you add the supplementary readability metric

# CI

# .github/workflows/ci.yml: no install step, just:

## 1. The Agent Skills standard: canonical spec and schema

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | 1–64 chars. Lowercase unicode alphanumerics and hyphens only. No leading/trailing hyphen, no `--`. **Must match the parent directory name.** |
| `description` | Yes | 1–1024 chars, non-empty. Must describe *what* it does and *when* to use it: this is the only field an idle agent reads at startup, so keyword density matters for activation. |
| `license` | No | License name or a pointer to a bundled license file. |
| `compatibility` | No | 1–500 chars. Free text describing environment requirements ("Requires git, docker, jq..."). Most skills should omit it. |
| `metadata` | No | Free-form string→string map (author, version, etc.). Clients may use it; the spec itself ignores it. |
| `allowed-tools` | No | Space-separated string of pre-approved tools. Marked **experimental**: support varies by harness. |

## 2. Distribution channels: exact schemas

### `skills` CLI (vercel-labs/skills, `npx skills`)

### Claude Code plugin marketplace: `plugin.json` and `marketplace.json`

### Claude Code output styles

- **Location for a plugin-shipped style:** `output-styles/` at the plugin root (SimpleEnglish ships `output-styles/simple-english.md`; Proof First should mirror this at `output-styles/proof-first.md`).
- **Format:** Markdown file, YAML frontmatter + instruction body.
- **Frontmatter fields:**

| Field | Purpose | Default |
|---|---|---|
| `name` | Style name if different from filename | filename |
| `description` | Shown in the `/config` picker | none |
| `keep-coding-instructions` | Keep Claude Code's built-in software-engineering system prompt underneath your style | `false` |
| `force-for-plugin` | Auto-apply this style whenever the plugin is enabled, no user selection needed (plugin output styles only) | `false` |

### claude.ai skill upload

- Path: **Customize → Skills → + → Upload** (web, desktop, and mobile apps).
- The ZIP must have the **skill folder as its root**: not the bare `SKILL.md`, not a nested wrapper folder.
- **Requires "Code execution" enabled** under Settings → Capabilities (Free/Pro/Max/Team/Enterprise).
- One official help article states a stricter **200-character cap on `description`** for claude.ai uploads, versus 1024 in the general agentskills.io spec. This is a real discrepancy between two official-ish sources and I could not fully reconcile it: **treat 200 chars as the safe ceiling** if claude.ai upload matters to the project, even though the general spec and Claude Code itself will accept up to 1024. (Confidence: LOW on the exact number, MEDIUM that *some* tighter description limit applies on claude.ai specifically: worth a manual smoke test before shipping v1.)

## 3. Eval harness tooling: reproducible baseline-vs-skill benchmark

### Headless invocation (Claude Code CLI)

- **`--bare` is the flag to add for benchmark determinism** and didn't exist when SimpleEnglish's `run_bench.py` was written (it only sets `cwd="/tmp"` and disallows tools). `--bare` skips auto-discovery of hooks, skills, custom commands, subagents, plugins, MCP servers, auto memory, and `CLAUDE.md`: i.e. it guarantees the benchmark isn't accidentally picking up a hook or a stray project-level skill from wherever the harness runs. Docs explicitly say **this is becoming the default for `-p` in a future release** and is "the recommended mode for scripted and SDK calls." Because `--bare` skips OAuth/keychain reading, pair it with `ANTHROPIC_API_KEY` set in the environment rather than relying on subscription login: this is a tradeoff against the reference implementation's "no API key needed" claim, and should be stated as a caveat if adopted.
- **Effort levels confirmed:** `low`, `medium`, `high`, `xhigh`, `max` (the reference implementation's own `RESULTS.md` text cites measured numbers at `low` and `xhigh`, corroborating both exist). One source additionally mentioned an `ultracode` level; I could not independently corroborate this and **do not recommend relying on it**: treat it as unverified.
- **`--json-schema`** (added since the reference implementation was written) can enforce that the model's output actually matches an expected shape, e.g. forcing structured `{"text": "..."}` output instead of parsing free text out of `result`. Not required, but reduces one class of parsing failure in the benchmark runner.
- **`--disallowedTools`** as SimpleEnglish uses it is still correct syntax and still the right call for a pure-writing benchmark (baseline and skill conditions should not be allowed to shell out or read files: that would contaminate the comparison with tool-use variance unrelated to the skill).

### Determinism: what you can and cannot pin

### Raw-result JSON structure

- Record the **exact scenario prompt text** inline in the raw file (not just a scenario ID), so a reader auditing a specific number doesn't have to cross-reference a separate `scenarios.json` that could drift.
- Record a **git commit SHA** of the `SKILL.md` used, since presales skills are more likely to be actively iterated post-launch than a stable linguistic standard: a violations number is meaningless without knowing which `SKILL.md` revision produced it.

## 4. Deterministic linting: stdlib regex vs. spaCy/textstat

- **The project's own constraints already decided this.** PROJECT.md states "Dependencies: Zero... no install step" and lists "A deterministic linter that counts observable proxies for the rules" as a v1 requirement modeled explicitly on SimpleEnglish's own linter, which states in its docstring that it is "a regex pass, not a grammar parser" and that this is a known, disclosed ceiling rather than a defect. Reproducibility of the benchmark two years from now depends on `python3 evals/lint.py --self-test` working with nothing but a system Python: that property is worth more to a credibility-first repo than a few points of linter recall.
- **spaCy would break that property for the eval harness.** A `pip install spacy` plus `python -m spacy download en_core_web_sm` is a ~15-50MB+ dependency and model download before the linter runs at all: turning "clone and run" into "clone, install, download a model, then run." For a repo whose entire pitch is "one folder, no dependencies," this is a real cost, not a style preference, even if scoped to `evals/` and not the skill itself.
- **The two specific targets called out in the question: unquantified superlatives and claims with no adjacent number: are both approximable with regex at acceptable precision for a *comparative* (not absolute) benchmark:**
- **Where spaCy would actually help: and where it wouldn't be worth it even so:** a POS tagger reliably distinguishes an adjective's superlative morphology (`JJS`/`RBS` tags) from a proper noun or an -est word that isn't a superlative at all, and named-entity/numeric typing (`like_num`, `ent_type_ in {CARDINAL, PERCENT, MONEY, QUANTITY}`) is strictly more precise than a bare `\d` regex for "is there a number here." But the actual hard part of this project's anchor rule: the **deletion test** ("is this term legal because deleting it changes technical meaning, or a buzzword because the sentence survives deletion intact"): is a semantic judgment no off-the-shelf NLP library performs either. Since the linter was never going to check the deletion test directly (the project's own Context section states this explicitly, mirroring SimpleEnglish's own linter/standard split), the marginal precision spaCy buys on superlative/number detection doesn't change what the linter can actually claim. You'd be paying the dependency cost to slightly better-approximate something you're already treating as a proxy, not a verdict.
- **Where the honest ceiling should be disclosed** (again, following the SimpleEnglish precedent of a docstring stating limits plainly): this linter undercounts semantic buzzwords with no morphological or listable signature (a truly novel piece of jargon has no regex to catch it), and it will false-positive on legitimate superlatives that *are* backed by an adjacent number three sentences later rather than in the same sentence. State this in the linter's own header, exactly as SimpleEnglish does.
- **`textstat` as a bolt-on, not a replacement:** if the team wants an externally-recognized number in `RESULTS.md` (Flesch Reading Ease, average sentence length) alongside the custom violation count, `textstat` is actively maintained (repo activity as recently as Feb 2026) and adds one well-known `pip install textstat`: a smaller, more justifiable dependency than spaCy because it's a pure-Python metrics library with no model download. Still: make it optional/additive in `evals/`, never a hard dependency for reproducing the headline number, and never anywhere near the skill itself.

## 5. Blind pairwise LLM-judge methodology

## 6. Repo hygiene

- **MIT `LICENSE`** at repo root: matches PROJECT.md's stated legal posture and the trademark-neutrality requirement for the three proprietary frameworks it paraphrases (Command of the Message, MEDDICC, Challenger).
- **CI: a single self-test job.** SimpleEnglish's linter ships a `--self-test` mode with fixture text engineered to trip every violation category plus a clean fixture that must score zero (`assert ... == 0`). The entire CI surface for a zero-dependency repo is one GitHub Actions job running `python3 evals/lint.py --self-test` on every push/PR: no build matrix, no package manager, nothing else needed. Proof First should do exactly this for its own linter, sized to whatever violation categories it ends up counting (superlatives, unquantified claims, hedges, sentence length, passive voice, etc.).
- **README built on before/after pairs**: this is SimpleEnglish's actual marketing mechanism (a reader decides whether to install a skill from the README's examples, not from reading `SKILL.md`), and PROJECT.md already states this is the intended strategy for Proof First.
- **A committed, reproducible `RESULTS.md`** generated by the benchmark runner, with the "Honest number warnings" section as a first-class, permanent part of the file rather than something that gets trimmed once results look good: this is what makes the "measured claims or no claims" constraint self-enforcing rather than aspirational.
- **Non-affiliation / trademark disclaimer,** stated once, plainly, near wherever Command of the Message / MEDDICC / Challenger are first named: the same posture SimpleEnglish takes toward ASD-STE100 and asd-ste100.org, applied to three rights-holders instead of one, per PROJECT.md's own constraint.
- **What SimpleEnglish does *not* have, and Proof First likely doesn't need either:** a `package.json`/build step, a test framework beyond the linter's own self-test, a `CONTRIBUTING.md`, or a versioning/release-automation pipeline. Adding any of these would be scope creep relative to the "one folder, no dependencies" model this project is explicitly copying.

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| A separate build/publish pipeline (npm package, PyPI package, compiled binary) for the skill itself | Contradicts the explicit "one folder, no install step" constraint and the entire distribution model this project is copying | Plain files: `SKILL.md`, `references/*.md`, `output-styles/*.md`, `.claude-plugin/*.json`: all hand-authored, no tooling |
| A maintained buzzword blocklist as the skill's core anti-slop mechanism | The project's own design already rejected this (endless maintenance, wrong in both directions); repeating it in the linter just moves the same mistake into eval tooling | The deletion test (skill) + a small, explicitly-labeled regex proxy list (linter only, disclosed as a proxy, not the standard) |
| spaCy (or any model-download NLP dependency) inside the shipped skill or as a hard dependency of the eval harness | Breaks reproducibility/zero-dependency posture for marginal precision gain on a problem (semantic buzzword detection) that no library solves anyway | stdlib `re`, with `textstat` as a fully optional bolt-on metric only |
| Single-order LLM judging (only one of A-vs-B or B-vs-A) | Position bias in pairwise LLM judging is well-documented at 10-15 point magnitude; a single order is not a reliable signal | Both-orders swap + averaging, exactly as the reference implementation already does |
| `temperature`/`seed` flags on Claude Code CLI for "determinism" | These flags do not exist in `-p` mode: attempting to rely on them will simply fail or be silently ignored depending on version | Pin `--model` (exact string) + `--effort` (recorded per raw file) + `--bare`; accept and disclose that true determinism isn't available, and increase N if variance matters |
| Inventing a `compatibility:` value shaped like a harness list (e.g. `claude-code cursor codex...`) as if it were a structured field | The agentskills.io spec treats `compatibility` as free-text prose about environment requirements, not a structured harness-compatibility list; there is no field the agent itself reads to advertise "works on these harnesses" | State cross-harness compatibility in the README/marketplace description for humans; omit `compatibility` from frontmatter entirely per the spec's own guidance that most skills don't need it |

## Version Compatibility

| Package/Tool | Compatible With | Notes |
|-----------|-----------------|-------|
| Agent Skills spec frontmatter | Claude Code, Cursor, Codex, Copilot, Gemini CLI, OpenCode, Goose, and dozens more via `skills` CLI | No version pin on the spec itself; it's additive/backward-compatible by design (unknown optional keys are the only thing that breaks: stick to the six documented frontmatter keys) |
| `--bare` flag | Claude Code CLI v2.1.x line (exact floor not stated in docs; assume any 2026-era release) | Not present in the SimpleEnglish reference implementation's `run_bench.py`: an intentional deviation recommended above, not a bug in the reference |
| `--permission-prompts none` | Requires Claude Code v2.1.259+ | Only relevant if the benchmark runner needs unattended permission handling beyond `--disallowedTools` |
| `keep-coding-instructions` / `force-for-plugin` output-style fields | Documented in current output-styles page; `force-for-plugin` is plugin-scoped only | Proof First likely wants neither `true` (it's a writing persona, not a coding-instruction layer, and users should opt in rather than have it forced) |
| claude.ai upload description length | 200 chars (help center) vs. 1024 chars (agentskills.io spec) | Unreconciled discrepancy between two official-ish sources: write descriptions ≤200 chars to be safe everywhere; LOW confidence on the exact claude.ai number, worth a manual smoke test |

## Sources

- `https://agentskills.io/specification`: fetched directly. Full frontmatter schema, progressive disclosure token/line budget, `references/`/`scripts/`/`assets/` conventions, validation via `skills-ref`. HIGH confidence.
- `https://github.com/vercel-labs/skills`: fetched directly. CLI command syntax, discovery paths, agent installation mapping. HIGH confidence on syntax, MEDIUM on the full discovery-path list.
- `https://code.claude.com/docs/en/plugin-marketplaces`: fetched directly. `marketplace.json`/`plugin.json` required fields and example. HIGH confidence.
- `https://github.com/hesreallyhim/claude-code-json-schema`: unofficial but actively maintained JSON Schema project, used to corroborate the long tail of optional plugin/marketplace fields. MEDIUM confidence (community source).
- `https://code.claude.com/docs/en/output-styles`: fetched directly. Output style file format, frontmatter fields, load-order rules. HIGH confidence.
- `https://code.claude.com/docs/en/headless`: fetched directly. `-p`/`--print` mode, `--bare`, streaming, structured output, permission flags. HIGH confidence.
- `https://code.claude.com/docs/en/cli-reference` (via targeted fetch): `--model`, `--effort` levels, `--disallowedTools`, `--json-schema`, system-prompt flags. HIGH confidence on documented flags; the `ultracode` effort level mentioned in one synthesis pass is UNVERIFIED and excluded from recommendations.
- `https://support.claude.com/en/articles/12512198-how-to-create-custom-skills`: fetched directly. claude.ai ZIP upload structure and the 200-char description figure. MEDIUM-HIGH confidence (official help center, but conflicts with the agentskills.io 1024-char figure: flagged, not resolved).
- Web search corroboration (Anthropic news posts, cometapi.com) confirming `claude-sonnet-5` (released 2026-06-30) and `claude-opus-5` (released 2026-07-24) are real, current model identifiers matching the reference implementation's `run_bench.py` model list. MEDIUM-HIGH confidence.
- arXiv survey/position-bias literature (`arxiv.org/html/2602.02219v2` and related 2025-2026 LLM-as-judge surveys): position bias magnitude, swap-augmentation and calibration-prompt mitigations. MEDIUM-HIGH confidence (converging findings, no single canonical source).
- Direct inspection of the local SimpleEnglish checkout (`~/cymarechal/.claude/plugins/marketplaces/simple-english/`): used as the working baseline throughout, per the task's reference-implementation instructions. HIGH confidence (primary source, read directly).
- `textstat` PyPI/GitHub activity: actively maintained as of Feb 2026. MEDIUM confidence (search-synthesis, not directly fetched from PyPI).
- No canonical, single-source comparison of stdlib regex vs. spaCy/textstat specifically for superlative/claim-number detection exists in the literature; the recommendation in Section 4 is this agent's engineering judgment applied to the project's stated constraints, not a verified external claim. Flagged as such inline.

<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->

## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
