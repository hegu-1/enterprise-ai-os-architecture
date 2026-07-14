# ③ Memory ★ — the first moat

> Position: the layer that makes the model swappable. Not a database — a living cognition
> substrate every agent reads and writes, with provenance and confidence on every node.
> **You build this.** It is one of the two layers you cannot buy, because it *is* your org's accumulated cognition.

## The five memory levels

```
L4 telos        org objectives, the "why"                    human-authored only
L3 semantic     concepts, SOPs, policies, knowledge graph    consolidated from below
L2 working      projects, docs, settled conclusions          agent-written, human-ratified
L1 episodic     decisions, incidents, interactions           org-scale "tracelets"
L0 raw          all ingestion, immutable, provenance-stamped fed only by layer ②
```

Consolidation runs upward continuously (raw → episodic → semantic: dedup, merge, expire);
authority runs downward (a decision recorded at L4/L3 overrides anything an agent inferred at L1).

## What this layer must provide

- **One hybrid store, queried as one.** Physically: temporal knowledge graph (entities/relations with validity windows) + vector store + document store. Logically: a single retrieval API.
- **Provenance on every write.** Who/what wrote this node, from which source, why — this is the same record shape ⑦ audits ([`../07-governance/templates/provenance-record.schema.json`](../07-governance/templates/provenance-record.schema.json)).
- **Permission travels with memory.** The same graph projects differently per role and per BU; retrieval filters by permission *before* returning, never after. A leak here is a breach, not a bug.
- **Recall that mimics memory, not search.** Association along graph edges (cross-BU edges are how silos break), lazy retrieval of the activated-and-permitted sub-graph, salience/recency weighting.
- **Forgetting is a feature.** Retention policy per level and per data class ([`templates/retention-policy.json`](templates/retention-policy.json)); judgments carry expiry; compliance deletion reaches every projection (including embeddings).

## The one rule that matters

**Distinguish authored judgment from inferred opinion.** Every node carries an `authority`
field: `human_authored` > `human_ratified` > `agent_inferred`. Agents may write freely at
`agent_inferred`; promotion upward requires a human in the loop (the calibration loop in ⑦).
This single field is what prevents *silent capture* — the org's memory quietly diverging from
what humans actually decided.

## Failure modes

- **Retrieval-time permission filtering** ("fetch then redact") — one prompt-injection away from a breach.
- **No expiry** — three-year-old conclusions retrieved with the same confidence as yesterday's decision.
- **Write-anything agents** — without the authority field, one hallucinated "fact" propagates into every future context.
- **Embeddings that outlive deletion** — compliance deletion must delete projections too.

## Templates in this directory

- [`templates/memory-node.schema.json`](templates/memory-node.schema.json) — the node envelope: level, authority, provenance, confidence, validity window, permission scope.
- [`templates/retention-policy.json`](templates/retention-policy.json) — per-level, per-class retention and consolidation cadence.
- [`templates/vault-layout.md`](templates/vault-layout.md) — the n=1 / small-team version: the same five levels as a markdown + git repo, runnable today with zero infrastructure.

## Acceptance checklist

- [ ] Every node has provenance, authority, and a validity window; writes without them are rejected.
- [ ] Retrieval is permission-filtered before return; tested with an adversarial "ask for what you shouldn't see" suite.
- [ ] Consolidation runs on a schedule and is observable (nodes merged/expired per day).
- [ ] A compliance delete provably removes graph nodes, documents, **and** embeddings.
- [ ] Cross-BU edges exist and are queried (measure: % of retrievals crossing a BU boundary).

**Worked examples:** [BrightPath memory](../../examples/brightpath-learning/03-memory.md) · [Meridian](../../examples/meridian-freight/README.md)
