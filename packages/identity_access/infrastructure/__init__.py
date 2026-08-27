"""Infrastructure adapters for Identity and Workspace."""
from .contributor_postgres import (
    PostgresContributorAuthorization,
    PostgresContributorProjection,
)

__all__ = ["PostgresContributorAuthorization", "PostgresContributorProjection"]
