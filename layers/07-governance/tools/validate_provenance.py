#!/usr/bin/env python3
"""Provenance audit-log validator — zero dependencies, python3 stdlib only.

Usage:
    python3 validate_provenance.py audit-log.jsonl [more.jsonl ...]

Validates every record against the provenance schema's required fields AND the
cross-field rules that make an audit trail mean something:

  R1  actor.kind == agent      => actor.on_behalf_of present (delegation chain)
  R2  risk_tier in {T0, T1}    => reversible is true
  R3  risk_tier == T2          => gate.mode in {human_ratify, multi_party}, >=1 approver
  R4  risk_tier == T3          => multi_party with >=2 DISTINCT approvers, or capability_token
  R5  gate.mode valid enum; risk_tier valid enum; ts is ISO 8601

Exit code 0 = all records pass; 1 = violations found (listed on stderr).
"""
import json
import sys
from datetime import datetime

REQUIRED = ["record_id", "ts", "actor", "action", "target", "origin", "risk_tier", "gate", "reversible"]
TIERS = {"T0", "T1", "T2", "T3"}
GATES = {"auto", "auto_with_review", "human_ratify", "multi_party", "forbid"}


def check_record(rec, where):
    errs = []
    for field in REQUIRED:
        if field not in rec:
            errs.append(f"missing required field '{field}'")
    if errs:
        return [f"{where}: {e}" for e in errs]

    actor, gate, tier = rec["actor"], rec["gate"], rec["risk_tier"]

    if tier not in TIERS:
        errs.append(f"invalid risk_tier '{tier}'")
    if gate.get("mode") not in GATES:
        errs.append(f"invalid gate.mode '{gate.get('mode')}'")
    try:
        datetime.fromisoformat(rec["ts"].replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        errs.append(f"ts '{rec['ts']}' is not ISO 8601")

    if actor.get("kind") == "agent" and not actor.get("on_behalf_of"):
        errs.append("R1: agent actor without on_behalf_of — delegation chain broken")
    if actor.get("kind") not in ("human", "agent"):
        errs.append(f"invalid actor.kind '{actor.get('kind')}'")

    # Refused (gate.mode=forbid) and simulated (dry_run) actions are logged too,
    # but nothing executed — approval-consistency rules R2-R4 don't apply to them.
    executed = gate.get("mode") != "forbid" and not rec.get("dry_run", False)

    if executed and tier in ("T0", "T1") and rec["reversible"] is not True:
        errs.append(f"R2: {tier} action marked irreversible — irreversible is T2 minimum")

    approvers = gate.get("approved_by", [])
    if executed and tier == "T2":
        if gate.get("mode") not in ("human_ratify", "multi_party") or len(approvers) < 1:
            errs.append("R3: T2 requires human_ratify/multi_party with >=1 approver")
    if executed and tier == "T3":
        token = gate.get("capability_token")
        distinct = len(set(approvers))
        if not token and not (gate.get("mode") == "multi_party" and distinct >= 2):
            errs.append("R4: T3 requires multi_party with >=2 distinct approvers or a capability_token")

    return [f"{where}: {e}" for e in errs]


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)

    violations, total = [], 0
    for path in sys.argv[1:]:
        with open(path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                if not line.strip():
                    continue
                total += 1
                where = f"{path}:{lineno}"
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError as e:
                    violations.append(f"{where}: invalid JSON ({e})")
                    continue
                violations.extend(check_record(rec, where))

    if violations:
        for v in violations:
            print(f"VIOLATION {v}", file=sys.stderr)
        print(f"FAIL: {len(violations)} violation(s) in {total} record(s)", file=sys.stderr)
        sys.exit(1)
    print(f"OK: {total} provenance record(s) valid")


if __name__ == "__main__":
    main()
