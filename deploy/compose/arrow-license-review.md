# Source-built Arrow runtime license scope

This review covers the exact versions, source archive hashes and notice hashes in
`arrow-source-build.json` and `arrow-native-licenses.json`. It applies only when
the actual image's wheel ELF files, notices and compilation inputs match the
producer provenance. A changed source, notice, compilation scope or image requires
new binding and review. This document alone does not approve an unobserved image.

The default project license allowlist is unchanged. Components outside it require
an exact SBOM/subject/declaration review record and verified obligation files.
The supported BSL-1.0, CC0-1.0 and Unicode-DFS-2015 profiles are evidence requirements,
not global grants or vulnerability waivers.

| Runtime component | Selected declaration | Distribution evidence |
|---|---|---|
| Boost 1.81 / Arrow utfcpp 3.1.1 | BSL-1.0 | Preserve complete Boost license and existing copyright notices, including shipped headers. This is Boost Software License, distinct from Business Source License. |
| Brotli | MIT | Retain upstream complete LICENSE. |
| LZ4 | BSD-2-Clause | Require every actual LZ4 compiler input to be from `lib/` or its installed headers; retain `lib/LICENSE` as well as the root license router. Do not extend this declaration to GPL tools elsewhere in the archive. |
| RE2, Snappy, xsimd | BSD-3-Clause | Retain upstream complete LICENSE/COPYING and copyright attribution; no endorsement claim. |
| RapidJSON | MIT | Require actual installed RapidJSON headers; exclude `msinttypes` from this MIT scope. Preserve complete upstream license text. Its `bin/jsonchecker` test data uses the non-OSS JSON license: do not distribute the optional full source tarball or project MIT onto it. |
| Thrift 0.24 | Apache-2.0 | Require actual Linux C++ inputs and generated config; reject Windows SocketPair and other language bindings. Retain full LICENSE and NOTICE. |
| utf8proc 2.7 | MIT AND Unicode-DFS-2015 | Retain the complete upstream LICENSE.md with the software and associated delivery documentation. Verify `utf8proc.c`, `utf8proc.h` and `utf8proc_data.c` against the pinned original archive and record unmodified status. Any modification needs explicit software/data and documentation notices. |
| zlib | Zlib | Retain copyright/license text; do not misrepresent origin or modified source. |
| Zstandard | BSD-3-Clause | Select the upstream BSD option for the library. Retain full LICENSE; COPYING is also preserved rather than rewriting upstream notices. |

The Arrow archive includes 12 internal runtime subsets whose exact source file
hashes and versions are pinned independently of dependency downloads. Date and
musl-strptime use MIT; double-conversion and uriparser use BSD-3-Clause; fast_float,
Folly and FlatBuffers use Apache-2.0; PCG offers Apache-2.0 OR MIT; utfcpp uses BSL-1.0;
xxHash uses BSD-2-Clause; cpp-base64 uses Zlib; the selected portable-snippets headers
carry CC0-1.0. Preserve the complete Arrow LICENSE.txt/NOTICE.txt and shipped source
headers. Commit-identified subsets must not be described as an invented upstream
release or the whole upstream project. Actual compiler coverage is mandatory.

Primary texts checked on 2026-09-08: exact archive notices selected by the pinned
build, [Boost Software License](https://spdx.org/licenses/BSL-1.0.html),
[Unicode Data Files and Software 2015](https://spdx.org/licenses/Unicode-DFS-2015.html),
and [CC0](https://spdx.org/licenses/CC0-1.0.html). CC0 does not grant patent/trademark
rights or imply endorsement; preserved attribution does not claim otherwise.

These permissive runtime declarations do not require publishing optional entire
Arrow/native archives. Separate GPL/LGPL/Sleepycat components elsewhere in the final
image retain their actual corresponding-source, relinking and using-code obligations.
Their source companions and final whole-set verification remain mandatory.
