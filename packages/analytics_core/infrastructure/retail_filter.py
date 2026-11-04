"""Columnar confirmed membership into the receipt calculation; v1 stays unchanged."""

from __future__ import annotations
from typing import Any
from uuid import UUID
from packages.analytics_core.infrastructure.columnar_filters import DuckDBFlatFilter, pa, pc
from packages.analytics_core.infrastructure.relational_filters import DuckDBRelationalFilter
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import FlatFilterRequest
from packages.contracts.analytics.retail_filter import (
    ReceiptFilterInput,
    ReceiptFilterProjection,
    BoundedSalesInputPort,
    ReceiptSelectionEvidence,
)
from packages.contracts.analytics.retail_relational import receipt_relational_request
from packages.contracts.analytics.retail_aggregate import (
    AggregateReceiptFilterInput,
    receipt_aggregate_request,
)
from packages.contracts.analytics.receipt_selection import ReceiptSelection
from packages.contracts.analytics.receipt_cohorts import (
    CohortReceiptFilterInput,
    receipt_cohort_request,
)


class PublishedReceiptFilter:
    def __init__(
        self,
        engine: DuckDBFlatFilter,
        artifacts: BoundedSalesInputPort | None = None,
        relational: DuckDBRelationalFilter | None = None,
        aggregate: DuckDBRelationalFilter | None = None,
        cohort: DuckDBRelationalFilter | None = None,
    ):
        self.cohort = cohort
        self.engine, self.artifacts, self.relational, self.aggregate = (
            engine,
            artifacts,
            relational,
            aggregate,
        )

    @staticmethod
    def request(workspace: UUID, dataset: UUID, value: ReceiptFilterInput) -> FlatFilterRequest:
        return FlatFilterRequest(
            workspace_id=workspace,
            dataset_version_id=dataset,
            registry_version_id=value.registry_version_id,
            expression=value.expression,
        )

    def correlated(self) -> DuckDBRelationalFilter:
        if self.relational is None:
            raise AnalyticsFailure("FILTER_PROVIDER_UNAVAILABLE")
        return self.relational

    def aggregated(self) -> DuckDBRelationalFilter:
        if self.aggregate is None:
            raise AnalyticsFailure("FILTER_PROVIDER_UNAVAILABLE")
        return self.aggregate

    def cohorts(self) -> DuckDBRelationalFilter:
        if self.cohort is None:
            raise AnalyticsFailure("FILTER_PROVIDER_UNAVAILABLE")
        return self.cohort

    def fingerprint(
        self, workspace: UUID, actor: UUID, dataset: UUID, value: ReceiptSelection
    ) -> str:
        if isinstance(value, ReceiptFilterInput):
            return self.engine.fingerprint(self.request(workspace, dataset, value), actor_id=actor)
        if isinstance(value, CohortReceiptFilterInput):
            return self.cohorts().fingerprint(
                receipt_cohort_request(workspace, dataset, value), actor_id=actor
            )
        if isinstance(value, AggregateReceiptFilterInput):
            return self.aggregated().fingerprint(
                receipt_aggregate_request(workspace, dataset, value), actor_id=actor
            )
        return self.correlated().fingerprint(
            receipt_relational_request(workspace, dataset, value), actor_id=actor
        )

    def inputs(
        self,
        workspace: UUID,
        actor: UUID,
        dataset: UUID,
        value: ReceiptSelection,
        source: dict[str, Any],
        *,
        metadata_only: bool = False,
    ) -> dict[str, Any]:
        if self.artifacts is None:
            raise AnalyticsFailure("FILTER_PROVIDER_UNAVAILABLE")
        self.fingerprint(workspace, actor, dataset, value)
        engine = (
            self.engine
            if isinstance(value, ReceiptFilterInput)
            else self.cohorts()
            if isinstance(value, CohortReceiptFilterInput)
            else self.aggregated()
            if isinstance(value, AggregateReceiptFilterInput)
            else self.correlated()
        )
        grant = engine.access.authorize(
            workspace_id=workspace, actor_id=actor, dataset_version_id=dataset
        )
        inputs = self.artifacts.read_bounded_sales_inputs(
            workspace_id=workspace,
            bindings=source["bindings"],
            supporting_artifacts=[
                *source["summary"]["raw_artifacts"].values(),
                source["summary"]["quarantine_artifact"],
            ],
            policy=grant.resource_policy,
            metadata_only=metadata_only,
        )
        if (
            engine.access.authorize(
                workspace_id=workspace, actor_id=actor, dataset_version_id=dataset
            )
            != grant
        ):
            raise AnalyticsFailure("FILTER_POLICY_CHANGED")
        return inputs

    def project(
        self,
        workspace: UUID,
        actor: UUID,
        dataset: UUID,
        value: ReceiptSelection,
        inputs: dict[str, Any],
    ) -> ReceiptFilterProjection:
        selection = None
        if isinstance(value, ReceiptFilterInput):
            result = self.engine.execute(self.request(workspace, dataset, value), actor_id=actor)
        else:
            result = (
                self.cohorts().execute(
                    receipt_cohort_request(workspace, dataset, value), actor_id=actor
                )
                if isinstance(value, CohortReceiptFilterInput)
                else self.aggregated().execute(
                    receipt_aggregate_request(workspace, dataset, value), actor_id=actor
                )
                if isinstance(value, AggregateReceiptFilterInput)
                else self.correlated().execute(
                    receipt_relational_request(workspace, dataset, value), actor_id=actor
                )
            )
            selection = ReceiptSelectionEvidence(
                request_hash=result.request_hash,
                matched_count=len(result.matched_ids),
                not_matched_count=result.not_matched_count,
                unknown_count=result.unknown_count,
                authorized_count=result.authorized_count,
                limitation_codes=result.limitation_codes,
            )
        rows = inputs["Receipt"]
        if not rows:
            return ReceiptFilterProjection(inputs, None, selection)
        table = pa.Table.from_pylist(rows)
        selected = pc.is_in(
            table["receipt_id"], value_set=pa.array(result.matched_ids, type=pa.string())
        )
        as_of = (
            pc.max(table["receipt_datetime"]).as_py()
            if "receipt_datetime" in table.column_names
            else None
        )
        return ReceiptFilterProjection(
            {**inputs, "Receipt": table.filter(selected).to_pylist()}, as_of, selection
        )
