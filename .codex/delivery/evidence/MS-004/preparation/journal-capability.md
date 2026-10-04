# MS-004 journal capability — read-only inspection

<!-- stage-ledger-capability:v1 -->
```json
{
  "mechanism": "custometry-stage-ledger/v1",
  "result": "pass",
  "implementation": [
    {
      "path": "../../../tools/custometry_quality/stage_ledger.py",
      "sha256": "884a4c12c071d82c44a4aa7947888498fe7d8eb81cfe7e7820af554550402692"
    },
    {
      "path": "../../../tools/custometry_quality/prompt_pack_validation.py",
      "sha256": "1e7a874382dad63ae48cdb548427feeb8a25ac4158b0b7511afec513486529d5"
    }
  ]
}
```

The current implementation was inspected on 2026-09-20: local POSIX flock on a
stable inode, actual private session ownership, expected-SHA compare-and-swap,
tracked source revalidation, fsync and atomic replacement. Paths/hashes bind the
loaded updater and validator. No MS-004 claim or lifecycle transition was run.
This is source/capability binding, not a new concurrency test or stage entry proof.
At authorized execution preflight must verify the target checkout, current source
hashes and ownership again. Separate Git worktrees are not one shared ledger lock.
