# Meridian Freight — enterprise-scale environment (fictional)

> 12,000-person freight & logistics group. Business units: Linehaul · Warehousing · Claims ·
> Finance · Compliance. ~200 agents in production. Regulated data: payments **and** driver
> records (transport regulator). **Fictional** — see [examples/README.md](../README.md).
>
> Read this as a **diff against [BrightPath](../brightpath-learning/README.md)**: same seven
> layers, same kernel, same gate tools running in CI against the files in
> [`governance/`](governance/) — what changes is scale and compliance, never the mechanism.

## Layer by layer — what scale actually changes

**① Substrate.** SSO + SCIM provisioning; 40+ human roles, ~200 agent principals — every one
still carrying `on_behalf_of`. The RBAC matrix is no longer one file but it is still *one
system*, and access reviews are quarterly and automated. The invariant survived: agents are
identities; zero shared credentials — now enforced by tooling instead of code review.

**② Sensor.** A real event platform: ~3M events/day from TMS, WMS, telematics, claims intake,
EDI, finance. Schema registry with connector version pinning; PII scrub at entry runs as a
stream processor with per-jurisdiction rule packs (driver IDs are scrubbed differently per
country). Quarantine is a monitored queue with an SLA, not a folder someone checks.

**③ Memory.** The markdown vault became a temporal knowledge graph + vector + document store,
role-scoped: a Claims adjuster's retrieval and a Warehouse supervisor's retrieval hit the
same graph and get different projections, filtered *before* return. The cross-BU edges are
where the money is: linking claims episodes to warehouse handling incidents surfaced a
packaging defect pattern (fictional) that neither BU could see alone — that edge type now has
an owning team. Compliance deletion provably reaches embeddings; that capability was a
regulator finding away from being mandatory.

**④ Brain.** Router adds an `internal_only` tier (self-hosted): anything touching driver
records or payment detail routes there as a hard constraint. Canary regulated-records run in
CI per BU. Fine-tunes exist only for two high-volume tasks (claims intake extraction, EDI
normalization); both are re-scored quarterly against the base model.

**⑤ Executor.** The MCP farm is ~40 servers behind one gateway team. Same registry shape as
the layer template, same invariant: gate before execution, idempotency declared or the
registry refuses the tool. Compensation is a first-class registry column because sagas (⑥)
compile from it.

**⑥ Orchestration.** A durable workflow engine runs day-to-week processes (claims
end-to-end, exception dispatch, month-end close support). Agent cards are the discovery
mechanism across BUs — Claims' orchestrator finds Warehousing's incident-lookup agent by
card, not by import. Orphaned-work detection pages a human coordinator.

**⑦ Governance.** The two files became a platform, but *the files in
[`governance/`](governance/) are still the kernel of it*:

- **Delegation chains**: every agent record's `on_behalf_of` resolves to a human with revocation rights; revocation propagates in minutes.
- **Compliance mapping**: transport-regulator and financial rules compiled into machine-checkable policies; audit evidence is generated from the provenance stream, not assembled by hand each audit season.
- **Capability tokens** in anger: an urgent after-hours claims payout goes out on a scoped, expiring, single-use token issued by the claims director — see `prov-m105` in [`governance/audit-log.sample.jsonl`](governance/audit-log.sample.jsonl) — instead of someone "borrowing" an approval or the agent improvising.
- **Observability**: gate decisions per tier per BU per week is a standing dashboard; a BU whose T2 ratifications pile up is under-delegating (fix the policy), one whose refusals spike is drifting (fix the agents).

## What did NOT change from BrightPath

The node schema (③), the provenance record (⑦), the gate decision function, the
refuse-and-surface behavior, the human-ratified promotion of judgment, `on_behalf_of` on
every agent action. That is the kernel, and it is the same JSON shapes this repo ships as
templates — which is the claim of the architecture: **get the kernel right at the cheapest
scale, then let scale change everything else.**
