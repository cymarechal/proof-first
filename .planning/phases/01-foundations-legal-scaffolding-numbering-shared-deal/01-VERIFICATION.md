---
phase: 01-foundations-legal-scaffolding-numbering-shared-deal
verified: 2026-09-10T07:21:30Z
status: gaps_found
score: 7/9 must-haves verified (2 truths present-in-content but not enforced; see gaps)
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "`python3 tools/check_repo.py` exits 0 when none of the attribution-pointer carrier files named in NOTICES.md exist yet, and exits non-zero when a named carrier file exists and does not contain the pointer string exactly once. (01-01 must_haves, edge LEG-03/empty)"
    status: failed
    reason: >
      tools/check_repo.py's parse_notices() extracts the canonical pointer with the regex
      `## Attribution pointer\s*\n+```[^\n]*\n(.*?)\n```` — this only matches when the fenced
      block begins immediately after the heading. Both 01-01-PLAN.md and 01-03-PLAN.md require
      (and NOTICES.md as shipped carries) an explanatory prose paragraph between the heading and
      the fence ("The following string is the canonical, verbatim attribution pointer..."). The
      regex therefore never matches against production NOTICES.md, `pointer` resolves to `None`,
      and `check_pointer()` returns `[]` unconditionally for a `None` pointer — so `pointer-missing`
      and `pointer-duplicated` can never fire against the live repository, no matter what any
      carrier file (README.md today; SKILL.md and the reference files once Phase 2/4 create them)
      actually contains. This is not a hypothetical: it is independently reproduced below.
    artifacts:
      - path: "tools/check_repo.py"
        issue: "parse_notices() (module-level regex near line 315) cannot parse the real NOTICES.md shape; check_pointer() (line ~336) short-circuits to [] when pointer is None instead of treating an unparseable pointer definition as a violation."
    missing:
      - "A parser tolerant of prose between the `## Attribution pointer` heading and its fenced block (e.g. capture the section body up to the next `## ` heading, then find the first fenced block inside that body, rather than anchoring the fence directly to the heading)."
      - "Fail-loud behavior when no pointer can be parsed at all — an unparseable pointer definition should itself be a violation, not silent success."
      - "A `--self-test` fixture whose inline NOTICES.md mirrors the real file's shape (heading, prose paragraph, then fence) so this exact regression class is caught by CI rather than only by manual/adversarial review. The current `_bad_notices()`/`_good_notices()` fixtures place the fence immediately after the heading, which is why `--self-test` reports the pointer checks as \"covered\" while they are dead code against production content."
---

# Phase 1: Foundations — Legal Scaffolding, Numbering, Shared Deal Verification Report

**Phase Goal:** The project's foundational scaffolding — rule numbering, shared example data, and legal posture — is frozen before any rule content is drafted, so nothing downstream forces a renumbering or a retrofit.
**Verified:** 2026-09-10T07:21:30Z
**Status:** gaps_found
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A contributor can look up the next free ID in either the `PF-<section>.<n>` or `MC-<n>` namespace without guessing (ROADMAP SC1) | ✓ VERIFIED | `NUMBERING.md` carries all 9 required headings, 6 PF ranges, 7 PF-1 sub-blocks (ceiling `PF-1.28`), 8 MC blocks, zero-row Allocated/Deprecated tables. Independently re-verified `dup-id`, `range-id`, `revived-id`, `undefined-id` all fire correctly when a duplicate/out-of-range/revived/undefined ID is injected into a production-shaped copy of `NUMBERING.md` (see Behavioral Spot-Checks). |
| 2 | Every worked example can cite facts (figures, roles, timeline, competitors) from one canonical fictional deal brief (ROADMAP SC2) | ✓ VERIFIED | `examples/deal-brief.md` carries all 14 required headings/sub-headings, the full cast (`Halverton Mutual`, `Kestrel Systems Group`, `Ardent Digital`, `Vantage Nine Consulting`, 5 named people), 18-key Canonical figures table (sorted, unique), the `landing zone` verbatim-retention example, and 2 explicitly-marked inconvenient facts. `unlisted-figure`/`dup-figure-key`/`figure-order` verified to fire correctly when a stray unlisted `$` figure is injected *before* the Canonical figures section (see Behavioral Spot-Checks and Anti-Patterns below for a position-dependent gap in the same check). |
| 3 | `LICENSE` and `NOTICES.md` individually name all three frameworks (Command of the Message, MEDDICC, Challenger) with non-affiliation and trademark language, before any framework-derived content ships (ROADMAP SC3) | ✓ VERIFIED | `LICENSE` is unmodified MIT text, one file at root. `NOTICES.md` carries `## Scope of this file` (precedence/no-trademark-grant/coverage-default sentences) and `## Framework statements` with exactly 3 fixed-order `###` subsections (`Command of the Message`, `MEDDIC, MEDDICC, and related marks`, `Challenger`), each with all 5 labelled elements. MEDDIC-family subsection states ownership is "claimed by multiple parties" (contested), not attributed to one holder. |
| 4 | Nothing in the repo reproduces proprietary framework text; framework concepts are paraphrased and sources are cited wherever they appear (ROADMAP SC4) | ⚠️ Content verified / enforcement FAILED — see gap | `SOURCES.md` defines the reproduction boundary, the 6 candidate source rows are honestly marked `unverified`/`to confirm at LEG-04` (by design — edge item 14, backstop tier), and both the independent code-review pass and this verifier's own read found no reproduced framework text in any of the 8 phase-1 files. **However**, the mechanical no-drift guarantee this same requirement's Phase-1 tracer plan (01-01) was explicitly built to prove — that `tools/check_repo.py` catches a carrier file that silently drops or duplicates the attribution pointer — is dead code against the real `NOTICES.md`/carrier-file shape. See gap below; content is fine today, but nothing enforces it going forward. |
| 5 | (01-01 must-have) `check_repo.py` exits non-zero when a named carrier file exists and lacks the pointer string exactly once (LEG-03/empty edge) | ✗ FAILED | See Gaps Summary and the empirical reproduction under Behavioral Spot-Checks. |
| 6 | (01-01 must-have) `check_repo.py --self-test` proves every check family fires on a known-bad fixture and stays silent on a known-good one | ⚠️ Present but misleading | `--self-test` exits 0 and names all 9 codes as "covered," including `pointer-missing`/`pointer-duplicated` — but its own inline fixture NOTICES.md places the fence directly under the heading, a shape that does not match (and is inconsistent with) the production NOTICES.md the plan itself mandates. The self-test genuinely proves the checker's logic works on *its own* fixture shape; it does not prove the checker works on this repository's actual file shape, which is the gap. |
| 7 | (01-04 key link) `README.md` is the first real attribution-pointer carrier, so `pointer-missing` "stops being fixture-only and starts enforcing against shipped content" | ✗ FAILED | Empirically falsified: deleting the entire pointer line from `README.md` and re-running `check_repo.py` still reports `0 violations`, exit 0. The key link does not hold; README's content is never actually inspected by this check. |
| 8 | `.github/workflows/ci.yml` runs the checker's self-test and live check on every push, before any rule content exists | ✓ VERIFIED | Single `check` job, `ubuntu-latest`, checkout + setup-python 3.11 + `--self-test` then live run, zero `pip install` lines. (CI actually going green on GitHub itself is unverifiable from this environment, as 01-01-SUMMARY itself discloses — routed as informational, not a gap, since the workflow file's structure and commands are directly verifiable and correct.) |
| 9 | No empty placeholder file was created for any documented-but-unbuilt path (D-15) | ✓ VERIFIED | `find . -type f -empty -not -path './.git/*'` → 0 files. |

**Score:** 7/9 verified, 2 failed (both tracing to the same root cause: the attribution-pointer parser).

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `NUMBERING.md` | 9-section ID registry, PF/MC ranges, empty Allocated/Deprecated tables | ✓ VERIFIED | All headings, ranges, and required literal strings present; wired into `check_repo.py` (ID checks proven to fire). |
| `tools/check_repo.py` | Stdlib-only checker, 9 violation codes, fixture self-test | ⚠️ PARTIAL | 7 of 9 codes (`dup-id`, `range-id`, `revived-id`, `undefined-id`, `dup-figure-key`, `figure-order`, `unlisted-figure`) independently proven to fire against production-shaped content. `pointer-missing`/`pointer-duplicated` are present in code and named by `--self-test` but are dead against the real `NOTICES.md` shape (see gap). Stdlib-only import purity confirmed. |
| `.github/workflows/ci.yml` | Single job, self-test then live check, no `pip install` | ✓ VERIFIED | Confirmed on disk; `grep -c 'pip install'` → 0. |
| `examples/deal-brief.md` | Complete fictional deal, Canonical figures table | ✓ VERIFIED | All required headings/content present and wired to the checker (with one narrow positional gap noted under Anti-Patterns). |
| `NOTICES.md` | Scope section, attribution pointer, 3 framework statements | ✓ VERIFIED (content) / the pointer block that content *feeds* the checker is what's unwired — see gap | |
| `LICENSE` | Unmodified MIT | ✓ VERIFIED | |
| `SOURCES.md` | Rule, reproduction boundary, 3 source tables, out-of-bounds list | ✓ VERIFIED | All 6 headings present; 6 status-bearing rows, all honestly `unverified` by design (LEG-04 deferral). |
| `README.md` | Claim-free entry point, first real pointer carrier | ✓ VERIFIED (content) / not actually enforced as a carrier — see gap | |

### Key Link Verification

| From | To | Via | Status | Details |
|------|-----|-----|--------|---------|
| `NUMBERING.md` reserved-range tables | `tools/check_repo.py` ID-integrity parser | reads ranges from the registry | ✓ WIRED | Confirmed: injecting an out-of-range/duplicate/revived ID into a production-shaped `NUMBERING.md` copy is caught. |
| `examples/deal-brief.md` Canonical figures table | `tools/check_repo.py` figure scanner | machine-readable interface | ⚠️ PARTIAL | Wired for content appearing before the last heading in the file (confirmed). Not wired for content appended after the `## Canonical figures` heading in any `examples/**/*.md` file where that heading is the file's last section — see Anti-Patterns. |
| `NOTICES.md` attribution-pointer block + carriers list | `tools/check_repo.py` pointer assertion | one canonical string, N pointers | ✗ NOT WIRED | `parse_notices()` cannot extract the pointer from the real file shape; `check_pointer()` never runs against real content. Confirmed empirically (see Behavioral Spot-Checks). |
| `.github/workflows/ci.yml` | `tools/check_repo.py` | CI runs both modes on every push | ✓ WIRED | Workflow steps and commands verified on disk. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Self-test passes | `python3 tools/check_repo.py --self-test` | `self-test PASS - verified violation codes: dup-figure-key, dup-id, figure-order, pointer-duplicated, pointer-missing, range-id, revived-id, undefined-id, unlisted-figure` | ✓ PASS (misleading for the 2 pointer codes — see gap) |
| Live run on repo as shipped | `python3 tools/check_repo.py` | `check_repo: 0 violations` | ✓ PASS |
| Two consecutive runs byte-identical | `diff -q` on two runs | identical | ✓ PASS |
| Stdlib-only imports | `ast`-based import scan | exit 0 | ✓ PASS |
| **CR-01 empirical reproduction:** stripping the attribution pointer entirely from `README.md` (the only real, shipped carrier) | copy repo to temp dir → delete the pointer line from `README.md` → `python3 tools/check_repo.py` | `check_repo: 0 violations`, exit 0 — the defect the check exists to catch produces zero signal | ✗ FAIL (this is the gap) |
| `dup-id`/`range-id`/`revived-id` fire on production-shaped `NUMBERING.md` | copy repo → inject dup/out-of-range/revived rows into the real `## Allocated IDs` / `## Deprecated IDs` tables → run checker | all three fired correctly with exit 1 | ✓ PASS |
| `undefined-id` fires on production-shaped scan roots | copy repo → add `skills/proof-first/SKILL.md` citing an unallocated `PF-3.99` | `undefined-id` fired correctly | ✓ PASS |
| `unlisted-figure` fires when injected before the last heading | copy repo → inject a stray `$999,999,999` inside the `## Timeline` section of `examples/deal-brief.md` | `unlisted-figure` fired correctly | ✓ PASS |
| `unlisted-figure` positional blind spot | copy repo → append a stray `$999,999,999` *after* `## Canonical figures` (the file's last heading) | `check_repo: 0 violations` — the figure is never scanned because `in_canonical` never resets after the last heading | ✗ FAIL (new finding, not currently exploited by any shipped content; documented under Anti-Patterns as a WARNING, not upgraded to a gap) |

### Probe Execution

No `scripts/*/tests/probe-*.sh` convention applies to this phase; `tools/check_repo.py --self-test` and the live run serve this role and are covered above.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
| CAT-07 | 01-01 | Citable IDs in two disjoint namespaces, ranges reserved per section | ✓ SATISFIED | `NUMBERING.md` + working ID-integrity checks |
| EX-01 | 01-01, 01-02 | Single fictional deal brief supplies canonical facts | ✓ SATISFIED | `examples/deal-brief.md` complete; figure checks work (with the narrow positional caveat above) |
| LEG-01 | 01-03 | MIT license covering all original content | ✓ SATISFIED | `LICENSE` + `NOTICES.md` scope section |
| LEG-02 | 01-03 | Individually named non-affiliation/trademark statement per framework | ✓ SATISFIED | `NOTICES.md` `## Framework statements`, 3 fixed-order subsections |
| LEG-03 | 01-01, 01-03, 01-04 | Zero proprietary text reproduced; concepts paraphrased, sources cited | ⚠️ CONTENT SATISFIED / ENFORCEMENT BLOCKED | Manual/code-review reads found no reproduction today. The no-drift enforcement mechanism this requirement's own tracer plan built to guarantee that stays true going forward is non-functional — see gap. |
| LEG-04 | Phase 6 | Legal review gate, MEDDIC-family status reconfirmed | Correctly deferred | Not in scope for Phase 1; `SOURCES.md` explicitly names it as owner. |
| LEG-05 | Phase 6 | README claims/badges sourced only from committed benchmarks | Correctly deferred | `README.md` already carries no claim; full enforcement is Phase 6's. |

No orphaned requirements: the union of `requirements:` fields across all four plans (`CAT-07, EX-01, LEG-01, LEG-02, LEG-03`) exactly matches REQUIREMENTS.md's Phase 1 mapping.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `tools/check_repo.py` | `parse_notices()` (~315) / `check_pointer()` (~336) | Attribution-pointer regex cannot match production `NOTICES.md` shape; `None` pointer silently short-circuits to zero violations | 🛑 BLOCKER | LEG-03's no-drift guarantee is asserted (in NUMBERING.md's key_links, 01-01's objective, and 01-04's key_link) but not enforced. Confirmed by this verifier independently of the prior code review. |
| `tools/check_repo.py` | `check_unlisted_figure()` (~266-293) | `in_canonical` flag never resets to `False` when `## Canonical figures` is the last heading in a file, so any content appended after it in `examples/**/*.md` is never scanned for unlisted figures | ⚠️ WARNING | Not currently exploited (nothing exists after the table today), but the figure-integrity guarantee has an undocumented positional blind spot symmetric to the already-flagged WR-02 (value-collision) finding. Distinct root cause; not previously reported by the code review. |
| `tools/check_repo.py` | `parse_numbering()` / `check_range_id()` (~97-134, ~152-169) | MC IDs validated against one aggregate `(min,max)` across all 8 dimension blocks rather than each block's own range (WR-01, previously flagged by 01-REVIEW.md) | ⚠️ WARNING | Currently harmless (blocks are contiguous, zero rows allocated); would silently under-enforce if a future range widening ever introduces a gap between MC blocks. Does not currently undermine SC1 since the "next free ID" answer is stated in NUMBERING.md's own prose, not computed by this check. |
| `tools/check_repo.py` | `check_unlisted_figure()` (~267, 287) | Value-based matching with no key binding (WR-02, previously flagged by 01-REVIEW.md) | ⚠️ WARNING | Confirmed as previously described; a new fact whose formatted value coincidentally equals an existing unrelated canonical value would be silently accepted. |

No `TBD`/`FIXME`/`XXX` debt markers found in any phase-1 file.

## Assessment of the flagged review finding (CR-01)

CR-01 is real, independently reproduced by this verifier (not merely re-stated from the review), and material to phase completion. 01-01-PLAN.md's own stated purpose was explicit: *"This is the tracer slice for the whole phase... proving that path on one ID, one figure, and one attribution string catches a format dead-end after one commit... D-14's no-drift attribution guarantee are all the same architectural mechanism applied three times."* Two of those three mechanisms (ID integrity, figure integrity) are proven to work end-to-end against production-shaped content. The third — attribution-pointer integrity — is not: it works only against the checker's own self-test fixture, which was written with a document shape (fence immediately under the heading) that the plan's own subsequent instructions (01-01 Task 3, 01-03 Task 1-2) require to *not* match (a prose paragraph must sit between the heading and the fence). The self-test therefore certifies a shape that was never going to exist in this repository, while the shape that does exist was never tested. This is a genuine BLOCKER, not a stylistic nitpick: the phase's stated goal is that scaffolding is frozen "so nothing downstream forces a renumbering or a retrofit," and the specific mechanism meant to prevent silent attribution drift once Phase 2/4 add `skills/proof-first/SKILL.md` and its reference files as new carriers currently cannot fire under any circumstance — a carrier file could ship with zero, one, or a hundred copies of the pointer string and CI would stay green regardless.

**This looks unintentional**, not an accepted deviation — no override is suggested.

## Assessment of "also worth checking" items

- **WINDOWS.md unrun-verify items (name-collision search, comparison read-through):** Correctly deferred, not a phase-1 blocker. Both are logged with clear descriptions, an honest disposition (`open`, no reason given because they are not yet resolved), and are explicitly scoped to "before the repository goes public" / LEG-04 territory rather than to Phase 1's own success criteria. Routed to Human Verification below.
- **SOURCES.md all-unverified rows:** Correctly deferred by design (edge item 14 in 01-01-PLAN.md's ledger is explicitly `verification: backstop`, owned by Phase 6's LEG-04 gate). The must-have this phase actually owns — that `SOURCES.md` *defines* the reproduction boundary and names its owner — is satisfied; the must-have this phase does *not* own — that each candidate source is actually confirmed — is correctly not claimed as done anywhere in the phase's artifacts. Not a gap.
- **WR-01 (MC aggregate range) / WR-02 (unlisted-figure value-collision):** Neither undermines success criterion 1 or 2 as they stand today (see Anti-Patterns table above for the specific reasoning). Kept as WARNINGs, consistent with the original review's own severity classification. Not escalated to BLOCKER.

## Human Verification Required

### 1. Name-collision web search over the 9 invented names

**Test:** Search the web for `Halverton Mutual`, `Kestrel Systems Group`, `Ardent Digital`, `Vantage Nine Consulting`, `Diane Osoria`, `Marcus Feld`, `Priya Raghunathan`, `Tom Weatherly`, `Gina Almeida`.
**Expected:** None matches an existing company or a real identifiable person in insurance, retirement services, or systems integration.
**Why human:** Requires live network access this verifier and both prior executors lacked. Already logged as `.planning/WINDOWS.md` item 1.

### 2. Independent comparison read-through of `examples/deal-brief.md`

**Test:** An independent reviewer (not the executor who wrote the text) reads the brief end to end.
**Expected:** No sentence compares two real companies or two real products; VMware vSphere/Oracle Database/AWS products appear only as migration source/target.
**Why human:** The plan explicitly requires an independent reviewer, distinct from the executor who authored the content; the self-review already performed is a substitute, not the specified check. Already logged as `.planning/WINDOWS.md` item 2.

### 3. Fix and re-verify the attribution-pointer parser (the gap above)

**Test:** After patching `parse_notices()`/`check_pointer()` per the missing items listed in the gap, re-run the CR-01 reproduction: strip the pointer string from README.md in a scratch copy and confirm `check_repo.py` now exits non-zero with `pointer-missing`.
**Expected:** Non-zero exit, `pointer-missing` line printed.
**Why human/not fully automatable here:** The fix itself is a code change requiring a planning/execution loop (a closure plan), not something this verifier should silently apply.

## Gaps Summary

One BLOCKER: `tools/check_repo.py`'s attribution-pointer check (`parse_notices`/`check_pointer`) cannot parse the real shape of `NOTICES.md` and therefore never fires against the live repository or any of its carrier files, including the one that already ships (`README.md`). This was independently reproduced by this verifier by deleting the pointer string from a copy of `README.md` and observing `check_repo: 0 violations`, exit 0. The `--self-test` fixture for this check uses a document shape that does not — and by the plan's own design, cannot — match production `NOTICES.md`, so CI stays green while the safety net for LEG-03's no-drift guarantee is dead code. This directly falsifies one of 01-01's own frontmatter must-have truths and one of 01-04's own frontmatter key-links. Everything else in the phase — the ID registry, the figure registry (content as shipped), the legal instruments' content, and the honest source-list scaffolding — is genuinely built and verified as claimed.

---

_Verified: 2026-09-10T07:21:30Z_
_Verifier: Claude (gsd-verifier)_
