# ⑥ Orchestration — agent mesh · A2A · workflows · durable execution

> Position: coordination above single agents — who works on what, across BUs, over hours or weeks.
> **Mature open-source exists; the craft is routing the right work to the right agent.**

## What this layer must provide

- **Agent cards** — every agent publishes a discoverable card ([`templates/agent-card.json`](templates/agent-card.json)): what it does, what it needs, its principal (①), its cost profile. Cross-BU delegation happens by card discovery, not by hardcoded wiring.
- **A workflow engine with durable execution** — long-running processes survive restarts and deploys; state is checkpointed, not held in an agent's context window.
- **Sagas / compensation** — multi-step business processes declare per-step compensation (⑤ provides the compensating actions) so partial failures unwind cleanly.
- **Ownership routing** — every piece of work has exactly one owning agent (or human) at all times; handoffs are explicit events, not silences.
- **Scheduling** — cron-like recurring work (consolidation ③, eval drift checks ④, access reviews ①) lives here, versioned.

## The one rule that matters

**Don't over-orchestrate.** Splitting what one agent could do into five coordinated agents
adds latency, cost, and failure modes while producing worse output — coordination overhead is
real for agents just as for humans. Start with one agent per vertical; split only when a
measured bottleneck (context size, permission boundary, throughput) forces it.

## Failure modes

- **Deadlocks and loops** — agent A waits on B, B on A; or a retry loop nobody bounded. Every workflow has a timeout and a human escalation path.
- **Responsibility drift** — work nobody's agent owns. The ownership invariant above; measure "orphaned items" weekly.
- **Lost long-running state** — a deploy wipes an in-flight process. Durable execution or don't run week-long workflows.
- **Hardcoded agent wiring** — BU-A's orchestrator names BU-B's agent directly; B refactors, A breaks silently. Discovery via cards.

## Templates in this directory

- [`templates/agent-card.json`](templates/agent-card.json) — the discoverable agent descriptor.
- [`templates/workflow.example.json`](templates/workflow.example.json) — a saga-style workflow spec with per-step compensation and escalation.

## Acceptance checklist

- [ ] Every agent has a card; cross-BU calls resolve through discovery.
- [ ] Long-running workflows survive a rolling deploy (tested, not assumed).
- [ ] Every workflow step names its compensation or is explicitly marked irreversible (which raises its ⑦ risk tier).
- [ ] Orphaned-work count is measured and alarmed.
- [ ] Recurring maintenance (③ consolidation, ④ drift evals, ① access review) runs from here, not from cron scripts on someone's laptop.

**Worked examples:** [BrightPath workflows](../../examples/brightpath-learning/06-orchestration.md) · [Meridian](../../examples/meridian-freight/README.md)
