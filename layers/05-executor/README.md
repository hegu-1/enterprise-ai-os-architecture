# ⑤ Executor — tool gateway · MCP farm · permission-checked actions

> Position: where decisions become real-world actions — and where mistakes stop being retractable.
> **You integrate this; MCP is the standard.** Every action passes RBAC (①) + governance (⑦) *before* execution.

## What this layer must provide

- **One tool gateway.** Every tool the org exposes to agents goes through a single registry ([`templates/tool-registry.json`](templates/tool-registry.json)) — uniform auth, uniform logging, uniform permission checks. An MCP server farm is the natural shape: one MCP server per system, all registered here.
- **Per-action permission checks** — resolved against the ① RBAC matrix per call, per principal. Not per session: an agent's authority can be revoked mid-run.
- **Governance gate before execution** — the ⑦ risk-tier decision (`auto` / `human_ratify` / `multi_party` / `forbid`) happens *before* the side effect, never as an after-the-fact filter.
- **Idempotency, retry, compensation** — every mutating tool declares an idempotency key strategy and (where possible) a compensating action. Agents retry; without idempotency, retries double-charge.
- **Dry-run as a first-class mode** — every mutating tool accepts `dry_run` and returns what it *would* do. Staging runs dry-run by default (①-environments).

## The one rule that matters

**Gate before, never filter after.** An "executed then flagged" action is an incident, not a
control. The gateway calls the ⑦ gate synchronously; if the gate says `human_ratify`, the
action parks in an approval queue — parked is a success state, not an error.

## Failure modes

- **Actions beyond authority** — an agent chains two individually-permitted tools into an unpermitted outcome. Mitigation: permission checks on *effects* (resource + action), not just tool names.
- **Non-idempotent retries** — double charges, duplicate emails. The registry refuses mutating tools that declare no idempotency strategy.
- **Tool sprawl** — every team wires its own API keys and the gateway becomes optional. One gateway, no exceptions; unregistered tools don't get credentials (①).

## Templates in this directory

- [`templates/tool-registry.json`](templates/tool-registry.json) — the registry entry shape: effects, permissions required, risk class, idempotency, compensation, dry-run support.

## Acceptance checklist

- [ ] 100% of agent-reachable tools are in the registry; credentials exist only inside the gateway.
- [ ] Every mutating tool declares idempotency + compensation (or documents why impossible).
- [ ] The ⑦ gate is called synchronously before every mutating action; parked actions have an owner and an SLA.
- [ ] Dry-run works on every mutating tool and staging uses it by default.
- [ ] An adversarial test exists: an agent instructed to exceed its authority is refused at the gateway (not by prompt politeness).

**Worked examples:** [BrightPath tool registry](../../examples/brightpath-learning/05-executor.md) · [Meridian](../../examples/meridian-freight/README.md)
