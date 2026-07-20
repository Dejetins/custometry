---
doc_id: RUNBOOK-DEVELOPMENT-RUNTIME-001
title: Hybrid development runtime operations
doc_version: 1
product_spec_version: 0.9.3-draft
visibility: internal
ship: false
owner: devops
requirement_ids: [ARCH-PRINCIPLE-001, DOC-RULE-008]
status: active
proof_boundary:
  label: hybrid-development-runtime-operations
  exclusions: [production-runtime, release-readiness, browser-product-acceptance]
---

# Hybrid Development Runtime Operations

## Preconditions

- Use exactly one selected Docker engine and context.
- Source `scripts/activate-toolchain.sh` before direct quality commands.
- Stop if ports `55432`, `55433`, `8000`, or `5173` belong to a foreign process.
- Do not copy secret files, DSNs, raw logs, or `.runtime/` state into evidence.

## Start and inspect

```bash
scripts/dev validate
scripts/dev up --mode hybrid
scripts/dev status
scripts/dev logs
```

`up` starts only the repository-owned control and demo PostgreSQL services,
runs control migrations from the host after both loopback ports are visible,
and starts owned API and Web process groups. When preserved volumes meet newly
generated temporary secret files,
the launcher synchronizes the owned database roles from mounted files through
container stdin without placing credentials in process arguments or logs. A
repeated `up` reuses the same healthy resources and processes.

`status` reports `healthy`, `degraded`, or `unavailable` for infrastructure and
host processes. Treat `degraded` as incomplete capability evidence and
`unavailable` as a failed runtime boundary; neither may be reported as passed.

## Bounded diagnostics

```bash
scripts/dev logs api
scripts/dev logs web
scripts/dev logs control-db
scripts/dev logs demo-source-db
```

Output is tail-bounded and redacts password-, secret-, token-, and DSN-shaped
values. Raw files under `.runtime/development/` are disposable local state, not
durable evidence.

## Demo reset

An absent or incorrect confirmation changes nothing:

```bash
scripts/dev reset-demo
scripts/dev reset-demo --confirm WRONG
```

The only destructive form is:

```bash
scripts/dev reset-demo --confirm RESET-DEMO
```

The command accepts no volume selector. It inspects the exact expected demo
volume and requires the W11 owner, Hybrid runtime, demo data-role, Compose
project, and Compose volume labels before removing it. The control volume is
never a valid target.

## Stop and persistence

```bash
scripts/dev down
```

`down` terminates only process groups whose PID, process-group ID, start time,
and observed command still match recorded ownership. It removes owned
containers, networks, runtime logs, process state, and temporary secret files.
The separate control and demo data volumes are preserved. Use the confirmed
demo reset command when demo data must be recreated; this runbook grants no
authority to delete control data or foreign Docker resources.
Runtime creation and cleanup fail closed when `.runtime`, its development
subtree, state, or secret paths are symbolic links or escape the repository.

## Verification and escalation

After stopping, verify that no project containers or networks remain, no owned
host processes are alive, and no temporary secret files exist. Escalate rather
than cleaning up when an identity or ownership label differs, a port is foreign,
Docker contexts are ambiguous, or a requested action crosses production,
release, or non-W11 data.
