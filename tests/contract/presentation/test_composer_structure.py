"""C03 graph evolution keeps pre-C03 payloads valid and exact stored bytes intact."""
from uuid import uuid4
import pytest
from pydantic import ValidationError
from packages.contracts.presentation.composer import ComposerDefinitionV1, duplicate_block, GridPlacement
from tests.contract.presentation.test_composer import fixture


def test_old_payload_defaults_and_copy_origin():
    raw = fixture()
    value = ComposerDefinitionV1.model_validate(raw)
    assert not value.pages[0].hidden and not value.pages[0].locked
    assert value.blocks[0].copied_from is None
    copied = duplicate_block(value, value.blocks[0].block_id,
                             section_id=value.sections[0].section_id, order=6,
                             placement=GridPlacement(row=3))
    assert copied.blocks[-1].copied_from.node_id == value.blocks[0].block_id
    assert copied.blocks[-1].block_id != value.blocks[0].block_id
    assert "hidden" not in raw["pages"][0]
    assert "hidden" not in value.model_dump(mode="json")["pages"][0]
    assert "copied_from" not in value.model_dump(mode="json")["blocks"][0]
    explicit = fixture()
    explicit["pages"][0]["hidden"] = False
    assert ComposerDefinitionV1.model_validate(explicit).model_dump(mode="json")["pages"][0]["hidden"] is False


@pytest.mark.parametrize("case", ["hidden_default", "hidden_chapter", "self_origin", "truthy_lock"])
def test_invalid_presentation_state_fails_closed(case):
    raw = fixture()
    if case == "hidden_default":
        raw["pages"][0]["hidden"] = True
    if case == "hidden_chapter":
        chapter = str(uuid4())
        raw["chapters"] = [{"chapter_id": chapter, "order": 0, "title": "Hidden", "hidden": True}]
        raw["pages"][0]["chapter_id"] = chapter
    if case == "self_origin":
        raw["blocks"][0]["copied_from"] = {"node_id": raw["blocks"][0]["block_id"]}
    if case == "truthy_lock":
        raw["pages"][0]["locked"] = "false"
    with pytest.raises(ValidationError):
        ComposerDefinitionV1.model_validate(raw)
