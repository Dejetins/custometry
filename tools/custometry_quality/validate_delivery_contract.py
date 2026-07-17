"""Validate Custometry's portable adapter to Global Delivery Contract v1."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .core import (
    CheckResult,
    add_common_arguments,
    main_guard,
    parse_frontmatter,
    render_result,
    require_file,
)


ADAPTER_PATH = Path(".codex/AGENTS.md")


def _require_text(
    path: Path,
    needle: str,
    code: str,
    message: str,
    result: CheckResult,
) -> None:
    if needle not in path.read_text(encoding="utf-8"):
        result.add(code, message, path)


def check(root: Path, contract_path: Path | None = None) -> CheckResult:
    """Check the repository adapter and optionally the installed global source.

    CI validates the portable repository-owned adapter. A local audit may pass
    ``contract_path`` to additionally resolve the installed global contract,
    its supplying skill, and the global agent router.
    """

    result = CheckResult("validate_delivery_contract")
    adapter = root / ADAPTER_PATH
    if not require_file(adapter, result, "delivery-contract-adapter-missing"):
        return result

    _require_text(
        adapter,
        "Global Delivery Contract v1",
        "delivery-contract-adapter-identity-invalid",
        "Custometry adapter must declare Global Delivery Contract v1",
        result,
    )
    _require_text(
        adapter,
        "delivery-orchestrator",
        "delivery-contract-adapter-routing-missing",
        "Custometry adapter must route artifact selection through delivery-orchestrator",
        result,
    )
    _require_text(
        adapter,
        "delivery-contract-v1.md",
        "delivery-contract-adapter-link-invalid",
        "Custometry adapter must name the canonical global contract file",
        result,
    )

    result.details["adapter"] = str(adapter)
    result.details["installed_contract_observed"] = contract_path is not None
    if contract_path is None:
        return result

    if not require_file(contract_path, result, "delivery-contract-global-missing"):
        return result

    contract_reference = contract_path.as_posix()
    _require_text(
        adapter,
        contract_reference,
        "delivery-contract-adapter-link-invalid",
        "Custometry adapter must link the selected installed Global Delivery Contract",
        result,
    )
    _require_text(
        contract_path,
        "# Global Delivery Contract v1",
        "delivery-contract-global-identity-invalid",
        "global contract must declare Global Delivery Contract v1",
        result,
    )
    _require_text(
        contract_path,
        "One ready ticket is one execution unit.",
        "delivery-contract-execution-unit-rule-missing",
        "global contract must preserve the one ready ticket / one execution unit rule",
        result,
    )

    skill_path = contract_path.parent.parent / "SKILL.md"
    if not require_file(skill_path, result, "delivery-contract-skill-missing"):
        return result
    try:
        skill_meta, _skill_body = parse_frontmatter(skill_path)
    except ValueError as exc:
        result.add("delivery-contract-skill-frontmatter-invalid", str(exc), skill_path)
        return result
    if skill_meta.get("name") != "delivery-orchestrator":
        result.add(
            "delivery-contract-skill-identity-invalid",
            "global contract must be supplied by the delivery-orchestrator skill",
            skill_path,
        )

    global_agent = contract_path.parents[3] / "AGENTS.md"
    if not require_file(global_agent, result, "delivery-contract-global-agent-missing"):
        return result
    _require_text(
        global_agent,
        contract_reference,
        "delivery-contract-global-agent-link-invalid",
        "global AGENTS.md must link the canonical delivery contract path",
        result,
    )
    _require_text(
        global_agent,
        "delivery-orchestrator",
        "delivery-contract-global-agent-routing-missing",
        "global AGENTS.md must route new delivery work through delivery-orchestrator",
        result,
    )
    result.details.update(contract=str(contract_path), skill=str(skill_path))
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the Custometry Global Delivery Contract adapter"
    )
    add_common_arguments(parser)
    parser.add_argument(
        "--contract",
        type=Path,
        help="optionally verify an installed Global Delivery Contract source",
    )
    args = parser.parse_args(argv)
    contract = args.contract.resolve() if args.contract else None
    return render_result(check(args.root.resolve(), contract), args.json)


if __name__ == "__main__":
    main_guard(cli)
