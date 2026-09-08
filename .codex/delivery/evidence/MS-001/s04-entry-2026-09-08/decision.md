# MS-001/DEC-13 — S04 environment preparation

Date: 2026-09-08. Covered plan: [MS-001 2.2.0](../../../../../docs/architecture/planning/milestones/MS-001/plan.md).
The owner accepted moving AMD64 environment/CI and exact-bundle transfer preparation
inside S04, keeping native ARM64/AMD64 checks mandatory for completion, preserving
accepted S03, and updating the necessary documents and next-entry permission.
The current request is document preparation; it does not execute S04 or broaden
remote publication, credential or audience authority.

The earlier S03 handoff left S04 disallowed while AMD64 availability was unverified.
DEC-13 supersedes that entry reservation only. The missing consumer job/transfer is
an S04 output to prepare using the existing target, not an owner-supplied entry file.
Actual runtime/transfer evidence is still required for S04 acceptance and S05 entry.

## Mapping and preservation

- Plan 2.1.0 -> 2.2.0 adds compatible execution detail within the same result,
  platform, trust and resource boundaries. All existing acceptance IDs remain.
- Unclaimed S04/S05 keep their IDs; their current contracts and plan bindings change.
- S01/S02 retain the 1.1.0 basis. S03 retains its exact contract, prompt, report,
  receipt, claim metadata and transitions against [plan 2.1.0](plan-2.1.0.md.snapshot).
- The existing exclusive updater owns reconciliation and subsequent `advance`.
  No stage is claimed, rerun or accepted by this document update.
- WS-001 changes only its navigation version to 1.0.6; L1/L2 and product requirements
  remain unchanged. S03 code, runtime/tooling docs, local artifacts and foreign edits
  are preserved.

## Entry observations

Read-only inspection found accepted S03 and unclaimed pending S04/S05.
`Pack.entry("MS-001-S04", require_allowed=False)` passed before the amendment:
accepted dependency bindings and current entry files were valid. The local final
manifest SHA-256 is `693cbe3b4dfcd5148c9aab6dd2b1e946d9b46ae0ce3c22a69b4a03111f1a735a`;
the six retained image archives and independent reader are present. Archive
integrity/runtime results are reused only at the boundary of the accepted S03 report;
this entry inspection does not rehash all archives or prove consumer runtime.

The next entry may be enabled after amended triad validation and independent review.
Use `advance` with this decision and the current ledger digest, then read-only
S04 preflight. S04 remains `pending`/unclaimed and S05 remains disallowed.
No native AMD64 proof is asserted until S04 actually collects it.

[Validation and independent review](checks.md).
