"""Typed receipt-filter evolution; v1 remains a supported unchanged reader branch."""

from packages.contracts.analytics.retail_filter import ReceiptFilterInput
from packages.contracts.analytics.retail_relational import RelationalReceiptFilterInput

from packages.contracts.analytics.retail_aggregate import AggregateReceiptFilterInput

from packages.contracts.analytics.receipt_cohorts import CohortReceiptFilterInput

ReceiptSelection = (
    ReceiptFilterInput
    | RelationalReceiptFilterInput
    | AggregateReceiptFilterInput
    | CohortReceiptFilterInput
)
