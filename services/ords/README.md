# services/ords/

Oracle REST Data Services (ORDS) — configuration and static files.

## Role

ORDS is an infrastructure component, not an application-level API. It serves:
- APEX applications (PL/SQL Gateway + static file server)
- Oracle-native REST endpoints (REST-enabled SQL)

Application code accesses data exclusively through the Python API. See [ADR-002](../../docs/adr/002-api-only-db-access.md) and [ADR-004](../../docs/adr/004-ords-separate-container.md).

## Deployment

ORDS runs as a dedicated Docker container. Configuration is managed here and mounted at runtime.

## Phase

Phase 1.
