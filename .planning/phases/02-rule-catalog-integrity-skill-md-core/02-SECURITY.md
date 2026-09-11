---
phase: "2"
slug: "rule-catalog-integrity-skill-md-core"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on (high)
threats_open: 0
asvs_level: 1
created: "2026-09-11"
---

# Phase 2 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

**43 threats across two ID namespaces.** Plans 02-01…02-06 number their threats
`T-2-NN` (21 threats). Plans 02-07, 02-08 and 02-09 number theirs `T-02-NN`
(22 threats), restarting the counter per plan. The two namespaces differ by a
single hyphen and do **not** refer to the same threats — `T-02-17` (02-09,
README attribution pointer) is a different threat from `T-2-17` (02-05, README
attribution pointer), and `T-02-01` (02-07, `ci.yml` permissions) is unrelated
to `T-2-01` (SKILL.md frontmatter). This collision is recorded here rather than
silently normalised, because any future register merge that pattern-matches one
namespace will drop or conflate the other. It is exactly what happened during
this audit's first assembly pass.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| repository text → `tools/check_repo.py` parsers | Locally-authored, arbitrarily-shaped Markdown and YAML-ish text crosses into stdlib parsers with no schema library behind them | Untrusted-shaped local text |
| `SKILL.md` frontmatter → every installing harness | Read at install and skill-selection time on a user's machine; a defect surfaces as a silent non-load with no local signal | Skill metadata |
| paraphrased framework concepts → published repository | Rule prose crosses from three proprietary, trademarked frameworks into an MIT-licensed public repo | Third-party IP |
| deal-brief facts → worked examples in the skill folder | Facts cross from `examples/deal-brief.md` into shipped examples, where a drifted figure becomes a published claim | Invented but publishable figures |
| vendor claim → published proposal prose | Rules govern sentences that become contractually, reputationally, or legally checkable once specific | Commercial claims |
| external state → the skill's knowledge | Certification status, disclosure permission, competitor capability and legal exposure are state the skill cannot access | Unavailable ground truth |
| customer source material → retained vendor prose | PF-3.3 lets an external document's vocabulary override the deletion rule | Provenance |
| check report → the writer's confidence to send | A clean report is the artifact most likely to be read as permission to send | Assurance |
| repository claims → a public reader | `README.md` and `evals/pressure-tests.md` are read as statements of measured fact | Public representations |
| a named check → the trust placed in a green build | A registered, documented, inert code makes the build assert something nobody verified | Build assurance |
| repository content → GitHub Actions runner | `check_repo.py` reads repo files including files a fork's PR modified; the runner executes the workflow | Fork-modified content |
| `check_repo.py` → the filesystem | Mutation mode copies a repo subset to a temp dir and writes mutated files there — the only write path in the tool | Temp-dir writes |

---

## Threat Register — `T-2-NN` namespace (plans 02-01…02-06)

| Threat ID | Category | Severity | Disposition | Mitigation (file:line) | Status |
|---|---|---|---|---|---|
| T-2-01 | Tampering / DoS | high | mitigate | `SKILL.md:1-14` four-key frontmatter, name==dir; enforced `tools/check_repo.py:726-728`, `:802-830`, `:833-836`; 4 mutations proven | closed |
| T-2-02 | Tampering | medium | mitigate | `tools/check_repo.py:543-555` `_carrier_is_repo_relative`, gate applied `:708`; `:223` fixed `SKILL_GLOB`; `:850` anchored regex; `:774-777` repeated-key handling. See precision note below | closed |
| T-2-03 | Tampering | high | mitigate | `SOURCES.md:5-9`, `:12-22`, `:24-54`, `:56-68`; `NOTICES.md:50-101`, `:30-32`; `SKILL.md:20`; mechanical half `tools/check_repo.py:640-685`; human half signed off `02-UAT.md` test 1 | closed |
| T-2-04 | Tampering | high | mitigate | `tools/check_repo.py:1118` MUTATION_SOURCES; `:1393-1416` 22 MUTATIONS; `:1483-1486` fails any code with no mutation; `:1462-1481` silent-on-control-then-fires. Measured 22/22 discrimination-proven | closed |
| T-2-05 | Info disclosure | low | mitigate | `tools/check_repo.py:475`, `:478-518`; `examples/deal-brief.md:5`, `:18`, `:97-123`; `worked-examples.md:3-6`. Live run 0 `unlisted-figure` | closed |
| T-2-06 | Tampering | high | mitigate | `worked-examples.md:36`, `:46`, `:61`, `:66`, `:71` — 5 `GAP:` markers, no substitute figures; `SKILL.md:157` forbids anonymised stand-ins | closed |
| T-2-07 | Tampering | high | mitigate | `SKILL.md:165-169` raises `REVIEW (commitment)` rather than deciding; `worked-examples.md:75-76` states a past fact, not a promise | closed |
| T-2-08 | Tampering | high | mitigate | `SKILL.md:177-181`; `worked-examples.md:85-86` uses an invented competitor declared at `examples/deal-brief.md:15`, `:18` | closed |
| T-2-09 | Tampering | high | mitigate | `SKILL.md:183-187` requires the gap stated plainly; `worked-examples.md:90-91` names Type I held / Type II required, never asserts verified | closed |
| T-2-10 | Spoofing | high | mitigate | `SKILL.md:207` override fires only against supplied customer material; `deletion-test.md:36-43` excludes vendor-written text | closed |
| T-2-11 | Repudiation | high | mitigate | `SKILL.md:207`, `:43` — retention never suppresses an integrity rule; worked instance `deletion-test.md:45-59`, `worked-examples.md:105-106` | closed |
| T-2-12 | DoS | high | mitigate | `SKILL.md:245`, `:251`, `:257` three prohibition halves; missing-device → GAP at `:247`, mechanism `:159-163` | closed |
| T-2-13 | Tampering | medium | mitigate | `deletion-test.md:61-67` — explicit "does not enumerate a list of banned or allowed terms" | closed |
| T-2-14 | Repudiation | high | mitigate | `SKILL.md:305-307` — four unverifiable items enumerated **and** "A clean check report is not legal clearance" | closed |
| T-2-15 | DoS | high | mitigate | `SKILL.md:298`, `:300`, `:301` additive sweep mandatory, `:303` warning sign stated | closed |
| T-2-16 | Tampering | high | mitigate | `evals/pressure-tests.md` 14 cells `not yet observed`; `:10-12` forbids extrapolation; `:32-35`; `:84-85`. No `%` anywhere in the file | closed |
| T-2-17 | Tampering | medium | mitigate | `README.md:114` exactly one pointer; enforced `tools/check_repo.py:583-596`; `NOTICES.md:39` carrier list; 2 mutations proven | closed |
| T-2-18 | Spoofing | medium | mitigate | `SKILL.md:45` register heading names sending as the boundary; `:276` every inline marker also a register row; `:290` D-17 contract | closed |
| T-2-19 | Repudiation | high | mitigate | `tools/check_repo.py:929` byte-exact regex, `:932-960` binds both directions; `SKILL.md:31` states 31 rules / 6 sections, matching `NUMBERING.md:86-116` | closed |
| T-2-20 | DoS | medium | mitigate | `tools/check_repo.py:999` 500-line ceiling, `:1002-1009`; boundary fixtures `:2175`/`:2179`; companion token check `:1020-1036`; WINDOWS id 5 `fixed` | closed |
| T-2-21 | Tampering | medium | mitigate | `tools/check_repo.py:311-337` `parse_pf_subblocks`; containment `:368-370`; gapped fixture `:2035-2062` wired `:2198`, asserted `:2304` | closed |

## Threat Register — `T-02-NN` namespace (plans 02-07, 02-08, 02-09)

| Threat ID | Plan | Category | Severity | Disposition | Mitigation / Rationale | Status |
|---|---|---|---|---|---|---|
| T-02-01 | 02-07 | Elevation of privilege | low | accept | `.github/workflows/ci.yml` has no `permissions:` block and triggers on `pull_request`. Confirmed absent. Accepted: no secrets, no deploy step, no untrusted interpolation into `run:`, and `pull_request` not `pull_request_target` | closed (accepted) |
| T-02-02 | 02-07 | Tampering | low | mitigate | `worked-examples.md` content move preserved fact-to-brief binding (`:3-6`) | closed |
| T-02-03 | 02-07 | Info disclosure | low | accept | Moved example content carries no new disclosure surface | closed (accepted) |
| T-02-04 | 02-07 | Tampering | medium | mitigate | WINDOWS.md id 5 recorded `fixed` with `resolved_at` set; token check ships with its mutation | closed |
| T-02-05…07 | 02-07 | Spoofing / DoS / EoP | — | accept | Explicit "no applicable threat in this STRIDE class" declarations | closed (declared n/a) |
| T-02-08 | 02-08 | Tampering | low | mitigate | `_copy_repo_subset` + `_mutate_*` write only inside a temp dir | closed |
| T-02-09 | 02-08 | Tampering | low | mitigate | Content-derived path reads gated by `_carrier_is_repo_relative` | closed |
| T-02-10 | 02-08 | Repudiation | **high** | mitigate | `tools/check_repo.py:1437-1439` separate `discrimination_proven` / `fire_only` sets; `:1472-1478` FIRE-ONLY branch; `:1488-1495` state-independent reporting. Measured 22 proven, 0 fire-only | closed |
| T-02-11 | 02-08 | Info disclosure | low | accept | Violation messages print only repo-relative paths and public content | closed (accepted) |
| T-02-12 | 02-08 | DoS | low | accept | Doubled work in mutation mode is a ~5s cost | closed (accepted) |
| T-02-13…14 | 02-08 | Spoofing / EoP | — | accept | Explicit "no applicable threat in this STRIDE class" declarations | closed (declared n/a) |
| T-02-15 | 02-09 | Tampering | **high** | mitigate | Every `README.md:20-33` "exists" claim confirmed on disk; every `:35-43` "(planned)" entry confirmed absent; `README.md:26` "20 worked ✗/✓ pairs" matches 20 `^## PF-` sections in `worked-examples.md`; no `%` in README | closed |
| T-02-16 | 02-09 | Tampering | **high** | mitigate | Exactly 14 unfilled Observed cells in `evals/pressure-tests.md`; no fabricated observation; no rate claim | closed |
| T-02-17 | 02-09 | Tampering | medium | mitigate | `README.md:114` pointer intact after the rewrite; `pointer-*` codes green | closed |
| T-02-18 | 02-09 | Repudiation | medium | mitigate | WINDOWS.md ledger ids 3 and 4 remain `open` with `resolved_at: null` — honestly unresolved, not silently closed | closed |
| T-02-19…22 | 02-09 | Info disc. / Spoofing / DoS / EoP | — | accept | Explicit "no applicable threat in this STRIDE class" declarations | closed (declared n/a) |

*Status: open · closed · closed (accepted) · closed (declared n/a)*
*Only open threats at or above `high` count toward `threats_open`.*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| R-02-01 | T-02-01 | `ci.yml` has no `permissions:` block. Accepted for this phase: the workflow holds no secrets, performs no deploy, interpolates nothing untrusted into `run:`, and triggers on `pull_request` (fork PRs get a read-only token) rather than `pull_request_target`. Adding an explicit least-privilege `permissions: contents: read` remains the correct hardening and is breadcrumbed for a future security pass | security audit 2026-09-11 | 2026-09-11 |
| R-02-02 | T-02-11 | Violation messages are printed into public CI logs. Verified to name only repo-relative paths and content that is already public in an MIT repo | security audit 2026-09-11 | 2026-09-11 |
| R-02-03 | T-02-03, T-02-12 | Moved example content adds no disclosure surface; mutation mode's doubled work costs ~5s | security audit 2026-09-11 | 2026-09-11 |
| R-02-04 | T-02-05…07, T-02-13…14, T-02-19…22 | Nine rows carry `—` severity because each plan explicitly declared *no applicable threat in that STRIDE class*, rather than omitting an assessment. Deliberately **not** escalated under a fail-closed "missing severity ⇒ critical" rule, which would manufacture blockers out of a completeness convention | security audit 2026-09-11 | 2026-09-11 |

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-11 | 43 | 43 | 0 | gsd-security-auditor (opus), ASVS L1, verified by orchestrator |

**Register origin:** `register_authored_at_plan_time: true` — all nine PLAN files
carried a parseable `<threat_model>` block, so this audit verified that registered
mitigations exist rather than scanning for new threats.

**Traceability finding.** No SUMMARY file contains a `## Threat Flags` section, and
no SUMMARY or `02-VERIFICATION.md` cites any threat ID in either namespace. Every
mitigation was found present in shipped files; none had ever been tagged back to
the threat that motivated it. Future phases should record threat IDs in SUMMARY
threat-flag sections so this audit is a lookup rather than a reconstruction.

**Precision note on T-2-02 (does not change the verdict).** The register's
mitigation text claims `parse_skill_catalog` *and* `parse_checklist` "extract only
ID tokens matched by an anchored regex." True of `parse_skill_catalog`
(`tools/check_repo.py:850`); **not** true of `parse_checklist` (`:867-877`), which
returns each row's first column unfiltered. The load-bearing half still holds and
is what closes the threat: every `repo_root /` and `root /` construction was traced
and no `parse_checklist` output reaches a path operand. If a future change makes a
checklist column path-valued, this threat reopens and the anchored-regex claim will
not save it.

**Open follow-up, outside this audit's scope.** `.planning/WINDOWS.md` ids 3 and 4
remain `open` while `02-UAT.md` records both as passed. Id 4 in particular should
**not** be closed while all 14 Observed cells in `evals/pressure-tests.md` still
read `not yet observed`. With `workflow.windows_enforce` on, `/gsd-ship` blocks
while `open_count > 0`.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed — 0 open at or above `high`
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-09-11
