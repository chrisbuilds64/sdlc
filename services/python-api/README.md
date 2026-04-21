# services/python-api/

The Python API — the only application-level interface to Oracle Database.

## Stack

- **Framework:** FastAPI
- **Oracle driver:** `oracledb` (Thin mode — no Oracle Client installation required)
- **Container:** Docker (multi-stage build)

## Principle

This service is the single door into the database for all application code. No consumer application (mobile, web, test client) connects to Oracle directly. See [ADR-002](../../docs/adr/002-api-only-db-access.md).

## API Contract

Defined in `shared/openapi.yaml`. The OpenAPI spec is the source of truth. Code generation from the spec is preferred over manual sync.

## Planned Structure

```
python-api/
├── Dockerfile
├── requirements.txt
├── app/
│   ├── main.py
│   ├── routers/
│   ├── models/
│   └── db/
└── tests/
```

## Phase

Phase 1. Hello-world endpoint with Oracle connection is the first milestone.
