"""Canonical bounded composition and renderer-neutral line specification."""

from __future__ import annotations

import hashlib
import json
from typing import Any
from uuid import UUID, uuid5
from packages.contracts.presentation import PresentationFailure

NAMESPACE = UUID("77421eb4-af82-40ae-9724-14dd19a571c1")


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode()
    ).hexdigest()


def versioned(kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    identity = str(uuid5(NAMESPACE, kind + digest(payload)))
    id_field = {
        "chart_spec": "chart_spec_id",
        "brand_profile": "brand_profile_version_id",
        "company_pack": "company_pack_version_id",
    }[kind]
    payload = {**payload, id_field: identity}
    content_hash = digest(payload)
    return {
        "kind": kind,
        "reference": {"id": identity, "content_hash": content_hash},
        "payload": payload,
    }


def validate_result(result: dict[str, Any]) -> None:
    try:
        complete = (
            result["schema_version"] == "sales-report/v1"
            and {b["entity"] for b in result["lineage"]["bindings"]}
            == {"Customer", "Product", "Receipt", "ReceiptItem", "Store", "Calendar"}
            and len(result["lineage"]["bindings"]) == 6
            and bool(result["trust"]["quality_report_id"])
            and bool(result["lineage"]["relationship_policy"])
            and bool(result["lineage"]["calendar_version_id"])
            and bool(result["policy_hash"] and result["manifest"]["content_hash"])
            and [m["metric_id"] for m in result["metrics"]]
            == ["net_revenue", "receipt_count", "average_receipt"]
            and all(
                m["version_id"] and m["content_hash"] and m["unit"] and m["format"]
                for m in result["metrics"]
            )
            and result["mart"]["output_grain"] == ["date"]
        )
        if not complete:
            raise PresentationFailure("INCOMPLETE_RESULT_BINDING")
    except (KeyError, TypeError) as exc:
        raise PresentationFailure("INCOMPLETE_RESULT_BINDING") from exc


def line_spec(
    result: dict[str, Any], workspace: UUID, owner: UUID, created_at: str
) -> dict[str, Any]:
    validate_result(result)
    manifest = result["manifest"]
    metric = result["metrics"][0]
    return {
        "schema_version": "1.0.0",
        "created_at": created_at,
        "chart_type": "line",
        "workspace_id": str(workspace),
        "title_key": "analytics.net_revenue",
        "title_override": None,
        "description_key": None,
        "source_binding": {
            "source_artifact_id": manifest["artifact_id"],
            "source_artifact_hash": manifest["content_hash"],
            "projection": {"current": "daily", "comparison": "comparison.daily"},
            "normalized_filter_expression": result["parameters"],
            "comparison_artifact_id": manifest["artifact_id"] if result["comparison"] else None,
        },
        "chart_data": {
            "data_artifact_id": manifest["artifact_id"],
            "schema_id": "sales-report",
            "schema_version": 1,
            "grain": "date",
            "row_count": len(result["daily"]),
            "column_count": 5,
            "deterministic_reduction": "none",
            "reduction_policy_hash": None,
        },
        "dimensions": [{"field": "date", "type": "date", "timezone": "UTC"}],
        "measures": [
            {
                "field": "net_revenue",
                "metric_version_id": metric["version_id"],
                "metric_content_hash": metric["content_hash"],
                "unit": metric["unit"],
                "number_format": metric["format"],
            }
        ],
        "axes": [
            {"id": "date", "dimension": "date"},
            {"id": "value", "measure": "net_revenue", "unit": "EUR"},
        ],
        "series": [
            {
                "id": "current",
                "projection": "daily",
                "x": "date",
                "y": "net_revenue",
                "color_role": "series-primary",
            },
            *(
                [
                    {
                        "id": "comparison",
                        "projection": "comparison.daily",
                        "x": "date",
                        "y": "net_revenue",
                        "color_role": "series-comparison",
                        "alignment": "same_dates_previous_year",
                    }
                ]
                if result["comparison"]
                else []
            ),
        ],
        "annotations": [],
        "range_timeline": None,
        "interaction": {
            "zoom": False,
            "pan": False,
            "brush": False,
            "tooltip": True,
            "legend_filter": False,
            "drilldown_action_id": None,
        },
        "visual_semantics": {
            "semantic_color_roles": ["series-primary", "series-comparison"],
            "current_period_style": {"line": "solid"},
            "comparison_period_style": {"line": "dashed"},
            "forecast_style": None,
            "interval_style": None,
            "promotion_style": None,
        },
        "accessibility": {
            "summary_key": "analytics.net_revenue",
            "summary_params": {},
            "table_alternative": "required",
            "series_descriptions": ["current", "comparison"],
        },
        "export_policy": {
            "email": "png_from_ssr_svg",
            "xlsx": "native_when_lossless_else_same_png_pipeline",
            "allow_raster_fallback": False,
        },
        "access_policy": {"owner_principal_id": str(owner), "policy_hash": result["policy_hash"]},
    }


def composition(
    report: UUID,
    version: UUID,
    workspace: UUID,
    owner: UUID,
    title: str,
    result: dict[str, Any],
    refs: dict[str, Any],
) -> dict[str, Any]:
    def node(name: str) -> str:
        return str(uuid5(report, name))

    binding = {
        "context": "analytics_core",
        "contract_version": result["schema_version"],
        "result_id": result["result_id"],
        "source_artifact": result["manifest"],
        "effective_filter_hash": digest(result["parameters"]),
        "metric_version_ids": [m["version_id"] for m in result["metrics"]],
        "schema": result["schema_version"],
        "grain": result["mart"]["output_grain"],
        "row_count": len(result["daily"]),
        "pii_class": "internal",
        "units_formats": [
            {k: m[k] for k in ("version_id", "unit", "format")} for m in result["metrics"]
        ],
    }
    blocks = [
        {
            "block_id": node(kind),
            "section_id": node("section"),
            "order": order,
            "block_type": kind,
            "source_binding": {**binding, "projection": projection},
            "content_binding": None,
            "presentation": {"chart_spec": refs["chart_spec"]["reference"]}
            if kind == "chart"
            else {},
        }
        for order, (kind, projection) in enumerate(
            [
                ("metric_group", "totals"),
                ("chart", "daily"),
                ("table", "daily"),
                ("result_trust", "trust"),
            ]
        )
    ]
    return {
        "analytical_document_version_id": str(version),
        "analytical_document_id": str(report),
        "workspace_id": str(workspace),
        "profile": "workbook_report",
        "composition_schema_version": 1,
        "source_owner_ref": {
            "context": "presentation",
            "resource_type": "draft_report",
            "resource_version_id": str(version),
        },
        "navigation_mode": "tabs",
        "default_page_id": node("page"),
        "chapters": [],
        "pages": [
            {
                "page_id": node("page"),
                "chapter_id": None,
                "order": 0,
                "title": {"en": title, "ru": title},
                "visibility": "visible",
                "layout_mode": "flow",
            }
        ],
        "sections": [
            {
                "section_id": node("section"),
                "page_id": node("page"),
                "parent_section_id": None,
                "order": 0,
                "title": None,
            }
        ],
        "blocks": blocks,
        "brand_profile_version_id": refs["brand_profile"]["reference"]["id"],
        "access_policy_id": node("owned-policy"),
        "filter_scope_bindings": [
            {
                "scope": "document",
                "scope_resource_id": str(report),
                "expression": result["parameters"],
                "combine_mode": "intersect",
                "linked_target_block_ids": [b["block_id"] for b in blocks],
                "precedence": ["security", "system_locked", "source_metric", "document"],
                "policy_hash": result["policy_hash"],
                "owner_principal_id": str(owner),
            }
        ],
    }
