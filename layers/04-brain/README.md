# ④ Brain — models · routing · adaptation · eval

> Position: the layer everyone stares at, and the fastest to commoditize. **You rent most of this.**
> The craft is in routing and adaptation. The real differentiation is not the model — it's the context ③ feeds it.

## What this layer must provide

- **A model pool, hot-swappable** — external APIs + any in-house/fine-tuned models, behind one interface. No agent code names a vendor directly.
- **A router** — picks the model per task by capability floor, cost, latency, and **data sensitivity** (regulated data never routes to an external endpoint — enforced here, audited by ⑦). See [`templates/model-routing.json`](templates/model-routing.json).
- **A rule layer in front of models** — deterministic checks (regex, lookup, threshold) run *before* any model call. Don't send trivial work to a large model; don't send any work to a model that a rule can settle.
- **Domain adaptation where it pays** — fine-tunes/adapters for narrow, high-volume tasks; measured against the base model quarterly (adapters rot).
- **Inference caching** — semantic-duplicate requests hit cache, not the API.
- **An eval harness** — every routing change and every adapter ships with before/after scores on a fixed task suite; see [`templates/eval-suite.md`](templates/eval-suite.md).

## The one rule that matters

**Route by sensitivity first, capability second, cost third.** A cheaper model that leaks
regulated data to an external endpoint is not cheaper. Sensitivity routing is a hard
constraint, not a weight in a scoring function.

## Failure modes

- **Everything routes to the biggest model** — slow, expensive, and it hides the fact that nobody understands the task taxonomy.
- **Fine-tunes overfit or catastrophically forget** — always keep the base-model fallback wired.
- **Sensitive data flows out** — the router is the enforcement point; if routing config isn't reviewed like security config, it will drift.
- **Eval theater** — a static leaderboard nobody gates deploys on. The eval suite must be a deploy gate, or it's decoration.

## Templates in this directory

- [`templates/model-routing.json`](templates/model-routing.json) — routing table: task class × sensitivity → model tier, with hard sensitivity constraints and cache policy.
- [`templates/eval-suite.md`](templates/eval-suite.md) — the minimum eval harness: task suites, gates, drift checks.

## Acceptance checklist

- [ ] No agent code references a concrete model/vendor; all calls go through the router.
- [ ] Sensitivity classes are defined and the router enforces them as hard constraints (test with a canary regulated-data task).
- [ ] A rule layer exists and its hit-rate is measured (rules resolving work = model calls saved).
- [ ] Every routing/adapter change passes the eval gate before deploy.
- [ ] Cost per task class is attributed and reviewed monthly.

**Worked examples:** [BrightPath routing](../../examples/brightpath-learning/04-brain.md) · [Meridian](../../examples/meridian-freight/README.md)
