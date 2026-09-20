from copy import deepcopy
from pathlib import Path
from uuid import uuid4
from typing import Any
import pytest
from pydantic import ValidationError
from packages.contracts.generate_workspace_client import outputs
from packages.contracts.presentation.workspace import (
    ConfiguredReportV2,
    ReaderViewOverride,
    SingleSelection,
    copy_workset,
    creator_saved_view_id,
    legacy_instance_ids,
    parse_configuration,
    AnalyticalDocumentCompositionV2,
    WorkspaceApplyRequest,
)
from packages.contracts.semantic import BusinessCalendarProfile
from packages.semantic_model.application.sales_metrics import definitions

ROOT = Path(__file__).resolve().parents[3]


def definition() -> dict[str, Any]:
    owner, report, workset, card = [uuid4() for _ in range(4)]
    metric = definitions()[0]
    ref = {"id": str(uuid4()), "content_hash": "a" * 64}
    return dict(
        schema_version="configured-report/v2",
        report_id=str(report),
        creator_principal_id=str(owner),
        title="Report",
        semantic_dataset_version_id=str(uuid4()),
        common_context={"starts_on": "2025-01-01", "ends_on": "2025-12-31", "store_ids": None},
        grain="year",
        calendar_ref={"version_id": str(uuid4()), "content_hash": "a" * 64},
        calendar_basis="fiscal",
        worksets=[
            dict(
                workset_id=str(workset),
                name={"ru": "Набор", "en": "Set"},
                visibility="personal",
                owner_principal_id=str(owner),
                cards=[
                    dict(
                        card_id=str(card),
                        metric_ref={
                            k: metric[k] for k in ("metric_id", "version_id", "content_hash")
                        },
                        local_store_ids=None,
                    )
                ],
            )
        ],
        default_workset_id=str(workset),
        selection=dict(mode="single", card_id=str(card), temporal="none", display="series"),
        brand_profile=ref,
        company_pack=ref,
        base_snapshot_ref={
            "version_id": str(uuid4()),
            "snapshot_id": str(uuid4()),
            "manifest": {"artifact_id": str(uuid4()), "content_hash": "b" * 64},
        },
    )


def test_generated_schema_openapi_and_typescript_are_current() -> None:
    for path, content in outputs().items():
        assert (ROOT / path).read_bytes() == content, path


def test_copy_keeps_registry_but_remaps_every_instance_and_selection() -> None:
    value = ConfiguredReportV2.model_validate(definition())
    before = value.model_dump_json()
    copy, selection = copy_workset(value.worksets[0], value.selection)
    assert copy.workset_id != value.worksets[0].workset_id
    assert copy.cards[0].card_id != value.worksets[0].cards[0].card_id
    assert copy.cards[0].metric_ref == value.worksets[0].cards[0].metric_ref
    assert isinstance(selection, SingleSelection) and selection.card_id == copy.cards[0].card_id
    assert value.model_dump_json() == before
    assert legacy_instance_ids(value.report_id) == legacy_instance_ids(value.report_id)
    assert creator_saved_view_id(
        value.report_id, value.creator_principal_id
    ) == creator_saved_view_id(value.report_id, value.creator_principal_id)


def test_empty_and_inheritance_are_explicit() -> None:
    raw = definition()
    inherited = ConfiguredReportV2.model_validate(raw)
    raw["common_context"]["store_ids"] = []
    empty = ConfiguredReportV2.model_validate(raw)
    assert inherited.common_context.store_ids is None and empty.common_context.store_ids == []
    raw["common_context"]["store_ids"] = ["same"] * 1001
    assert ConfiguredReportV2.model_validate(raw).common_context.store_ids == ["same"]
    raw.update(worksets=[], default_workset_id=None, selection=None)
    value = ConfiguredReportV2.model_validate(raw)
    AnalyticalDocumentCompositionV2(
        composition_schema_version=2,
        analytical_document_version_id=uuid4(),
        analytical_document_id=value.report_id,
        workspace_id=uuid4(),
        profile="workbook_report",
        source_owner_ref={},
        navigation_mode="tabs",
        default_page_id=uuid4(),
        chapters=[],
        pages=[],
        sections=[],
        blocks=[],
        brand_profile_version_id=uuid4(),
        access_policy_id=uuid4(),
        filter_scope_bindings=[],
        definition=value,
        chart_specs=[],
        bindings_by_card=[],
    )


@pytest.mark.parametrize(
    "case",
    [
        "duplicate",
        "owner",
        "metric",
        "unsupported",
        "selection",
        "range",
        "worksets",
        "cards",
        "total",
        "stores",
        "field",
        "version",
    ],
)
def test_closed_configuration_and_resource_limits(case: str) -> None:
    raw = definition()
    card = raw["worksets"][0]["cards"][0]
    if case == "duplicate":
        raw["worksets"][0]["cards"].append(deepcopy(card))
    elif case == "owner":
        raw["worksets"][0]["owner_principal_id"] = str(uuid4())
    elif case == "metric":
        card["metric_ref"]["metric_id"] = "profit"
    elif case == "unsupported":
        card["population_binding"] = {"id": "x"}
    elif case == "selection":
        raw["selection"]["card_id"] = str(uuid4())
    elif case == "range":
        raw["common_context"]["ends_on"] = "2026-01-02"
    elif case == "worksets":
        raw["worksets"] *= 21
    elif case == "cards":
        raw["worksets"][0]["cards"] *= 51
    elif case == "total":
        raw["worksets"] = [
            {
                **deepcopy(raw["worksets"][0]),
                "workset_id": str(uuid4()),
                "cards": [{**card, "card_id": str(uuid4())} for _ in range(50)],
            }
            for _ in range(5)
        ]
    elif case == "stores":
        card["local_store_ids"] = [str(i) for i in range(1001)]
    elif case == "field":
        raw["javascript"] = "alert(1)"
    else:
        raw["schema_version"] = "configured-report/v3"
    with pytest.raises(ValidationError):
        ConfiguredReportV2.model_validate(raw)


def test_no_numeric_partial_save_and_no_reader_definition_override() -> None:
    raw = definition()
    value = ConfiguredReportV2.model_validate(raw)
    with pytest.raises(ValidationError, match="INCOMPLETE_CARD_BINDINGS"):
        AnalyticalDocumentCompositionV2(
            composition_schema_version=2,
            analytical_document_version_id=uuid4(),
            analytical_document_id=value.report_id,
            workspace_id=uuid4(),
            profile="workbook_report",
            source_owner_ref={},
            navigation_mode="tabs",
            default_page_id=uuid4(),
            chapters=[],
            pages=[],
            sections=[],
            blocks=[],
            brand_profile_version_id=uuid4(),
            access_policy_id=uuid4(),
            filter_scope_bindings=[],
            definition=value,
            chart_specs=[],
            bindings_by_card=[],
        )
    with pytest.raises(ValidationError):
        WorkspaceApplyRequest.model_validate(
            {
                "contract_version": "configured-report/v2",
                "mode": "reader",
                "base_revision": 1,
                "definition": raw,
            }
        )
    display = {
        "active_workset_id": None,
        "selection": None,
        "card_order": [],
        "hidden_card_ids": [],
        "representation": "table",
        "density": "compact",
    }
    with pytest.raises(ValidationError):
        ReaderViewOverride.model_validate(
            {
                "query_context": {
                    **raw["common_context"],
                    "grain": "day",
                    "calendar_basis": "fiscal",
                },
                "display": display,
            }
        )
    with pytest.raises(ValueError, match="configuration_bytes"):
        parse_configuration(b" " * (1024 * 1024 + 1))


@pytest.mark.parametrize(
    "field,value",
    [
        ("fiscal_year_start_month", 0),
        ("fiscal_year_start_month", 13),
        ("fiscal_year_start_month", True),
        ("fiscal_year_start_month", "4"),
        ("fiscal_year_start_day", 2),
        ("fiscal_year_start_day", True),
        ("kind", "4-4-5"),
        ("timezone", "Europe/Moscow"),
        ("week_start", "sunday"),
        ("year_label", "unknown"),
    ],
)
def test_unsupported_calendar_profiles_are_rejected(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        BusinessCalendarProfile.model_validate({field: value})


def legacy_fixture() -> dict[str, Any]:
    """A strict saved-v1 fixture, not runtime calculation/intake evidence."""
    import json
    from packages.presentation.domain.reports import composition, line_spec, versioned

    owner, workspace, report, version, snapshot = [uuid4() for _ in range(5)]
    metric_refs = definitions()
    manifest = {"artifact_id": str(uuid4()), "content_hash": "d" * 64}
    result = {
        "schema_version": "sales-report/v1",
        "result_id": str(uuid4()),
        "semantic_dataset_version_id": str(uuid4()),
        "manifest": manifest,
        "parameters": {
            "period": {"starts_on": "2025-01-01", "ends_on": "2025-11-30"},
            "store_id": None,
            "comparison": "none",
        },
        "metrics": metric_refs,
        "daily": [],
        "comparison": None,
        "policy_hash": "f" * 64,
        "mart": {"output_grain": ["date"]},
        "lineage": {
            "bindings": [
                {"entity": e}
                for e in ("Customer", "Product", "Receipt", "ReceiptItem", "Store", "Calendar")
            ],
            "relationship_policy": "fixture",
            "calendar_version_id": str(uuid4()),
        },
        "trust": {"quality_report_id": str(uuid4())},
    }
    brand = versioned(
        "brand_profile",
        json.loads(
            (ROOT / "packages/presentation/infrastructure/system-brand.v1.json").read_text()
        ),
    )
    refs = {
        "contract_version": "draft-report/v1",
        "brand_profile": brand,
        "chart_spec": versioned(
            "chart_spec", line_spec(result, workspace, owner, "2026-09-20T00:00:00Z")
        ),
        "company_pack": versioned(
            "company_pack",
            {
                "schema_version": "system-company-pack/v1",
                "name": "System",
                "brand_profile": brand["reference"],
                "metric_versions": metric_refs,
                "methodology_packs": [],
                "localization_catalogs": ["en", "ru"],
            },
        ),
    }
    return {
        "contract_version": "draft-report/v1",
        "lifecycle": "owned_draft_preview",
        "report_id": str(report),
        "revision": 1,
        "title": "Legacy",
        "version_id": str(version),
        "snapshot_id": str(snapshot),
        "author_principal_id": str(owner),
        "saved_at": "2026-09-20T00:00:00Z",
        "composition": composition(report, version, workspace, owner, "Legacy", result, refs),
        "snapshot": {},
        "page_snapshot": {},
        "result": result,
        "references": refs,
        "manifest": manifest,
    }


def test_new_reader_dispatch_and_legacy_projection_preserve_original_bytes() -> None:
    import json
    from packages.contracts.presentation import DraftResponse
    from packages.contracts.presentation.workspace import (
        VersionedReport,
        adapt_legacy_definition,
        ChartSpec,
        AnalyticalDocumentComposition,
    )
    from packages.contracts.semantic import CalendarRef
    from packages.semantic_model.application.calendar import initial_calendar_id
    from uuid import UUID

    raw = legacy_fixture()
    original = json.dumps(raw, sort_keys=True)
    parsed = VersionedReport.model_validate(raw).root
    assert isinstance(parsed, DraftResponse)
    pin = CalendarRef(
        version_id=initial_calendar_id(UUID(raw["composition"]["workspace_id"])),
        content_hash="a" * 64,
    )
    adapted = adapt_legacy_definition(parsed, pin)
    again = adapt_legacy_definition(parsed, pin)
    assert adapted == again and adapted.calendar_basis == "calendar" and adapted.grain == "day"
    assert len(adapted.worksets) == 1 and len(adapted.worksets[0].cards) == 3
    assert adapted.base_snapshot_ref.snapshot_id == parsed.snapshot_id
    assert adapted.worksets[0].cards[0].metric_ref.version_id == UUID(
        definitions()[0]["version_id"]
    )
    assert json.dumps(raw, sort_keys=True) == original
    assert parsed.model_dump(mode="json")["result"] == raw["result"]
    assert (
        ChartSpec.model_validate(raw["references"]["chart_spec"]["payload"]).root.schema_version
        == "1.0.0"
    )
    assert (
        AnalyticalDocumentComposition.model_validate(
            raw["composition"]
        ).root.composition_schema_version
        == 1
    )
    invalid = deepcopy(raw)
    invalid["contract_version"] = "configured-report/v99"
    with pytest.raises(ValidationError):
        VersionedReport.model_validate(invalid)


def test_dual_reader_accepts_v2_without_relaxing_legacy_request() -> None:
    from packages.contracts.presentation.workspace import VersionedReport, WorkspaceReportResponse
    from packages.contracts.presentation import SaveRequest

    raw = definition()
    raw.update(worksets=[], default_workset_id=None, selection=None)
    report_id = raw["report_id"]
    version_id = uuid4()
    page_id = uuid4()
    response = {
        "contract_version": "configured-report/v2",
        "report_id": report_id,
        "revision": 2,
        "version_id": str(version_id),
        "snapshot_id": str(uuid4()),
        "author_principal_id": raw["creator_principal_id"],
        "saved_at": "2026-09-20T00:00:00Z",
        "composition": {
            "composition_schema_version": 2,
            "analytical_document_version_id": str(version_id),
            "analytical_document_id": report_id,
            "workspace_id": str(uuid4()),
            "profile": "workbook_report",
            "source_owner_ref": {"context": "presentation"},
            "navigation_mode": "tabs",
            "default_page_id": str(page_id),
            "chapters": [],
            "pages": [],
            "sections": [],
            "blocks": [],
            "brand_profile_version_id": str(uuid4()),
            "access_policy_id": str(uuid4()),
            "filter_scope_bindings": [],
            "definition": raw,
            "chart_specs": [],
            "bindings_by_card": [],
        },
        "saved_view": {"id": str(uuid4()), "content_hash": "a" * 64},
        "manifest": {"artifact_id": str(uuid4()), "content_hash": "b" * 64},
        "page_manifests": [],
        "capabilities": {
            "definition_edit": True,
            "view_apply": True,
            "saved_view_save": True,
            "exact_preview": True,
        },
    }
    assert isinstance(VersionedReport.model_validate(response).root, WorkspaceReportResponse)
    with pytest.raises(ValidationError):
        SaveRequest.model_validate(
            {
                "contract_version": "configured-report/v2",
                "result_id": str(uuid4()),
                "title": "Legacy cannot change version",
                "expected_revision": 1,
                "idempotency_key": str(uuid4()),
                "chart_spec": raw["brand_profile"],
                "brand_profile": raw["brand_profile"],
                "company_pack": raw["company_pack"],
            }
        )
