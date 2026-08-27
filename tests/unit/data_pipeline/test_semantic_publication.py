from uuid import uuid4

import pytest

from packages.contracts.data_pipeline import DataPipelineFailure
from packages.semantic_model import build_retail_publication


def arguments() -> dict[str, object]:
    entities = ("Customer", "Receipt", "ReceiptItem", "Product")
    return {
        "semantic_dataset_id": uuid4(),
        "workspace_id": uuid4(),
        "batch_id": uuid4(),
        "quality_report_id": uuid4(),
        "quality_decision": "passed",
        "artifact_ids": {entity: uuid4() for entity in entities},
        "artifact_hashes": {entity: str(index) * 64 for index, entity in enumerate(entities, 1)},
        "row_counts": {entity: index for index, entity in enumerate(entities, 1)},
        "violation_counts": {},
    }


def test_semantic_publication_pins_four_entities_and_impact() -> None:
    publication = build_retail_publication(**arguments())  # type: ignore[arg-type]
    assert publication.status == "published"
    assert [item.entity for item in publication.bindings] == [
        "Customer",
        "Receipt",
        "ReceiptItem",
        "Product",
    ]
    assert publication.capability_matrix == {
        "customer": "available",
        "receipts": "available",
        "basket": "available",
        "products": "available",
    }
    assert len(publication.request_hash) == 64


def test_semantic_publication_is_blocked_by_dq_and_incomplete_inputs() -> None:
    blocked = arguments()
    blocked["quality_decision"] = "failed"
    with pytest.raises(DataPipelineFailure, match="SEMANTIC_PUBLICATION_DQ_BLOCKED"):
        build_retail_publication(**blocked)  # type: ignore[arg-type]

    incomplete = arguments()
    incomplete["artifact_ids"] = {"Customer": uuid4()}
    with pytest.raises(DataPipelineFailure, match="SEMANTIC_PUBLICATION_INPUT_INCOMPLETE"):
        build_retail_publication(**incomplete)  # type: ignore[arg-type]


def test_waived_product_reference_degrades_declared_capabilities() -> None:
    values = arguments()
    values["quality_decision"] = "passed_with_waivers"
    values["violation_counts"] = {"receipt_item.product.reference": 5}
    publication = build_retail_publication(**values)  # type: ignore[arg-type]
    assert publication.capability_matrix["basket"] == "degraded"
    assert publication.impact_summary["product_reference_misses"] == 5
