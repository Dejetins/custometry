---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: <WORKSTREAM-VERB-NOUN>
status: draft
workstream_id: <B01-or-W00>
summary: <one complete observable behavior>
requirement_ids: [<requirement-id>]
blockers: []
# Add this mapping only while status is blocked:
# blocker_record:
#   technical_blocker: <specific technical condition>
#   evidence: [<existing-repository-local-evidence>]
#   next_safe_action: <one bounded action that does not bypass the blocker>
# Add this scalar only when status is superseded:
# supersession_reason: <why this ticket will not be accepted>
context_sources: [AGENTS.md, .codex/AGENTS.md]
# Add this mapping only when an external or volatile target is the first
# execution boundary. It is an early read-only readiness probe, not a second
# execution mode or a substitute for the pre-write guard in validation.
# start_probe:
#   boundary: <external-file-or-runtime-identity>
#   read_only_check: <smallest-permitted-check>
#   stop_on: [unavailable, identity_mismatch, state_drift]
change_scope:
  allowed_write_paths: [<exact-path-or-directory>]
  forbidden_write_paths: [<exact-path-or-directory>]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  # Historical design-tool artifacts are evidence only. For screenshot-led
  # UX/design audit, use product-design:audit. For browser runtime, component
  # catalog, or HTML candidate proof, use browser-qa-evidence.
  # Add browser-qa-evidence only when a browser surface is in scope.
  proof_skills: []
  commands: [<focused-command>]
  proof_boundary: <exact-boundary>
  evidence_target: <repository-local-evidence-path>
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

<The end-to-end behavior that is independently demonstrable.>

# Non-goals

- <Excluded scope.>

# Work and repair boundary

<Implementation seam, compatible repair allowed inside scope, and invalidated
evidence that must be rerun.>

# Acceptance evidence

<Exact checks, real-boundary observation, exclusions, and durable output.>
