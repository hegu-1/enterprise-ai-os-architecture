# ① Substrate — compute · data · identity · network

> Position: bottom of the stack. No agents live here — pure infrastructure. **You buy this.**
> Upward interface: every layer above resolves *who is acting* and *what data exists* through this layer.

## What this layer must provide

| Capability | Minimum viable | Enterprise-grade |
|---|---|---|
| Identity | one SSO source of truth, humans **and** agents get identities | SSO + SCIM provisioning + service-account lifecycle |
| Authorization | a single RBAC matrix, versioned in git | org RBAC + per-BU scoping + periodic access review |
| Compute | wherever your models/tools run (cloud is fine) | GPU pools + inference scheduling + cost attribution |
| Data | one place raw data lands (object store / lakehouse) | lakehouse + catalog + lineage |
| Secrets | a secrets manager; nothing in code or prompts | + rotation policy + break-glass procedure |
| Network | environment separation (dev / staging / prod) | + egress control for agent traffic |

## The one rule that matters

**Agents are identities, not scripts.** Every agent gets its own principal in the identity
system, its own role in the RBAC matrix, and its own secrets scope. If an agent acts under a
human's borrowed credentials, every layer above — permission-checked actions (⑤), role-scoped
memory (③), audit (⑦) — is built on sand, because you can no longer answer *who did this*.

## Failure modes

- **Identity is wrong → everything downstream is wrong.** Permission bugs here are not bugs, they are breaches.
- **The data lake silts into a swamp.** If nothing enforces schema and ownership at landing time, layer ② inherits garbage.
- **Shared credentials.** One API key used by three agents means audit trails that cannot assign responsibility.

## Templates in this directory

- [`templates/rbac-matrix.json`](templates/rbac-matrix.json) — machine-readable role × resource × action matrix, covering human roles *and* agent principals. Referenced by the ⑤ Executor permission check and ⑦ Governance audit.
- [`templates/environments.md`](templates/environments.md) — minimum environment separation and secrets policy, copy-paste and adapt.

## Acceptance checklist (exit criteria before building ② on top)

- [ ] Every human and every agent has exactly one identity; zero shared credentials.
- [ ] The RBAC matrix lives in version control and review is required to change it.
- [ ] Raw data lands in one governed place with an owner per source.
- [ ] Secrets are in a manager, never in code, config files, or prompts.
- [ ] dev / staging / prod are separated; agents in staging cannot touch prod data.

**Worked examples:** [BrightPath (startup)](../../examples/brightpath-learning/01-substrate.md) · [Meridian (enterprise)](../../examples/meridian-freight/README.md)
