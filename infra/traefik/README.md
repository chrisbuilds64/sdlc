# infra/traefik/

Traefik reverse proxy configuration.

## Responsibilities

- HTTPS termination (Let's Encrypt via ACME)
- Routing to `python-api`, `ords`, and other services
- Per-environment subdomain routing (`dev.*`, `test.*`, `api.*`)

## Phase

Phase 2. Traefik is already running on the production server — configuration will be migrated here in Phase 2.
