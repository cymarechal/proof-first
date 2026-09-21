# API Coverage — Phase 06 (legal-review-gate-launch)

This phase ships no code that calls an external API, SDK, or service. Every external surface that
was touched during the work was touched by a human doing research, and opts out below.

## Why the detector fired

The `api-coverage.verify-pre` gate detected the signal `(surface) + rest` in
`06-02-PLAN.md:151`:

> `| Caption | *MEDDICC Ltd. v. 01 Consulting LLC* | CourtListener REST v4 search, q=MEDDICC&type=r |`

That line is a **retrieval-path citation**. It records how a docket fact in `LEGAL-REVIEW.md` was
obtained during legal diligence, so a reader can reproduce the lookup. The phase records the answer;
it does not ship the query.

## What the phase actually delivers

Four plans produced `SOURCES.md`, `NOTICES.md`, `LEGAL-REVIEW.md`, the README claim-region edits, a
results renderer over committed JSON fixtures, and the launch-gate ledger sweep. All Markdown, plus
stdlib-only Python over local files.

## Surface

| capability | decision | reason |
|---|---|---|
| CourtListener REST v4 search | OPT-OUT | One-off diligence lookup. Its result is a static fact in LEGAL-REVIEW.md with the reproducing curl shown for audit. No repo code issues the request at build, test, or run time. |
| CourtListener REST v4 docket | OPT-OUT | Same lookup, docket-scoped. Latest entry recorded as a dated fact, not polled. Integrating it would put a network call in a repo whose stated constraint is zero dependencies. |
| USPTO TSDR register status | OPT-OUT | Attempted in research; returned HTTP 503 and 403. Register state is recorded as NOT CONFIRMED in LEGAL-REVIEW.md rather than integrated or guessed. |
| USPTO TMSearch | OPT-OUT | Attempted in research; POST returned HTTP 405. Same disposition as TSDR — the unknown is published as unknown. |
| Anthropic Messages API | OPT-OUT | evals/benchmark/run_benchmark.py drives the local claude CLI over subprocess, not the HTTP API. The repo holds no API client, no auth handling, and no endpoint knowledge. |

## Evidence

- `grep -rnE "urllib|requests|http\.client|import socket|fetch\(|axios"` across `evals/ tools/
  skills/ prompts/ output-styles/ .github/` returns no client code. The only matches are
  `web_search_requests: 0` / `web_fetch_requests: 0` telemetry fields inside committed benchmark
  result JSON — recorded values, not call sites.
- Project constraint (`PROJECT.md`): "Dependencies: Zero. One folder, no install step."
- CI runs stdlib-only Python over committed files; no network step.

Recorded at the `verify:pre` gate of `/gsd-verify-work 06`.
