#!/usr/bin/env bash
# CI checks — zero dependencies beyond python3 stdlib.
# Green here means: every JSON file parses, both example environments' policies
# pass their gate test cases, both audit logs validate against the provenance
# rules, and the PII scrubber provably cleans the raw event fixture.
set -euo pipefail
cd "$(dirname "$0")"

echo "== 1/4 JSON syntax: every .json file parses =="
find layers examples -name '*.json' -print0 | while IFS= read -r -d '' f; do
  python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f" || { echo "INVALID JSON: $f"; exit 1; }
done
echo "OK"

echo "== 2/4 Risk gate: policy test cases (both environments) =="
python3 layers/07-governance/tools/risk_gate.py \
  --policy examples/brightpath-learning/governance/risk-policy.json \
  --cases  examples/brightpath-learning/governance/gate-cases.json
python3 layers/07-governance/tools/risk_gate.py \
  --policy examples/meridian-freight/governance/risk-policy.json \
  --cases  examples/meridian-freight/governance/gate-cases.json

echo "== 3/4 Provenance: audit logs validate =="
python3 layers/07-governance/tools/validate_provenance.py \
  examples/brightpath-learning/governance/audit-log.sample.jsonl \
  examples/meridian-freight/governance/audit-log.sample.jsonl

echo "== 4/4 PII scrub: raw fixture scrubs clean =="
tmp="$(mktemp)"
python3 layers/02-sensor/tools/pii_scrub.py \
  --rules layers/02-sensor/templates/pii-scrub-rules.json \
  --in examples/brightpath-learning/sensor/events.raw.sample.jsonl \
  --out "$tmp"
python3 layers/02-sensor/tools/pii_scrub.py \
  --rules layers/02-sensor/templates/pii-scrub-rules.json --check "$tmp"
rm -f "$tmp"

echo
echo "ALL CHECKS PASS"
