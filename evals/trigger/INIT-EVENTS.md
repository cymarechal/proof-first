# Trigger Round Init-Event Distillation

This file records what each session in the CAT-10 gap-closure round was actually **given** at
activation time — the harness's own `system`/`init` event, read out of the raw transcript stream
each session wrote — not what the activation ranker did with it. Settling that latter question
(why a given phrasing did or did not activate `proof-first`) is a separate, unmechanised judgment;
this file only states the input surface, by measurement rather than by citation.

This corresponds to open causal questions Q3 and H3 in
`.planning/debug/DEBUG-cat10-trigger-over-fire.md`:

- **Q3** — is it structurally true that only the frontmatter `description` is read at activation?
  That file's own answer was "CONFIRMED as this repository's own sourced, HIGH-confidence reading
  of the Agent Skills standard... not independently measured in this repository." The extraction
  below is that independent measurement.
- **H3** — did a competing installed skill win the selection on the plain-English row (`Rewrite
  this paragraph in plain English for a general reader.`)? The `simple-english:simple-english`
  install is confirmed present as a candidate in every session (see below); whether it won the
  selection on that row is not measured by this file — the event stream shows what was on offer,
  not the ranker's internal reasoning.

## Extraction command

Run once per arm, against every transcript file captured under `evals/trigger/transcripts/<arm>/`:

```
python3 - <<'PYEOF'
import json, pathlib, hashlib

d = pathlib.Path('evals/trigger/transcripts/control')  # or 'treatment'
files = sorted(d.iterdir())

def first_init(text):
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith('{'):
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get('type') == 'system' and e.get('subtype') == 'init':
            return e
    return None

keysets = set()
skill_hashes = {}
missing = []
for f in files:
    e = first_init(f.read_text(encoding='utf-8'))
    if e is None:
        missing.append(f.name)
        continue
    keysets.add(tuple(sorted(e.keys())))
    h = hashlib.sha256(json.dumps(e.get('skills'), sort_keys=True).encode()).hexdigest()[:12]
    skill_hashes.setdefault(h, []).append(f.name)

print("total files:", len(files))
print("distinct key sets:", len(keysets))
print("missing init event in:", missing)
print("distinct skills-field hashes:", len(skill_hashes))
PYEOF
```

## Arm B (control) — 70 sessions, `evals/trigger/transcripts/control/`

- Every one of the 70 captured transcripts carries a `system`/`init` event (none missing).
- All 70 sessions' init events share **one identical top-level key set** (`distinct key sets: 1`)
  and **one identical `skills` field** (`distinct skills-field hashes: 1`) — the harness gave every
  session in this arm the same environment regardless of which phrasing it was driving.

**The init event's full top-level key set** (one representative event, keys sorted; identical
across all 70 sessions in this arm, and across all 140 in both arms). *Corrected 2026-09-22
(06-09): this block listed 23 keys and omitted `subtype` — the key the extraction script above
selects on to find the event in the first place. Every init event in all 140 committed transcripts
carries 24. The block is now asserted rather than restated:
`run_trigger_test.py --self-test` reads it back out of this file and compares it to the key set it
extracts from `transcripts-cat10.tar.gz`, so a future drift fails the build instead of surviving
four cold reads.*

```
agents, analytics_disabled, apiKeySource, capabilities, claude_code_version, cwd,
fast_mode_disabled_reason, fast_mode_state, mcp_servers, memory_paths,
messaging_socket_path, model, output_style, permissionMode, plugins,
product_feedback_disabled, session_id, skills, slash_commands, subtype,
terminal_slash_commands, tools, type, uuid
```

**The one key whose name contains "skill" (case-insensitive): `skills`.** Its value is a flat list
of skill *names* — no descriptions, no trigger text, no frontmatter fields — identical across all
70 sessions:

```
graphify, gsd-add-tests, gsd-ai-integration-phase, gsd-audit-fix, gsd-audit-milestone,
gsd-audit-uat, gsd-autonomous, gsd-capture, gsd-cleanup, gsd-code-review,
gsd-complete-milestone, gsd-config, gsd-debug, gsd-discuss-phase, gsd-docs-update,
gsd-eval-review, gsd-execute-phase, gsd-explore, gsd-extract-learnings, gsd-fast,
gsd-forensics, gsd-graphify, gsd-health, gsd-help, gsd-import, gsd-inbox,
gsd-ingest-docs, gsd-manager, gsd-map-codebase, gsd-mempalace-capture,
gsd-mempalace-recall, gsd-milestone-summary, gsd-mvp-phase, gsd-new-milestone,
gsd-new-project, gsd-next, gsd-ns-context, gsd-ns-ideate, gsd-ns-manage,
gsd-ns-project, gsd-ns-review, gsd-ns-workflow, gsd-onboard, gsd-pause-work,
gsd-phase, gsd-plan-phase, gsd-plan-review-convergence, gsd-pr-branch,
gsd-profile-user, gsd-progress, gsd-quick, gsd-resume-work, gsd-review,
gsd-review-backlog, gsd-secure-phase, gsd-settings, gsd-ship, gsd-sketch,
gsd-spec-phase, gsd-spike, gsd-stats, gsd-surface, gsd-thread, gsd-ui-phase,
gsd-ui-review, gsd-ultraplan-phase, gsd-undo, gsd-update, gsd-validate-phase,
gsd-verify-work, gsd-workspace, gsd-workstreams, orca-cli, proof-first,
deep-research, superpowers:brainstorming, superpowers:dispatching-parallel-agents,
superpowers:executing-plans, superpowers:finishing-a-development-branch,
superpowers:receiving-code-review, superpowers:requesting-code-review,
superpowers:subagent-driven-development, superpowers:systematic-debugging,
superpowers:test-driven-development, superpowers:using-git-worktrees,
superpowers:using-superpowers, superpowers:verification-before-completion,
superpowers:writing-plans, superpowers:writing-skills, simple-english:simple-english,
impeccable:impeccable, design, design-sync, dataviz, update-config, verify, debug,
code-review, simplify, batch, fewer-permission-prompts, doctor, loop, schedule,
claude-api, workflow-authoring, run, run-skill-generator
```

**What this settles.** The init event names every skill available to the session by name only —
`proof-first` is one name among roughly a hundred others, `simple-english:simple-english` is
confirmed present as a candidate on every session including the plain-English row, and no
description text, trigger vocabulary, or frontmatter content appears anywhere in the init event
itself. This is consistent with (and independently confirms, for the first time in this
repository) the Agent Skills specification's own progressive-disclosure model as
`.planning/research/STACK.md` already cited it: the harness's activation surface at init time is a
name list, and whatever ranking happens to select `proof-first` off a bare phrasing must consult
each named skill's own frontmatter `description` at some point after this event, not visible in
this event itself. **This file does not and cannot show that later step** — no event in the
captured stream carries a per-candidate score or a rejection reason. It shows what was on offer,
not why one name was picked.

**H3, evaluated on measurement rather than citation:** `simple-english:simple-english` was present
as a candidate in all 5 of Arm B's `Rewrite this paragraph in plain English for a general reader.`
sessions, all 5 of which recorded `did not fire` for `proof-first`. Whether `simple-english` itself
fired in place of `proof-first` on those sessions is not measured here — this runner only detects a
`Skill` tool-use naming `proof-first` (`detect_activation()`), by design, so it cannot and does not
report on any other skill's activation. This file states the candidate was present; it does not
state which skill, if any, was selected.

## Transcript retention

`du -k` on the gzipped tarball of this arm's 70 transcripts alone: **1964 KB**. The combined
retention decision across both arms is recorded once, in this file, at the end of Task 5 (Arm A),
per the pre-committed transcript-retention rule in `evals/trigger/DECISION-RULE-cat10.md`.

## Arm A (treatment) — 70 sessions, `evals/trigger/transcripts/treatment/`

Same extraction command as Arm B, with `d = pathlib.Path('evals/trigger/transcripts/treatment')`.

- All 70 captured transcripts carry a `system`/`init` event (none missing).
- All 70 sessions share **one identical top-level key set** and **one identical `skills` field**,
  and that field's content hash (`14563d17bfe7`) is byte-for-byte the same value Arm B's sessions
  recorded. **The two arms saw the identical activation environment** — the only variable between
  them was the `description` text itself, confirming the pairing the round's attribution claim
  depends on.
- The top-level key set and the `skills` field's contents are identical to Arm B's — see the Arm B
  section above; they are not reproduced a second time here since a byte-identical duplicate would
  only be a place for the two copies to silently drift apart.

**What this settles, for Arm A specifically.** The description that produced Arm A's zero over-fires
and one must-fire regression (`evals/trigger/RESULTS-trigger.md`'s Arm A block) was given to the
harness in the same bare-name-list form as Arm B's — no description text, no exclusion clause, no
trigger vocabulary appears in the init event for either arm. Whatever mechanism produced the
regression on "We're putting together our bid response — write the commercial section." acted on
information available to the harness at some point after this event (most plausibly, the
per-skill `description` fetched during activation ranking), not on anything visible in the init
event stream itself.

## Transcript retention (applied once, over both arms)

Per the pre-committed transcript-retention rule in `evals/trigger/DECISION-RULE-cat10.md`:
gzipping both arms' combined 140 transcripts (`evals/trigger/transcripts/control/` and
`evals/trigger/transcripts/treatment/`) into one tarball measured **`du -k` = 3988 KB**, under the
5120 KB threshold. The tarball is committed as `evals/trigger/transcripts-cat10.tar.gz`.

(Arm B alone measured 1964 KB gzipped, recorded above before the combined measurement was taken.)
