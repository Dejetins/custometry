from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID


RuleKind = Literal["not_null", "unique", "valid_datetime", "reference"]


@dataclass(frozen=True, slots=True)
class QualityRuleVersion:
    rule_id: str
    version: int
    entity: str
    kind: RuleKind
    fields: tuple[str, ...]
    reference_entity: str | None = None
    reference_field: str | None = None
    required: bool = True
    waivable: bool = False
    ignore_null: bool = False


@dataclass(frozen=True, slots=True)
class QualityWaiver:
    waiver_id: UUID
    workspace_id: UUID
    rule_id: str
    status: Literal["active", "revoked"]
    expires_at: datetime
    approved_by: UUID
    reason_code: str

    def applies(self, rule: QualityRuleVersion, *, now: datetime) -> bool:
        return (
            rule.waivable
            and self.rule_id == rule.rule_id
            and self.status == "active"
            and self.expires_at > now
        )


@dataclass(frozen=True, slots=True)
class QualityViolation:
    rule_id: str
    count: int
    sample_keys: tuple[str, ...]
    waived: bool


@dataclass(frozen=True, slots=True)
class QualityReport:
    report_id: UUID
    workspace_id: UUID
    batch_id: UUID
    decision: Literal["passed", "passed_with_waivers", "failed"]
    violations: tuple[QualityViolation, ...]
    applied_waiver_ids: tuple[UUID, ...]
    evaluated_at: datetime

    @property
    def allows_publication(self) -> bool:
        return self.decision in {"passed", "passed_with_waivers"}

    def as_dict(self) -> dict[str, object]:
        return {
            "report_id": str(self.report_id),
            "workspace_id": str(self.workspace_id),
            "batch_id": str(self.batch_id),
            "decision": self.decision,
            "violations": [
                {
                    "rule_id": violation.rule_id,
                    "count": violation.count,
                    "sample_keys": list(violation.sample_keys),
                    "waived": violation.waived,
                }
                for violation in self.violations
            ],
            "applied_waiver_ids": [str(item) for item in self.applied_waiver_ids],
            "evaluated_at": self.evaluated_at.isoformat(),
        }
