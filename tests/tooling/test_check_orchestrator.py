from __future__ import annotations

from pathlib import Path

import pytest

from tools.custometry_quality import check as orchestrator
from tools.custometry_quality.core import CheckResult


def passing(name: str) -> tuple[str, orchestrator.StaticCheck]:
    def checker(_root: Path) -> CheckResult:
        return CheckResult(name)

    return name, checker


def test_scope_composition_and_runtime_boundary(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    static_checks: list[tuple[str, orchestrator.StaticCheck]] = [passing("static")]
    ci_checks: list[tuple[str, orchestrator.StaticCheck]] = [
        passing("doctor-static"),
        passing("runtime-contract-static"),
    ]
    release_checks: list[tuple[str, orchestrator.StaticCheck]] = [passing("real-runtime")]
    monkeypatch.setattr(orchestrator, "_static_checks", lambda: static_checks)
    monkeypatch.setattr(
        orchestrator,
        "_ci_additional",
        lambda: ci_checks,
    )
    monkeypatch.setattr(orchestrator, "_release_checks", lambda: release_checks)

    pre_commit = orchestrator.check(tmp_path, "pre-commit")
    assert pre_commit.ok
    assert pre_commit.details["scope_contract"]["selected_checks"] == ["static"]
    assert pre_commit.details["scope_contract"]["runtime_observed"] is False
    assert pre_commit.details["outcomes"]["real-runtime"] == "not_observed"

    local = orchestrator.check(tmp_path, "local")
    assert local.details["scope_contract"]["selected_checks"] == ["static", "doctor-static"]

    ci = orchestrator.check(tmp_path, "ci")
    assert ci.details["scope_contract"]["selected_checks"] == [
        "static",
        "doctor-static",
        "runtime-contract-static",
    ]
    assert ci.details["scope_contract"]["runtime_observed"] is False
    assert ci.details["outcomes"]["real-runtime"] == "not_observed"

    release = orchestrator.check(tmp_path, "release")
    assert release.details["scope_contract"]["selected_checks"][-1] == "real-runtime"
    assert release.details["scope_contract"]["runtime_observed"] is True
    assert release.details["outcomes"]["real-runtime"] == "executed_passed"


def test_orchestrator_propagates_failed_observation(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    missing = CheckResult("missing", observed=False)
    missing.add("missing-input", "required artifact absent")
    def missing_check(_root: Path) -> CheckResult:
        return missing

    static_checks: list[tuple[str, orchestrator.StaticCheck]] = [("missing", missing_check)]
    empty: list[tuple[str, orchestrator.StaticCheck]] = []
    monkeypatch.setattr(orchestrator, "_static_checks", lambda: static_checks)
    monkeypatch.setattr(orchestrator, "_ci_additional", lambda: empty)
    monkeypatch.setattr(orchestrator, "_release_checks", lambda: empty)
    result = orchestrator.check(tmp_path, "ci")
    assert not result.ok
    assert not result.observed
