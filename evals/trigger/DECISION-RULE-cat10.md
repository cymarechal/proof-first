# Trigger Sensitivity Evaluation Protocol (CAT-10)

## 1. Overview & Objective

Requirement CAT-10 specifies that `skills/proof-first/SKILL.md`'s frontmatter `description` must trigger the skill reliably on presales writing requests while ignoring unrelated or excluded tasks.

Initial single-session pressure tests across 14 phrasings demonstrated:
- **Must-fire recall**: 9 of 9 presales writing phrasings correctly activated the skill.
- **Must-not-fire specificity**: 2 of 5 out-of-scope phrasings over-fired (`Build me a slide deck for the kickoff meeting.` and `Work out pricing and sizing for a 500-seat deployment.`). Both phrasings address activities that `SKILL.md` explicitly lists under `## Limits`, but which the activation classifier must judge purely from the frontmatter `description`.

This experiment evaluates an explicit exclusion clause appended to the description to determine whether negative guidance suppresses over-firing on adjacent presales tasks without impairing must-fire recall on core presales drafting.

---

## 2. Experimental Design

The evaluation executes an A/B benchmark using `evals/trigger/run_trigger_test.py`:
- **Model**: `claude-sonnet-5`
- **Replications**: 5 independent runs per phrasing
- **Sample**: 14 distinct phrasings (9 must-fire, 5 must-not-fire)
- **Total Sessions**: 70 sessions per arm (140 sessions total)

### Evaluation Arms

- **Arm B (Control)**: The baseline 439-character description without exclusion phrasing (head-14 sha256: `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`).
- **Arm A (Treatment)**: The candidate 551-character description with an explicit exclusion clause appended (head-14 sha256: `9049c7d82fadce008b00cdf70c7dc74add0d23691c7c61b8d586740a3beb3e1e`):

```
Write or check RFP and RFI responses, solution proposals, executive
summaries, and demo or discovery documents for technical presales and
bid teams. Use for a scored technical response, a customer-facing
proposal, or a check pass over a finished draft that flags invented
metrics, missing evidence, undisclosed customer references, competitor
comparisons, compliance claims, and unquantified buzzwords before the
document ships to a buyer. Not for slide decks or visual design,
pricing, sizing, or commercial modelling, or marketing and brand
writing.
```

---

## 3. Statistical Methodology

1. **Two-Tailed Fisher's Exact Test**: Evaluates the 2x2 contingency table comparing over-fire counts between Arm A and Arm B at significance level $\alpha = 0.05$.
2. **Clopper-Pearson 95% Exact Confidence Intervals**: Computed for any zero-event outcome to establish the statistical ceiling of the observed rate.
3. **Pre-Registered Precedence Hierarchy**:
   - **Priority 1 (Preserve Must-Fire Recall)**: Must-fire recall is paramount. If the treatment causes any statistically significant regression on must-fire phrasings, or drops any must-fire phrasing to 0 of 5 firings, the intervention is rejected.
   - **Priority 2 (Suppress Over-Fires)**: If must-fire recall is fully preserved and over-fires are reduced with $p < 0.05$, the treatment description is adopted.
   - **Priority 3 (Default Reversion)**: In the event of a tie, null effect, or ambiguous trade-off, the shorter baseline description is retained to avoid unnecessary prompt bloat.

---

## 4. Evaluation Disposition

As recorded in `evals/trigger/RESULTS-trigger.md`:
- **Over-fire suppression**: Arm A achieved 0 over-fires across 25 sessions compared to 9 over-fires in Arm B (Fisher exact test $p = 0.0016$), demonstrating that the negative exclusion clause effectively suppressed unwanted activations on near-miss tasks.
- **Must-fire recall regression**: However, Arm A suffered a complete recall failure on the phrasing *"We're putting together our bid response — write the commercial section"*, firing in 0 of 5 sessions (versus 5 of 5 in Arm B).
- **Decision**: In strict accordance with Priority 1, the candidate text was reverted to preserve 100% recall on core presales drafting. The original 439-character description was retained, and the measured over-fire residual is documented as a known limitation.
