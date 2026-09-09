"""Bounded public operational status; no Identity or domain state."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ComponentState = Literal["ready", "not_ready"]
FailureCode = Literal["DATABASE_UNAVAILABLE", "SCHEMA_INCOMPATIBLE", "STORAGE_UNAVAILABLE"]


class InstallationComponents(BaseModel):
    model_config = ConfigDict(extra="forbid")

    database: ComponentState
    schema_state: ComponentState = Field(alias="schema")
    storage: ComponentState


class InstallationStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["custometry-installation-status/v1"] = (
        "custometry-installation-status/v1"
    )
    state: Literal["ready_for_bootstrap", "not_ready"]
    version: str = Field(min_length=1)
    components: InstallationComponents
    next_action: Literal["bootstrap_not_available"] = "bootstrap_not_available"
    code: FailureCode | None = None
