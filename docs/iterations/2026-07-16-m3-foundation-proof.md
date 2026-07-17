# Custometry — M3 Pro Foundation proof

## Status and scope

- status: `accepted historical Foundation runtime proof`;
- date: `2026-07-16`, `Europe/Moscow`;
- base revision observed: `7125a90da3348df75eea24c750823d6723f2f237`;
- applicable requirement IDs: `ARCH-PRINCIPLE-001`, `DOC-RULE-008`,
  `SCALE-004`;
- proof boundary: repository Foundation on the first supported local Apple
  Silicon host.

This report retains only observed Foundation and runtime facts. Planning,
prompt-pack, ledger, and workstream-activation material from the original
preparation run was removed when Custometry adopted Global Delivery Contract
v1. The report does not authorize a current delivery unit.

## Host and runtime envelope

The proof used only non-sensitive host facts. Serial numbers, UUIDs, device
identifiers, credentials, raw environment dumps, and Docker provider payloads
were excluded.

| Surface | Observed value |
|---|---|
| Host model | `Mac15,6` |
| Processor | Apple M3 Pro, `arm64`, 11 logical CPUs |
| Memory | 18 GiB physical |
| Operating system | macOS `15.7.4` |
| Docker engine | Docker Desktop `29.6.1`, `aarch64`, 11 CPUs, 7.75 GiB runtime capacity |
| Python | `3.12.2` through the locked uv workspace |
| Node | `24.18.0` |
| pnpm | `11.13.0` through Corepack |
| uv | `0.9.26` |
| Foundation Compose budget | 2.938 GiB declared aggregate memory, below the 6 GiB policy |
| Repository-owned disk | 0.428 GiB observed by doctor |

## Reproducible tool activation

The repository bootstrap and shell activation selected the pinned Node, pnpm,
uv, and Python environments and failed closed on incompatible ambient tools.
Git hooks used the same activation wrapper. This observation proves the tested
host path only; it does not establish every operating system or architecture.

## Source and runtime observations

The accepted run observed:

- locked toolchain bootstrap;
- Ruff success, Pyright with zero errors, Python tests, strict MkDocs build,
  pnpm lint/typecheck/tests, and a production Web build;
- runtime doctor success with the recorded CPU and memory envelope;
- an empty/upgrade/repeat/downgrade/re-upgrade PostgreSQL migration lifecycle;
- a six-service Compose lifecycle with loopback Edge publication,
  Edge-to-Web success, Edge-to-API denial, and negative egress probes for Web
  and API;
- five real browser journeys, including public documentation;
- cleanup with no remaining `custometry-ci-*` containers, volumes, or networks.

Foreign Docker resources were neither stopped nor removed. Generated ignored
build and browser artifacts were removed after the proof.

## Acceptance boundary and exclusions

The evidence accepts the Foundation runtime boundary that was actually
observed. It does not claim:

- product analytics, forecasting, reporting, identity, or other feature
  implementation;
- a published immutable release, final installer, SBOM/provenance, recovery,
  performance, or production firewall/CNI acceptance;
- canonical Penpot ownership or authority;
- freshness for the current repository tree.

Future tickets must rerun every boundary affected by their change. This
historical receipt may establish prior context, but it cannot substitute for a
current test, browser, Compose, recovery, performance, CI, or release result.
