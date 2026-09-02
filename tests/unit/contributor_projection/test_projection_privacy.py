from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import cast
from uuid import UUID, uuid4

from hypothesis import given, strategies as st
import pytest

from packages.contracts.people import (
    ActivityEventType,
    ContributorActivityBucket,
    ContributorCandidate,
    ContributorDomainEvent,
    PeopleFailure,
    PeopleViewVariant,
    ResourceType,
    ViewerContext,
)
from packages.identity_access.application.contributor_activity import (
    ContributorProjectionFailure,
    validate_redacted_event,
)
from packages.presentation.application.people import PeopleService


NOW = datetime(2026, 8, 27, 12, tzinfo=UTC)


def _profile_event(**overrides: object) -> ContributorDomainEvent:
    values: dict[str, object] = {
        "event_id": uuid4(),
        "workspace_id": uuid4(),
        "principal_id": uuid4(),
        "event_type": "profile.published",
        "occurred_at": NOW,
        "display_name": "Safe Contributor",
        "title": "Analytics Lead",
        "title_visible": True,
        "contribution_labels": ("maintainer",),
        "expertise_domains": ("sales",),
    }
    values.update(overrides)
    return ContributorDomainEvent(**values)  # type: ignore[arg-type]


def _activity_event(**overrides: object) -> ContributorDomainEvent:
    values: dict[str, object] = {
        "event_id": uuid4(),
        "workspace_id": uuid4(),
        "principal_id": uuid4(),
        "event_type": "resource.published",
        "occurred_at": NOW,
        "resource_type": "report",
        "resource_id": uuid4(),
        "safe_resource_title": "Visible report",
    }
    values.update(overrides)
    return ContributorDomainEvent(**values)  # type: ignore[arg-type]


def test_event_intake_is_allowlisted_and_has_no_raw_payload_shape() -> None:
    normalized = validate_redacted_event(_profile_event())
    assert not hasattr(normalized, "payload")
    assert not hasattr(normalized, "audit_event")

    with pytest.raises(ContributorProjectionFailure, match="allowlisted"):
        validate_redacted_event(
            _activity_event(event_type=cast(ActivityEventType, "audit.login.observed"))
        )
    with pytest.raises(ContributorProjectionFailure, match="unsafe"):
        validate_redacted_event(_activity_event(safe_resource_title="person@example.test"))
    with pytest.raises(ContributorProjectionFailure, match="profile fields"):
        validate_redacted_event(_activity_event(display_name="Raw actor"))
    with pytest.raises(ContributorProjectionFailure, match="cannot contain a resource"):
        validate_redacted_event(
            _profile_event(
                resource_type="report", resource_id=uuid4(), safe_resource_title="Hidden"
            )
        )


class MemoryProjection:
    def __init__(
        self,
        candidate: ContributorCandidate,
        buckets: tuple[ContributorActivityBucket, ...],
    ) -> None:
        self.candidate = candidate
        self.buckets = buckets

    def list_candidates(self, workspace_id: UUID) -> tuple[ContributorCandidate, ...]:
        return (self.candidate,) if workspace_id == WORKSPACE_ID else ()

    def activity_buckets(
        self, workspace_id: UUID, principal_id: UUID
    ) -> tuple[ContributorActivityBucket, ...]:
        if workspace_id != WORKSPACE_ID or principal_id != TARGET_ID:
            return ()
        return self.buckets


class MemoryAuthorization:
    def __init__(
        self, *, variant: PeopleViewVariant, visible_resource_ids: frozenset[UUID]
    ) -> None:
        self.variant: PeopleViewVariant = variant
        self.visible_resource_ids = visible_resource_ids

    def view_variant(
        self, viewer: ViewerContext, target_principal_id: UUID, *, at: datetime
    ) -> PeopleViewVariant:
        assert viewer.workspace_id == WORKSPACE_ID
        assert target_principal_id == TARGET_ID
        return self.variant

    def resource_visible(
        self,
        viewer: ViewerContext,
        *,
        target_org_unit_id: UUID,
        resource_type: ResourceType,
        resource_id: UUID,
    ) -> bool:
        assert target_org_unit_id == ORG_ID
        return resource_id in self.visible_resource_ids


WORKSPACE_ID = UUID("10000000-0000-0000-0000-000000000001")
TARGET_ID = UUID("20000000-0000-0000-0000-000000000001")
VIEWER_ID = UUID("20000000-0000-0000-0000-000000000002")
ORG_ID = UUID("30000000-0000-0000-0000-000000000001")
VISIBLE_ID = UUID("40000000-0000-0000-0000-000000000001")


def _candidate() -> ContributorCandidate:
    return ContributorCandidate(
        principal_id=TARGET_ID,
        display_name="Visible Creator",
        title="Research Lead",
        contribution_labels=("maintainer",),
        expertise_domains=("sales",),
        org_unit_id=ORG_ID,
        org_unit_name="Sales",
        projection_version="a" * 64,
        updated_at=NOW,
    )


def _bucket(resource_id: UUID, *, title: str, count: int) -> ContributorActivityBucket:
    return ContributorActivityBucket(
        principal_id=TARGET_ID,
        resource_type="report",
        resource_id=resource_id,
        safe_resource_title=title,
        activity_date=date(2026, 8, 26),
        created_count=0,
        published_count=count,
        materially_updated_count=0,
        maintained_count=0,
        coauthored_count=0,
        reviewed_count=0,
        resolved_count=0,
        last_activity_at=NOW - timedelta(days=1),
    )


@given(hidden_count=st.integers(min_value=0, max_value=25))
def test_hidden_resource_titles_and_counts_cannot_change_public_projection(
    hidden_count: int,
) -> None:
    hidden = tuple(
        _bucket(uuid4(), title=f"Hidden confidential {index}", count=100 + index)
        for index in range(hidden_count)
    )
    service = PeopleService(
        projection=MemoryProjection(
            _candidate(), (_bucket(VISIBLE_ID, title="Visible report", count=1), *hidden)
        ),
        authorization=MemoryAuthorization(
            variant="public", visible_resource_ids=frozenset({VISIBLE_ID})
        ),
    )
    viewer = ViewerContext(
        principal_id=VIEWER_ID,
        workspace_id=WORKSPACE_ID,
        permissions=frozenset({"organization.read", "report.read"}),
    )
    person = service.get_person(viewer, principal_id=TARGET_ID, at=NOW)

    assert person["view_variant"] == "public"
    assert person["activity"] is None
    assert person["visible_resource_count"] == 1
    assert person["visible_resources"] == [
        {
            "resource_type": "report",
            "resource_id": VISIBLE_ID,
            "title": "Visible report",
            "last_activity_at": NOW - timedelta(days=1),
        }
    ]
    serialized = repr(person).casefold()
    assert "hidden confidential" not in serialized
    assert "ranking" not in serialized
    assert "productivity" not in serialized
    assert "audit" not in serialized


@pytest.mark.parametrize("variant", ["self", "leader", "grantee"])
def test_extended_variants_share_events_but_keep_explicit_policy_reason(
    variant: PeopleViewVariant,
) -> None:
    service = PeopleService(
        projection=MemoryProjection(
            _candidate(), (_bucket(VISIBLE_ID, title="Visible report", count=2),)
        ),
        authorization=MemoryAuthorization(
            variant=variant, visible_resource_ids=frozenset({VISIBLE_ID})
        ),
    )
    viewer = ViewerContext(
        principal_id=TARGET_ID if variant == "self" else VIEWER_ID,
        workspace_id=WORKSPACE_ID,
        permissions=frozenset(
            {"organization.read", "organization.activity.read", "report.read"}
        ),
    )
    person = service.get_person(viewer, principal_id=TARGET_ID, at=NOW)

    assert person["view_variant"] == variant
    activity = cast(dict[str, object], person["activity"])
    windows = cast(list[dict[str, object]], activity["windows"])
    assert [window["window_days"] for window in windows] == [30, 90]
    assert [window["published_count"] for window in windows] == [2, 2]


def test_cross_workspace_candidates_are_not_loaded() -> None:
    service = PeopleService(
        projection=MemoryProjection(_candidate(), ()),
        authorization=MemoryAuthorization(variant="public", visible_resource_ids=frozenset()),
    )
    foreign = ViewerContext(
        principal_id=VIEWER_ID,
        workspace_id=uuid4(),
        permissions=frozenset({"organization.read"}),
    )
    with pytest.raises(PeopleFailure, match="NOT_FOUND"):
        service.get_person(foreign, principal_id=TARGET_ID, at=NOW)
