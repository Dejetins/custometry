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
from tools.custometry_quality import validate_delivery_contract
from tools.custometry_quality import validate_fixture_manifest
from tools.custometry_quality import validate_delivery_tickets
from tools.custometry_quality import validate_repository_layout
from tools.custometry_quality import validate_route_registry


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
    for name in (
        "spec_template.md",
        "ticket_template.md",
        "iteration_report_template.md",
    ):
        write(root / ".codex/agents" / name, f"---\nspec_version: {version}\n---\n# Template\n")


def test_agent_profiles_detect_stale_requirement_ranges(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# B\nREQ-001 REQ-002 REQ-003\n",
    )
    instructions = (
        "Result reports status, mode, decision_scope, change_scope, contract impact, handoff_to. "
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


def test_agent_profiles_do_not_repeat_delivery_contract_boilerplate(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nREQ-001\n",
    )
    _templates(tmp_path)
    base = "Protect the agreed QA evidence boundary and hand off material findings."
    profile = tmp_path / ".codex/agents/qa.toml"
    write(
        profile,
        'name="qa"\ndescription="Use for QA. Do not use for implementation."\n'
        f'developer_instructions="{base}"\n',
    )
    assert validate_agent_profiles.check(tmp_path).ok

    assert validate_agent_profiles.check(tmp_path).ok


def test_agent_profiles_reject_unknown_top_level_keys(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nREQ-001\n",
    )
    _templates(tmp_path)
    profile = tmp_path / ".codex/agents/qa.toml"
    write(
        profile,
        'name="qa"\ndescription="Use for QA. Do not use for implementation."\n'
        'developer_instructions="Complete, partial and blocked are defined. '
        "Result reports status, mode, decision_scope, change_scope, contract impact, "
        'and handoff_to."\nlanguage="ru"\n',
    )

    result = validate_agent_profiles.check(tmp_path)

    assert "profile-schema-invalid" in {finding.code for finding in result.findings}


def test_ticket_template_version_is_checked_with_other_agent_templates(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nREQ-001\n",
    )
    instructions = (
        "Result reports status, mode, decision_scope, change_scope, contract impact, handoff_to. "
        "Complete, partial and blocked are defined."
    )
    write(
        tmp_path / ".codex/agents/qa.toml",
        'name="qa"\ndescription="Use for QA. Do not use for implementation."\n'
        f'developer_instructions="{instructions}"\n',
    )
    _templates(tmp_path, version="1.0")
    assert validate_agent_profiles.check(tmp_path).ok
    ticket_template = tmp_path / ".codex/agents/ticket_template.md"
    ticket_template.write_text(
        ticket_template.read_text(encoding="utf-8").replace("1.0", "2.0"),
        encoding="utf-8",
    )
    failed = validate_agent_profiles.check(tmp_path)
    assert any(
        item.code == "agent-template-version-drift" and item.path == str(ticket_template)
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
        "---\nui_spec_version: 0.6.0-draft\n---\n"
        "| ID | Route | Page | Phase | Roles |\n|---|---|---|---|---|\n"
        "| UI-AN-001 | `/analytics` | Analytics | MVP | AN |\n\n"
        "| UI-OVR-001 | Filter editor | Analytics | ROUTE-001 |\n"
        "| UI-SYS-001 | Forbidden | Protected routes | ROUTE-001 |\n"
        "| UI-CAP-001 | Governed analytics | Analytics | ROUTE-001 |\n",
    )
    write(
        tmp_path / "product.md",
        "---\nspec_version: 0.9.0-draft\n---\n"
        "permissions:\n  - analysis.read\n\n"
        "requirements:\n  - id: UC-001\n  - id: ROUTE-001\n",
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
    contract = dump(
        tmp_path / "route-contracts.json",
        {
            "schema_version": "1.0.0",
            "product_spec_version": "0.9.0-draft",
            "ui_spec_version": "0.6.0-draft",
            "identity_registry_schema_version": "2.0.0",
            "source_files": [
                "custometry-technical-blueprint-ru.md",
                "custometry-ui-blueprint-ru.md",
                "packages/contracts/routes/ui-routes.json",
            ],
            "role_catalog": sorted(validate_route_registry.ROLE_HINTS),
            "permission_catalog": ["analysis.read"],
            "profiles": {
                "guards": {
                    "workspace_permission": {
                        "authenticated": True,
                        "workspace_resolution": True,
                        "membership": True,
                        "permission": True,
                        "object_access": False,
                        "deny_before_fetch": True,
                    }
                },
                "states": {
                    "browse": {
                        "required_states": ["first_loading", "ready", "forbidden", "failed"],
                        "preserve_previous_data_on_refresh": True,
                    }
                },
                "navigation": {
                    "browse": {
                        "history_entry": "push",
                        "shell_persistent": True,
                        "restore_focus": True,
                        "restore_scroll": True,
                        "dirty_guard": False,
                    }
                },
                "queries": {
                    "standard": {
                        "allowed_keys": ["tab"],
                        "sensitive_values_forbidden": True,
                        "complex_state": "saved_view_or_opaque_reference",
                    }
                },
            },
            "routes": [
                {
                    "id": "UI-AN-001",
                    "path": "/w/:workspaceKey/analytics",
                    "title_key": "UI-AN-001",
                    "family": "workspace",
                    "shell_profile": "workspace",
                    "navigation_group": "analytics",
                    "surface_kind": "list",
                    "release": "MVP",
                    "status": "planned",
                    "role_hints": ["AN"],
                    "authorization": {
                        "mode": "workspace_permission",
                        "entry_permissions_any": ["analysis.read"],
                        "action_permissions": [],
                        "object_scoped": False,
                    },
                    "guard_profile": "workspace_permission",
                    "state_profile": "browse",
                    "navigation_profile": "browse",
                    "query_profile": "standard",
                    "focus_explore": "not_applicable",
                    "source": {
                        "ui_blueprint_id": "UI-AN-001",
                        "requirement_ids": ["ROUTE-001"],
                    },
                    "design": {
                        "penpot_status": "baseline_verified",
                        "frame_key": "UI-AN-001",
                        "baseline_version": "0.4.1-draft",
                    },
                }
            ],
        },
    )
    schema = dump(
        tmp_path / "route-contracts.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "additionalProperties": False,
            "properties": {"schema_version": {"const": "1.0.0"}},
            "$defs": {
                "routeContract": {
                    "additionalProperties": False,
                    "required": sorted(validate_route_registry.ROUTE_CONTRACT_KEYS),
                }
            },
        },
    )
    surface_contract = dump(
        tmp_path / "ui-surface-contracts.json",
        {
            "schema_version": "1.0.0",
            "product_spec_version": "0.9.0-draft",
            "ui_spec_version": "0.6.0-draft",
            "route_contract_schema_version": "1.0.0",
            "source_files": [
                "custometry-technical-blueprint-ru.md",
                "custometry-technical-blueprint-human-ru.md",
                "custometry-ui-blueprint-ru.md",
                "packages/contracts/routes/ui-routes.json",
                "packages/contracts/routes/ui-route-contracts.json",
            ],
            "route_decision_policy": {"route_count_is_ceiling": False},
            "penpot_baseline": {
                "file_id": validate_route_registry.CANONICAL_PENPOT_FILE_ID,
                "verified_route_count": 1,
                "target_route_count": 1,
            },
            "overlays": [
                {
                    "id": "UI-OVR-001",
                    "name": "Filter editor",
                    "kind": "editor",
                    "route_backed": False,
                    "history_semantics": "return_to_owner",
                    "requirement_ids": ["ROUTE-001"],
                }
            ],
            "system_surfaces": [
                {
                    "id": "UI-SYS-001",
                    "name": "Forbidden",
                    "requirement_ids": ["ROUTE-001"],
                }
            ],
            "cross_surface_capabilities": [
                {
                    "id": "UI-CAP-001",
                    "name": "Governed analytics",
                    "delivery_form": "shared_component",
                    "requirement_ids": ["ROUTE-001"],
                }
            ],
            "use_case_bindings": [
                {
                    "use_case_id": "UC-001",
                    "surface_ids": [
                        "UI-AN-001",
                        "UI-OVR-001",
                        "UI-SYS-001",
                        "UI-CAP-001",
                    ],
                    "coverage_types": [
                        "route",
                        "overlay",
                        "system",
                        "cross_surface_capability",
                    ],
                    "rationale": "The route owns the durable result while shared and transient surfaces govern it.",
                }
            ],
        },
    )
    surface_schema = dump(
        tmp_path / "ui-surface-contracts.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "additionalProperties": False,
            "properties": {"schema_version": {"const": "1.0.0"}},
        },
    )
    paths = (
        Path("ui.md"),
        registry.relative_to(tmp_path),
        en_titles.relative_to(tmp_path),
        ru_titles.relative_to(tmp_path),
        contract.relative_to(tmp_path),
        schema.relative_to(tmp_path),
        Path("product.md"),
        surface_contract.relative_to(tmp_path),
        surface_schema.relative_to(tmp_path),
    )
    assert validate_route_registry.check(tmp_path, *paths).ok

    contract_data = json.loads(contract.read_text())
    contract_data["routes"][0]["role_hints"] = ["VW"]
    dump(contract, contract_data)
    failed = validate_route_registry.check(tmp_path, *paths)
    assert {finding.code for finding in failed.findings} == {"route-contract-role-hints-drift"}

    contract_data["routes"][0]["role_hints"] = ["AN"]
    dump(contract, contract_data)
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

    registry_data["routes"][0]["title_key"] = "UI-AN-001"
    dump(registry, registry_data)
    surface_data = json.loads(surface_contract.read_text())
    surface_data["use_case_bindings"] = []
    dump(surface_contract, surface_data)
    failed = validate_route_registry.check(tmp_path, *paths)
    assert {finding.code for finding in failed.findings} == {"ui-surface-use-case-gap"}

    surface_data["use_case_bindings"] = [
        {
            "use_case_id": "UC-001",
            "surface_ids": ["UI-AN-001", "UI-OVR-001", "UI-SYS-001", "UI-CAP-001"],
            "coverage_types": [
                "route",
                "overlay",
                "system",
                "cross_surface_capability",
            ],
            "rationale": "The route owns the durable result while shared and transient surfaces govern it.",
        }
    ]
    surface_data["cross_surface_capabilities"][0]["requirement_ids"] = ["UC-001"]
    dump(surface_contract, surface_data)
    failed = validate_route_registry.check(tmp_path, *paths)
    assert {finding.code for finding in failed.findings} == {
        "ui-surface-blueprint-requirements-drift"
    }

    surface_data["cross_surface_capabilities"][0]["requirement_ids"] = ["ROUTE-001"]
    surface_data["overlays"][0]["requirement_ids"] = ["UC-001"]
    dump(surface_contract, surface_data)
    failed = validate_route_registry.check(tmp_path, *paths)
    assert {finding.code for finding in failed.findings} == {
        "ui-surface-blueprint-requirements-drift"
    }


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


def delivery_contract_fixture(root: Path) -> Path:
    contract = (
        root
        / "global"
        / "skills"
        / "delivery-orchestrator"
        / "references"
        / "delivery-contract-v1.md"
    )
    write(
        contract,
        "# Global Delivery Contract v1\n\nExecution units follow global AGENTS.md.\n",
    )
    write(
        contract.parent.parent / "SKILL.md",
        "---\nname: delivery-orchestrator\n---\n# Delivery Orchestrator\n",
    )
    write(
        contract.parents[3] / "AGENTS.md",
        f"Use delivery-orchestrator at {contract.as_posix()}.\n"
        "One ready ticket is one execution unit.\n",
    )
    write(
        root / ".codex/AGENTS.md",
        "This repository adopts Global Delivery Contract v1 through "
        f"delivery-orchestrator at {contract.as_posix()}.\n",
    )
    return contract


def test_delivery_contract_accepts_linked_global_skill(tmp_path: Path) -> None:
    contract = delivery_contract_fixture(tmp_path)

    assert validate_delivery_contract.check(tmp_path, contract).ok


def test_delivery_contract_rejects_rule_missing_from_global_owner(tmp_path: Path) -> None:
    contract = delivery_contract_fixture(tmp_path)
    global_agent = contract.parents[3] / "AGENTS.md"
    write(global_agent, f"Use delivery-orchestrator at {contract.as_posix()}.\n")
    # A stale duplicate in the reference cannot replace the canonical owner.
    write(contract, "# Global Delivery Contract v1\nOne ready ticket is one execution unit.\n")

    result = validate_delivery_contract.check(tmp_path, contract)

    findings = [
        item
        for item in result.findings
        if item.code == "delivery-contract-execution-unit-rule-missing"
    ]
    assert len(findings) == 1
    assert not result.ok


def test_delivery_contract_accepts_portable_adapter_without_installed_source(
    tmp_path: Path,
) -> None:
    contract = delivery_contract_fixture(tmp_path)

    assert validate_delivery_contract.check(tmp_path).ok
    assert contract.is_file()


def test_delivery_contract_rejects_missing_adapter_link(tmp_path: Path) -> None:
    contract = delivery_contract_fixture(tmp_path)
    write(tmp_path / ".codex/AGENTS.md", "# Adapter without global link\n")

    result = validate_delivery_contract.check(tmp_path, contract)

    assert "delivery-contract-adapter-link-invalid" in {item.code for item in result.findings}


def test_delivery_contract_rejects_wrong_global_skill_identity(tmp_path: Path) -> None:
    contract = delivery_contract_fixture(tmp_path)
    write(
        contract.parent.parent / "SKILL.md",
        "---\nname: wrong-skill\n---\n# Wrong\n",
    )

    result = validate_delivery_contract.check(tmp_path, contract)

    assert "delivery-contract-skill-identity-invalid" in {item.code for item in result.findings}


def delivery_ticket(
    path: Path, *, status: str = "ready", blockers: list[str] | None = None
) -> Path:
    blocked_record = ""
    if status == "blocked":
        blocked_record = """blocker_record:
  technical_blocker: The dependent technical discovery has not completed.
  evidence: [AGENTS.md]
  next_safe_action: Complete the named dependency before reopening this ticket.
"""
    return write(
        path,
        f"""---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
ticket_id: {path.stem}
status: {status}
workstream_id: B01
summary: Restore Focus return behavior.
requirement_ids: [ROUTE-006]
blockers: {json.dumps(blockers or [])}
{blocked_record}context_sources: [AGENTS.md]
change_scope:
  allowed_write_paths: [apps/web/**, docs/README.md]
  forbidden_write_paths: [custometry-technical-blueprint-ru.md]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [browser-qa-evidence]
  commands: [pnpm --dir apps/web test]
  proof_boundary: local-browser
  evidence_target: .codex/delivery/evidence/{path.stem}.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---
# Outcome

Restore the route-backed return behavior.

# Non-goals

Do not add a new product capability.

# Acceptance evidence

Record browser evidence at the declared boundary.
""",
    )


def delivery_evidence(
    path: Path,
    *,
    ticket_id: str,
    proof_boundary: str = "local-browser",
    proof_skills: list[str] | None = None,
    verdict: str = "passed",
) -> Path:
    selected_proof_skills = proof_skills if proof_skills is not None else ["browser-qa-evidence"]
    return write(
        path,
        f"""---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
ticket_id: {ticket_id}
proof_boundary: {proof_boundary}
proof_skills: {json.dumps(selected_proof_skills)}
verdict: {verdict}
redaction: No credentials, cookies, or raw browser state retained.
executed_checks: [pnpm --dir apps/web test]
observations: [The declared route return behavior passed in the disposable browser run.]
---

# Outcome and scope

The declared behavior was observed at the named boundary.

# Commands and observations

The focused test completed successfully.

# Verdict

The terminal verdict is recorded in frontmatter.
""",
    )


def test_delivery_tickets_accept_a_ready_vertical_goal(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    delivery_ticket(tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md")

    result = validate_delivery_tickets.check(tmp_path)

    assert result.ok, result.to_dict()
    assert result.details["ready"] == ["B01-FOCUS-RETURN"]


def test_delivery_tickets_allow_repeated_lifecycle_commands(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    ticket = delivery_ticket(tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md")
    ticket.write_text(
        ticket.read_text(encoding="utf-8").replace(
            "commands: [pnpm --dir apps/web test]",
            "commands: [pnpm --dir apps/web test, pnpm --dir apps/web test]",
        ),
        encoding="utf-8",
    )

    assert validate_delivery_tickets.check(tmp_path).ok


def test_delivery_tickets_reject_a_ready_ticket_with_an_open_blocker(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    delivery_ticket(tmp_path / ".codex/delivery/tickets/B01-DISCOVERY.md", status="blocked")
    delivery_ticket(
        tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md",
        blockers=["B01-DISCOVERY"],
    )

    result = validate_delivery_tickets.check(tmp_path)

    assert "delivery-ticket-frontier-invalid" in {item.code for item in result.findings}


def test_delivery_tickets_require_evidence_for_an_accepted_ticket(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    delivery_ticket(tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md", status="accepted")

    result = validate_delivery_tickets.check(tmp_path)

    assert "delivery-ticket-evidence-missing" in {item.code for item in result.findings}


def test_delivery_tickets_require_terminal_evidence_at_the_declared_target(
    tmp_path: Path,
) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    ticket = delivery_ticket(
        tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md",
        status="accepted",
    )
    ticket.write_text(
        ticket.read_text(encoding="utf-8").replace("evidence: []", "evidence: [AGENTS.md]"),
        encoding="utf-8",
    )

    result = validate_delivery_tickets.check(tmp_path)

    assert "delivery-ticket-evidence-target-missing" in {item.code for item in result.findings}


def test_delivery_tickets_accept_structured_terminal_evidence(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    ticket = delivery_ticket(
        tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md",
        status="accepted",
    )
    evidence = delivery_evidence(
        tmp_path / ".codex/delivery/evidence/B01-FOCUS-RETURN.md",
        ticket_id="B01-FOCUS-RETURN",
    )
    ticket.write_text(
        ticket.read_text(encoding="utf-8").replace(
            "evidence: []",
            f"evidence: [{evidence.relative_to(tmp_path)}]",
        ),
        encoding="utf-8",
    )

    assert validate_delivery_tickets.check(tmp_path).ok


def test_delivery_tickets_reject_unstructured_terminal_evidence(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    ticket = delivery_ticket(
        tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md",
        status="accepted",
    )
    evidence = delivery_evidence(
        tmp_path / ".codex/delivery/evidence/B01-FOCUS-RETURN.md",
        ticket_id="B01-FOCUS-RETURN",
        proof_boundary="wrong-boundary",
    )
    ticket.write_text(
        ticket.read_text(encoding="utf-8").replace(
            "evidence: []",
            f"evidence: [{evidence.relative_to(tmp_path)}]",
        ),
        encoding="utf-8",
    )

    result = validate_delivery_tickets.check(tmp_path)

    assert "delivery-ticket-evidence-schema-invalid" in {item.code for item in result.findings}


def test_delivery_tickets_require_browser_qa_for_browser_depth(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    ticket = delivery_ticket(tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md")
    ticket.write_text(
        ticket.read_text(encoding="utf-8").replace(
            "proof_skills: [browser-qa-evidence]",
            "proof_skills: []",
        ),
        encoding="utf-8",
    )

    result = validate_delivery_tickets.check(tmp_path)

    assert "delivery-ticket-validation-invalid" in {item.code for item in result.findings}


def test_delivery_tickets_require_terminal_proof_skill_match(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    ticket = delivery_ticket(
        tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md",
        status="accepted",
    )
    evidence = delivery_evidence(
        tmp_path / ".codex/delivery/evidence/B01-FOCUS-RETURN.md",
        ticket_id="B01-FOCUS-RETURN",
        proof_skills=[],
    )
    ticket.write_text(
        ticket.read_text(encoding="utf-8").replace(
            "evidence: []",
            f"evidence: [{evidence.relative_to(tmp_path)}]",
        ),
        encoding="utf-8",
    )

    result = validate_delivery_tickets.check(tmp_path)

    assert "delivery-ticket-evidence-schema-invalid" in {item.code for item in result.findings}


def test_delivery_tickets_require_supersession_reason_and_matching_evidence(
    tmp_path: Path,
) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    ticket = delivery_ticket(
        tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md",
        status="superseded",
    )
    evidence = delivery_evidence(
        tmp_path / ".codex/delivery/evidence/B01-FOCUS-RETURN.md",
        ticket_id="B01-FOCUS-RETURN",
        verdict="superseded",
    )
    ticket.write_text(
        ticket.read_text(encoding="utf-8").replace(
            "evidence: []",
            f"evidence: [{evidence.relative_to(tmp_path)}]",
        ),
        encoding="utf-8",
    )

    missing_reason = validate_delivery_tickets.check(tmp_path)

    assert "delivery-ticket-supersession-reason-missing" in {
        item.code for item in missing_reason.findings
    }
    ticket.write_text(
        ticket.read_text(encoding="utf-8").replace(
            "summary: Restore Focus return behavior.\n",
            "summary: Restore Focus return behavior.\n"
            "supersession_reason: The replacement ticket owns the corrected behavior.\n",
        ),
        encoding="utf-8",
    )

    assert validate_delivery_tickets.check(tmp_path).ok


def test_delivery_tickets_require_a_blocked_record(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    ticket = delivery_ticket(
        tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md",
        status="blocked",
    )
    ticket.write_text(
        ticket.read_text(encoding="utf-8").replace(
            "blocker_record:\n"
            "  technical_blocker: The dependent technical discovery has not completed.\n"
            "  evidence: [AGENTS.md]\n"
            "  next_safe_action: Complete the named dependency before reopening this ticket.\n",
            "",
        ),
        encoding="utf-8",
    )

    result = validate_delivery_tickets.check(tmp_path)

    assert "delivery-ticket-blocked-record-invalid" in {item.code for item in result.findings}


def test_delivery_tickets_reject_duplicate_execution_mode(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nROUTE-006\n",
    )
    write(tmp_path / "AGENTS.md", "# Repository\n")
    ticket = delivery_ticket(tmp_path / ".codex/delivery/tickets/B01-FOCUS-RETURN.md")
    ticket.write_text(
        ticket.read_text(encoding="utf-8").replace(
            "workstream_id: B01\n",
            "workstream_id: B01\nexecution_mode: goal_driven\n",
        ),
        encoding="utf-8",
    )

    result = validate_delivery_tickets.check(tmp_path)

    assert "delivery-ticket-execution-mode-duplicate" in {item.code for item in result.findings}
