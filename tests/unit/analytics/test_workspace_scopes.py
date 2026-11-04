"""Scoped identity and calculation share one server normalizer; old meaning is preserved."""
from copy import deepcopy
import pytest
from packages.analytics_core.application.workspace_calculation import build_workspace, normalize
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.workspace import WorkspaceRunRequest, WorkspaceResultV2, WorkspaceScopeInput
from tests.unit.analytics.test_workspace_calculation import fixture


def scoped(request, values, dependency='d' * 64):
    return request.model_copy(update={'scope': WorkspaceScopeInput.model_validate({
        'dependency_hash': dependency,
        'filters': [{'semantic_dataset_version_id': request.semantic_dataset_version_id,
                     'expression': {'kind': 'store_in', 'values': values}}],
    })})


def test_scope_changes_real_calculation_identity_and_keeps_legacy_payload_absent():
    req, source, inputs, access, calendar = fixture()
    old = build_workspace(req, source, inputs, access, calendar)
    assert 'scope' not in req.model_dump(mode='json')
    assert 'scope_hash' not in WorkspaceResultV2.model_validate({**old, 'manifest': {'artifact_id': req.semantic_dataset_version_id, 'content_hash': 'f'*64}}).model_dump(mode='json')['effective_context']
    none = build_workspace(scoped(req, ['2']), source, inputs, access, calendar)
    assert none['effective_context']['store_ids'] == ['2']
    assert none['totals']['net_revenue'] is None
    assert none['request_hash'] != old['request_hash'] and none['result_id'] != old['result_id']
    same_values = build_workspace(scoped(req, ['1']), source, inputs, access, calendar)
    assert same_values['totals'] == old['totals']
    other_dependencies = build_workspace(scoped(req, ['1'], 'e'*64), source, inputs, access, calendar)
    assert same_values['request_hash'] != other_dependencies['request_hash']
    assert build_workspace(req, source, inputs, access, calendar) == old


def test_scope_hash_canonicalizes_boolean_order_and_enforces_mandatory_selection():
    req, source, inputs, access, calendar = fixture()
    value = scoped(req, ['1', '2']).model_dump(mode='json')
    value['scope']['filters'][0]['expression'] = {'kind': 'or', 'children': [
        {'kind': 'store_in', 'values': ['1']}, {'kind': 'store_in', 'values': ['2']}]}
    first = WorkspaceRunRequest.model_validate(value)
    value['scope']['filters'][0]['expression']['children'].reverse()
    second = WorkspaceRunRequest.model_validate(value)
    assert normalize(first, source, inputs, access, calendar) == normalize(second, source, inputs, access, calendar)
    value['local_store_ids'] = ['2']
    result = build_workspace(WorkspaceRunRequest.model_validate(value), source, inputs, access, calendar)
    assert result['effective_context']['store_ids'] == ['2']
    assert result['totals']['net_revenue'] is None


def test_scope_permission_does_not_short_circuit_after_empty_selection():
    req, source, inputs, access, calendar = fixture()
    value = scoped(req, ['forbidden']).model_dump(mode='json')
    value['common']['store_ids'] = []
    with pytest.raises(AnalyticsFailure, match='FORBIDDEN'):
        build_workspace(WorkspaceRunRequest.model_validate(value), source, inputs, access, calendar)
    altered = deepcopy(source)
    altered['metrics'][0]['content_hash'] = '0'*64
    with pytest.raises(AnalyticsFailure, match='METRIC_BASIS_MISMATCH'):
        build_workspace(scoped(req, []), altered, inputs, access, calendar)
