# The n=1 / small-team memory layer: markdown + git

The same five levels, zero infrastructure. This is the cheapest place to validate the
mechanism before you build the graph/vector/document version. (A cloneable starter exists:
[personal-memory-vault-starter](https://github.com/hegu-1/personal-memory-vault-starter).)

```
vault/
├── telos/            # L4 — why this org/team exists, goals. Human-written, rarely changes.
├── knowledge/        # L3 — concepts, SOPs, policies. One file = one concept, wiki-linked.
├── projects/         # L2 — active work, settled conclusions per project.
├── log/              # L1 — daily/weekly episodic records: decisions, incidents, calibrations.
│   └── 2026-07-14.md
├── raw/              # L0 — inbox: exports, transcripts, dumps. Append-only. Consolidated upward, then archived.
└── INDEX.md          # the map — one line per file, so any new collaborator (human or AI) can orient in one read
```

Conventions that make it work (these ARE the memory-node schema, in frontmatter form):

```markdown
---
id: knowledge/escalation-policy
level: L3
authority: human_ratified        # human_authored | human_ratified | agent_inferred
provenance: {who: alex, source: "log/2026-07-01.md", why: "recurring incident pattern"}
valid_until: until_superseded
---
One concept per file. Link related nodes with [[wiki-links]] — the links are the graph.
```

- **git = provenance.** Every commit says who changed what and why. Agents commit under their own identity (①).
- **Consolidation = a weekly review**: merge duplicate notes, expire stale ones, promote settled conclusions from `log/` to `knowledge/` — a human ratifies the promotion (that's the ⑦ calibration loop, human-scale).
- **Permission scoping** at this scale = repo boundaries: a private repo per scope; don't put mixed-scope content in one repo and hope.

When retrieval by grep/wiki-links stops scaling (usually well past 10k nodes), migrate the
*same* node metadata into graph + vector stores. The schema survives the migration; that is the point.
