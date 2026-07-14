# BrightPath ⑥ Orchestration

> Template: [`layers/06-orchestration/`](../../layers/06-orchestration/README.md) · Everything fictional.

## Deliberately minimal

Three agents publish cards; there is exactly **one** multi-step workflow (the refund saga,
instantiated from [`layers/06-orchestration/templates/workflow.example.json`](../../layers/06-orchestration/templates/workflow.example.json))
plus a scheduler. No workflow engine yet — the saga state is a row per refund in a
`workflow_state` table with a checkpointed step column, which survives deploys, which is all
"durable execution" has to mean at this scale.

This is the "don't over-orchestrate" rule applied: triage → draft → park-for-approval is a
*single agent plus a queue*, not a workflow. Only the refund path, which crosses two agents
and an irreversible action, earns saga treatment.

## The schedule

| When | What | Layer |
|---|---|---|
| nightly | scrubbed prod events → staging replay | ①/② |
| weekly (Mon) | vault consolidation review — 30 min, human ratifies promotions | ③/⑦ |
| weekly (Mon) | eval drift check, unchanged suites | ④ |
| quarterly | access review of the RBAC matrix + secrets rotation check | ① |

The schedule lives in one versioned file in the infra repo, not in anyone's crontab —
"recurring maintenance is orchestration" is what keeps it alive when the engineer who set it up leaves.

## Escalation

Every agent card names its human: triage → ops on low confidence or legal/regulatory flags;
billing-reconciler → founder on any amount above the coaching-package price; content-qa →
content lead on style-guide conflicts (the SOP might be the thing that's wrong — that
escalation is how L3 nodes get challenged rather than ossified).
