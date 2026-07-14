# ② Sensor — ingestion · event bus · entry-time PII scrub

> Position: everything the org hears, normalized onto one bus. **You integrate this.**
> Downward interface: lands raw data on ① storage. Upward interface: feeds ③ Memory L0 — nothing enters memory except through this layer.

## What this layer must provide

- **Connectors** — one per source system (chat, email, tickets, meetings, docs, code, CRM, ERP, logs), each owned by a named team.
- **A unified event envelope** — every source is normalized into the same shape ([`templates/event.schema.json`](templates/event.schema.json)) with a schema registry so drift is caught, not discovered.
- **Dedup** — the same signal arriving via two channels must collapse to one event (content hash + source key).
- **PII scrub at the entry point** — redaction happens *before* the event is persisted or enters memory. Entry-time scrubbing is the precondition for layer ③'s permission model: you cannot role-scope what you already leaked.

## The one rule that matters

**Scrub at entry, not at query.** If raw PII enters the memory layer, every downstream
projection, embedding, cache, and model context is contaminated, and no retrieval-time filter
can un-ring that bell. The scrubber runs *inside* the ingestion path, synchronously, and an
event that fails scrubbing is quarantined, not passed through.

## Failure modes

- **Silent schema drift** — a source changes a field, the connector keeps "working," memory fills with garbage. Registry + schema validation on every event.
- **Duplicates and drops** — the bus must be at-least-once + dedup, or exactly-once. Ad-hoc webhooks are neither.
- **Unscrubbed PII enters** — see above; this is the unrecoverable one.

## Tools & templates in this directory

- [`templates/event.schema.json`](templates/event.schema.json) — the unified event envelope (JSON Schema-style, machine-checkable).
- [`templates/pii-scrub-rules.json`](templates/pii-scrub-rules.json) — pattern-based scrub rules: emails, phones, payment cards, government IDs. A starting set — extend per jurisdiction.
- [`tools/pii_scrub.py`](tools/pii_scrub.py) — zero-dependency scrubber. Reads JSONL events, applies the rules, writes scrubbed JSONL. `--check` mode exits non-zero if any pattern survives (used in CI).

```bash
# scrub a batch of raw events
python3 tools/pii_scrub.py --rules templates/pii-scrub-rules.json \
    --in raw-events.jsonl --out clean-events.jsonl

# CI gate: assert a file is clean
python3 tools/pii_scrub.py --rules templates/pii-scrub-rules.json --check clean-events.jsonl
```

## Acceptance checklist

- [ ] Every source system flows through a registered connector with an owner.
- [ ] All events validate against the envelope schema; schema changes require a registry update.
- [ ] Dedup rate is measured (duplicate events per day) and alarmed.
- [ ] PII scrubbing is in the ingestion path, synchronous, with quarantine on failure.
- [ ] A red-team sample (fake PII of every rule type) is run through the pipeline in CI — see `checks.sh` at repo root.

**Worked examples:** [BrightPath sensor config + sample events](../../examples/brightpath-learning/02-sensor.md) · [Meridian](../../examples/meridian-freight/README.md)
