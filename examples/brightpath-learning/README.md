# BrightPath Learning — startup-scale environment (fictional)

> 45-person online-learning company: self-serve courses + 1:1 coaching for adult upskilling.
> Teams: Content (10) · Coaching (12) · Growth (8) · Ops (6) · Engineering (9).
> **Fictional** — see [examples/README.md](../README.md).

## The deployment at a glance

Three agents, one thin gateway, memory as a git vault. Total infrastructure: a cloud account,
a git host, a secrets manager, and three MCP servers. This is deliberately the *smallest
honest instance* of the seven layers — nothing here requires a platform team.

| Layer | BrightPath instance | Config |
|---|---|---|
| ① Substrate | SSO + RBAC matrix in git; dev/staging/prod projects | [`01-substrate.md`](01-substrate.md) |
| ② Sensor | helpdesk + chat + billing webhooks → one event stream, scrub-at-entry | [`02-sensor.md`](02-sensor.md) |
| ③ Memory | markdown vault + git, five levels, weekly consolidation | [`03-memory.md`](03-memory.md) |
| ④ Brain | rules-first routing, two model tiers, eval gate in CI | [`04-brain.md`](04-brain.md) |
| ⑤ Executor | 3 MCP servers behind one gateway, dry-run default in staging | [`05-executor.md`](05-executor.md) |
| ⑥ Orchestration | one refund saga + scheduled consolidation; 3 agent cards | [`06-orchestration.md`](06-orchestration.md) |
| ⑦ Governance | risk-tier policy + audit log (CI-validated) + weekly calibration | [`07-governance.md`](07-governance.md) |

## The three agents

- **`agent.triage`** (on behalf of Ops) — classifies inbound helpdesk/chat, routes to owning queue, drafts first replies. Sends nothing itself.
- **`agent.billing-reconciler`** (on behalf of Finance-in-Ops) — matches billing webhooks against expected subscriptions, recommends refunds. Cannot move money.
- **`agent.content-qa`** (on behalf of Content) — checks new course modules against the style SOP (memory L3), files findings as L1 nodes.

## What to notice at this scale

- **Permissions are coarse but real** — repo boundaries and one RBAC file, yet already zero shared credentials and agents as identities.
- **Governance is two files and a habit** — the risk policy, the audit log, and a weekly 30-minute calibration review. The mechanism, not the platform.
- **The moats already exist at n=45**: the vault compounds (③), and the audit trail is already the thing a customer's security questionnaire asks for (⑦).
