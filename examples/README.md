# Worked examples — two fictional production environments

> **Everything here is fictional.** BrightPath Learning and Meridian Freight do not exist.
> Names, numbers, events, and people are invented to be *production-shaped*: realistic enough
> to copy, fictional enough to publish. Any resemblance to real companies is coincidental.

Two environments, one per scale, so you can diff them and see exactly what changes with scale
— and what doesn't (the kernel):

| | [BrightPath Learning](brightpath-learning/README.md) | [Meridian Freight](meridian-freight/README.md) |
|---|---|---|
| Scale | 45-person online-learning startup | 12,000-person freight & logistics group |
| Memory ③ | markdown vault + git | temporal knowledge graph, role-scoped |
| Agents | 3 (triage, billing-reconciler, content-qa) | ~200 across 5 business units |
| Governance ⑦ | risk gates + weekly calibration | + compliance mapping, delegation chains, audit platform |
| Regulated data | payment records | payment + driver records (transport regulator) |

The config files in these directories are **live test fixtures**: the repo's CI
(`checks.sh` at the root) runs the layer tools against them on every push — the PII scrubber
over BrightPath's raw events, the provenance validator over both audit logs, the risk-gate
test cases against both policies. If the badge is green, what you are copying runs.

## How to copy this into your company

1. Read the environment closest to your scale, layer by layer, next to the matching [`layers/`](../layers/) guide.
2. Copy the layer templates; replace the fictional names with your systems.
3. Keep the invariants (each layer README's "one rule that matters" + acceptance checklist) — those are the architecture. Everything else is placeholder.
4. Wire your own `checks.sh` so your policies and audit logs are CI-validated from day one.
