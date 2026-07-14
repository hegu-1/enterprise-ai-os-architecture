# Environments & secrets policy (template)

Copy this file, replace the placeholder names, and commit it to your infra repo.

## Environment separation

| | dev | staging | prod |
|---|---|---|---|
| Purpose | build & break | rehearse with prod-shaped data | real actions, real users |
| Data | synthetic only | **masked** copies of prod (PII scrubbed at copy time, see ②) | real |
| Agent autonomy | anything | dry-run by default; actions logged, not executed | governed by ⑦ risk tiers |
| Model access | cheap/small models | same routing config as prod | full routing (④) |
| Who can deploy | any engineer | any engineer, after checks pass | release role only |

Rules:

1. **Agents in dev/staging can never reach prod tools or prod memory.** Enforce at network/credential level, not by convention.
2. **Staging runs the same configs as prod** (routing, policies, RBAC) with different credentials — otherwise it rehearses nothing.
3. **Dry-run is a first-class mode.** Every action-taking agent must support `dry_run: true` where it logs the action it *would* take. This is the single cheapest safety mechanism in the whole stack.

## Secrets

- All credentials live in a secrets manager (`<your-secrets-manager>`), scoped per environment and per principal.
- No secret ever appears in: source code, config committed to git, prompts, agent memory (③), or logs.
- Rotation: `<90 days>` for service credentials; immediately on any suspected exposure.
- Break-glass: `<named role>` can revoke all agent credentials in one action; rehearse this quarterly.
