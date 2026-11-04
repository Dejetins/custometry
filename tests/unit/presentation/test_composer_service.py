"""Composer command boundary: no implicit compute and no authorization shortcuts."""
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest
from packages.contracts.presentation import PresentationFailure
from packages.contracts.presentation.composer import ComposerDefinitionV1, ComposerSaveRequest
from packages.presentation.application.composer import ComposerService
from tests.contract.presentation.test_composer import fixture


def setup():
    definition = ComposerDefinitionV1.model_validate(fixture())
    workspace, actor = uuid4(), definition.creator_principal_id
    legacy = Mock()
    legacy.repository.metadata.side_effect = PresentationFailure("NOT_FOUND")
    legacy.repository.replay.return_value = None
    legacy.access.resolve_resource.return_value = SimpleNamespace(
        allowed=True, store_ids=None,
        permissions={"report.read", "report.manage", "analysis.read", "analysis.run"},
    )
    legacy.results.context.return_value = {"metrics": [
        m.model_dump(mode="json") for m in definition.definitions[0].query.metric_refs
    ]}
    legacy.results.resolve.return_value = SimpleNamespace(allowed_store_ids=[])
    legacy.artifacts.commit.side_effect = lambda **kw: {"artifact_id": str(kw["artifact_id"]), "content_hash": "a" * 64}
    legacy.repository.save_composer.side_effect = lambda *args: args[4]
    return ComposerService(legacy), legacy, workspace, actor, definition


def save_request(definition):
    return ComposerSaveRequest(contract_version="analytical-authoring/v1", definition=definition, expected_revision=0, idempotency_key=uuid4())


def test_save_persists_graph_without_calculation():
    service, old, workspace, actor, definition = setup()
    saved = service.save(workspace, actor, save_request(definition))
    assert saved.definition == definition
    assert saved.contract_version == "composed-report/v1"
    old.results.apply.assert_not_called()
    old.results.verify.assert_not_called()
    old.repository.save_composer.assert_called_once()


@pytest.mark.parametrize("case", ["creator", "permission", "existing_other_creator", "unsupported_origin", "forged_metric"])
def test_save_rejects_invalid_authority_before_persistence(case):
    service, old, workspace, actor, definition = setup()
    if case == "creator":
        actor = uuid4()
    if case == "permission":
        old.access.resolve_resource.return_value.permissions.remove("report.manage")
    if case == "existing_other_creator":
        old.repository.metadata.side_effect = None
        old.repository.metadata.return_value = {"creator": uuid4()}
    if case == "unsupported_origin":
        definition = ComposerDefinitionV1.model_validate({**definition.model_dump(mode="json"), "origin": {"report_id": str(uuid4()), "version_id": str(uuid4()), "snapshot_id": str(uuid4())}})
    if case == "forged_metric":
        old.results.context.return_value = {"metrics": []}
    with pytest.raises(PresentationFailure):
        service.save(workspace, actor, save_request(definition))
    old.repository.save_composer.assert_not_called()
    old.results.apply.assert_not_called()


def test_unknown_version_is_not_disclosed_before_access():
    service, old, workspace, actor, definition = setup()
    old.guard.side_effect = PresentationFailure("FORBIDDEN")
    with pytest.raises(PresentationFailure, match="FORBIDDEN"):
        service.get(workspace, actor, definition.document_id)
    old.repository.read.assert_not_called()


def test_changed_shared_source_cannot_reuse_stale_result():
    service, old, workspace, actor, definition = setup()
    from packages.contracts.presentation.composer import ComposerResultRef
    body = save_request(definition).model_copy(update={"results": [ComposerResultRef(
        block_id=definition.blocks[0].block_id, result_id=uuid4()
    )]})
    old.results.verify.side_effect = PresentationFailure("RESULT_BINDING_MISMATCH")
    with pytest.raises(PresentationFailure, match="RESULT_BINDING_MISMATCH"):
        service.save(workspace, actor, body)
    old.repository.save_composer.assert_not_called()


def test_report_store_ceiling_applies_to_common_local_intersection():
    service, old, workspace, actor, definition = setup()
    a, b = str(uuid4()), str(uuid4())
    old.results.resolve.return_value.allowed_store_ids = [a, b]
    old.access.resolve_resource.return_value.store_ids = [a]
    payload = definition.model_dump(mode="json")
    payload["definitions"][0]["query"]["common"]["store_ids"] = [a]
    payload["definitions"][0]["query"]["local_store_ids"] = [a, b]
    service.validate_sources(workspace, actor, ComposerDefinitionV1.model_validate(payload))
    payload["definitions"][0]["query"]["common"]["store_ids"] = [a, str(uuid4())]
    with pytest.raises(PresentationFailure, match="FORBIDDEN"):
        service.validate_sources(workspace, actor, ComposerDefinitionV1.model_validate(payload))


def test_canvas_filter_uses_effective_report_ceiling_and_rejects_unauthorized_values():
    from tests.contract.presentation.test_composer_canvas import canvas
    service, old, workspace, actor, _ = setup()
    raw=canvas()
    raw['creator_principal_id']=str(actor)
    # Restrict every analytical block to the report's allowed subset.
    raw['blocks'][-1]['control']['target_block_ids']=[b['block_id'] for b in raw['blocks'] if b.get('source')]
    definition=ComposerDefinitionV1.model_validate(raw)
    old.results.context.return_value={'metrics':[m.model_dump(mode='json') for m in definition.definitions[0].query.metric_refs]}
    old.results.resolve.return_value=SimpleNamespace(allowed_store_ids=['north','south'])
    old.access.resolve_resource.return_value.store_ids=['north']
    old.results.preflight.return_value=SimpleNamespace(effective_context=SimpleNamespace(store_ids=['north']))
    service.validate_sources(workspace,actor,definition)
    assert old.results.preflight.call_count==6
    raw['blocks'][-1]['control']['store_ids']=['forbidden']
    with pytest.raises(PresentationFailure,match='FORBIDDEN'):
        service.validate_sources(workspace,actor,ComposerDefinitionV1.model_validate(raw))
