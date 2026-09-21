# Proof First

An agent skill for technical presales writing that replaces adjectives with specificity and evidence.

## Before and after

Below: an unrevised draft, then a rewrite. The rewrite's numbers come from the one shared
canonical deal brief this repository ships. One full pair, reproduced from
`examples/before-after.md`:

**RFP and RFI response**

✗ "Kestrel Systems Group brings decades of experience delivering large-scale cloud transformations for complex, regulated enterprises across many industries. Our proven methodology and world-class team have consistently delivered exceptional outcomes for clients facing challenges like Halverton Mutual's. Before turning to the specific migration approach Question 1 asks for, it is worth noting the breadth of our platform expertise and the strength of our partner ecosystem. Our approach is comprehensive and follows industry best practices, backed by a proven cut-over methodology and rigorous testing."
✓ "Question 1, the highest-weighted scored question in this RFP at 30%, asks for the migration approach and cut-over plan. Kestrel Systems Group moves Halverton Mutual's 850-VM VMware vSphere estate and 40 Oracle Database instances to Amazon EC2 and Amazon Aurora PostgreSQL. Each cut-over runs inside its own scheduled maintenance window. Settlement-batch completion is validated against the required 6-hour window before the next cut-over proceeds."

Rules applied: PF-2.1, MC-11.

`PF-` and `MC-` are this project's two rule namespaces. `NUMBERING.md` is the registry that
defines every ID; `skills/proof-first/references/checklist.md` indexes them.

The other three artifact families this skill classifies — solution proposal, executive summary,
and demo and discovery material — each have their own full before/after pair in
[`examples/before-after.md`](examples/before-after.md).

## What this is

Proof First is a public, MIT-licensed agent skill for technical presales writing: RFP and RFI
responses, solution proposals, executive summaries, and demo and discovery material. It is built
for presales engineers, solution architects, and bid teams who need a document a technical
evaluator finishes believing the author genuinely understands their problem. It is vendor-neutral
— usable by anyone, regardless of who they sell for — and it has zero dependencies: one folder,
no install step.

## Install

Proof First supports four install paths: one for every harness the Agent Skills standard reaches,
two that are Claude Code's own, and one for a harness with no skill support.

Routes 1 and 2 name the publish-location placeholder `<owner>/<repo>`, which stands for wherever
this repository is published. Neither resolves until it is published. The placeholder is
deliberate and disclosed: `publish-location-drift` in `tools/check_repo.py` fails the build if any
command or manifest carrying it stops agreeing with the others.

Route 4 runs from a local clone with no step beyond the clone: `prompts/system-prompt.md` is a
committed file, and pasting it is the whole action. Route 3 runs from a local clone too, but it
needs one copy step first, stated in full below. `output-styles/` at this repository's root is
where a plugin ships an output style from, not a directory Claude Code scans, so the file is not
offered in `/config` until it is copied to one that is. Both routes 3 and 4 need that local clone,
and the clone URL is the same unpublished `<owner>/<repo>` as routes 1 and 2: until this repository
is published, there is no URL to clone from.

**1. Skills CLI** — for any harness the Agent Skills standard covers (Cursor, Codex, Copilot,
Gemini CLI, OpenCode, and the rest), install with the `skills` CLI's one-line command:

```
npx skills add <owner>/<repo>
```

**2. Claude Code plugin** — Claude Code installs this skill as a plugin from the marketplace
manifest committed in this repository at `.claude-plugin/`:

```
claude plugin marketplace add <owner>/<repo> && claude plugin install proof-first@proof-first
```

Or inside a running Claude Code session:

```
/plugin marketplace add <owner>/<repo>
/plugin install proof-first@proof-first
```

**3. Output style** — `output-styles/proof-first.md` is a Claude Code output style, generated
mechanically from the skill content rather than written separately. Copy it into the directory
Claude Code scans for output styles, then select it through `/config`; once selected it stays on
for the whole session.

```
mkdir -p ~/.claude/output-styles
cp output-styles/proof-first.md ~/.claude/output-styles/
```

Use a project's own `.claude/output-styles/` instead of `~/.claude/output-styles/` to scope the
style to that project. What this repository checks is that the file exists and that this README
names the directory it has to reach. That a Claude Code session then lists it in `/config` has not
been observed here. This repository does drive live sessions — `evals/conformance/run_conformance.py`
runs headless `claude -p`, and the conformance figure under `## Status` comes from those sessions —
but a headless session has no `/config` picker, so the picker is the one link in this route nothing
here exercises.

What is now observed is the rest of the route. `evals/routes/run_routes.py` copied this file into a
headless session's own `.claude/output-styles/`, named it in that session's `.claude/settings.json`,
and the session cited this project's rule markers where an unrouted control session on the same
prompt cited none. Twelve sessions under this route reached the artifact-family line; see
`evals/routes/RESULTS-routes.md`.

**4. System prompt** — `prompts/system-prompt.md` is a paste-able system prompt for a harness with
no skill support: paste it whole into a system-prompt field, an `AGENTS.md`, or an equivalent.

The output style and the system prompt carry the same rule text, the same completeness audit, and
the same artifact-family conventions as the skill, proven by a check in this repository. Whether a
session driven by either behaves like one with the skill folder installed is now measured rather
than asserted: 36 headless sessions, three routes, four artifact families, recorded in
`evals/routes/RESULTS-routes.md`. That run did not distinguish the three routes — every pair of
arms has overlapping observed ranges on the mechanical proxy count — which is a weaker statement
than equivalence and is the only one the records support. Read the caveats there before reading
anything else into it; one of them matters for choosing between routes. The installed skill has to
be triggered and was not in 3 of its 12 sessions, while the output style and the pasted prompt are
unconditionally on once selected.

## Status

This repository is under active construction. `NUMBERING.md`'s rule-ID registry, the
`skills/proof-first/` rule catalog and its reference files, and the integrity checker are in
place.

What exists today:

- `NUMBERING.md` — the frozen rule-ID registry.
- `skills/proof-first/SKILL.md` — the 31-rule prose catalog.
- `skills/proof-first/references/checklist.md` — the rule-ID index.
- `skills/proof-first/references/completeness-audit.md` — the MEDDICC-derived completeness audit, in its own `MC-` namespace.
- `skills/proof-first/references/artifact-patterns.md` — the four artifact families' conventions and expected orders.
- `skills/proof-first/references/deletion-test.md` — deletion-test edge cases.
- `skills/proof-first/references/worked-examples.md` — the 28 worked ✗/✓ pairs, keyed by rule ID.
- `examples/deal-brief.md` — the one canonical fictional deal every worked example cites.
- `evals/pressure-tests.md` — the trigger-pressure-test method and its 14 recorded observations.
- `evals/lint.py` — the stdlib-only mechanical proxy linter the benchmark counts with.
- `evals/trigger/run_trigger_test.py` — a stdlib-only, self-testing runner that drives one live
  session per phrasing and reads activation from the session's own event stream.
- `evals/trigger/RESULTS-trigger.md` — the recorded run: 9 of 9 must-fire phrasings activated the
  skill, and 2 of 5 near-miss phrasings activated it when they should not have, with caveats
  stated in the file.
- `evals/conformance/run_conformance.py` — a stdlib-only, self-testing scorer that drives live
  sessions against the shipped skill and checks whether each one names its artifact family before
  drafting, the write-mode conformance contract this repository calls MOD-04.
- `evals/conformance/RESULTS-mod04.md` — a MOD-04 write-mode conformance run, with its own caveats
  stated in the file.
- `evals/routes/run_routes.py` — a stdlib-only, self-testing runner that measures whether the four
  install routes deliver equivalent behaviour.
- `evals/routes/RESULTS-routes.md` — the recorded route-equivalence run, published as a null
  result with its own caveats stated in the file.
- `evals/benchmark/run_benchmark.py` — the stdlib-only skill-on/skill-off benchmark runner and its
  free, offline `--report-only` recompute.
- `evals/benchmark/RESULTS.md` — the benchmark's committed figures, regenerable from the committed
  raw records.
- `LICENSE` — the MIT grant.
- `NOTICES.md` — the trademark and attribution posture.
- `SOURCES.md` — the approved-source list and the paraphrase boundary.
- `tools/check_repo.py` — a stdlib-only checker enforcing all of the above, wired into CI.
- `.claude-plugin/` — the Claude Code plugin manifests (`plugin.json`, `marketplace.json`).
- `output-styles/proof-first.md` — the output style.
- `prompts/system-prompt.md` — the paste-able system prompt.
- `examples/before-after.md` — the worked before-and-after examples.

What does not exist yet:

- Any human evaluation. No human evaluator has scored any text this repository produces. Every
  judged figure below is one language model's rating against a rubric.
- Any measurement outside Anthropic-hosted models. Every figure here comes from `claude-opus-5` and
  `claude-sonnet-5`; nothing establishes that any of it transfers to another vendor's model.
- Any claim that this skill makes documents more persuasive. The benchmark measured that directly
  and found the opposite — see the claim region below.

### What the benchmark measured

<!-- claim-region:start -->

The benchmark ran on 2026-09-18 across `claude-opus-5` and `claude-sonnet-5` and recorded 96
generations. Each scenario was drafted twice, once with the skill loaded and once without, and the
two drafts were judged blind against each other in both orders, with the orders averaged before a
pair was scored. That gives 48 both-orders-averaged pairs per judged dimension. Figures below are
regenerable offline with `python3 evals/benchmark/run_benchmark.py --report-only`.

On evidence, the skill-on draft won 45 pairs, tied 1 and lost 2, measured 2026-09-18 across
`claude-opus-5` and `claude-sonnet-5`.

On clarity, the skill-on draft won 32 pairs, tied 3 and lost 13, measured 2026-09-18 across
`claude-opus-5` and `claude-sonnet-5`.

On persuasive force, the skill-on draft lost 38 pairs. It won 7 and tied 3. The judge preferred the
un-skilled draft in four pairs out of five, measured 2026-09-18 across `claude-opus-5` and
`claude-sonnet-5`, and the direction is the same for both models rather than driven by one.

The mechanical proxy count does not move in one direction at all: across 16 (model, scenario) cells
measured 2026-09-18, the count is lower with the skill on in 8 cells, equal in 1 and higher in 7.
`claude-opus-5` improves and `claude-sonnet-5` worsens, so the two models move opposite ways.

What the persuasive-force result does and does not establish, for the 2026-09-18 run across
`claude-opus-5` and `claude-sonnet-5`: it is one language model's rating against a rubric, and no
human evaluator scored any text. The skill-off condition also received a materially shorter prompt
than the skill-on condition, so prompt length is not held constant between the two arms. Both
caveats are stated in full, with four others, in `evals/benchmark/RESULTS.md`.

One reading of the gap — that the skill trades persuasive framing for evidence density — is an
untested hypothesis, not a measurement. Nothing in the 2026-09-18 run across `claude-opus-5` and
`claude-sonnet-5` tests it. The per-generation texts are in `evals/benchmark/raw/` for a reader who
wants to judge it themselves.

<!-- claim-region:end -->

This repository discloses one measured v1 limitation: whether a live write-mode session names its
artifact family before its first rule citation, reproducible from the committed, stdlib-only
`evals/conformance/run_conformance.py` script.

Measured 2026-09-16, under the anchored scorer,
across five committed fixtures: `claude-sonnet-5` conformed in 3 of 10 scoreable sessions
(30.0%) — a 10-point decline against a paired same-instrument baseline of the immediately prior
skill version at 4 of 10 (40.0%).

This is a known, accepted, disclosed v1 limitation of live
model behavior, not a quality or persuasion claim — the shipped classification instruction and
its two mechanical gates (family-line presence, family-line ordering) are present and enforced
in `SKILL.md` regardless of what any individual live session does.

Full run-by-run figures,
exclusions, and caveats live in `evals/conformance/RESULTS-mod04.md` — read that file before
trusting anything downstream of it, including its "v1 disposition decision (03-15)" section
recording why this residual is accepted for v1 rather than pursued further.

Among those caveats, at minimum:
`claude-sonnet-5`, the only model behind the anchored figures above, is Anthropic-hosted; the
harness gives no determinism guarantee (no temperature or seed flag); and every figure recorded
before this project's own scorer-anchoring fix (see that file's "Scorer anchoring correction
(CR-01)" section) is an optimistic, unrecoverable ceiling, not comparable to the anchored figures
above — including the file's earlier, superseded `claude-opus-5` sessions, none of which sit
behind an anchored figure this README states.

The conformance limitation above is a separate measurement from the persuasion benchmark reported
in the claim region, and the two are never combined into one figure. Every number this README
carries is sourced from a committed results file under `evals/`, states the model versions and the
date it was produced, and is checked by `tools/check_repo.py` — `readme-claim-unsourced` fails the
build on a claim-region number that appears in no committed results file, and
`readme-claim-unanchored` fails it on a claim-region paragraph that carries a number without a
model string and a date.

## Keeping derivatives in sync

`output-styles/proof-first.md` and `prompts/system-prompt.md` are generated, not hand-written.
After editing `skills/proof-first/SKILL.md` or any of its reference files, run:

```
python3 tools/generate_derivatives.py
```

CI runs the generator's own `--check` mode and `tools/check_repo.py`'s `skill-derivative-stale`
code; either one fails the build if a derivative is committed stale, so skipping this step cannot
ship silently.

## Repository layout

The tree below shows this repository's layout. Every path it names exists in this repository
today.

```
proof-first/
├── skills/
│   └── proof-first/
│       ├── SKILL.md
│       └── references/
│           ├── checklist.md
│           ├── completeness-audit.md
│           ├── artifact-patterns.md
│           ├── deletion-test.md
│           └── worked-examples.md
├── output-styles/
│   └── proof-first.md
├── prompts/
│   └── system-prompt.md
├── examples/
│   ├── deal-brief.md
│   └── before-after.md
├── evals/
│   ├── pressure-tests.md
│   ├── proxy-sources.md
│   ├── lint.py
│   ├── conformance/
│   │   ├── run_conformance.py
│   │   ├── fixtures/
│   │   ├── transcripts/
│   │   └── RESULTS-mod04.md
│   ├── trigger/
│   │   ├── run_trigger_test.py
│   │   └── RESULTS-trigger.md
│   ├── routes/
│   │   ├── run_routes.py
│   │   ├── raw/
│   │   ├── probe/
│   │   └── RESULTS-routes.md
│   └── benchmark/
│       ├── run_benchmark.py
│       ├── scenarios.json
│       ├── bench-deal-brief.md
│       ├── fixtures/
│       ├── raw/
│       └── RESULTS.md
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── tools/
│   ├── check_repo.py
│   └── generate_derivatives.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── LICENSE
├── NOTICES.md
├── SOURCES.md
├── NUMBERING.md
└── README.md — this file
```

The skill lives at `skills/proof-first/`: the folder name must equal the frontmatter `name` field
the Agent Skills specification requires, and a single-folder upload to a harness or to claude.ai
is that one directory zipped with the folder as its root. `NOTICES.md`, `SOURCES.md`,
`NUMBERING.md`, `examples/`, `tools/`, and `evals/` stay at the repository root and never ship to
an installed user.

## Rule numbering

`NUMBERING.md` is the authoritative registry for this project's two rule namespaces: a
prose-rule prefix for the numbered writing catalog and a separate completeness-audit prefix for
the qualification checklist. Numeric ranges are reserved per section before any rule content is
drafted, so a rule added later inside its section's range never disturbs an existing citation.

## Versioning

Releases use semantic versioning, matched by a git tag. `NUMBERING.md`'s versioning section
states exactly what a patch, a minor, and a major bump each mean for this project's rule catalog.

## License and notices

Everything original in this repository is MIT-licensed. `LICENSE` carries the unmodified license
grant. `NOTICES.md` names the third-party frameworks this project's concepts derive from, states
non-affiliation with each rights-holder, and defines the paraphrase boundary. `SOURCES.md` lists
the approved public sources those concepts must trace to, and the material that is out of bounds
regardless of how readily it can be reproduced.

```
Concepts here are paraphrased from publicly described sales frameworks. Not affiliated with or endorsed by any framework rights-holder. See NOTICES.md.
```
