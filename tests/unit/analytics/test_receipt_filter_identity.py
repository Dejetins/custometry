"""Reader compatibility and refusal to evaluate typed filters without their owner."""
import importlib.util
import sys
from pathlib import Path
from uuid import uuid4

from pydantic import ValidationError
import pytest

from packages.analytics_core.application.workspace_calculation import normalize
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.workspace import WorkspaceRunRequest
from packages.contracts.analytics.columnar_filters import FlatPredicate, FilterValue
from packages.contracts.analytics.retail_filter import ReceiptFilterInput
from tests.unit.analytics.test_workspace_calculation import fixture


def test_actual_pre_ms011_reader_rejects_new_input_and_accepts_unchanged_old_bytes():
    request, source, inputs, access, calendar = fixture()
    pre = Path('.codex/delivery/evidence/MS-011/preparation')
    def load(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    old_reader = load('ms011_old_workspace', pre / 'workspace-before.py')
    old_calculation = load('ms011_old_calculation', pre / 'workspace-calculation-before.py')
    old = request.model_dump(mode='json')
    assert 'receipt_filter' not in old
    old_request = old_reader.WorkspaceRunRequest.model_validate(old)
    assert WorkspaceRunRequest.model_validate(old).model_dump(mode='json') == old
    baseline = old_calculation.normalize(old_request, source, inputs, access, calendar)
    assert normalize(request, source, inputs, access, calendar) == baseline
    explicit_null = request.model_copy(update={'receipt_filter': None})
    assert normalize(explicit_null, source, inputs, access, calendar) == baseline
    new = request.model_copy(update={'receipt_filter': ReceiptFilterInput(registry_version_id=uuid4(), expression=FlatPredicate(
        field_id='Receipt.status', field_version_id=uuid4(), operator='eq', values=(FilterValue(data_type='string',value='completed'),)))})
    new_bytes = new.model_dump_json()
    with pytest.raises(ValidationError, match='extra_forbidden'):
        old_reader.WorkspaceRunRequest.model_validate(new.model_dump(mode='json'))
    assert WorkspaceRunRequest.model_validate_json(new_bytes).model_dump_json() == new_bytes
    with pytest.raises(AnalyticsFailure, match='FILTER_PROVIDER_UNAVAILABLE'):
        normalize(new, source, inputs, access, calendar)
    filtered = normalize(new, {**source, 'receipt_filter_hash':'a'*64}, inputs, access, calendar)
    assert filtered[1] != baseline[1]
    assert normalize(new, {**source, 'receipt_filter_hash':'b'*64}, inputs, access, calendar)[1] != filtered[1]
