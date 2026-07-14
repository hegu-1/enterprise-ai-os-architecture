# BrightPath ⑤ Executor

> Template: [`layers/05-executor/`](../../layers/05-executor/README.md) · Everything fictional.

## The gateway and the three MCP servers

One gateway process; three MCP servers behind it: `mcp-helpdesk` (tickets, replies),
`mcp-billing` (subscriptions, refunds), `mcp-cms` (course content). Registry excerpt —
the full shape is the layer template:

```json
{
  "tool": "helpdesk.send_reply",
  "mcp_server": "mcp-helpdesk",
  "mutating": true,
  "effects": [{"resource": "tools.email.customer", "action": "send"}],
  "risk_hint": {"blast_radius": "external", "reversible": false},
  "idempotency": "ticket_id + draft content hash — the same draft never sends twice",
  "compensation": "follow-up correction (imperfect; hence the gate)",
  "dry_run_supported": true
}
```

## What the gate feels like in practice

`agent.triage` drafts a reply and calls `helpdesk.send_reply`. The gateway: (1) resolves the
agent's effects against the RBAC matrix — pass; (2) calls the ⑦ risk gate — an irreversible
external send floors at **T2 / human_ratify**, so the action **parks** in the ops approval
queue; (3) emits a provenance record with `gate.mode` and the queue reference.

An ops specialist approves batches from the queue twice a day; approval executes the send and
completes the record's `approved_by`. Median human overhead: ~4 seconds per reply, because
the draft plus the agent's one-line *why* is usually enough context. That 4 seconds is the
entire current cost of "no unsupervised external sends" — which is what makes the rule survivable.

## Idempotency in anger

The billing webhook connector redelivers on timeout (at-least-once). Twice in the fictional
spring, `agent.billing-reconciler` processed the same dispute event twice; both times the
refund request deduped on `refund_request_id` at the billing MCP server. The double-charge
that *creates* refund work never became a double-refund that creates more.
