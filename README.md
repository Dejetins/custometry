# Custometry

Custometry is an open-source, self-hosted low-code platform for customer analytics and reproducible forecasting.

> Repository status: Foundation. The repository, delivery contracts, validation tools and local development topology are being established before product implementation. Reserved folders and passing static checks do not prove application runtime readiness.

The repository is permanently public. Never commit credentials, customer data, private deployment topology, raw provider payloads or environment dumps.

## Specifications

- [Machine-readable technical blueprint](./custometry-technical-blueprint-ru.md) — normative source of truth, version `0.10.0-draft`.
- [Human-readable technical blueprint](./custometry-technical-blueprint-human-ru.md) — synchronized explanatory representation.
- [UI/UX requirements](./custometry-ui-blueprint-ru.md) — product UI requirements and current surface inventory.
- [Target UI concept](./docs/architecture/ui/target-pilot/README.md) — the preserved final interactive pilot, including demonstrated composition and behavior.

If the documents diverge, the machine-readable blueprint wins. New normative requirements must first be added there and mirrored into the human-readable document.

## Architecture baseline

- modular monolith with explicit domain contracts;
- PostgreSQL as the control-plane source of truth;
- local immutable Parquet/JSON/model artifacts through `v1_target`;
- one execution engine for Guided and Pipeline modes;
- transactional outbox, at-least-once delivery, fencing, and reconciliation;
- multiple isolated workspaces in one installation;
- versioned company structure, department-scoped access/ownership, and privacy-safe contributor insights;
- English default/fallback and complete Russian localization;
- single-server Docker Compose topology through `v1_target`.

Development is contract-backed and UI-first. The previous Linear/Penpot target
and G0-G6 design program have been retired. Web work uses product requirements,
the accepted target pilot, ADR-0007, and ordinary bounded implementation tickets
under the Web implementation source contract. Current frontend code is working
implementation evidence, not automatic proof of target-concept conformance.
Each bounded context still replaces
contract-generated mocks with a real vertical slice through API,
domain/application, PostgreSQL or artifacts, and browser/runtime proof. Static
disconnected screens are not accepted as a product increment.

Start with the [architecture index](./docs/architecture/README.md). The approved Foundation direction is summarized in the [system design](./docs/architecture/system-design.md), while the [repository layout](./docs/architecture/repository-layout.md) records exact ownership paths.

## Repository areas

- `apps/` — process entrypoints and the Web application;
- `packages/` — contracts and bounded domain/application modules;
- `plugins/` — trusted connectors and extension examples;
- `migrations/` — PostgreSQL control-plane migrations;
- `deploy/` — Compose and deployment examples;
- `tests/` — unit through real-boundary verification suites;
- `docs-site/docs/` — fail-closed public Markdown source shipped by the current Foundation image;
- `docs/` — contributor architecture, ADRs, contracts, templates, runbooks, future metadata-driven user guidance, and iteration evidence;
- `.codex/` — durable agent policy, role definitions, delivery templates,
  vertical tickets, and compact evidence.

Read [AGENTS.md](./AGENTS.md) before making repository changes.

## Foundation checks

Activate the exact local toolchain before running repository commands:

```bash
scripts/bootstrap-toolchain.sh       # one time per machine/version change
source scripts/activate-toolchain.sh # every shell
```

The activation fails closed unless Node `24.18.0`, pnpm `11.13.0`, and uv
`0.9.26` are active.

The canonical grouped quality entrypoint is:

```bash
uv run --locked python -m tools.check --scope local
```

`pre-commit`, `local`, `pre-push`, `ci` and `release` are explicit evidence profiles. They are not interchangeable: release-only runtime, recovery, supply-chain and performance evidence cannot be inferred from a passing local profile. Exact tool triggers are listed in [docs/architecture/tooling-gates.md](./docs/architecture/tooling-gates.md).

## Local-first target

The first deployment target is the owner-selected Apple Silicon Mac M5 Max with 36 GB RAM, with separate Linux VM testing on the same Mac. The normal development profile has a planning ceiling of 6 GiB RAM and 25 GiB repository-owned/container data; heavier benchmark data is opt-in. Installation is download-first rather than a multi-gigabyte offline bundle: a small versioned launcher/configuration downloads pinned artifacts, validates digests and starts the stack. Web/API/data core remains usable without outbound network after dependencies and images have been acquired. The accepted Edge target is an infrastructure ingress adapter with only read-only installation TLS key/chain credentials; issuance and renewal stay outside Edge. Current HTTP Foundation code does not prove this HTTPS target. Edge remains on separate `edge_to_web`/`web_to_api` boundaries; Compose does not portably prove Edge outbound denial, so strict production enforcement is a separate target firewall/CNI hardening gate.

Foundation currently supports repository development with
`./deploy/compose/bootstrap.sh --build`. Protected `main` may publish immutable
SHA-scoped candidate images, but no accepted end-user release bundle exists yet.
`--release` is reserved for the later protected, checksummed and attested bundle flow
and fails closed without its validated manifest.
