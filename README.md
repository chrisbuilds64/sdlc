# chrisbuilds64/sdlc — ARCHIVED

**This repository was dissolved into [chrisbuilds64/develop](https://github.com/chrisbuilds64/develop) on 2026-07-19.**

The experiment of running a separate public "reference stack" next to the real development system created two competing worlds. The real one won. There is now one development system, governed by one canon, in one place.

## Where things went

| Asset | New home |
|---|---|
| Oracle 26ai automation (3 PDBs Dev/Test/Prod, Liquibase) | `develop/infra/ansible/oracle.yml` + `develop/services/oracle/` |
| APEX/ORDS playbooks and compose | `develop/infra/ansible/apex.yml`, `develop/services/oracle/` |
| Order-management teaching schema (PL/SQL) | `develop/services/oracle/test-schema/` |
| ADRs 001-004 | `develop/docs/adr/ADR-002..005` (renumbered, provenance noted) |
| Evolved Ansible set (foundation, monitoring, verify) | `develop/infra/ansible/` |

Not migrated, preserved here in history: the Traefik playbook (Caddy is what actually runs) and the PL/SQL vector-RAG pipeline (no longer relevant to the current direction).

This repo stays readable as build-in-public history: everything here was really built, really deployed, and really debugged. It just lives somewhere better now.

MIT License.
