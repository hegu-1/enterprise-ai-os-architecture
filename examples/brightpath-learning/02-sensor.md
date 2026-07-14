# BrightPath ② Sensor

> Template: [`layers/02-sensor/`](../../layers/02-sensor/README.md) · Everything fictional.

## Sources → one stream

Four connectors, each an owned piece of code: **helpdesk** (support tickets), **community
chat** (learner questions), **billing webhooks** (subscription events), **CMS** (course
content changes). All normalize into the unified event envelope and land on a single append-only
stream (a managed queue — at this scale, even a database table with an offset column works).

## Scrub at entry — live fixture

[`sensor/events.raw.sample.jsonl`](sensor/events.raw.sample.jsonl) is a captured-shape sample
of raw inbound events, seeded with the kinds of PII learners actually paste into tickets
(emails, phone numbers, card numbers). The repo CI runs the layer scrubber over it and then
asserts the output is clean:

```bash
python3 layers/02-sensor/tools/pii_scrub.py \
  --rules layers/02-sensor/templates/pii-scrub-rules.json \
  --in examples/brightpath-learning/sensor/events.raw.sample.jsonl \
  --out /tmp/bp-clean.jsonl
python3 layers/02-sensor/tools/pii_scrub.py \
  --rules layers/02-sensor/templates/pii-scrub-rules.json --check /tmp/bp-clean.jsonl
```

Events that fail scrubbing quarantine to a locked queue that only `ops_specialist` can read;
the quarantine count is on the weekly ops dashboard (it is usually zero, and when it isn't,
that's a new PII pattern to add to the rules — via pull request, so the rule change itself has provenance).

## Dedup

`dedup_key` = learner ref + normalized subject hash. The same learner asking the same question
in chat and then opening a ticket collapses to one signal with two source pointers — this
single field is why the triage agent doesn't answer people twice.
