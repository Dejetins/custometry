# Custometry — M3 Pro Foundation proof

## Status and scope

- status: `accepted; W00 closed and B01 S00 activated but not executed`;
- date: `2026-07-16`, `Europe/Moscow`;
- branch: `codex/program-preparation-b01`;
- base revision: `7125a90da3348df75eea24c750823d6723f2f237`;
- applicable requirement IDs: `ARCH-PRINCIPLE-001`, `DOC-RULE-008`,
  `SCALE-004`;
- proof boundary: repository Foundation on the first supported local Apple
  Silicon host;
- this report does not claim product implementation, a final installer,
  release-candidate supply-chain evidence, recovery/performance acceptance,
  production firewall/CNI enforcement, or Penpot authority.

## Host and runtime envelope

The proof used only non-sensitive host facts. Serial numbers, UUIDs, device
identifiers, credentials, raw environment dumps, and Docker provider payloads
are excluded.

| Surface | Observed value |
|---|---|
| Host model | `Mac15,6` |
| Processor | `Apple M3 Pro`, `arm64`, 11 logical CPUs |
| Memory | 18 GiB physical |
| Operating system | macOS `15.7.4` |
| Docker engine | Docker Desktop server `29.6.1`, `aarch64`, 11 CPUs, 7.75 GiB runtime capacity |
| Python | `3.12.2` through the locked uv workspace |
| Node | `24.18.0` |
| pnpm | `11.13.0` through Corepack |
| uv | `0.9.26` |
| Foundation Compose budget | 2.938 GiB declared aggregate memory, below the 6 GiB policy |
| Repository-owned disk observed by doctor | 0.428 GiB |

## Reproducible tool activation

The repository now has one documented activation path:

```bash
scripts/bootstrap-toolchain.sh
source scripts/activate-toolchain.sh
```

The bootstrap:

- selected the exact Node pin shared by `.node-version` and `.nvmrc`;
- activated the exact pnpm version from `package.json#packageManager`;
- rejected a uv version different from `.uv-version`;
- ran `uv sync --locked --all-groups --all-packages`;
- ran `corepack pnpm install --frozen-lockfile`.

Fresh Bash and Zsh shells both reported Node `24.18.0`, pnpm `11.13.0`, and uv
`0.9.26`. The activation fails closed when a pin is missing, mismatched, or not
installed.

The first publication attempt exposed a separate hook boundary: Git inherited
ambient Node `22.22.2` and pnpm `11.9.0` because the thin hook wrappers entered
the Python profile before activating repository pins. Publication stopped as
designed. The hooks now delegate to `scripts/run-hook-profile.sh`, which
activates the exact pins before either quality profile. A regression test starts
the runner with deliberately incompatible ambient Node/pnpm shims and proves
that the pinned `24.18.0`/`11.13.0` tools execute the requested profile.

## Source and CI-equivalent evidence

| Command/boundary | Result |
|---|---|
| `uv run --locked python -m tools.check --scope ci --json` | passed: 13 deterministic source checks plus doctor/migration/Compose/browser static contracts |
| Program matrix | passed: 649 indexed requirements, 649 unique allocations, 15 catalog workstreams, and 14 staged triads |
| Staged-work validator | passed: B01–B13 plus W14, exact module/plan/prompt/ledger links, dormant-state rules, dependencies, milestone gates, and requirement ownership |
| `uv run --locked ruff check apps/api/src migrations tests tools` | passed |
| `uv run --locked pyright` | passed with 0 errors |
| `uv run --locked pytest -q` | passed: 119 tests |
| `uv run --locked mkdocs build --strict --config-file mkdocs.yml` | passed |
| `corepack pnpm check` | passed: lint, typecheck, 12 tests, and production Web build |
| Real `.githooks/pre-commit` and `.githooks/pre-push` entrypoints | passed after self-activating Node `24.18.0`, pnpm `11.13.0`, and uv `0.9.26` |
| Contributor/shipped documentation indexes | passed: 66 contributor documents and 8 shipped public documents |
| Documentation links | passed: 82 documents and 132 local links |

The first CI-equivalent run correctly detected a stale contributor index after
the final module/template changes. The owned generator refreshed
`docs/README.md`, and the complete CI profile then passed. The rejected run is
not counted as acceptance evidence.

## M3 Pro real-boundary evidence

### Runtime doctor

`doctor --mode runtime` observed one healthy local Docker engine, exact
toolchain pins, 11 CPUs, 7.75 GiB Docker memory capacity, and sufficient
repository/free-disk budgets. The doctor now rejects an exit-zero Docker
response whose server identity, root, version, CPU, memory, or error state is
unhealthy.

### Migration lifecycle

`validate_migration_lifecycle --mode runtime` observed all four declared
lifecycle steps against disposable PostgreSQL state: empty upgrade, repeat,
downgrade, and re-upgrade. One current migration revision was exercised.

### Compose lifecycle and network boundary

`compose_lifecycle --mode runtime` built and started six disposable services
under a unique `custometry-ci-*` project and observed:

- exactly one loopback-only published Edge port;
- Edge → Web health success;
- direct Edge → API denial;
- Web → API health success;
- API and Web negative general-egress probes;
- a `200` public Edge health response;
- control PostgreSQL without a host-published database port;
- successful cleanup of disposable containers, networks, volumes, secrets,
  and runtime files.

This proves the local Compose ingress and negative-egress contract. It does not
claim that Docker Compose provides a portable ingress-only network for Edge or
that a production firewall/CNI policy has been enforced.

### Browser and documentation runtime

`browser_smoke --mode runtime` ran the self-contained disposable lifecycle and
five real browser journeys through the loopback Edge surface. The proof covered
the Foundation Web shell, API health/version boundary, local `/docs`, shipped
Help content, and declared browser smoke expectations. It is Foundation browser
evidence, not B01 product-screen acceptance.

### Cleanup post-condition

After migration, Compose, and browser proof, read-only Docker queries found no
remaining containers, volumes, or networks with the `custometry-ci-*` prefix.
Foreign Docker resources were neither stopped nor removed.

## Foundation acceptance boundary

The complete preparation set received the required terminal cold review,
bounded findings were fixed, and the final post-review tree passed the same
source and runtime boundaries. W00 `repository_foundation` is therefore
accepted.

Explicit exclusions:

- no B01–B13 feature stage has been executed;
- no published OCI digest, SBOM, provenance, or final license decision;
- no accepted recovery drill or comparable performance baseline;
- no end-user install/upgrade release receipt;
- no production Edge firewall/CNI proof;
- no remote-worker, object-storage, Kubernetes, or multi-host evidence;
- no canonical Penpot file or write-authority decision.

## Contract impact

| Surface | Classification | Rationale |
|---|---|---|
| Public API, DTOs, events, PostgreSQL product schemas | `none` | Foundation preparation does not change product behavior |
| Toolchain activation and contributor setup | `compatible-change` | Exact pins and one fail-closed activation path replace ambient tool selection |
| Staged plan/prompt/ledger schema | `breaking-change` with atomic zero-instance cutover | The stricter schema was introduced before any accepted staged instance existed; every initial instance and validator changed together |
| Program ownership/dependency/milestone contract | `compatible-change` | A new authoritative planning contract is added before product implementation |
| Browser-visible product behavior | `none` | Only the existing Foundation smoke surface was exercised |
| Runtime/network policy | `none` | Existing Foundation topology was observed; production hardening remains deferred |

## Cold review and correction

The independent terminal read-only review returned `Block` before activation.
It found:

- first-milestone ownership contradictions for 29 forecasting/security/risk
  requirements;
- an empty-hash loophole for the active executable current prompt;
- no fail-closed equality check between the plan requirement set and the union
  of S00–S06 requirement IDs;
- stale proof counts and ambiguous 15-catalog/14-staged terminology;
- dormant/blocked prose drift and one B02 maturity wording mismatch.

The preparation set was corrected before any workstream activation:

- B06 now owns the complete Vertical Alpha forecast baseline, while B09 begins
  the expanded lifecycle and monitoring at `public_mvp`;
- security requirements now follow their real W00/B03/B04/B05/B06/B09/B10/
  B11/B12 capability owners and first milestones;
- both the matrix generator and staged validator reject a primary owner outside
  the first-milestone hard-dependency closure;
- an active executable current stage requires at least one matching pinned
  source hash;
- the staged validator enforces exact plan-to-stage requirement coverage;
- modules, plans, ledgers, prompt outlines, templates, rules, and terminology
  were synchronized.

Focused Ruff and Pyright passed, 52 focused tooling tests passed, the generated
649-row matrix was current, the 14 staged triads validated, and the complete
`check:ci` profile passed after the corrections.

The follow-up terminal review returned `Release after fixes`. Its only remaining
items were a stale full-suite count and a missing negative regression for a
syntactically valid but stale active source hash. The test was added and now
fails closed with `source-hash-mismatch`; the focused suite passed 52 tests, the
full suite passed 119 tests, Ruff and Pyright passed, and `check:ci` passed
again. Under the reviewer verdict, B01 may now perform the documented narrow
activation transition.

## Finalization

### Independent review

The initial terminal review returned `Block`. After the routing, validator,
artifact, and documentation fixes, the same independent read-only reviewer
returned `Release after fixes`. Its final two bounded requests were completed:
the proof counts were refreshed and a non-empty-but-stale active hash regression
was added. No architecture redesign or further independent review was required
by that verdict.

### Activation transition

After W00 acceptance, B01 was activated by the documented narrow transition:

- `.codex/PLANS.md` registers only the B01 plan/prompt-pack/ledger trio;
- the B01 ledger is `active` with `current_stage: S00`;
- only S00 has `next_allowed: true`;
- S00 pins seven reviewed repository sources and every SHA-256 matches;
- B02–B13 and W14 remain dormant with no allowed stage;
- S00 remains pending and no B01 product implementation has been executed;
- Penpot access and canonical-file authority remain explicitly outside this
  activation.

### Final source and runtime evidence

The final source-state digest is:

`sha256:67f91f4b26970b8d93ffe38f0897d5f66fbbff2a666f0636d4abc59e6869d680`

It is the SHA-256 of the sorted stream of `shasum -a 256` records for every
tracked or unignored repository file, excluding this proof report itself to
avoid a circular digest.

On that activated state:

- locked toolchain bootstrap completed;
- Ruff passed, Pyright reported 0 errors, and 119 Python tests passed;
- strict MkDocs build passed;
- pinned pnpm lint/typecheck, 12 tests, and production Web build passed;
- `check:ci` passed with 649/649 requirements and only B01 active;
- Docker runtime doctor passed with 11 CPUs and 7.75 GiB engine capacity;
- the four-step PostgreSQL migration lifecycle passed;
- the six-service Compose lifecycle passed with Edge-to-Web success,
  Edge-to-API denial, API/Web negative-egress probes, one loopback Edge port,
  and public health `200`;
- all five real browser journeys passed;
- cleanup queries found no remaining `custometry-ci-*` containers, volumes, or
  networks;
- generated ignored build and browser artifacts were removed before
  publication.

This closes repository preparation and authorizes only B01 S00 Discovery. It
does not claim B01 implementation, another workstream, public MVP, v1, or
release readiness.

## Post-acceptance governance amendment

On `2026-07-16`, after the W00 observations above were accepted, the project
owner accepted the four-mode development runtime contract. The active B01 S00
prompt now pins that contract in addition to the original seven sources. This
is a documentation and staged-governance amendment only: the W00 runtime
observations and the source-state digest above remain the historical accepted
snapshot and were not relabelled as freshly rerun evidence.
