# NUMBERING.md

Authoritative ID registry for Proof First's two rule namespaces. This file is the single source
of truth `tools/check_repo.py` reads its ranges from — widening a range here changes enforcement
everywhere, not just in this document.

## Namespaces

`PF-<section>.<n>` addresses the numbered prose rule catalog. `MC-<n>` addresses the MEDDICC
completeness audit. The two namespaces are disjoint: no ID exists in both. A citation is always
prefixed — never a bare number — because a check-mode report can audit both catalogs in the same
line, and `PF-2.3` and `MC-2` printed side by side must never be mistaken for the same kind of
thing that two bare numbers (`2.3` and `2`) drawn from unrelated catalogs would be.

## PF reserved ranges

| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-0 | PF-0.1-PF-0.9 | Opening / Reframe | 1 | PF-0.2 |
| PF-1 | PF-1.1-PF-1.28 | Structure — the message-articulation spine | 9 | PF-1.26 |
| PF-2 | PF-2.1-PF-2.20 | Proof and Integrity | 1 | PF-2.12 |
| PF-3 | PF-3.1-PF-3.10 | Specificity and Buzzwords | 1 | PF-3.2 |
| PF-4 | PF-4.1-PF-4.20 | Prose Mechanics | 0 | PF-4.1 |
| PF-5 | PF-5.1-PF-5.10 | Consistency and Voice | 0 | PF-5.1 |

## PF-1 sub-blocks

`PF-1`'s reserved range (`PF-1.1`-`PF-1.28`) is carved into seven named sub-blocks, one per
Command of the Message element. A contributor adding a rule reads the element name below rather
than inferring it from a number.

| Element | Range |
|---|---|
| Before scenario | PF-1.1-PF-1.4 |
| After scenario | PF-1.5-PF-1.8 |
| Required Capabilities | PF-1.9-PF-1.12 |
| Metrics | PF-1.13-PF-1.16 |
| Proof Points | PF-1.17-PF-1.20 |
| Differentiators | PF-1.21-PF-1.24 |
| Positive Business Outcomes | PF-1.25-PF-1.28 |

Ceiling: `PF-1.28`, four slots per element, uniform headroom. Twenty slots do not divide evenly
across seven elements — six elements would get three slots and Positive Business Outcomes (the
element most likely to grow, since it is where quantified outcome rules land) would get only two,
forcing an early major-version widening. Widening to 28 exercises the explicit "unless planning
surfaces a reason to widen a block" clause this phase's context recorded for exactly this
situation, and gives every element the same room to grow. This supersedes the `PF-1.20` figure
proposed in `.planning/research/ARCHITECTURE.md:166`, which was a research proposal, not a locked
decision — seven elements do not divide evenly into twenty slots.

## PF-2 sub-blocks

`PF-2`'s reserved range (`PF-2.1`-`PF-2.20`) is carved into two named sub-blocks: Proof rules
attach evidence and name its source; Integrity rules refuse fabrication and flag what needs human
review. A rule added later to Integrity must not land next to a Proof rule — the two are
different jobs, and the range split keeps a contributor from inferring the wrong one from a bare
number.

| Element | Range |
|---|---|
| Proof | PF-2.1-PF-2.10 |
| Integrity | PF-2.11-PF-2.20 |

## MC reserved blocks

| Dimension | Range |
|---|---|
| Metric | MC-1-MC-5 |
| Economic Buyer | MC-6-MC-10 |
| Decision Criteria | MC-11-MC-15 |
| Decision Process | MC-16-MC-20 |
| Paper Process | MC-21-MC-25 |
| Pain | MC-26-MC-30 |
| Champion | MC-31-MC-35 |
| Competition | MC-36-MC-40 |

Ceiling: `MC-40`.

## Allocated IDs

Rows are kept sorted ascending by ID. Phase 2 adds `PF-*` rows as prose rules are written; Phase 3
adds `MC-*` rows as the completeness audit is written.

| ID | Title | Defined in | Added in |
|---|---|---|---|
| PF-0.1 | The opening reframe | SKILL.md | v0.1.0 |
| PF-1.1 | Name the current state in the buyer's own terms | SKILL.md | v0.1.0 |
| PF-1.2 | Name what the current state costs | SKILL.md | v0.1.0 |
| PF-1.5 | State the after-state as an observable change, paired with its before | SKILL.md | v0.1.0 |
| PF-1.9 | State the capability the buyer needs, not the product that has it | SKILL.md | v0.1.0 |
| PF-1.13 | Name the measure and its current baseline | SKILL.md | v0.1.0 |
| PF-1.14 | Name where the baseline came from | SKILL.md | v0.1.0 |
| PF-1.17 | Attach one comparable, verifiable proof to each capability claim | SKILL.md | v0.1.0 |
| PF-1.21 | Claim a differentiator only where a named alternative cannot do it | SKILL.md | v0.1.0 |
| PF-1.25 | Tie the outcome to the stated priority of the person who owns it | SKILL.md | v0.1.0 |
| PF-2.11 | Never invent a metric, a baseline, or a benchmark number | SKILL.md | v0.1.0 |
| PF-3.1 | The deletion test | SKILL.md | v0.1.0 |

## Deprecated IDs

A retired ID is recorded here with the version it was retired in and what absorbed it, and it is
never reassigned to new content in any future version — the guarantee only holds if it has always
held. Zero rules are deprecated as of this plan.

| ID | Deprecated in | Absorbed by |
|---|---|---|

## Range exhaustion

A section's reserved range is a hard ceiling. An allocated ID above its section's ceiling, below
its section's start, or inside another section's range is a build failure, not a judgement call —
`tools/check_repo.py` exits non-zero on it. Widening a range is a major-version action recorded in
this file, naming the version that widened it. The same rule holds for MC dimension blocks: an ID
outside the reserved MC range is a build failure.

## Versioning

Semantic versioning is carried in the skill's frontmatter `metadata` and in the plugin manifest,
matched by a git tag. Patch means a wording change with no rule added, removed, or renumbered.
Minor means a rule added inside an existing reserved range. Major means a rule deprecated or a
section restructured. Rule numbers are stable within a major version; only a major version bump
may renumber a rule, and only with a published migration note.

## Next free ID

To find the next free ID in a section or dimension block: if the section or block has zero
allocations, the next free ID is that section's or block's range start (for example, the next free
ID in `PF-2` with zero allocations is `PF-2.1`). If the section or block has allocations, the next
free ID is one above the highest allocated ID in that section or block — never a gap-filling reuse
of a deprecated number.
