# Write-Mode Artifact Conformance Evaluation (MOD-04)

## Executive Summary

Proof First defines a structured output contract for presales writing in Write Mode:
1. **Artifact Family Declaration**: The generation must open with an explicit artifact family declaration within the first 400 characters (e.g., `**Artifact family:** RFP and RFI response` or `**Artifact family:** No family fits`).
2. **Drafted Response**: The substantive presales prose adhering to the Command of the Message proof-point disciplines.
3. **Verification**: Completeness checklist citations and rule references (`PF-*` and `MC-*`).

This evaluation benchmarks whether Claude Code sessions in Write Mode reliably emit the artifact family declaration in the header before rule citations, or whether rule citations precede the family name, or the family declaration is omitted.

Under an anchored scorer bounding the family declaration search to the opening 400 characters (`FAMILY_LINE_WINDOW_CHARS = 400`), live evaluation on `claude-sonnet-5` measured a **30.0% conformance rate** (3 of 10 scoreable sessions). Every non-conformant session in this measurement omitted the family declaration in the header (`no-family`), while zero sessions emitted rule markers before the family line (`rule-before-family: 0`).

---

## Benchmark Results

### Anchored Measurement Summary (2026-09-16)

Evaluated across five distinct presales fixtures with `claude-sonnet-5` using `evals/conformance/run_conformance.py`:

| Evaluation Arm | Model | Description | Scoreable Sessions | Conformant Sessions | Conformance Rate |
|---|---|---|---|---|---|
| **Arm A (Current Skill)** | `claude-sonnet-5` | Live skill with self-check ordering gate | 10 | 3 | **30.0%** |
| **Arm B (Baseline Skill)** | `claude-sonnet-5` | Baseline skill prior to ordering gate | 10 | 4 | **40.0%** |

#### Detailed Verdict Breakdown — Arm A (Current Skill)

- conformant: 3 (B-proposal-section retry, D-demo-discovery first attempt, E-ambiguous first attempt)
- no-family: 7 (A-rfp-answer x2, B-proposal-section first attempt, C-exec-summary x2, D-demo-discovery second attempt, E-ambiguous second attempt)
- rule-before-family: 0
- unscoreable: 2 (A-rfp-answer first attempt, B-proposal-section second attempt)

**Result: 3 conformant of 10 scoreable sessions (30.0%).**

#### Detailed Verdict Breakdown — Arm B (Baseline Skill)

- conformant: 4 (A-rfp-answer retry, C-exec-summary x2, E-ambiguous first attempt)
- no-family: 6 (A-rfp-answer first attempt, B-proposal-section x2, D-demo-discovery x2, E-ambiguous second attempt)
- rule-before-family: 0
- unscoreable: 1 (A-rfp-answer second attempt)

**Result: 4 conformant of 10 scoreable sessions (40.0%).**

---

### Comparison with Unanchored Exploratory Runs

Earlier exploratory runs without prefix window anchoring scored higher:
- **Arm 1 (Unanchored exploratory):** 16 of 20 scoreable sessions conformant (80.0%) across `claude-opus-5` (10/10) and `claude-sonnet-5` (6/10 = 60.0%).
- **Arm 2 (Unanchored baseline):** 5 of 11 scoreable sessions conformant (45.5%) on `claude-sonnet-5`.

However, investigation revealed that unanchored whole-transcript searches introduce an optimistic bias: presales documents frequently reuse words like "executive summary" or "solution proposal" in section headings later in the body. The anchored scorer eliminates this false-positive rate by restricting the search to the opening 400 characters, confirming that true header conformance is approximately 30.0% to 40.0% on `claude-sonnet-5`.

---

## Findings & v1 Disposition Decision

### Key Findings

1. **Ordering gates do not overcome model stochasticity**: Adding a self-check ordering gate to the skill instructions produced a 30.0% conformance rate versus 40.0% in the baseline. At n=10 per arm, this delta is consistent with sampling noise and demonstrates that prompt-level instructions cannot reliably force deterministic generation ordering in 100% of cases.
2. **Residual failure shape**: Every non-conformant session in the anchored measurement scored `no-family` (the model dove directly into drafting or cited rules without declaring the family up front). Zero sessions scored `rule-before-family`.

### Disposition Decision

For v1, the project adopts an **accept-and-disclose** posture:
- The measured ~30% write-mode conformance rate is accepted and prominently disclosed in `README.md` under Known Limitations.
- **Architectural Trade-off**: The alternative of enforcing 100% ordering via runtime interceptors (e.g., a custom CLI wrapper or post-generation regex filter) was rejected because it would violate Proof First's core architectural commitments: zero dependencies, pure Markdown implementation, and portable operation across any Agent Skills-compliant harness (including web interfaces and system prompt pasting).

---

## Methodology & Scorer Anchoring

The evaluation uses `evals/conformance/run_conformance.py` to drive live Claude Code sessions:

1. **Anchoring Window**: `FAMILY_LINE_WINDOW_CHARS = 400`. The family declaration must appear within the first 400 characters of the generation.
2. **Five Presales Scenarios**:
   - `A-rfp-answer`: Highly structured question-and-answer format.
   - `B-proposal-section`: Section-level narrative proposal drafting.
   - `C-exec-summary`: Concise executive-level summary for stakeholder review.
   - `D-demo-discovery`: Discovery notes translated into demonstration flow.
   - `E-ambiguous`: Borderline prompt testing fallback to `No family fits`.
3. **Execution Mode**: Sessions run in live headless mode (`claude -p`) in isolated temporary environments.

### Caveats

- **Model Specificity**: Live evaluations were measured on `claude-sonnet-5` and `claude-opus-5`.
- **Sample Size**: The anchored measurement covers 23 total sessions (20 planned plus 3 retry sessions following harness timeouts).
- **Non-determinism**: Claude Code does not expose temperature or seed parameters; individual run repeats may vary within typical sampling bounds.

---

## Raw Session Records (Anchored Scorer)

The 23 session logs recorded under the anchored scorer (`FAMILY_LINE_WINDOW_CHARS = 400`) are preserved below for empirical audit:

## Run recorded 2026-09-16T06:23:26.865109+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=unscoreable | reason=timeout

conformant 0 of 0 scoreable sessions
unscoreable 1 sessions
  - excluded: model=claude-sonnet-5 fixture=A-rfp-answer repeat=0 reason=timeout

## Run recorded 2026-09-16T06:31:45.559491+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=73, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T06:37:20.821712+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=636, marker='PF-1.2')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T06:42:11.983431+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=1013, marker='PF-2.13')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T06:48:34.377750+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=unscoreable | reason=timeout

conformant 0 of 0 scoreable sessions
unscoreable 1 sessions
  - excluded: model=claude-sonnet-5 fixture=B-proposal-section repeat=0 reason=timeout

## Run recorded 2026-09-16T06:56:50.135039+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=conformant | evidence=family 'Solution proposal' at offset 2 (window=400), marker_at=1604

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:02:46.131767+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=546, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:07:53.175382+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=612, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:14:12.088281+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=conformant | evidence=family 'Demo or discovery material' at offset 2 (window=400), marker_at=841

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:21:00.546743+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=1176, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:27:19.044526+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=conformant | evidence=family 'No family fits' at offset 2 (window=400), marker_at=1336

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:33:46.055691+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=312, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:40:29.839977+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=594, marker='PF-1.2')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:45:44.241555+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=unscoreable | reason=timeout

conformant 0 of 0 scoreable sessions
unscoreable 1 sessions
  - excluded: model=claude-sonnet-5 fixture=A-rfp-answer repeat=0 reason=timeout

## Run recorded 2026-09-16T07:53:55.751856+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=conformant | evidence=family 'RFP and RFI response' at offset 2 (window=400), marker_at=614

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:58:45.274766+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=1028, marker='PF-2.13')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:03:22.501771+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=876, marker='PF-2.13')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:08:55.790418+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=conformant | evidence=family 'Executive summary' at offset 2 (window=400), marker_at=576

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:13:31.662960+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=conformant | evidence=family 'Executive summary' at offset 2 (window=400), marker_at=565

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:17:21.490987+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=874, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:22:45.863745+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=898, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:28:18.574834+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=conformant | evidence=family 'No family fits' at offset 2 (window=400), marker_at=1215

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:33:31.569939+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=282, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions
