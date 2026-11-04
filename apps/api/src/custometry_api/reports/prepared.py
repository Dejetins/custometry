"""Prepared serving adapter: immutable output and admission metadata, not raw history.

The computation service remains unchanged. Only read/identity normalization paths
use the Store projection; retained result/artifact/calendar hashes and current
policy are still checked. Instances are strictly request scoped.
"""

from typing import Any, cast
from uuid import UUID
from pydantic import TypeAdapter
from packages.analytics_core.application.workspace_service import WorkspaceAnalyticsService
from packages.analytics_core.application.workspace_calculation import normalize
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.workspace import (
    WorkspaceAccess,
    WorkspaceRunRequest,
    WorkspaceResultV2,
)
from packages.analytics_core.application.snapshot_verification import SnapshotResultVerifier
from packages.artifacts.infrastructure.workspace import WorkspaceArtifactStore
from packages.artifacts.infrastructure.local import LocalArtifactStore

_accounted_json = TypeAdapter[Any](Any)


class RequestReadBudget:
    def __init__(self):
        self.entries = 0
        self.bytes = 0

    def admit(self, size: int) -> bool:
        if self.entries >= 64 or self.bytes + size > 16 * 1024 * 1024:
            return False
        self.entries += 1
        self.bytes += size
        return True


class RequestArtifactStore(WorkspaceArtifactStore):
    def __init__(self, *args: Any, budget: RequestReadBudget, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._manifests: dict[tuple[UUID, str], dict[str, Any]] = {}
        self._budget = budget

    @property
    def _local(self) -> LocalArtifactStore:
        # Reuse only this request's filesystem configuration, never file bytes
        # or verification outcomes. Every read still resolves and hashes its path.
        if not hasattr(self, '_request_local'):
            self._request_local = super()._local
        return self._request_local

    def _manifest(self, cursor: Any, workspace_id: UUID, artifact_id: str) -> dict[str, Any]:
        key = (workspace_id, artifact_id)
        if key in self._manifests:
            return dict(self._manifests[key])
        manifest = super()._manifest(cursor, workspace_id, artifact_id)
        size = len(_accounted_json.dump_json(manifest, fallback=str))
        if self._budget.admit(size):
            self._manifests[key] = dict(manifest)
        return manifest


class PreparedAnalyticsService(WorkspaceAnalyticsService):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._identity_memo: dict[tuple[UUID, UUID], tuple[dict[str, Any], dict[str, Any]]] = {}
        self._result_memo: dict[tuple[UUID, UUID, UUID, UUID], WorkspaceResultV2] = {}
        self._result_sizes: dict[int, int] = {}
        self._memo_bytes = 0

    def query_inputs(
        self, access: WorkspaceAccess, request: WorkspaceRunRequest, *, metadata_only: bool = False
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        # Scope preflight normalizes identities, not receipt values. Reuse the
        # same verified Store projection as saved-result verification. Compute
        # and receipt-filter providers keep their existing full/bounded paths.
        if metadata_only and request.receipt_filter is None:
            return self.identity_inputs(access)
        return super().query_inputs(access, request, metadata_only=metadata_only)

    def encoded_size(self, result: WorkspaceResultV2) -> int:
        size = self._result_sizes.get(id(result))
        return size if size is not None else len(result.model_dump_json().encode())

    def identity_inputs(self, access: WorkspaceAccess) -> tuple[dict[str, Any], dict[str, Any]]:
        key = (access.workspace_id, access.semantic_dataset_version_id)
        if key in self._identity_memo:
            return self._identity_memo[key]
        if len(self._identity_memo) >= 32:
            raise AnalyticsFailure("WORKSPACE_LIMIT_EXCEEDED")
        source = self.semantics.sales_projection(
            workspace_id=access.workspace_id, version_id=access.semantic_dataset_version_id
        )
        bindings = source["bindings"]
        entities = {b["entity"] for b in bindings}
        if entities != {"Customer", "Product", "Receipt", "ReceiptItem", "Store", "Calendar"}:
            raise AnalyticsFailure("SIX_ENTITY_BINDING_REQUIRED")
        stores = self.artifacts.read_sales_inputs(
            workspace_id=access.workspace_id,
            bindings=[b for b in bindings if b["entity"] == "Store"],
            supporting_artifacts=[],
        )
        # normalize() consumes Store identities and source metadata only. Empty
        # histories here cannot reach run/apply, which retain verified_inputs().
        value = (
            source,
            {entity: stores["Store"] if entity == "Store" else () for entity in entities},
        )
        self._identity_memo[key] = value
        return value

    def context(
        self, *, workspace_id: UUID, principal_id: UUID, dataset_id: UUID
    ) -> dict[str, Any]:
        access = self.resolve_access(workspace_id, principal_id, dataset_id, "read")
        source, inputs = self.identity_inputs(access)
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

    def get(
        self, *, workspace_id: UUID, principal_id: UUID, dataset_id: UUID, result_id: UUID
    ) -> WorkspaceResultV2:
        access = self.resolve_access(workspace_id, principal_id, dataset_id, "read")
        key = (workspace_id, principal_id, dataset_id, result_id)
        if key in self._result_memo:
            prior = self._result_memo[key]
            if prior.policy_hash != access.policy_hash or not set(
                prior.effective_context.store_ids
            ) <= set(access.allowed_store_ids):
                raise AnalyticsFailure("FORBIDDEN")
            return prior
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
        source, _ = self.identity_inputs(access)
        if result.publication_hash != source["publication_hash"]:
            raise AnalyticsFailure("ARTIFACT_BINDING_MISMATCH")
        self.calendars.get_version(result.effective_context.calendar_ref, access)
        self.artifacts.verify_workspace(workspace_id=workspace_id, payload=payload)
        self.recheck_access(access, "read")
        size = len(result.model_dump_json().encode())
        if len(self._result_memo) < 32 and self._memo_bytes + size <= 16 * 1024 * 1024:
            self._memo_bytes += size
            self._result_memo[key] = result
            self._result_sizes[id(result)] = size
        return result

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
        source, inputs = (self.query_inputs(access, request, metadata_only=True)
                          if request.receipt_filter is not None else self.identity_inputs(access))
        source, inputs = self.filter_context(access, request, source, inputs)
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
            and request.time_comparison is None
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


class PreparedSnapshotVerifier(SnapshotResultVerifier):
    def verify(
        self, *, workspace_id: UUID, principal_id: UUID, result_owner: UUID, stored: dict[str, Any]
    ) -> WorkspaceAccess:
        dataset = UUID(stored["semantic_dataset_version_id"])
        access = self.access(workspace_id, principal_id, dataset, result_owner)
        actual = self.results.get_sales(
            workspace_id=workspace_id,
            principal_id=result_owner,
            result_id=UUID(stored["result_id"]),
        )
        if actual != stored or actual["schema_version"] != "sales-report/v1":
            raise AnalyticsFailure("RESULT_BINDING_MISMATCH")
        _, inputs = cast(PreparedAnalyticsService, self.workspace).identity_inputs(access)
        store = actual["parameters"]["store_id"]
        scope = {str(s["store_id"]) for s in inputs["Store"]} if store is None else {store}
        if not scope <= set(access.allowed_store_ids):
            raise AnalyticsFailure("FORBIDDEN")
        self.artifacts.verify_sales(workspace_id=workspace_id, payload=actual)
        if self.access(workspace_id, principal_id, dataset, result_owner) != access:
            raise AnalyticsFailure("FORBIDDEN")
        return access


class RequestReadMemo:
    """A bounded memo for immutable repository reads inside one GET request."""

    def __init__(self, repository: Any, methods: frozenset[str], budget: RequestReadBudget | None = None):
        self.repository = repository
        self.methods = methods
        self.values: dict[tuple[Any, ...], Any] = {}
        self.budget = budget or RequestReadBudget()

    def __getattr__(self, name: str):
        method = getattr(self.repository, name)
        if name not in self.methods:
            return method

        def read(*args: Any, **kwargs: Any):
            import json

            # Reference arguments may be mappings; canonical strings avoid identity
            # collisions without retaining another copy of repository payloads.
            key = (name, json.dumps([args, kwargs], sort_keys=True, default=str))
            if key in self.values:
                return self.values[key]
            value = method(*args, **kwargs)
            size = len(_accounted_json.dump_json(value, fallback=str))
            if self.budget.admit(size):
                self.values[key] = value
            return value

        return read


class RequestWorkspaceReadMemo(RequestReadMemo):
    """Alias a current view pointer to the same verified immutable version."""

    def view(self, workspace: UUID, owner: UUID, view_id: UUID, version: UUID | None = None):
        if version is None:
            version = self.repository.latest_view_version(workspace, owner, view_id)
        return super().__getattr__('view')(workspace, owner, view_id, version)
