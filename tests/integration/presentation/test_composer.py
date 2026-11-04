"""C02 real API/Identity/Analytics/PostgreSQL rehearsal on a disposable database."""
from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from custometry_api.config import Settings
import psycopg

ROOT = Path(__file__).resolve().parents[3]


def test_composer_vertical_persistence(tmp_path, monkeypatch):
    if os.environ.get("MS006_OWNED_DATABASE") != "1":
        pytest.skip("requires run_composer owned disposable database")
    corpus_path = tmp_path / "corpus.json"
    monkeypatch.setenv("MS004_S04_CORPUS_OUT", str(corpus_path))
    spec = importlib.util.spec_from_file_location("composer_synthetic_scenario", ROOT / "tests/e2e/ms-004-workspace/scenario.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    app = module.create_scenario(tmp_path / "artifacts")
    client = TestClient(app, base_url="https://testserver")
    scenario = client.get("/fixture/scenario").json()
    response = client.post("/identity/login", json={
        "workspace_id": scenario["workspace"], "email": "author@example.test",
        "password": "synthetic-author-password", "device_label": "C02 disposable proof",
    })
    assert response.status_code == 200, response.text
    author_session = response.json()["session_id"]
    headers = {"X-CSRF-Token": response.json()["csrf_token"], "Origin": Settings().cors_allowed_origins[0]}
    corpus = json.loads(corpus_path.read_text())
    report = str(uuid4())
    response = client.post("/reports/composer/v1/prepare", headers=headers, json={
        "report_id": report, "semantic_dataset_version_id": corpus["semantic_dataset_version_id"],
        "common_context": {"starts_on": "2025-01-01", "ends_on": "2025-01-31", "store_ids": None},
        "template": "blank", "locale": "en",
    })
    assert response.status_code == 200, response.text
    definition = response.json()["definition"]
    # Obtain a current provider calendar through the existing native prepare seam.
    legacy_prepare = client.post("/reports/v2/new/prepare", headers=headers, json={
        "report_id": str(uuid4()), "semantic_dataset_version_id": corpus["semantic_dataset_version_id"],
        "common_context": {"starts_on": "2025-01-01", "ends_on": "2025-01-31", "store_ids": None},
        "template": "blank", "locale": "en",
    })
    assert legacy_prepare.status_code == 200, legacy_prepare.text
    native = legacy_prepare.json()["definition"]
    metric = corpus["metric_refs"][0]
    for i in range(4):
        source = str(uuid4())
        definition["definitions"].append({"definition_id": source, "provider": "metric-workspace/v2", "query": {
            "semantic_dataset_version_id": corpus["semantic_dataset_version_id"],
            "common": {"starts_on": "2025-01-01", "ends_on": "2025-01-31", "store_ids": None},
            "local_store_ids": None, "grain": ["day", "week", "month", "year"][i],
            "calendar_ref": native["calendar_ref"], "calendar_basis": "calendar", "alignment": "none",
            "metric_refs": [metric],
        }})
        definition["blocks"].append({"block_id": str(uuid4()), "section_id": definition["sections"][0]["section_id"],
            "order": i, "block_type": "chart", "source": {"definition_id": source, "metric_ref": metric},
            "presentation": {"title": "Chart " + str(i)}, "placement": {"column": i % 2 * 6, "span": 6, "row": i // 2}})
    for i in range(2):
        block = deepcopy(definition["blocks"][i])
        block.update(block_id=str(uuid4()), order=4 + i, block_type="table", placement={"column": i * 6, "span": 6, "row": 2})
        definition["blocks"].append(block)
    result_refs = []
    for block in definition["blocks"]:
        response = client.post("/reports/composer/v1/apply", headers=headers, json={
            "contract_version": "analytical-authoring/v1", "definition": definition, "block_id": block["block_id"],
        })
        assert response.status_code == 200, response.text
        result_refs.append({"block_id": block["block_id"], "result_id": response.json()["result"]["result_id"]})
    assert result_refs[0]["result_id"] == result_refs[4]["result_id"]
    assert result_refs[1]["result_id"] == result_refs[5]["result_id"]
    assert len({r["result_id"] for r in result_refs}) == 4
    body = {"contract_version": "analytical-authoring/v1", "definition": definition,
            "expected_revision": 0, "idempotency_key": str(uuid4()), "results": result_refs}
    response = client.post("/reports/composer/v1/versions", headers=headers, json=body)
    assert response.status_code == 200, response.text
    saved = response.json()
    # Pre-C03 metadata omissions remain absent in immutable snapshots and replay payloads.
    for key in ("pages", "sections", "blocks"):
        assert all("hidden" not in value and "locked" not in value and "copied_from" not in value
                   for value in saved["definition"][key])
    replay = client.post("/reports/composer/v1/versions", headers=headers, json=body)
    assert replay.status_code == 200 and replay.json() == saved
    reopened = client.get("/reports/composer/v1/" + report)
    assert reopened.status_code == 200, reopened.text
    assert reopened.json()["report"] == saved
    assert len(saved["definition"]["blocks"]) == 6
    for ref in result_refs:
        result = client.get(f'/reports/composer/v1/{report}/snapshots/{saved["snapshot_id"]}/blocks/{ref["block_id"]}/result')
        assert result.status_code == 200, result.text
        assert result.json()["result"]["result_id"] == ref["result_id"]
    assert client.get("/reports/v2/" + report).status_code == 409
    assert client.get("/reports/" + report).status_code == 409
    old = client.get("/reports/" + scenario["report"])
    assert old.status_code == 200, old.text
    listing = client.get("/reports/")
    assert listing.status_code == 200, listing.text
    assert report in {r["report_id"] for r in listing.json()["reports"]}
    stale = {**body, "idempotency_key": str(uuid4())}
    assert client.post("/reports/composer/v1/versions", headers=headers, json=stale).status_code == 409
    changed = deepcopy(body)
    changed["definition"]["title"] = "Changed"
    assert client.post("/reports/composer/v1/versions", headers=headers, json=changed).status_code == 409
    settings = Settings()
    with psycopg.connect(host=settings.database_host, port=settings.database_port, dbname=settings.database_name,
                         user=settings.database_user, password=settings.read_database_password()) as connection:
        assert connection.execute("SELECT count(*) FROM presentation_versions WHERE document_id=%s", (report,)).fetchone()[0] == 1
    # A crash after artifact admission and version insert cannot move the current pointer.
    from packages.presentation.infrastructure.workspace import PostgresWorkspaceRepository
    from packages.contracts.presentation import PresentationFailure
    original_save = PostgresWorkspaceRepository.save_composer

    def crash_save(self, *args):
        def crash():
            raise PresentationFailure("STORAGE_UNAVAILABLE")
        self._checkpoint = crash
        return original_save(self, *args)

    revision_two = deepcopy(body)
    revision_two.update(expected_revision=1, idempotency_key=str(uuid4()))
    revision_two["definition"]["title"] = "Layout-only revision"
    revision_two["definition"]["profile"] = "dashboard"
    chapter = str(uuid4())
    revision_two["definition"]["chapters"] = [{"chapter_id": chapter, "title": "C03 group", "order": 0}]
    revision_two["definition"]["pages"][0].update(chapter_id=chapter, locked=True, hidden=False)
    revision_two["definition"]["blocks"][0]["hidden"] = True
    with monkeypatch.context() as patch:
        patch.setattr(PostgresWorkspaceRepository, "save_composer", crash_save)
        crashed = client.post("/reports/composer/v1/versions", headers=headers, json=revision_two)
        assert crashed.status_code == 503
    assert client.get("/reports/composer/v1/" + report).json()["report"] == saved
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda _: client.post("/reports/composer/v1/versions", headers=headers, json=revision_two), range(2)))
    assert [r.status_code for r in responses] == [200, 200]
    assert responses[0].json() == responses[1].json()
    assert responses[0].json()["revision"] == 2
    assert responses[0].json()["definition"]["profile"] == "dashboard"
    assert responses[0].json()["definition"]["pages"][0]["locked"] is True
    assert responses[0].json()["results"] == result_refs
    assert client.get(f'/reports/composer/v1/{report}/snapshots/{saved["snapshot_id"]}').json()["report"] == saved
    assert client.get("/reports/" + scenario["report"]).json() == old.json()
    # Downgrade must refuse new rows, without deleting data or changing the migration head.
    import subprocess
    refused = subprocess.run(["uv", "run", "--locked", "--no-sync", "alembic", "-c", "migrations/alembic.ini", "downgrade", "0013_identity_lifecycle"],
                             cwd=ROOT, capture_output=True, text=True)
    assert refused.returncode != 0
    assert "COMPOSER_FORWARD_REPAIR_OR_PREUPGRADE_BACKUP_REQUIRED" in refused.stderr
    assert client.get("/reports/composer/v1/" + report).json()["report"]["revision"] == 2
    # C04 scopes use real current access and the same normalized query at every boundary.
    scoped_definition = deepcopy(definition)
    scoped_report = str(uuid4())
    scoped_definition["document_id"] = scoped_report
    target_block = scoped_definition["blocks"][0]["block_id"]
    initial_preflight = client.post("/reports/composer/v1/preflight", headers=headers, json={
        "contract_version": "analytical-authoring/v1", "definition": scoped_definition, "block_id": target_block})
    assert initial_preflight.status_code == 200, initial_preflight.text
    provider = initial_preflight.json()["provider"]
    allowed = provider["effective_context"]["store_ids"]
    assert allowed and provider["dimensions"] == ["date", "store_id"]
    assert provider["locked_metric_rules"][0]["currency"] == "EUR"
    assert "channels" in provider["unsupported"] and provider["estimate_state"] == "unavailable"
    scope_binding = {"binding_id": str(uuid4()), "target": {"kind": "document", "id": scoped_report}, "order": 0,
        "filter": {"semantic_dataset_version_id": corpus["semantic_dataset_version_id"],
                   "expression": {"kind": "store_in", "values": [allowed[0]]}}, "locked": True}
    isolated = deepcopy(scoped_definition)
    isolated["scopes"] = {"filters": [{**deepcopy(scope_binding), "target": {"kind": "block", "id": isolated["blocks"][4]["block_id"]}}]}
    isolated["scopes"]["filters"][0]["filter"]["semantic_dataset_version_id"] = str(uuid4())
    # Blocks 0 and 4 share one definition, but only 4 has the invalid local scope.
    independent = {"contract_version": "analytical-authoring/v1", "definition": isolated, "block_id": target_block}
    assert client.post("/reports/composer/v1/preflight", headers=headers, json=independent).status_code == 200
    assert client.post("/reports/composer/v1/apply", headers=headers, json=independent).status_code == 200
    independent["block_id"] = isolated["blocks"][4]["block_id"]
    assert client.post("/reports/composer/v1/apply", headers=headers, json=independent).status_code == 400
    assert client.post("/reports/composer/v1/validate", headers=headers, json=isolated).status_code == 400
    assert client.post("/reports/composer/v1/versions", headers=headers, json={"contract_version": "analytical-authoring/v1", "definition": isolated, "expected_revision": 0, "idempotency_key": str(uuid4())}).status_code == 400
    scoped_definition["scopes"] = {"filters": [scope_binding], "contexts": [{"binding_id": str(uuid4()),
        "target": {"kind": "document", "id": scoped_report}, "context": {"grain": "month"}}]}
    scoped_command = {"contract_version": "analytical-authoring/v1", "definition": scoped_definition, "block_id": target_block}
    scoped_preflight = client.post("/reports/composer/v1/preflight", headers=headers, json=scoped_command)
    assert scoped_preflight.status_code == 200, scoped_preflight.text
    assert scoped_preflight.json()["provider"]["effective_context"]["store_ids"] == [allowed[0]]
    assert scoped_preflight.json()["provider"]["effective_context"]["grain"] == "month"
    invalid_scope = deepcopy(scoped_command)
    invalid_scope["definition"]["scopes"]["filters"][0]["filter"]["expression"]["values"] = ["not-authorized"]
    assert client.post("/reports/composer/v1/preflight", headers=headers, json=invalid_scope).status_code == 403
    assert client.post("/reports/composer/v1/apply", headers=headers, json=invalid_scope).status_code == 403
    applied_scope = client.post("/reports/composer/v1/apply", headers=headers, json=scoped_command)
    assert applied_scope.status_code == 200, applied_scope.text
    scoped_result = applied_scope.json()["result"]
    assert scoped_result["request_hash"] == scoped_preflight.json()["provider"]["request_hash"]
    scoped_body = {"contract_version": "analytical-authoring/v1", "definition": scoped_definition,
        "expected_revision": 0, "idempotency_key": str(uuid4()),
        "results": [{"block_id": target_block, "result_id": scoped_result["result_id"]}]}
    scoped_save = client.post("/reports/composer/v1/versions", headers=headers, json=scoped_body)
    assert scoped_save.status_code == 200, scoped_save.text
    scoped_saved = scoped_save.json()
    assert client.get("/reports/composer/v1/" + scoped_report).json()["report"] == scoped_saved
    scoped_read = client.get(f'/reports/composer/v1/{scoped_report}/snapshots/{scoped_saved["snapshot_id"]}/blocks/{target_block}/result')
    assert scoped_read.status_code == 200, scoped_read.text
    assert scoped_read.json()["result"]["result_id"] == scoped_result["result_id"]
    assert client.post("/reports/composer/v1/versions", headers=headers, json=scoped_body).json() == scoped_saved
    persisted_isolation = deepcopy(scoped_definition)
    persisted_isolation["scopes"]["filters"].append({**deepcopy(isolated["scopes"]["filters"][0]), "binding_id": str(uuid4())})
    isolated_command = {"contract_version": "analytical-authoring/v1", "definition": persisted_isolation, "block_id": target_block}
    assert client.post("/reports/composer/v1/preflight", headers=headers, json=isolated_command).status_code == 200
    assert client.post("/reports/composer/v1/apply", headers=headers, json=isolated_command).status_code == 200
    isolated_command["block_id"] = isolated["blocks"][4]["block_id"]
    assert client.post("/reports/composer/v1/apply", headers=headers, json=isolated_command).status_code == 400
    assert client.post("/reports/composer/v1/validate", headers=headers, json=persisted_isolation).status_code == 400
    pair_definition = deepcopy(scoped_definition)
    right_block = pair_definition["blocks"][4]["block_id"]
    pair_definition["pair"] = {"left_block_id": target_block, "right_block_id": right_block}
    pair_refs = [{"block_id": target_block, "result_id": scoped_result["result_id"]},
                 {"block_id": right_block, "result_id": scoped_result["result_id"]}]
    pair_response = client.post("/reports/composer/v1/compare", headers=headers, json={
        "contract_version": "analytical-authoring/v1", "definition": pair_definition, "results": pair_refs})
    assert pair_response.status_code == 200, pair_response.text
    comparison = pair_response.json()
    assert comparison["mode"] == "pair" and comparison["comparability_status"] == "comparable"
    pair_body = {"contract_version": "analytical-authoring/v1", "definition": pair_definition,
                 "expected_revision": 1, "idempotency_key": str(uuid4()), "results": pair_refs, "comparison": comparison}
    pair_save = client.post("/reports/composer/v1/versions", headers=headers, json=pair_body)
    assert pair_save.status_code == 200, pair_save.text
    assert pair_save.json()["comparison"] == comparison
    assert client.get("/reports/composer/v1/" + scoped_report).json()["report"] == pair_save.json()
    forged_pair = deepcopy(pair_body)
    forged_pair.update(expected_revision=2, idempotency_key=str(uuid4()))
    forged_pair["comparison"]["totals"]["absolute_delta"] = "999999"
    denied_pair = client.post("/reports/composer/v1/versions", headers=headers, json=forged_pair)
    assert denied_pair.status_code == 409, denied_pair.text
    assert denied_pair.json()["code"] == "ARTIFACT_CORRUPT"
    missing_pair = deepcopy(pair_body)
    missing_pair.update(expected_revision=2, idempotency_key=str(uuid4()))
    missing_pair["definition"]["pair"] = None
    assert client.post("/reports/composer/v1/versions", headers=headers, json=missing_pair).status_code == 400
    unlocked = deepcopy(scoped_body)
    unlocked.update(expected_revision=1, idempotency_key=str(uuid4()))
    unlocked["definition"]["scopes"]["filters"] = []
    denied_unlock = client.post("/reports/composer/v1/versions", headers=headers, json=unlocked)
    assert denied_unlock.status_code == 400, denied_unlock.text
    assert denied_unlock.json()["code"] == "COMPOSER_SCOPE_LOCKED"
    assert client.get(f'/reports/composer/v1/{report}/snapshots/{saved["snapshot_id"]}').json()["report"] == saved
    reader = TestClient(app, base_url="https://testserver")
    reader_login = reader.post("/identity/login", json={"workspace_id": scenario["workspace"], "email": "admin_reader@example.test",
                              "password": "synthetic-reader-password", "device_label": "C02 denied reader"})
    assert reader_login.status_code == 200
    reader_headers = {"X-CSRF-Token": reader_login.json()["csrf_token"], "Origin": Settings().cors_allowed_origins[0]}
    assert reader.get("/reports/composer/v1/" + report).status_code in {403, 404}
    assert reader.post("/reports/composer/v1/versions", headers=reader_headers, json=body).status_code == 403
    with psycopg.connect(host=settings.database_host, port=settings.database_port, dbname=settings.database_name,
                         user=settings.database_user, password=settings.read_database_password()) as connection:
        connection.execute("UPDATE identity_sessions SET revoked_at=now() WHERE id=%s", (author_session,))
    assert client.get("/reports/composer/v1/" + report).status_code == 401
    assert client.post("/reports/composer/v1/versions", headers=headers, json=body).status_code == 401
