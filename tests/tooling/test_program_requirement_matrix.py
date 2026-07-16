from __future__ import annotations

import copy
from pathlib import Path
from typing import cast

import pytest

from tools.custometry_quality import (
    generate_program_requirement_matrix,
    validate_staged_workstream,
)
from tools.custometry_quality.core import (
    JsonValue,
    json_list,
    json_object,
    json_string,
    load_json,
)


ROOT = Path(__file__).resolve().parents[2]
INDEX = Path("docs/generated/requirement-index.json")
ROUTING = Path("docs/architecture/program/requirement-routing.json")
MATRIX = Path("docs/architecture/program/requirement-matrix.json")
PROGRAM = Path("docs/architecture/program/custometry-program-plan.md")


def test_program_requirement_matrix_is_exact_and_staged_validator_compatible() -> None:
    generated = generate_program_requirement_matrix.check(
        ROOT,
        index_path=INDEX,
        routing_path=ROUTING,
        output_path=MATRIX,
        check_mode=True,
    )
    assert generated.ok, generated.findings
    assert generated.details["requirements"] == 649
    assert generated.details["unique_requirements"] == 649
    assert generated.details["workstreams"] == 14

    index = load_json(ROOT / INDEX)
    requirement_ids = frozenset(
        json_string(
            json_object(item, f"requirements[{position}]").get("id"),
            f"requirements[{position}].id",
        )
        for position, item in enumerate(
            json_list(index.get("requirements"), "requirements")
        )
    )
    assert len(requirement_ids) == 649
    validation = validate_staged_workstream.check(ROOT)
    matrix_findings = [
        finding
        for finding in validation.findings
        if finding.path == str(ROOT / MATRIX)
    ]
    assert not matrix_findings, matrix_findings


def test_program_requirement_matrix_rejects_duplicate_primary_allocation() -> None:
    index = load_json(ROOT / INDEX)
    routing = copy.deepcopy(load_json(ROOT / ROUTING))
    rules = json_list(routing.get("rules"), "rules")
    duplicated = copy.deepcopy(json_object(rules[0], "rules[0]"))
    duplicated["selectors"] = cast(JsonValue, ["DOC-RULE-001"])
    rules.append(duplicated)

    with pytest.raises(ValueError, match="routed more than once"):
        generate_program_requirement_matrix.build_matrix(index, routing)


def test_program_requirement_matrix_rejects_primary_owner_after_first_milestone() -> None:
    index = load_json(ROOT / INDEX)
    routing = copy.deepcopy(load_json(ROOT / ROUTING))
    rules = json_list(routing.get("rules"), "rules")
    rule = json_object(rules[0], "rules[0]")
    rule["primary_workstream"] = "B13"
    rule["contributing_workstreams"] = cast(JsonValue, [])

    with pytest.raises(
        ValueError,
        match="primary workstream B13.*cannot satisfy first milestone",
    ):
        generate_program_requirement_matrix.build_matrix(index, routing)


def test_program_requirement_matrix_cli_and_grouped_gate_are_wired() -> None:
    args = generate_program_requirement_matrix.build_parser().parse_args(
        ["--routing", str(ROUTING), "--check"]
    )
    assert args.routing == ROUTING
    assert args.check is True
    orchestrator = (ROOT / "tools/custometry_quality/check.py").read_text(
        encoding="utf-8"
    )
    project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"program-requirements"' in orchestrator
    assert "custometry-generate-program-requirement-matrix" in project
