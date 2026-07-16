---
doc_id: RUNBOOK-GITHUB-GOVERNANCE-001
title: GitHub repository governance
doc_version: 2
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: engineering-productivity
requirement_ids: [DOC-RULE-008]
status: accepted
proof_boundary:
  label: github-repository-policy
  exclusions: [github-availability, ci-run-success, collaborator-identity]
---

# GitHub repository governance

## Purpose and scope

This runbook applies the accepted public-repository policy to
`Dejetins/custometry`. The source-of-truth payloads are:

- [repository settings](../../.github/repository-settings.json);
- [main branch protection](../../.github/branch-protection-main.json).

The policy keeps the repository public, permits only squash merges, deletes merged
branches, and protects `main` with a current-branch CI requirement, linear history,
resolved conversations, and protection from force-push or deletion. The approval count
is deliberately zero while the repository has a single owner: the PR and required CI
remain mandatory without creating an impossible self-approval rule. Increase the count
only after a second accountable reviewer exists.

`publish-candidates.yml` is deliberately a protected-`main` workflow rather than a
release workflow. It repeats the Foundation gate, grants `packages: write` only to the
two image jobs, publishes SHA-scoped candidate images, and records the actual digests in
the workflow summary. It has no manual or tag trigger and produces no installer
manifest. A candidate is not an accepted end-user release.

## Preconditions

1. `gh auth status` identifies an administrator of `Dejetins/custometry`.
2. The repository is public and its default branch is `main`.
3. `.github/workflows/ci.yml` exposes exactly one aggregate job named
   `Foundation gate` on pull requests.
4. The working tree payloads were reviewed; commands below read them and do not generate
   replacements.

Never print authentication tokens or copy them into evidence.

## Apply

Run from the repository root:

```bash
gh api --method PATCH repos/Dejetins/custometry \
  --input .github/repository-settings.json

gh api --method PUT repos/Dejetins/custometry/branches/main/protection \
  --input .github/branch-protection-main.json
```

The operation changes GitHub-hosted policy only. It does not push local content, create a
branch, or make a release.

## Verify

```bash
gh api repos/Dejetins/custometry \
  --jq '{visibility,default_branch,allow_merge_commit,allow_squash_merge,allow_rebase_merge,delete_branch_on_merge}'

gh api repos/Dejetins/custometry/branches/main/protection \
  --jq '{required_status_checks,enforce_admins,required_pull_request_reviews,required_linear_history,required_conversation_resolution,allow_force_pushes,allow_deletions}'
```

Expected post-conditions:

- `visibility=public`, `default_branch=main`;
- merge commit and rebase merge are disabled; squash merge is enabled;
- `Foundation gate` is strict and required;
- PR review policy exists with `required_approving_review_count=0`;
- admins are covered, linear history and conversation resolution are required;
- force-push and branch deletion are disabled.

Record only the redacted JSON fields above. Do not record raw headers or credentials.

## Failure and safe recovery

- `404`: verify repository identity and the authenticated account's admin permission; do
  not weaken the payload.
- `422` for the required context: confirm the exact CI job name and that a pull-request
  check has been observed, then retry. Do not substitute a partial job.
- A sole owner cannot merge: first inspect the protection response. Restore the accepted
  zero-approval payload; do not disable PR or CI requirements.
- CI is unavailable: leave `main` protected and repair CI on a branch. Bypass is not the
  normal recovery path.

To restore the previously captured settings, apply an explicitly reviewed prior JSON
snapshot with the same endpoints. Deleting branch protection is a destructive policy
change and is not an authorized rollback for this runbook.

## Review trigger

Review this contract when the aggregate required-check name, repository owner, merge
strategy, CODEOWNERS model, or accountable reviewer count changes.
