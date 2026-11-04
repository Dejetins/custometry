"""Request-local projection cannot retain oversized rows or mutable caller aliases."""
import pytest
from packages.identity_access.infrastructure.request_projection import ProjectionCursor, RequestProjection


class Rows:
    def __init__(self, values):
        self.values, self.calls = values, 0

    def execute(self, query, parameters):
        self.calls += 1

    def fetchall(self):
        return self.values


def test_row_reuse_is_bounded_and_caller_mutation_is_isolated():
    source = Rows([{'scope': ['store-a']}])
    projection = RequestProjection(lambda: None)
    cursor = ProjectionCursor(source, projection)
    cursor.execute('SELECT scope', ('principal-a',))
    first = cursor.fetchone()
    first['scope'].append('store-b')
    cursor.execute('SELECT scope', ('principal-a',))
    assert cursor.fetchone() == {'scope': ['store-a']}
    assert source.calls == 1
    cursor.execute('SELECT scope', ('principal-b',))
    assert source.calls == 2
    oversized = ProjectionCursor(Rows([{'scope': 'x' * (1024 * 1024)}]), projection)
    before = len(projection.rows)
    oversized.execute('SELECT large_scope')
    assert len(projection.rows) == before
    assert projection.bytes <= 1024 * 1024


def test_projection_rejects_write_and_lock_statements():
    cursor = ProjectionCursor(Rows([]), RequestProjection(lambda: None))
    for statement in ('UPDATE identity_memberships SET status=%s', 'SELECT * FROM identity_memberships FOR UPDATE', 'SELECT pg_advisory_xact_lock(1)'):
        with pytest.raises(RuntimeError, match='READ_PROJECTION_STATEMENT_REQUIRED'):
            cursor.execute(statement)


@pytest.mark.parametrize('payload', [
    b'{"values":[null,true,false,0,-1,1.5,1e-12,123456789012345678901234567890],"amount":"100.01"}',
    '{"label":"Розница \U0001f30d","nested":{"scope":["a","b"]},"unicode":"\\u20ac"}'.encode(),
    b'{"negative_zero":-0.0,"text":"2025-01-01","escape":"a\\nb"}',
])
def test_database_json_decoder_preserves_plain_json_values(payload):
    import json
    from custometry_api.database import load_json_value

    expected = json.loads(payload)
    assert load_json_value(payload) == expected
    assert load_json_value(memoryview(payload)) == expected
    assert json.dumps(load_json_value(payload), sort_keys=True) == json.dumps(expected, sort_keys=True)
