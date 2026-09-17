"""Save/reopen common document snapshots through public owner ports; never compute."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4, uuid5
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.presentation import (
    VERSION,
    LineChartSpecV1,
    DraftResponse,
    PresentationFailure,
    ReportRepository,
    ResultReader,
    SaveRequest,
    SnapshotArtifacts,
)
from packages.presentation.domain.reports import (
    composition,
    digest,
    line_spec,
    validate_result,
    versioned,
)


class ReportService:
    def __init__(
        self,
        repository: ReportRepository,
        results: ResultReader,
        artifacts: SnapshotArtifacts,
        system_brand: dict[str, Any],
    ):
        self._repository = repository
        self._results = results
        self._artifacts = artifacts
        self._system_brand = system_brand

    @staticmethod
    def _require(permissions: frozenset[str], *, write: bool = False) -> None:
        required = {"report.read", "analysis.read"}
        if write:
            required.add("report.manage")
        if not required <= permissions:
            raise PresentationFailure("FORBIDDEN")

    def _result(
        self, workspace_id: UUID, principal_id: UUID, permissions: frozenset[str], result_id: UUID
    ) -> dict[str, Any]:
        try:
            result = self._results.get_sales_report(
                workspace_id=workspace_id,
                principal_id=principal_id,
                permissions=permissions,
                result_id=result_id,
            )
        except AnalyticsFailure as exc:
            if exc.code == "ARTIFACT_UNAVAILABLE":
                code = (
                    "ARTIFACT_MISSING"
                    if isinstance(exc.__cause__, FileNotFoundError)
                    else "STORAGE_UNAVAILABLE"
                )
                raise PresentationFailure(code) from exc
            if exc.code == "ARTIFACT_INTEGRITY_FAILED":
                raise PresentationFailure("ARTIFACT_CORRUPT") from exc
            raise
        validate_result(result)
        return result

    def prepare(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        permissions: frozenset[str],
        result_id: UUID,
    ) -> dict[str, Any]:
        self._require(permissions, write=True)
        result = self._result(workspace_id, principal_id, permissions, result_id)
        brand = versioned("brand_profile", self._system_brand)
        company = versioned(
            "company_pack",
            {
                "schema_version": "system-company-pack/v1",
                "name": "Custometry system",
                "brand_profile": brand["reference"],
                "metric_versions": [
                    {k: m[k] for k in ("metric_id", "version_id", "content_hash", "unit", "format")}
                    for m in result["metrics"]
                ],
                "methodology_packs": [],
                "localization_catalogs": ["en", "ru"],
            },
        )
        chart = versioned(
            "chart_spec",
            line_spec(result, workspace_id, principal_id, datetime.now(UTC).isoformat()),
        )
        LineChartSpecV1.model_validate(chart["payload"])
        return {
            "contract_version": VERSION,
            **{
                v["kind"]: self._repository.put_reference(workspace_id, principal_id, v)
                for v in (chart, brand, company)
            },
        }

    def _resolve_refs(
        self, workspace: UUID, owner: UUID, request: SaveRequest, result: dict[str, Any]
    ) -> dict[str, Any]:
        refs: dict[str, Any] = {"contract_version": VERSION}
        for name in ("chart_spec", "brand_profile", "company_pack"):
            refs[name] = self._repository.get_reference(
                workspace, owner, getattr(request, name).model_dump(mode="json"), name
            )
        # Only the server-owned bounded canonical line subset is admitted.
        if refs["chart_spec"] != versioned(
            "chart_spec",
            line_spec(result, workspace, owner, refs["chart_spec"]["payload"]["created_at"]),
        ):
            raise PresentationFailure("INVALID_CHART_BINDING")
        pack = refs["company_pack"]["payload"]
        expected_metrics = [
            {k: m[k] for k in ("metric_id", "version_id", "content_hash", "unit", "format")}
            for m in result["metrics"]
        ]
        if (
            pack["brand_profile"] != refs["brand_profile"]["reference"]
            or pack["metric_versions"] != expected_metrics
        ):
            raise PresentationFailure("INVALID_DEFAULT_BINDING")
        return refs

    def save(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        permissions: frozenset[str],
        request: SaveRequest,
        report_id: UUID | None = None,
    ) -> dict[str, Any]:
        self._require(permissions, write=True)
        if report_id is None:
            if request.expected_revision != 0:
                raise PresentationFailure("REVISION_CONFLICT")
            report_id = uuid5(workspace_id, f"{principal_id}:{request.idempotency_key}")
        else:
            # Recheck access to the currently saved result before accepting a replacement.
            self.get(
                workspace_id=workspace_id,
                principal_id=principal_id,
                permissions=permissions,
                report_id=report_id,
            )
        result = self._result(workspace_id, principal_id, permissions, request.result_id)
        refs = self._resolve_refs(workspace_id, principal_id, request, result)
        request_hash = digest(request.model_dump(mode="json"))
        version_id, snapshot_id, page_snapshot_id = uuid4(), uuid4(), uuid4()
        comp = composition(
            report_id, version_id, workspace_id, principal_id, request.title, result, refs
        )
        page = {
            "analytical_page_snapshot_id": str(page_snapshot_id),
            "analytical_document_snapshot_id": str(snapshot_id),
            "page_id": comp["default_page_id"],
            "resolved_blocks": [
                {
                    "block_id": b["block_id"],
                    "source_artifact_id": result["manifest"]["artifact_id"],
                    "effective_filter_hash": digest(result["parameters"]),
                    "segment_binding": None,
                    "comparison_artifact_id": result["manifest"]["artifact_id"]
                    if result["comparison"]
                    else None,
                    "metric_version_ids": [m["version_id"] for m in result["metrics"]],
                    "chart_spec_id": refs["chart_spec"]["reference"]["id"]
                    if b["block_type"] == "chart"
                    else None,
                    "lineage_artifact_id": result["manifest"]["artifact_id"],
                    "readiness": "ready",
                }
                for b in comp["blocks"]
            ],
        }
        page_manifest = self._artifacts.commit(
            workspace_id=workspace_id,
            artifact_id=page_snapshot_id,
            payload=page,
            parents=[result["manifest"]],
        )
        root = {
            "analytical_document_snapshot_id": str(snapshot_id),
            "analytical_document_version_id": str(version_id),
            "page_snapshot_refs": [
                {
                    "page_id": comp["default_page_id"],
                    "analytical_page_snapshot_id": str(page_snapshot_id),
                    "manifest": page_manifest,
                }
            ],
            "resolved_document_context": {
                "result_id": result["result_id"],
                "parameters": result["parameters"],
                "metrics": result["metrics"],
                "lineage": result["lineage"],
                "trust": result["trust"],
                "policy_hash": result["policy_hash"],
                "timezone": "UTC",
                "currency": "EUR",
                "locale_policy": "viewer_en_or_ru",
                "brand_profile": refs["brand_profile"]["reference"],
                "company_pack": refs["company_pack"]["reference"],
                "renderer": "deferred_to_S04",
            },
            "manifest_artifact_id": str(snapshot_id),
        }
        payload = {
            "contract_version": VERSION,
            "lifecycle": "owned_draft_preview",
            "report_id": str(report_id),
            "revision": request.expected_revision + 1,
            "title": request.title,
            "version_id": str(version_id),
            "snapshot_id": str(snapshot_id),
            "author_principal_id": str(principal_id),
            "saved_at": datetime.now(UTC).isoformat(),
            "composition": comp,
            "snapshot": root,
            "page_snapshot": page,
            "result": result,
            "references": refs,
        }
        root_manifest = self._artifacts.commit(
            workspace_id=workspace_id,
            artifact_id=snapshot_id,
            payload=payload,
            parents=[page_manifest, result["manifest"]],
        )
        payload["manifest"] = root_manifest
        DraftResponse.model_validate(payload)
        saved = self._repository.save(
            workspace_id, principal_id, report_id, request_hash, request, payload
        )
        return self._verify(workspace_id, principal_id, permissions, saved)

    def _verify(
        self, workspace: UUID, owner: UUID, permissions: frozenset[str], saved: dict[str, Any]
    ) -> dict[str, Any]:
        try:
            DraftResponse.model_validate(saved)
            return self._verify_payload(workspace, owner, permissions, saved)
        except (KeyError, TypeError, ValueError) as exc:
            raise PresentationFailure("ARTIFACT_CORRUPT") from exc

    def _verify_payload(
        self, workspace: UUID, owner: UUID, permissions: frozenset[str], saved: dict[str, Any]
    ) -> dict[str, Any]:
        result = self._result(workspace, owner, permissions, UUID(saved["result"]["result_id"]))
        if result != saved["result"]:
            raise PresentationFailure("RESULT_BINDING_CORRUPT")
        for name in ("chart_spec", "brand_profile", "company_pack"):
            ref = saved["references"][name]
            if self._repository.get_reference(workspace, owner, ref["reference"], name) != ref:
                raise PresentationFailure("INVALID_REFERENCE")
        self._artifacts.verify(
            workspace_id=workspace,
            reference=saved["manifest"],
            payload={k: v for k, v in saved.items() if k != "manifest"},
        )
        page_ref = saved["snapshot"]["page_snapshot_refs"][0]["manifest"]
        self._artifacts.verify(
            workspace_id=workspace, reference=page_ref, payload=saved["page_snapshot"]
        )
        return saved

    def get(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        permissions: frozenset[str],
        report_id: UUID,
        snapshot_id: UUID | None = None,
    ) -> dict[str, Any]:
        self._require(permissions)
        saved = self._repository.latest(workspace_id, principal_id, report_id, snapshot_id)
        return self._verify(workspace_id, principal_id, permissions, saved)

    def list(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        permissions: frozenset[str],
        offset: int,
        limit: int,
    ) -> dict[str, Any]:
        self._require(permissions)
        visible: list[dict[str, Any]] = []
        for report_id in self._repository.candidates(workspace_id, principal_id):
            try:
                saved = self.get(
                    workspace_id=workspace_id,
                    principal_id=principal_id,
                    permissions=permissions,
                    report_id=report_id,
                )
            except (PresentationFailure, AnalyticsFailure) as exc:
                if exc.code in {"FORBIDDEN", "NOT_FOUND", "ARTIFACT_NOT_VISIBLE"}:
                    continue
                raise
            visible.append(
                {
                    k: saved[k]
                    for k in (
                        "report_id",
                        "revision",
                        "title",
                        "version_id",
                        "snapshot_id",
                        "saved_at",
                        "lifecycle",
                    )
                }
            )
        visible.sort(key=lambda r: (r["saved_at"], r["report_id"]), reverse=True)
        return {"reports": visible[offset : offset + limit], "visible_count": len(visible)}
