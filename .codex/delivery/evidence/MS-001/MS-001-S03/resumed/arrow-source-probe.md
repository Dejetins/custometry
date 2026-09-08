# PyArrow 20 source-build diagnostic

Boundary: one actual native Linux ARM64 diagnostic build, followed by a disposable
overlay of diagnostic API6. This is neither the final image nor complete S03 proof.
The default runtime dependency constraint remains PyArrow `>=20,<21`.

Apache Arrow 20.0.0 resolves to source commit
`3ad0370a04ccdae638755b94c3c31c8760a11193`. The exact upstream archive is
17601573 bytes, SHA-256
`2d645173a55fd98e1f31764f6fbe0cbcaf64a62fefdca7548549f9bdea28654c`.
Source inspection of `ThirdpartyToolchain.cmake` confirms OpenSSL is conditional
on Flight, cloud adapters, Gandiva or encrypted Parquet. Those options are disabled;
local filesystem, IPC, Parquet, compute, Acero, dataset, CSV, JSON and Brotli/LZ4/
Snappy/Zlib/Zstd remain enabled. Optional jemalloc/mimalloc are disabled. This does
not establish a performance result; S04/runtime performance acceptance is separate.

The source basis is blueprint section 8.3 (local filesystem through v1) and section
18 (Arrow batches and IPC). The coordinator's bounded source review found no
application/tests reliance on the removed Flight/cloud interfaces. Required local
storage behavior is exercised below; other integration paths still need execution.

The diagnostic wheel is `pyarrow-20.0.0-cp312-cp312-linux_aarch64.whl`, 18306527 bytes,
SHA-256 `244b113aed09006763fc05a8c82dd359bf728dbd89eff5e85d1cc6ebbfbc2e6e`.
CMake explicitly reported building without OpenSSL. All inspected wheel ELF files
lacked the `OpenSSL 3.` marker. Absence of that marker alone is not a full native
dependency or vulnerability proof. The build still contains source-pinned native
dependencies whose inventory, advisories and license obligations must be checked.

Actual read-only, no-network API overlay checks passed:

- Imports: `custometry_api.main`, `pyarrow`, `pyarrow.parquet`, `pyarrow.fs`.
- Local filesystem Parquet 2.6/ZSTD round trip, column statistics, Decimal, UTC
  timestamps and nulls.
- RecordBatch chunking, IPC stream round trip and memory-mapped IPC file round trip.
- Reading a Parquet file produced by the earlier prebuilt PyArrow 20 wheel.
- `tests/unit/data_pipeline/test_artifact_store.py`: **3 passed**, including atomic
  commit/idempotency, identity conflict and path rejection.

The focused tests ran inside the diagnostic image with the current repository
mounted read-only, isolated pytest 8.4.1 dependencies and temporary filesystem:

```text
python -m pytest -q -p no:cacheprovider --override-ini addopts= \
  --confcutdir=tests/unit/data_pipeline tests/unit/data_pipeline/test_artifact_store.py
```

Raw build logs and wheel remain task-owned scratch under
`/tmp/ms001-s03-pyarrow-probe/`. Compact exact observations and diagnostic input
snapshots are retained alongside this report. They must not be substituted for
clean-source, repeated native producer evidence or actual source delivery.
