---
phase: "01"
slug: "foundations-legal-scaffolding-numbering-shared-deal"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
block_on: high
created: "2026-09-10"
---

# Phase 01 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Reconstructed from artifacts (State B — no SECURITY.md existed; 7 PLANs, all carrying a
> `<threat_model>` block, so `register_authored_at_plan_time: true`).

---

## Register namespace note (read this before using a threat ID)

**Threat IDs collide across this phase's plans.** Plans 01-01 through 01-04 opened one ID
namespace for content and legal-exposure threats; the gap-closure plans 01-05 through 01-07
independently opened a second namespace for tooling threats, reusing `T-01-01` … `T-01-10` with
entirely different meanings. `T-01-01` denotes "framework-derived wording reaching a public
repository" in plan 01-01 and "carrier path traversal in `check_pointer()`" in plan 01-05.

Nothing is unmitigated because of this, but a bare ID is ambiguous. Every row below is therefore
qualified as **A** (content/legal, plans 01-01…01-04) or **B** (tooling, plans 01-05…01-07).
A future phase reusing this register should renumber rather than extend either namespace.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| Framework source material → repository content | Proprietary wording could cross into a public MIT repo through too-close paraphrase or model reproduction of training-portal text | Framework-derived prose |
| Fictional example data → public repository | Invented company/person/deal facts could match a real entity once published | Invented names, figures |
| Canonical registry → every downstream file | A dropped attribution pointer or drifted canonical figure propagates into every citing artifact | Pointer string, canonical figures |
| Repository → forks, scrapers, search indexes | Marks in paths and headings propagate more widely than body prose | Filenames, headings |
| Repository Markdown → `tools/check_repo.py` | **The only untrusted input crossing into executable code.** CI triggers on `pull_request`, so a fork supplies the `NOTICES.md`, `README.md`, and `examples/**/*.md` this script parses inside the runner | Attacker-controlled Markdown |
| `tools/check_repo.py` → CI exit status | The exit code is the entire enforcement surface; a false zero is the failure this phase's BLOCKER was | Exit code |
| `tools/check_repo.py` → developer filesystem | The mutation harness copies and writes files, so a path or copy-scope mistake could touch the working tree | Scratch-tree writes |

There is no runtime, no network surface, no authentication, no session, no data store, and no
deserialization of untrusted formats in this phase. The ASVS L1 controls for session management,
access control, cryptography, and output encoding have no counterpart here and are deliberately
not padded into the register.

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| **A**/T-01-01 | Tampering / Info Disclosure | Framework-derived wording in any shipped file | high | mitigate | `SOURCES.md` fixes the approved-source list and reproduction boundary; semantic judgement owned by Phase 6 LEG-04. **Verified:** `SOURCES.md` carries "What counts as reproduction", an approved-source table per framework, and an "Out of bounds" section | closed |
| **A**/T-01-02 | Spoofing / Repudiation | The three `NOTICES.md` framework statements | high | mitigate | Three separately named statements with fixed element order; MEDDIC family records contested ownership rather than naming a holder. **Verified:** all three headings present, and now *mechanically enforced* by the `framework-statement-missing` check added this session | closed |
| **A**/T-01-11 | Spoofing | Unmeasured claims or badges in `README.md` | high | mitigate | Badges, images, percentages, result-shaped figures forbidden. **Verified:** 0 image/badge markers, 0 percentages in `README.md` | closed |
| **B**/T-01-SC | Tampering | Package-manager installs (supply chain) | high | mitigate | Not applicable by construction *and enforced*. **Verified:** AST import scan reports `{argparse, pathlib, re, shutil, sys, tempfile}` — all stdlib; `grep -c 'pip install' .github/workflows/ci.yml` = 0 | closed |
| **A**/T-01-03 | Repudiation | `LICENSE` ↔ `NOTICES.md` boundary | medium | mitigate | Unmodified MIT `LICENSE` plus precedence / no-trademark-grant / coverage-default sentences. **Verified:** `LICENSE` present, MIT; now enforced by the `license-missing` check added this session | closed |
| **A**/T-01-04 | Info Disclosure | Invented party and person names | medium | mitigate | Fictional-parties disclaimer plus a reviewer name-collision search over all 9 names. **Verified:** `01-UAT.md` test 1 passed 2026-09-10 | closed |
| **A**/T-01-05 | Tampering | Attribution pointer across carrier files | medium | mitigate | One canonical string in a fenced block, N pointers, `pointer-missing` / `pointer-duplicated` in CI. **Verified:** both codes proven live by `--mutation-test` against the real `README.md` | closed |
| **A**/T-01-06 | Tampering | Canonical figures drifting between examples | medium | mitigate | `dup-figure-key`, `figure-order`, `unlisted-figure`, with the bare-count ceiling declared in the module docstring. **Verified:** all three proven live by `--mutation-test` | closed |
| **A**/T-01-07 | Repudiation | The shared deal as benchmark substrate | medium | mitigate | `## Inconvenient facts` deliberately puts four vendor-unfavorable facts in the brief so Phase 5 is not drawn from a favorable proving ground. **Verified:** section present in `examples/deal-brief.md` | closed |
| **A**/T-01-08 | Tampering | Real product names used comparatively | medium | mitigate | Platform-naming boundary stated in the Parties section; independent reviewer confirms no sentence sets two real products or companies against each other. **Verified:** `01-UAT.md` test 2 passed 2026-09-10 | closed |
| **A**/T-01-09 | Spoofing | A fabricated citation in `SOURCES.md` | medium | mitigate | Unchecked URLs forbidden; any unconfirmed row must carry `unverified` + `to confirm at LEG-04`. **Verified:** all 6 source rows carry both markers and no URL | closed |
| **A**/T-01-10 | Elevation of Privilege | Framing this project as a *version of* a named framework | medium | mitigate | Version / implementation / edition / automation framing forbidden — this framing is what removes the nominative-fair-use defence. **Verified:** no such framing in shipped content | closed |
| **A**/T-01-12 | Info Disclosure | Framework marks in filenames, directories, headings | medium | mitigate | Sweep of every path and heading outside `NOTICES.md` (the single documented carve-out per D-11). **Verified:** 0 marks in any shipped path or heading. *Residual — see Observations* | closed |
| **B**/T-01-01 | Tampering | `check_pointer()` carrier path join `repo_root / carrier` | medium | mitigate | `_carrier_is_repo_relative()` rejects absolute, drive-letter, and `..`-bearing entries before opening. **Independently reproduced this session:** injecting `/etc/passwd`, `../../../../etc/hosts`, and `C:\Windows\win.ini` into the carriers list yields three `pointer-unparseable` violations, exit 1, and no file outside the repo is opened | closed |
| **B**/T-01-06 | Tampering | `check_unlisted_figure()` exempt-region state machine | medium | mitigate | Exempt region bounded by table shape, not by a following heading — otherwise appending content after `## Canonical figures` suppresses scanning for the rest of the file, a submitter-controllable way to disable the check. **Verified:** proven live by the `unlisted-figure` mutation, which appends a stray figure after the table at end-of-file | closed |
| **B**/T-01-08 | Tampering | `_copy_repo_subset()` and the `_mutate_*` writers | medium | mitigate | All writes under a `tempfile.TemporaryDirectory`; `MUTATION_SOURCES` is an explicit allowlist, so `.git` and `.planning` are never copied or written. **Independently reproduced this session:** `git status --porcelain` byte-identical before and after a full `--mutation-test` run | closed |
| **A**/T-01-13 | Repudiation | Empty placeholder file for a documented-but-unbuilt path | low | mitigate | D-15's documented-not-pre-created rule; build fails on any zero-byte file outside `.git`. **Verified:** 0 zero-byte files | closed |
| **B**/T-01-03 | Denial of Service | Whole-document lazy-quantifier regex over attacker-influenceable Markdown | low | mitigate | Replaced with the line-scanning `split_sections()` helper; fence search bounded to one section body | closed |
| **B**/T-01-07 | Tampering | `check_range_id()` MC aggregate range | low | mitigate | Validates membership in each *declared* block, not one aggregate (min,max) that a registry edit can widen. **Verified:** proven live by the `range-id` mutation | closed |
| **B**/T-01-02 | Denial of Service | `Path.read_text()` on every example and carrier | low | accept | See Accepted Risks R-01 | closed |
| **B**/T-01-04 | Info Disclosure | Violation messages printed to CI logs | low | accept | See Accepted Risks R-02 | closed |
| **B**/T-01-05 | Denial of Service | `CURRENCY_RE`, `PERCENT_RE`, `ISO_DATE_RE` per line | low | accept | See Accepted Risks R-03 | closed |
| **B**/T-01-09 | Denial of Service | Repository subset copied once per mutation | low | accept | See Accepted Risks R-04 | closed |
| **B**/T-01-10 | Elevation of Privilege | The third CI run-block command | low | accept | See Accepted Risks R-05 | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `high` count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

**24 unique threats · 19 mitigated · 5 accepted · 0 open.**

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| R-01 | **B**/T-01-02 | Files are repository-committed Markdown read once each into an ephemeral CI runner. A size cap would add a failure mode with no attacker benefit — a fork can already make the runner do more work by committing more files. | 01-05-PLAN.md threat model | 2026-09-10 |
| R-02 | **B**/T-01-04 | Messages print only a carrier path, an ID token, or a figure token — all values the submitter already controls. With **B**/T-01-01 mitigated, no content from outside the repository can reach a message. | 01-05-PLAN.md threat model | 2026-09-10 |
| R-03 | **B**/T-01-05 | All three patterns are linear, with no nested quantifier and no alternation over a repeated group, so no catastrophic backtracking path exists; they run per line rather than over a whole document. Reviewed and accepted rather than rewritten. | 01-06-PLAN.md threat model | 2026-09-10 |
| R-04 | **B**/T-01-09 | Twelve copies of a few small Markdown files and one script per run. A shared copy would be faster but would let one mutation's violations mask another's absence — a worse trade than a second of CI time. | 01-07-PLAN.md threat model | 2026-09-10 |
| R-05 | **B**/T-01-10 | The command runs the same script the job already runs twice, with no new permission, no new action, no network access, and no secret. The `pull_request` trigger's default token is read-only for forks. | 01-07-PLAN.md threat model | 2026-09-10 |

---

## Observations (non-blocking, recorded rather than closed silently)

1. **`.planning/` is git-tracked and carries framework marks in headings.** The **A**/T-01-12
   sweep covered the eight files the phase produced and found zero marks in any shipped path or
   heading. It did not cover `.planning/`, which is GSD working material — but that directory
   *is* tracked by git, and `.planning/research/FEATURES.md`, `SUMMARY.md`, `ARCHITECTURE.md`,
   and `PITFALLS.md` carry `### …MEDDICC…`, `### …Challenger…`, and
   `### Command of the Message…` headings. If the repository is published as-is, those headings
   ship. This does not change the phase verdict (T-01-12 is medium; the block threshold is
   `high`), but it is a decision that has not been made yet and belongs in the LEG-04
   pre-publication gate: either exclude `.planning/` from the public repo or extend the sweep
   to it.

2. **Threat-ID namespace collision** — see the note at the top of this file. Two disjoint
   meanings share `T-01-01` … `T-01-10`. No threat is unmitigated as a result, but any future
   reference to a bare `T-01-0x` in this phase is ambiguous.

3. **`pointer-*` checks still cannot fire when `NOTICES.md` is absent.** `run_notices_checks()`
   returns empty for a missing file. The equivalent hole in the LEG-02 check was closed this
   session (see `01-VALIDATION.md`); the pointer family's was deliberately left alone as
   out-of-scope for the two validation gaps under audit. Worth a future ticket — it is the same
   "check that cannot fire" class this phase exists to prevent.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-10 | 24 | 24 | 0 | `/gsd-secure-phase 01` (orchestrator, ASVS L1 short-circuit — `threats_open: 0`, register authored at plan time, `asvs_level == 1`) |

Verification depth: ASVS L1 grep-depth as specified, plus independent runtime reproduction of the
two genuinely security-bearing controls (**B**/T-01-01 carrier path traversal and **B**/T-01-08
working-tree isolation) rather than grep alone.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-09-10
