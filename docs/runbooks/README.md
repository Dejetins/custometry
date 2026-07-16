# Runbooks

Versioned runbooks describe a specific user-impacting operational failure and safe recovery. A runbook is created with the implementation that introduces the failure mode, metric/alert or recovery action; an empty placeholder does not prove operations readiness.

A new document is created from the [runbook template](./runbook-template.md).

Current operational runbooks:

- [GitHub repository governance](./github-repository-governance.md) — application,
  verification, and safe recovery of the protected-main, squash-only policy.

Each runbook contains:

- stable ID, owner, scope, supported versions and last review;
- symptoms and exact alert/trigger;
- impact and affected roles/workspaces without leaking protected resources;
- safe prerequisites and evidence to collect with redaction;
- diagnosis decision tree;
- bounded mitigation and rollback;
- verification/post-conditions;
- escalation/stop conditions;
- recovery data integrity checks;
- links to metrics, logs schema and related ADR/contracts.

Commands must be non-destructive by default. Secret/PII values and raw provider payloads never enter examples or captured evidence. An operator/admin runbook is `authenticated`; contributor-only implementation notes remain `internal`.

Recovery release acceptance requires an observed drill. Review of this Markdown alone is not evidence that backup or restore works.
