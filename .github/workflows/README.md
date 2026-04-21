# .github/workflows/

CI/CD pipelines.

Planned pipelines:
- `deploy-dev.yml` — triggered on push to `develop`, deploys to Dev environment
- `deploy-test.yml` — triggered on push to `release/*`, deploys to Test environment
- `deploy-prod.yml` — triggered manually after tag on `main`, deploys to Prod (with approval gate)

See [ADR-003](../../docs/adr/003-environment-strategy.md) for environment and branching strategy.

## Phase

Phase 2.
