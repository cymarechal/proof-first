# Trigger Pressure Test

This file records whether Proof First's frontmatter `description` actually fires the skill on the
phrasings a writer would use, and stays quiet on the phrasings that sit just outside its stated
scope. Method: run each phrasing in a fresh harness session with the skill installed, with nothing
else in the prompt to bias activation, and record whether the skill activated. A must-not-fire row
is the load-bearing half of this file — a description that fires on everything is not a trigger
list, it is a catch-all, and the near-miss rows below are what tells the two apart. An Observed
cell that was not actually run is recorded as `not yet observed`, never left blank and never
claimed as a result. Trigger reliability at scale — a measured rate across many phrasings and
models — is Phase 5's eval-harness work; this file records a method and, where available, a real
observation, never an extrapolated figure.

## Scope

The 14 phrasings below were authored against, and must be run against, the frontmatter
`description` in `skills/proof-first/SKILL.md` as of the commit this note lands in. That
description's first line reads `Write or check RFP and RFI responses, solution proposals,
executive` and its whitespace-collapsed length is 439 characters — both greppable facts an
auditor can check against the live file without this note carrying a second copy of the
description text, which would only create a place for the two to silently drift apart.

The Phase 2 gap-closure trim (plan 02-07) did not modify this `description` — its frontmatter is
byte-identical before and after that trim (sha256 of `SKILL.md`'s first 14 lines:
`d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`) — so every row below remains
runnable exactly as written; none was invalidated by that trim.

An observation recorded in the tables below is valid only for the `description` it was run
against. If the `description` changes in a later phase, previously recorded observations must be
re-run against the new text rather than carried forward as still-current.

Every row below now carries a real observation, recorded 2026-09-20 against the description whose
hash is named above. They were produced by `evals/trigger/run_trigger_test.py`, which starts one
fresh `claude -p` session per phrasing in a temp directory outside this repository with only
`skills/proof-first/` installed, and reads activation from the session's own event stream rather
than from the prose it produced. The earlier note here said this environment could not start such
a session; that was true when written and is no longer true — the method was proven during Phase
3 and is now a committed script.

## Must fire

Each phrasing below draws on a term the frontmatter `description` itself front-loads (RFP, RFI,
solution proposal, executive summary, demo or discovery material, presales, bid, scored technical
response), phrased the way a writer actually asks rather than as a bare keyword.

| Phrasing | Expected | Observed | Date | Harness |
|---|---|---|---|---|
| Write our response to RFP question 4 about the cut-over plan. | Fires | fired | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| We got an RFI back from procurement — draft the answers. | Fires | fired | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Draft the solution proposal section for the migration approach. | Fires | fired | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| I need an executive summary for the Halverton board deck. | Fires | fired | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Write the demo script for tomorrow's discovery call. | Fires | fired | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Turn these discovery notes into the after-state section of the proposal. | Fires | fired | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Help me write this presales response before it ships to the customer. | Fires | fired | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| We're putting together our bid response — write the commercial section. | Fires | fired | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| This is a scored technical response — write section 3 so it holds up. | Fires | fired | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |

## Must not fire

Each near-miss phrasing sits just outside the skill's stated scope — PROJECT.md's Out of Scope
list and SKILL.md's own Limits section — which is exactly what makes a correct non-fire on these
rows meaningful rather than incidental.

| Phrasing | Expected | Observed | Date | Harness |
|---|---|---|---|---|
| Write launch copy for our new product announcement. | Does not fire | did not fire | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Build me a slide deck for the kickoff meeting. | Does not fire | fired | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Work out pricing and sizing for a 500-seat deployment. | Does not fire | fired | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Write the API reference docs for the /migrations endpoint. | Does not fire | did not fire | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Rewrite this paragraph in plain English for a general reader. | Does not fire | did not fire | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |

## Observations

Run 2026-09-20, `claude-sonnet-5` on `claude` 2.1.267, one session per phrasing, 14 of 14
scoreable. Full run block with caveats: `evals/trigger/RESULTS-trigger.md`.

**Must fire: 9 of 9 fired.** Every phrasing drawn from a term the description front-loads
activated the skill on the description alone, with nothing in the prompt naming it.

**Must not fire: 3 of 5 stayed quiet. Two fired.** This is the finding, and it is the half of this
file that was built to catch it:

| Phrasing | Observed | What it means |
|---|---|---|
| Build me a slide deck for the kickoff meeting. | fired | A kickoff deck is not a scored response, a proposal, or a check pass over a draft. |
| Work out pricing and sizing for a 500-seat deployment. | fired | Pricing and sizing is a commercial calculation, not presales writing. |

Both sit outside PROJECT.md's scope and outside the Limits section of `SKILL.md`, and the skill
still activated. The likely pull is the description's two broadest phrases — "for technical
presales and bid teams", which names an audience rather than a document, and "a customer-facing
proposal", which a model can read as any customer-facing deliverable. A description that names who
the reader is rather than what the document is will collect work that merely happens near presales.

What this does and does not establish. It establishes that the must-fire half of the trigger list
works on this model and this harness, and that the description is measurably over-broad on 2 of 5
near-miss phrasings. It does not establish a rate: one session per phrasing is one observation, and
`claude -p` exposes no temperature or seed flag, so a repeat can differ. No percentage is computed
from these 14 rows anywhere in this repository.

Reproduce with:

    python3 evals/trigger/run_trigger_test.py --model claude-sonnet-5

The runner refuses to fill in any row if the live `description` no longer hashes to the value bound
in the Scope section above — an observation recorded against a different description is not an
observation of these rows.

Narrowing the description is a change to a shipped, distributed trigger surface, so it is recorded
here as a measured defect rather than patched inside the run that found it. Tracked in
`.planning/WINDOWS.md`.
