"""One GET shares its admission budget across otherwise independent adapters."""
from custometry_api.reports.prepared import RequestReadBudget, RequestReadMemo


class Repository:
    def __init__(self, value=None):
        self.calls = 0
        self.value = value

    def read(self, key):
        self.calls += 1
        return self.value if self.value is not None else {'key': key}


def test_repository_entry_budget_is_shared_and_next_request_is_fresh():
    budget = RequestReadBudget()
    left, right = Repository(), Repository()
    a = RequestReadMemo(left, frozenset({'read'}), budget)
    b = RequestReadMemo(right, frozenset({'read'}), budget)
    for key in range(40):
        a.read(key)
        b.read(key)
    for key in range(40):
        a.read(key)
        b.read(key)
    assert budget.entries == 64
    assert left.calls + right.calls == 96  # 16 unadmitted keys are reread.
    fresh = RequestReadMemo(left, frozenset({'read'}), RequestReadBudget())
    before = left.calls
    fresh.read(0)
    assert left.calls == before + 1


def test_repository_byte_budget_is_shared():
    budget = RequestReadBudget()
    left, right = Repository('x' * (9 * 1024 * 1024)), Repository('y' * (9 * 1024 * 1024))
    a = RequestReadMemo(left, frozenset({'read'}), budget)
    b = RequestReadMemo(right, frozenset({'read'}), budget)
    for _ in range(2):
        a.read(0)
        b.read(0)
    assert left.calls == 1
    assert right.calls == 2
    assert budget.entries == 1
    assert budget.bytes <= 16 * 1024 * 1024


def prepared_fixture():
    from unittest.mock import Mock
    from custometry_api.reports.prepared import PreparedAnalyticsService
    from tests.unit.analytics.test_workspace_calculation import fixture
    request, source, inputs, access, calendar = fixture()
    source['summary'] = {'raw_artifacts': {}, 'quarantine_artifact': 'synthetic'}
    semantics, results, artifacts, calendars, policy = [Mock() for _ in range(5)]
    semantics.sales_projection.return_value = source
    results.find_sales.return_value = None
    calendars.get_version.return_value = calendar
    policy.resolve.return_value = access
    artifacts.read_sales_inputs.side_effect = lambda **kw: {b['entity']: inputs[b['entity']] for b in kw['bindings']}
    service = PreparedAnalyticsService(semantics=semantics, results=results, artifacts=artifacts, calendars=calendars, access=policy)
    return service, request, source, inputs, access, calendar


def test_prepared_preflight_preserves_identity_without_reading_raw_history():
    from packages.analytics_core.application.workspace_calculation import normalize
    service, request, source, inputs, access, calendar = prepared_fixture()
    expected, fingerprint = normalize(request, source, inputs, access, calendar)
    result = service.preflight(workspace_id=access.workspace_id, principal_id=access.principal_id, request=request)
    assert result.request_hash == fingerprint
    assert result.effective_context.model_dump(mode='json') == expected
    calls = service.artifacts.read_sales_inputs.call_args_list
    assert len(calls) == 1
    assert [b['entity'] for b in calls[0].kwargs['bindings']] == ['Store']
    assert calls[0].kwargs['supporting_artifacts'] == []
    assert service.access.resolve.call_count == 2


def test_prepared_calculation_still_reads_full_history():
    service, request, source, inputs, access, calendar = prepared_fixture()
    _, actual = service.query_inputs(access, request)
    assert actual == inputs
    assert len(service.artifacts.read_sales_inputs.call_args.kwargs['bindings']) == 6


def test_prepared_preflight_still_rejects_forbidden_store():
    import pytest
    from packages.contracts.analytics import AnalyticsFailure
    service, request, source, inputs, access, calendar = prepared_fixture()
    request = request.model_copy(update={'local_store_ids': ['forbidden']})
    with pytest.raises(AnalyticsFailure, match='STORE_NOT_AVAILABLE'):
        service.preflight(workspace_id=access.workspace_id, principal_id=access.principal_id, request=request)
