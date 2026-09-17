---
phase: 04-distribution-worked-examples
verified: 2026-09-17T08:12:34Z
status: human_needed
score: "3/5 roadmap success criteria structurally verified (2 correctly route to human/behavioral verification by design)"
behavior_unverified: 0
overrides_applied: 0
human_verification:
  - test: "Run `npx skills add <real-owner>/<real-repo>` and `claude plugin marketplace add <real-owner>/<real-repo> && claude plugin install proof-first@proof-first` against the published repository once it exists."
    expected: "Both commands resolve and install the skill/plugin from this repository."
    why_human: "No git remote is configured (`git remote -v` prints nothing); the install commands currently name the disclosed `<owner>/<repo>` placeholder. A live install is a network-and-harness behavior no file-reading checker can observe. Tracked as WINDOWS.md entry 11 (open) and unresolved edges A4-E1/A4-E2, routed to Phase 6 LEG-04."
  - test: "Drive a live Claude Code session with `output-styles/proof-first.md` selected, and a second live session in a harness with `prompts/system-prompt.md` pasted as the system prompt. Compare both against a session with the skill folder installed on the same task."
    expected: "All three routes apply the same rule text, the same completeness audit, and the same artifact-family conventions, producing comparably disciplined output."
    why_human: "This is model behavior. The plan authors this exact claim as a `verification: backstop` truth (04-03-PLAN.md) specifically so no automated check ever marks it passed — this project publishes measured claims or none, and Phase 5's benchmark is the only place such a claim could ever be sourced from. Structural coverage (every rule/family heading reaches both derivatives) is mechanically proven; behavioral equivalence is not, by design."
  - test: "Have a person unfamiliar with this project read `examples/before-after.md`'s four after-columns and judge whether each genuinely demonstrates the rewrite its cited rule asks for, rather than restating the rule's own wording back to the reader."
    expected: "Each after column reads as an applied rewrite grounded in the deal brief, not a paraphrase of the rule text."
    why_human: "Authored in 04-02-PLAN.md as a `verification: backstop` truth. No file-reading checker in this stack performs this semantic judgment; only presence of a citation and presence of a ✗/✓ pair are mechanically enforced."
  - test: "Have a first-time reader open README.md cold and report whether the lead-in genuinely reads as leading with a real example, and whether the Install section is clear enough to act on without cross-referencing other files."
    expected: "A prospective evaluator understands what the skill does and how to install it within the first screen or two, with no confusion about which of the four routes to pick."
    why_human: "DIST-06's prose-quality half — WINDOWS.md entry 12 (open). Only the structural half (four anchors present, Before-and-after precedes Install and Status) is CI-enforced by `readme-install-path-missing`/`readme-before-after-order`; clarity and reading experience are not."
---

# Phase 4: Distribution & Worked Examples Verification Report

**Phase Goal:** The finished rule catalog reaches a writer through every distribution channel the project promises, backed by real worked examples.
**Verified:** 2026-09-17T08:12:34Z
**Status:** human_needed
**Re-verification:** No — initial verification

## Project Gate (run independently by this verifier)

```
python3 tools/check_repo.py --self-test      -> self-test PASS - 40 verified violation codes listed
python3 tools/check_repo.py --mutation-test  -> mutation-test PASS: 41 codes discrimination-proven
                                                  CONTROL: 0 violations on the unmutated copy (0 known-open, 0 unexpected)
                                                  0 lines containing "FIRE-ONLY"
python3 tools/check_repo.py                  -> check_repo: 0 violations
python3 tools/generate_derivatives.py --check -> exit 0
```

All four gate commands were re-run directly by this verifier (not taken from SUMMARY.md) immediately
before writing this report. Numbers observed match every SUMMARY's claim: 41 discrimination-proven,
up from 32 at Phase 3's close, CONTROL clean, no FIRE-ONLY.

## Goal Achievement

### Observable Truths (roadmap Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Reader sees before/after pairs covering each of the four artifact families, after column citing real, shipped rule numbers | ✓ VERIFIED (structural) | `examples/before-after.md` has exactly the four frozen family headings in frozen order, 4 `✗` lines, 4 `✓` lines; every cited `PF-`/`MC-` token (`PF-2.1, MC-11, PF-1.9, PF-2.14, PF-2.17, PF-0.1, PF-1.25, PF-2.11, PF-3.3, MC-31`) is in NUMBERING.md's Allocated IDs table (`a-n` set difference is empty, independently computed). Content-quality (does the rewrite genuinely apply the rule rather than restate it) is an explicit `verification: backstop` truth in 04-02-PLAN.md — routed to human verification below, not silently passed. |
| 2 | User can install via the skills CLI with one command, and separately as a Claude Code plugin from a marketplace manifest in this repo | ⚠️ Structural only — routes to human | Both manifests exist, parse, agree on version (`0.1.0`/`0.1.0`/`0.1.0`), agree on name/source (`proof-first proof-first ./`), and `publish-location-drift` proves every carrier (both manifests + README) states the identical `https://github.com/<owner>/<repo>` placeholder. **No live install has been exercised anywhere in this environment** — no git remote is configured (`git remote -v` prints nothing), so `npx skills add` and `claude plugin marketplace add` cannot resolve. This is a genuine capability claim ("can install") no file-reading checker can prove; correctly disclosed as WINDOWS.md entry 11 (open) and unresolved edges A4-E1/A4-E2 across all four SUMMARYs. |
| 3 | User can turn the discipline on permanently as an output style, or paste a system-prompt version, and get equivalent behavior either way | ⚠️ Structural only — routes to human, by design | `output-styles/proof-first.md` and `prompts/system-prompt.md` both exist, are generator output (not hand-written), reproduce byte-for-byte on re-run, carry the identical sha256 stamp over the same 5 sources, and contain all 39 allocated rule headings plus all 4 family headings (independently re-derived from NUMBERING.md's `## Allocated IDs` section only, matching `parse_numbering`'s scoping — 0 missing in either file). **The "equivalent behavior" clause is deliberately unverified**: no benchmark has run, the plan authors this exact sentence as a `verification: backstop` truth, and neither derivative nor README asserts sameness anywhere (scanned for 8 sameness phrasings across 4 files — 0 hits). This is the correct disposition per this project's "measured claims or no claims" discipline, not a gap this phase failed to close. |
| 4 | A documented re-sync step exists that regenerates the output style and system prompt whenever SKILL.md changes | ✓ VERIFIED | `tools/generate_derivatives.py` exists (imports only `argparse`,`hashlib`,`pathlib`,`re`,`sys` — verified by AST scan), `--check` mode runs and exits 0 against the committed files, `skill-derivative-stale` is discrimination-proven in the mutation test, CI runs `python3 tools/generate_derivatives.py --check` as the fifth command in the one existing job (confirmed in `.github/workflows/ci.yml`), and README's `## Keeping derivatives in sync` section names the command and the two enforcing checks. |
| 5 | Reader opens a README that leads with before/after pairs and states an install path for every supported harness | ✓ VERIFIED (structural) | Heading order independently re-derived: `['What this is', 'Before and after', 'Install', 'Keeping derivatives in sync', 'Status', 'Repository layout', 'Rule numbering', 'Versioning', 'License and notices']` — Before-and-after precedes both Install and Status, mechanically enforced by `readme-before-after-order`. All four install anchors present (`npx skills add`, `claude plugin marketplace add` + `claude plugin install proof-first@proof-first`, `output-styles/proof-first.md`, `prompts/system-prompt.md`), enforced by `readme-install-path-missing`. The existing measured-figure disclosure (`evals/conformance/RESULTS-mod04.md`, 2 occurrences — see Anti-Patterns note below) and the single attribution pointer both survive untouched. Prose-quality (does it *read* as leading with examples to a first-time reader) is WINDOWS.md entry 12 (open) — routed to human verification below. |

**Score:** 3/5 truths structurally VERIFIED outright (#1, #4, #5); 2/5 (#2, #3) have their mechanical/structural half fully verified but their behavioral half is *correctly* left unverified by explicit project design (measured-claims-or-none discipline) rather than by an oversight. Nothing in this phase is FAILED.

## Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `.claude-plugin/plugin.json` | Plugin manifest DIST-02 install resolves | ✓ VERIFIED | Exists, parses, `name=proof-first` equals skill folder, all required keys present |
| `.claude-plugin/marketplace.json` | Marketplace manifest, one entry rooted at repo root | ✓ VERIFIED | Exists, parses, `source: "./"`, entry restates plugin.json's fields exactly |
| `tools/check_repo.py` (plugin checks) | 3 codes with 3-part contract | ✓ VERIFIED | `plugin-manifest-invalid`, `plugin-manifest-version-mismatch`, `publish-location-drift` all discrimination-proven |
| `examples/before-after.md` | 4 document-level pairs, real citations | ✓ VERIFIED | 4/4 families, 4 `✗`/4 `✓` lines, all citations allocated, `</content>` stray tag (CR-01) confirmed removed |
| `tools/check_repo.py` (example checks) | 2 codes | ✓ VERIFIED | `before-after-family-missing`, `before-after-citation-missing` discrimination-proven |
| `tools/generate_derivatives.py` | stdlib-only generator with `--check` | ✓ VERIFIED | `def check_derivatives` present, imports only 5 named stdlib modules, `--check` exits 0 |
| `output-styles/proof-first.md` | DIST-03 derivative | ✓ VERIFIED | Generated, hash-stamped, YAML frontmatter at line 1, all 39 rule + 4 family headings present |
| `prompts/system-prompt.md` | DIST-04 derivative | ✓ VERIFIED | Generated, hash-stamped, stamp at line 1, identical digest to output style, all headings present |
| `tools/check_repo.py` (derivative checks) | 2 codes | ✓ VERIFIED | `skill-derivative-stale`, `derivative-rule-coverage-incomplete` discrimination-proven |
| `.github/workflows/ci.yml` | generator `--check` wired into the one job | ✓ VERIFIED | 1 named step, 5-command run block, no `|| true` |
| `README.md` | Before/after lead-in, 4 install routes, re-sync step | ✓ VERIFIED | `## Install` present; heading order and anchor presence both mechanically enforced |
| `tools/check_repo.py` (README checks) | 2 codes | ✓ VERIFIED | `readme-install-path-missing`, `readme-before-after-order` discrimination-proven |

**Independent artifact/key-link check** via `gsd_run query verify.artifacts`/`verify.key-links` against all four PLAN frontmatters: **16/16 artifacts passed, 16/16 key links verified**, across all four plans.

### Key Link Verification

| From | To | Via | Status |
|------|----|----|--------|
| `.claude-plugin/plugin.json` | `skills/proof-first/SKILL.md` | version equality | ✓ WIRED |
| `.claude-plugin/marketplace.json` | `.claude-plugin/plugin.json` | restated fields | ✓ WIRED |
| `tools/check_repo.py` | `.claude-plugin/plugin.json` | `_load_json_manifest` | ✓ WIRED |
| `.claude-plugin/marketplace.json` | `skills/proof-first/` | `source: "./"` auto-discovery | ✓ WIRED |
| `examples/before-after.md` | `tools/check_repo.py` | `ARTIFACT_FAMILY_SECTIONS` reuse | ✓ WIRED |
| `examples/before-after.md` | `NUMBERING.md` | rule token allocation | ✓ WIRED |
| `examples/before-after.md` | `examples/deal-brief.md` | figure traceability | ✓ WIRED |
| `examples/before-after.md` | `references/artifact-patterns.md` | Order line demonstrated | ✓ WIRED |
| `output-styles/proof-first.md` | `skills/proof-first/SKILL.md` | sha256 stamp | ✓ WIRED |
| `prompts/system-prompt.md` | `references/completeness-audit.md` | MC headings carried | ✓ WIRED |
| `tools/generate_derivatives.py` | `tools/check_repo.py` | shared `DERIVATIVE_SOURCE_NAMES` | ✓ WIRED |
| `.github/workflows/ci.yml` | `tools/generate_derivatives.py` | `--check` invocation | ✓ WIRED |
| `README.md` | `examples/before-after.md` | reproduced pair | ✓ WIRED |
| `README.md` | `.claude-plugin/marketplace.json` | identical publish location | ✓ WIRED |
| `README.md` | `tools/generate_derivatives.py` | re-sync command named | ✓ WIRED |
| `README.md` | `evals/conformance/RESULTS-mod04.md` | guarded results pointer | ✓ WIRED |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Manifests agree on name/version/source | `python3 -c "import json; ..."` | `proof-first proof-first ./ 0.1.0 0.1.0` | ✓ PASS |
| Derivatives are a pure function of sources | `generate_derivatives.py && generate_derivatives.py --check` | exit 0, byte-identical | ✓ PASS |
| All 39 rule headings + 4 family headings reach both derivatives | independent regex scoped to `## Allocated IDs` | `[]` missing for both files | ✓ PASS |
| No sameness-of-outcome phrasing anywhere | 8-phrase scan × 4 files | `[]` for every file | ✓ PASS |
| Full CI command sequence | self-test + mutation-test + live + conformance self-test + generator check | all exit 0 | ✓ PASS |
| Stray `</content>` tag (CR-01) is gone | `grep -n '</content>' examples/before-after.md` | no match (exit 1) | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|--------------|--------|----------|
| EX-02 | 04-02 | Before/after pairs per family, real rule citations | Structural: SATISFIED. Content-quality: NEEDS HUMAN | `examples/before-after.md`, `before-after-family-missing`/`before-after-citation-missing` |
| DIST-01 | 04-01 (mechanism), 04-04 (command) | Install via skills CLI, one command | Structural: SATISFIED. Live flow: NEEDS HUMAN | README install anchor + `publish-location-drift`; no live install exercised (WINDOWS #11) |
| DIST-02 | 04-01 | Install as Claude Code plugin from marketplace manifest | Structural: SATISFIED. Live flow: NEEDS HUMAN | Both manifests, `plugin-manifest-invalid`/`plugin-manifest-version-mismatch`; no live install exercised |
| DIST-03 | 04-03 | Turn discipline on as output style | Structural: SATISFIED. Behavioral: NEEDS HUMAN (by design) | `output-styles/proof-first.md`, `derivative-rule-coverage-incomplete` |
| DIST-04 | 04-03 | Paste system prompt, harness with no skill support | Structural: SATISFIED. Behavioral: NEEDS HUMAN (by design) | `prompts/system-prompt.md`, same coverage code |
| DIST-05 | 04-03 (mechanism), 04-04 (README restatement) | Derivatives regenerated from SKILL.md, documented re-sync | SATISFIED | `generate_derivatives.py --check`, `skill-derivative-stale`, CI wiring, README section |
| DIST-06 | 04-04 | README leads with before/after, states install paths per harness | Structural: SATISFIED. Prose-quality: NEEDS HUMAN | `readme-before-after-order`/`readme-install-path-missing` |

No orphaned requirements: REQUIREMENTS.md's Phase 4 traceability row set (`EX-02, DIST-01..06`) exactly matches the union of `requirements:` fields declared across all four PLAN frontmatters.

**Finding — REQUIREMENTS.md checkbox caveat gap (WARNING, not a blocker).** This is the fourth
recurrence of a pattern this project's own memory log already tracks: `git log -p` on
`.planning/REQUIREMENTS.md` shows commit `32e24bf` flipped `EX-02`, `DIST-01`, `DIST-02`, and
`DIST-06` to `[x]` with **no caveat annotation**, even though every one of them has an explicitly
unverified live-behavior or content-quality half stated in its own SUMMARY (confirmed above). Other
requirements this project marked `[x]` with a genuinely unverified residual — `CAT-10`, `AUD-01`,
`ART-01`–`ART-04` — all carry an italic caveat sentence after the checkbox explaining exactly what
remains unverified and naming the closure condition. `EX-02`/`DIST-01`/`DIST-02`/`DIST-06` do not.
A reader skimming REQUIREMENTS.md's checkboxes alone (rather than the per-phase SUMMARYs) would
reasonably conclude these four are fully verified, when in fact each has a disclosed open item
(WINDOWS.md entries 11 and 12) or an explicit `verification: backstop` truth still pending Phase 5/6.
**Recommendation:** append the same italic caveat convention to these four checkboxes, naming
WINDOWS.md entries 11/12 and the backstop truths in 04-02/04-03-PLAN.md as the closure conditions —
matching the existing project convention rather than leaving the discipline inconsistently applied.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `examples/before-after.md` | (formerly line 37) | Stray `</content>` tool-output tag (CR-01) | Was Critical | **Fixed and confirmed absent** — commit `8c30dfd` present in `git log`, `grep` finds no match. No action needed. |
| `tools/check_repo.py:2268-2278` (`_owner_segment`) | — | `publish-location-drift` only strips an `https://github.com/` prefix; an SSH (`git@github.com:owner/repo.git`) or scheme-less carrier value would false-positive as disagreeing (WR-01) | Warning | **Dormant today** — every existing carrier uses the identical `https://github.com/<owner>/<repo>` placeholder form, so this does not currently fire and does not undermine any of this phase's must-haves. Real latent defect, correctly logged as an open review finding (04-REVIEW.md), not silently dropped. Does not block phase goal. |
| `tools/generate_derivatives.py:33-37,226-264` | — | Docstring promises byte-for-byte comparison; `check_derivatives`/`write_derivatives` actually use `read_text`/`write_text` with universal-newline translation and no pinned `newline='\n'` (WR-02) | Warning | **Dormant today** — this repository and its CI both run on Linux with LF line endings, so the current guarantee holds in practice; the gap is between the docstring's claim and a cross-platform edge case. Does not affect the verified truth that `--check` currently passes and CI currently enforces it. |
| `tools/check_repo.py:2144-2226` | — | Plugin manifest checks silently assume exactly one `skills/*/SKILL.md`; a 0-or-2+-skill repo would skip the name-equality check with no violation raised (WR-03) | Warning | **Dormant today** — repository ships exactly one skill folder. Correctly logged as an open review finding, not blocking. |

None of the three open WARNING items (WR-01/02/03) is a debt marker (`TBD`/`FIXME`/`XXX`) — a
repository-wide scan of every file this phase modified found zero such markers and zero
`TODO`/`HACK`/`PLACEHOLDER` occurrences. They are disclosed, dormant, non-blocking code-review
findings tracked in `04-REVIEW.md`, appropriately left as follow-up rather than in-phase scope
creep.

## Human Verification Required

See the `human_verification` list in this file's frontmatter — 4 items: the live skills-CLI/plugin
install once a real repository location exists, the behavioral equivalence claim across the three
distribution routes (explicitly deferred to Phase 5's benchmark by this project's own evidence
discipline), the content-quality judgment on `examples/before-after.md`'s four after-columns, and
README's prose-quality/first-reader-clarity judgment.

## Gaps Summary

**No gaps block this phase's goal.** Every roadmap Success Criterion has its structural/mechanical
half fully built, wired, and CI-enforced — verified independently by this verifier re-running all
four project-gate commands plus 16 artifact checks and 16 key-link checks, all passing. The
`mutation-test` discrimination-proven total is genuinely 41 (up from 32 at Phase 3's close), CONTROL
is genuinely clean, and no code is FIRE-ONLY.

What remains open is exactly what the phase's own plans, SUMMARYs, and threat models disclosed in
advance as out of this phase's reach: (1) a live install cannot be exercised without a published
`owner/repo`, which does not exist yet (no git remote configured); (2) whether the output style or
system prompt produces equivalent live-session behavior to the installed skill is a claim this
project's "measured claims or no claims" discipline forbids asserting before Phase 5's benchmark
runs; (3) two content-quality judgments (worked-example rewrite quality, README prose clarity) that
no file-reading checker in this stack performs, matching `workflow.human_verify_mode: end-of-phase`.
None of these is a phase failure — they are correctly-disclosed ceilings, not oversights, and this
report is what should route them into end-of-phase UAT rather than let them pass silently.

The one documentation finding worth a maintainer's attention before shipping (not blocking): four
REQUIREMENTS.md checkboxes (`EX-02`, `DIST-01`, `DIST-02`, `DIST-06`) were marked `[x]` without the
same caveat-annotation convention this project uses everywhere else for a requirement with a
disclosed unverified residual.

---

*Verified: 2026-09-17T08:12:34Z*
*Verifier: Claude (gsd-verifier)*
