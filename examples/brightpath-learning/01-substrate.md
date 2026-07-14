# BrightPath ① Substrate

> Template: [`layers/01-substrate/`](../../layers/01-substrate/README.md) · Everything fictional.

## Identity

One SSO org. Six human roles (`content_editor`, `coach`, `growth_analyst`, `ops_specialist`,
`engineer`, `founder`) and three agent principals (`agent.triage`, `agent.billing-reconciler`,
`agent.content-qa`), each with `on_behalf_of` set. No service account is shared between two
agents — the billing MCP server and the triage agent hold different credentials even though
both were written by the same engineer in the same week.

## RBAC (excerpt — full shape in the layer template)

```json
{
  "role": "agent.content-qa",
  "kind": "agent",
  "on_behalf_of": "content_editor",
  "grants": [
    {"resource": "memory.vault", "actions": ["read", "write"]},
    {"resource": "tools.cms", "actions": ["read"]}
  ],
  "denied": [
    {"resource": "tools.cms", "actions": ["publish"], "why": "publishing is a human act; agent files findings, editor publishes"}
  ]
}
```

The matrix is one JSON file in the infra repo. Changing it requires a pull-request review from
the founder or the engineering lead — that review *is* the access-review process at this scale.

## Environments

Three cloud projects: `bp-dev`, `bp-staging`, `bp-prod`. Staging receives a nightly copy of
prod events **already scrubbed by ②** (never raw). All three agents run in staging with
`dry_run: true` — staging exists to read their would-have-done logs before promoting changes.

## Secrets

One managed secrets store, paths scoped per principal per environment
(`bp-prod/agent.triage/helpdesk-token`). Rotation every 90 days. Break-glass: the founder can
disable the gateway (⑤) with one flag, which stops all agent actions org-wide.
