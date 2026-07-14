# Minimum eval harness (template)

The eval suite is a **deploy gate**, not a dashboard. No routing change, adapter, or prompt
revision ships without passing it.

## Structure

```
evals/
├── suites/
│   ├── classify-intake.jsonl    # frozen input → expected output pairs, per task class
│   ├── draft-reply.jsonl        # graded by rubric (see below), not exact match
│   └── regulated-extract.jsonl  # includes canary records that MUST refuse external routing
├── rubrics/
│   └── draft-reply.md           # what "good" means, written down, versioned
└── results/
    └── 2026-07-14--router-v3.json   # every run archived: config hash + scores
```

## The three gates

| Gate | Question | Fails when |
|---|---|---|
| Quality | did scores drop vs. the last accepted run? | any suite falls > agreed tolerance (e.g. 2 pts) |
| Sensitivity | did any canary regulated record reach an external tier? | one canary escape = hard fail, no tolerance |
| Cost/latency | did cost-per-task or p95 latency regress > threshold? | silent 3× cost increases hide inside "upgrades" |

## Cadence

- **On every change** to routing / prompts / adapters: full gate run (CI).
- **Weekly drift check**: same suite, unchanged config — catches upstream model/vendor drift you didn't cause.
- **Quarterly adapter review**: every fine-tune re-scored against the current base model; retire adapters the base has caught up to.

## Writing suites that mean something

- Source cases from **real (scrubbed) production events** (②), not invented examples — invented cases test what you imagined, not what arrives.
- Include the ugly ones: mixed-language, half-formed, wrong-channel, adversarial.
- Freeze suites per version; when you change a suite, both old and new run once so score history stays comparable.
