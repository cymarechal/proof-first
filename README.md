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

This repository is in early construction. The foundational scaffolding is in place; the skill
itself has not been written yet.

What exists today:

- `NUMBERING.md` — the frozen rule-ID registry.
- `examples/deal-brief.md` — the one canonical fictional deal every worked example will cite.
- `LICENSE` — the MIT grant.
- `NOTICES.md` — the trademark and attribution posture.
- `SOURCES.md` — the approved-source list and the paraphrase boundary.
- `tools/check_repo.py` — a stdlib-only checker enforcing all of the above, wired into CI.

What does not exist yet:

- The skill itself.
- Its reference files.
- The distribution manifests.
- The output style.
- The paste-able system prompt.
- The worked before-and-after examples.
- The evaluation harness.

No measured claim is published in this repository yet. The benchmark has not run. Any number
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
│           ├── completeness-audit.md   (planned)
│           ├── artifact-patterns.md    (planned)
│           └── deletion-test.md
├── output-styles/
│   └── proof-first.md                  (planned)
├── prompts/
│   └── system-prompt.md                (planned)
├── examples/
│   ├── deal-brief.md                   (exists)
│   └── before-after.md                 (planned)
├── evals/
│   └── pressure-tests.md
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
