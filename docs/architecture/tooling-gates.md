---
doc_id: ARCH-QUALITY-TOOLING-001
title: Custometry quality tooling and gates
doc_version: 6
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

Browser runtime proof does not use an arbitrary host Node version. `tests/e2e/Dockerfile` builds
a test-only multi-architecture runner from digest-pinned Node `24.18.0` and Playwright `1.52.0`;
the runner is downloaded and cached separately and is not included in the API/Web release images
or installer manifest. On Linux it connects to loopback test ingress through host networking; on
Docker Desktop it uses `host.docker.internal`. Product Web/API still pass separate negative-egress
probes.

`--apply` is permitted only after reviewing the dry run, with the exact confirmation phrase, and only for a manifest created by the current installation/workspace. CI does not delete host-wide resources.

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
| Compose/network/image | `doctor` + `compose_lifecycle` + browser smoke + SBOM/license; the static gate validates exact `Edge↔Web↔API` adjacency and the fixed Edge→Web proxy source/upstream, while the runtime gate observes Edge→Web success and Edge→API failure; production Edge egress denial still requires separate target firewall/CNI evidence |
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
