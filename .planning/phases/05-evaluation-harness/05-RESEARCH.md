# Phase 5: Evaluation Harness - Research

**Researched:** 2026-09-18
**Domain:** Reproducible LLM-behavior benchmarking (stdlib-only linting + multi-model headless generation + blind pairwise LLM judging) for a Claude Code Agent Skill
**Confidence:** MEDIUM-HIGH — the repo's own conventions, prior art (Phase 3's conformance runner, SimpleEnglish's bench harness), and live CLI behavior are all directly verified this session; the cost/runtime arithmetic and the persuasion-rubric design are engineering judgment grounded in n=1-3 live samples, not a large-N measurement.

## Summary

Phase 5 has no CONTEXT.md, so this research resolves the eight open design decisions itself and hands the planner recommendations, not options. The phase adds three new instruments beside the two that already exist in `evals/` (`pressure-tests.md`, `conformance/run_conformance.py`): a **stdlib-only linter** with an externally-sourced buzzword/superlative proxy list (EVAL-01/02/03), a **committed scenario set** covering all four artifact families with its own fresh fictional deal — never the shared `examples/deal-brief.md` (EVAL-04), and a **multi-model, multi-repeat benchmark + blind pairwise judge** whose every generation and judgement is committed as JSON and whose headline numbers can be recomputed offline with one command (EVAL-05..EVAL-12).

Everything in this phase follows house style already established by `tools/check_repo.py` (self-test + mutation-test + docstring-declared ceilings) and `evals/conformance/run_conformance.py` (per-session isolated temp directories, `SessionFailedError` to keep a failed CLI call from being scored as data, write-then-flush durability, `git hash-object`-based skill versioning). The new benchmark runner should be **architecturally modeled on, but not literally share code with,** `run_conformance.py`: its own docstring states it is "deliberately narrower" than Phase 5's eventual harness (verified by reading the file in full this session), and its transcript-persistence policy (ephemeral by default) is the opposite of what EVAL-11 requires (raw JSON committed). SimpleEnglish's `run_bench.py`/`ste_lint.py` (the project's own named reference implementation) supply a second, corroborating precedent for nearly every design choice below, and this document names concretely what to copy, what to improve on, and what not to repeat.

Live testing this session (three real `claude -p` invocations, see Sources) falsified one part of `.claude/CLAUDE.md`'s existing stack notes: `--bare` **fails outright** in this environment ("Not logged in") because no `ANTHROPIC_API_KEY` is set and this project's actual auth is subscription OAuth — exactly the tradeoff CLAUDE.md flagged but did not resolve. The recommendation is to *not* adopt `--bare`, and to keep matching `run_conformance.py`'s existing OAuth-based invocation pattern.

**Primary recommendation:** Build three new files under `evals/` — `evals/lint.py` (linter + proxy provenance), `evals/proxy-sources.md` (the two-source, mechanically-checked provenance registry), and `evals/benchmark/run_benchmark.py` (scenario runner + judge, modeled on but not importing `run_conformance.py`) — with a minimal-but-complete live matrix of 2 models × 8 scenarios × 3 repeats × 2 conditions (96 generations + 96 judge calls), costing an estimated $40-55 and roughly 45-90 minutes of serial wall-clock, all committed to `evals/benchmark/raw/*.json` and aggregated into `evals/benchmark/RESULTS.md` via a `--report-only` mode that makes zero network calls.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Deterministic proxy-violation counting (EVAL-01/02/03) | Local stdlib script (`evals/lint.py`) | — | Pure text-in/JSON-out function; no network, no model call. Same tier as `tools/check_repo.py`. |
| Proxy-term provenance registry (EVAL-02) | Local flat file (`evals/proxy-sources.md`) + a mechanical checker | External published word lists (Wikipedia MOS, plainlanguage.gov) as the source of truth for term selection | The registry lives in-repo; the *authority* for what counts as a buzzword lives outside it, on purpose — that's what "independently sourced" means. |
| Scenario content (EVAL-04) | Local committed data (`evals/benchmark/scenarios.json`, `evals/benchmark/bench-deal-brief.md`) | — | No live dependency; must be stable across repeated runs so numbers are comparable over time. |
| Live generation (EVAL-05/06) | External API tier — Anthropic-hosted Claude models, reached via the locally-installed `claude` CLI in `-p` mode | Local orchestration script (`evals/benchmark/run_benchmark.py`) | The actual "skill effect" only exists as a live-model-behavior fact; the local script's job is orchestration, retry/failure handling, and durable recording, not judgment. |
| Blind pairwise judging (EVAL-07/08) | External API tier — a second Claude model invocation, judge-blind to labels | Local orchestration (same script) | Judging must happen in the same tier as generation (an LLM call) because no local heuristic can score "persuasive force"; the *labels-stripped* framing is what keeps this from re-becoming a local rule the harness could grade itself on. |
| Result publication (EVAL-09/10) | Local file (`evals/benchmark/RESULTS.md`), generated deterministically from committed raw JSON | — | Must be reproducible with **no** live/API tier involved — this is the offline recompute path EVAL-11+EVAL-12 jointly require (see Decision 7 and 8). |
| Raw artifact storage (EVAL-11) | Local filesystem, committed to git | — | Git is the durability and audit tier this project already uses for every other claim (`SOURCES.md`, `NUMBERING.md`); no external result store is introduced. |

## User Constraints

No CONTEXT.md exists for this phase. In its place, the following are the **hard constraints already fixed by the codebase and by `.planning/config.json`**, which this research treats with the same authority a locked CONTEXT.md decision would carry:

- Python 3 standard library only for anything on the reproduction path — no `pip install` step (`.claude/CLAUDE.md` § Constraints; `tools/check_repo.py` docstring, read in full: "It imports only the Python standard library; no package-manager dependency is introduced by this file or by the CI job that runs it.").
- `skills/proof-first/` stays dependency-free; nothing in `skills/` may import from `evals/`.
- Every headline number must be reproducible from a committed script with honest caveats stated; the repo makes measured claims or no claims (repeated verbatim across `README.md`, `PROJECT.md`'s Constraints, and every `evals/` docstring read this session).
- CI (`.github/workflows/ci.yml`, read in full) currently runs exactly:
  ```
  python3 tools/check_repo.py --self-test
  python3 tools/check_repo.py --mutation-test
  python3 tools/check_repo.py
  python3 evals/conformance/run_conformance.py --self-test
  python3 tools/generate_derivatives.py --check
  ```
  Phase 5 must add its own `--self-test` line(s) to this list, never a live/paid step (a live benchmark run must never be a CI gate — it costs real money and calls a live model on every push).
- `workflow.nyquist_validation: true` and `workflow.security_enforcement: true` are both set in `.planning/config.json` (read via Bash this session) — Validation Architecture and Security Domain sections are both required below, not optional.
- This is not a rename/refactor/migration phase — the Runtime State Inventory section is correctly omitted.

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EVAL-01 | "A deterministic linter counts rule-proxy violations using only the Python standard library, and passes its own self-test" | Decision analysis below + `evals/lint.py` design, modeled on `tools/check_repo.py`'s and SimpleEnglish's `ste_lint.py`'s self-test conventions |
| EVAL-02 | "The linter's buzzword proxy list is sourced independently of the skill's own worked examples, so measured improvement is not circular" | Decision 1 — two named external sources + a mechanical non-circularity checker |
| EVAL-03 | "The linter states plainly that the deletion test is a semantic judgment it cannot perform, and that its numbers are not a compliance verdict" | Decision 1 / Code Examples — disclaimer string pattern copied from `tools/check_repo.py`'s and `SOURCES.md`'s own house style |
| EVAL-04 | "A committed scenario set drives generations across all four artifact families" | Decision 2 — 8 scenarios (2/family), fresh fictional deal, no leakage into skill-off |
| EVAL-05 | "A benchmark runner drives multiple Claude models headlessly with the model string and reasoning effort pinned and recorded per result" | Decision 4 + Decision 7 (raw-record schema) |
| EVAL-06 | "Each benchmark cell runs at least three times, and published results report variance alongside the mean" | Decision 4 (matrix arithmetic) + "Statistical honesty for n=3" research item |
| EVAL-07 | "A blind pairwise judge scores skill-on against skill-off with labels stripped and both text orders run" | Decision 5 |
| EVAL-08 | "The judge rubric scores persuasive force as its own dimension, so a flat but clean draft cannot pass on clarity alone" | Decision 5 (3-dimension rubric) |
| EVAL-09 | "Published results report mechanical-proxy counts and judged persuasion as two separately labeled figures, never blended into one number" | Decision 8, item 6 — two-heading structural gate |
| EVAL-10 | "RESULTS.md carries an honest-caveats section naming position bias, judge family bias, baseline prompt parity, proxy provenance, and sample size" | Decisions 3, 5, 6, 8 collectively supply the five named caveats |
| EVAL-11 | "Every raw generation and judgement is committed as JSON so any published number can be recomputed from the repo" | Decision 7 — raw-record JSON schema |
| EVAL-12 | "A reader can reproduce the benchmark with one documented command" | Decision 6 (auth) + "offline recompute path" research item |

## The Eight Decisions

### Decision 1 — Proxy provenance (EVAL-02)

**Recommendation:** Source the buzzword/superlative proxy list from exactly two named, externally-published, non-affiliated lists, and enforce non-circularity with a mechanical checker rather than a promise.

- **Source A — Wikipedia:Manual of Style/Words to watch** (`https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch`, also referenced as `MOS:PUFFERY`/`MOS:WTW`). A community-maintained, independently curated list of "peacock terms" / puffery: unsupported superlatives such as *leading, premier, world-class, best-in-class, cutting-edge, state-of-the-art, unparalleled, revolutionary, landmark, iconic, renowned, acclaimed*. `[CITED: en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch]`
- **Source B — GSA plainlanguage.gov / digital.gov "Avoid jargon"** (`https://digital.gov/guides/plain-language/principles/avoid-jargon`; underlying word lists at `https://github.com/GSA/plainlanguage.gov/blob/main/_pages/guidelines/words/avoid-jargon.md`). A U.S. federal government resource, maintained under the Plain Writing Act of 2010, naming corporate-jargon terms: *robust, leverage, streamline, synergy, comprehensive, seamless, facilitate, utilize, impactful, solution*. `[CITED: digital.gov/guides/plain-language/principles/avoid-jargon]`

Both sources predate this project, are maintained by parties with no relationship to Proof First, and are the kind of source `SOURCES.md`'s own house rule already requires for framework concepts ("Every framework-derived concept... must trace to a source listed in this file" — `SOURCES.md`, read in full this session, line 7-9). Reuse that exact pattern for the linter's word list.

**Concrete artifact:** `evals/proxy-sources.md` — one row per proxy term/phrase, columns `Term | Source (A or B) | URL`. Exactly two allowed source labels (`A`, `B`), mirroring `NUMBERING.md`'s reserved-range-table style.

**Mechanical non-circularity check** (add to `evals/lint.py`'s own self-test-adjacent function, or as a new violation code in `tools/check_repo.py` if the planner prefers one checker to own all provenance claims — recommend the former, to keep `evals/` self-contained per the "never `skills/` importing from `evals/`" constraint's spirit):
1. `proxy-term-unsourced` — fires if any term in the linter's live `PROXY_TERMS` list has no row in `evals/proxy-sources.md`.
2. `proxy-term-source-invalid` — fires if a row's source label is anything other than `A` or `B`, or if the URL column does not start with `https://en.wikipedia.org/` (for `A`) or `https://digital.gov/` / `https://github.com/GSA/` (for `B`) — an explicit allow-list, not a free-text field, so a future contributor cannot silently add "worked-examples.md" as a "source."
3. `proxy-term-source-is-internal` — fires if any URL column resolves to a path inside this repository (a defense-in-depth check even though check 2 already forecloses it).

**Declared ceiling** (state this in the checker's own docstring, per house style): this cannot prove a human never *looked at* `worked-examples.md` while curating which external-list terms to include — that is the same class of semantic-judgment ceiling `SOURCES.md` itself already discloses for LEG-04 ("This is a semantic judgement — no tool in this project's stated stack performs it" — `SOURCES.md` line 18, read in full). What it *does* prove mechanically: every shipped term traces to one of exactly two named external sources, and none traces only to this repo's own content.

**Rejected alternative:** hand-curating a bespoke buzzword list from reading `worked-examples.md`'s own ✗ columns (fast, but is exactly the circularity EVAL-02 forbids — this project's own examples deliberately contain terms like "comprehensive," "best-in-class," "significant," "robust," "enterprise-grade," "fully governed" as ✗-column illustrations of PF-3.1/3.2, verified by reading `worked-examples.md` in full this session; using those same words as the *only* source of the linter's proxy list would let the skill's own authored examples silently become the measuring stick for the skill's own claimed improvement).

### Decision 2 — Scenario set shape (EVAL-04)

**Recommendation:** 8 scenarios, 2 per artifact family (RFP/RFI response, solution proposal, executive summary, demo/discovery material — the four family names are `artifact-patterns.md`'s own headings, read in full this session), each a self-contained prompt with no proof-first vocabulary (no "PF-", "MC-", "deletion test," "buzzword," "gap marker" anywhere in scenario text), grounded in a **fresh, separate fictional deal** — not `examples/deal-brief.md`'s Halverton Mutual.

**Concrete artifacts:**
- `evals/benchmark/bench-deal-brief.md` — a new fictional company/deal (different industry, different numbers, different names from Halverton Mutual/Kestrel Systems Group), giving each scenario enough concrete facts (a customer name, a workload, a dollar figure, a timeline, a named buyer priority) that PF-1.x/MC- rules have real material to apply to. Because scenario-generation sessions run in isolated temp directories with no filesystem access outside their own copy (see Decision 6), the relevant facts must be embedded **inline in each scenario prompt**, not referenced by path.
- `evals/benchmark/scenarios.json` — shape modeled directly on SimpleEnglish's `evals/scenarios.json` (read in full this session): `{"id": ..., "family": "rfp-rfi" | "solution-proposal" | "executive-summary" | "demo-discovery", "prompt": "..."}`.

**Why not `examples/deal-brief.md`:** every fact in `examples/deal-brief.md` is already baked into every worked ✗/✓ pair in `worked-examples.md` and `examples/before-after.md` — both of which ship as reference material the skill reads (`worked-examples.md` is explicitly listed as a reference file in `SKILL.md`'s own "Reference files" section, read in full this session: "Before writing or checking a ✗/✓ contrast for a rule, read `references/worked-examples.md`"). If benchmark scenarios reused Halverton Mutual's exact facts, a skill-on session could reproduce memorized-pattern phrasing from its own shipped examples rather than demonstrating that the rules generalize to a document the model has never seen phrased this way before — the same non-circularity concern EVAL-02 raises for the linter, applied to the benchmark itself. A fresh deal tests transfer, which is the more credible claim.

**Leakage control:** scenario prompts stay in the register SimpleEnglish's own `scenarios.json` uses — plain task descriptions ("Write a two-paragraph executive summary for X, covering Y and Z. Return only the text.") — never mentioning rule IDs, "proof-first," or catalog vocabulary, so the skill-off condition is not accidentally cued toward disciplined prose by the prompt itself rather than by the skill.

**Rejected alternative:** grounding scenarios in `examples/deal-brief.md` for "consistency with the rest of the repo" — rejected for the memorization-contamination reason above; consistency is not free here, it is the exact failure mode EVAL-02 is written to prevent, generalized to a second measurement.

### Decision 3 — Baseline prompt parity (EVAL-10's named caveat)

**Recommendation:** skill-off = the scenario's bare task prompt, unmodified. Skill-on = the same prompt, preceded by the full skill content (mirroring `run_conformance.py`'s pattern of installing the real skill folder into an isolated `.claude/skills/proof-first/`, and SimpleEnglish's `build_prompt()` which for the `skill` condition prepends `SKILL.md`'s full text with "Follow these writing instructions exactly, including the self-check step").

**Rejected alternative:** a length/effort-matched generic "write persuasively, with evidence" instruction as the baseline. Rejected because writing that generic instruction requires the experimenter to invent *some* persuasion heuristic — and any such heuristic is either drawn from the same body of sales-writing craft Proof First paraphrases (recreating EVAL-02's circularity problem inside the control condition instead of solving it) or is an arbitrary made-up instruction whose similarity to Proof First's own rules is unknowable and uncontrolled. A bare prompt is the standard null/uninstructed control; it does not remove the parity gap, it makes the gap visible and honestly named, which is exactly what EVAL-10 asks for.

**The caveat to state verbatim in RESULTS.md's honest-caveats section:** the skill-off condition receives a materially shorter prompt (no skill text, no explicit instruction to attach evidence or watch sentence length) — the comparison measures "default unguided model behavior vs. skill-guided behavior," not "the best a careful human prompt-writer could get without the skill." This is a deliberate design choice, not an oversight, and it is the same choice SimpleEnglish's own `run_bench.py` makes (`build_prompt()`, read in full this session: `if condition == "baseline": return scenario["prompt"]`).

### Decision 4 — Model matrix and cost (EVAL-05, EVAL-06)

**Models:** `claude-sonnet-5` and `claude-opus-5` — both already used as this repo's two pinned models for the Phase 3 MOD-04 conformance runs (`evals/conformance/run_conformance.py`'s own `--models claude-sonnet-5,claude-opus-5` invocation is quoted directly in `REQUIREMENTS.md`'s MOD-04 entry, read in full this session), so this reuses existing repo precedent rather than introducing a third, previously-untested model. Both confirmed live and working on the machine this research ran on: `[VERIFIED: live claude -p invocation, this session]` — `claude -p "reply with exactly: OK" --model claude-sonnet-5 ...` returned `is_error: false`, and the identical call with `--model claude-opus-5` returned `is_error: false, result: "OK", canonical model: claude-opus-5`.

**Effort:** pin to `low` for the main run, following SimpleEnglish's own `DEFAULT_EFFORT = "low"` (`run_bench.py`, read in full), with the caveat SimpleEnglish's own `RESULTS.md` names verbatim and this project should reuse: effort moves the numbers substantially (SimpleEnglish measured "85.0% at `low` and 90.2% at `xhigh`" for the same scenarios, read in full from `evals/results/RESULTS.md`). A 1-2 scenario spot-check at `high` or `xhigh` is a reasonable optional addition to the caveats section, not required for the headline number.

**Matrix:** 8 scenarios × 2 models × 3 repeats (the EVAL-06 floor) × 2 conditions (skill-on/skill-off) = **96 generations**. Judge pairs = 8 × 2 × 3 = 48 skill-on/skill-off pairs; both orders run per EVAL-07 = **96 judge calls**. Total live invocations = **192**.

**Cost and wall-clock arithmetic — grounded in three live invocations run this session, not an adjective:**

| Call | Context | Cost | Output tokens | Wall time |
|---|---|---|---|---|
| `claude -p "reply with exactly: OK" --model claude-sonnet-5 --effort low` (isolated empty tmp dir, no ambient CLAUDE.md) | trivial prompt | $0.0789 | 4 | — |
| `claude -p "reply with exactly: OK" --model claude-opus-5 --effort low` (same isolated dir) | trivial prompt | $0.267 | 4 | — |
| `claude -p` skill-off, ~120-word exec-summary task, sonnet-5, effort low, `--disallowedTools Write,Edit,Bash,NotebookEdit` | realistic scenario | $0.189 | 665 | 12s |
| `claude -p` skill-on (skill folder installed, same task), sonnet-5, effort low | realistic scenario | $0.113 (cache reuse from prior call) | 1040 | 20s |

`[VERIFIED: live claude -p invocations, this session — exact commands and JSON output captured above]`

Opus's trivial-prompt cost was ≈3.4× sonnet's trivial-prompt cost under identical conditions — use **3× sonnet** as the opus cost multiplier for planning purposes. Using $0.15/call as a representative sonnet generation cost and $0.45/call for opus (3×):

- Generation: 48 sonnet calls × $0.15 + 48 opus calls × $0.45 ≈ **$7.20 + $21.60 = $28.80**
- Judging (judge model = opus-5, shorter prompt, no skill text — see Decision 5): 96 calls × ≈$0.20 ≈ **$19.20**
- **Total estimated cost: ≈ $48**, order-of-magnitude, derived from n=1-3 live samples — not a precise prediction. State this derivation basis in the plan so a reader knows it is not a vendor-quoted number.
- **Wall-clock:** 192 calls × ~18s average, run serially (no parallelism — matches `run_conformance.py`'s single-writer-per-path safety convention, read in full: "Exactly one call site writes any given out_path -- concurrent writers to one path is the defect that produced a false 'duplicated sections' finding") ≈ **58 minutes**, i.e. under 90 minutes and likely under 60.
- The CLI supports `--max-budget-usd <amount>` (confirmed present in `claude --help` output this session) — the runner should pass a conservative per-session cap (e.g. `--max-budget-usd 2`) as a safety guard, since none of this repo's existing scripts currently use it.

**If this is impractical, the smallest matrix that still satisfies "multiple pinned Claude models" (2) and "at least three times per cell" (3, the literal floor) is exactly the matrix above — it already sits at the floor on models and repeats.** The only further-shrinkable axis is scenario count: dropping to 4 scenarios (1 per family instead of 2) still satisfies "all four artifact families" and roughly halves every number (~$24, ~30 min), but **loses** the ability to distinguish a scenario-specific quirk from a family-general effect — with 1 scenario/family, all within-family variance across repeats is confounded with that single scenario's own idiosyncrasies. Recommend keeping 8 unless the plan review finds $48/60min genuinely unworkable for this project's actual budget.

### Decision 5 — Judge design (EVAL-07, EVAL-08)

**Judge model:** `claude-opus-5` — matches SimpleEnglish's own precedent of using a stronger/different-tier model than the weakest generation model as judge (`JUDGE_MODEL = "claude-opus-4-8"`, one tier above several of its own generation models, `run_bench.py` read in full). Since generation already uses both sonnet-5 and opus-5, using opus-5 as judge means **judge-family bias is real and must be named**: the judge is a Claude model scoring Claude-generated text. Reuse SimpleEnglish's own exact disclosure sentence (its `RESULTS.md`, read in full): *"The judge is a Claude model and the texts are Claude output, so family bias is possible."* — do not invent a softer euphemism for this; state it in those terms in this project's own RESULTS.md.

**Rubric — three dimensions, each 0-10, scored independently so persuasive force cannot be inferred from the other two (EVAL-08):**
1. **Evidence discipline** — does every claim carry evidence or an explicit gap marker; are there fabricated numbers, reference customers, or benchmarks. Maps to `SKILL.md`'s PF-2.x integrity rules (read in full this session).
2. **Clarity/mechanics** — sentence length, active voice, one claim per sentence. Maps to PF-4.x.
3. **Persuasive force** — would a technical evaluator finish this document believing the author understands their specific problem; does it read as a coherent case for a decision rather than a checklist. This is the dimension EVAL-08 explicitly requires be scored *separately*, so a flat-but-clean draft (high on dimension 2, low on dimension 3) cannot pass by proxy.

**Label-stripping:** exactly SimpleEnglish's pattern (`judge()`, read in full) — texts sent to the judge as anonymous "TEXT A"/"TEXT B," with no "skill"/"baseline" label and no mention of "Proof First," "PF-," or rule numbers anywhere in the judge prompt.

**Both-orders swap:** run the judge twice per pair, swapping which condition is "A" — average the two scores per dimension to cancel position bias, following SimpleEnglish's `order1_base_first` / `order2_skill_first` pattern exactly.

**Ties/refusals:** if the judge's reply fails to parse or the model refuses, record the pair `verdict: "unscoreable"` with a `reason` field and **exclude it from the mean** — do not default to a 0 or a midpoint score. This reuses `run_conformance.py`'s own `unscoreable`-vocabulary discipline (its `VERDICTS` tuple, read in full, includes `'unscoreable'` precisely so a failed session is never silently scored as data). A genuine tie (equal averaged scores) is recorded and counted as a tie in the win/tie/loss table, not forced to a winner — SimpleEnglish's own win/tie/loss table (read in full) already does this.

**Concrete improvement over the reference implementation:** use the installed CLI's `--json-schema <schema>` flag (confirmed present in `claude --help` output this session: *"JSON Schema for structured output validation"*) to force the judge's reply into `{"evidence": 0-10, "clarity": 0-10, "persuasive_force": 0-10}` directly, instead of SimpleEnglish's fragile `res["text"].strip().strip("\`json\n")` free-text parse (`run_bench.py` line 269, read in full) — this removes a disclosed parse-failure risk class the reference implementation carries.

### Decision 6 — Auth and reproducibility (EVAL-12)

**Finding, empirically confirmed this session:** `evals/conformance/run_conformance.py` does **not** use `--bare` anywhere (confirmed by reading the entire file — its `run_session()` invokes `['claude', '-p', prompt, '--model', model, '--disallowedTools'] + DISALLOWED_TOOLS` with no `--bare`). This machine's actual auth state is subscription OAuth (`claude auth status` → `{"loggedIn": true, "authMethod": "claude.ai", "subscriptionType": "team"}`, no `ANTHROPIC_API_KEY` set in the environment).

**Live falsification of `.claude/CLAUDE.md`'s `--bare` recommendation for this project's actual environment:** running `claude -p "reply with exactly: OK" --model claude-sonnet-5 --bare ...` in this exact session returned:
```
{"is_error":true, "terminal_reason":"api_error", "result":"Not logged in · Please run /login", ...}
```
`[VERIFIED: live claude -p invocation with --bare, this session — full JSON above]`. This is a real, positive falsification, not an assumption: `--bare`'s own `--help` text states it accepts only `ANTHROPIC_API_KEY` or `apiKeyHelper` and never reads OAuth/keychain — so a reader following CLAUDE.md's `--bare` recommendation on this project would need to separately provision and pay for an API key even with a working Claude subscription already logged in.

**Recommendation: do not use `--bare`.** Match `run_conformance.py`'s existing, already-working precedent: plain `claude -p ...`, relying on ambient OAuth, invoked with `cwd` set to a fresh `tempfile.mkdtemp()` per session (never the repo root) so no project `CLAUDE.md`/skills leak into either condition — this isolation is what already keeps `run_conformance.py`'s sessions clean without needing `--bare`'s blanket suppression, and it is testably cheaper too: this session's own trivial-prompt test from an isolated empty tmp dir cost $0.079 (19K cache-creation + 13K cache-read tokens of base system-prompt overhead) versus $0.171 for the identical prompt run from this repo's own root with its ~large CLAUDE.md in scope (`[VERIFIED: live claude -p invocations, this session]`, both JSON payloads captured above).

**Document the auth precondition explicitly**, in the same sentence class as SimpleEnglish's own docstring (`run_bench.py` line 8, read in full): *"Requires: Claude Code CLI logged in. No API key needed."*

**The one documented command (EVAL-12):**
- Live (paid) run: `python3 evals/benchmark/run_benchmark.py` — requires `claude auth status` to show `loggedIn: true`.
- Offline recompute (free, no network/model call): `python3 evals/benchmark/run_benchmark.py --report-only` — reads only committed files under `evals/benchmark/raw/*.json` and rewrites `evals/benchmark/RESULTS.md`.

### Decision 7 — Raw-artifact schema (EVAL-11)

**One JSON file per generation and per judgement**, under `evals/benchmark/raw/`, filenames modeled directly on `run_conformance.py`'s own naming convention (`f'{model}__{fixture_stem}__r{repeat}.txt'`, read in full):

- Generations: `{model}__{condition}__{scenario_id}__r{repeat}.json`
- Judgements: `{model}__judge__{scenario_id}__r{repeat}__order{1|2}.json`

**Generation record fields** (every field a discrete value this document quotes is taken from real CLI JSON output captured live this session, or from `run_conformance.py`'s own documented conventions, both cited inline above):

```json
{
  "run_id": "<uuid4>",
  "timestamp": "<ISO 8601 UTC>",
  "model": "claude-sonnet-5",
  "canonical_model": "claude-sonnet-5",
  "effort": "low",
  "condition": "skill-on",
  "family": "executive-summary",
  "scenario_id": "exec-summary-1",
  "scenario_prompt": "<verbatim prompt text sent>",
  "skill_sha": "<git hash-object of SKILL.md at skill_src, null for skill-off>",
  "repeat": 0,
  "text": "<generated text>",
  "usage": {
    "input_tokens": 4,
    "output_tokens": 1040,
    "cache_creation_input_tokens": 22832,
    "cache_read_input_tokens": 55997
  },
  "cost_usd": 0.1129354,
  "duration_ms": 18436,
  "cli_version": "2.1.267"
}
```

**Judgement record fields:**

```json
{
  "run_id": "<uuid4>",
  "timestamp": "<ISO 8601 UTC>",
  "judge_model": "claude-opus-5",
  "judge_effort": "high",
  "scenario_id": "exec-summary-1",
  "model": "claude-sonnet-5",
  "repeat": 0,
  "order": 1,
  "text_a_condition": "skill-off",
  "text_b_condition": "skill-on",
  "scores": {"evidence": 8, "clarity": 6, "persuasive_force": 7},
  "raw_judge_output": "<verbatim structured output>",
  "verdict": "scored",
  "reason": null
}
```

`skill_sha` reuses `run_conformance.py`'s `_git_blob_sha()` design exactly (`git hash-object` on the actual `SKILL.md` under `skill_src`, content-addressed — deliberately **not** `git rev-parse HEAD:...`, because the latter silently reports the wrong SHA for any materialized non-HEAD skill copy, the precise bug `_git_blob_sha()`'s own docstring documents fixing in this repo's history, read in full).

**The one documented command that recomputes every published figure:** `python3 evals/benchmark/run_benchmark.py --report-only` reads every file under `evals/benchmark/raw/*.json`, recomputes means/ranges and judge win/tie/loss tallies, and rewrites `evals/benchmark/RESULTS.md` deterministically — directly reusing SimpleEnglish's `aggregate()`/`report()` split (`run_bench.py`, read in full), which already implements exactly this "pure function over committed raw files" pattern with no live call.

### Decision 8 — What the harness must NOT claim

The project's constraint is "measured claims or no claims" (`.claude/CLAUDE.md`, `PROJECT.md`, `README.md` — the same sentence appears in all three, each read this session). Concrete overclaims this harness could enable, and the guard against each:

1. **"The skill makes writing X% more persuasive" stated with no model/date/N attached.** Guard: the headline sentence in `RESULTS.md` must always carry model versions, date, and generation count in the same sentence — SimpleEnglish's own headline pattern already does this ("...averaged across 7 models x 8 tasks (112 generations, measured)", `RESULTS.md` read in full). Add a `results-headline-missing-context` check requiring any percentage figure in the headline sentence to co-occur with a model-count and a date token, modeled on `check_repo.py`'s own `readme-results-pointer-missing`-style "a figure with no anchoring context is a violation" pattern.
2. **"This proves the skill works on GPT/Gemini/other providers."** Guard: cross-provider validation is explicitly `[out of scope / v2]` per `REQUIREMENTS.md`'s XPRV-01/XPRV-02 (v2 Requirements section, read via Bash this session — v2 items, not yet Read-tool-verified verbatim, but corroborated by the same file's Traceability table showing no XPRV row mapped to any v1 phase). RESULTS.md must name every tested model by exact string and never generalize beyond them.
3. **"The linter's violation count is a compliance verdict."** EVAL-03 already requires the linter to disclaim this. Make the exact disclaimer sentence a checked constant (self-test asserts it prints), reusing the disclaimer voice already established in this repo (`tools/check_repo.py`'s own docstring: "It... cannot judge whether a paraphrase reproduces proprietary text — that judgement is Phase 6's legal review gate," read in full — same pattern, different judgment).
4. **"N=3 shows a statistically significant effect."** Never compute or print a p-value, confidence interval, or the word "significant" as an affirmative claim. See "Statistical honesty for n=3" below.
5. **"A judged persuasion score of 8.1 means real buyers will be persuaded."** Guard: RESULTS.md must state the judge is an LLM proxy for a technical evaluator's reaction, not a measurement of real buyer behavior — mirrors `SKILL.md`'s own Limits section discipline (read in full: "What this skill flags but cannot verify... A clean check report is not legal clearance").
6. **Blending the two headline numbers into one composite "quality score."** EVAL-09 explicitly forbids this. Guard: `RESULTS.md` keeps two separately headed sections, `## Mechanical proxy counts` and `## Judged persuasion` (EVAL-09's own words), checked the same lightweight way `check_repo.py` checks heading presence (`artifact-family-section-missing`'s exact pattern, read in full) — a new `results-sections-missing` code.

**Explicitly rejected as over-engineering:** building a second hand-rolled NLP pass to detect prose that "implies significance" or "blends two numbers into a sentence" semantically. `PROJECT.md`'s own Out of Scope table already rejects "a maintained buzzword blocklist as the skill's core anti-slop mechanism" for exactly this reason (endless maintenance, wrong in both directions) — the same argument applies to inventing a semantic overclaim-detector inside the eval harness. Structural/lexical gates (heading presence, headline-sentence co-occurrence) catch the cheap, high-value cases; the rest is a human-reviewed writing discipline, stated as such in the runner's own docstring.

## Also Researched

### `claude -p` CLI flags — verified against the actually-installed CLI, not assumed from training data

Ran `claude --help` on this machine (version `2.1.267`, confirmed via `claude --version`) this session. All five flags CLAUDE.md names exist exactly as described:

- `--bare` — confirmed present; confirmed (by live invocation) to require `ANTHROPIC_API_KEY`/`apiKeyHelper` and to refuse OAuth — see Decision 6.
- `--effort <level>` — confirmed present, choices `low, medium, high, xhigh, max`. `[VERIFIED: claude --help output, this session]` — CLAUDE.md's separately-flagged, unconfirmed `ultracode` level does **not** appear anywhere in this CLI's help text; CLAUDE.md's own caution not to rely on it is corroborated, not contradicted.
- `--json-schema <schema>` — confirmed present: "JSON Schema for structured output validation."
- `--disallowedTools`/`--disallowed-tools <tools...>` — confirmed present, and already used by both `run_conformance.py` and this session's live test calls.
- `--model <model>` — confirmed present, and both `claude-sonnet-5` and `claude-opus-5` confirmed live-working this session.
- Additional flags relevant to Phase 5 that CLAUDE.md did not name but this session's `--help` read surfaced: `--output-format json` (used by SimpleEnglish's `run_bench.py` and recommended here too, for parseable structured envelopes rather than raw stdout text), `--max-budget-usd <amount>` (a per-session cost safety cap — recommend adopting it, since no existing script in this repo uses it), `--permission-prompts none` (relevant only if the runner needs unattended permission handling beyond `--disallowedTools`; not needed here since `--disallowedTools` alone already sufficed in this session's live tests).

### Statistical honesty for n=3

No standard deviation, no confidence interval, no significance claim. A sample stdev computed from n=3 (dividing by n−1=2) is enormously unstable and *looks* more rigorous than the data supports — reporting it invites exactly the overclaim Decision 8 item 4 forbids. **Recommendation:** report the mean **and** the full range (min–max, or literally all three raw values) per cell, with an explicit sentence: *"n=3 per cell is not powered to detect statistical significance; treat differences smaller than the observed range as noise."* This directly extends a precedent already set inside this repo: `REQUIREMENTS.md`'s own MOD-04 entry states, for a comparably small sample, "this sits within plausible sampling noise for a true difference of zero" (read via Read tool this session, MOD-04 checkbox text) — reuse that exact honesty posture for Phase 5's own small-N cells. `[ASSUMED — general statistics reasoning, not sourced from an external citation; low risk if wrong, since the recommendation is strictly more conservative than an alternative that reports a false-precision statistic]`

### Offline recompute path

Required, and directly implied by reading EVAL-11 and EVAL-12 together: EVAL-11 requires every raw file committed "so any published number can be recomputed from the repo," and EVAL-12 requires reproduction "with one documented command" — read together, that command cannot always require a live paid model call, because a reader with no Claude access, no budget, or offline must still be able to verify the *arithmetic* (means, ranges, win/tie/loss tallies) that RESULTS.md prints. **Concrete implementation:** `python3 evals/benchmark/run_benchmark.py --report-only`, a pure function over `evals/benchmark/raw/*.json`, no subprocess call, no network call — exactly SimpleEnglish's own `aggregate()`+`report()` split, confirmed by reading `run_bench.py` in full (its own `--report-only` flag: `elif "--report-only" not in sys.argv: generate(...)`, i.e. skip generation, just re-aggregate and re-render).

### Prior art: SimpleEnglish's `evals/` harness (this project's own named reference implementation)

Read `run_bench.py`, `ste_lint.py`, and `results/RESULTS.md` in full this session (`~/devoteam/.claude/plugins/marketplaces/simple-english/evals/`).

**Copy directly:**
- The `scenarios.json` shape (`id`, `type`/`family`, `prompt`) and its plain-task-prompt register (no leaked jargon from the skill it's testing).
- Pinning effort and recording it per raw file, with a named `DEFAULT_EFFORT` constant.
- The blind pairwise judge's both-orders-swap-and-average pattern, and its win/tie/loss reporting table.
- The `aggregate()`/`report()` split — one pure function that turns committed raw JSON into the published Markdown, callable standalone via `--report-only`.
- The "Honest number warnings" section as a permanent, non-trimmable part of `RESULTS.md` (`report()`'s closing block, read in full) — Phase 5 should have an equivalent, structurally required section (EVAL-10 already names this as mandatory).
- Skip-if-exists resumability in `generate()` (`if out.exists(): ... continue`) — lets an interrupted live run be safely re-invoked without re-paying for already-scored cells.

**Improve on:**
- SimpleEnglish's `call_claude()` runs every invocation from a single shared `cwd="/tmp"` (`run_bench.py` line 55, read in full) — this repo's own `run_conformance.py` already does better, allocating a fresh `tempfile.mkdtemp()` **per session** (read in full) — use the latter, both for cleanliness and because this session's own cost test shows an isolated dir with no ambient CLAUDE.md is measurably cheaper.
- SimpleEnglish's judge output parsing (`res["text"].strip().strip("\`json\n")`) is a fragile free-text scrape with a disclosed failure mode; use `--json-schema` instead (see Decision 5).
- SimpleEnglish's `RESULTS.md` does not budget for or disclose real per-call dollar cost beyond the aggregate reduction percentage; this session's own live testing shows real per-call cost is dominated by ~20-40K tokens of session/system-prompt overhead even for trivial prompts — Phase 5's plan should surface budget more explicitly than the reference implementation does (see Decision 4's arithmetic).

**Do not repeat:**
- Running the whole matrix with **no** isolation-guaranteed skill install path — SimpleEnglish reads `SKILL.md` text directly into the prompt string rather than installing a real skill folder into a scoped `.claude/skills/` directory the way `run_conformance.py` does; the skill-folder-install approach is more faithful to how a real user actually invokes the skill and should be preferred here, matching this repo's own existing (better) pattern.
- A single-generation-per-cell default (SimpleEnglish's own docs: "One generation per cell. Re-run the matrix for variance") — EVAL-06 already forbids this for Phase 5; the 3-repeat floor is a repo-specific improvement over the reference implementation, not merely a requirement to satisfy grudgingly.

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python stdlib: `re`, `json`, `argparse`, `pathlib`, `subprocess`, `tempfile`, `uuid`, `datetime`, `hashlib`, `shutil` | 3.11+ (matches `.github/workflows/ci.yml`'s pinned `python-version: "3.11"`, read in full) | Linter, benchmark runner, judge, offline aggregation | Zero-dependency constraint is a hard project rule; every existing `evals/`/`tools/` script in this repo already uses only these modules |
| `claude` CLI | 2.1.267 (confirmed installed and logged in on this machine, via `claude --version` this session) | Headless model driver for generation and judging | No API key needed with subscription OAuth (see Decision 6); already the mechanism `run_conformance.py` uses |

### Supporting

None required. No `textstat`, no `spaCy` — both explicitly out of scope per `PROJECT.md`'s Out of Scope table and CLAUDE.md's "What NOT to Use" table (both consistent, both already-decided project constraints, not this research's own recommendation).

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| stdlib regex linter | `textstat` supplementary metric | Optional, additive only, never on the reproduction path — matches CLAUDE.md's own existing guidance; not needed to satisfy any EVAL requirement |
| Two named external proxy-list sources | A single larger public corpus (e.g. a full corporate-jargon dictionary scrape) | A single source is easier to maintain but weaker for the non-circularity claim — two independent, differently-governed sources (a community wiki style guide and a federal plain-language mandate) make "independently sourced" a stronger, more defensible claim than one |
| `--json-schema`-based judge parsing | Free-text scrape (SimpleEnshlish's approach) | Free-text parsing is simpler to write but has a disclosed, already-observed failure mode in the reference implementation; `--json-schema` is confirmed present on the installed CLI this session, so there is no reason to accept the weaker approach |

**Installation:** None — no `pip install`. `claude auth status` must show `loggedIn: true` before any live run.

**Version verification:** `claude --version` → `2.1.267` (confirmed this session, live command). Python `3.11` pinned in CI (`.github/workflows/ci.yml`, read in full).

## Package Legitimacy Audit

Not applicable — this phase installs no external packages. Everything is Python standard library plus the already-installed `claude` CLI. `Packages removed due to [SLOP] verdict: none.` `Packages flagged as suspicious [SUS]: none.`

## Architecture Patterns

### System Architecture Diagram

```
                         ┌─────────────────────────┐
                         │  evals/proxy-sources.md │  (external-source registry)
                         └────────────┬────────────┘
                                      │ read by
                                      ▼
 free text  ──────────►  evals/lint.py  ──────────►  {violations, disclaimer}
 (any draft)             (stdlib regex,                (EVAL-01/03)
                          proxy-checked)

 evals/benchmark/scenarios.json  ─┐
 evals/benchmark/bench-deal-brief.md ─┤
                                   ▼
                    evals/benchmark/run_benchmark.py
                    ┌──────────────────────────────────────────┐
                    │  for model × scenario × repeat:           │
                    │    isolated tmp dir (tempfile.mkdtemp)    │
                    │    skill-off: bare prompt  ─┐             │
                    │    skill-on: install skill  │─► claude -p │──► generation JSON
                    │      folder + prompt        │   (--model, │    (committed,
                    │                              │   --effort, │     Decision 7 schema)
                    │                              │   --disallowedTools,
                    │                              │   --output-format json)
                    └──────────────────────────────────────────┘
                                      │  pairs (skill-on, skill-off)
                                      ▼
                    judge pass: claude -p (judge model, --json-schema,
                    labels stripped as "TEXT A"/"TEXT B", both orders)
                                      │
                                      ▼
                    evals/benchmark/raw/*.json  (committed to git)
                                      │
                     `--report-only` │  (pure function, no network call)
                                      ▼
                    evals/benchmark/RESULTS.md
                    ┌───────────────────────────────┐
                    │ ## Mechanical proxy counts     │  ← from evals/lint.py over raw text
                    │ ## Judged persuasion            │  ← from judge JSON, mean + range
                    │ ## Honest caveats                │  ← EVAL-10's five named items
                    └───────────────────────────────┘
```

### Recommended Project Structure

```
evals/
├── pressure-tests.md              # existing (Phase 2)
├── lint.py                        # NEW — EVAL-01/03: stdlib linter, --self-test
├── proxy-sources.md               # NEW — EVAL-02: two-source provenance registry
├── conformance/                   # existing (Phase 3) — untouched by this phase
│   └── run_conformance.py
└── benchmark/                     # NEW — EVAL-04..12
    ├── bench-deal-brief.md        # a fresh fictional deal, distinct from examples/deal-brief.md
    ├── scenarios.json             # 8 scenarios, 2 per artifact family
    ├── run_benchmark.py           # generation + judge + --report-only aggregation, --self-test
    ├── raw/                       # committed JSON: one file per generation, one per judgement
    └── RESULTS.md                 # generated by run_benchmark.py --report-only
```

### Pattern 1: Isolated per-session temp directory with skill-folder install

**What:** Copy the real `skills/proof-first/` folder into a fresh `tempfile.mkdtemp()`'s `.claude/skills/proof-first/` for the skill-on condition; run the bare prompt with no skill folder present for skill-off. Never run from the repo's own root (avoids ambient `CLAUDE.md`/skills leakage and is measurably cheaper — see Decision 6).

**When to use:** Every generation call in the benchmark matrix.

**Example (adapted from `run_session()` in `evals/conformance/run_conformance.py`, read in full this session):**
```python
# Source: evals/conformance/run_conformance.py, run_session() — this session's Read
tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix='proof-first-benchmark-'))
try:
    if condition == 'skill-on':
        skill_dst = tmp_dir / '.claude' / 'skills' / 'proof-first'
        skill_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(skill_src, skill_dst)
    argv = ['claude', '-p', prompt, '--model', model, '--effort', effort,
            '--output-format', 'json',
            '--disallowedTools', 'Write,Edit,Bash,NotebookEdit']
    result = subprocess.run(argv, cwd=str(tmp_dir), capture_output=True,
                             text=True, timeout=timeout_s)
finally:
    shutil.rmtree(tmp_dir, ignore_errors=True)
```

### Pattern 2: Write-then-flush durability for the raw results

**What:** Every generation/judgement record is written to its own file (or appended, flushed immediately) the moment it is produced — never buffered in memory until the whole matrix finishes.

**When to use:** Every write inside the model×scenario×repeat loop.

**Example (mirrors `_write_result_line()` in `run_conformance.py`, read in full this session — its own docstring states this is "the single place durability is established... so a future edit that drops the flush is a one-line diff rather than a scattered one"):**
```python
def _write_json_atomic(path, record):
    path.write_text(json.dumps(record, indent=2))
    # pathlib.Path.write_text() opens, writes, and closes in one call —
    # no separate flush needed, unlike run_conformance.py's append-mode
    # results handle, which is why THIS module needs no _write_result_line
    # equivalent: one file per record, not one shared append-mode file.
```

### Anti-Patterns to Avoid

- **Sharing a shared, global `cwd` across all sessions:** SimpleEnglish's `call_claude()` uses `cwd="/tmp"` for every call — a single shared directory across dozens of concurrent-in-time sessions is a needless collision risk and, per this session's own cost test, more expensive than a clean isolated tmp dir. Use one fresh temp dir per session.
- **Parsing judge output as free text with `.strip("\`json\n")`:** disclosed, observed failure mode in the reference implementation. Use `--json-schema`.
- **Blending the mechanical linter count and the judged persuasion score into one composite number:** EVAL-09 forbids this explicitly; keep two headed sections.
- **Computing a standard deviation or confidence interval from n=3:** false precision; report mean + range instead (see "Statistical honesty for n=3").

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Detecting whether prose "implies statistical significance" | A semantic slop-detector inside the eval harness | A fixed writing-discipline rule stated in the runner's own docstring, enforced at code review | Same argument `PROJECT.md`'s Out of Scope table already makes against a maintained buzzword blocklist: endless maintenance, wrong in both directions, and a semantic judgment no regex performs reliably |
| Structured judge output parsing | A hand-rolled fenced-code-block stripper | `--json-schema` (confirmed present on the installed CLI) | Removes a disclosed, already-observed parse-failure class from the reference implementation |
| Cross-model determinism | Retrying until two runs match | Accept and disclose non-determinism; increase N (repeats) if variance matters | `temperature`/`seed` flags do not exist in `-p` mode (CLAUDE.md's own "What NOT to Use" table, corroborated by this session's `--help` read finding no such flags) |
| Buzzword/superlative detection precision | spaCy POS tagging | stdlib regex, disclosed ceiling | Already decided project-wide (`PROJECT.md` Out of Scope, CLAUDE.md "What NOT to Use") — not re-litigated here |

**Key insight:** every "don't hand-roll" item in this phase is already a decided project-wide constraint from Phases 1-4; Phase 5's job is to apply the same discipline to two new problems (statistical overclaim, judge-output parsing), not invent new exceptions to it.

## Common Pitfalls

### Pitfall 1: Scoring an error string as if it were generated text

**What goes wrong:** A `claude -p` call that fails (quota exhaustion, transient API error) returns a short error string on stdout; if that string is fed straight into the linter or judge, it produces a false result indistinguishable from real (bad) data.

**Why it happens:** `subprocess.run`'s stdout is non-empty even on failure; only `returncode` and/or `is_error` in the JSON envelope reveal the problem.

**How to avoid:** Exactly `run_conformance.py`'s `SessionFailedError` pattern (read in full this session) — check `result.returncode != 0` (or, with `--output-format json`, check the envelope's `is_error` field) before ever touching the text, and record `verdict: "unscoreable"` with the real reason instead. This repo has already paid for this lesson once (the MOD-04 run invalidated by exactly this bug, documented in `REQUIREMENTS.md`'s own MOD-04 entry, read this session, referencing "all ten claude-opus-5 sessions share this exact signature after a usage-limit exhaustion mid-run").

**Warning signs:** A model/condition whose violation count or judge score looks suspiciously uniform or suspiciously bad across many cells at once — check for a shared exit-code-nonzero pattern before trusting the numbers.

### Pitfall 2: Treating `--output-format json`'s stdout as already-parsed JSON

**What goes wrong:** on some CLI versions, `--output-format json` returns a single JSON object; on others (per SimpleEnglish's own comment, read in full: "CLI >= 2.1 returns the message stream"), it can return a JSON array of message objects, and the caller must find the one with `"type": "result"`.

**How to avoid:** defensively handle both shapes, exactly as SimpleEnglish's `call_claude()` already does (`if isinstance(env, list): env = next(m for m in env if m.get("type") == "result")`) — this session's own live tests on CLI `2.1.267` returned a single object (not a list), so both code paths should be tested, not just the one observed live today.

### Pitfall 3: Letting the benchmark's own cost surprise the plan mid-execution

**What goes wrong:** a plan that budgets "one generation per cell, cheap" without live-testing actual per-call cost discovers mid-run that real system-prompt/cache overhead makes even trivial prompts cost $0.05-0.27/call — at 192 calls, an unbudgeted plan could run to $50+ unexpectedly.

**How to avoid:** the arithmetic in Decision 4 is derived from real, live, this-session invocations, not assumed — use it as the planning budget, and pass `--max-budget-usd` per session as a hard stop.

## Code Examples

### Linter self-test pattern (mirrors `tools/check_repo.py`'s and SimpleEnglish's `ste_lint.py`'s conventions)

```python
# Source: evals/lint.py (new file), modeled on
# ~/devoteam/.claude/plugins/marketplaces/simple-english/evals/ste_lint.py self_test(),
# read in full this session.
SLOP_FIXTURE = "This comprehensive, best-in-class, world-class solution delivers a robust, enterprise-grade landing zone."
CLEAN_FIXTURE = "AWS Control Tower governs the new account structure across 850 virtual machines."

def self_test():
    dirty = lint(SLOP_FIXTURE)
    clean = lint(CLEAN_FIXTURE)
    assert dirty["violations_total"] >= 4, dirty
    assert clean["violations_total"] == 0, clean
    print("self-test PASS:", dirty["violations_total"], "in slop fixture, 0 in clean")
```

### `--report-only` offline aggregation entry point

```python
# Source: adapted from run_bench.py's main(), read in full this session
def main():
    args = parser.parse_args()
    if args.self_test:
        sys.exit(0 if self_test() else 1)
    if not args.report_only:
        run_matrix(...)  # live, paid, network calls
    build_results_md(load_raw_records())  # pure function, no network call
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| Free-text scrape of judge output (`.strip("\`json\n")`) | `--json-schema`-constrained structured output | Added to the `claude` CLI since SimpleEnglish's `run_bench.py` was last updated (its own comment already flags CLI output-shape drift between versions) | Removes a disclosed parse-failure class |
| `--bare` assumed as the benchmark-determinism default (CLAUDE.md's own earlier note) | OAuth-based invocation, matching this repo's actual auth state | This session's live test | `--bare` fails outright without a provisioned `ANTHROPIC_API_KEY`; not adopted for Phase 5 |

**Deprecated/outdated:** CLAUDE.md's suggestion to pair `--bare` with `ANTHROPIC_API_KEY` "rather than relying on subscription login" is not adopted for this phase — this project's actual working auth is subscription OAuth, and `--bare` was confirmed, live, to reject that auth method entirely.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | $0.15/sonnet-call and $0.45/opus-call are representative average generation costs across the full 8-scenario matrix | Decision 4 | Actual cost could be materially higher or lower depending on scenario length/output length variance; mitigated by `--max-budget-usd` per-session cap and by stating the estimate's derivation basis (n=1-3 samples) explicitly in the plan |
| A2 | ~18s average wall-clock per call, giving ~58 minutes total serial runtime | Decision 4 | Real runtime could be longer under API rate-limiting or longer generations at higher effort; mitigated by recommending `effort: low` for the main run |
| A3 | Reporting mean + range (not stdev/CI) is the statistically honest choice at n=3 | "Statistical honesty for n=3" | This is general statistical reasoning, not sourced from an external citation; low risk since it is strictly more conservative than reporting a false-precision statistic |
| A4 | Wikipedia MOS:WTW and plainlanguage.gov/digital.gov's word lists, taken together, are legally and practically sufficient "external, non-circular" sources for a buzzword proxy list | Decision 1 | If a future reviewer judges these too thin or too US-government-specific, additional sources can be added to `evals/proxy-sources.md` without restructuring the checker — low risk, additive fix |
| A5 | XPRV-01/XPRV-02 (cross-provider validation) are correctly out-of-scope for v1 | Decision 8, item 2 | Read via Bash (not Read tool) this session, so tagged `[CITED]` rather than `[VERIFIED]`; corroborated by the Traceability table showing no XPRV row mapped to any v1 phase — low risk of misreading given the corroboration |

## Open Questions

1. **Whether the planner splits this into 2 or 3 plans.**
   - What we know: the phase description itself suggests "likely splits across the linter, the scenario/benchmark runner, and the judge; EVAL-06's mandatory 3x-per-cell repetition raises benchmark runtime meaningfully and may warrant its own plan separate from the linter" (`ROADMAP.md`, read in full this session).
   - What's unclear: whether judge implementation should be its own plan or folded into the benchmark-runner plan.
   - Recommendation: 3 plans — (A) linter + proxy provenance (EVAL-01/02/03, no live calls, fast, cheap to iterate), (B) scenario set + benchmark runner scaffolding with `--self-test`/`--report-only` built and tested against committed fixture JSON but the live matrix NOT yet run (EVAL-04, 05 structure, 11 schema, 12 offline path), (C) judge implementation + the actual paid live matrix execution, committing `raw/*.json` and `RESULTS.md` (EVAL-06, 07, 08, 09, 10). This isolates the expensive, non-reversible, paid step (C) from the cheap, iterable steps (A, B), so a plan-review cycle on (A)/(B) never re-triggers paid live calls.

2. **Whether `evals/proxy-sources.md`'s provenance checker lives inside `evals/lint.py` or is added to `tools/check_repo.py`.**
   - What we know: `tools/check_repo.py` is the project's one existing, CI-wired, all-repo structural checker; adding a code here is the path of least new machinery.
   - What's unclear: whether the project wants `evals/`'s own instruments to stay fully self-contained (matching the `skills/` cannot import `evals/` boundary's spirit) or whether `check_repo.py` growing to also police `evals/` content is acceptable, given it already explicitly excludes `evals/` from `unlisted-figure` ("evals/ is deliberately excluded because Phase 5's benchmark data is not bound by the Canonical figures interface," read in full this session).
   - Recommendation: keep it inside `evals/lint.py`'s own `--self-test`, not `tools/check_repo.py` — consistent with that prior exclusion decision, and it keeps Phase 5's CI addition to `evals/lint.py --self-test` (parallel to the existing `evals/conformance/run_conformance.py --self-test` line already in `ci.yml`) rather than growing `check_repo.py`'s already-6891-line scope.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `claude` CLI | Live generation + judging (EVAL-05..EVAL-08) | ✓ | 2.1.267 | — |
| Claude subscription OAuth login | Live calls without provisioning an API key | ✓ | `authMethod: claude.ai`, `subscriptionType: team` | `ANTHROPIC_API_KEY` + `--bare`, confirmed NOT to work in this exact environment absent a provisioned key — not a live fallback here |
| Python 3.11+ | Linter, benchmark runner, offline aggregation | ✓ (CI pins 3.11; this repo's other `evals/`/`tools/` scripts already run under it) | — | — |
| Network access to Anthropic's API | Any live generation/judge call | Assumed available (this session's live calls succeeded) | — | The `--report-only` offline path has **no** network dependency at all — this is itself the fallback for every other row |

**Missing dependencies with no fallback:** none identified.

**Missing dependencies with fallback:** none required beyond the `--report-only` path already designed into Decision 6/7.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | None (this repo has no pytest/unittest framework anywhere — confirmed by the existing house pattern: `tools/check_repo.py` and `evals/conformance/run_conformance.py` both implement their own `--self-test` mode with inline assertions, no test runner) |
| Config file | none — see Wave 0 |
| Quick run command | `python3 evals/lint.py --self-test` |
| Full suite command | `python3 evals/lint.py --self-test && python3 evals/benchmark/run_benchmark.py --self-test` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| EVAL-01 | Linter counts violations correctly, self-test passes | unit (offline) | `python3 evals/lint.py --self-test` | ❌ Wave 0 |
| EVAL-02 | Every proxy term traces to an external source; none traces only internally | unit (offline) | `python3 evals/lint.py --self-test` (extended to include provenance checks) | ❌ Wave 0 |
| EVAL-03 | Linter output includes the fixed deletion-test/non-compliance-verdict disclaimer | unit (offline) | `python3 evals/lint.py --self-test` | ❌ Wave 0 |
| EVAL-04 | Scenario file has exactly 4 families represented, ≥1 scenario each | unit (offline) | `python3 evals/benchmark/run_benchmark.py --self-test` | ❌ Wave 0 |
| EVAL-05 | Every raw record carries model, effort, and reproduces its own `--model`/`--effort` args | unit (offline, via fixture raw files) + manual-only for the live call itself | `python3 evals/benchmark/run_benchmark.py --self-test` (offline schema check); live call is inherently manual/paid | ❌ Wave 0 |
| EVAL-06 | ≥3 raw records exist per (model, scenario, condition) cell; RESULTS.md prints mean+range | unit (offline, over committed `raw/`) | `python3 evals/benchmark/run_benchmark.py --report-only` | ❌ Wave 0 |
| EVAL-07 | Judge label-stripping + both-orders present in every judgement record | unit (offline, via fixture judge files) | `python3 evals/benchmark/run_benchmark.py --self-test` | ❌ Wave 0 |
| EVAL-08 | Judge rubric JSON always includes a `persuasive_force` key distinct from `evidence`/`clarity` | unit (offline) | `python3 evals/benchmark/run_benchmark.py --self-test` | ❌ Wave 0 |
| EVAL-09 | RESULTS.md contains both `## Mechanical proxy counts` and `## Judged persuasion` headings, never one merged figure | unit (offline, text check) | `python3 evals/benchmark/run_benchmark.py --self-test` or a `check_repo.py`-style code | ❌ Wave 0 |
| EVAL-10 | RESULTS.md's caveats section names all 5 required items verbatim | unit (offline, text check) | same as EVAL-09 | ❌ Wave 0 |
| EVAL-11 | Every generation/judgement referenced by RESULTS.md corresponds to a committed file under `raw/` | unit (offline) | `python3 evals/benchmark/run_benchmark.py --report-only` | ❌ Wave 0 |
| EVAL-12 | `--report-only` produces byte-identical RESULTS.md from the same `raw/` with zero network calls | unit (offline; assert no `subprocess`/socket call made, e.g. by monkeypatching `subprocess.run` to raise if called) | `python3 evals/benchmark/run_benchmark.py --self-test` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `python3 evals/lint.py --self-test` (and `evals/benchmark/run_benchmark.py --self-test` once it exists) — both offline, fast, free.
- **Per wave merge:** the full offline self-test suite above; the live paid matrix run is NOT part of routine sampling — it runs once per plan-C execution and its output is committed, not re-run on every merge.
- **Phase gate:** full offline self-test suite green, plus a human-reviewed spot-check that `RESULTS.md`'s committed numbers actually match what `--report-only` recomputes from the committed `raw/` files (a live diff check: `git stash; python3 evals/benchmark/run_benchmark.py --report-only; git diff evals/benchmark/RESULTS.md` should show no diff).

### Wave 0 Gaps

- [ ] `evals/lint.py` — does not exist yet; needs `--self-test`
- [ ] `evals/proxy-sources.md` — does not exist yet
- [ ] `evals/benchmark/run_benchmark.py` — does not exist yet; needs `--self-test` and `--report-only`
- [ ] `evals/benchmark/scenarios.json`, `evals/benchmark/bench-deal-brief.md` — do not exist yet
- [ ] `evals/conformance/transcripts/*.txt`-style committed fixture files for the new runner's own `--self-test` (mirroring `run_conformance.py`'s own fixture-file cross-check pattern, read in full this session) — needed so `--self-test` can validate real committed judge/generation JSON shapes offline
- [ ] `.github/workflows/ci.yml` — needs a new line, `python3 evals/lint.py --self-test`, added alongside the existing `python3 evals/conformance/run_conformance.py --self-test` line (read in full this session); the live paid benchmark matrix must NOT be added to CI

*(Everything above is a genuine gap — this is a net-new phase with no existing test infrastructure of its own to inherit.)*

## Security Domain

`security_enforcement: true` in `.planning/config.json` (confirmed via Bash read this session), so this section is required even though the phase is low-risk internal tooling with no user-facing surface, no auth flow of its own, and no network-facing service.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | This phase consumes the `claude` CLI's own existing OAuth session; it introduces no new authentication surface |
| V3 Session Management | No | No sessions of this project's own are created |
| V4 Access Control | No | No multi-user access-control surface exists in a local CLI script |
| V5 Input Validation | Yes | Scenario IDs and CLI arguments (`--models`, `--fixtures`-equivalent, `--transcript-dir`/`--raw-dir`, `--out`) must be validated the same way `run_conformance.py` already does — via `pathlib.Path` construction with no `shell=True` and no string-interpolated shell commands (confirmed by reading `run_session()`'s `subprocess.run(argv, ...)` call — `argv` is a list, never a shell string) |
| V6 Cryptography | No | No cryptographic operation is performed by this phase; `git hash-object` (SHA-1 content addressing) is used for content-identity tracking only, not for any security guarantee |
| V12 Files and Resources | Yes | Filenames for `raw/*.json` are built from a fixed template (`{model}__{condition}__{scenario_id}__r{repeat}.json`); `scenario_id` must be drawn only from the committed `scenarios.json` (never from free-text user input) so no path-traversal character can reach a filename — mirrors `run_conformance.py`'s own fixed-template naming |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Argument/path injection via a crafted `--transcript-dir`/`--out`/`--skill-src` value | Tampering | Construct paths with `pathlib.Path`, never string-concatenate into a shell command; `subprocess.run` called with a list `argv`, never `shell=True` — exactly `run_conformance.py`'s existing pattern, read in full |
| A malicious or malformed judge/generation JSON response silently accepted as valid data | Tampering / Repudiation | Validate the structured `--json-schema` response against the expected keys before writing it to `raw/`; treat a schema-validation failure the same as `SessionFailedError` — record `verdict: "unscoreable"`, never partial/garbage data |
| Accidentally committing an `ANTHROPIC_API_KEY` if a contributor later adopts `--bare` for a different reason | Information Disclosure | Never read secrets from `raw/*.json` records; if a future plan adds API-key support, keep the key out of any committed file and out of `cost_usd`/`usage` fields, which never need it |

## Sources

### Primary (HIGH confidence — files read in full with the Read tool, this session)

- `evals/conformance/run_conformance.py` — full file, 955 lines. Session/durability/isolation/`SessionFailedError`/`_git_blob_sha` patterns.
- `skills/proof-first/SKILL.md` — full file, 308 lines. Rule IDs, marker vocabulary, write/check mode contracts.
- `skills/proof-first/references/worked-examples.md` — full file, 148 lines. Buzzword-example overlap check for Decision 1/2.
- `skills/proof-first/references/artifact-patterns.md` — full file, 145 lines. Four family names and classification signals.
- `tools/generate_derivatives.py` — full file, 299 lines. `DERIVATIVE_SOURCE_NAMES`, `evals/` exclusion precedent, anti-sibling-import philosophy.
- `evals/pressure-tests.md` — full file, 85 lines. Established "no observation yet" honesty convention, explicit hand-off of trigger-reliability measurement to Phase 5.
- `.github/workflows/ci.yml` — full file, 21 lines. Current CI surface Phase 5 must extend.
- `README.md` — full file, 256 lines. Current Status/claim posture, downstream consumer of this phase's numbers.
- `SOURCES.md` — full file, 68 lines. House pattern for external-source provenance tables.
- `.planning/REQUIREMENTS.md` (EVAL-01..EVAL-12 lines, offset 69-80) — verbatim requirement text.
- `.planning/ROADMAP.md` (Phase 5 section, offset 257-270) — verbatim goal/success-criteria text.
- `~/devoteam/.claude/plugins/marketplaces/simple-english/evals/run_bench.py` — full file, 308 lines (external reference implementation).
- `~/devoteam/.claude/plugins/marketplaces/simple-english/evals/ste_lint.py` — full file, 133 lines (external reference implementation).
- `~/devoteam/.claude/plugins/marketplaces/simple-english/evals/results/RESULTS.md` — full file, 63 lines (external reference implementation's published output).
- Live `claude --help` output, this session (CLI version `2.1.267`) — flag verification.
- Live `claude auth status`, `claude --version` — this session — auth state and CLI version.
- Three live `claude -p` invocations, this session (trivial-prompt sonnet/opus, and a realistic skill-off/skill-on exec-summary generation pair) — cost/timing/token arithmetic for Decision 4 and Decision 6.

### Secondary (MEDIUM confidence — CITED, official/authoritative external sources not fetched via a full-page tool but corroborated by WebSearch this session)

- Wikipedia:Manual of Style/Words to watch — `https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch`
- GSA plainlanguage.gov / digital.gov "Avoid jargon" — `https://digital.gov/guides/plain-language/principles/avoid-jargon`, `https://github.com/GSA/plainlanguage.gov/blob/main/_pages/guidelines/words/avoid-jargon.md`

### Tertiary (LOW confidence — Bash-read, not Read-tool-verified this session; corroborated but flagged)

- `.planning/REQUIREMENTS.md`'s v2 Requirements section (XPRV-01/02) and its Traceability table — read via Bash `cat`, not the Read tool, this session; corroborated by the same file's own Traceability table showing no XPRV row mapped to any v1 phase, but tagged `[CITED]` rather than `[VERIFIED]` per this document's own provenance discipline.
- `.planning/WINDOWS.md` — read via `grep` only, this session; used only for background context (the run_conformance.py durability-bug history), not for any load-bearing recommendation.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — every tool/flag named is either already in use in this repo or was live-tested this session.
- Architecture: HIGH — directly modeled on two working, fully-read prior-art implementations (`run_conformance.py`, SimpleEnglish's `run_bench.py`).
- Pitfalls: HIGH — two of three pitfalls are documented, already-occurred bugs in this exact repo's own history (read from `REQUIREMENTS.md`'s MOD-04 entry and `run_conformance.py`'s own docstrings).
- Cost/runtime arithmetic (Decision 4): MEDIUM — grounded in real live measurements but only n=1-3 samples; stated explicitly as an estimate, not a guarantee.
- Proxy-list source selection (Decision 1): MEDIUM — the two sources are real and citable, but which specific external lists are "best" is this research's own engineering judgment, not a requirement dictated by any spec.

**Research date:** 2026-09-18
**Valid until:** 30 days for the architectural/pattern recommendations (stable); 7 days for the exact cost-per-call figures (Anthropic pricing and CLI overhead behavior can change faster than the rest of this document)

## RESEARCH COMPLETE

**Phase:** 05 - Evaluation Harness
**Confidence:** MEDIUM-HIGH

### Key Findings
- `--bare` fails in this environment (live-confirmed: "Not logged in") — do not adopt CLAUDE.md's `--bare`+API-key recommendation for this phase; keep OAuth-based invocation matching `run_conformance.py`'s existing precedent.
- Real live-tested costs: ~$0.08-0.27 for even a trivial prompt, ~$0.11-0.19 for a realistic single scenario generation — the full 96-generation + 96-judge matrix (2 models × 8 scenarios × 3 repeats × 2 conditions) is estimated at ≈$48 and ≈58 minutes serial wall-clock, both derived from this session's own live measurements, not assumed.
- Benchmark scenarios must use a fresh fictional deal, never `examples/deal-brief.md`'s Halverton Mutual — reusing it risks memorized-pattern reproduction from the skill's own shipped worked examples, the same circularity concern EVAL-02 already raises for the linter's word list.
- The new benchmark runner should be modeled on, but not literally share code with, `evals/conformance/run_conformance.py` — that file's own docstring explicitly scopes Phase 5's harness as separate, and their raw-data persistence policies are opposite (ephemeral vs. committed).
- Recommended 3-plan split: (A) linter + proxy provenance (cheap, offline, iterable), (B) benchmark scaffolding self-tested against fixtures with no live calls, (C) the paid live matrix + judge, isolating the one expensive/non-reversible step.

### Confidence Assessment
| Area | Level | Reason |
|------|-------|--------|
| Standard Stack | HIGH | Every flag/tool live-verified or already in repo use |
| Architecture | HIGH | Modeled on two fully-read working implementations |
| Pitfalls | HIGH | Two of three are this repo's own documented past incidents |
| Cost/runtime arithmetic | MEDIUM | Real measurements, small sample size, stated as estimate |

### Open Questions
- Exact plan split (2 vs 3 plans) — recommendation given, planner's call.
- Whether the proxy-provenance checker lives in `evals/lint.py` or `tools/check_repo.py` — recommendation given (keep in `evals/lint.py`), planner's call.

### Ready for Planning
Research complete. Planner can now create PLAN.md files for Phase 5.
