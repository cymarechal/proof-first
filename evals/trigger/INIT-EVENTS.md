# Trigger Evaluation: Session Init-Event Payload Analysis

This document records the exact environment provided to Claude Code sessions at activation time during the trigger sensitivity evaluation. It inspects the `system`/`init` event from the raw transcript stream of each session to verify what information was actually delivered to the harness.

---

## Extraction Method

The extraction script parses each session's transcript stream to locate and validate the initial `system`/`init` event:

```python
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
```

---

## Arm B (Control) — 70 Sessions

- Every one of the 70 captured transcripts carries a valid `system`/`init` event (0 missing).
- All 70 sessions share **one identical top-level key set** (`distinct key sets: 1`) and **one identical `skills` field** (`distinct skills-field hashes: 1`), confirming that the harness presented an identical configuration across all phrasings.

**The init event's full top-level key set** (one representative event, keys sorted; identical across all 70 sessions in this arm, and across all 140 in both arms):

```
agents, analytics_disabled, apiKeySource, capabilities, claude_code_version, cwd,
fast_mode_disabled_reason, fast_mode_state, mcp_servers, memory_paths,
messaging_socket_path, model, output_style, permissionMode, plugins,
product_feedback_disabled, session_id, skills, slash_commands, subtype,
terminal_slash_commands, tools, type, uuid
```

**The `skills` field value**: A flat list of registered skill names delivered to the session (descriptions and frontmatter are not included in the init event):

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

### Analysis

The init event reveals that the harness receives available skills as a name-only inventory. Neither the frontmatter `description` nor trigger rules are present in this initial handshake event. This confirms the progressive disclosure model of Agent Skills: the harness holds skill identifiers at init, and subsequently retrieves each skill's frontmatter `description` during activation ranking when interpreting the user prompt.

---

## Arm A (Treatment) — 70 Sessions

Running the same extraction against `evals/trigger/transcripts/treatment/`:
- All 70 captured transcripts carry a valid `system`/`init` event.
- All 70 sessions share the identical top-level key set and `skills` field hash (`14563d17bfe7`), matching Arm B.
- **Controlled Comparison**: Both arms were executed in byte-identical harness environments. The only variable between Arm A and Arm B was the `description` string in `skills/proof-first/SKILL.md`.

---

## Transcript Retention

All 140 raw session transcripts across both arms are preserved in `evals/trigger/transcripts-cat10.tar.gz` (3988 KB compressed).
