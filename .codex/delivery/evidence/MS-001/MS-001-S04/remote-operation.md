# Prepared exact-archive transfer operation

Stage [MS-001-S04](../../../ledgers/MS-001.md), plan [2.2.0](../../../../../docs/architecture/planning/milestones/MS-001/plan.md).
This is a prepared operation, not an upload, permission grant or runtime result.

## Exact source and target

Source: `/Users/daniildegtyarev/.local/share/custometry/delivery/MS-001/s04-transfer-01/transfer.zip`.
Size: 478,787,131 bytes. SHA-256:
`c89759d1459ec2e09f4e89b08b10cf725df0357fc04f63ec6268cb6d1cdb1b77`.
The [trusted inventory](transfer.json) binds every retained archive, independent S03
reader file and the inner manifest. Stored ZIP entries preserve all selected file
bytes; it includes six archives, `delivery.zip` and the exact reader/configuration.
It contains no secrets, repository checkout or executable instruction from an
unselected provider. The consumer checks trust before loading the reader.

Proposed bridge: one **unpublished draft release** in `Dejetins/custometry`, draft
identifier `ms001-s04-transfer-20260908-01`, one asset `transfer.zip`. Draft audience:
repository users with push access plus the explicitly scoped workflow token. The
repository is PUBLIC; current `gh repo view` reports ADMIN for this session.
A public published release is not selected. GitHub's
[release API documentation](https://docs.github.com/en/rest/releases/releases)
limits draft listings to users with push access; actual denial remains a required
workflow check. Signed download redirects/tokens are never retained in reports.

The prepared [workflow](../../../../../.github/workflows/verify-internal-bundle.yml)
uses `workflow_dispatch`, `ubuntu-24.04`, a 15-minute job limit and 30/180-second
metadata/download timeouts. No retry loop or new account/service is introduced.
It checks the draft flag and representative anonymous denial, downloads through
existing authenticated GitHub access, verifies the outer trusted hash, and invokes
the same consumer with native AMD64. The workflow token needs `contents: write`
for draft visibility; executable steps only read the draft. It uploads only redacted
observations as an Actions artifact with 90-day retention.

## Missing decision and exact effect

The current prompt explicitly requires authority for the exact external effect.
The S01 provider selection authorized an Actions-artifact target and explicitly did
not authorize a new remote store. DEC-13 authorizes preparation, not broader remote
publication. A draft-release bridge is a new remote object/effect. Authorize creation,
one internal upload and deletion of this named draft/asset after the AMD64 result is
retrieved. Retain the existing authenticated scope; no credentials/account are needed.
This is not a request for a new server, registry, public release or license waiver.
Unresolved S03 license metadata and `not_observed` scan/SBOM status remain visible;
no official release or wider distribution is proposed. Any actual unmet redistribution
condition remains binding, independently of transfer authorization.

## Prepared commands after that decision

Publish the owned harness/workflow/trust changes using the already selected protected
branch/PR policy. Preserve and exclude foreign changes; do not broadly stage this
shared checkout. The workflow must first exist on the default branch for dispatch.
Use its actual reviewed commit for the draft target, recorded at execution time.
No commit, branch, push, PR, upload or workflow run was performed in this preparation.

```sh
gh release create ms001-s04-transfer-20260908-01 \
  /Users/daniildegtyarev/.local/share/custometry/delivery/MS-001/s04-transfer-01/transfer.zip \
  --repo Dejetins/custometry --draft --target <reviewed-commit> \
  --title 'Temporary MS-001 S04 internal transfer' \
  --notes 'Unpublished exact S03 archives for native AMD64 verification; delete after retrieval.'
gh workflow run verify-internal-bundle.yml --repo Dejetins/custometry --ref main
# Resolve the exact dispatched run, wait, then retrieve its redacted observation artifact.
gh run download <observed-run-id> --repo Dejetins/custometry \
  --name ms001-s04-native-amd64-observations --dir <new-owned-evidence-directory>
# Remove only this draft and its asset; do not delete unrelated tags/releases.
gh release delete ms001-s04-transfer-20260908-01 --repo Dejetins/custometry --yes
```

Record actual release/asset/run IDs, archive hashes, engine architecture, observed
resource/timing data and deletion result before accepting any remote claim. On
failure preserve redacted evidence and remove the draft once it is no longer needed;
never publish it to make downloads work. The hosted runner is disposable; its `finally`
path removes owned Compose resources and its last step removes transfer/secret files.
Images stay in the ephemeral runner until runner disposal. A cancelled or killed job
is incomplete proof; no manual acceptance can be inferred from environment setup.

Resume S04 through the original session's normal updater transaction using the actual
owner answer. S05 remains unavailable until native dual-platform proof is complete.
