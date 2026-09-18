# API Coverage — Anthropic models via the locally-installed `claude` CLI (headless `-p` mode)

> Full coverage by default. Opt-outs are explicit, reasoned decisions.

**Why this file exists.** Phase 5 drives an external service: Anthropic's models, reached
through the `claude` CLI in `-p` mode. The detector returned `detected: false` against the
ROADMAP phase section alone and `detected: true` against `05-RESEARCH.md` + `05-PATTERNS.md`
(both runs performed 2026-09-18, this planning session). The wider scope is the honest one —
the research document is where the integration is actually described — so the matrix is
produced rather than skipped.

**What the capability surface is.** This phase does not call an HTTP API directly. Its
integration surface is the `claude` CLI's headless invocation contract: the flags that change
what is sent, what is returned, how it is authenticated, and what it costs. That flag set is
what a future contributor would discover was silently unavailable, so that is what gets
decided here. Enumerated from `claude --help` on version `2.1.267`, run this session.

| capability | decision | reason |
|---|---|---|
| `-p` / `--print` headless invocation | INTEGRATE | |
| `--model <model>` | INTEGRATE | |
| `--effort <level>` | INTEGRATE | |
| `--output-format json` | INTEGRATE | |
| `--json-schema <schema>` | INTEGRATE | |
| `--disallowedTools <tools...>` | INTEGRATE | |
| `--max-budget-usd <amount>` | INTEGRATE | |
| isolated `cwd` per session (skill-on / skill-off condition control) | INTEGRATE | |
| `claude auth status` (precondition check before a live run) | INTEGRATE | |
| `--bare` | OPT-OUT | live-falsified in this environment — returns `Not logged in · Please run /login` because it reads only `ANTHROPIC_API_KEY`/`apiKeyHelper` and this project's auth is subscription OAuth (05-RESEARCH.md Decision 6). Adopting it would require provisioning and paying for a separate API key. |
| `--allowedTools <tools...>` | OPT-OUT | not needed — the benchmark is a pure-writing task; the tool surface is closed by `--disallowedTools`, and an allow-list would add a second, redundant control over the same thing. |
| `--append-system-prompt` / `--system-prompt` / `--system-prompt-file` | OPT-OUT | explicitly out of scope — Decision 3 fixes baseline prompt parity as "bare scenario prompt vs. real skill-folder install". Injecting a system prompt would make the skill-on condition something other than how a real user invokes the skill. |
| `--resume` / `--continue` / `--fork-session` | OPT-OUT | not needed — every benchmark cell is a fresh single-turn session by design; conversation state would contaminate repeats. |
| `--output-format stream-json` and its companions (`--include-partial-messages`, `--forward-subagent-text`, `--include-hook-events`) | OPT-OUT | not needed — the runner reads one terminal result envelope per call; streaming adds parse surface with no measurement value. |
| `--fallback-model` | OPT-OUT | explicitly out of scope — EVAL-05 requires the model string be pinned and recorded per result. A silent fallback would record a model that did not produce the text. |
| `--agents` / `--agent` / `--mcp-config` / `--plugin-dir` / `--add-dir` | OPT-OUT | not needed — the only context the session may see is the scenario prompt and, in the skill-on condition, the installed skill folder. Every one of these widens ambient context and breaks condition parity. |
| `--permission-prompts none` | OPT-OUT | not needed yet — `--disallowedTools` alone sufficed in the research session's live calls. Revisit only if an unattended run is observed stalling on a prompt. |
| `--dangerously-skip-permissions` / `--allow-dangerously-skip-permissions` | OPT-OUT | explicitly out of scope — the runner needs no write tools at all, so bypassing permission checks buys nothing and removes a guard. |
| `--betas` | OPT-OUT | not needed — API-key users only; this project authenticates by subscription OAuth. |
| `--cloud` / `--environment` / `--bg` | OPT-OUT | not needed — the matrix runs serially on the operator's machine, which is also what makes the wall-clock and cost figures in RESULTS.md reproducible. |
| `--autocompact` | OPT-OUT | not needed — single-turn sessions never reach a compaction boundary. |
| `--settings` | OPT-OUT | not needed — the isolated temp directory already supplies the only configuration that matters (presence or absence of the skill folder). |
| `--chrome` / `--ide` / `--file` / `--from-pr` / `--brief` / `--debug` | OPT-OUT | explicitly out of scope — interactive/IDE/diagnostic surface with no role in a headless measurement. |

**Not carried over from a prior integration.** `evals/conformance/run_conformance.py` is this
repository's first `claude -p` integration. Its own flag choices were re-decided from a full
coverage baseline above rather than inherited, per the fragment's second-integration rule.
Two of its choices are deliberately *not* reused: it passes no `--effort` (EVAL-05 requires
effort be pinned and recorded, so this phase pins it) and no `--max-budget-usd` (this phase
adds one, since this matrix spends roughly 50× what a conformance run does).
