#!/usr/bin/env python3
"""Risk-tier gate — zero dependencies, python3 stdlib only.

Decide the gate for an action against a risk-tier policy (templates/risk-tier-policy.json).

    tier = max(blast_radius_score, sensitivity_score)          # clamped T0..T3
    if irreversible: tier = max(tier, irreversible_floor)      # a human must ratify; floor, not bump
    explicit rules may RAISE the tier or force a gate; they can never lower it

Usage:
    # one action -> prints tier + gate
    python3 risk_gate.py --policy policy.json --action action.json

    # CI: run a policy's test cases; exit 1 on any mismatch
    python3 risk_gate.py --policy policy.json --cases gate-cases.json

action.json shape:
    {"action": "billing.issue_refund", "blast_radius": "external",
     "data_sensitivity": "regulated", "reversible": false}
"""
import argparse
import fnmatch
import json
import sys


def decide(policy, action):
    dims = policy["dimensions"]
    br = dims["blast_radius"][action["blast_radius"]]
    sens = dims["data_sensitivity"][action["data_sensitivity"]]
    score = max(br, sens)
    if not action.get("reversible", True):
        score = max(score, dims.get("irreversible_floor", 2))
    score = min(score, 3)
    tier = f"T{score}"
    gate = policy["tier_gates"][tier]
    why = [f"computed {tier} (blast={action['blast_radius']}, sensitivity={action['data_sensitivity']}, reversible={action.get('reversible', True)})"]

    for rule in policy.get("rules", []):
        if fnmatch.fnmatch(action["action"], rule["match_action"]):
            if "gate" in rule:
                gate, tier = rule["gate"], tier
                why.append(f"rule '{rule['match_action']}' forces gate={rule['gate']}: {rule.get('why', '')}")
            elif "min_tier" in rule and rule["min_tier"] > tier:
                tier = rule["min_tier"]
                gate = policy["tier_gates"][tier]
                why.append(f"rule '{rule['match_action']}' raises to {tier}: {rule.get('why', '')}")

    return {"tier": tier, "gate": gate, "why": "; ".join(why)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--action", help="single action JSON file")
    ap.add_argument("--cases", help="test-cases JSON file: [{action: {...}, expect_gate: ...}]")
    args = ap.parse_args()

    with open(args.policy, "r", encoding="utf-8") as f:
        policy = json.load(f)

    if args.action:
        with open(args.action, "r", encoding="utf-8") as f:
            result = decide(policy, json.load(f))
        print(json.dumps(result, indent=2))
        return

    if args.cases:
        with open(args.cases, "r", encoding="utf-8") as f:
            cases = json.load(f)["cases"]
        failed = 0
        for i, case in enumerate(cases, 1):
            result = decide(policy, case["action"])
            ok = result["gate"] == case["expect_gate"] and (
                "expect_tier" not in case or result["tier"] == case["expect_tier"]
            )
            status = "ok" if ok else "FAIL"
            if not ok:
                failed += 1
            print(
                f"{status}  case {i}: {case['action']['action']} -> {result['tier']}/{result['gate']}"
                + ("" if ok else f"  (expected {case.get('expect_tier', '*')}/{case['expect_gate']})")
            )
        if failed:
            print(f"FAIL: {failed}/{len(cases)} case(s) mismatched", file=sys.stderr)
            sys.exit(1)
        print(f"OK: {len(cases)} gate case(s) pass")
        return

    ap.error("need --action or --cases")


if __name__ == "__main__":
    main()
