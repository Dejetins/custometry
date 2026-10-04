"""S03 real source intake, Identity sessions and atomic report/view persistence."""

from __future__ import annotations
import json
import os
from pathlib import Path
from uuid import UUID, uuid4
from datetime import date
from typing import Any, Callable, NoReturn, TypedDict, cast
from httpx import Response
import psycopg
import pytest
from fastapi.testclient import TestClient
from custometry_api.config import Settings
from custometry_api.main import create_app
from packages.identity_access.application.service import IdentityService
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository
from packages.identity_access.application.organization import OrganizationService
from packages.identity_access.infrastructure.organization_postgres import (
    PostgresOrganizationRepository,
)
from packages.contracts.analytics.sales_report import SalesReportRequest
from packages.contracts.presentation import SaveRequest
from packages.presentation.application.reports import ReportService
from packages.presentation.infrastructure.postgres import PostgresReportRepository
from packages.artifacts.infrastructure.document_snapshots import DocumentSnapshotArtifacts
from packages.artifacts.infrastructure.local import LocalArtifactStore
from apps.worker_data.vertical_slice import DataPipelineRunner
from custometry_api.analytics.router import build_analytics_services
from tests.integration.data_pipeline.conftest import DataPipelineRuntime
from tests.integration.data_pipeline.test_retail_report import request_for
from plugins.connector_postgresql.adapter import PostgreSQLConnector, PostgreSQLTarget

ROOT = Path(__file__).resolve().parents[3]


class ActorArguments(TypedDict):
    workspace_id: UUID
    principal_id: UUID
    permissions: frozenset[str]


def test_real_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    if os.environ.get("MS004_S03_OWNED_DATABASE") != "1":
        pytest.skip("requires S03 disposable runner")
    settings = Settings(analytics_artifact_root=tmp_path)

    def connect() -> psycopg.Connection[tuple[Any, ...]]:
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
    boot = identity.bootstrap(
        presented_secret="synthetic-bootstrap",
        email="author@example.test",
        password="synthetic-author-password",
        workspace_key="s03-owned",
        workspace_name="S03",
    )
    tokens = identity.login(
        email="author@example.test",
        password="synthetic-author-password",
        workspace_id=boot.workspace_id,
        device_label="S03",
    )
    actor = identity.authenticate(tokens.access_token)
    organization = OrganizationService(PostgresOrganizationRepository(connect))
    units = organization.list_units(actor)
    root = UUID(str(units[0]["org_unit_id"]))
    department = organization.create_unit(
        actor, key="sales", kind="department", parent_org_unit_id=root, display_name="Sales"
    )
    department_id = UUID(str(department["org_unit_id"]))
    organization.assign_primary(actor, principal_id=actor.principal_id, org_unit_id=department_id)
    draft = organization.create_policy_draft(
        actor,
        policy_id=None,
        org_unit_id=department_id,
        expected_version=None,
        allowed_actions=("view_snapshot", "run", "edit"),
        row_scope_refs=(),
        column_policy_refs=(),
        pii_allowed=False,
        include_descendants=True,
        effective_from=None,
    )
    published = organization.publish_policy(
        actor,
        policy_id=UUID(str(draft["policy_id"])),
        expected_version=int(cast(int, draft["version"])),
        effective_from=None,
    )
    source = PostgreSQLConnector(
        PostgreSQLTarget(
            host=os.environ["CUSTOMETRY_TEST_SOURCE_HOST"],
            port=int(os.environ["CUSTOMETRY_TEST_SOURCE_PORT"]),
            dbname=os.environ["CUSTOMETRY_TEST_SOURCE_DATABASE"],
            user=os.environ["CUSTOMETRY_TEST_SOURCE_USER"],
            password=Path(os.environ["CUSTOMETRY_TEST_SOURCE_PASSWORD_FILE"]).read_text().strip(),
        )
    )
    runtime = DataPipelineRuntime(connect, source, actor.workspace_id, actor.principal_id)
    intake = DataPipelineRunner(
        connector=source, connect=connect, artifact_store=LocalArtifactStore(tmp_path)
    ).run(request_for(runtime))
    dataset = intake.semantic_dataset_version_id
    assert dataset is not None

    def bind(
        kind: str, resource: UUID, owner: UUID = actor.principal_id, stores: tuple[str, ...] = ()
    ) -> dict[str, object]:
        return organization.bind_resource(
            actor,
            resource_type=kind,
            resource_id=resource,
            creator_principal_id=actor.principal_id,
            owner_type="principal",
            owner_id=owner,
            allowed_actions=("view_snapshot", "run", "edit"),
            required_row_scope_refs=stores,
            required_column_policy_refs=(),
            requires_pii=False,
            effective_from=None,
        )

    _, legacy_analytics = build_analytics_services(settings)
    result = legacy_analytics.run_sales_report(
        workspace_id=actor.workspace_id,
        principal_id=actor.principal_id,
        permissions=actor.permissions,
        request=SalesReportRequest(
            dataset,
            starts_on=date(2025, 1, 1),
            ends_on=date(2025, 1, 31),
            comparison="previous_year_same_dates",
        ),
    )
    legacy = ReportService(
        PostgresReportRepository(connect),
        legacy_analytics,
        DocumentSnapshotArtifacts(connect, tmp_path),
        json.loads(
            (ROOT / "packages/presentation/infrastructure/system-brand.v1.json").read_text()
        ),
    )
    args = cast(
        ActorArguments,
        dict(
            workspace_id=actor.workspace_id,
            principal_id=actor.principal_id,
            permissions=actor.permissions,
        ),
    )
    refs = legacy.prepare(**args, result_id=UUID(result["result_id"]))
    old_request = SaveRequest(
        contract_version="draft-report/v1",
        result_id=result["result_id"],
        title="Original",
        expected_revision=0,
        idempotency_key=uuid4(),
        **{n: refs[n]["reference"] for n in ("chart_spec", "brand_profile", "company_pack")},
    )
    old = legacy.save(**args, request=old_request)
    report = old["report_id"]
    app = create_app(settings=settings)
    client = TestClient(app)
    headers = {"Authorization": f"Bearer {tokens.access_token}"}
    observed_statuses: dict[str, int] = {}

    def req(
        method: str,
        path: str,
        body: object = None,
        expected: int = 200,
        using: dict[str, str] = headers,
    ) -> Any:
        response = client.request(method, path, headers=using, json=body)
        assert response.status_code == expected, (path, response.status_code, response.text[:800])
        key = str(expected)
        observed_statuses[key] = observed_statuses.get(key, 0) + 1
        return response.json()

    base = f"/reports/v2/{report}"
    # Actual pre-S03 baseline: neither report nor dataset has an organization binding.
    assert req("GET", f"/reports/{report}") == old
    assert req("GET", f"/reports/{report}/snapshots/{old['snapshot_id']}") == old
    assert req("POST", "/reports/", old_request.model_dump(mode="json")) == old
    stranger_invite = identity.invite(
        actor,
        workspace_id=actor.workspace_id,
        email="stranger@example.test",
        roles=["analyst"],
        expires_in_hours=1,
    )
    identity.accept_invitation(token=stranger_invite.token, password="synthetic-stranger-password")
    stranger = identity.login(
        email="stranger@example.test",
        password="synthetic-stranger-password",
        workspace_id=actor.workspace_id,
        device_label="stranger",
    )
    req(
        "GET",
        f"/reports/{report}",
        using={"Authorization": f"Bearer {stranger.access_token}"},
        expected=403,
    )
    # Direct v2 never gains the internal legacy exact-snapshot exception.
    req("GET", f"/analytics/metric-workspace/v2/datasets/{dataset}/context", expected=403)
    assert req("GET", base)["definition"]["report_id"] == report
    bind("analysis", dataset)
    editor = req("GET", base)
    assert editor["report"] == old
    definition = editor["definition"]
    definition["title"] = "Personal workspace"
    applied = req(
        "POST",
        base + "/apply",
        dict(
            contract_version="configured-report/v2",
            mode="creator",
            base_revision=1,
            definition=definition,
        ),
    )
    request: dict[str, Any] = dict(
        contract_version="configured-report/v2",
        definition=definition,
        expected_revision=1,
        expected_saved_view_revision=0,
        idempotency_key=str(uuid4()),
        configuration_hash=applied["configuration_hash"],
        result_ids=[b["result"]["result_id"] for b in applied["bindings_by_card"]],
        chart_specs=applied["chart_specs"],
    )
    saved = req("POST", base + "/versions", request)
    assert saved["revision"] == 2
    assert req("POST", base + "/versions", request) == saved
    assert req("GET", base)["report"] == saved
    assert req("GET", f"/reports/{report}/snapshots/{old['snapshot_id']}") == old
    req("GET", f"/reports/{report}", expected=409)
    assert req("GET", base + "/saved-views")[0]["revision"] == 1
    # Comparison bytes are indispensable even though result and root/page bytes remain intact.
    comparison = saved["composition"]["comparisons"][0]["manifest"]
    with connect() as c:
        uri = cast(
            tuple[Any, ...],
            c.execute(
                "SELECT relative_uri FROM artifact_manifests WHERE id=%s",
                (comparison["artifact_id"],),
            ).fetchone(),
        )[0]
    path = tmp_path / uri
    raw = path.read_bytes()
    path.unlink()
    req("GET", base, expected=409)
    path.write_bytes(b"corrupt")
    req("GET", base, expected=409)
    path.write_bytes(raw)
    # Result artifacts have the same mandatory integrity boundary on exact reads.
    result_manifest = saved["composition"]["bindings_by_card"][0]["result"]["manifest"]
    with connect() as c:
        result_uri = cast(
            tuple[Any, ...],
            c.execute(
                "SELECT relative_uri FROM artifact_manifests WHERE id=%s",
                (result_manifest["artifact_id"],),
            ).fetchone(),
        )[0]
    result_path = tmp_path / result_uri
    result_bytes = result_path.read_bytes()
    result_path.unlink()
    assert req("GET", base, expected=409)["code"] == "ARTIFACT_MISSING"
    result_path.write_bytes(b"corrupt")
    assert req("GET", base, expected=409)["code"] == "ARTIFACT_CORRUPT"
    result_path.write_bytes(result_bytes)
    # Same key/different semantic body and stale report revision both leave revision 2 intact.
    from copy import deepcopy

    altered = deepcopy(request)
    altered["definition"]["title"] = "Changed idempotency body"
    req("POST", base + "/versions", altered, expected=409)
    stale = deepcopy(request)
    stale["idempotency_key"] = str(uuid4())
    req("POST", base + "/versions", stale, expected=409)
    # Title/order/display reuse: exact bindings can be re-prepared without analysis.run.
    scoped = identity.issue_api_token(
        actor,
        name="read-manage",
        scopes=[p for p in actor.permissions if p != "analysis.run"],
        expires_in_hours=1,
    )
    readonly_run = {"Authorization": f"Bearer {scoped.token}"}
    definition["title"] = "No compute title"
    definition["worksets"][0]["cards"].reverse()
    ids_by_card = {b["card_id"]: b["result"]["result_id"] for b in applied["bindings_by_card"]}
    reused_ids = [ids_by_card[c["card_id"]] for c in definition["worksets"][0]["cards"]]
    definition["selection"] = {
        "mode": "pair",
        "left_card_id": definition["worksets"][0]["cards"][0]["card_id"],
        "right_card_id": definition["worksets"][0]["cards"][1]["card_id"],
        "display": "series",
    }
    body: dict[str, Any] = dict(
        contract_version="configured-report/v2",
        mode="creator",
        base_revision=2,
        definition=definition,
        reuse_result_ids=reused_ids,
    )
    from packages.analytics_core.application.workspace_service import WorkspaceAnalyticsService

    def no_compute(*args: Any, **kwargs: Any) -> NoReturn:
        raise AssertionError("display-only must not compute")

    with monkeypatch.context() as m:
        m.setattr(WorkspaceAnalyticsService, "run", no_compute)
        prepared = req("POST", base + "/apply", body, using=readonly_run)
        display_save: dict[str, Any] = dict(
            contract_version="configured-report/v2",
            definition=definition,
            expected_revision=2,
            expected_saved_view_revision=1,
            idempotency_key=str(uuid4()),
            configuration_hash=prepared["configuration_hash"],
            result_ids=reused_ids,
            chart_specs=prepared["chart_specs"],
        )
        display_saved = req("POST", base + "/versions", display_save, using=readonly_run)
    assert display_saved["revision"] == 3
    req(
        "POST",
        base + "/apply",
        {k: v for k, v in body.items() if k != "reuse_result_ids"},
        using=readonly_run,
        expected=403,
    )
    # Cookie session mutations require both same-origin and CSRF, including direct Analytics.
    cookies = TestClient(app)
    cookies.cookies.set("custometry_access", tokens.access_token)
    assert cookies.post(base + "/apply", json=body).status_code == 403
    assert (
        cookies.post(
            base + "/apply", json=body, headers={"Origin": "http://127.0.0.1:5173"}
        ).status_code
        == 403
    )
    assert client.get(base).status_code == 401
    # Reader/admin with explicit grants sees the original base, never creator's personal overlay.
    invitation = identity.invite(
        actor,
        workspace_id=actor.workspace_id,
        email="reader@example.test",
        roles=["analyst", "workspace_admin"],
        expires_in_hours=1,
    )
    reader_id = identity.accept_invitation(
        token=invitation.token, password="synthetic-reader-password"
    )
    reader_tokens = identity.login(
        email="reader@example.test",
        password="synthetic-reader-password",
        workspace_id=actor.workspace_id,
        device_label="S03-reader",
    )
    organization.assign_primary(actor, principal_id=reader_id, org_unit_id=department_id)
    reader_headers = {"Authorization": f"Bearer {reader_tokens.access_token}"}
    req(
        "GET", base, using=reader_headers, expected=403
    )  # unbound legacy report never grants others
    bind("report", UUID(report))
    grants: list[dict[str, object]] = []
    for kind, resource in [("report", UUID(report)), ("analysis", dataset)]:
        grants.append(
            organization.create_grant(
                actor,
                subject_type="principal",
                subject_id=reader_id,
                target_org_unit_id=department_id,
                resource_type=kind,
                resource_id=resource,
                actions=("view_snapshot", "run", "edit"),
                reason="S03 synthetic reader",
                effective_from=None,
                expires_at=None,
            )
        )
    reader_editor = req("GET", base, using=reader_headers)
    assert reader_editor["report"] == old and reader_editor["definition"] is None
    req("GET", base + f"/snapshots/{saved['snapshot_id']}", using=reader_headers, expected=404)
    req("POST", base + "/versions", display_save, using=reader_headers, expected=403)
    req(
        "POST",
        f"/reports/{report}/versions",
        dict(
            contract_version="draft-report/v1",
            result_id=result["result_id"],
            title="Attempt",
            expected_revision=3,
            idempotency_key=str(uuid4()),
            **{n: refs[n]["reference"] for n in ("chart_spec", "brand_profile", "company_pack")},
        ),
        using=reader_headers,
        expected=403,
    )
    # Direct result access remains actor-private even when the reader can inspect authorized base bytes.
    analytics_base = "/analytics/metric-workspace/v2"
    result_id = request["result_ids"][0]
    req(
        "GET",
        f"{analytics_base}/datasets/{dataset}/results/{result_id}",
        using=reader_headers,
        expected=404,
    )
    # Reader view changes have their own CAS and do not touch the report's revision.
    base_def = reader_editor["base_definition"]
    override: dict[str, Any] = dict(
        query_context={**base_def["common_context"], "grain": "month"},
        display=dict(
            active_workset_id=base_def["default_workset_id"],
            selection=base_def["selection"],
            card_order=[c["card_id"] for c in base_def["worksets"][0]["cards"]],
            hidden_card_ids=[],
            representation="table",
            density="compact",
        ),
    )
    reader_apply = req(
        "POST",
        base + "/apply",
        dict(
            contract_version="configured-report/v2",
            mode="reader",
            base_revision=1,
            view_override=override,
        ),
        using=reader_headers,
    )
    view_request: dict[str, Any] = dict(
        contract_version="saved-view/v1",
        document_version_id=old["version_id"],
        expected_revision=0,
        idempotency_key=str(uuid4()),
        view_override=override,
        result_ids=[b["result"]["result_id"] for b in reader_apply["bindings_by_card"]],
    )
    view = req("POST", base + "/saved-views", view_request, using=reader_headers)
    assert req("POST", base + "/saved-views", view_request, using=reader_headers) == view
    assert req("GET", base + "/saved-views", using=reader_headers) == [view]
    assert req("GET", base)["report"]["revision"] == 3
    req(
        "POST",
        base + f"/saved-views/{view['saved_view_id']}/versions",
        {**view_request, "expected_revision": 1, "idempotency_key": str(uuid4())},
        expected=404,
    )
    # An admin role never supersedes immutable creator; the actual grant above includes edit.
    assert not reader_editor["capabilities"]["definition_edit"]
    # Cross-workspace session and viewer role have no implicit data/run grant.
    other = identity.create_workspace(actor, key="s03-other", name="Other")
    other_tokens = identity.login(
        email="author@example.test",
        password="synthetic-author-password",
        workspace_id=other.workspace_id,
        device_label="other",
    )
    foreign = {"Authorization": f"Bearer {other_tokens.access_token}"}
    req("GET", base, using=foreign, expected=404)
    for suffix in ("context", "catalog", f"results/{result_id}"):
        req("GET", f"{analytics_base}/datasets/{dataset}/{suffix}", using=foreign, expected=403)
    # Competing Save uses report and companion CAS together; exactly one durable revision wins.
    current = req("GET", base)
    definition = current["definition"]

    def prepare_save(title: str, revision: int, view_revision: int) -> dict[str, Any]:
        candidate = deepcopy(definition)
        candidate["title"] = title
        p = req(
            "POST",
            base + "/apply",
            dict(
                contract_version="configured-report/v2",
                mode="creator",
                base_revision=revision,
                definition=candidate,
                reuse_result_ids=reused_ids,
            ),
        )
        return dict(
            contract_version="configured-report/v2",
            definition=candidate,
            expected_revision=revision,
            expected_saved_view_revision=view_revision,
            idempotency_key=str(uuid4()),
            configuration_hash=p["configuration_hash"],
            result_ids=reused_ids,
            chart_specs=p["chart_specs"],
        )

    one = prepare_save("Race one", 3, 2)
    two = prepare_save("Race two", 3, 2)
    from concurrent.futures import ThreadPoolExecutor

    def submit_save(b: dict[str, Any]) -> Response:
        return client.post(base + "/versions", headers=headers, json=b)

    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(submit_save, [one, two]))
    assert sorted(r.status_code for r in responses) == [200, 409]
    winner = next(r.json() for r in responses if r.status_code == 200)
    assert winner["revision"] == 4
    # After a successful commit, a simulated client retry returns the identical stored winner.
    winning_request = one if winner["composition"]["definition"]["title"] == "Race one" else two
    assert req("POST", base + "/versions", winning_request) == winner
    definition = winner["composition"]["definition"]
    failure_request = prepare_save("Must not switch", 4, 3)
    from packages.presentation.infrastructure.workspace import PostgresWorkspaceRepository

    original_save = PostgresWorkspaceRepository.save_workspace

    def failed_transaction(
        self: PostgresWorkspaceRepository, *args: Any, **kwargs: Any
    ) -> dict[str, Any]:
        def failure() -> NoReturn:
            raise psycopg.OperationalError("synthetic pre-pointer failure")

        setattr(self, "_checkpoint", failure)
        return original_save(self, *args, **kwargs)

    with monkeypatch.context() as m:
        m.setattr(PostgresWorkspaceRepository, "save_workspace", failed_transaction)
        req("POST", base + "/versions", failure_request, expected=503)
    with connect() as c:
        assert (
            cast(
                tuple[Any, ...],
                c.execute(
                    "SELECT revision FROM presentation_documents WHERE id=%s", (report,)
                ).fetchone(),
            )[0]
            == 4
        )
        assert (
            cast(
                tuple[Any, ...],
                c.execute(
                    "SELECT revision FROM presentation_saved_views WHERE id=%s",
                    (
                        str(
                            __import__(
                                "packages.contracts.presentation.workspace",
                                fromlist=["creator_saved_view_id"],
                            ).creator_saved_view_id(UUID(report), actor.principal_id)
                        ),
                    ),
                ).fetchone(),
            )[0]
            == 3
        )

    def failed_artifact(self: DocumentSnapshotArtifacts, **kwargs: Any) -> NoReturn:
        from packages.contracts.presentation import PresentationFailure

        raise PresentationFailure("STORAGE_UNAVAILABLE")

    with monkeypatch.context() as m:
        m.setattr(DocumentSnapshotArtifacts, "commit", failed_artifact)
        req("POST", base + "/versions", failure_request, expected=503)
    assert req("GET", base)["report"] == winner
    # Pinned calendar survives a changed default; adoption requires new Apply and Save.
    calendar = req("GET", "/semantic/workspace-calendar/v1")
    profile = dict(calendar["calendar"]["profile"])
    profile["fiscal_year_start_month"] = 4
    new_calendar = req(
        "POST",
        "/semantic/workspace-calendar/v1/versions",
        dict(profile=profile, expected_revision=calendar["revision"], idempotency_key=str(uuid4())),
    )
    assert req("GET", base)["report"] == winner
    definition = deepcopy(definition)
    definition["calendar_ref"] = {
        k: new_calendar["calendar"][k] for k in ("version_id", "content_hash")
    }
    definition["calendar_basis"] = "fiscal"
    adoption = req(
        "POST",
        base + "/apply",
        dict(
            contract_version="configured-report/v2",
            mode="creator",
            base_revision=4,
            definition=definition,
        ),
    )
    adoption_request: dict[str, Any] = dict(
        contract_version="configured-report/v2",
        definition=definition,
        expected_revision=4,
        expected_saved_view_revision=3,
        idempotency_key=str(uuid4()),
        configuration_hash=adoption["configuration_hash"],
        result_ids=[b["result"]["result_id"] for b in adoption["bindings_by_card"]],
        chart_specs=adoption["chart_specs"],
    )
    adopted = req("POST", base + "/versions", adoption_request)
    assert (
        adopted["revision"] == 5
        and adopted["composition"]["definition"]["calendar_ref"]
        != winner["composition"]["definition"]["calendar_ref"]
    )
    assert req("GET", base + f"/snapshots/{winner['snapshot_id']}")["report"] == winner
    # Direct Analytics public routes authenticate and enforce CSRF/current data ceilings.
    query: dict[str, Any] = dict(
        semantic_dataset_version_id=str(dataset),
        common=definition["common_context"],
        local_store_ids=None,
        grain=definition["grain"],
        calendar_ref=definition["calendar_ref"],
        calendar_basis="fiscal",
        alignment="previous_year_same_dates",
        metric_refs=[c["metric_ref"] for c in definition["worksets"][0]["cards"]],
    )
    direct = req("POST", analytics_base + "/results", query)
    for suffix in ("context", "catalog", f"results/{direct['result_id']}"):
        req("GET", f"{analytics_base}/datasets/{dataset}/{suffix}")
    assert cookies.post(analytics_base + "/results", json=query).status_code == 403
    # All worksets (including inactive cards) are required; empty configurations stay valid.
    extra_old = legacy.save(
        **args,
        request=SaveRequest(
            contract_version="draft-report/v1",
            result_id=result["result_id"],
            title="Multi",
            expected_revision=0,
            idempotency_key=uuid4(),
            **{n: refs[n]["reference"] for n in ("chart_spec", "brand_profile", "company_pack")},
        ),
    )
    extra_base = f"/reports/v2/{extra_old['report_id']}"
    multi = req("GET", extra_base)["definition"]
    inactive = deepcopy(multi["worksets"][0])
    inactive["workset_id"] = str(uuid4())
    inactive["name"] = {"en": "Inactive", "ru": "Неактивный"}
    inactive["cards"] = inactive["cards"][:1]
    inactive["cards"][0]["card_id"] = str(uuid4())
    inactive["cards"][0]["local_store_ids"] = ["2"]
    multi["worksets"].append(inactive)
    multi_apply = req(
        "POST",
        extra_base + "/apply",
        dict(
            contract_version="configured-report/v2",
            mode="creator",
            base_revision=1,
            definition=multi,
        ),
    )
    assert len(multi_apply["bindings_by_card"]) == 4
    multi_request: dict[str, Any] = dict(
        contract_version="configured-report/v2",
        definition=multi,
        expected_revision=1,
        expected_saved_view_revision=0,
        idempotency_key=str(uuid4()),
        configuration_hash=multi_apply["configuration_hash"],
        result_ids=[b["result"]["result_id"] for b in multi_apply["bindings_by_card"]],
        chart_specs=multi_apply["chart_specs"],
    )
    req(
        "POST",
        extra_base + "/versions",
        {**multi_request, "result_ids": multi_request["result_ids"][:-1]},
        expected=400,
    )
    multi_saved = req("POST", extra_base + "/versions", multi_request)
    assert len(req("GET", extra_base)["report"]["composition"]["bindings_by_card"]) == 4
    companion = req("GET", extra_base + "/saved-views")[0]
    companion_request: dict[str, Any] = dict(
        contract_version="saved-view/v1",
        document_version_id=multi_saved["version_id"],
        expected_revision=1,
        idempotency_key=str(uuid4()),
        view_override=dict(
            query_context=companion["query_context"],
            display={**companion["display"], "density": "compact"},
        ),
        result_ids=multi_request["result_ids"],
    )
    req(
        "POST",
        extra_base + f"/saved-views/{companion['saved_view_id']}/versions",
        companion_request,
    )
    conflict = {
        **multi_request,
        "expected_revision": 2,
        "expected_saved_view_revision": 1,
        "idempotency_key": str(uuid4()),
    }
    assert (
        req("POST", extra_base + "/versions", conflict, expected=409)["code"]
        == "SAVED_VIEW_REVISION_CONFLICT"
    )
    empty = deepcopy(multi)
    empty["worksets"] = []
    empty["default_workset_id"] = None
    empty["selection"] = None
    empty_apply = req(
        "POST",
        extra_base + "/apply",
        dict(
            contract_version="configured-report/v2",
            mode="creator",
            base_revision=2,
            definition=empty,
        ),
    )
    empty_request: dict[str, Any] = dict(
        contract_version="configured-report/v2",
        definition=empty,
        expected_revision=2,
        expected_saved_view_revision=2,
        idempotency_key=str(uuid4()),
        configuration_hash=empty_apply["configuration_hash"],
        result_ids=[],
        chart_specs=[],
    )
    emptied = req("POST", extra_base + "/versions", empty_request)
    assert emptied["composition"]["bindings_by_card"] == []
    assert req("GET", extra_base)["report"] == emptied
    assert (
        req("POST", extra_base + "/versions", multi_request) == multi_saved
    )  # historical replay after deletions
    req(
        "POST",
        extra_base + "/apply",
        dict(
            contract_version="configured-report/v2",
            mode="creator",
            base_revision=3,
            definition=multi,
        ),
        expected=400,
    )
    too_many = deepcopy(definition)
    too_many["worksets"] = too_many["worksets"] * 21
    assert (
        req(
            "POST",
            base + "/apply",
            dict(
                contract_version="configured-report/v2",
                mode="creator",
                base_revision=5,
                definition=too_many,
            ),
            expected=413,
        )["code"]
        == "WORKSPACE_LIMIT_EXCEEDED"
    )
    req(
        "POST",
        base + "/apply",
        dict(
            contract_version="unsupported", mode="creator", base_revision=5, definition=definition
        ),
        expected=422,
    )
    list_old = legacy.save(
        **args,
        request=SaveRequest(
            contract_version="draft-report/v1",
            result_id=result["result_id"],
            title="List legacy",
            expected_revision=0,
            idempotency_key=uuid4(),
            **{n: refs[n]["reference"] for n in ("chart_spec", "brand_profile", "company_pack")},
        ),
    )
    listing = req("GET", "/reports/?offset=0&limit=1")
    assert listing["visible_count"] == 3 and len(listing["reports"]) == 1
    assert {r["report_id"] for r in req("GET", "/reports/?offset=0&limit=20")["reports"]} == {
        report,
        extra_old["report_id"],
        list_old["report_id"],
    }
    reader_listing = req("GET", "/reports/?offset=0&limit=20", using=reader_headers)
    assert (
        reader_listing["visible_count"] == 1
        and reader_listing["reports"][0]["title"] == old["title"]
    )

    # Revoked data scope blocks direct results/context/catalog/compare and both report write versions.
    def revoke_data() -> None:
        organization.bind_resource(
            actor,
            resource_type="analysis",
            resource_id=dataset,
            creator_principal_id=actor.principal_id,
            owner_type="principal",
            owner_id=actor.principal_id,
            allowed_actions=("edit",),
            required_row_scope_refs=(),
            required_column_policy_refs=(),
            requires_pii=False,
            effective_from=None,
        )

    committing = {
        **adoption_request,
        "expected_revision": 5,
        "expected_saved_view_revision": 4,
        "idempotency_key": str(uuid4()),
    }

    def revoke_at_commit(
        self: PostgresWorkspaceRepository, *args: Any, **kwargs: Any
    ) -> dict[str, Any]:
        setattr(self, "_checkpoint", revoke_data)
        return original_save(self, *args, **kwargs)

    with monkeypatch.context() as m:
        m.setattr(PostgresWorkspaceRepository, "save_workspace", revoke_at_commit)
        req("POST", base + "/versions", committing, expected=403)
    with connect() as c:
        assert (
            cast(
                tuple[Any, ...],
                c.execute(
                    "SELECT revision FROM presentation_documents WHERE id=%s", (report,)
                ).fetchone(),
            )[0]
            == 5
        )
    for suffix in ("context", "catalog", f"results/{direct['result_id']}"):
        req("GET", f"{analytics_base}/datasets/{dataset}/{suffix}", expected=403)
    req("POST", analytics_base + "/results", query, expected=403)
    req(
        "POST",
        analytics_base + "/comparisons",
        dict(
            semantic_dataset_version_id=str(dataset),
            left=adoption["bindings_by_card"][0],
            right=None,
        ),
        expected=403,
    )
    req("GET", base, expected=403)
    req("POST", base + "/versions", adoption_request, expected=403)
    req("GET", base + "/saved-views", using=reader_headers, expected=403)
    report_routes: list[tuple[str, str, dict[str, Any] | None]] = [
        ("GET", base, None),
        ("GET", base + f"/snapshots/{old['snapshot_id']}", None),
        ("POST", base + "/apply", body),
        ("POST", base + "/versions", adoption_request),
        ("GET", base + "/saved-views", None),
        ("POST", base + "/saved-views", view_request),
        ("POST", base + f"/saved-views/{view['saved_view_id']}/versions", view_request),
    ]
    direct_routes: list[tuple[str, str, dict[str, Any] | None]] = [
        ("GET", f"{analytics_base}/datasets/{dataset}/context", None),
        ("GET", f"{analytics_base}/datasets/{dataset}/catalog", None),
        ("GET", f"{analytics_base}/datasets/{dataset}/results/{direct['result_id']}", None),
        ("POST", analytics_base + "/results", query),
        (
            "POST",
            analytics_base + "/comparisons",
            dict(
                semantic_dataset_version_id=str(dataset),
                left=adoption["bindings_by_card"][0],
                right=None,
            ),
        ),
    ]
    for method, url, payload in report_routes:
        req(method, url, payload, using=foreign, expected=404)
    for method, url, payload in direct_routes:
        req(method, url, payload, using=foreign, expected=403)
    for method, url, payload in report_routes[:5] + direct_routes:
        req(method, url, payload, expected=403)
    for method, url, payload in report_routes[5:]:
        req(method, url, payload, using=reader_headers, expected=403)
    # New session cannot use old data after revocation, even for a still-v1 report.
    v1_update: dict[str, Any] = dict(
        contract_version="draft-report/v1",
        result_id=result["result_id"],
        title="Denied v1",
        expected_revision=1,
        idempotency_key=str(uuid4()),
        **{n: refs[n]["reference"] for n in ("chart_spec", "brand_profile", "company_pack")},
    )
    # Create a separate old document through the unchanged internal v1 service for this negative HTTP test.
    old2 = legacy.save(
        **args,
        request=SaveRequest(
            **cast(
                dict[str, Any], {**v1_update, "expected_revision": 0, "idempotency_key": uuid4()}
            )
        ),
    )
    req("POST", f"/reports/{old2['report_id']}/versions", v1_update, expected=403)
    with connect() as c:
        assert (
            cast(
                tuple[Any, ...],
                c.execute(
                    "SELECT revision FROM presentation_documents WHERE id=%s", (old2["report_id"],)
                ).fetchone(),
            )[0]
            == 1
        )
    # Restoring an allowed scope changes its version: old Apply bindings require re-Apply.
    bind("analysis", dataset)
    assert (
        req("POST", base + "/versions", committing, expected=409)["code"]
        == "ACCESS_CONTEXT_CHANGED"
    )
    # The unchanged v1 HTTP path also rechecks data immediately before latest switch.
    original_v1_save = PostgresReportRepository.save

    def revoke_v1_commit(self: PostgresReportRepository, *a: Any, **kw: Any) -> dict[str, Any]:
        current_check = cast(Callable[[], None], getattr(self, "_checkpoint"))

        def revoked_check() -> None:
            revoke_data()
            current_check()

        setattr(self, "_checkpoint", revoked_check)
        return original_v1_save(self, *a, **kw)

    with monkeypatch.context() as m:
        m.setattr(PostgresReportRepository, "save", revoke_v1_commit)
        req("POST", f"/reports/{old2['report_id']}/versions", v1_update, expected=403)
    with connect() as c:
        assert (
            cast(
                tuple[Any, ...],
                c.execute(
                    "SELECT revision FROM presentation_documents WHERE id=%s", (old2["report_id"],)
                ).fetchone(),
            )[0]
            == 1
        )
    # Current scope can authorize a narrower new query without changing exact old bytes.
    policy2 = organization.create_policy_draft(
        actor,
        policy_id=UUID(str(published["policy_id"])),
        org_unit_id=department_id,
        expected_version=int(cast(int, published["version"])),
        allowed_actions=("view_snapshot", "run", "edit"),
        row_scope_refs=("store:1",),
        column_policy_refs=(),
        pii_allowed=False,
        include_descendants=True,
        effective_from=None,
    )
    published2 = organization.publish_policy(
        actor,
        policy_id=UUID(str(policy2["policy_id"])),
        expected_version=int(cast(int, policy2["version"])),
        effective_from=None,
    )
    bind("analysis", dataset, stores=("store:1",))
    context = req("GET", f"{analytics_base}/datasets/{dataset}/context", using=reader_headers)
    assert [x["id"] for x in context["stores"]] == ["1"]
    req(
        "GET", base, using=reader_headers, expected=403
    )  # Exact broad base is never silently narrowed.
    narrow = deepcopy(override)
    narrow["query_context"]["store_ids"] = ["1"]
    narrower = req(
        "POST",
        base + "/apply",
        dict(
            contract_version="configured-report/v2",
            mode="reader",
            base_revision=1,
            view_override=narrow,
        ),
        using=reader_headers,
    )
    assert narrower["bindings_by_card"]
    req(
        "POST",
        analytics_base + "/results",
        {**query, "common": {**query["common"], "store_ids": ["2"]}},
        expected=403,
    )
    # An unknown row expression and any column ceiling fail closed even when named refs match.
    policy3 = organization.create_policy_draft(
        actor,
        policy_id=UUID(str(published2["policy_id"])),
        org_unit_id=department_id,
        expected_version=int(cast(int, published2["version"])),
        allowed_actions=("view_snapshot", "run", "edit"),
        row_scope_refs=("unimplemented:row",),
        column_policy_refs=("restricted:column",),
        pii_allowed=False,
        include_descendants=True,
        effective_from=None,
    )
    organization.publish_policy(
        actor,
        policy_id=UUID(str(policy3["policy_id"])),
        expected_version=int(cast(int, policy3["version"])),
        effective_from=None,
    )
    organization.bind_resource(
        actor,
        resource_type="analysis",
        resource_id=dataset,
        creator_principal_id=actor.principal_id,
        owner_type="principal",
        owner_id=actor.principal_id,
        allowed_actions=("view_snapshot", "run", "edit"),
        required_row_scope_refs=("unimplemented:row",),
        required_column_policy_refs=("restricted:column",),
        requires_pii=False,
        effective_from=None,
    )
    req("GET", f"{analytics_base}/datasets/{dataset}/context", expected=403)
    # Even an empty own-view list must resolve current dataset access.
    stranger_actor = identity.authenticate(stranger.access_token)
    organization.assign_primary(
        actor, principal_id=stranger_actor.principal_id, org_unit_id=department_id
    )
    organization.create_grant(
        actor,
        subject_type="principal",
        subject_id=stranger_actor.principal_id,
        target_org_unit_id=department_id,
        resource_type="report",
        resource_id=UUID(report),
        actions=("view_snapshot",),
        reason="S03 empty view list",
        effective_from=None,
        expires_at=None,
    )
    req(
        "GET",
        base + "/saved-views",
        using={"Authorization": f"Bearer {stranger.access_token}"},
        expected=403,
    )
    identity.revoke_session(actor, reader_tokens.session_id)
    for method, url, payload in report_routes + direct_routes:
        req(method, url, payload, using=reader_headers, expected=401)
    if evidence_path := os.environ.get("MS004_S03_EVIDENCE_PATH"):
        Path(evidence_path).write_text(
            json.dumps(
                {
                    "stage": "MS-004-S03",
                    "workspace_id": str(actor.workspace_id),
                    "semantic_dataset_version_id": str(dataset),
                    "legacy_result_id": result["result_id"],
                    "legacy_snapshot_id": old["snapshot_id"],
                    "configured_snapshot_id": adopted["snapshot_id"],
                    "report_revision_after_denied_commit": 5,
                    "lineage": direct["lineage"],
                    "result_manifest": direct["manifest"],
                    "comparison_manifest": comparison,
                    "http_status_counts": observed_statuses,
                    "boundary": "Disposable PostgreSQL, actual six-table intake, Identity sessions, ASGI API and immutable local artifacts; no browser or deployment proof.",
                },
                indent=2,
            )
            + "\n"
        )
