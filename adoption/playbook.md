# Adoption playbook — from zero to an OS, in four phases

The same sequence at any scale. Each phase has **exit criteria**; entering the next phase
without them is how companies end up with N disconnected automations and a governance debt.
(The phase logic is argued in [the paper, §6](../README.md#6-build-sequence); this file is the operational version.)

## Phase 0 — the kernel, before any agent (1–2 weeks)

Do this with zero AI in production:

1. Copy [`layers/01-substrate/templates/rbac-matrix.json`](../layers/01-substrate/templates/rbac-matrix.json); fill in your real roles. Add your first agent principal *now*, even though it doesn't exist yet — with `on_behalf_of` and a `denied` list.
2. Copy [`layers/07-governance/templates/risk-tier-policy.json`](../layers/07-governance/templates/risk-tier-policy.json); write 5–10 gate test cases for actions that exist in *your* business ([BrightPath's](../examples/brightpath-learning/governance/gate-cases.json) are a model).
3. Wire `checks.sh` (copy from this repo's root) into your CI so policy + audit-log validation runs on every change.
4. Decide your memory substrate: below ~50 people, a markdown vault ([`layers/03-memory/templates/vault-layout.md`](../layers/03-memory/templates/vault-layout.md)) is the honest answer.

**Exit criteria:** the RBAC file and risk policy exist, are versioned, are CI-tested — and one human owns each.

## Phase 1 — one vertical, end-to-end (4–8 weeks)

Pick **one** flow with real volume and bounded blast radius (inbound triage is the classic).
Build the smallest instance of every layer for it: one connector with entry-time scrubbing
(②), memory writes with provenance (③), rules-first routing (④), one MCP server behind a
gateway that calls the gate (⑤), one agent card with a named human escalation (⑥), the audit
log validating in CI (⑦).

Run **dry-run for the first two weeks**: the agent logs what it would do; a human reviews
the would-have-done log daily. Promote to `auto` for T0/T1 only when the would-have-done
accuracy is boring.

**Exit criteria:** 30 days live; every action gated *before* execution; a random audit record traceable to its source event in <5 min; the human owner says the review load is sustainable.

## Phase 2 — replicate to prove the substrate (4–8 weeks per vertical)

Second and third verticals reuse the *same* bus, memory, gateway, and policy — different
connectors, agents, and rules only. Whatever you had to copy-paste instead of reuse is the
platform gap; fix it now, while it's cheap. This is where the platform layer forms —
resist the urge to build "the platform" before you have two consumers for it.

**Exit criteria:** a new vertical stands up in days, not weeks, and adds zero new governance machinery.

## Phase 3 — signals flow back and across (ongoing)

Consolidation (③) starts producing cross-vertical patterns; ratified conclusions flow back
into agent context. Add the cross-BU edges and the weekly calibration review if you haven't.
Watch the two standing dashboards: gate decisions per tier (over-gating vs. drift) and
orphaned work (⑥).

**Exit criteria:** at least one decision was changed by a cross-vertical pattern no single vertical could see. That's the moment the memory moat became real.

## Phase 4 — the OS layer

Shared memory graph with role-scoped projection, cross-BU routing, role/exec digests,
compliance mapping — the [Meridian example](../examples/meridian-freight/README.md) shows the
target shape. Only here does platform investment (workflow engine, observability, delegation
tooling) pay for itself. Most companies that fail, fail by starting here.

---

## The three ways this goes wrong

1. **Agents before kernel** — capability first, governance "later." Later never comes; retrofit costs 10× and the first incident is external.
2. **Platform before consumers** — a year of "AI platform" with zero verticals live. The platform layer *emerges* from Phase 2 friction, or it's fiction.
3. **Gates without calibration** — the policy ossifies, everything piles at human_ratify, humans rubber-stamp. The weekly calibration review exists precisely to keep the policy honest against reality.
