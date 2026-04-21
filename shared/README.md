# shared/

Shared artifacts consumed by multiple layers of the stack.

## Contents

- `openapi.yaml` — API contract between the Python API and all consumers. Single source of truth. Coming in Phase 1.

## Principle

The OpenAPI spec is written first, not generated from code. The contract defines what the API does. The implementation follows.
