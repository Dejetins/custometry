from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ExecutionClaim:
    batch_id: UUID
    attempt_id: UUID
    fencing_token: int
