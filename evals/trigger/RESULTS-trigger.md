# Trigger Pressure Test — Run Results

Produced by `python3 evals/trigger/run_trigger_test.py`. Each row below is one live
`claude -p` session in a fresh temp directory outside this repository, with only
`skills/proof-first/` copied into its `.claude/skills/`, no `--bare`, and nothing in the
prompt naming the skill. The verdict is read from the session's own event stream (a
`Skill` tool-use naming `proof-first`), not from the prose it produced.

## Run

| Field | Value |
|---|---|
| Date | 2026-09-20 |
| Model | `claude-sonnet-5` |
| Harness | `claude` 2.1.267 (Claude Code) |
| SKILL.md description sha256 (first 14 lines) | `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675` |
| Sessions | 14 |

## Verdicts

| Table | Phrasing | Expected | Observed | Match |
|---|---|---|---|---|
| must-fire | Write our response to RFP question 4 about the cut-over plan. | Fires | fired | yes |
| must-fire | We got an RFI back from procurement — draft the answers. | Fires | fired | yes |
| must-fire | Draft the solution proposal section for the migration approach. | Fires | fired | yes |
| must-fire | I need an executive summary for the Halverton board deck. | Fires | fired | yes |
| must-fire | Write the demo script for tomorrow's discovery call. | Fires | fired | yes |
| must-fire | Turn these discovery notes into the after-state section of the proposal. | Fires | fired | yes |
| must-fire | Help me write this presales response before it ships to the customer. | Fires | fired | yes |
| must-fire | We're putting together our bid response — write the commercial section. | Fires | fired | yes |
| must-fire | This is a scored technical response — write section 3 so it holds up. | Fires | fired | yes |
| must-not-fire | Write launch copy for our new product announcement. | Does not fire | did not fire | yes |
| must-not-fire | Build me a slide deck for the kickoff meeting. | Does not fire | fired | NO |
| must-not-fire | Work out pricing and sizing for a 500-seat deployment. | Does not fire | fired | NO |
| must-not-fire | Write the API reference docs for the /migrations endpoint. | Does not fire | did not fire | yes |
| must-not-fire | Rewrite this paragraph in plain English for a general reader. | Does not fire | did not fire | yes |

## Totals

- Sessions run: 14
- Scoreable: 14
- Matched expectation: 12
- Did not match expectation: 2
- Unscoreable (session failed, no verdict claimed): 0

## Honest caveats

- One session per phrasing on one Anthropic-hosted model. This is a set of single
  observations, not a rate; no percentage is computed from it anywhere in this repository.
- `claude -p` exposes no temperature or seed flag, so the run is not deterministic and a
  repeat can differ. A non-fire here is a non-fire in this session, not a proof that the
  description can never fire on that phrasing.
- `--bare` is deliberately off, because skill auto-discovery is the behaviour under test.
  The operator's user-level `$HOME` configuration therefore still loads, so other
  installed skills were present in every session.
- The verdicts bind to the `description` whose hash is recorded above. If that description
  changes, these observations must be re-run, not carried forward.

---

## Run — Arm B (control) — 439-character description, head-14 sha256 d5dd651a…

| Field | Value |
|---|---|
| Date | 2026-09-20 |
| Model | `claude-sonnet-5` |
| Harness | `claude` 2.1.267 (Claude Code) |
| SKILL.md description sha256 (first 14 lines) | `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675` |
| Repeats per phrasing | 5 |
| Sessions planned | 70 |
| Sessions scoreable | 70 |

### Verdicts

| Table | Phrasing | Expected | Observed | Match | Clopper-Pearson upper bound (alpha 0.05) |
|---|---|---|---|---|---|
| must-fire | Write our response to RFP question 4 about the cut-over plan. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | We got an RFI back from procurement — draft the answers. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | Draft the solution proposal section for the migration approach. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | I need an executive summary for the Halverton board deck. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | Write the demo script for tomorrow's discovery call. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | Turn these discovery notes into the after-state section of the proposal. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | Help me write this presales response before it ships to the customer. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | We're putting together our bid response — write the commercial section. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | This is a scored technical response — write section 3 so it holds up. | Fires | fired 5 of 5 scoreable | yes | - |
| must-not-fire | Write launch copy for our new product announcement. | Does not fire | fired 0 of 5 scoreable | yes | 0.4507 |
| must-not-fire | Build me a slide deck for the kickoff meeting. | Does not fire | fired 5 of 5 scoreable | NO | - |
| must-not-fire | Work out pricing and sizing for a 500-seat deployment. | Does not fire | fired 4 of 5 scoreable | NO | - |
| must-not-fire | Write the API reference docs for the /migrations endpoint. | Does not fire | fired 0 of 5 scoreable | yes | 0.4507 |
| must-not-fire | Rewrite this paragraph in plain English for a general reader. | Does not fire | fired 0 of 5 scoreable | yes | 0.4507 |

### Totals

- OF (over-fires, must-not-fire rows) = 9
- SN (scoreable, must-not-fire rows) = 25
- MH (must-fire hits) = 45
- SM (scoreable, must-fire rows) = 45

---

## Run — Arm A (treatment) — 551-character description with exclusion clause, head-14 sha256 9049c7d8…

| Field | Value |
|---|---|
| Date | 2026-09-20 |
| Model | `claude-sonnet-5` |
| Harness | `claude` 2.1.267 (Claude Code) |
| SKILL.md description sha256 (first 14 lines) | `9049c7d82fadce008b00cdf70c7dc74add0d23691c7c61b8d586740a3beb3e1e` |
| Repeats per phrasing | 5 |
| Sessions planned | 70 |
| Sessions scoreable | 70 |

### Verdicts

| Table | Phrasing | Expected | Observed | Match | Clopper-Pearson upper bound (alpha 0.05) |
|---|---|---|---|---|---|
| must-fire | Write our response to RFP question 4 about the cut-over plan. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | We got an RFI back from procurement — draft the answers. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | Draft the solution proposal section for the migration approach. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | I need an executive summary for the Halverton board deck. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | Write the demo script for tomorrow's discovery call. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | Turn these discovery notes into the after-state section of the proposal. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | Help me write this presales response before it ships to the customer. | Fires | fired 5 of 5 scoreable | yes | - |
| must-fire | We're putting together our bid response — write the commercial section. | Fires | fired 0 of 5 scoreable | NO | 0.4507 |
| must-fire | This is a scored technical response — write section 3 so it holds up. | Fires | fired 5 of 5 scoreable | yes | - |
| must-not-fire | Write launch copy for our new product announcement. | Does not fire | fired 0 of 5 scoreable | yes | 0.4507 |
| must-not-fire | Build me a slide deck for the kickoff meeting. | Does not fire | fired 0 of 5 scoreable | yes | 0.4507 |
| must-not-fire | Work out pricing and sizing for a 500-seat deployment. | Does not fire | fired 0 of 5 scoreable | yes | 0.4507 |
| must-not-fire | Write the API reference docs for the /migrations endpoint. | Does not fire | fired 0 of 5 scoreable | yes | 0.4507 |
| must-not-fire | Rewrite this paragraph in plain English for a general reader. | Does not fire | fired 0 of 5 scoreable | yes | 0.4507 |

### Totals

- OF (over-fires, must-not-fire rows) = 0
- SN (scoreable, must-not-fire rows) = 25
- MH (must-fire hits) = 40
- SM (scoreable, must-fire rows) = 45

### Findings and Decision

Comparing Arm A against Arm B:
- **Over-fire suppression**: `p_attr = fisher_exact_two_tailed(9, 16, 0, 25) = 0.0016` (computed with `evals/trigger/stats.py`) on the pooled over-fire 2x2. The elimination of all must-not-fire over-fires was statistically significant ($p < 0.05$), confirming that the negative exclusion clause effectively suppressed unwanted activations on near-miss phrasings.
- **Must-fire recall regression**: However, one must-fire row (*"We're putting together our bid response — write the commercial section"*) regressed from `5 of 5` firings under Arm B to `0 of 5` under Arm A. The negative clause's reference to "commercial modelling" appears to have caused semantic suppression of legitimate commercial presales requests.

**Decision & Reversion**:
Per the pre-registered protocol in `evals/trigger/DECISION-RULE-cat10.md`, preserving must-fire recall takes strict precedence over suppressing over-fires. Because the candidate description regressed on legitimate presales writing, the 551-character intervention was reverted, and the baseline 439-character description (sha256 `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`) was retained.

The baseline description's measured over-fire rate (`OF_B/SN_B = 9/25` across must-not-fire sessions at n=5) remains documented in `README.md` and this evaluation suite as an accepted known limitation.
