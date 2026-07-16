from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools.custometry_quality import check_contract_drift
from tools.custometry_quality import check_ddd_boundaries
from tools.custometry_quality import check_docs_links
from tools.custometry_quality import check_i18n_parity
from tools.custometry_quality import generate_docs_index
from tools.custometry_quality import generate_requirement_index
from tools.custometry_quality import validate_agent_profiles
from tools.custometry_quality import validate_blueprints
from tools.custometry_quality import validate_fixture_manifest
from tools.custometry_quality import validate_repository_layout
from tools.custometry_quality import validate_route_registry
from tools.custometry_quality import validate_staged_workstream


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def dump(path: Path, value: object) -> Path:
    return write(path, json.dumps(value, ensure_ascii=False, sort_keys=True))


def blueprint_pair(root: Path, *, human_id: str = "REQ-001") -> None:
    write(
        root / "machine.md",
        """---
document_family_id: FAMILY
spec_version: 1.0
representation: machine
normative: true
alternate_document:
  path: ./human.md
  expected_spec_version: 1.0
---
# Machine
- id: REQ-001
  requirement: MUST work
""",
    )
    write(
        root / "human.md",
        f"""---
document_family_id: FAMILY
spec_version: 1.0
representation: human
normative: false
source_of_truth:
  path: ./machine.md
  expected_spec_version: 1.0
---
# Human
| ID | Rule |
|---|---|
| {human_id} | works |
""",
    )


def shipped_blueprint(root: Path) -> None:
    write(
        root / "custometry-technical-blueprint-ru.md",
        """---
spec_version: 0.8.1-draft
---
# Blueprint
- id: HELP-001
  requirement: MUST ship local documentation
- id: HELP-002
  requirement: MUST expose shortcuts
""",
    )


def shipped_document(
    *,
    doc_id: str,
    title: str,
    route: str,
    locale: str = "en",
    visibility: str = "public",
    ship: bool = True,
    status: str = "active",
    body_title: str | None = None,
) -> str:
    return f"""---
doc_id: {doc_id}
title: {title}
doc_version: 1
product_spec_version: 0.8.1-draft
locale: {locale}
visibility: {visibility}
ship: {str(ship).lower()}
audiences: [installer, user]
route: {route}
status: {status}
owner: product-documentation
requirement_ids: [HELP-001]
proof_boundary:
  label: generated-index-contract
  exclusions: [browser-authorization]
reviewed_at: "2026-07-16"
---
# {body_title or title}
"""


def test_blueprint_sync_and_requirement_index_detect_drift(tmp_path: Path) -> None:
    blueprint_pair(tmp_path)
    result = validate_blueprints.check(tmp_path, Path("machine.md"), Path("human.md"))
    assert result.ok

    generated = generate_requirement_index.check(
        tmp_path,
        machine=Path("machine.md"),
        human=Path("human.md"),
        output=Path("index.json"),
        check_mode=False,
    )
    assert generated.ok
    assert json.loads((tmp_path / "index.json").read_text())["requirement_count"] == 1
    assert generate_requirement_index.check(
        tmp_path,
        machine=Path("machine.md"),
        human=Path("human.md"),
        output=Path("index.json"),
        check_mode=True,
    ).ok

    blueprint_pair(tmp_path, human_id="REQ-002")
    drift = validate_blueprints.check(tmp_path, Path("machine.md"), Path("human.md"))
    assert not drift.ok
    assert {finding.code for finding in drift.findings} == {
        "human-mirror-missing-ids",
        "human-mirror-extra-ids",
    }


def test_docs_index_uses_docs_relative_links_and_link_checker_checks_anchors(
    tmp_path: Path,
) -> None:
    write(tmp_path / "docs/architecture/a.md", "# Alpha\n\n[Guide](../user-guide/b.md#details)\n")
    write(tmp_path / "docs/user-guide/b.md", "# Guide\n\n## Details\n")
    generated = generate_docs_index.check(tmp_path, Path("docs"), Path("docs/README.md"), False)
    assert generated.ok
    index = (tmp_path / "docs/README.md").read_text()
    assert "architecture/a.md" in index
    assert "docs/architecture/a.md" not in index
    assert check_docs_links.check(tmp_path, [Path("docs")]).ok

    write(tmp_path / "docs/architecture/a.md", "# Alpha\n\n[Guide](../user-guide/b.md#missing)\n")
    failed = check_docs_links.check(tmp_path, [Path("docs")])
    assert not failed.ok
    assert failed.findings[0].code == "broken-anchor"


def test_contributor_docs_require_english_authoring(tmp_path: Path) -> None:
    write(tmp_path / "docs/architecture/a.md", "# Architecture\n\nEnglish source.\n")
    assert generate_docs_index.check(
        tmp_path,
        Path("docs"),
        Path("docs/README.md"),
        False,
    ).ok

    write(tmp_path / "docs/architecture/a.md", "# Архитектура\n")
    failed = generate_docs_index.check(
        tmp_path,
        Path("docs"),
        Path("docs/README.md"),
        False,
    )
    assert any(item.code == "contributor-doc-language-invalid" for item in failed.findings)


def test_shipped_docs_index_is_visibility_aware_and_excludes_non_public_docs(
    tmp_path: Path,
) -> None:
    shipped_blueprint(tmp_path)
    write(
        tmp_path / "docs-site/docs/user-guide/public.md",
        shipped_document(
            doc_id="public-guide",
            title="Public guide",
            route="/docs/user-guide/public/",
        ),
    )
    write(
        tmp_path / "docs-site/docs/user-guide/admin.md",
        shipped_document(
            doc_id="admin-guide",
            title="Admin guide",
            route="/docs/user-guide/admin/",
            visibility="authenticated",
            ship=False,
        ),
    )
    write(
        tmp_path / "docs-site/docs/user-guide/draft.md",
        shipped_document(
            doc_id="draft",
            title="Draft",
            route="/docs/user-guide/draft/",
            visibility="internal",
            ship=False,
            status="draft",
        ),
    )
    result = generate_docs_index.check(
        tmp_path,
        Path("docs-site/docs"),
        Path("apps/web/public/help-index.json"),
        False,
        "shipped",
    )
    assert result.ok
    payload = json.loads((tmp_path / "apps/web/public/help-index.json").read_text())
    assert [item["visibility"] for item in payload["documents"]] == ["public"]
    assert all(item["path"].startswith("docs/") for item in payload["documents"])
    assert all(item["locale"] == "en" for item in payload["documents"])
    assert {item["id"] for item in payload["documents"]} == {"public-guide"}
    assert all("doc_id" not in item for item in payload["documents"])
    assert all("owner" not in item for item in payload["documents"])
    assert {item["route"] for item in payload["documents"]} == {"/docs/user-guide/public/"}

    write(
        tmp_path / "docs-site/docs/user-guide/admin.md",
        shipped_document(
            doc_id="admin-guide",
            title="Admin guide",
            route="/docs/user-guide/admin/",
            visibility="authenticated",
            ship=True,
        ),
    )
    leaked = generate_docs_index.check(
        tmp_path,
        Path("docs-site/docs"),
        Path("apps/web/public/help-index.json"),
        True,
        "shipped",
    )
    assert any(item.code == "non-public-doc-shipping-forbidden" for item in leaked.findings)

    write(
        tmp_path / "docs-site/docs/user-guide/admin.md",
        shipped_document(
            doc_id="admin-guide",
            title="Admin guide",
            route="/docs/user-guide/admin/",
            visibility="authenticated",
            ship=False,
        ),
    )

    write(tmp_path / "docs-site/docs/user-guide/missing.md", "# Missing metadata\n")
    failed = generate_docs_index.check(
        tmp_path,
        Path("docs-site/docs"),
        Path("apps/web/public/help-index.json"),
        True,
        "shipped",
    )
    assert any(item.code == "shipped-doc-metadata-missing" for item in failed.findings)


def test_shipped_docs_reject_title_route_and_identity_drift(tmp_path: Path) -> None:
    shipped_blueprint(tmp_path)
    write(
        tmp_path / "docs-site/docs/index.md",
        shipped_document(
            doc_id="docs-home",
            title="Wrong title",
            route="/docs/wrong/",
            body_title="Documentation",
        ),
    )
    result = generate_docs_index.check(
        tmp_path,
        Path("docs-site/docs"),
        Path("apps/web/public/help-index.json"),
        False,
        "shipped",
    )
    assert any(item.code == "shipped-doc-route-drift" for item in result.findings)

    write(
        tmp_path / "docs-site/docs/index.md",
        shipped_document(
            doc_id="docs-home",
            title="Wrong title",
            route="/docs/",
            body_title="Documentation",
        ),
    )
    result = generate_docs_index.check(
        tmp_path,
        Path("docs-site/docs"),
        Path("apps/web/public/help-index.json"),
        False,
        "shipped",
    )
    assert any(item.code == "shipped-doc-title-drift" for item in result.findings)

    write(
        tmp_path / "docs-site/docs/a.md",
        shipped_document(doc_id="duplicate", title="A", route="/docs/a/"),
    )
    write(
        tmp_path / "docs-site/docs/b.md",
        shipped_document(doc_id="duplicate", title="B", route="/docs/b/"),
    )
    result = generate_docs_index.check(
        tmp_path,
        Path("docs-site/docs"),
        Path("apps/web/public/help-index.json"),
        False,
        "shipped",
    )
    assert any(item.code == "shipped-doc-identity-duplicate" for item in result.findings)


@pytest.mark.parametrize(
    ("old", "new", "expected_code"),
    [
        ("doc_version: 1", "doc_version: 0", "shipped-doc-metadata-invalid"),
        (
            "product_spec_version: 0.8.1-draft",
            "product_spec_version: 0.8.0",
            "shipped-doc-spec-version-drift",
        ),
        ("audiences: [installer, user]", "audiences: [unknown]", "shipped-doc-metadata-invalid"),
        (
            "requirement_ids: [HELP-001]",
            "requirement_ids: [HELP-999]",
            "shipped-doc-requirement-unknown",
        ),
        (
            "exclusions: [browser-authorization]",
            "exclusions: []",
            "shipped-doc-metadata-invalid",
        ),
        ('reviewed_at: "2026-07-16"', 'reviewed_at: "2026-02-30"', "shipped-doc-metadata-invalid"),
    ],
)
def test_shipped_docs_reject_invalid_normative_metadata(
    tmp_path: Path,
    old: str,
    new: str,
    expected_code: str,
) -> None:
    shipped_blueprint(tmp_path)
    source = shipped_document(doc_id="docs-home", title="Documentation", route="/docs/")
    write(tmp_path / "docs-site/docs/index.md", source.replace(old, new))
    result = generate_docs_index.check(
        tmp_path,
        Path("docs-site/docs"),
        Path("apps/web/public/help-index.json"),
        False,
        "shipped",
    )
    assert any(item.code == expected_code for item in result.findings)


def test_shipped_docs_require_doc_id_and_reject_draft_shipping(tmp_path: Path) -> None:
    shipped_blueprint(tmp_path)
    source = shipped_document(
        doc_id="docs-home",
        title="Documentation",
        route="/docs/",
        status="draft",
    )
    write(tmp_path / "docs-site/docs/index.md", source.replace("doc_id:", "id:"))
    missing_doc_id = generate_docs_index.check(
        tmp_path,
        Path("docs-site/docs"),
        Path("apps/web/public/help-index.json"),
        False,
        "shipped",
    )
    assert any(item.code == "shipped-doc-metadata-invalid" for item in missing_doc_id.findings)

    write(tmp_path / "docs-site/docs/index.md", source)
    draft_shipping = generate_docs_index.check(
        tmp_path,
        Path("docs-site/docs"),
        Path("apps/web/public/help-index.json"),
        False,
        "shipped",
    )
    assert any(item.code == "draft-doc-shipping-forbidden" for item in draft_shipping.findings)


def test_repository_layout_checks_required_and_forbidden_tracked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write(tmp_path / "required.txt", "ok")
    (tmp_path / "required-dir").mkdir()
    manifest = dump(
        tmp_path / "layout.json",
        {
            "schema_version": 1,
            "required_files": ["required.txt"],
            "required_directories": ["required-dir"],
            "forbidden_tracked_globs": ["**/.DS_Store"],
        },
    )

    def clean_tracked(_root: Path) -> list[str]:
        return ["ok.txt"]

    def forbidden_tracked(_root: Path) -> list[str]:
        return ["x/.DS_Store"]

    monkeypatch.setattr(validate_repository_layout, "_tracked_files", clean_tracked)
    assert validate_repository_layout.check(tmp_path, manifest).ok
    monkeypatch.setattr(validate_repository_layout, "_tracked_files", forbidden_tracked)
    failed = validate_repository_layout.check(tmp_path, manifest)
    assert any(item.code == "forbidden-tracked-file" for item in failed.findings)


def _templates(root: Path, version: str = "1.0") -> None:
    write(root / "AGENTS.md", "# Repository instructions\n")
    write(root / "CONTRIBUTING.md", "# Contributing\n")
    write(root / "README.md", "# Project\n")
    write(root / "SECURITY.md", "# Security\n")
    write(root / ".codex/AGENTS.md", "# Agent contract\n")
    write(root / ".codex/PLANS.md", "# Plan registry\n")
    for name in (
        "prompt_template.md",
        "stage_execution_ledger_template.md",
        "iteration_report_template.md",
    ):
        write(root / ".codex/agents" / name, f"---\nspec_version: {version}\n---\n# Template\n")


def test_agent_profiles_detect_stale_requirement_ranges(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# B\nREQ-001 REQ-002 REQ-003\n",
    )
    instructions = (
        "Result reports status, mode, contract impact, next owner. "
        "Complete, partial and blocked are defined. Resolve REQ-001..003."
    )
    write(
        tmp_path / ".codex/agents/qa.toml",
        'name="qa"\ndescription="Use for QA. Do not use for implementation."\n'
        f'developer_instructions="{instructions}"\n',
    )
    _templates(tmp_path)
    assert validate_agent_profiles.check(tmp_path).ok
    profile = tmp_path / ".codex/agents/qa.toml"
    profile.write_text(profile.read_text().replace("001..003", "001..002"))
    failed = validate_agent_profiles.check(tmp_path)
    assert any(item.code == "stale-requirement-range" for item in failed.findings)

    profile.write_text(
        profile.read_text().replace("Result reports", "Отчёт содержит"),
        encoding="utf-8",
    )
    failed = validate_agent_profiles.check(tmp_path)
    assert any(item.code == "agent-artifact-language-invalid" for item in failed.findings)

    write(tmp_path / ".codex/AGENTS.md", "# Правила\n")
    failed = validate_agent_profiles.check(tmp_path)
    assert any(
        item.code == "agent-artifact-language-invalid"
        and item.path == str(tmp_path / ".codex/AGENTS.md")
        for item in failed.findings
    )


def test_staged_workstream_accepts_no_workstreams_but_rejects_broken_explicit_plan(
    tmp_path: Path,
) -> None:
    _templates(tmp_path)
    (tmp_path / "docs/architecture").mkdir(parents=True)
    (tmp_path / ".codex/agents/generated").mkdir(parents=True)
    assert validate_staged_workstream.check(tmp_path).ok

    plan = write(
        tmp_path / "docs/architecture/p.md",
        "---\nplan_doc: docs/architecture/p.md\n"
        "prompt_pack_dir: .codex/agents/generated/p\n"
        "stage_ledger: docs/architecture/p-reports/p-ledger.md\n---\n# P\n",
    )
    failed = validate_staged_workstream.check(tmp_path, [plan.relative_to(tmp_path)])
    assert {item.code for item in failed.findings} >= {
        "prompt-pack-missing",
        "stage-ledger-missing",
    }

    prompt_pack = tmp_path / ".codex/agents/generated/p"
    prompt_pack.mkdir(parents=True)
    write(
        tmp_path / "docs/architecture/p-reports/p-ledger.md",
        "---\nplan_doc: docs/architecture/p.md\n"
        "prompt_pack_dir: .codex/agents/generated/p\n"
        "stage_ledger: docs/architecture/p-reports/p-ledger.md\n"
        "allowed_stage_statuses: [pending, in_progress, accepted, blocked, skipped, superseded]\n"
        'current_stage: "00"\n---\n# Ledger\n',
    )
    prompt = write(
        prompt_pack / "00-start.md",
        "---\nprompt_pack_execution:\n"
        "  enabled: true\n"
        "  plan_doc: docs/architecture/p.md\n"
        "  prompt_pack_dir: .codex/agents/generated/p\n"
        "  stage_ledger: docs/architecture/p-reports/p-ledger.md\n"
        "  required_source_hashes: {}\n"
        "  branch_policy:\n"
        "    per_stage_branches: forbidden\n"
        "---\n# Этап\n",
    )
    failed = validate_staged_workstream.check(tmp_path, [plan.relative_to(tmp_path)])
    assert any(
        item.code == "staged-artifact-language-invalid" and item.path == str(prompt)
        for item in failed.findings
    )


def test_ddd_boundary_rejects_cross_context_and_framework_core_import(tmp_path: Path) -> None:
    write(tmp_path / "packages/a/domain/model.py", "from packages.contracts import DTO\n")
    (tmp_path / "packages/contracts").mkdir(parents=True)
    assert check_ddd_boundaries.check(tmp_path).ok
    write(
        tmp_path / "packages/a/domain/model.py", "import fastapi\nfrom packages.b import private\n"
    )
    (tmp_path / "packages/b").mkdir()
    failed = check_ddd_boundaries.check(tmp_path)
    assert {item.code for item in failed.findings} == {
        "cross-context-import",
        "framework-import-in-core",
    }


def test_ddd_boundary_checks_typescript_alias_relative_and_framework_imports(
    tmp_path: Path,
) -> None:
    (tmp_path / "packages/a/application").mkdir(parents=True)
    (tmp_path / "packages/b/src").mkdir(parents=True)
    (tmp_path / "packages/contracts/src").mkdir(parents=True)
    write(
        tmp_path / "packages/a/application/use-case.ts",
        'import React from "react";\n'
        'import { privateValue } from "../../b/src/private";\n'
        'import { Contract } from "@custometry/contracts";\n',
    )
    failed = check_ddd_boundaries.check(tmp_path)
    assert {item.code for item in failed.findings} == {
        "cross-context-import",
        "framework-import-in-core",
    }
    assert failed.details["typescript_files"] == 1


def test_contract_drift_uses_source_digest(tmp_path: Path) -> None:
    openapi = dump(
        tmp_path / "contracts/openapi.json",
        {
            "openapi": "3.1.0",
            "paths": {
                "/health": {
                    "get": {
                        "operationId": "getHealth",
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Health"}
                                    }
                                }
                            }
                        },
                    }
                }
            },
            "components": {
                "schemas": {
                    "Health": {
                        "type": "object",
                        "required": ["status"],
                        "properties": {"status": {"type": "string"}},
                    }
                }
            },
        },
    )
    dump(
        tmp_path / "contracts/a.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "a",
            "type": "object",
            "required": ["status"],
            "properties": {"status": {"type": "string"}},
        },
    )
    manifest = dump(
        tmp_path / "manifest.json",
        {
            "schema_version": 1,
            "openapi": "contracts/openapi.json",
            "json_schemas": ["contracts/a.schema.json"],
            "openapi_schema_bindings": {"contracts/a.schema.json": "Health"},
            "typescript_client": {
                "path": "client/foundation-client.ts",
                "generator": check_contract_drift.GENERATOR,
                "generator_version": check_contract_drift.GENERATOR_VERSION,
            },
        },
    )
    generated = check_contract_drift.check(
        tmp_path, manifest.relative_to(tmp_path), write_client=True
    )
    assert generated.ok
    assert check_contract_drift.check(tmp_path, manifest.relative_to(tmp_path)).ok
    external = tmp_path / "contracts/a.schema.json"
    external_data = json.loads(external.read_text())
    external_data["required"] = []
    dump(external, external_data)
    semantic_drift = check_contract_drift.check(tmp_path, manifest.relative_to(tmp_path))
    assert semantic_drift.findings[0].code == "json-schema-openapi-drift"

    external_data["required"] = ["status"]
    dump(external, external_data)
    client = tmp_path / "client/foundation-client.ts"
    client.write_text(
        client.read_text().replace("readonly status: string", "readonly status: number")
    )
    client_drift = check_contract_drift.check(tmp_path, manifest.relative_to(tmp_path))
    assert client_drift.findings[0].code == "generated-client-drift"

    assert check_contract_drift.check(
        tmp_path, manifest.relative_to(tmp_path), write_client=True
    ).ok
    dump(openapi, {"openapi": "3.1.0", "paths": {"/changed": {}}})
    failed = check_contract_drift.check(tmp_path, manifest.relative_to(tmp_path))
    assert failed.findings[0].code in {"contract-source-invalid", "generated-client-drift"}


def test_route_registry_requires_exact_complete_metadata(tmp_path: Path) -> None:
    write(
        tmp_path / "ui.md",
        "| ID | Route | Page | Phase | Roles |\n|---|---|---|---|---|\n"
        "| UI-AN-001 | `/analytics` | Analytics | MVP | AN |\n",
    )
    registry = dump(
        tmp_path / "routes.json",
        {
            "schema_version": "2.0.0",
            "routes": [
                {
                    "id": "UI-AN-001",
                    "path": "/w/:workspaceKey/analytics",
                    "title_key": "UI-AN-001",
                    "release": "MVP",
                    "status": "planned",
                }
            ],
        },
    )
    en_titles = dump(tmp_path / "en-titles.json", {"UI-AN-001": "Analytics"})
    ru_titles = dump(tmp_path / "ru-titles.json", {"UI-AN-001": "Аналитика"})
    paths = (
        Path("ui.md"),
        registry.relative_to(tmp_path),
        en_titles.relative_to(tmp_path),
        ru_titles.relative_to(tmp_path),
    )
    assert validate_route_registry.check(tmp_path, *paths).ok
    dump(en_titles, {"UI-AN-001": "Wrong"})
    failed = validate_route_registry.check(tmp_path, *paths)
    assert failed.findings[0].code == "route-title-source-drift"

    dump(en_titles, {"UI-AN-001": "Analytics"})
    dump(ru_titles, {})
    failed = validate_route_registry.check(tmp_path, *paths)
    assert {finding.code for finding in failed.findings} == {"russian-route-title-missing"}

    dump(ru_titles, {"UI-AN-001": "Аналитика"})
    registry_data = json.loads(registry.read_text())
    registry_data["routes"][0]["title_key"] = "localized title"
    dump(registry, registry_data)
    failed = validate_route_registry.check(tmp_path, *paths)
    assert failed.findings[0].code == "route-title-key-invalid"


def test_i18n_parity_rejects_missing_or_empty_values(tmp_path: Path) -> None:
    dump(tmp_path / "en.json", {"nav": {"home": "Home"}})
    dump(tmp_path / "ru.json", {"nav": {"home": "Главная"}})
    assert check_i18n_parity.check(tmp_path, Path("en.json"), Path("ru.json")).ok
    dump(tmp_path / "ru.json", {"nav": {"other": ""}})
    failed = check_i18n_parity.check(tmp_path, Path("en.json"), Path("ru.json"))
    assert {item.code for item in failed.findings} == {
        "russian-key-missing",
        "english-key-missing",
        "catalog-value-invalid",
    }


def test_i18n_directory_catalogs_require_file_and_key_parity(tmp_path: Path) -> None:
    dump(tmp_path / "locales/en/foundation.json", {"nav": {"home": "Home"}})
    dump(tmp_path / "locales/ru/foundation.json", {"nav": {"home": "Главная"}})
    assert check_i18n_parity.check(tmp_path, Path("locales/en"), Path("locales/ru")).ok
    dump(tmp_path / "locales/en/errors.json", {"error": "Error"})
    failed = check_i18n_parity.check(tmp_path, Path("locales/en"), Path("locales/ru"))
    assert any(item.code == "russian-catalog-missing" for item in failed.findings)


def test_fixture_manifest_detects_hash_drift(tmp_path: Path) -> None:
    fixture = write(tmp_path / "tests/golden/a.csv", "a,b\n1,2\n")
    digest = hashlib.sha256(fixture.read_bytes()).hexdigest()
    manifest = dump(
        tmp_path / "tests/golden/manifest.json",
        {
            "schema_version": 1,
            "fixtures": [
                {
                    "path": "tests/golden/a.csv",
                    "sha256": digest,
                    "size": fixture.stat().st_size,
                    "profile": "smoke",
                    "seed": 42,
                    "data_schema_version": "1",
                }
            ],
        },
    )
    assert validate_fixture_manifest.check(tmp_path, manifest.relative_to(tmp_path)).ok
    fixture.write_text("changed")
    failed = validate_fixture_manifest.check(tmp_path, manifest.relative_to(tmp_path))
    assert {item.code for item in failed.findings} == {"fixture-size-drift", "fixture-hash-drift"}


def test_fixture_profile_manifest_validates_seed_counts_and_scenarios(tmp_path: Path) -> None:
    manifest = dump(
        tmp_path / "tests/golden/retail-demo-manifest.json",
        {
            "schema_version": "1.0.0",
            "profile": "demo",
            "seed": 42,
            "timezone": "UTC",
            "default_currency": "EUR",
            "grain": {"receipts": "one row per receipt"},
            "primary_keys": {"receipts": ["receipt_id"]},
            "pii_class": {"customers.email": "direct_identifier"},
            "expected_counts": {"receipts": 100},
            "scenarios": ["returns", "anonymous_receipts"],
        },
    )
    result = validate_fixture_manifest.check(tmp_path, manifest.relative_to(tmp_path))
    assert result.ok and result.details["seed"] == 42
    data = json.loads(manifest.read_text())
    data["scenarios"] = ["returns", "returns"]
    dump(manifest, data)
    failed = validate_fixture_manifest.check(tmp_path, manifest.relative_to(tmp_path))
    assert failed.findings[0].code == "fixture-manifest-invalid"


def test_missing_required_inputs_are_not_observed(tmp_path: Path) -> None:
    result = check_contract_drift.check(tmp_path)
    assert not result.ok
    assert not result.observed
    assert result.findings[0].code == "missing-input"
