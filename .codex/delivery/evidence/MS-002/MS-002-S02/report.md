# MS-002-S02 — Installed HTTPS, restricted ingress and truthful readiness

[Plan MS-002 1.0.0](../../../../../docs/architecture/planning/milestones/MS-002/plan.md).
[Journal](../../../ledgers/MS-002.md) owns the stage state and permission.
The owner requested S02 only. Normal `advance`, preflight and the actual session's
exclusive claim were used. No publication, subagent or successor execution occurs.

## Delivered scope

The [installer](../../../../../tools/custometry_quality/installation.py) now
validates supplied TLS, generates a separate restricted Nginx/Compose profile,
allocates/retains the actual Docker host port, verifies protected file mounts and
trusted leaf identity, rotates validated candidates and inspects real operational
status. Both proxy hops preserve the external Host including port. Only Edge
publishes HTTPS on container port 8443; fixed Web upstream and network separation
remain. Installation ingress permits only GET root/assets/public docs and exact
health/version/status routes. Other product paths, bootstrap and methods are denied.
The developer HTTP Nginx files remain separate.

[Health](../../../../../apps/api/src/custometry_api/health.py) checks the real DB,
exact single `0009_notifications` head and canonical artifact write/fsync/unlink.
It neither creates storage nor migrates on a request. The bounded
[status DTO](../../../../../apps/api/src/custometry_api/installation.py) reports
only the accepted component states and safe codes with no-store. Existing health
and version DTO shapes remain. OpenAPI and deterministic TypeScript client are
updated for the S03 consumer.

## Validation and observed boundary

[Checks](checks-01.json) records exact commands, outcomes and current source hashes.
[Runtime](runtime-01.json) records the final real Docker observations and image
identity. The test creates a fresh private owned root from the retained verified
Compose input and explicitly selects the newly built local API image. This is
installed transport/API proof, not a newly published or distributed bundle.

- Focused health/installer tests: 27 passed; existing DTO/provider compatibility,
  safe failures and canonical storage checks included.
- Real runtime test: trusted HTTPS through Edge/Web/API/PostgreSQL and mounted
  storage; allowed/denied paths, methods, Host and Origin; actual published mapping,
  protected mounts, image/environment/network identities and leaf comparison.
- Real negative cases: unavailable DB, unsupported head and read-only artifact
  mount return HTTP 503 with the exact safe code. Recovery returns actual readiness.
- Wrong-name, mismatched-key and expired PEM candidates retain the active revision.
  An injected invalid Nginx directive is rejected by real `nginx -t` before
  promotion. Valid rotation changes the revision and rechecks trusted handshake.
- Edge reaches Web and Web reaches API; Edge TCP probes to API and DB fail.
  Plain HTTP cannot return the installation entry. Stop/restart preserves TLS,
  secret bytes and supported DB head.
- Focused Ruff/Pyright, contract drift, TypeScript contract typecheck, static
  Compose lifecycle and final grouped local gate are recorded in checks.

The initial runtime attempts identified two introduced configuration errors:
unsupported `create --no-deps` and missing `/tmp` Nginx FastCGI/uWSGI/SCGI paths.
Both were corrected against direct CLI/Nginx evidence. A test incorrectly assumed
header casing after converting headers to a dict; the assertion was corrected.
On Docker Desktop, chmod on the host bind did not deny actual container writes;
the required failure now uses an actual read-only mount and observes EROFS through
safe API status. These failed attempts are not counted as passing proof. An initial
static-gate lookup named a nonexistent module; the selected `compose_lifecycle`
command is the actual check. OpenSSL's rejected negative validity interval was
replaced with explicit past fixture dates; production certificate issuance is
unchanged.

## Criterion coverage and compatibility

| Criterion / requirements | Actual contribution |
|---|---|
| AC-03; TECH-04/05; SEC-001/007/012/016/017 | Direct trusted local HTTPS; exact host/origin and port; read-only private-parent mounts; safe rotation and negative candidates; restricted route/method boundary and real adjacency probes |
| AC-04; TECH-06; OPS-002; SCALE-003/004 | Real DB/schema/storage checks, unchanged health DTOs, additive bounded status, no-store, safe errors and actual installer reconciliation |
| AC-06; OPS-001/002 | Invalid candidates preserve the active revision; restart preserves secrets/TLS/head; S01's accepted real failed-migration proof remains the migration producer evidence |
| SEC-018 | No production egress/firewall claim; Compose segmentation only |

`breaking-change`: installed HTTP/unrestricted callers must use exact HTTPS and
restricted GET routes; old weak readiness no longer succeeds for unsupported
schema/unwritable storage. These are accepted plan changes. `compatible-change`:
the new status DTO/client is additive; existing health/version JSON shapes remain.
`none`: domain schema/head bytes, Identity private state, existing developer routes,
MS-001 delivery identity and immutable accepted artifacts. New UI with old bundled
API cannot use this DTO; S04 must build a new identified bundle. No cross-version
upgrade, DB downgrade or universal target compatibility is claimed.

## Ownership, documentation and recovery limits

Changed paths are API health/main and bounded installation module, Foundation
OpenAPI/generated client, the installer, focused integration tests, runtime doc
revision 22, architecture navigation, generated contributor index, this evidence
directory and updater-only journal transitions. The checkout was clean on entry;
no foreign source edits were adopted. No schema, dependency, new service, custom
PKI, branch, commit, remote write, volume wipe or MS-001 artifact edit was made.
The existing mkcert CA remained external; OpenSSL generated only a negative expired
fixture under its private test directory. No key, secret, raw log or host-sensitive
path is included in this evidence.

[Runtime contract](../../../../../docs/architecture/runtime-network-installation.md#installed-https-and-operational-status--ms-002-s02)
contains current commands, DTO/recovery behavior and reciprocal evidence links.
State and Compose are separately atomic files; an interruption between promotion
writes fails closed as `CONFIG_CHANGED` and requires reconciliation of retained
owned revisions. There is no online revocation service: external custody must
withdraw compromised material. Mounted Nginx config leaves use the same protected
private-parent/read-only 0444 mechanism needed by the non-root image. No production
revocation or firewall qualification is inferred.

## Next-stage inputs

The actual S03 prompt was read. Its declared inputs are the accepted plan, this
report and the installer; all exist. The operational endpoint and generated client
are produced here. Host-Vite/API/browser target setup and visual work belong to
S03, not S02 entry requirements. S03 remains disallowed because this request runs
S02 only; a separate request can use normal `advance` after renewed entry checks.
S04 retains new bundle packaging, native Mac/Linux matrix and second-computer LAN
proof. No complete UI, bootstrap, browser visual acceptance or production delivery
is claimed. Test installations are stopped with their owned volumes retained.
