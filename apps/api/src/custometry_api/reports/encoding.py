"""Negotiated report JSON transport; limits and identities use decoded bytes."""
import gzip
from fastapi import Request, Response


def report_json_response(content: str, request: Request) -> Response:
    body = content.encode()
    headers = {'Cache-Control': 'no-store', 'Vary': 'Accept-Encoding'}
    accepted = False
    for choice in request.headers.get('accept-encoding', '').lower().split(','):
        coding, *parameters = choice.strip().split(';')
        if coding != 'gzip':
            continue
        quality = next((p.strip()[2:] for p in parameters if p.strip().startswith('q=')), '1')
        try:
            accepted = 0 < float(quality) <= 1
        except ValueError:
            accepted = False
        break
    if accepted and len(body) >= 4096:
        compressed = gzip.compress(body, compresslevel=1, mtime=0)
        if len(compressed) < len(body):
            body = compressed
            headers['Content-Encoding'] = 'gzip'
    return Response(content=body, media_type='application/json', headers=headers)
