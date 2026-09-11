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

## Must fire

Each phrasing below draws on a term the frontmatter `description` itself front-loads (RFP, RFI,
solution proposal, executive summary, demo or discovery material, presales, bid, scored technical
response), phrased the way a writer actually asks rather than as a bare keyword.

| Phrasing | Expected | Observed | Date | Harness |
|---|---|---|---|---|
| Write our response to RFP question 4 about the cut-over plan. | Fires | not yet observed | — | — |
| We got an RFI back from procurement — draft the answers. | Fires | not yet observed | — | — |
| Draft the solution proposal section for the migration approach. | Fires | not yet observed | — | — |
| I need an executive summary for the Halverton board deck. | Fires | not yet observed | — | — |
| Write the demo script for tomorrow's discovery call. | Fires | not yet observed | — | — |
| Turn these discovery notes into the after-state section of the proposal. | Fires | not yet observed | — | — |
| Help me write this presales response before it ships to the customer. | Fires | not yet observed | — | — |
| We're putting together our bid response — write the commercial section. | Fires | not yet observed | — | — |
| This is a scored technical response — write section 3 so it holds up. | Fires | not yet observed | — | — |

## Must not fire

Each near-miss phrasing sits just outside the skill's stated scope — PROJECT.md's Out of Scope
list and SKILL.md's own Limits section — which is exactly what makes a correct non-fire on these
rows meaningful rather than incidental.

| Phrasing | Expected | Observed | Date | Harness |
|---|---|---|---|---|
| Write launch copy for our new product announcement. | Does not fire | not yet observed | — | — |
| Build me a slide deck for the kickoff meeting. | Does not fire | not yet observed | — | — |
| Work out pricing and sizing for a 500-seat deployment. | Does not fire | not yet observed | — | — |
| Write the API reference docs for the /migrations endpoint. | Does not fire | not yet observed | — | — |
| Rewrite this paragraph in plain English for a general reader. | Does not fire | not yet observed | — | — |

## Observations

No row above carries a real observation. Running this pressure test requires installing
`skills/proof-first/` into a harness's own skills directory and driving a fresh session per
phrasing — an interactive, per-session harness action this execution environment cannot perform:
it has no way to launch a separate Claude Code (or other harness) session, install a skill into
it, and read back whether that session activated. Every Observed cell above therefore reads
`not yet observed` rather than a claimed result, per this repository's evidence rule (PROJECT.md
§ Constraints: measured claims or no claims).

This gap is logged as an open unrun-verify entry in `.planning/WINDOWS.md`, naming this file and
this method, exactly as Phase 1 logged its own two unrun `<manual>` verification steps. A human
running each phrasing above in a real harness session, filling in the Observed/Date/Harness
columns, and marking the ledger entry fixed is what closes it — not an estimate written here.

Nothing in this file states a trigger-reliability rate, a percentage, or a score. That number does
not exist yet; it is Phase 5's job to produce one, reproducibly, from a committed benchmark run.
