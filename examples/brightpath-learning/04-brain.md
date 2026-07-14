# BrightPath ④ Brain

> Template: [`layers/04-brain/`](../../layers/04-brain/README.md) · Everything fictional.

## Routing

Two rented model tiers (`small`, `large`) plus the rule layer. No in-house models — at 45
people, "internal_only" maps to "don't send it to a model at all":

```json
{
  "sensitivity_constraints": {
    "public":       ["rules", "small", "large"],
    "internal":     ["rules", "small", "large"],
    "confidential": ["rules", "small", "large"],
    "regulated":    ["rules"]
  },
  "routes": [
    {"task": "classify.ticket",    "prefer": "rules", "fallback": "small", "cache": true},
    {"task": "draft.reply",        "prefer": "small", "fallback": "large", "cache": false},
    {"task": "qa.course_module",   "prefer": "large", "fallback": null,    "cache": false},
    {"task": "reconcile.billing",  "prefer": "rules", "fallback": null,    "cache": false,
     "note": "regulated: reconciliation is pure rules — amounts and dates never reach an external model"}
  ]
}
```

The rule layer settles ~60% of ticket classification (keyword + learner-state lookup) before
any model is called — measured weekly, because that number *is* the cost model.

## Eval gate

`bp-evals` has three suites built from scrubbed production events (②): `classify-ticket`
(320 cases), `draft-reply` (rubric-graded, 60 cases), `qa-module` (24 cases). CI runs them on
every routing/prompt change; the sensitivity gate includes four canary "card-number-shaped"
records that must route to `rules` — one escape fails the build.

Weekly drift check runs the same suites unchanged. In April (fictional), the drift check
caught a vendor model update that dropped draft-reply rubric scores by 11% — routing flipped
the fallback order the same day, which is the whole argument for never hardcoding a vendor.
