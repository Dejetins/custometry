from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Callable, cast

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
from tools.custometry_quality.core import parse_frontmatter


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
        "plan_template.md",
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


def frontmatter_document(path: Path, metadata: object, body: str) -> Path:
    return write(path, f"---\n{json.dumps(metadata, indent=2)}\n---\n{body}")


def executable_prompt_body() -> str:
    headings = (
        "# Objective",
        "## Non-goals",
        "## Verified current context",
        "## Context acquisition",
        "## Requirements",
        "## Forbidden actions",
        "## Work plan and stop gates",
        "## Contracts and side effects",
        "## Validation and evidence",
        "## Acceptance criteria",
        "## Result and handoff",
    )
    return "\n\n".join(f"{heading}\n\nResolved content." for heading in headings) + "\n"


def staged_program_fixture(tmp_path: Path, *, active_b01: bool = True) -> dict[str, Path]:
    _templates(tmp_path)
    blueprint = write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        '---\nspec_version: "1.0"\n---\n# Blueprint\nREQ-001\n',
    )
    blueprint_digest = hashlib.sha256(blueprint.read_bytes()).hexdigest()
    (tmp_path / "docs/architecture").mkdir(parents=True)
    (tmp_path / ".codex/agents/generated").mkdir(parents=True)
    dump(
        tmp_path / "docs/generated/requirement-index.json",
        {
            "schema_version": 1,
            "spec_version": "1.0",
            "requirements": [{"id": "REQ-001"}],
        },
    )
    workstream_ids = ["W00", *(f"B{number:02d}" for number in range(1, 14)), "W14"]
    staged_ids = workstream_ids[1:]
    dependency_map: dict[str, dict[str, list[str]]] = {
        "W00": {"hard": [], "soft": []},
        "B01": {"hard": ["W00"], "soft": []},
        "B02": {"hard": ["W00"], "soft": ["B01"]},
        "B03": {"hard": ["B01", "B02"], "soft": []},
        "B04": {"hard": ["B02", "B03"], "soft": ["B01"]},
        "B05": {"hard": ["B02", "B03", "B04"], "soft": ["B01"]},
        "B06": {
            "hard": ["B01", "B02", "B03", "B04", "B05"],
            "soft": [],
        },
        "B07": {"hard": ["B01", "B03", "B04", "B06"], "soft": ["B05"]},
        "B08": {
            "hard": ["B01", "B03", "B04", "B05", "B06"],
            "soft": ["B07"],
        },
        "B09": {"hard": ["B04", "B05", "B06", "B08"], "soft": ["B07"]},
        "B10": {
            "hard": ["B01", "B03", "B04", "B05", "B06", "B07", "B08", "B09"],
            "soft": [],
        },
        "B11": {
            "hard": ["B04", "B07", "B10"],
            "soft": ["B05", "B08", "B09"],
        },
        "B12": {
            "hard": [f"B{number:02d}" for number in range(1, 11)],
            "soft": ["B11"],
        },
        "B13": {
            "hard": ["B10", "B11", "B12"],
            "soft": ["B06", "B08", "B09"],
        },
        "W14": {"hard": list(staged_ids[:-1]), "soft": []},
    }
    release_map: dict[str, list[str]] = {
        "W00": ["repository_foundation"],
        "B01": ["product_foundation", "vertical_alpha", "public_mvp", "v1_target"],
        "B02": ["product_foundation", "vertical_alpha", "public_mvp", "v1_target"],
        "B03": ["product_foundation", "vertical_alpha", "public_mvp", "v1_target"],
        "B04": ["product_foundation", "vertical_alpha", "public_mvp", "v1_target"],
        "B05": ["vertical_alpha", "public_mvp", "v1_target"],
        "B06": ["vertical_alpha", "public_mvp", "v1_target"],
        "B07": ["public_mvp", "v1_target"],
        "B08": ["public_mvp", "v1_target"],
        "B09": ["public_mvp", "v1_target"],
        "B10": ["public_mvp", "v1_target"],
        "B11": ["v1_target"],
        "B12": ["public_mvp", "v1_feature_freeze", "v1_target"],
        "B13": ["v1_feature_freeze", "v1_target"],
        "W14": ["v1_target"],
    }
    workstreams: list[dict[str, object]] = [
        {
            "workstream_id": "W00",
            "kind": "foundation_baseline",
            "hard_dependencies": [],
            "soft_dependencies": [],
            "release_milestones": ["repository_foundation"],
        }
    ]
    paths: dict[str, Path] = {}
    for workstream_id in staged_ids:
        slug = workstream_id.lower()
        plan_rel = f"docs/architecture/workstreams/{slug}-plan.md"
        pack_rel = f".codex/agents/generated/{slug}"
        ledger_rel = (
            f"docs/architecture/workstreams/{slug}-stage-reports/{slug}-stage-ledger.md"
        )
        hard_dependencies = dependency_map[workstream_id]["hard"]
        soft_dependencies = dependency_map[workstream_id]["soft"]
        milestones = release_map[workstream_id]
        entry: dict[str, object] = {
            "workstream_id": workstream_id,
            "kind": "acceptance_bookend" if workstream_id == "W14" else "delivery",
            "hard_dependencies": hard_dependencies,
            "soft_dependencies": soft_dependencies,
            "release_milestones": milestones,
            "plan_doc": plan_rel,
            "prompt_pack_dir": pack_rel,
            "stage_ledger": ledger_rel,
        }
        if workstream_id != "W14":
            module_rel = f"docs/architecture/workstreams/{slug}-module.md"
            entry["module_definition"] = module_rel
            frontmatter_document(
                tmp_path / module_rel,
                {
                    "artifact_kind": "module_definition",
                    "staged_schema_version": 1,
                    "workstream_id": workstream_id,
                    "product_spec_version": "1.0",
                    "requirement_ids": ["REQ-001"]
                    if workstream_id == "B01"
                    else [],
                },
                f"# {workstream_id} module\n",
            )
            paths[f"{workstream_id}_module"] = tmp_path / module_rel
        workstreams.append(entry)
        plan_metadata: dict[str, object] = {
            "artifact_kind": "workstream_plan",
            "staged_schema_version": 1,
            "workstream_id": workstream_id,
            "plan_maturity": "detailed" if workstream_id in {"B01", "B02"} else "initial",
            "program_plan": "docs/architecture/program/custometry-program-plan.md",
            "plan_doc": plan_rel,
            "prompt_pack_dir": pack_rel,
            "stage_ledger": ledger_rel,
            "execution_mode": "goal_driven",
            "hard_dependencies": hard_dependencies,
            "soft_dependencies": soft_dependencies,
            "stage_ids": [f"S{number:02d}" for number in range(7)],
            "release_milestones": milestones,
            "spec_version": "1.0",
            "requirement_ids": ["REQ-001"],
        }
        if workstream_id != "W14":
            plan_metadata["module_definition"] = entry["module_definition"]
        frontmatter_document(
            tmp_path / plan_rel,
            plan_metadata,
            f"# {workstream_id} plan\n",
        )
        executable = workstream_id in {"B01", "B02"}
        stages: list[dict[str, object]] = []
        for stage_number in range(7):
            stage_id = f"S{stage_number:02d}"
            prompt_rel = f"{pack_rel}/{stage_id}-{stage_id.lower()}.md"
            stages.append(
                {
                    "stage_id": stage_id,
                    "status": "pending",
                    "prompt_path": prompt_rel,
                    "prompt_readiness": "executable" if executable else "outline",
                    "previous_gate": None if stage_number == 0 else f"S{stage_number - 1:02d}",
                    "next_allowed": active_b01
                    and workstream_id == "B01"
                    and stage_number == 0,
                    "requirement_ids": ["REQ-001"],
                    "evidence": [],
                    "blocker": None,
                    "supersedes": [],
                }
            )
            next_stage = f"S{stage_number + 1:02d}" if stage_number < 6 else None
            prompt_metadata: dict[str, object] = {
                "prompt_name": f"{workstream_id.lower()}-{stage_id.lower()}",
                "scope": "Resolved staged outcome",
                "spec_version": "1.0",
                "requirement_ids": ["REQ-001"],
                "prompt_pack_execution": {
                    "staged_schema_version": 1,
                    "readiness": "executable" if executable else "outline",
                    "enabled": executable,
                    "workstream_id": workstream_id,
                    "execution_mode": "goal_driven",
                    "plan_doc": plan_rel,
                    "prompt_pack_dir": pack_rel,
                    "stage_ledger": ledger_rel,
                    "stage_id": stage_id,
                    "predecessor_gate": {
                        "stage_id": None if stage_number == 0 else f"S{stage_number - 1:02d}",
                        "allowed_statuses": []
                        if stage_number == 0
                        else ["accepted", "superseded"],
                    },
                    "state_preconditions": [],
                    "required_source_hashes": (
                        {
                            "custometry-technical-blueprint-ru.md": (
                                f"sha256:{blueprint_digest}"
                            )
                        }
                        if active_b01
                        and workstream_id == "B01"
                        and stage_number == 0
                        else {}
                    ),
                    "branch_policy": {
                        "default_branch": "main",
                        "separate_branch_requested": True,
                        "allowed_branch": f"codex/{workstream_id.lower()}",
                        "per_stage_branches": "forbidden",
                    },
                    "next_stage_rule": {
                        "candidate_stage": next_stage,
                        "unlock_on": "accepted",
                        "authority": "stage_ledger",
                    },
                },
            }
            frontmatter_document(
                tmp_path / prompt_rel,
                prompt_metadata,
                executable_prompt_body() if executable else "# Outline\n",
            )
        ledger_metadata = {
            "artifact_kind": "stage_ledger",
            "staged_schema_version": 1,
            "ledger_name": f"{slug}-stage-ledger",
            "workstream_id": workstream_id,
            "plan_doc": plan_rel,
            "prompt_pack_dir": pack_rel,
            "stage_ledger": ledger_rel,
            "execution_mode": "goal_driven",
            "ledger_status": "active"
            if active_b01 and workstream_id == "B01"
            else "dormant",
            "current_stage": "S00",
            "allowed_stage_statuses": [
                "pending",
                "in_progress",
                "accepted",
                "blocked",
                "skipped",
                "superseded",
            ],
            "spec_version": "1.0",
            "updated_at": "2026-07-16",
            "stages": stages,
        }
        frontmatter_document(
            tmp_path / ledger_rel,
            ledger_metadata,
            f"# {workstream_id} ledger\n",
        )
        paths[f"{workstream_id}_plan"] = tmp_path / plan_rel
        paths[f"{workstream_id}_ledger"] = tmp_path / ledger_rel
        paths[f"{workstream_id}_S00"] = tmp_path / f"{pack_rel}/S00-s00.md"
    program_metadata = {
        "artifact_kind": "program_plan",
        "staged_schema_version": 1,
        "program_id": "custometry-v1",
        "execution_mode": "goal_driven",
        "spec_version": "1.0",
        "requirement_matrix": "docs/architecture/program/requirement-traceability.json",
        "requirement_routing": "docs/architecture/program/requirement-routing.json",
        "workstreams": workstreams,
        "release_milestones": [
            {
                "milestone_id": "repository_foundation",
                "terminal_workstream": "W00",
                "terminal_stage": "foundation_proof",
            },
            {
                "milestone_id": "product_foundation",
                "terminal_workstream": "B04",
                "terminal_stage": "S06",
            },
            {
                "milestone_id": "vertical_alpha",
                "terminal_workstream": "B06",
                "terminal_stage": "S06",
            },
            {
                "milestone_id": "public_mvp",
                "terminal_workstream": "B12",
                "terminal_stage": "S05",
            },
            {
                "milestone_id": "v1_feature_freeze",
                "terminal_workstream": "B13",
                "terminal_stage": "S06",
            },
            {
                "milestone_id": "v1_target",
                "terminal_workstream": "W14",
                "terminal_stage": "S06",
            },
        ],
    }
    program_path = frontmatter_document(
        tmp_path / "docs/architecture/program/custometry-program-plan.md",
        program_metadata,
        "# Program\n",
    )
    dump(
        tmp_path / "docs/architecture/program/requirement-routing.json",
        {
            "schema_version": 1,
            "spec_version": "1.0",
            "milestones": [
                "repository_foundation",
                "product_foundation",
                "vertical_alpha",
                "public_mvp",
                "v1_feature_freeze",
                "v1_target",
            ],
            "terminal_milestones": {
                "repository_foundation": "W00",
                "product_foundation": "B04",
                "vertical_alpha": "B06",
                "public_mvp": "B12",
                "v1_feature_freeze": "B13",
                "v1_target": "W14",
            },
            "milestone_terminal_stages": {
                "repository_foundation": "foundation_proof",
                "product_foundation": "S06",
                "vertical_alpha": "S06",
                "public_mvp": "S05",
                "v1_feature_freeze": "S06",
                "v1_target": "S06",
            },
            "workstream_release_milestones": release_map,
            "workstream_dependencies": dependency_map,
        },
    )
    dump(
        tmp_path / "docs/architecture/program/requirement-traceability.json",
        {
            "schema_version": 1,
            "spec_version": "1.0",
            "requirements": [
                {
                    "requirement_id": "REQ-001",
                    "primary_workstream": "B01",
                    "contributing_workstreams": [
                        *(f"B{number:02d}" for number in range(2, 14)),
                        "W14",
                    ],
                    "implementation_evidence": ["source"],
                    "acceptance_evidence": ["browser"],
                    "first_required_milestone": "product_foundation",
                    "status": "allocated",
                }
            ],
        },
    )
    active_entries: list[dict[str, object]] = []
    if active_b01:
        b01 = workstreams[1]
        active_entries.append(
            {
                "workstream_id": "B01",
                **{key: b01[key] for key in ("plan_doc", "prompt_pack_dir", "stage_ledger")},
            }
        )
    registry_metadata: dict[str, object] = {
        "registry_schema_version": 1,
        "program_plan": "docs/architecture/program/custometry-program-plan.md",
        "execution_mode": "goal_driven",
        "active_workstreams": active_entries,
    }
    frontmatter_document(
        tmp_path / ".codex/PLANS.md",
        registry_metadata,
        "# Plan registry\n",
    )
    paths["program"] = program_path
    paths["matrix"] = tmp_path / "docs/architecture/program/requirement-traceability.json"
    paths["routing"] = tmp_path / "docs/architecture/program/requirement-routing.json"
    return paths


def mutate_frontmatter(
    path: Path,
    mutate: Callable[[dict[str, object]], None],
) -> None:
    meta, body = parse_frontmatter(path)
    mutable_meta: dict[str, object] = {key: value for key, value in meta.items()}
    mutate(mutable_meta)
    frontmatter_document(path, mutable_meta, body)


def test_staged_workstream_schema_v1_accepts_active_and_dormant_packs(
    tmp_path: Path,
) -> None:
    paths = staged_program_fixture(tmp_path)
    result = validate_staged_workstream.check(tmp_path)
    assert result.ok, result.to_dict()
    assert result.details["workstreams"] == 14
    assert result.details["active_workstreams"] == ["B01"]
    assert paths["B02_S00"].is_file()


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("active-outline", "active-ledger-outline-forbidden"),
        ("cross-link", "staged-trio-link-mismatch"),
        ("cycle", "program-dependency-cycle"),
        ("program-execution-mode", "program-execution-mode-invalid"),
        ("plan-execution-mode", "plan-execution-mode-invalid"),
        ("ledger-execution-mode", "ledger-execution-mode-invalid"),
        ("prompt-execution-mode", "prompt-execution-mode-invalid"),
        ("registry-execution-mode", "plans-registry-execution-mode-invalid"),
        ("public-mvp-hard-gated-by-b11", "public-mvp-dependency-gate-invalid"),
        ("public-mvp-stage-drift", "requirement-routing-gate-drift"),
        ("matrix-incomplete", "requirement-matrix-incomplete"),
        (
            "matrix-owner-outside-first-milestone",
            "requirement-primary-owner-outside-first-milestone",
        ),
        ("registry-drift", "plans-registry-active-drift"),
        ("placeholder", "executable-prompt-placeholder"),
        ("active-empty-source-hashes", "source-hash-gate-empty"),
        ("active-stale-source-hash", "source-hash-mismatch"),
        ("stage-coverage-missing", "plan-stage-requirement-coverage-drift"),
        ("stage-coverage-extra", "plan-stage-requirement-coverage-drift"),
    ],
)
def test_staged_workstream_schema_v1_rejects_contract_drift(
    tmp_path: Path,
    mutation: str,
    expected_code: str,
) -> None:
    paths = staged_program_fixture(tmp_path)
    if mutation == "active-outline":
        def ledger_outline(meta: dict[str, object]) -> None:
            stages = cast(list[dict[str, object]], meta["stages"])
            stages[0]["prompt_readiness"] = "outline"

        def prompt_outline(meta: dict[str, object]) -> None:
            execution = cast(dict[str, object], meta["prompt_pack_execution"])
            execution["readiness"] = "outline"
            execution["enabled"] = False

        mutate_frontmatter(paths["B01_ledger"], ledger_outline)
        mutate_frontmatter(paths["B01_S00"], prompt_outline)
    elif mutation == "cross-link":
        def cross_link(meta: dict[str, object]) -> None:
            execution = cast(dict[str, object], meta["prompt_pack_execution"])
            execution["plan_doc"] = "docs/architecture/workstreams/b02-plan.md"

        mutate_frontmatter(paths["B01_S00"], cross_link)
    elif mutation == "cycle":
        def cycle(meta: dict[str, object]) -> None:
            workstreams = cast(list[dict[str, object]], meta["workstreams"])
            workstreams[0]["hard_dependencies"] = ["B01"]

        mutate_frontmatter(paths["program"], cycle)
    elif mutation == "program-execution-mode":
        mutate_frontmatter(
            paths["program"],
            lambda meta: meta.__setitem__("execution_mode", "unsupported"),
        )
    elif mutation == "plan-execution-mode":
        mutate_frontmatter(
            paths["B01_plan"],
            lambda meta: meta.__setitem__("execution_mode", "unsupported"),
        )
    elif mutation == "ledger-execution-mode":
        mutate_frontmatter(
            paths["B01_ledger"],
            lambda meta: meta.__setitem__("execution_mode", "unsupported"),
        )
    elif mutation == "prompt-execution-mode":
        def unsupported_prompt_mode(meta: dict[str, object]) -> None:
            execution = cast(dict[str, object], meta["prompt_pack_execution"])
            execution["execution_mode"] = "unsupported"

        mutate_frontmatter(paths["B01_S00"], unsupported_prompt_mode)
    elif mutation == "registry-execution-mode":
        mutate_frontmatter(
            tmp_path / ".codex/PLANS.md",
            lambda meta: meta.__setitem__("execution_mode", "unsupported"),
        )
    elif mutation == "public-mvp-hard-gated-by-b11":
        routing = json.loads(paths["routing"].read_text(encoding="utf-8"))
        routing["workstream_dependencies"]["B12"]["hard"].append("B11")
        routing["workstream_dependencies"]["B12"]["soft"] = []
        dump(paths["routing"], routing)
    elif mutation == "public-mvp-stage-drift":
        routing = json.loads(paths["routing"].read_text(encoding="utf-8"))
        routing["milestone_terminal_stages"]["public_mvp"] = "S06"
        dump(paths["routing"], routing)
    elif mutation == "matrix-incomplete":
        dump(
            tmp_path / "docs/generated/requirement-index.json",
            {
                "schema_version": 1,
                "spec_version": "1.0",
                "requirements": [{"id": "REQ-001"}, {"id": "REQ-002"}],
            },
        )
    elif mutation == "matrix-owner-outside-first-milestone":
        matrix = json.loads(paths["matrix"].read_text(encoding="utf-8"))
        allocation = matrix["requirements"][0]
        allocation["primary_workstream"] = "B13"
        allocation["contributing_workstreams"] = [
            item for item in allocation["contributing_workstreams"] if item != "B13"
        ]
        allocation["contributing_workstreams"].append("B01")
        dump(paths["matrix"], matrix)
    elif mutation == "registry-drift":
        def registry_drift(meta: dict[str, object]) -> None:
            meta["active_workstreams"] = []

        mutate_frontmatter(tmp_path / ".codex/PLANS.md", registry_drift)
    elif mutation == "placeholder":
        path = paths["B01_S00"]
        meta, body = parse_frontmatter(path)
        frontmatter_document(path, meta, body + "\nTBD\n")
    elif mutation == "active-empty-source-hashes":
        def empty_hashes(meta: dict[str, object]) -> None:
            execution = cast(dict[str, object], meta["prompt_pack_execution"])
            execution["required_source_hashes"] = {}

        mutate_frontmatter(paths["B01_S00"], empty_hashes)
    elif mutation == "active-stale-source-hash":
        def stale_hash(meta: dict[str, object]) -> None:
            execution = cast(dict[str, object], meta["prompt_pack_execution"])
            execution["required_source_hashes"] = {
                "custometry-technical-blueprint-ru.md": f"sha256:{'0' * 64}"
            }

        mutate_frontmatter(paths["B01_S00"], stale_hash)
    elif mutation == "stage-coverage-missing":
        def clear_ledger_requirements(meta: dict[str, object]) -> None:
            stages = cast(list[dict[str, object]], meta["stages"])
            for stage in stages:
                stage["requirement_ids"] = []

        def clear_prompt_requirements(meta: dict[str, object]) -> None:
            meta["requirement_ids"] = []

        mutate_frontmatter(paths["B01_ledger"], clear_ledger_requirements)
        for prompt in sorted(paths["B01_S00"].parent.glob("S*.md")):
            mutate_frontmatter(prompt, clear_prompt_requirements)
    elif mutation == "stage-coverage-extra":
        def add_ledger_requirement(meta: dict[str, object]) -> None:
            stages = cast(list[dict[str, object]], meta["stages"])
            requirements = cast(list[str], stages[0]["requirement_ids"])
            requirements.append("REQ-EXTRA")

        def add_prompt_requirement(meta: dict[str, object]) -> None:
            requirements = cast(list[str], meta["requirement_ids"])
            requirements.append("REQ-EXTRA")

        mutate_frontmatter(paths["B01_ledger"], add_ledger_requirement)
        mutate_frontmatter(paths["B01_S00"], add_prompt_requirement)
    failed = validate_staged_workstream.check(tmp_path)
    assert expected_code in {item.code for item in failed.findings}, failed.to_dict()


def test_staged_workstream_dormant_hash_is_not_revalidated(tmp_path: Path) -> None:
    paths = staged_program_fixture(tmp_path)
    source = write(tmp_path / "source.txt", "changed\n")

    def stale_dormant_hash(meta: dict[str, object]) -> None:
        execution = cast(dict[str, object], meta["prompt_pack_execution"])
        execution["required_source_hashes"] = {
            source.relative_to(tmp_path).as_posix(): f"sha256:{'0' * 64}"
        }

    mutate_frontmatter(paths["B02_S00"], stale_dormant_hash)
    result = validate_staged_workstream.check(tmp_path)
    assert result.ok, result.to_dict()


@pytest.mark.parametrize("status", ["open", "reference_only"])
def test_staged_workstream_accepts_canonical_matrix_statuses(
    tmp_path: Path,
    status: str,
) -> None:
    paths = staged_program_fixture(tmp_path)
    matrix = json.loads(paths["matrix"].read_text(encoding="utf-8"))
    matrix["requirements"][0]["status"] = status
    dump(paths["matrix"], matrix)
    result = validate_staged_workstream.check(tmp_path)
    assert result.ok, result.to_dict()


def test_staged_workstream_allows_goal_prohibition_text_but_rejects_goal_file(
    tmp_path: Path,
) -> None:
    paths = staged_program_fixture(tmp_path)
    ledger = paths["B01_ledger"]
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + "\nDo not create GOAL.md.\n",
        encoding="utf-8",
    )
    allowed = validate_staged_workstream.check(tmp_path)
    assert allowed.ok, allowed.to_dict()

    write(tmp_path / ".codex/GOAL.md", "# Unapproved coordination source\n")
    failed = validate_staged_workstream.check(tmp_path)
    assert "forbidden-coordination-source" in {
        finding.code for finding in failed.findings
    }


def test_staged_workstream_rejects_missing_primary_and_unrouted_supporting_ids(
    tmp_path: Path,
) -> None:
    paths = staged_program_fixture(tmp_path)
    dump(
        tmp_path / "docs/generated/requirement-index.json",
        {
            "schema_version": 1,
            "spec_version": "1.0",
            "requirements": [{"id": "REQ-001"}, {"id": "REQ-002"}],
        },
    )
    matrix = json.loads(paths["matrix"].read_text(encoding="utf-8"))
    matrix["requirements"].append(
        {
            "requirement_id": "REQ-002",
            "primary_workstream": "B01",
            "contributing_workstreams": [],
            "implementation_evidence": ["source"],
            "acceptance_evidence": ["browser"],
            "status": "allocated",
        }
    )
    dump(paths["matrix"], matrix)
    mutate_frontmatter(
        tmp_path / "docs/architecture/workstreams/b02-plan.md",
        lambda meta: cast(list[str], meta["requirement_ids"]).append("REQ-002"),
    )
    result = validate_staged_workstream.check(tmp_path)
    codes = {finding.code for finding in result.findings}
    assert "plan-primary-requirements-missing" in codes
    assert "plan-supporting-requirements-invalid" in codes


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("schema", "module-schema-invalid"),
        ("workstream", "module-workstream-id-drift"),
        ("version", "module-spec-version-drift"),
        ("requirements", "module-primary-requirements-drift"),
    ],
)
def test_staged_workstream_validates_module_definition_contract(
    tmp_path: Path,
    mutation: str,
    expected_code: str,
) -> None:
    paths = staged_program_fixture(tmp_path)

    def change(meta: dict[str, object]) -> None:
        if mutation == "schema":
            meta["artifact_kind"] = "architecture_note"
        elif mutation == "workstream":
            meta["workstream_id"] = "B02"
        elif mutation == "version":
            meta["product_spec_version"] = "2.0"
        else:
            meta["requirement_ids"] = []

    mutate_frontmatter(paths["B01_module"], change)
    result = validate_staged_workstream.check(tmp_path)
    assert expected_code in {finding.code for finding in result.findings}


def test_staged_workstream_accepts_empty_pre_program_repository(tmp_path: Path) -> None:
    _templates(tmp_path)
    (tmp_path / "docs/architecture").mkdir(parents=True)
    (tmp_path / ".codex/agents/generated").mkdir(parents=True)
    assert validate_staged_workstream.check(tmp_path).ok


def test_plan_template_version_is_checked_with_other_agent_templates(tmp_path: Path) -> None:
    write(
        tmp_path / "custometry-technical-blueprint-ru.md",
        "---\nspec_version: 1.0\n---\n# Blueprint\nREQ-001\n",
    )
    instructions = (
        "Result reports status, mode, contract impact, next owner. "
        "Complete, partial and blocked are defined."
    )
    write(
        tmp_path / ".codex/agents/qa.toml",
        'name="qa"\ndescription="Use for QA. Do not use for implementation."\n'
        f'developer_instructions="{instructions}"\n',
    )
    _templates(tmp_path, version="1.0")
    assert validate_agent_profiles.check(tmp_path).ok
    plan_template = tmp_path / ".codex/agents/plan_template.md"
    plan_template.write_text(
        plan_template.read_text(encoding="utf-8").replace("1.0", "2.0"),
        encoding="utf-8",
    )
    failed = validate_agent_profiles.check(tmp_path)
    assert any(
        item.code == "agent-template-version-drift" and item.path == str(plan_template)
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
