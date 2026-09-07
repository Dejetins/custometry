# MS-001-S02 — Clean-source preparation before publication

Owner authorization is recorded in `../owner-resolution-2026-09-08.md`.
The original claim resumed through `stage_ledger resume`; the old pause report
is preserved byte-for-byte as `../report-pause-2026-09-08.md` and in source commit
`475ef389dbb291f4f27f11ed069ef56819ba5608`. Its receipt was not modified.

The scoped publication branch starts from actual `origin/main`
`f3f72a9204e461ddcb7dff3e6b4f823f62e58358` (the exact resolved reference is also
recorded by Git; no local-only ancestor is included). Source commit
`bc347d7e74c57640b42462c24cc2ed60d76ef055` contains the S01/S02 delta only.
A clean `git archive` of its 340 declared tracked build files was captured and
built for API/Web on ARM64 and AMD64 with version
`0.1.0-dev.0+sha.bc347d7e74c5`. All four builds succeeded. No uncommitted overlay,
source checkout mount, registry publication or deployment was used.

`source-capture.json`, `clean-builds.json`, `clean-images.json`, `image-checks.json`
and four actual image file inventories bind the observations. All imports,
Parquet round-trips, Alembic head checks and Nginx checks pass. ARM64 is native;
AMD64 is emulated on the local engine. All uncompressed layer-tar upper bounds
fit the existing API/Web image caps. Archive input bytes were checked unchanged
again after building.

The CI source profile, full CI Ruff and CI-targeted Pyright pass.
Full pytest reports 336 passed and 15 skipped; skipped database/runtime cases do
not establish runtime proof. Required hosted Foundation CI and protected-main
publication remain to be observed. The stage is not terminally accepted before
that publication check. Final-image supply/signature/native-target and license
policy verdicts remain S03/S04 obligations; none is claimed by local packaging.
