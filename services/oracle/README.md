# services/oracle/

Oracle Database 23ai — schema, migrations, and seed data.

## Approach

Migration-based deployment using **Liquibase** via **Oracle SQLcl**.

Two categories of database objects:

| Type | Examples | Deployment |
|---|---|---|
| Stateful (run once) | Tables, indexes, sequences, constraints | `releases/YYYY.MM/` — versioned, never modified |
| Stateless (repeatable) | Packages, procedures, views, triggers | `packages/`, `views/` etc. — `CREATE OR REPLACE` on every deploy |

## Planned Structure

```
oracle/
├── controller.xml          # Master Liquibase changelog
├── liquibase.properties    # Connection config (per environment via env vars)
├── releases/               # Versioned, immutable changesets (DDL, migrations)
│   └── 2026.01/
├── packages/               # PL/SQL packages (idempotent)
├── views/
├── triggers/
├── seed/                   # Reference data
└── tests/                  # utPLSQL test packages
```

## Local Development

Oracle Database 23ai Free runs locally via Docker:
```
container-registry.oracle.com/database/free:latest-lite
```
Native ARM64 images available for Apple Silicon (announced Nov 2024).

## Phase

Phase 1.
