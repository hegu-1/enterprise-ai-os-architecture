# BrightPath ③ Memory

> Template: [`layers/03-memory/`](../../layers/03-memory/README.md) · Everything fictional.

## The vault

One private git repo, `bp-vault`, laid out exactly as
[`layers/03-memory/templates/vault-layout.md`](../../layers/03-memory/templates/vault-layout.md):

```
bp-vault/
├── telos/goals-2026.md              # L4 — founder-written, agents read-only (⑦ forbids agent writes)
├── knowledge/                       # L3 — refund-policy.md, coaching-escalation.md, course-style-guide.md ...
├── projects/module-4-relaunch.md    # L2 — settled conclusions per project
├── log/2026-07-10.md                # L1 — the day the module-4 incident happened
├── raw/                             # L0 — scrubbed event exports (② is the only writer)
└── INDEX.md
```

## A real node (the memory the refund saga wrote)

```markdown
---
id: log/2026-07-10#refund-7734
level: L1_episodic
authority: agent_inferred
provenance: {who: agent.billing-reconciler, source: "evt-9f03", why: "duplicate charge confirmed against subscription record"}
valid_until: until_superseded
confidence: 0.93
scope: {visibility: ops}
---
Learner 7734 double-charged on 2026-07-09 renewal. Recommended refund of one charge.
Root cause matches [[knowledge/billing-retry-bug]] — third occurrence this quarter.
```

The wiki-link to `knowledge/billing-retry-bug` is the graph edge: when the third occurrence
appeared, the weekly consolidation review promoted "billing retry can double-charge" from
recurring L1 pattern to an L3 node — **a human ratified the promotion** (that commit is the
calibration loop, ⑦, running at human scale).

## Scoping

Coaching session notes live in a *separate* repo (`bp-vault-coaching`) — coaches' notes about
learners are confidential-class and the triage agent has no grant to that repo (①). At this
scale, repo boundary = permission boundary; retrieval cannot leak what the principal cannot clone.
