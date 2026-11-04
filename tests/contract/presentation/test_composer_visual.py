"""Typed visual settings retain legacy serialization and snapshot roundtrips."""
import pytest
from pydantic import ValidationError
from packages.contracts.presentation.composer import BlockPresentation, ComposerDefinitionV1
from packages.contracts.presentation.visual import BlockVisual
from tests.contract.presentation.test_composer import fixture


def test_legacy_presentation_has_no_new_defaults():
    assert BlockPresentation(title='Revenue').model_dump() == {'title':'Revenue','density':'comfortable','legend':True}


def test_visual_snapshot_roundtrip():
    raw=fixture()
    raw['blocks'][0]['presentation'].update(description='Server sales',chart_type='combo',visual={'series':[{'key':'net_revenue','kind':'bar','axis':'left'},{'key':'receipt_count','kind':'line','axis':'right','labels':True}],'tooltip_previous':True,'goal':100})
    d=ComposerDefinitionV1.model_validate(raw)
    assert ComposerDefinitionV1.model_validate_json(d.model_dump_json())==d
    assert d.blocks[0].presentation.visual.series[1].axis=='right'


@pytest.mark.parametrize('settings',[{'formatter':'eval(1)'},{'decimals':-1},{'y_min':10,'y_max':5},{'goal':float('nan')},{'gauge_min':100,'gauge_max':50},{'series':[{'key':'x'},{'key':'x'}]}])
def test_invalid_or_executable_visual_settings_rejected(settings):
    with pytest.raises(ValidationError):
        BlockVisual.model_validate(settings)


def test_empty_block_title_survives_snapshot_roundtrip():
    raw = fixture()
    raw['blocks'][0]['presentation']['title'] = ''
    definition = ComposerDefinitionV1.model_validate(raw)
    restored = ComposerDefinitionV1.model_validate_json(definition.model_dump_json())
    assert restored.blocks[0].presentation.title == ''
