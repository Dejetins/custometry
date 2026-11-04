"""C01 pure contract fixtures; these do not exercise an API writer or database."""

from copy import deepcopy
from uuid import uuid4

import pytest
from pydantic import ValidationError

from packages.contracts.presentation.composer import (
    ComposerDefinitionV1,
    ComposerSaveRequest,
    GridPlacement,
    duplicate_block,
    input_fingerprint,
)
from packages.contracts.presentation.workspace import ConfiguredReportV2
from tests.contract.presentation.test_workspace import definition as legacy_definition


def fixture() -> dict:
    legacy = legacy_definition()
    page, section, source = [str(uuid4()) for _ in range(3)]
    metric = legacy["worksets"][0]["cards"][0]["metric_ref"]
    return {
        "schema_version": "analytical-authoring/v1",
        "document_id": str(uuid4()),
        "creator_principal_id": legacy["creator_principal_id"],
        "profile": "workbook_report",
        "title": "Synthetic multi-block report",
        "brand_profile": legacy["brand_profile"],
        "company_pack": legacy["company_pack"],
        "default_page_id": page,
        "pages": [{"page_id": page, "order": 0, "title": "Overview", "layout": "dashboard_grid"}],
        "sections": [{"section_id": section, "page_id": page, "order": 0, "title": "Results"}],
        "blocks": [
            {
                "block_id": str(uuid4()), "section_id": section, "order": i,
                "block_type": "chart" if i < 4 else "table",
                "source": {"definition_id": source, "metric_ref": deepcopy(metric)},
                "presentation": {"title": f"Block {i}"},
                "placement": {"column": (i % 2) * 6, "span": 6, "row": i // 2},
            }
            for i in range(6)
        ],
        "definitions": [{
            "definition_id": source,
            "query": {
                "semantic_dataset_version_id": legacy["semantic_dataset_version_id"],
                "common": legacy["common_context"],
                "local_store_ids": None,
                "grain": legacy["grain"],
                "calendar_ref": legacy["calendar_ref"],
                "calendar_basis": legacy["calendar_basis"],
                "alignment": "none",
                "metric_refs": [deepcopy(metric)],
            },
        }],
    }


def test_four_charts_two_tables_round_trip_and_shared_analytical_input():
    value = ComposerDefinitionV1.model_validate(fixture())
    assert ComposerDefinitionV1.model_validate_json(value.model_dump_json()) == value
    assert [b.block_type for b in value.blocks].count("chart") == 4
    assert [b.block_type for b in value.blocks].count("table") == 2
    assert len({b.source.definition_id for b in value.blocks}) == 1


@pytest.mark.parametrize("layout", ["flow", "narrative"])
def test_standalone_table_and_empty_document_require_no_chart(layout):
    raw = fixture()
    raw["pages"][0]["layout"] = layout
    raw["blocks"] = [raw["blocks"][-1]]
    raw["blocks"][0]["placement"] = None
    value = ComposerDefinitionV1.model_validate(raw)
    assert len(value.blocks) == 1 and value.blocks[0].block_type == "table"
    raw.update(blocks=[], definitions=[])
    assert ComposerDefinitionV1.model_validate(raw).blocks == []


@pytest.mark.parametrize("case", [
    "duplicate_id", "document_id_reused", "duplicate_order", "unknown_default_page",
    "unknown_chapter", "unknown_page", "unknown_section", "unknown_source", "wrong_metric",
    "unused_definition", "duplicate_metric", "orphan_parent", "cross_page_parent", "cycle",
    "missing_placement", "flow_placement", "overlap", "overflow", "negative_order",
    "boolean_order", "unsupported_version", "unsupported_block", "unsafe_presentation",
    "unsafe_binding", "raw_sql", "nonfinite_position", "fractional_position",
])
def test_invalid_graph_or_untyped_input_fails_closed(case):
    raw = fixture()
    block, section, query = raw["blocks"][0], raw["sections"][0], raw["definitions"][0]["query"]
    if case == "duplicate_id":
        raw["blocks"][1]["block_id"] = block["block_id"]
    elif case == "document_id_reused":
        block["block_id"] = raw["document_id"]
    elif case == "duplicate_order":
        raw["blocks"][1]["order"] = block["order"]
    elif case == "unknown_default_page":
        raw["default_page_id"] = str(uuid4())
    elif case == "unknown_chapter":
        raw["pages"][0]["chapter_id"] = str(uuid4())
    elif case == "unknown_page":
        section["page_id"] = str(uuid4())
    elif case == "unknown_section":
        block["section_id"] = str(uuid4())
    elif case == "unknown_source":
        block["source"]["definition_id"] = str(uuid4())
    elif case == "wrong_metric":
        block["source"]["metric_ref"]["content_hash"] = "b" * 64
    elif case == "unused_definition":
        raw["definitions"].append({**deepcopy(raw["definitions"][0]), "definition_id": str(uuid4())})
    elif case == "duplicate_metric":
        query["metric_refs"].append(deepcopy(query["metric_refs"][0]))
    elif case == "orphan_parent":
        section["parent_section_id"] = str(uuid4())
    elif case == "cross_page_parent":
        p = {**raw["pages"][0], "page_id": str(uuid4()), "order": 1}
        raw["pages"].append(p)
        s = {**section, "section_id": str(uuid4()), "page_id": p["page_id"]}
        raw["sections"].append(s)
        section["parent_section_id"] = s["section_id"]
    elif case == "cycle":
        s = {**section, "section_id": str(uuid4()), "parent_section_id": section["section_id"]}
        raw["sections"].append(s)
        section["parent_section_id"] = s["section_id"]
    elif case == "missing_placement":
        block["placement"] = None
    elif case == "flow_placement":
        raw["pages"][0]["layout"] = "flow"
    elif case == "overlap":
        raw["blocks"][1]["placement"] = deepcopy(block["placement"])
    elif case == "overflow":
        block["placement"].update(column=10, span=6)
    elif case == "negative_order":
        block["order"] = -1
    elif case == "boolean_order":
        block["order"] = True
    elif case == "unsupported_version":
        raw["schema_version"] = "configured-report/v2"
    elif case == "unsupported_block":
        block["block_type"] = "forecast"
    elif case == "unsafe_presentation":
        block["presentation"]["library_options"] = {"formatter": "untrusted"}
    elif case == "unsafe_binding":
        block["source"]["url"] = "https://invalid.example/"
    elif case == "raw_sql":
        query["sql"] = "select 1"
    elif case == "nonfinite_position":
        block["placement"]["row"] = float("inf")
    elif case == "fractional_position":
        block["placement"]["row"] = 0.5
    with pytest.raises(ValidationError):
        ComposerDefinitionV1.model_validate(raw)


def test_copy_has_fresh_block_and_definition_ids_without_mutating_original():
    value = ComposerDefinitionV1.model_validate(fixture())
    before = value.model_dump_json()
    result = duplicate_block(
        value, value.blocks[0].block_id, section_id=value.sections[0].section_id,
        order=6, placement=GridPlacement(row=3),
    )
    assert result.blocks[-1].block_id not in {b.block_id for b in value.blocks}
    assert result.blocks[-1].source.definition_id != value.blocks[0].source.definition_id
    assert input_fingerprint(result.definitions[-1]) == input_fingerprint(value.definitions[0])
    assert value.model_dump_json() == before
    raw = result.model_dump(mode="json")
    raw["definitions"][-1]["query"]["grain"] = "month"
    edited = ComposerDefinitionV1.model_validate(raw)
    assert input_fingerprint(edited.definitions[-1]) != input_fingerprint(value.definitions[0])
    assert input_fingerprint(edited.definitions[0]) == input_fingerprint(value.definitions[0])


def test_layout_density_title_order_do_not_change_analytical_input():
    value = ComposerDefinitionV1.model_validate(fixture())
    raw = value.model_dump(mode="json")
    raw["title"] = "Renamed"
    raw["blocks"][0]["presentation"].update(title="Changed", density="compact", legend=False)
    raw["blocks"][0]["placement"]["row"] = 20
    raw["blocks"][0]["order"] = 10
    changed = ComposerDefinitionV1.model_validate(raw)
    assert changed != value
    assert input_fingerprint(changed.definitions[0]) == input_fingerprint(value.definitions[0])


def test_legacy_readers_unchanged_and_new_format_cannot_masquerade_as_v2():
    raw = legacy_definition()
    before = deepcopy(raw)
    legacy = ConfiguredReportV2.model_validate(raw)
    assert raw == before
    assert ConfiguredReportV2.model_validate_json(legacy.model_dump_json()) == legacy
    with pytest.raises(ValidationError):
        ConfiguredReportV2.model_validate(fixture())
    with pytest.raises(ValidationError):
        ComposerDefinitionV1.model_validate(raw)


def test_save_request_requires_explicit_version_cas_key_and_closed_definition():
    raw = {
        "contract_version": "analytical-authoring/v1", "definition": fixture(),
        "expected_revision": 0, "idempotency_key": str(uuid4()),
    }
    assert ComposerSaveRequest.model_validate(raw).expected_revision == 0
    for field in ("contract_version", "expected_revision", "idempotency_key"):
        candidate = deepcopy(raw)
        del candidate[field]
        with pytest.raises(ValidationError):
            ComposerSaveRequest.model_validate(candidate)
    raw["expected_revision"] = True
    with pytest.raises(ValidationError):
        ComposerSaveRequest.model_validate(raw)


def test_schema_contains_no_open_payload_dictionaries():
    schema = ComposerDefinitionV1.model_json_schema()
    for model in [schema, *schema["$defs"].values()]:
        if model.get("type") == "object":
            assert model.get("additionalProperties") is False


def test_large_document_structure_does_not_inherit_legacy_small_caps():
    raw = fixture()
    page, section, block = raw["pages"][0], raw["sections"][0], raw["blocks"][0]
    raw.update(pages=[], sections=[], blocks=[])
    for p in range(100):
        page_id, section_id = str(uuid4()), str(uuid4())
        raw["pages"].append({**page, "page_id": page_id, "order": p})
        raw["sections"].append({**section, "section_id": section_id, "page_id": page_id})
        for b in range(30):
            raw["blocks"].append({
                **block, "block_id": str(uuid4()), "section_id": section_id, "order": b,
                "placement": {"row": b, "column": 0, "span": 12},
            })
    raw["default_page_id"] = raw["pages"][0]["page_id"]
    value = ComposerDefinitionV1.model_validate(raw)
    assert len(value.blocks) == 3000
    # This is shape admission, deliberately not a runtime performance benchmark.
