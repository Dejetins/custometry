---
doc_id: ARCH-QUALITY-TOOLING-001
title: Custometry quality tooling and gates
doc_version: 13
product_spec_version: 0.9.0-draft
visibility: internal
ship: false
owner: engineering-productivity
requirement_ids: [DOC-RULE-008]
status: accepted
proof_boundary:
  label: repository-tooling-contract
  exclusions: [release-runtime-evidence, github-hosted-ci-proof]
---

# Custometry Quality Tooling and Gates

## 1. Canonical interface

All repository validators live in the importable `tools.custometry_quality` package. Business logic is not duplicated in shell scripts or GitHub Actions. The canonical grouped entrypoint is:

```bash
source scripts/activate-toolchain.sh
uv run --locked python -m tools.check --scope pre-commit
uv run --locked python -m tools.check --scope local
uv run --locked python -m tools.check --scope pre-push
uv run --locked python -m tools.check --scope ci
uv run --locked python -m tools.check --scope release
```

Every command:

- is deterministic for the same tree and input;
- has `--help`, a stable non-zero exit on violation, and bounded redacted output;
- does not modify files in check, validate, or gate mode;
- allows a generator to modify only its owned artifact without `--check`; CI uses `--check`;
- distinguishes `not_applicable` from `not_observed`; required release proof cannot become green through a skip;
- has focused automated tests for success, failure, unsafe input, and missing input.

## 2. Hook profiles

| Profile | When | Contract |
|---|---|---|
| `pre-commit` | Commit hook | All deterministic source checks: blueprints, requirement/documentation indexes, links, layout, delivery contract/tickets, profiles, DDD, contracts, routes, i18n, fixtures, and migration graph |
| `local` | Before handing off a bounded change | `pre-commit` + `doctor --mode static` |
| `pre-push` | Push hook | `local` + Compose/browser static contracts; migration static validation already runs in every profile |
| `ci` | Every pull request and merge SHA | Exact `pre-push` parity independent of developer hooks |
| `release` | Release candidate in the target environment | `ci` + runtime-required doctor, migration, Compose, browser, SBOM/license, recovery, and performance; missing evidence = failure |

The commit hook invokes `--scope pre-commit`, and the push hook invokes
`--scope pre-push`; neither contains its own validator rules. Both delegate to
`scripts/run-hook-profile.sh`, which activates the exact repository Node, pnpm,
and uv pins before entering the locked Python environment. Direct grouped
profiles must source `scripts/activate-toolchain.sh` first for the same reason.
Author handoff uses `--scope local`, GitHub Actions uses `--scope ci`, and the
protected release environment uses `--scope release`.

## 3. Tool matrix

The prefix for every direct command is `uv run python -m tools.custometry_quality.`

| Tool / command suffix | Trigger | Grouped scopes | Direct CI/release use | What it proves / does not prove |
|---|---|---|---|---|
| `generate_requirement_index --check` | Machine/human blueprint or requirement references changed | PC, L, PP, CI, R | CI checks committed `docs/generated/requirement-index.json` | The index has not drifted; it does not prove that a requirement is correct |
| `validate_blueprints` | Any blueprint or requirement-consuming documentation changed | PC, L, PP, CI, R | Always | Version, mutual-link, and ID parity plus machine-first invariants |
| `generate_docs_index --check` | Contributor Markdown tree changed | PC, L, PP, CI, R | CI checks committed `docs/README.md` | Contributor index is deterministic and contributor mode enforces the repository's English-default authoring policy; it does not prove product `/help` authorization or search |
| `check_docs_links` | Any Markdown, index, or anchor changed | PC, L, PP, CI, R | Always | Real relative links and anchors resolve |
| `validate_repository_layout` | App, package, tool, documentation, or test path added or moved | PC, L, PP, CI, R | Always | The tree matches declared ownership and blueprint section 25 extensions |
| `validate_delivery_contract` | Global delivery adapter or routing changed | PC, L, PP, CI, R | Always; local audit may add `--contract <installed-path>` | Portable CI validates the adapter identity/routing; an explicit installed path additionally validates the global source, supplying `delivery-orchestrator` skill, and global router |
| `validate_delivery_tickets` | Delivery ticket changed or a Goal is prepared | PC, L, PP, CI, R | Always | Ticket identity, frontier blockers, exact scope, repair policy, validation boundary/proof-skill route, escalation set, blocked records, and the schema of terminal evidence; it does not prove the behavior |
| `validate_agent_profiles` | Root governance documents, `AGENTS`, role TOML, templates, or skill routes changed | PC, L, PP, CI, R | Semantic role changes also require a canary | Schema, routing, reference integrity, and English-authoring rules for root contributor/governance documents, repository agent instructions, registries, profiles, and templates |
| `doctor` | Setup, engine, configuration, ports, network, resources, Compose, or release changed | L static; PP/CI static; R static+runtime | `custometry-doctor --mode runtime` on the target | Preconditions, engine, and resources; not application readiness |
| `validate_prompt_packs` | Milestone plan, prompts, journal, updater or bound capability evidence changed | PC, L, PP, CI, R | Always | Schema, accepted plan/hash bindings, receipts and declared entry inputs; no stage execution or concurrent-claim proof |
| `development_runtime` | Hybrid CLI, development Compose override, host-process ownership, demo reset, or release isolation changed | PC, L, PP, CI, R | `scripts/dev validate`; real lifecycle is executed separately for W11 acceptance | Static ownership, loopback publication, volume separation, bounded logs, reset target, and release-entrypoint exclusion; static validation does not prove the Docker/host lifecycle |
| `cleanup` | Generated, temporary, or container data deletion, or disk remediation | Not included automatically | Dry-run when triggered; R synthetic apply drill | Ownership-bounded deletion and post-condition; not broad deletion authority |
| `check_ddd_boundaries` | Imports, package boundaries, allowlist, or context map changed | PC, L, PP, CI, R | Always | Compile-time dependency policy; not runtime SQL proof |
| `check_contract_drift` | OpenAPI, JSON Schema, DTOs, examples, generated TypeScript, or mocks changed | PC, L, PP, CI, R | Always + provider/consumer tests | The generated client byte-matches its sources, and explicitly bound JSON Schema and OpenAPI components match in payload-validation semantics; not real API behavior |
| `validate_route_registry` | Routes, UI map, navigation, or Help mapping changed | PC, L, PP, CI, R | Always + browser when runnable | Route ID and path mappings; not history/guard runtime |
| `check_i18n_parity` | UI, copy, error, Help catalogs, or locale-neutral IDs changed | PC, L, PP, CI, R | Always | en/ru key parity; not linguistic quality |
| `validate_fixture_manifest` | Generator, profile, seed, schema, or golden outcomes changed | PC, L, PP, CI, R | Always + generated fixture tests | Manifest, hash, and expectations are deterministic |
| `validate_migration_lifecycle` | Schema, migrations, or image compatibility changed | PC/L/PP/CI/R static; R runtime | `custometry-validate-migration-lifecycle --mode runtime` | Static graph plus accepted-revision SHA/evidence seal; release observes empty, repeat, downgrade, and re-upgrade lifecycle |
| `compose_lifecycle` | Compose, images, configuration, health, network, or volumes changed | PP/CI/R static; R runtime | `custometry-compose-lifecycle --mode runtime` | Static configuration or observed disposable lifecycle, depending on mode |
| `browser_smoke` | Web, API, authentication, routes, documentation, Help, or system states changed | PP/CI/R static; R runtime | `custometry-browser-smoke --mode runtime` | A static manifest is not a browser; runtime executes the named journey |
| `gate_sbom` | Dependency, base image, or build layer added or changed | R actual artifact | Artifact-producing CI runs directly with `--sbom`; R required | SBOM is tied to the final digest; it is not provenance by itself |
| `gate_licenses` | Dependency, image, or license policy changed | R actual artifact | Artifact-producing CI runs directly with `--sbom`; R required | Policy and NOASSERTION handling; not legal approval |
| `gate_recovery` | Persistence, artifact, migration, backup, or runtime changed | R fresh evidence | Direct integration when the boundary changes; R required | A fresh observed drill on the named target |
| `gate_performance` | Hot path, resource, default, or benchmark corpus changed | R fresh evidence | Direct comparable regression when the boundary changes; R required | Baseline, corpus, environment, and threshold comparability |

`PC/L/PP/CI/R` means `pre-commit/local/pre-push/ci/release`. `pre-push` and `ci` have exact parity; release first runs the CI set and then the runtime and evidence gates.

## 4. Direct usage rules

Generators:

```bash
uv run python -m tools.custometry_quality.generate_requirement_index
uv run python -m tools.custometry_quality.generate_requirement_index --check
uv run python -m tools.custometry_quality.generate_docs_index
uv run python -m tools.custometry_quality.generate_docs_index --check
```

Validators and gates are run directly for focused feedback:

```bash
uv run python -m tools.custometry_quality.validate_blueprints
uv run python -m tools.custometry_quality.check_docs_links
uv run python -m tools.custometry_quality.validate_repository_layout
uv run python -m tools.custometry_quality.validate_delivery_contract
uv run python -m tools.custometry_quality.validate_delivery_tickets
uv run python -m tools.custometry_quality.validate_agent_profiles
uv run python -m tools.custometry_quality.doctor
uv run python -m tools.custometry_quality.development_runtime validate
uv run python -m tools.custometry_quality.check_ddd_boundaries
uv run python -m tools.custometry_quality.check_contract_drift
uv run python -m tools.custometry_quality.validate_route_registry
uv run python -m tools.custometry_quality.check_i18n_parity
uv run python -m tools.custometry_quality.validate_migration_lifecycle
uv run python -m tools.custometry_quality.validate_fixture_manifest
uv run python -m tools.custometry_quality.compose_lifecycle
uv run python -m tools.custometry_quality.browser_smoke
uv run python -m tools.custometry_quality.gate_sbom
uv run python -m tools.custometry_quality.gate_licenses
uv run python -m tools.custometry_quality.gate_recovery
uv run python -m tools.custometry_quality.gate_performance
```

Runtime and evidence examples with required arguments:

```bash
custometry-doctor --mode runtime
custometry-validate-migration-lifecycle --mode runtime
custometry-compose-lifecycle --mode runtime
custometry-browser-smoke --mode runtime
custometry-gate-sbom --sbom <final-sbom.cdx.json>
custometry-gate-licenses --sbom <final-sbom.cdx.json> --policy deploy/license-policy.json
custometry-gate-recovery --evidence <fresh-recovery-evidence.json>
custometry-gate-performance --evidence <fresh-performance-evidence.json>
```

`deploy/license-policy.json` implements the normative allow/deny/review policy. The gate evaluates
package-level CycloneDX components, does not treat file inventory as separate dependencies,
deduplicates repeated layer records, and emits a separate `license-review-required` result for
MPL/LGPL. Unknown, not-allowed, review-required, and denied results fail closed; the release
workflow does not create an accepted installer manifest until architecture/legal review and
`THIRD_PARTY_NOTICES` are closed by real artifacts.

Cleanup always starts with a dry run:

```bash
uv run python -m tools.custometry_quality.cleanup --ownership-manifest <path>
uv run python -m tools.custometry_quality.cleanup --apply --ownership-manifest <path> \
  --confirm DELETE-CUSTOMETRY-OWNED-PATHS
```

The canonical manifest includes repository-local disposable state only. In particular,
`.pnpm-store/` and `.playwright-cli/` count against the owned-disk budget, are excluded from Git
and the Docker context, and may be deleted only with this exact-confirmation command. Global or
shared caches and every path outside the repository root are never cleanup candidates.
This is the repository cleanup CLI boundary. The runtime installation document
describes a separate target ownership boundary for installed resources; its
acceptance requires installer-specific implementation and synthetic evidence
and does not widen this CLI allowlist.

Browser runtime proof does not use an arbitrary host Node version. `tests/e2e/Dockerfile` builds
a test-only multi-architecture runner from digest-pinned Node `24.18.0` and Playwright `1.52.0`;
the runner is downloaded and cached separately and is not included in the API/Web release images
or installer manifest. On Linux it connects to loopback test ingress through host networking; on
Docker Desktop it uses `host.docker.internal`. Product Web/API still pass separate negative-egress
probes.

`--apply` is permitted only after reviewing the dry run, with the exact confirmation phrase, and only for a manifest created by the current installation/workspace. CI does not delete host-wide resources.

### Internal delivery structural reader

`deploy/compose/validate-delivery-manifest.py` is the dependency-free v1 delivery
input reader, owned by the runtime delivery tooling boundary. Changes to its schema,
policy or parsing require these focused checks before handoff:

```sh
uv run --locked python -m pytest -q tests/tooling/test_delivery_bundle.py tests/tooling/test_delivery_bundle_producer.py tests/integration/test_release_manifest.py
uv run --locked python deploy/compose/validate-delivery-manifest.py tests/tooling/fixtures/delivery-manifest.valid.json
uv run --locked python deploy/compose/validate-delivery-manifest.py --policy deploy/compose/delivery-verification-policy.json
```

The first two artifact checks report `DELIVERY_STRUCTURE_VALID`, not verified
signatures, archive closure or release readiness. The source-level fixture uses
synthetic digests. This is a parser seam, not a new grouped runtime gate; S03's
artifact-producing workflow must invoke the completed producer/consumer and final
subject gates. The existing local profile still supplies documentation, migration,
contract and prompt-pack source checks. See the
[internal delivery contract](runtime-network-installation.md#11-internal-delivery-v1-contract-ms-001s01)
and its separately allocated S02–S04 proof obligations.

S02 adds `python -m tools.custometry_quality.delivery_bundle` with `capture`,
`assemble`, `prepare`, `check`, `pack` and `observe-image-files`. See each command's
`--help` and the runtime contract's candidate packaging section. `check` is read-only;
the other commands create explicit new local outputs. Image observation needs an
existing authorized local image and creates/removes its own stopped container.
Fixture tests cover actual Compose rendering outside the repository and a copied
standard-library toolkit, so that test file requires Docker CLI with Compose but
not an engine. No fixture certifies real image subjects or signature trust.

The original `check-image-size.sh` uses Docker's `Size` field. Record engine/store
semantics: the observed containerd image store reports compressed content there.
For the unpacked cap, S02 also measured streamed decompressed layer-tar bytes from
`docker image save`, a conservative upper bound including layer metadata. S03/S04
must retain separate compressed, unpacked and transfer observations; neither a
local image ID nor an unpacked upper bound is a registry download measurement.

## 5. Change-trigger groups

| Change | Minimum before handoff |
|---|---|
| Markdown only | `validate_blueprints` when blueprint references are involved + `generate_docs_index --check` for the contributor index and English-default authoring policy + `check_docs_links` |
| Agent/governance | Markdown group + `validate_delivery_contract` + `validate_delivery_tickets` + `validate_agent_profiles` |
| Package/import | `check_ddd_boundaries` + applicable backend/frontend gates |
| Contract/API | `check_contract_drift` + API contract tests |
| Route/UI/i18n | `validate_route_registry` + `check_i18n_parity` + browser smoke when runnable |
| Schema/migration | `validate_migration_lifecycle` + clean PostgreSQL integration |
| Fixture/generator | `validate_fixture_manifest` + golden expectations |
| Compose/network/image | `doctor` + `development_runtime` when Hybrid paths change + `compose_lifecycle` + browser smoke + SBOM/license; the static gates validate development/release separation and exact `Edge↔Web↔API` adjacency, while runtime evidence observes the selected boundary; production Edge egress denial still requires separate target firewall/CNI evidence |
| Recovery/upgrade | `gate_recovery` + migration lifecycle + actual drill |
| Performance/resource | `gate_performance` with baseline + doctor resource capture |
| Release | Full `check --scope release`; separate green subsets do not replace it |

## 6. Evolution rules

- A new validator must have an owner, trigger, proof boundary, tests, and placement in one or more profiles before merge.
- The orchestrator does not catch or suppress an individual gate failure.
- Profile output lists executed, not-applicable, and not-observed tools.
- Path-based optimization is added only after measuring CI duration and must not permit false skips for shared contracts.
- Tool output contains no secrets, DSNs, raw PII, cookies, or provider payloads.
- Auto-fix in CI is prohibited; a local generator or fixer shows the exact owned diff.


## 7. Stage journal transactions

The accepted planning framework uses `prompt-pack-ledger/v1`, `stage-prompt/v1`
and `prompt-pack-receipt/v1`. The repository snapshot
[`prompt_pack_validation.py`](../../tools/custometry_quality/prompt_pack_validation.py)
records its Prompt Manager source SHA and preserves that profile, adding accepted
plan/version/hash checks and in-memory candidate validation. It needs no installed
home-directory skill to validate repository artifacts in CI. The read-only
`validate_prompt_packs` gate runs in every source profile. It checks actual
journals under `.codex/delivery/ledgers/`; no journal is activated by a gate.

The [`stage_ledger.py`](../../tools/custometry_quality/stage_ledger.py) updater is
`custometry-stage-ledger/v1`, available on macOS and Linux with Python and Git.
The runner resolves current user authority and reviews real evidence; the updater
supplies the exclusive local transaction. Use one canonical checkout and journal
for a pack. Separate clones/worktrees or network filesystems are not a shared
coordination service. Distributed execution is outside this mechanism's scope.

```sh
uv run --locked python -m tools.custometry_quality.validate_prompt_packs
uv run --locked python -m tools.custometry_quality.prompt_pack_validation --root "$PWD" --ledger "$PWD/.codex/delivery/ledgers/MS-001.md" --check entry --stage MS-001-S01
uv run --locked python -m tools.custometry_quality.stage_ledger preflight --ledger .codex/delivery/ledgers/MS-001.md --stage MS-001-S01
```

`preflight` checks entry plus actual updater availability and returns the current
`ledger_sha256`; it never claims a stage. After the user requests execution, use
`claim` with the same ledger/stage and `--expected-sha256 <observed-sha256>`.
Each mutating command requires that exact observed hash and returns the new hash.
A stale hash requires a reread and renewed checks, never a blind retry. Resolve
`CODEX_THREAD_ID` from the actual runner session; outside Codex explicitly pass
`--session <actual-stable-session-id>`. A new session may claim a new pending stage;
it cannot resume another session's existing claim. Never copy a foreign session
identifier, reset a claim or delete updater metadata to obtain ownership.

The updater holds a nonblocking POSIX `flock` on a stable file in the checkout's
Git metadata for the entire read/validate/write transaction. Lock files are never
unlinked. Session ownership uses a private 0600 random key in Git metadata; only
its hash is recorded in the journal. Neither the key nor its bytes are printed,
committed or included in evidence. A process exit releases the transaction lock;
the durable stage claim survives, so another executor cannot silently restart it.
An unavailable original session requires an explicit reconciled recovery change;
this CLI deliberately offers no force-steal or state-reset operation.

Before each transition, the updater verifies the bound implementation/capability,
live plan and prompts, current claim, dependencies, entry inputs and receipt.
It validates the proposed state in memory, checks source/evidence hashes again,
then uses a same-directory temporary file, `fsync` and atomic `os.replace`.
All cooperating writers must use this updater. Direct file editors and malicious
processes running as the same OS user are outside its concurrency guarantee.

| Operation | Required evidence and result |
|---|---|
| `claim` | Allowed pending stage and current entry inputs; activates the journal and records one claim atomically |
| `advance` | After current-stage acceptance with a disallowed successor: `--reason` and `--evidence` for renewed input/authority checks; enables that pending successor without rewriting the accepted row or its receipt |
| `pause` | `--reason`, `--evidence`, `--question`, `--resume-condition`; records recoverable `needs_input` |
| `resume` | Original session plus `--resolution` pointing to the actual answer; rechecks entry and resumes the same claim |
| `accept` | `--receipt` pointing to a new immutable receipt; `review_ready` pauses for required user acceptance, `ready` accepts and enables only its independently verified successor, or completes the final stage |
| `block` | `--reason` and `--evidence`; records a demonstrated hard blocker, preserving the terminal row and all history |

Evidence/receipt/resolution paths are relative to the journal directory and must
resolve within the checkout. Consumed receipts are recorded by canonical resolved path and content hash.
Every transaction rejects changed/missing consumed receipts and path aliases.
`pause`/`block` verify the claim and evidence without requiring lost runtime
entry inputs to be restored first; control artifacts must remain parseable.

The runner writes immutable reports/check evidence
and receipts before a terminal transition, reviews their meaning, and never
uses a fabricated `pass` or acceptance file. A hash establishes bytes, not truth.
For a paused completed result, preserve the earlier report/receipt snapshot,
record the actual user decision, rerun required checks and create a new receipt.
An absent successor remains disallowed; normal MS-001 handoffs produce declared
inputs before allowing the next stage. If a successor becomes ready only after
acceptance, the new execution request uses `advance --stage <successor>
--reason <reason> --evidence <journal-relative-readiness-evidence>
--expected-sha256 <current-observed-hash>` and then its normal preflight/claim. Repair revisions and deliberate migration
of an already activated plan require an explicitly scoped reconciliation; the
normal CLI does not silently rewrite existing contracts or terminal history.

Commands emit one bounded JSON result. Exit 0 with `status: pass` confirms only
the reported operation; nonzero, malformed or interrupted output requires reading
actual journal state before retry. If interruption follows atomic replacement,
the durable record and history determine whether the operation already completed.
[`test_stage_ledger.py`](../../tests/tooling/test_stage_ledger.py) exercises actual
subprocess contention, process death, stale writes, session isolation, receipt
binding, pause/resume/final acceptance and interrupted replacement in temporary
Git checkouts. These tests never execute a product milestone.


### S03 supply preparation checks

The disabled workflow/producer is covered by:

```sh
uv run --locked pytest -q tests/tooling/test_delivery_supply.py tests/tooling/test_delivery_bundle.py tests/tooling/test_delivery_bundle_producer.py tests/tooling/test_license_reviews.py tests/tooling/test_license_expressions.py
uv run --locked ruff check tools/custometry_quality/delivery_supply.py tools/custometry_quality/delivery_bundle.py tests/tooling/test_delivery_supply.py deploy/compose/install-supply-tools.py
uv run --locked pyright tools/custometry_quality/delivery_supply.py tests/tooling/test_delivery_supply.py deploy/compose/install-supply-tools.py
```

Synthetic tests exercise native evidence assembly, subject/freshness failures,
filesystem comparison, immutable provider reconciliation and bounded transport
unwrapping. They do not certify actual scanner output, signatures or publication.
The Web producer additionally runs `pnpm --filter @custometry/web build` and
`node deploy/compose/collect-web-notices.mjs`; included module/package identities,
source/metadata/chunk hash mismatches and notice coverage have focused negative tests.
Component reviews bind policy, exact SBOM, OCI subjects, name/version/PURL,
declaration and nonempty hashed obligation evidence. Structural validation does
not supply a substantive license review or authorize an unknown license.
Real selected-image SBOM/license/Trivy findings remain hard supply gates; source
profiles and ordinary Foundation CI cannot waive them. See the
[runtime supply contract](runtime-network-installation.md#13-internal-supply-producer-preparation-ms-001s03).
