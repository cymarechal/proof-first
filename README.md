# Proof First

An agent skill for technical presales writing that replaces adjectives with specificity and evidence.

## What this is

Proof First is a public, MIT-licensed agent skill for technical presales writing: RFP and RFI
responses, solution proposals, executive summaries, and demo and discovery material. It is built
for presales engineers, solution architects, and bid teams who need a document a technical
evaluator finishes believing the author genuinely understands their problem. It is vendor-neutral
— usable by anyone, regardless of who they sell for — and it has zero dependencies: one folder,
no install step.

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
- `evals/pressure-tests.md` — the trigger-pressure-test method; no observation has been recorded
  yet, see the file itself.
- `evals/conformance/run_conformance.py` — a stdlib-only, self-testing scorer that drives live
  sessions against the shipped skill and checks whether each one names its artifact family before
  drafting, the write-mode conformance contract this repository calls MOD-04.
- `evals/conformance/RESULTS-mod04.md` — this repository's one committed measurement, a MOD-04
  write-mode conformance run, with its own caveats stated in the file.
- `LICENSE` — the MIT grant.
- `NOTICES.md` — the trademark and attribution posture.
- `SOURCES.md` — the approved-source list and the paraphrase boundary.
- `tools/check_repo.py` — a stdlib-only checker enforcing all of the above, wired into CI.

What does not exist yet:

- The distribution manifests (`.claude-plugin/`).
- The output style.
- The paste-able system prompt.
- The worked before-and-after examples.
- Phase 5's skill-on/skill-off, multi-model, judge-scored persuasion benchmark (the pressure-test
  method exists; no observations are recorded yet).

This repository discloses one measured v1 limitation: whether a live write-mode session names its
artifact family before its first rule citation, reproducible from the committed, stdlib-only
`evals/conformance/run_conformance.py` script. Measured 2026-09-16, under the anchored scorer,
across five committed fixtures: `claude-sonnet-5` conformed in 3 of 10 scoreable sessions
(30.0%) — a 10-point decline against a paired same-instrument baseline of the immediately prior
skill version at 4 of 10 (40.0%). This is a known, accepted, disclosed v1 limitation of live
model behavior, not a quality or persuasion claim — the shipped classification instruction and
its two mechanical gates (family-line presence, family-line ordering) are present and enforced
in `SKILL.md` regardless of what any individual live session does. Full run-by-run figures,
exclusions, and caveats live in `evals/conformance/RESULTS-mod04.md` — read that file before
trusting anything downstream of it, including its "v1 disposition decision (03-15)" section
recording why this residual is accepted for v1 rather than pursued further. At minimum: both
measured models are Anthropic-hosted, the harness gives no determinism guarantee (no temperature
or seed flag), and every figure recorded
before this project's own scorer-anchoring fix (see that file's "Scorer anchoring correction
(CR-01)" section) is an optimistic, unrecoverable ceiling, not comparable to the anchored figures
above.

This is not the persuasion benchmark. The skill-on/skill-off, multi-model, judge-scored benchmark
that will eventually let this README state a headline persuasion or quality number is Phase 5's
and has not run. No persuasion or quality claim is made anywhere in this repository. Any number
this README ever carries in the future will be sourced from committed benchmark results, and it
will state the model versions and the date it was produced.

## Repository layout

The tree below shows the target layout. Entries marked "planned" are documented here but not yet
created — this repository does not ship empty placeholder files for work that has not started.

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
│   └── proof-first.md                  (planned)
├── prompts/
│   └── system-prompt.md                (planned)
├── examples/
│   ├── deal-brief.md                   (exists)
│   └── before-after.md                 (planned)
├── evals/
│   ├── pressure-tests.md
│   └── conformance/                     (exists)
│       ├── run_conformance.py          (exists)
│       ├── fixtures/                   (exists)
│       ├── transcripts/                (exists)
│       └── RESULTS-mod04.md            (exists)
├── .claude-plugin/                     (planned)
├── tools/
│   └── check_repo.py                   (exists)
├── .github/
│   └── workflows/
│       └── ci.yml                      (exists)
├── LICENSE                             (exists)
├── NOTICES.md                          (exists)
├── SOURCES.md                          (exists)
├── NUMBERING.md                        (exists)
└── README.md                           (exists — this file)
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
