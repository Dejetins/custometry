import gzip
import json
import pytest
from starlette.requests import Request
from custometry_api.reports.encoding import report_json_response


@pytest.mark.parametrize('accept,compressed', [
    ('gzip, deflate, br', True), ('gzip;q=0.5', True), ('gzip;q=0', False),
    ('br', False), ('', False), ('gzip;q=invalid', False), ('gzip;q=2', False),
])
def test_report_transport_preserves_decoded_json_and_negotiation(accept, compressed):
    content = json.dumps({'label': 'Розница €' * 2048}, ensure_ascii=False)
    request = Request({'type': 'http', 'headers': [(b'accept-encoding', accept.encode())]})
    response = report_json_response(content, request)
    assert response.headers['cache-control'] == 'no-store'
    assert response.headers['vary'] == 'Accept-Encoding'
    if compressed:
        assert response.headers['content-encoding'] == 'gzip'
        assert gzip.decompress(response.body) == content.encode()
        assert len(response.body) < len(content.encode())
    else:
        assert 'content-encoding' not in response.headers
        assert response.body == content.encode()
