"""Fail-closed quality tooling for the Custometry repository.

Every command returns ``0`` only when the boundary it claims to inspect was
actually observed.  A missing required input is a validation failure, not a
skip.  Runtime-dependent commands expose explicit static/runtime modes so CI
can distinguish source validation from real-boundary evidence.
"""

from .core import CheckResult, Finding

__all__ = ["CheckResult", "Finding"]
