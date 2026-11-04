"""Genuine saved v4 read with a current scoped API token lacking analysis.run."""

from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
from uuid import UUID, uuid4
import psycopg
import pytest
from fastapi.testclient import TestClient
from custometry_api.config import Settings
from packages.identity_access.application.service import IdentityService
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository

ROOT = Path(__file__).resolve().parents[3]


def test_saved_cohort_read_does_not_require_or_enable_run(tmp_path, monkeypatch):
    if os.environ.get("MS010_OWNED_DATABASE") != "1":
        pytest.skip("requires owned disposable run_retail_filters")
    corpus_path = tmp_path / "corpus.json"
    monkeypatch.setenv("MS004_S04_CORPUS_OUT", str(corpus_path))
    spec = importlib.util.spec_from_file_location(
        "cohort_saved_fixture", ROOT / "tests/e2e/ms-004-workspace/scenario.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    app = module.create_scenario(tmp_path / "artifacts")
    corpus = json.loads(corpus_path.read_text())
    settings = Settings()
    client = TestClient(app, base_url="https://testserver")
    login = client.post(
        "/identity/login",
        json={
            "workspace_id": corpus["workspace_id"],
            "email": "author@example.test",
            "password": "synthetic-author-password",
            "device_label": "MS024 saved proof",
        },
    )
    assert login.status_code == 200
    headers = {
        "X-CSRF-Token": login.json()["csrf_token"],
        "Origin": settings.cors_allowed_origins[0],
    }
    report = str(uuid4())
    dataset = corpus["semantic_dataset_version_id"]
    prepared = client.post(
        "/reports/composer/v1/prepare",
        headers=headers,
        json={
            "report_id": report,
            "semantic_dataset_version_id": dataset,
            "common_context": {
                "starts_on": "2025-01-01",
                "ends_on": "2025-01-31",
                "store_ids": None,
            },
            "template": "blank",
            "locale": "en",
        },
    )
    assert prepared.status_code == 200, prepared.json().get("code")
    definition = prepared.json()["definition"]
    native = client.post(
        "/reports/v2/new/prepare",
        headers=headers,
        json={
            "report_id": str(uuid4()),
            "semantic_dataset_version_id": dataset,
            "common_context": {
                "starts_on": "2025-01-01",
                "ends_on": "2025-01-31",
                "store_ids": None,
            },
            "template": "blank",
            "locale": "en",
        },
    )
    assert native.status_code == 200, native.json().get("code")
    catalog = client.get(f"/reports/composer/v1/filters/v4/{dataset}/catalog").json()
    root, customer, child = map(str, (uuid4(), uuid4(), uuid4()))
    edge = catalog["relationships"][0]["relationship"]
    event = catalog["events"][0]
    field = next(
        f["field"] for f in catalog["fields"] if f["field"]["field_id"] == "Receipt.receipt_id"
    )
    sequence = {
        "kind": "sequence",
        "node_id": str(uuid4()),
        "scope_id": customer,
        "parent_scope_id": customer,
        "relationship_id": edge["relationship_id"],
        "relationship_version_id": edge["version_id"],
        "child_entity": "Receipt",
        "window": {"kind": "fixed", "timezone": "UTC", **event["observation"]},
        "steps": [
            {
                "kind": "positive",
                "step_id": str(uuid4()),
                "child_scope_id": child,
                "event": event["definition"],
                "predicate": {
                    "kind": "predicate",
                    "node_id": str(uuid4()),
                    "scope_id": child,
                    "field_id": field["field_id"],
                    "field_version_id": field["version_id"],
                    "operator": "is_not_null",
                    "values": [],
                },
            }
        ],
    }
    value = {
        "schema_version": "receipt-filter/v4",
        "root_scope_id": root,
        "registry_versions": catalog["registry_versions"],
        "receipt_registry_versions": catalog["receipt_registry_versions"],
        "legacy_registry_version_id": catalog["legacy_registry_version_id"],
        "expression": {
            "kind": "customer_event_membership",
            "node_id": str(uuid4()),
            "scope_id": root,
            "customer_scope_id": customer,
            "relationship_id": edge["relationship_id"],
            "relationship_version_id": edge["version_id"],
            "predicate": sequence,
        },
    }
    source, block = map(str, (uuid4(), uuid4()))
    metric = corpus["metric_refs"][0]
    definition["definitions"] = [
        {
            "definition_id": source,
            "provider": "metric-workspace/v2",
            "query": {
                "semantic_dataset_version_id": dataset,
                "common": {"starts_on": "2025-01-01", "ends_on": "2025-01-31", "store_ids": None},
                "local_store_ids": None,
                "grain": "month",
                "calendar_ref": native.json()["definition"]["calendar_ref"],
                "calendar_basis": "calendar",
                "alignment": "none",
                "metric_refs": [metric],
                "receipt_filter": value,
            },
        }
    ]
    definition["blocks"] = [
        {
            "block_id": block,
            "section_id": definition["sections"][0]["section_id"],
            "order": 0,
            "block_type": "table",
            "source": {"definition_id": source, "metric_ref": metric},
            "presentation": {"title": "Saved cohort"},
            "placement": {"column": 0, "span": 12, "row": 0},
        }
    ]
    apply = {
        "contract_version": "analytical-authoring/v1",
        "definition": definition,
        "block_id": block,
    }
    result = client.post("/reports/composer/v1/apply", headers=headers, json=apply)
    assert result.status_code == 200, result.json().get("code")
    result_id = result.json()["result"]["result_id"]
    saved = client.post(
        "/reports/composer/v1/versions",
        headers=headers,
        json={
            "contract_version": "analytical-authoring/v1",
            "definition": definition,
            "expected_revision": 0,
            "idempotency_key": str(uuid4()),
            "results": [{"block_id": block, "result_id": result_id}],
        },
    )
    assert saved.status_code == 200, saved.json().get("code")

    def connect():
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
        )

    identity = IdentityService(
        PostgresIdentityRepository(connect), bootstrap_secret="synthetic-bootstrap"
    )
    full = identity.login(
        workspace_id=UUID(corpus["workspace_id"]),
        email="author@example.test",
        password="synthetic-author-password",
        device_label="MS024 token issuer",
    )
    actor = identity.authenticate(full.access_token)
    token = identity.issue_api_token(
        actor,
        name="MS024 disposable read without run",
        scopes=sorted(actor.permissions - {"analysis.run"}),
        expires_in_hours=1,
    )
    assert "analysis.run" not in identity.authenticate(token.token).permissions
    read_client = TestClient(
        app, base_url="https://testserver", headers={"Authorization": f"Bearer {token.token}"}
    )
    reopened = read_client.get("/reports/composer/v1/" + report)
    assert reopened.status_code == 200, reopened.json().get("code")
    assert reopened.json()["report"] == saved.json()
    snapshot = saved.json()["snapshot_id"]
    read_result = read_client.get(
        f"/reports/composer/v1/{report}/snapshots/{snapshot}/blocks/{block}/result"
    )
    assert read_result.status_code == 200, read_result.json().get("code")
    assert read_result.json()["result"]["result_id"] == result_id
    assert read_client.post("/reports/composer/v1/apply", json=apply).status_code == 403
    assert (
        read_client.post(
            "/reports/composer/v1/filters/v4/preview",
            json={"dataset_version_id": dataset, "filter": value},
        ).status_code
        == 403
    )
    assert (
        read_client.post(
            "/reports/composer/v1/filters/v4/facets",
            json={
                "dataset_version_id": dataset,
                "filter": value,
                "facet": {"entity": "Receipt", "field_id": "Receipt.status", "limit": 10},
            },
        ).status_code
        == 403
    )
    identity.revoke_api_token(actor, token.token_id)
    assert read_client.get("/reports/composer/v1/" + report).status_code == 401
