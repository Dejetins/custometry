---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W11-HYBRID-DEVELOPMENT-RUNTIME
proof_boundary: local-hybrid-development-runtime-lifecycle-and-release-isolation
proof_skills: []
verdict: passed
redaction: No credentials, DSNs, raw runtime logs, or environment dumps are retained; resource identities and observations are bounded to the repository-owned Hybrid project.
executed_checks:
  - docker context show && docker compose version && docker info
  - docker context ls and selected/default engine ID comparison
  - source scripts/activate-toolchain.sh
  - bash -n scripts/dev
  - docker compose -f compose.yaml -f compose.dev.yaml config
  - uv run --locked pytest -q tests/tooling/test_development_runtime.py tests/integration/test_development_runtime.py
  - uv run --locked pytest -q
  - scripts/dev validate
  - run scripts/dev validate with an unavailable NVM directory
  - scripts/dev up --mode hybrid
  - scripts/dev status
  - repeat scripts/dev up --mode hybrid and compare owned API/Web PIDs
  - query both loopback PostgreSQL endpoints and host API/Web readiness
  - scripts/dev logs and verify byte bound, redaction marker, and absence of runtime secret values
  - stop the owned Web process group, observe degraded, and recover through scripts/dev up --mode hybrid
  - run scripts/dev status with an unreachable temporary DOCKER_HOST and observe unavailable
  - reject missing and incorrect reset confirmations and a target-selector attempt
  - create isolated control/demo markers and run scripts/dev reset-demo --confirm RESET-DEMO
  - scripts/dev down and inspect owned processes, containers, networks, runtime state, secrets, and persistent volumes
  - restart from preserved volumes with fresh temporary secrets, remove the control proof marker, and stop cleanly
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.check --scope local
  - uv run python -m tools.check --scope pre-push
  - git diff --check
observations:
  - Docker context desktop-linux and Compose v5.3.0 reached one Docker Desktop engine; default and desktop-linux resolved to the same engine ID and Colima was not running.
  - The repository-specific project custometry-hybrid-383a7390af published control PostgreSQL on 127.0.0.1:55432 and demo PostgreSQL on 127.0.0.1:55433 through separate labelled volumes and networks.
  - Host SQL queries, control migration, API readiness on 127.0.0.1:8000, and Web readiness on 127.0.0.1:5173 succeeded.
  - Repeated up reused the same owned API and Web PIDs; an intentionally stopped owned Web group produced degraded and a safe restart returned healthy.
  - An unreachable temporary Docker endpoint produced unavailable without stopping or changing the real engine.
  - Bounded logs were 3478 bytes and 53 lines in the observed run; injected fake token content and all actual runtime secret values were absent from rendered output.
  - Missing confirmation, incorrect confirmation, and an unsupported volume selector returned failure while both volume identities remained unchanged.
  - Confirmed demo reset recreated only the demo volume and removed the demo marker; the control volume and marker were preserved until the marker was explicitly removed after proof.
  - Restart from preserved volumes succeeded after file-backed credential synchronization through container stdin; credentials were absent from process arguments and retained output.
  - Final down left no owned host processes, containers, networks, runtime logs, state, or temporary secret files; separate control and demo volumes remained according to policy.
  - Static validation remained available without Node/NVM because it requires only the pinned Python toolchain; full host toolchain activation remains mandatory for up.
  - Focused tests passed 14 tests, the full suite passed 123 tests, and local plus pre-push grouped profiles passed.
---

# W11 Hybrid Development Runtime Evidence

## Outcome and scope

- outcome: contributors can run host API and Web processes against two
  repository-owned loopback PostgreSQL services through one deterministic
  Hybrid lifecycle without rebuilding application images;
- requirement IDs: [ARCH-PRINCIPLE-001, DOC-RULE-008];
- included: Hybrid Compose override, project/resource identity, host-process
  ownership, migrations, readiness, idempotent startup, status classes,
  bounded redacted logs, safe demo reset, persistent restart, release-path
  exclusion, and cleanup postconditions;
- exclusions: no product browser acceptance, production firewall/CNI, Full
  Stack runtime, immutable release, deployment, recovery, performance, or
  external-environment proof.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
|---|---|---|
| Docker start probe | pass | One selected Docker Desktop engine through `desktop-linux`; Compose v5.3.0. |
| `scripts/dev validate` and development static gate in grouped profiles | pass | Validation remained available without Node/NVM; loopback ports, separate volumes, exact reset target, bounded logging contract, and release-entrypoint exclusion passed. |
| Fresh `scripts/dev up --mode hybrid` | pass | Both PostgreSQL services, migration, owned API, and owned Web reached `overall=healthy`. |
| Host SQL and HTTP readiness | pass | Both loopback databases answered `select 1`; API and Web returned HTTP 200. |
| Repeated `up` | pass | API/Web PIDs were reused and no duplicate process groups or containers appeared. |
| Status behavior | pass | Observed healthy, controlled degraded, recovered healthy, and unavailable through a non-existent Docker endpoint. |
| Bounded logs | pass | 3478 bytes/53 lines observed; fake token and actual runtime secrets absent. |
| Reset negative cases | pass | Missing/wrong confirmation and target selection were rejected without changing either volume identity. |
| Confirmed demo reset | pass | Demo volume recreated and demo marker removed; control volume and marker preserved. |
| Persistent restart | pass | Fresh secret files were synchronized through container stdin and preserved data reopened successfully. |
| Final `down` | pass | No owned processes, containers, networks, state, logs, or secret files remained; control/demo volumes were preserved. |
| Focused and full tests | pass | 14 focused tests and 123 repository tests passed. |
| Repository gates | pass | Delivery-ticket validator, local profile, pre-push profile, docs index/links, and `git diff --check` passed. |

## Verdict

`passed` at `local-hybrid-development-runtime-lifecycle-and-release-isolation`.
The result is limited to the local Docker Desktop/host boundary. Release,
deployment, production security, browser-product behavior, recovery, and
performance remain unverified and require their own tickets and evidence.
