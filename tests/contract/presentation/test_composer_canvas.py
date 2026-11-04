"""Canvas persistence and filter boundaries; no browser or database proof."""

from uuid import uuid4
import pytest
from pydantic import ValidationError
from packages.contracts.presentation.composer import ComposerDefinitionV1
from packages.contracts.presentation.scopes import ComposerScopesV1
from packages.presentation.domain.scopes import resolve_scope
from tests.contract.presentation.test_composer import fixture


def canvas():
    raw = fixture()
    raw["grid_columns"] = 24
    for b in raw["blocks"]:
        b["placement"]["column"] *= 2
        b["placement"]["span"] *= 2
        b["placement"]["row"] *= 8
        b["placement"]["row_span"] = 8
    raw["blocks"].append(
        dict(
            block_id=str(uuid4()),
            section_id=raw["sections"][0]["section_id"],
            order=6,
            block_type="text",
            presentation={"title": "Note"},
            text="<script>plain text</script>",
            placement=dict(column=0, span=24, row=24, row_span=3),
        )
    )
    raw["blocks"].append(
        dict(
            block_id=str(uuid4()),
            section_id=raw["sections"][0]["section_id"],
            order=7,
            block_type="filter",
            presentation={"title": "Stores"},
            control=dict(
                semantic_dataset_version_id=raw["definitions"][0]["query"][
                    "semantic_dataset_version_id"
                ],
                target_block_ids=[raw["blocks"][0]["block_id"]],
                store_ids=["north"],
            ),
            placement=dict(column=0, span=24, row=27, row_span=2),
        )
    )
    return raw


def test_legacy_serialization_omits_new_defaults():
    value = ComposerDefinitionV1.model_validate(fixture()).model_dump(mode="json")
    assert "grid_columns" not in value
    assert all(not {"text", "text_style", "control"} & b.keys() for b in value["blocks"])


def test_canvas_roundtrip_and_selected_filter_only():
    d = ComposerDefinitionV1.model_validate(canvas())
    assert ComposerDefinitionV1.model_validate_json(d.model_dump_json()) == d
    assert resolve_scope(d, ComposerScopesV1(), d.blocks[0].block_id).query.local_store_ids == [
        "north"
    ]
    assert resolve_scope(d, ComposerScopesV1(), d.blocks[1].block_id).query.local_store_ids is None


def test_filter_intersects_existing_local_constraint():
    raw = canvas()
    raw["definitions"][0]["query"]["local_store_ids"] = ["south"]
    d = ComposerDefinitionV1.model_validate(raw)
    assert resolve_scope(d, ComposerScopesV1(), d.blocks[0].block_id).query.local_store_ids == []


@pytest.mark.parametrize(
    "failure",
    [
        "legacy_overflow",
        "nondata_target",
        "wrong_dataset",
        "source_on_text",
        "missing_source",
        "overlap",
    ],
)
def test_invalid_canvas_rejected(failure):
    raw = canvas()
    if failure == "legacy_overflow":
        raw.pop("grid_columns")
    if failure == "nondata_target":
        raw["blocks"][-1]["control"]["target_block_ids"] = [raw["blocks"][-2]["block_id"]]
    if failure == "wrong_dataset":
        raw["blocks"][-1]["control"]["semantic_dataset_version_id"] = str(uuid4())
    if failure == "source_on_text":
        raw["blocks"][-2]["source"] = raw["blocks"][0]["source"]
    if failure == "missing_source":
        raw["blocks"][0].pop("source")
    if failure == "overlap":
        raw["blocks"][-1]["placement"]["row"] = 24
    with pytest.raises(ValidationError):
        ComposerDefinitionV1.model_validate(raw)


def test_copy_content_and_advertise_supported_types():
    from packages.contracts.presentation.composer import (
        duplicate_block,
        GridPlacement,
        ComposerCapabilities,
    )

    d = ComposerDefinitionV1.model_validate(canvas())
    copied = duplicate_block(
        d,
        d.blocks[-1].block_id,
        section_id=d.sections[0].section_id,
        order=8,
        placement=GridPlacement(column=0, span=24, row=30, row_span=2),
    )
    assert copied.blocks[-1].control == d.blocks[-1].control
    assert copied.blocks[-1].block_id != d.blocks[-1].block_id
    assert set(ComposerCapabilities().blocks) == {"chart", "table", "metric", "text", "filter"}


def test_metric_card_and_chart_style_roundtrip():
    raw = canvas()
    raw["blocks"][0]["block_type"] = "metric"
    raw["blocks"][1]["presentation"]["chart_type"] = "bar"
    value = ComposerDefinitionV1.model_validate(raw)
    assert value.blocks[0].source is not None
    assert ComposerDefinitionV1.model_validate_json(value.model_dump_json()) == value
    legacy = ComposerDefinitionV1.model_validate(fixture()).model_dump(mode="json")
    assert all("chart_type" not in b["presentation"] for b in legacy["blocks"])
