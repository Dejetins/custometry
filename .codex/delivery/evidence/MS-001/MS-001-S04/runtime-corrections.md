# S04 observed runtime failures and bounded corrections

The failed runs remain evidence, never acceptance. All runs consume the same
S03 transfer archive `c89759d1459ec2e09f4e89b08b10cf725df0357fc04f63ec6268cb6d1cdb1b77`.
No image, dependency, migration or original bundle bytes were rebuilt or modified.

1. Run `34274373939`: authenticated transfer/hash checks and API import passed;
   `docker image inspect` of the recorded manifest ID failed on Docker 28.0.4.
   Run `34274628232` enabled the standard containerd store and all three recorded
   manifest IDs resolved. Its before/after evidence shows legacy overlay2 metadata
   versus `io.containerd.snapshotter.v1`. This paired observation confirms the
   image-store compatibility cause. The M5 engine also reports that snapshotter.
   [Docker's documented configuration](https://docs.docker.com/engine/storage/containerd/)
   supplies the ordinary setting; only the disposable hosted runner is changed.
2. Runs `34274628232` and diagnostic run `34274872500`: database startup failed;
   fixed-label container diagnostics reported permission denial. The new extractor
   made all files 0600 and the bound demo directory 0700. The retained ZIP declares
   shell files 0755 and SQL files 0644. Restoring those modes for the five validated
   init files and 0755 for the mount root removed the permission indicator in run
   `34275132200`. Private parent directories and generated secret containment stay
   unchanged. A regression test verifies modes, unchanged bytes and private parent.
3. Run `34275132200`: startup still failed with `invalid`, after permission denial
   disappeared. Exact retained `010_create_reader.sh` requires `^[a-f0-9]{64}$`;
   the harness used `token_urlsafe(32)`, which violates that input contract. Use
   `token_hex(32)` and query `retail.receipts` as `demo_reader` for exactly 5,000 rows.
   This strengthens demo initialization proof beyond transient health/restart state.
   The first ARM64 health-only runs cannot be used to claim completed demo seeding;
   final acceptance requires the corrected reader query on both native platforms.

An editing command failed to locate a formatted function signature and made no
change; its enclosing shell nonetheless dispatched unchanged run `34275055370`.
That redundant run was promptly cancelled and contributes no proof. Subsequent
publication commands stop on the first failure. No repeated result is counted
as success merely because another attempt passed.

The final correction is in PR #61; actual successful run IDs and results are in
[the current stage report](report.md). The initial partial report is preserved as
[report-partial-01.md](report-partial-01.md). Error evidence contains fixed diagnostic
labels rather than raw PostgreSQL logs, SQL statements, credentials or provider data.
