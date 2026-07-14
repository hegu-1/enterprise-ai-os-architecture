# BrightPath ⑦ Governance

> Template: [`layers/07-governance/`](../../layers/07-governance/README.md) · Everything fictional.

## Two files and a habit

Governance at 45 people is: [`governance/risk-policy.json`](governance/risk-policy.json)
(the gate policy, with [`governance/gate-cases.json`](governance/gate-cases.json) as its CI-run
test suite), [`governance/audit-log.sample.jsonl`](governance/audit-log.sample.jsonl) (a slice
of the provenance stream — every record CI-validated), and the **weekly calibration review**:
30 minutes on Monday where a human walks the week's `auto_with_review` queue and ratifies or
reverts vault promotions. That habit is the calibration loop; the files are its rails.

```bash
python3 layers/07-governance/tools/risk_gate.py \
  --policy examples/brightpath-learning/governance/risk-policy.json \
  --cases  examples/brightpath-learning/governance/gate-cases.json

python3 layers/07-governance/tools/validate_provenance.py \
  examples/brightpath-learning/governance/audit-log.sample.jsonl
```

## What the sample audit slice shows

One morning's records, deliberately spanning the whole gate spectrum:

- a **T1** vault write by `agent.triage` (auto, lands in Monday's review queue)
- a **T2** customer reply — drafted by the agent, ratified by an ops specialist
- a **T3** refund — the billing reconciler recommended, founder + ops lead both approved
- a **refusal** — `agent.content-qa` attempted a write to `telos/` (L4); the gateway logged `gate.mode: forbid` and the agent surfaced it to its human instead of improvising
- a **dry-run** — staging's copy of the same refund, simulated, zero approvers needed

The refusal record is the one to study: *no token → refuse and surface* produced an audit
line, a ping to the content lead, and no action. Silent failure and silent success are both
absent, which is the entire design goal.

## What a customer security review sees

BrightPath's answer to "how do you control your AI agents?" is this directory: the policy
(versioned, tested), the audit trail (validated, complete), the delegation chains
(`on_behalf_of` on every agent record). At startup scale the ⑦ moat is not a platform — it's
*having answers with receipts* while competitors have a paragraph of reassurance.
