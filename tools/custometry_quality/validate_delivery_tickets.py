"""Validate ready-to-run vertical delivery tickets.

This protects only execution invariants that are hard to recover after an
execution unit starts. It does not prescribe a stage topology.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .core import (
    CheckResult,
    add_common_arguments,
    main_guard,
    parse_frontmatter,
    render_result,
    require_dir,
    require_file,
    stable_ids,
)


TICKET_ROOT = Path(".codex/delivery/tickets")
TICKET_ID = re.compile(r"[A-Z][A-Z0-9]{0,15}(?:-[A-Z0-9][A-Z0-9-]{0,47})+")
WORKSTREAM_ID = re.compile(r"(?:B\d{2}|W\d{2})")
STATUSES = {"draft", "ready", "active", "blocked", "accepted", "superseded"}
TERMINAL_STATUSES = {"accepted", "superseded"}
VALIDATION_DEPTHS = {"tests", "integration", "api", "browser", "runtime", "delivery"}
EVIDENCE_VERDICTS = {"passed", "superseded"}
BROWSER_PROOF_SKILL = "browser-qa-evidence"
CANONICAL_ESCALATIONS = (
    "normative_product_change",
    "material_user_scope_change",
    "external_or_irreversible_side_effect",
    "secrets_or_production_authority",
    "write_outside_allowed_scope",
)


@dataclass(frozen=True, slots=True)
class Ticket:
    identifier: str
    path: Path
    status: str
    blockers: tuple[str, ...]


def _strings(
    value: object,
    *,
    non_empty: bool = False,
    unique: bool = True,
) -> tuple[str, ...] | None:
    if not isinstance(value, list) or (non_empty and not value):
        return None
    if not all(isinstance(item, str) and item.strip() for item in value):
        return None
    items = tuple(value)
    return items if not unique or len(items) == len(set(items)) else None


def _repo_path(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value or value.startswith("/"):
        return None
    path = (root / value).resolve(strict=False)
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    return path


def _scope_paths(root: Path, value: object) -> tuple[str, ...] | None:
    paths = _strings(value, non_empty=True)
    if paths is None:
        return None
    for path in paths:
        if path.startswith("/") or ".." in Path(path).parts or path.startswith("./"):
            return None
        if not path.endswith("/**") and _repo_path(root, path) is None:
            return None
    return paths


def _proof_paths(root: Path, value: object) -> tuple[str, ...] | None:
    paths = _strings(value)
    if paths is None:
        return None
    return paths if all(_repo_path(root, path) is not None for path in paths) else None


def _add(result: CheckResult, code: str, message: str, path: Path) -> None:
    result.add(code, message, path)


def _non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_blocker_record(
    root: Path,
    value: object,
    result: CheckResult,
    path: Path,
) -> None:
    record = value if isinstance(value, dict) else None
    evidence = _proof_paths(root, record.get("evidence")) if record else None
    valid = (
        record is not None
        and _non_empty_string(record.get("technical_blocker"))
        and evidence is not None
        and bool(evidence)
        and all((root / item).is_file() for item in evidence)
        and _non_empty_string(record.get("next_safe_action"))
    )
    if not valid:
        _add(
            result,
            "delivery-ticket-blocked-record-invalid",
            "blocked ticket requires blocker_record with technical_blocker, existing evidence, and next_safe_action",
            path,
        )


def _validate_terminal_evidence(
    root: Path,
    path: Path,
    *,
    ticket_id: str,
    status: str,
    proof_boundary: object,
    proof_skills: tuple[str, ...] | None,
    result: CheckResult,
) -> None:
    try:
        meta, body = parse_frontmatter(path)
    except ValueError as exc:
        _add(result, "delivery-ticket-evidence-schema-invalid", str(exc), path)
        return

    expected_verdict = "passed" if status == "accepted" else "superseded"
    checks = _strings(meta.get("executed_checks"), non_empty=True, unique=False)
    observations = _strings(meta.get("observations"), non_empty=True, unique=False)
    evidence_skills = _strings(meta.get("proof_skills"))
    valid = (
        path.suffix == ".md"
        and meta.get("artifact_kind") == "delivery_evidence"
        and meta.get("delivery_contract") == "global/v1"
        and meta.get("delivery_schema_version") == 1
        and meta.get("ticket_id") == ticket_id
        and meta.get("proof_boundary") == proof_boundary
        and meta.get("verdict") in EVIDENCE_VERDICTS
        and meta.get("verdict") == expected_verdict
        and _non_empty_string(meta.get("redaction"))
        and checks is not None
        and observations is not None
        and evidence_skills is not None
        and proof_skills is not None
        and set(evidence_skills) == set(proof_skills)
        and "# Outcome and scope" in body
        and "# Commands and observations" in body
        and "# Verdict" in body
    )
    if not valid:
        _add(
            result,
            "delivery-ticket-evidence-schema-invalid",
            "terminal evidence must be a redacted Global Delivery Contract v1 record matching the ticket, boundary, proof skills, and terminal verdict",
            path,
        )


def _validate_ticket(
    root: Path,
    path: Path,
    known_requirements: frozenset[str],
    result: CheckResult,
) -> Ticket | None:
    try:
        meta, body = parse_frontmatter(path)
    except ValueError as exc:
        _add(result, "delivery-ticket-frontmatter-invalid", str(exc), path)
        return None

    identifier = meta.get("ticket_id")
    if (
        meta.get("artifact_kind") != "delivery_ticket"
        or meta.get("delivery_contract") != "global/v1"
        or meta.get("delivery_schema_version") != 1
        or not isinstance(identifier, str)
        or TICKET_ID.fullmatch(identifier) is None
        or path.stem != identifier
    ):
        _add(result, "delivery-ticket-identity-invalid", "ticket requires Global Delivery Contract v1, delivery_ticket/v1 frontmatter, and a filename matching ticket_id", path)
        return None

    status = meta.get("status")
    workstream = meta.get("workstream_id")
    summary = meta.get("summary")
    if status not in STATUSES or not isinstance(workstream, str) or WORKSTREAM_ID.fullmatch(workstream) is None or not isinstance(summary, str) or not summary.strip():
        _add(result, "delivery-ticket-state-invalid", "ticket requires a known status, Bxx/Wxx workstream_id, and non-empty summary", path)
        return None

    requirements = _strings(meta.get("requirement_ids"), non_empty=True)
    if requirements is None or not set(requirements) <= known_requirements:
        _add(result, "delivery-ticket-requirements-invalid", "requirement_ids must be a non-empty unique list from the current blueprint", path)

    blockers = _strings(meta.get("blockers"))
    if blockers is None or identifier in (blockers or ()):
        _add(result, "delivery-ticket-blockers-invalid", "blockers must be a unique ticket_id list that excludes the ticket itself", path)
        blockers = ()

    if "execution_mode" in meta:
        _add(
            result,
            "delivery-ticket-execution-mode-duplicate",
            "tickets must not declare a second execution_mode; one ready ticket is one execution unit by the Global Delivery Contract",
            path,
        )

    if status == "blocked":
        _validate_blocker_record(root, meta.get("blocker_record"), result, path)
    elif "blocker_record" in meta:
        _add(
            result,
            "delivery-ticket-blocked-record-unexpected",
            "blocker_record is allowed only while status is blocked",
            path,
        )

    if status == "superseded" and not _non_empty_string(meta.get("supersession_reason")):
        _add(
            result,
            "delivery-ticket-supersession-reason-missing",
            "superseded ticket requires a non-empty supersession_reason",
            path,
        )

    scope = meta.get("change_scope")
    if not isinstance(scope, dict) or _scope_paths(root, scope.get("allowed_write_paths")) is None or _scope_paths(root, scope.get("forbidden_write_paths")) is None or scope.get("mixed_file_policy") != "stop_if_safe_hunk_separation_is_impossible":
        _add(result, "delivery-ticket-scope-invalid", "scope requires exact allowed/forbidden paths and the canonical mixed-file policy", path)

    repair = meta.get("repair_policy")
    if not isinstance(repair, dict) or repair.get("allowed_within_scope") is not True or repair.get("retest_invalidated_evidence") is not True:
        _add(result, "delivery-ticket-repair-policy-invalid", "repair_policy must authorize in-scope repair and rerun invalidated evidence", path)

    validation = meta.get("validation")
    proof_skills = (
        _strings(validation.get("proof_skills")) if isinstance(validation, dict) else None
    )
    if (
        not isinstance(validation, dict)
        or validation.get("depth") not in VALIDATION_DEPTHS
        or proof_skills is None
        or (
            validation.get("depth") == "browser"
            and BROWSER_PROOF_SKILL not in proof_skills
        )
        or _strings(validation.get("commands"), non_empty=True, unique=False) is None
        or _repo_path(root, validation.get("evidence_target")) is None
        or not isinstance(validation.get("proof_boundary"), str)
        or not validation["proof_boundary"].strip()
    ):
        _add(
            result,
            "delivery-ticket-validation-invalid",
            "validation requires depth, proof_skills, commands, proof_boundary, and repository-local evidence_target; browser depth requires browser-qa-evidence",
            path,
        )

    sources = _proof_paths(root, meta.get("context_sources"))
    if sources is None or any(not (root / source).is_file() for source in sources or ()):
        _add(result, "delivery-ticket-context-invalid", "context_sources must be existing repository-local files", path)

    if _strings(meta.get("escalation_triggers"), non_empty=True) != CANONICAL_ESCALATIONS:
        _add(result, "delivery-ticket-escalation-invalid", "escalation_triggers must be the canonical closed set", path)

    evidence = _proof_paths(root, meta.get("evidence"))
    evidence_target_value = validation.get("evidence_target") if isinstance(validation, dict) else None
    proof_boundary = validation.get("proof_boundary") if isinstance(validation, dict) else None
    evidence_target = _repo_path(root, evidence_target_value)
    if evidence is None:
        _add(result, "delivery-ticket-evidence-invalid", "evidence must be a repository-local path list", path)
    elif status in TERMINAL_STATUSES:
        if not evidence or any(not (root / item).is_file() for item in evidence):
            _add(result, "delivery-ticket-evidence-missing", "accepted or superseded tickets require existing durable evidence", path)
        elif (
            not isinstance(evidence_target_value, str)
            or evidence_target_value not in evidence
            or evidence_target is None
            or not evidence_target.is_file()
        ):
            _add(result, "delivery-ticket-evidence-target-missing", "accepted or superseded tickets must link the existing validation.evidence_target", path)
        else:
            _validate_terminal_evidence(
                root,
                evidence_target,
                ticket_id=identifier,
                status=str(status),
                proof_boundary=proof_boundary,
                proof_skills=proof_skills,
                result=result,
            )

    if "# Outcome" not in body or "# Non-goals" not in body or "# Acceptance evidence" not in body:
        _add(result, "delivery-ticket-body-incomplete", "ticket body requires Outcome, Non-goals, and Acceptance evidence sections", path)
    return Ticket(identifier, path, str(status), blockers or ())


def _cycles(tickets: dict[str, Ticket]) -> set[str]:
    visiting: set[str] = set()
    visited: set[str] = set()
    members: set[str] = set()

    def visit(identifier: str) -> None:
        if identifier in visiting:
            members.update(visiting)
            return
        if identifier in visited:
            return
        visiting.add(identifier)
        for blocker in tickets[identifier].blockers:
            if blocker in tickets:
                visit(blocker)
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in tickets:
        visit(identifier)
    return members


def check(root: Path, ticket_root: Path = TICKET_ROOT) -> CheckResult:
    result = CheckResult("validate_delivery_tickets")
    blueprint = root / "custometry-technical-blueprint-ru.md"
    if not require_file(blueprint, result, "delivery-ticket-blueprint-missing"):
        return result
    try:
        _meta, body = parse_frontmatter(blueprint)
    except ValueError as exc:
        _add(result, "delivery-ticket-blueprint-invalid", str(exc), blueprint)
        return result
    directory = root / ticket_root
    if not require_dir(directory, result, "delivery-ticket-root-missing"):
        return result

    tickets: dict[str, Ticket] = {}
    for path in sorted(directory.glob("*.md")):
        ticket = _validate_ticket(root, path, frozenset(stable_ids(body)), result)
        if ticket is None:
            continue
        if ticket.identifier in tickets:
            _add(result, "delivery-ticket-duplicate", f"duplicate ticket_id {ticket.identifier}", path)
        else:
            tickets[ticket.identifier] = ticket

    for ticket in tickets.values():
        for blocker in ticket.blockers:
            dependency = tickets.get(blocker)
            if dependency is None:
                _add(result, "delivery-ticket-blocker-missing", f"blocker {blocker} does not exist", ticket.path)
            elif ticket.status in {"ready", "active"} and dependency.status not in TERMINAL_STATUSES:
                _add(result, "delivery-ticket-frontier-invalid", f"{ticket.status} ticket has open blocker {blocker} ({dependency.status})", ticket.path)
    for identifier in _cycles(tickets):
        _add(result, "delivery-ticket-cycle", "blocker graph contains a cycle", tickets[identifier].path)

    result.details.update(
        tickets=len(tickets),
        ready=sorted(item.identifier for item in tickets.values() if item.status == "ready"),
        active=sorted(item.identifier for item in tickets.values() if item.status == "active"),
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Custometry delivery tickets")
    add_common_arguments(parser)
    parser.add_argument("--tickets", type=Path, default=TICKET_ROOT)
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.tickets), args.json)


if __name__ == "__main__":
    main_guard(cli)
