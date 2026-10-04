"""V2 orchestration with mandatory provider-resolved current access; not mounted in S02."""

from __future__ import annotations
from typing import Any, Literal
from uuid import UUID
from packages.analytics_core.application.workspace_calculation import (
    build_workspace,
    normalize,
    digest,
    delta,
)
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.sales_report import SalesSemanticPort, SalesResultPort
from packages.contracts.analytics.workspace import (
    WorkspaceAccess,
    WorkspaceAccessPort,
    WorkspaceArtifactPort,
    WorkspaceRunRequest,
    WorkspaceResultV2,
    WorkspaceCardRequest,
    WorkspaceApplyResult,
    CardResultBinding,
    CardComparisonV1,
)
from packages.contracts.semantic import WorkspaceCalendarPort

UNITS = {"net_revenue": "EUR", "receipt_count": "receipt", "average_receipt": "EUR/receipt"}


class WorkspaceAnalyticsService:
    def __init__(
        self,
        *,
        semantics: SalesSemanticPort,
        results: SalesResultPort,
        artifacts: WorkspaceArtifactPort,
        calendars: WorkspaceCalendarPort,
        access: WorkspaceAccessPort,
    ):
        self.semantics, self.results, self.artifacts = semantics, results, artifacts
        self.calendars, self.access = calendars, access

    def resolve_access(
        self,
        workspace_id: UUID,
        principal_id: UUID,
        dataset_id: UUID,
        action: Literal["read", "run"],
    ) -> WorkspaceAccess:
        access = self.access.resolve(
            workspace_id=workspace_id,
            principal_id=principal_id,
            dataset_id=dataset_id,
            action=action,
        )
        required = {"analysis.read", "analysis.run"} if action == "run" else {"analysis.read"}
        if (access.workspace_id, access.principal_id, access.semantic_dataset_version_id) != (
            workspace_id,
            principal_id,
            dataset_id,
        ) or not required <= access.permissions:
            raise AnalyticsFailure("FORBIDDEN")
        return access

    def recheck_access(self, old: WorkspaceAccess, action: Literal["read", "run"]) -> None:
        if (
            self.resolve_access(
                old.workspace_id, old.principal_id, old.semantic_dataset_version_id, action
            )
            != old
        ):
            raise AnalyticsFailure("FORBIDDEN")

    def verified_inputs(self, access: WorkspaceAccess) -> tuple[dict[str, Any], dict[str, Any]]:
        source = self.semantics.sales_projection(
            workspace_id=access.workspace_id, version_id=access.semantic_dataset_version_id
        )
        inputs = self.artifacts.read_sales_inputs(
            workspace_id=access.workspace_id,
            bindings=source["bindings"],
            supporting_artifacts=[
                *source["summary"]["raw_artifacts"].values(),
                source["summary"]["quarantine_artifact"],
            ],
        )
        return source, inputs

    def context(
        self, *, workspace_id: UUID, principal_id: UUID, dataset_id: UUID
    ) -> dict[str, Any]:
        access = self.resolve_access(workspace_id, principal_id, dataset_id, "read")
        source, inputs = self.verified_inputs(access)
        stores = [
            {"id": str(s["store_id"]), "label": str(s.get("store_name") or s["store_id"])}
            for s in inputs["Store"]
            if str(s["store_id"]) in access.allowed_store_ids
        ]
        self.recheck_access(access, "read")
        return {
            "schema_version": "workspace-context/v2",
            "semantic_dataset_version_id": str(dataset_id),
            "stores": stores,
            "metrics": source["metrics"],
            "policy_hash": access.policy_hash,
        }

    def run(
        self, *, workspace_id: UUID, principal_id: UUID, request: WorkspaceRunRequest
    ) -> WorkspaceResultV2:
        access = self.resolve_access(
            workspace_id, principal_id, request.semantic_dataset_version_id, "run"
        )
        source, inputs = self.verified_inputs(access)
        calendar = self.calendars.get_version(request.calendar_ref, access)
        _, request_hash = normalize(request, source, inputs, access, calendar)
        existing = self.results.find_sales(
            workspace_id=workspace_id, principal_id=principal_id, request_hash=request_hash
        )
        if existing is None:
            payload = build_workspace(request, source, inputs, access, calendar)
            self.recheck_access(access, "run")
            payload["manifest"] = self.artifacts.commit_workspace(
                workspace_id=workspace_id, payload=payload, bindings=source["bindings"]
            )
            WorkspaceResultV2.model_validate(payload)
            existing = self.results.save_sales(
                payload, workspace_id=workspace_id, principal_id=principal_id
            )
        self.artifacts.verify_workspace(workspace_id=workspace_id, payload=existing)
        self.recheck_access(access, "run")
        return WorkspaceResultV2.model_validate(existing)

    def get(
        self, *, workspace_id: UUID, principal_id: UUID, dataset_id: UUID, result_id: UUID
    ) -> WorkspaceResultV2:
        access = self.resolve_access(workspace_id, principal_id, dataset_id, "read")
        payload = self.results.get_sales(
            workspace_id=workspace_id, principal_id=principal_id, result_id=result_id
        )
        result = WorkspaceResultV2.model_validate(payload)
        if (
            result.semantic_dataset_version_id != dataset_id
            or result.policy_hash != access.policy_hash
            or not set(result.effective_context.store_ids) <= set(access.allowed_store_ids)
        ):
            raise AnalyticsFailure("FORBIDDEN")
        # Verify admitted input integrity as well as the immutable output.
        source, _ = self.verified_inputs(access)
        if result.publication_hash != source["publication_hash"]:
            raise AnalyticsFailure("ARTIFACT_BINDING_MISMATCH")
        self.calendars.get_version(result.effective_context.calendar_ref, access)
        self.artifacts.verify_workspace(workspace_id=workspace_id, payload=payload)
        self.recheck_access(access, "read")
        return result

    def apply(
        self, *, workspace_id: UUID, principal_id: UUID, cards: list[WorkspaceCardRequest]
    ) -> WorkspaceApplyResult:
        if len(cards) > 200 or len({c.card_id for c in cards}) != len(cards):
            raise AnalyticsFailure("WORKSPACE_LIMIT_EXCEEDED")
        # Normalize once per source/policy; group equivalent local inheritance before computing.
        loaded: dict[UUID, tuple[WorkspaceAccess, dict[str, Any], dict[str, Any]]] = {}
        results: dict[str, WorkspaceResultV2] = {}
        bindings: list[CardResultBinding] = []
        for card in cards:
            request = card.query
            if card.metric_ref not in request.metric_refs:
                raise AnalyticsFailure("METRIC_BASIS_MISMATCH")
            dataset = request.semantic_dataset_version_id
            if dataset not in loaded:
                a = self.resolve_access(workspace_id, principal_id, dataset, "run")
                source, inputs = self.verified_inputs(a)
                loaded[dataset] = a, source, inputs
            a, source, inputs = loaded[dataset]
            calendar = self.calendars.get_version(request.calendar_ref, a)
            _, key = normalize(request, source, inputs, a, calendar)
            if key not in results:
                results[key] = self.run(
                    workspace_id=workspace_id, principal_id=principal_id, request=request
                )
            result = results[key]
            bindings.append(
                CardResultBinding.model_validate(
                    {
                        "card_id": card.card_id,
                        "metric_ref": card.metric_ref,
                        "result": {
                            "result_id": result.result_id,
                            "schema_version": result.schema_version,
                            "manifest": result.manifest,
                        },
                        "effective_context_hash": digest(
                            result.effective_context.model_dump(mode="json")
                        ),
                        "configuration_hash": card.configuration_hash,
                        "bucket_projection": card.metric_ref.metric_id,
                        "unit": UNITS[card.metric_ref.metric_id],
                        "format": {
                            "decimal_places": 0
                            if card.metric_ref.metric_id == "receipt_count"
                            else 2
                        },
                        "readiness": result.trust.status,
                    }
                )
            )
        for a, _, _ in loaded.values():
            self.recheck_access(a, "run")
        return WorkspaceApplyResult(results=list(results.values()), bindings=bindings)

    def compare(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        dataset_id: UUID,
        left: CardResultBinding,
        right: CardResultBinding | None = None,
    ) -> CardComparisonV1:
        left_result = self.get(
            workspace_id=workspace_id,
            principal_id=principal_id,
            dataset_id=dataset_id,
            result_id=left.result.result_id,
        )
        right_result = (
            left_result
            if right is None
            else self.get(
                workspace_id=workspace_id,
                principal_id=principal_id,
                dataset_id=dataset_id,
                result_id=right.result.result_id,
            )
        )

        def side(binding: CardResultBinding, result: WorkspaceResultV2) -> dict[str, Any]:
            if (
                binding.metric_ref not in result.metric_refs
                or binding.bucket_projection != binding.metric_ref.metric_id
                or binding.unit != UNITS[binding.metric_ref.metric_id]
                or binding.format.decimal_places
                != (0 if binding.metric_ref.metric_id == "receipt_count" else 2)
                or binding.result.manifest != result.manifest
                or binding.effective_context_hash
                != digest(result.effective_context.model_dump(mode="json"))
            ):
                raise AnalyticsFailure("RESULT_BINDING_MISMATCH")
            return {
                "card_id": str(binding.card_id),
                "metric_ref": binding.metric_ref.model_dump(mode="json"),
                "result": binding.result.model_dump(mode="json"),
                "unit": binding.unit,
                "format": binding.format.model_dump(mode="json"),
                "context": result.effective_context.model_dump(mode="json"),
                "baseline_dates": None,
            }

        ls, rs = side(left, left_result), side(right or left, right_result)
        reasons: list[str] = []
        lc, rc = left_result.effective_context, right_result.effective_context
        if (lc.starts_on, lc.ends_on) != (rc.starts_on, rc.ends_on):
            reasons.append("PERIOD_MISMATCH")
        if lc.grain != rc.grain:
            reasons.append("GRAIN_MISMATCH")
        if (lc.calendar_ref, lc.calendar_basis) != (rc.calendar_ref, rc.calendar_basis):
            reasons.append("CALENDAR_MISMATCH")
        if left_result.publication_hash != right_result.publication_hash or (
            left.metric_ref.metric_id == (right or left).metric_ref.metric_id
            and left.metric_ref != (right or left).metric_ref
        ):
            reasons.append("METRIC_BASIS_MISMATCH")
        different_units = ls["unit"] != rs["unit"]
        codes = reasons + (["UNIT_MISMATCH"] if different_units else [])
        lm, rm = left.metric_ref.metric_id, (right or left).metric_ref.metric_id
        buckets: list[dict[str, Any]] = []
        if right is None:
            if left_result.temporal is None:
                raise AnalyticsFailure("COMPARISON_DISABLED")
            rs["baseline_dates"] = [str(d) for d in left_result.temporal.baseline_dates]
            for b in left_result.temporal.buckets:
                buckets.append({"bucket_id": b.bucket_id, **b.changes[lm].model_dump(mode="json")})
            total = left_result.temporal.changes[lm].model_dump(mode="json")
            cov = left_result.temporal.coverage.model_dump(mode="json")
        else:
            total = delta(
                getattr(left_result.totals, lm),
                getattr(right_result.totals, rm),
                left_result.coverage.model_dump(),
                right_result.coverage.model_dump(),
                codes,
            )
            cov = right_result.coverage.model_dump(mode="json")
            if not reasons:
                rb = {b.bucket_id: b for b in right_result.buckets}
                for b in left_result.buckets:
                    other = rb[b.bucket_id]
                    buckets.append(
                        {
                            "bucket_id": b.bucket_id,
                            **delta(
                                getattr(b.values, lm),
                                getattr(other.values, rm),
                                b.coverage.model_dump(),
                                other.coverage.model_dump(),
                                codes,
                            ),
                        }
                    )
        status = (
            "unavailable"
            if reasons
            else "descriptive"
            if different_units
            else "comparable"
            if total["absolute_delta"] is not None
            else "unavailable"
        )
        payload: dict[str, Any] = {
            "schema_version": "card-comparison/v1",
            "mode": "temporal" if right is None else "pair",
            "left": ls,
            "right": rs,
            "comparability_status": status,
            "buckets": buckets,
            "totals": total,
            "coverage": cov,
        }
        access = self.resolve_access(workspace_id, principal_id, dataset_id, "read")
        if (
            access.policy_hash != left_result.policy_hash
            or access.policy_hash != right_result.policy_hash
        ):
            raise AnalyticsFailure("FORBIDDEN")
        payload["manifest"] = self.artifacts.commit_workspace(
            workspace_id=workspace_id,
            payload=payload,
            bindings=[
                left_result.manifest.model_dump(mode="json"),
                right_result.manifest.model_dump(mode="json"),
            ],
        )
        self.artifacts.verify_workspace(workspace_id=workspace_id, payload=payload)
        self.recheck_access(access, "read")
        return CardComparisonV1.model_validate(payload)

    def verify_query(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        request: WorkspaceRunRequest,
        result_id: UUID,
    ) -> WorkspaceResultV2:
        """Exact binding verification without computing or silently rebasing a saved result."""
        access = self.resolve_access(
            workspace_id, principal_id, request.semantic_dataset_version_id, "read"
        )
        source, inputs = self.verified_inputs(access)
        calendar = self.calendars.get_version(request.calendar_ref, access)
        _, expected = normalize(request, source, inputs, access, calendar)
        stored = self.results.get_sales(
            workspace_id=workspace_id, principal_id=principal_id, result_id=result_id
        )
        if stored.get("policy_hash") != access.policy_hash:
            raise AnalyticsFailure("ACCESS_CONTEXT_CHANGED")
        result = self.get(
            workspace_id=workspace_id,
            principal_id=principal_id,
            dataset_id=request.semantic_dataset_version_id,
            result_id=result_id,
        )
        if (
            result.request_hash != expected
            and request.alignment == "none"
            and result.effective_context.alignment == "previous_year_same_dates"
        ):
            # Display-only removal/pair selection can retain an already verified richer
            # artifact. Enabling absent temporal data still requires explicit compute.
            _, expected = normalize(
                request.model_copy(update={"alignment": "previous_year_same_dates"}),
                source,
                inputs,
                access,
                calendar,
            )
        if result.request_hash != expected:
            raise AnalyticsFailure("RESULT_BINDING_MISMATCH")
        self.recheck_access(access, "read")
        return result
