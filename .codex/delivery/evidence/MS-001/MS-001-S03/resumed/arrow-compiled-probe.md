# Arrow compilation scope and API7 size observation

This is additional diagnostic evidence for MS-001-S03, not final native supply
acceptance. The [stage report](../report.md) and canonical journal retain ownership
of execution state. Earlier Thrift 0.20 diagnostic evidence is preserved unchanged.

The Thrift 0.24/full Boost 1.81 source build completed on native Linux ARM64 with
PyArrow 20.0.0. Its runtime Parquet/IPC probe and three artifact-store tests passed.
An added observer reused the completed compiler stage and inspected all 11 Ninja
build directories, actual object files and static archive members. It did not
recompile source. [Compilation inputs](arrow-compiled-probe/compilation-inputs.json)
bind source/header/object hashes and 12 internal vendored component coverage sets.
[Pins](arrow-compiled-probe/arrow-source-build.json.snapshot),
[observer](arrow-compiled-probe/arrow-build-provenance.py.snapshot) and
[hashes](arrow-compiled-probe/hashes.json) preserve the exact diagnostic inputs.

The coordinator independently parsed the original Ninja outputs: 580 object
records, all dependency counts consistent and every status `VALID`. No compiler
dependency contains `IOBuf`; the sole Folly path is the adapted
`ProducerConsumerQueue.h`. The primary
[Folly correction](https://github.com/facebook/folly/commit/4f304af1411e68851bdd00ef6140e9de4616f7d3)
changes `folly/io/IOBuf.cpp`. This supports a source-subset distinction for this
diagnostic build; raw CVE-2021-24036 Critical findings must remain visible and final
image-bound applicability evidence must be repeated on both native platforms.

LZ4 has five static members (`lz4`, `lz4file`, `lz4frame`, `lz4hc`, `xxhash`) and
11 upstream compiler input paths, all under `lib/`. Thrift has 43 static members;
110 upstream compiler input paths are under `lib/cpp/src/thrift/`, with no Windows
SocketPair or other language bindings. Installed/build archive member lists agree.
The final producer now collects this evidence, retains the full LZ4 `lib/LICENSE`
and Thrift LICENSE/NOTICE, and checks utf8proc code/data against the original archive.
These production changes have not yet been proven in a final clean native run.

The full diagnostic API7 image is a separate build subject:
`sha256:2d79463e936164c8a42bd70da31c46e06812bb6c41ade7f7c8a293bcc60675c4`.
Its [runtime probe](arrow-compiled-probe/api7-runtime-probe.json) passed.
The [size observation](arrow-compiled-probe/api7-size-observation.json) verifies the
child manifest, configuration, both compressed descriptors and ordered DiffIDs:
55,396,251 compressed layer bytes; **194,012,672 uncompressed layer tar bytes**.
Docker's engine `Size` was 55,399,102 bytes. The coordinator independently saved
this same subject and reproduced these values with separate standard-library code.
This diagnostic subject satisfies the unchanged API cap of 367,001,600 bytes.

The metric includes tar headers/padding and overwritten lower-layer content; it
does not measure allocated disk blocks or registry transfer. S04 must use the same
method on its baseline before making comparative claims. Native production and
assembly now require this observation; a legacy engine `Size` result alone is
insufficient. See the [tooling contract](../../../../../../docs/architecture/tooling-gates.md).

Focused source-capture checks passed 45 tests, including six real temporary Git
fixtures that reject a changed executed helper with `DELIVERY_SOURCE_CAPTURE_REQUIRED`.
The compiler-parser/size/supply group passed 62 tests and Ruff. A later Pyright
finding in test dictionary inference was corrected; subsequent full focused checks
are recorded at the next checkpoint. No signature, provider upload, complete
license closure or final AMD64/ARM64 acceptance is claimed here.

## Complete dependency correction

The first normalized observer above retained only 1813 owned inputs and omitted
562 external compiler headers. Its snapshot is historical and cannot by itself
prove absence across all compiler dependencies. The original raw Ninja evidence
was complete, so the coordinator's diagnostic inspection remains valid.

The corrected observer uses schema 2 / `ninja-complete-deps-and-ar-members/v2`.
It records every input's SHA/size, original include spelling, any resolved symlink
identity, each object's dependency count and the exact referenced input union.
The reader rejects missing or unreferenced input records and mismatched counts.
A real temporary object/header fixture preserves an external `folly/io/IOBuf.h`;
removing that dependency record fails validation. The narrow Folly adapter also
rejects any IOBuf input, including builder-system or resolved paths, and retains
the raw Critical count and original scanner records.

The [complete diagnostic observation](arrow-compiled-probe/compilation-inputs-v2.json.gz)
contains **580 objects / 2375 inputs / 562 external inputs**. Its uncompressed
SHA-256 is `e68a7edcebf45558aa1a5f5da924a5dea786031074313a6d44adc1ba1f14d671`,
size 8557344 bytes. This gzip is evidence storage only; it is not recursively
extracted delivery content. The [v2 hashes](arrow-compiled-probe/hashes-v2.json)
bind it and the corrected observer snapshot. The coordinator independently compared
every object count/list and the complete input union with all 11 original Ninja
streams: exact match, no IOBuf path. Production reader validation also passed.

After the correction, 24 focused compiler/native tests, Ruff and Pyright passed.
The prior broader group passed 192 tests with one expected duplicate-ZIP fixture
warning; `check:local` passed. API8 is a diagnostic current-producer build in progress,
not the final clean source run. No complete S03 supply result is implied.

## API8 observation and loader correction

Diagnostic API8 completed and its actual native inventory verified 23 components,
notice hashes, full compiler evidence and utf8proc source/data invariance against
the selected pins. Subject:
`sha256:6a509490e7cbe8a41e1098db9261047439fa645d40bf69085dacddb0d6bddafe`.
It is not a runtime pass: explicit `pyarrow.dataset` / `pyarrow.acero` imports
exposed missing transitive sibling library lookup. `libarrow_acero.so.2000` exists
in the actual image, but the source-built C++ libraries lacked a sibling RUNPATH.
The same image imports both modules with an explicit diagnostic `LD_LIBRARY_PATH`,
establishing the lookup cause. That environment override is not the production fix.

The producer now sets `CMAKE_INSTALL_RPATH=$ORIGIN` and the final scratch stage
executes nonroot imports of the API, psycopg, Dataset, Acero, Parquet and IPC during
the image build. The native profile reader requires the selected RPATH. The API9
diagnostic build is testing this correction. Earlier Parquet probes could fall back
when Dataset was unavailable, so their passing Parquet/IPC assertions do not prove
Dataset/Acero import coverage. One additional API8 probe invocation also lacked its
required `/probe/old.parquet` input; that invocation failed and is not counted passed.

The subsequent focused group passed **276 tests**, Ruff, Pyright and `check:local`.
It includes v2 whole-set obligation checking against actual synthetic companion
files, rejection of legacy relative-path reviews in the v2 context, complete source
capture checks and preservation of raw vulnerability findings. The source collector,
actual subject review records, complete assembler/publisher integration and both
final native platforms remain pending. No S04 deferral substitutes for those S03
outcomes. Task-owned BuildKit cache was reduced by 3.281 GB before API9 to maintain
the existing owned-storage budget; foreign images/containers were not cleaned up.

## API9 verified diagnostic outcome

API9 completed with the `$ORIGIN` fix and mandatory nonroot final-stage imports.
Subject `sha256:e708451951e3daf5a0831e0131ef202665512c6365ef3a02d907ccd052a9eba2`;
configuration `sha256:9b9de4418488cac5e4fb2bcd9c7eb51531d144680427f9d7e8dc92f25caba381`.
The [expanded runtime probe](api9/runtime-probe.json) and
[artifact-store tests](api9/artifact-store-tests.txt) passed (three tests). The
coordinator independently ran the exact digest read-only, with network disabled,
all capabilities dropped, no new privileges, UID 10001 and no source mounts.
It asserted no `LD_LIBRARY_PATH`/`LD_PRELOAD`, imported all selected modules, and
verified an actual Dataset filter, Acero table-source result and IPC roundtrip.

The [size observation](api9/size-observation.json) verifies every layer descriptor
and DiffID: **202791936 uncompressed layer tar bytes**, 55808284 compressed layer
bytes, Docker engine Size 55811664. The API cap remains 367001600 bytes.

The [full-image Trivy result](api9/trivy-result.json) has zero Critical/unknown,
eight findings (four High, three Medium, one Low). The
[native supplement result](api9/native-vulnerability-result.json) retains 11 raw
findings, including one Critical Folly match, with one exact source/complete-compiler
`not_affected` resolution and zero applicable Critical/unknown findings. Raw reports,
23-component native SBOM, source provenance and complete compiler inputs are bound
by [API9 hashes](api9/hashes.json). The coordinator independently checked actual image
layer bytes, native ELF/proof hashes and reproduced the supplemental result.

Two actual scanner integration issues were corrected: Grype rejects `/dev/null`
as a configuration without a supported extension, so the producer now supplies an
independently captured empty YAML configuration; a synthetic container component in
the supplemental SBOM made Grype reconstruct an empty image hint, so this SBOM now
contains only actual package components and the bound subject property. It remains
a file scan. Raw report and binding are persisted before applicability can reject.

The [unreviewed license gate](api9/license-gate-unreviewed.json) still fails:
component-specific source/license conclusions and complete obligations are unfinished.
This diagnostic result does not prove final clean source, AMD64, repeated native
build equality, final source companions, signed publication or private handoff.
