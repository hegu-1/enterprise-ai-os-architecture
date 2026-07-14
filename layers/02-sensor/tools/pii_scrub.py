#!/usr/bin/env python3
"""Entry-time PII scrubber — zero dependencies, python3 stdlib only.

Modes:
  scrub:  --rules rules.json --in raw.jsonl --out clean.jsonl
  check:  --rules rules.json --check clean.jsonl        (CI gate: exit 1 if any PII pattern matches)

Events are JSONL, one event envelope per line (see templates/event.schema.json).
Only string values inside the fields listed in the rules file's `scrub_fields`
are scrubbed/checked; the envelope itself is expected to be PII-free by design.
"""
import argparse
import json
import re
import sys


def load_rules(path):
    with open(path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    return [
        (r["name"], re.compile(r["pattern"]), r["replace"]) for r in spec["rules"]
    ], spec.get("scrub_fields", ["payload"])


def walk_strings(obj, fn):
    """Apply fn to every string in a nested dict/list; return new structure."""
    if isinstance(obj, str):
        return fn(obj)
    if isinstance(obj, dict):
        return {k: walk_strings(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk_strings(v, fn) for v in obj]
    return obj


def scrub_event(event, rules, fields):
    hits = []

    def scrub_str(s):
        for name, pat, repl in rules:
            s, n = pat.subn(repl, s)
            if n:
                hits.append((name, n))
        return s

    for field in fields:
        if field in event:
            event[field] = walk_strings(event[field], scrub_str)
    event["pii_scrubbed"] = True
    return event, hits


def find_pii(event, rules, fields):
    found = []

    def check_str(s):
        for name, pat, _ in rules:
            if pat.search(s):
                found.append(name)
        return s

    for field in fields:
        if field in event:
            walk_strings(event[field], check_str)
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--in", dest="infile")
    ap.add_argument("--out", dest="outfile")
    ap.add_argument("--check", help="file to verify is clean; exit 1 on any hit")
    args = ap.parse_args()

    rules, fields = load_rules(args.rules)

    if args.check:
        dirty = 0
        with open(args.check, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                if not line.strip():
                    continue
                event = json.loads(line)
                found = find_pii(event, rules, fields)
                if found:
                    dirty += 1
                    print(f"DIRTY line {lineno}: matches {sorted(set(found))}", file=sys.stderr)
        if dirty:
            print(f"FAIL: {dirty} event(s) contain PII patterns", file=sys.stderr)
            sys.exit(1)
        print(f"OK: {args.check} is clean")
        return

    if not (args.infile and args.outfile):
        ap.error("need --in and --out for scrub mode, or --check for check mode")

    total = scrubbed = 0
    with open(args.infile, "r", encoding="utf-8") as fin, open(
        args.outfile, "w", encoding="utf-8"
    ) as fout:
        for line in fin:
            if not line.strip():
                continue
            total += 1
            event, hits = scrub_event(json.loads(line), rules, fields)
            if hits:
                scrubbed += 1
            fout.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(f"OK: {total} events, {scrubbed} contained PII and were scrubbed -> {args.outfile}")


if __name__ == "__main__":
    main()
