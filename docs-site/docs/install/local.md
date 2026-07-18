---
doc_id: install-local
title: Local development installation
doc_version: 2
product_spec_version: 0.9.1-draft
locale: en
visibility: public
ship: true
audiences: [installer]
route: /docs/install/local/
status: active
owner: product-documentation
requirement_ids: [HELP-001, HELP-003, HELP-004]
proof_boundary:
  label: foundation-local-installation-guide
  exclusions: [release-artifact-acceptance, production-deployment-readiness]
reviewed_at: "2026-07-16"
---
# Local development installation

Foundation does not yet publish an accepted end-user release bundle. The currently
supported path is a repository development installation that builds the pinned source
checkout with Docker Compose. Passing candidate-image publication on protected `main`
does not make those images an installable release.

## Requirements

- Apple Silicon MacBook is the first development target;
- Docker Desktop or one compatible Docker engine;
- at least 6 GiB available to the container engine and 25 GiB free owned disk space;
- `bash`, `curl`, `openssl`, and `python3` on the host.

## Start from the repository

From the repository root:

```bash
./deploy/compose/bootstrap.sh --build
```

The bootstrap command:

1. verifies that one Docker engine is reachable;
2. chooses a free loopback port and stores it in an ignored runtime environment file;
3. creates local secret files with restrictive permissions;
4. builds the API and Web images from the current tracked checkout;
5. starts PostgreSQL and runs the explicit migration job;
6. starts the API and Web services and verifies readiness.

Add `--with-demo` to start the separate deterministic retail source database.

## Reserved release mode

`--release` is a fail-closed contract for a future protected, versioned, checksummed
and attested release bundle. Do not construct `.release.env` manually. Until the
release workflow produces and accepts the complete bundle, the end-user release path
is unavailable by design.

## Find the local URL

```bash
./deploy/compose/bootstrap.sh --print-url
```

Only the selected loopback HTTP port is published. PostgreSQL is not exposed to the host.
