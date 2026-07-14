# ⑦ Governance ★ — the second moat, and the procurement gate

> Position: top of the stack — the kernel that lets autonomous agents act fast *without*
> silent drift, and makes that auditable. **You build this.** It is the layer no serious
> enterprise will deploy agents without, and the one no vendor can sell you finished,
> because it encodes *your* org's judgment.

## The six primitives

| Primitive | One line | Template / spec |
|---|---|---|
| Provenance-enforced | every mutation emits who/what/why/source — the audit trail exists *by construction* | [`templates/provenance-record.schema.json`](templates/provenance-record.schema.json) |
| Drift-aware | execution-overrun, abstraction-drift, premature closure are instrumented and surfaced | [drift-aware-agent](https://github.com/hegu-1/drift-aware-agent) |
| Judgment-aware | memory distinguishes current judgment from stale opinion; judgments expire | ③ `authority` + `valid_until` fields |
| Schema-coexistence | stable judgment in a slow human-ratified core; evolving capability in a fast agent edge | [schema-coexistence-spec](https://github.com/hegu-1/schema-coexistence-spec) |
| Calibration loop | external feedback → tagged source → schema delta → **human ratifies** → audit trail | [calibration-loop-protocol](https://github.com/hegu-1/calibration-loop-protocol) |
| Capability tokens | boundary-crossing actions need scoped, expiring, logged tokens; no token → refuse-and-surface | [`templates/capability-token.schema.json`](templates/capability-token.schema.json) |

## Risk-tiered judgment gates

Route every action by **risk × reversibility × blast-radius**, so you neither over-gate (and
kill the speed that justified agents) nor under-gate (and lose accountability):

| Tier | Meaning | Gate |
|---|---|---|
| T0 | reversible, self-contained, low sensitivity | `auto` — act, log, report |
| T1 | reversible, team-visible | `auto` + same-day human review queue |
| T2 | irreversible (any), or org-wide blast radius | `human_ratify` before execution |
| T3 | regulated data, mass external reach, or money movement | `multi_party` (two approvers) or capability token |

Irreversibility floors an action at T2 — a human must ratify — but never reaches T3 by
itself: T3 is reserved for the dimensions above, so two-approver friction lands only where it pays.

Policy is data, not code: [`templates/risk-tier-policy.json`](templates/risk-tier-policy.json). The ⑤ gateway calls the gate synchronously before every mutating action.

## Tools in this directory (zero-dependency, python3)

```bash
# validate an audit log: every record well-formed, gates consistent with tiers
python3 tools/validate_provenance.py <audit-log.jsonl> [more.jsonl ...]

# decide the gate for one action against a policy
python3 tools/risk_gate.py --policy risk-tier-policy.json --action action.json

# run a policy's test cases (CI gate)
python3 tools/risk_gate.py --policy risk-tier-policy.json --cases gate-cases.json
```

`validate_provenance.py` enforces the cross-field rules that make audit *mean* something:
T2 records must show a ratifier, T3 records must show two distinct approvers or a capability
token reference, irreversible actions can never be T0/T1.

## Enterprise additions

Beyond the six primitives, enterprise scale adds: **compliance mapping** (policies compiled
into machine-checkable rules with audit evidence generated automatically), observability
across thousands of agents, **delegation chains** (which agent acts on whose authority,
revocably — the `on_behalf_of` field from ① travels through every record), and **incident
rollback** (every action reversible or compensable; ⑤ carries the compensation registry).

## Acceptance checklist

- [ ] Every mutation across all layers emits a provenance record; sampled daily for completeness.
- [ ] The risk-tier policy is versioned, reviewed, and its test cases run in CI.
- [ ] T3 actions are impossible without two approvers or a valid capability token (tested adversarially).
- [ ] The calibration loop has run end-to-end at least once (feedback → delta → ratified → audit) before you scale agent count.
- [ ] A random audit record can be traced to its source event (②) and memory writes (③) in under five minutes.

**Worked examples:** [BrightPath governance + audit log](../../examples/brightpath-learning/07-governance.md) · [Meridian](../../examples/meridian-freight/README.md)
