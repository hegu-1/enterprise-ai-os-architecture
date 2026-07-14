# Maturity self-assessment — where are you, per layer?

Score each layer 0–3. Be harsh; the gap map is the roadmap. A company at Brain=3 and
Governance=0 is not "mostly done" — it is one incident away from a program freeze, because
the layers don't average: **your effective maturity is your minimum across ③ and ⑦.**

| Layer | 0 — absent | 1 — ad-hoc | 2 — systematic | 3 — compounding |
|---|---|---|---|---|
| ① Substrate | shared API keys in code | secrets manager, human SSO | agents are identities, RBAC versioned | access reviews automated, revocation in minutes |
| ② Sensor | copy-paste into prompts | per-tool scripts | unified envelope + dedup + entry-time scrub | schema registry, quarantine SLA, drift alarms |
| ③ Memory | none (context window is "memory") | notes/wiki nobody's agent reads | provenance + authority on every node, permission-scoped retrieval | consolidation running, cross-BU edges producing decisions |
| ④ Brain | one hardcoded vendor | model picked per project | router + rule layer + sensitivity constraints | eval as deploy gate, drift checks, cost attribution |
| ⑤ Executor | agents call APIs directly | some tools wrapped | one gateway, idempotency declared, gate-before-execution | dry-run standard, compensation registry, adversarial tests |
| ⑥ Orchestration | chains inside one prompt | scripts + cron | cards + explicit ownership + durable state | cross-BU discovery, orphan detection, sagas |
| ⑦ Governance | "we trust the model" | logging after the fact | risk-tiered gates before execution, CI-validated policy | calibration loop running, delegation chains, compliance mapping |

## Reading your scores

- **③ or ⑦ at 0–1, anything else at 3** — you built capability on sand; go to [Phase 0 of the playbook](playbook.md) regardless of how much is "already live."
- **Everything at 1** — normal 2025-era state. Phase 1 of the playbook, one vertical, resist breadth.
- **③⑦ at 2, capability layers at 1** — rare and *good*: the expensive part is done; verticals will now stand up fast (Phase 2).
- **Uneven across BUs** — pick the strongest BU as the Phase 2 template rather than averaging efforts across all.

Re-score quarterly. The commodity layers (①②④⑤⑥) will drift up on vendor gravity alone;
the moats (③⑦) move **only** when someone owns them — which is the empirical version of this
repo's whole argument.
