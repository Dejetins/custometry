from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Callable, Sequence

from . import (
    browser_smoke,
    check_contract_drift,
    check_ddd_boundaries,
    check_docs_links,
    check_i18n_parity,
    compose_lifecycle,
    doctor,
    gate_licenses,
    gate_performance,
    gate_recovery,
    gate_sbom,
    generate_docs_index,
    generate_requirement_index,
    validate_agent_profiles,
    validate_blueprints,
    validate_fixture_manifest,
    validate_migration_lifecycle,
    validate_repository_layout,
    validate_route_registry,
    validate_staged_workstream,
)
from .core import CheckResult, add_common_arguments, main_guard, render_result


StaticCheck = Callable[[Path], CheckResult]


def _docs_indexes(root: Path) -> CheckResult:
    result = CheckResult("generate_docs_indexes")
    checks = {
        "contributor": generate_docs_index.check(
            root, Path("docs"), Path("docs/README.md"), True
        ),
        "shipped": generate_docs_index.check(
            root,
            Path("docs-site/docs"),
            Path("apps/web/public/help-index.json"),
            True,
            "shipped",
        ),
    }
    for label, item in checks.items():
        result.observed = result.observed and item.observed
        result.findings.extend(item.findings)
        result.details[label] = item.details
    return result


def _static_checks() -> list[tuple[str, StaticCheck]]:
    return [
        ("blueprints", lambda root: validate_blueprints.check(root, Path("custometry-technical-blueprint-ru.md"), Path("custometry-technical-blueprint-human-ru.md"))),
        ("requirements", lambda root: generate_requirement_index.check(root, machine=Path("custometry-technical-blueprint-ru.md"), human=Path("custometry-technical-blueprint-human-ru.md"), output=Path("docs/generated/requirement-index.json"), check_mode=True)),
        ("docs-index", _docs_indexes),
        ("docs-links", lambda root: check_docs_links.check(root)),
        ("layout", lambda root: validate_repository_layout.check(root)),
        ("staged-work", lambda root: validate_staged_workstream.check(root)),
        ("agent-profiles", lambda root: validate_agent_profiles.check(root)),
        ("ddd", lambda root: check_ddd_boundaries.check(root)),
        ("contract-drift", lambda root: check_contract_drift.check(root)),
        ("routes", lambda root: validate_route_registry.check(root)),
        ("i18n", lambda root: check_i18n_parity.check(root, Path("packages/localization/locales/en"), Path("packages/localization/locales/ru"))),
        ("fixtures", lambda root: validate_fixture_manifest.check(root)),
    ]


def _ci_additional() -> list[tuple[str, StaticCheck]]:
    return [
        (
            "doctor-static",
            lambda root: doctor.check(
                root,
                mode="static",
                ownership_manifest=Path("deploy/compose/ownership-manifest.json"),
            ),
        ),
        ("migrations-static", lambda root: validate_migration_lifecycle.check(root, mode="static")),
        ("compose-static", lambda root: compose_lifecycle.check(root, mode="static", compose=Path("compose.yaml"), policy=Path("deploy/compose/runtime-policy.json"))),
        ("browser-static", lambda root: browser_smoke.check(root, mode="static", manifest=Path("tests/e2e/browser-smoke.json"))),
    ]


def _release_checks() -> list[tuple[str, StaticCheck]]:
    sbom = Path(os.environ.get("CUSTOMETRY_SBOM", "build/sbom.cdx.json"))
    sbom_subjects = [
        value.strip()
        for value in os.environ.get("CUSTOMETRY_SBOM_SUBJECT_DIGESTS", "").split(",")
        if value.strip()
    ]
    release_env_raw = os.environ.get("CUSTOMETRY_RELEASE_ENV_FILE")
    release_env = Path(release_env_raw) if release_env_raw else None
    return [
        (
            "doctor-runtime",
            lambda root: doctor.check(
                root,
                mode="runtime",
                ownership_manifest=Path("deploy/compose/ownership-manifest.json"),
            ),
        ),
        ("migrations-runtime", lambda root: validate_migration_lifecycle.check(root, mode="runtime")),
        (
            "compose-runtime",
            lambda root: compose_lifecycle.check(
                root,
                mode="runtime",
                compose=Path("compose.yaml"),
                policy=Path("deploy/compose/runtime-policy.json"),
                release_env=release_env,
            ),
        ),
        ("browser-runtime", lambda root: browser_smoke.check(root, mode="runtime", manifest=Path("tests/e2e/browser-smoke.json"))),
        (
            "sbom",
            lambda root: gate_sbom.check(
                root,
                sbom,
                expected_subjects=sbom_subjects,
                require_subjects=True,
            ),
        ),
        ("licenses", lambda root: gate_licenses.check(root, sbom, Path("deploy/license-policy.json"))),
        ("recovery", lambda root: gate_recovery.check(root, Path("tests/recovery/evidence.json"))),
        ("performance", lambda root: gate_performance.check(root, Path("tests/performance/evidence.json"))),
    ]


def check(root: Path, scope: str) -> CheckResult:
    result = CheckResult(f"check:{scope}")
    base_checks = _static_checks()
    ci_checks = _ci_additional()
    release_checks = _release_checks()
    checks = list(base_checks)
    if scope == "pre-commit":
        pass
    elif scope == "local":
        checks += ci_checks[:1]
    elif scope in {"pre-push", "ci", "release"}:
        checks += ci_checks
    else:
        result.add("scope-invalid", f"unknown scope {scope}")
        return result
    if scope == "release":
        checks += release_checks
    selected_names = {name for name, _ in checks}
    runtime_names = {name for name, _ in release_checks}
    universe = [*base_checks, *ci_checks, *release_checks]
    outcomes: dict[str, str] = {
        name: (
            "not_observed"
            if name in runtime_names and name not in selected_names
            else "not_applicable"
        )
        for name, _ in universe
    }
    result.details["scope_contract"] = {
        "selected_checks": [name for name, _ in checks],
        "runtime_required": [name for name, _ in release_checks],
        "runtime_observed": False,
    }
    for name, checker in checks:
        item = checker(root)
        outcomes[name] = "executed_passed" if item.ok else "executed_failed"
        result.merge(item)
    if scope == "release":
        result.details["scope_contract"]["runtime_observed"] = all(
            outcomes[name] == "executed_passed" for name in runtime_names
        )
    result.details["outcomes"] = outcomes
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Custometry quality gate groups")
    add_common_arguments(parser)
    parser.add_argument(
        "--scope", choices=("pre-commit", "local", "pre-push", "ci", "release"), default="local"
    )
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.scope), args.json)


if __name__ == "__main__":
    main_guard(cli)
