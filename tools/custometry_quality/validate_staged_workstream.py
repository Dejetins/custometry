from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence, cast

from .core import (
    CheckResult,
    add_common_arguments,
    load_json,
    main_guard,
    parse_frontmatter,
    render_result,
    require_file,
    sha256_file,
)


TRIO_KEYS = ("plan_doc", "prompt_pack_dir", "stage_ledger")
STAGE_IDS = tuple(f"S{number:02d}" for number in range(7))
DELIVERY_WORKSTREAM_IDS = tuple(f"B{number:02d}" for number in range(1, 14))
STAGED_WORKSTREAM_IDS = (*DELIVERY_WORKSTREAM_IDS, "W14")
PROGRAM_WORKSTREAM_IDS = ("W00", *STAGED_WORKSTREAM_IDS)
REQUIRED_MILESTONE_GATES = {
    "repository_foundation": ("W00", "foundation_proof"),
    "product_foundation": ("B04", "S06"),
    "vertical_alpha": ("B06", "S06"),
    "public_mvp": ("B12", "S05"),
    "v1_feature_freeze": ("B13", "S06"),
    "v1_target": ("W14", "S06"),
}
REQUIRED_MILESTONES = frozenset(REQUIRED_MILESTONE_GATES)
ALLOWED_STAGE_STATUSES = {
    "pending",
    "in_progress",
    "accepted",
    "blocked",
    "skipped",
    "superseded",
}
TERMINAL_STAGE_STATUSES = {"accepted", "skipped", "superseded"}
LEDGER_STATUSES = {"dormant", "active", "blocked", "completed", "superseded"}
PROMPT_READINESS = {"outline", "executable"}
CANONICAL_EXECUTION_MODE = "goal_driven"
CYRILLIC = re.compile(r"[\u0400-\u04FF]")
STAGE_FILE = re.compile(r"^(S[0-9]{2}[A-Z]?)-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
PLACEHOLDER = re.compile(r"<[^>\n]+>|\bTBD\b")
EXECUTABLE_HEADINGS = (
    "# Objective",
    "## Non-goals",
    "## Verified current context",
    "## Context acquisition",
    "## Requirements",
    "## Forbidden actions",
    "## Work plan and stop gates",
    "## Contracts and side effects",
    "## Validation and evidence",
    "## Acceptance criteria",
    "## Result and handoff",
)


@dataclass(frozen=True, slots=True)
class StageRecord:
    stage_id: str
    status: str
    prompt_path: Path | None
    prompt_readiness: str
    previous_gate: str | None
    next_allowed: bool
    requirement_ids: tuple[str, ...]
    evidence: tuple[Path, ...]
    blocker: str | None


@dataclass(frozen=True, slots=True)
class LedgerRecord:
    path: Path
    status: str
    current_stage: str | None
    execution_mode: str
    stages: dict[str, StageRecord]


@dataclass(frozen=True, slots=True)
class ProgramRecord:
    path: Path
    workstreams: dict[str, dict[str, object]]
    dependencies: dict[str, tuple[str, ...]]
    soft_dependencies: dict[str, tuple[str, ...]]
    milestones: dict[str, tuple[str, str]]
    milestone_closures: dict[str, frozenset[str]]
    requirement_allocations: dict[str, RequirementAllocation]
    requirement_ids: frozenset[str]
    spec_version: str


@dataclass(frozen=True, slots=True)
class RoutingRecord:
    path: Path
    dependencies: dict[str, tuple[str, ...]]
    soft_dependencies: dict[str, tuple[str, ...]]
    release_milestones: dict[str, tuple[str, ...]]
    milestone_gates: dict[str, tuple[str, str]]


@dataclass(frozen=True, slots=True)
class RequirementAllocation:
    primary_workstream: str | None
    contributing_workstreams: tuple[str, ...]
    first_required_milestone: str | None = None


def _mapping(value: object) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return None
    mapping = cast(dict[object, object], value)
    if not all(isinstance(key, str) for key in mapping):
        return None
    return {cast(str, key): item for key, item in mapping.items()}


def _sequence(value: object) -> list[object] | None:
    if not isinstance(value, list):
        return None
    return list(cast(list[object], value))


def _strings(value: object, *, non_empty: bool = False) -> tuple[str, ...] | None:
    items = _sequence(value)
    if items is None or (non_empty and not items):
        return None
    if not all(isinstance(item, str) and item for item in items):
        return None
    return tuple(str(item) for item in items)


def _path(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value.strip() or "<" in value:
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    candidate = root / relative
    try:
        candidate.resolve(strict=False).relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def _same_path(left: Path | None, right: Path | None) -> bool:
    return (
        left is not None
        and right is not None
        and left.resolve(strict=False) == right.resolve(strict=False)
    )


def _read_frontmatter(
    path: Path,
    result: CheckResult,
    *,
    code: str,
) -> tuple[dict[str, object], str] | None:
    try:
        meta, body = parse_frontmatter(path)
    except (FileNotFoundError, ValueError) as exc:
        result.add(code, str(exc), path)
        return None
    return ({key: value for key, value in meta.items()}, body)


def _check_english(path: Path, result: CheckResult, artifact: str) -> None:
    try:
        source = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return
    if CYRILLIC.search(source):
        result.add(
            "staged-artifact-language-invalid",
            f"{artifact} must be written in English",
            path,
        )


def _blueprint_contract(root: Path, result: CheckResult) -> tuple[str, frozenset[str]] | None:
    blueprint = root / "custometry-technical-blueprint-ru.md"
    parsed = _read_frontmatter(blueprint, result, code="blueprint-frontmatter-invalid")
    if parsed is None:
        result.observed = False
        return None
    meta, _ = parsed
    spec_version = meta.get("spec_version")
    if not isinstance(spec_version, str) or not spec_version:
        result.add("blueprint-spec-version-invalid", "spec_version is required", blueprint)
        return None

    index_path = root / "docs/generated/requirement-index.json"
    if not require_file(index_path, result, "requirement-index-missing"):
        return None
    try:
        index = load_json(index_path)
    except ValueError as exc:
        result.add("requirement-index-invalid", str(exc), index_path)
        return None
    requirements = _sequence(index.get("requirements"))
    if requirements is None:
        result.add(
            "requirement-index-invalid",
            "requirements must be a list",
            index_path,
        )
        return None
    identifiers: set[str] = set()
    for item in requirements:
        entry = _mapping(item)
        identifier = entry.get("id") if entry is not None else None
        if not isinstance(identifier, str) or not identifier:
            result.add(
                "requirement-index-invalid",
                "every requirement needs a stable id",
                index_path,
            )
            continue
        identifiers.add(identifier)
    if index.get("spec_version") != spec_version:
        result.add(
            "requirement-index-version-drift",
            f"expected requirement index spec_version {spec_version}",
            index_path,
        )
    return spec_version, frozenset(identifiers)


def _discover_artifacts(root: Path) -> tuple[list[Path], list[Path]]:
    programs: list[Path] = []
    plans: list[Path] = []
    architecture = root / "docs/architecture"
    if not architecture.is_dir():
        return programs, plans
    for path in architecture.rglob("*.md"):
        try:
            meta, _ = parse_frontmatter(path)
        except ValueError:
            continue
        kind = meta.get("artifact_kind")
        if kind == "program_plan":
            programs.append(path)
        elif kind == "workstream_plan":
            plans.append(path)
    return sorted(programs), sorted(plans)


def _dependency_cycle(
    dependencies: dict[str, tuple[str, ...]],
) -> tuple[str, ...] | None:
    visiting: list[str] = []
    visited: set[str] = set()

    def visit(node: str) -> tuple[str, ...] | None:
        if node in visiting:
            start = visiting.index(node)
            return (*visiting[start:], node)
        if node in visited:
            return None
        visiting.append(node)
        for dependency in dependencies.get(node, ()):
            cycle = visit(dependency)
            if cycle is not None:
                return cycle
        visiting.pop()
        visited.add(node)
        return None

    for workstream_id in dependencies:
        cycle = visit(workstream_id)
        if cycle is not None:
            return cycle
    return None


def _transitive_dependencies(
    workstream_id: str,
    dependencies: dict[str, tuple[str, ...]],
) -> set[str]:
    resolved: set[str] = set()
    pending = list(dependencies.get(workstream_id, ()))
    while pending:
        dependency = pending.pop()
        if dependency in resolved:
            continue
        resolved.add(dependency)
        pending.extend(dependencies.get(dependency, ()))
    return resolved


def _validate_requirement_routing(
    root: Path,
    program_path: Path,
    routing_value: object,
    expected_spec_version: str,
    result: CheckResult,
) -> RoutingRecord | None:
    routing_path = _path(root, routing_value)
    if routing_path is None or not routing_path.is_file():
        result.add(
            "requirement-routing-missing",
            "program requirement_routing must resolve to a file",
            program_path,
        )
        return None
    try:
        routing = load_json(routing_path)
    except ValueError as exc:
        result.add("requirement-routing-invalid", str(exc), routing_path)
        return None
    if routing.get("schema_version") != 1:
        result.add(
            "requirement-routing-schema-invalid",
            "requirement routing requires schema_version=1",
            routing_path,
        )
    if routing.get("spec_version") != expected_spec_version:
        result.add(
            "requirement-routing-version-drift",
            f"expected spec_version {expected_spec_version}",
            routing_path,
        )

    dependency_items = _mapping(routing.get("workstream_dependencies"))
    dependencies: dict[str, tuple[str, ...]] = {}
    soft_dependencies: dict[str, tuple[str, ...]] = {}
    if dependency_items is None:
        result.add(
            "requirement-routing-dependencies-invalid",
            "workstream_dependencies must be an object",
            routing_path,
        )
        dependency_items = {}
    for workstream_id, raw_dependency_item in dependency_items.items():
        dependency_item = _mapping(raw_dependency_item)
        hard = (
            _strings(dependency_item.get("hard"))
            if dependency_item is not None
            else None
        )
        soft = (
            _strings(dependency_item.get("soft"))
            if dependency_item is not None
            else None
        )
        if hard is None or soft is None:
            result.add(
                "requirement-routing-dependencies-invalid",
                f"{workstream_id} requires hard and soft dependency lists",
                routing_path,
            )
            continue
        dependencies[workstream_id] = hard
        soft_dependencies[workstream_id] = soft
    if set(dependencies) != set(PROGRAM_WORKSTREAM_IDS):
        result.add(
            "requirement-routing-workstream-set-invalid",
            "workstream_dependencies must contain exactly W00, B01-B13, and W14",
            routing_path,
        )

    release_items = _mapping(routing.get("workstream_release_milestones"))
    release_milestones: dict[str, tuple[str, ...]] = {}
    if release_items is None:
        result.add(
            "requirement-routing-milestones-invalid",
            "workstream_release_milestones must be an object",
            routing_path,
        )
        release_items = {}
    for workstream_id, raw_milestones in release_items.items():
        milestones = _strings(raw_milestones, non_empty=True)
        if milestones is None or any(
            milestone not in REQUIRED_MILESTONES for milestone in milestones
        ):
            result.add(
                "requirement-routing-milestones-invalid",
                f"{workstream_id} has invalid release milestones",
                routing_path,
            )
            continue
        release_milestones[workstream_id] = milestones
    if set(release_milestones) != set(PROGRAM_WORKSTREAM_IDS):
        result.add(
            "requirement-routing-workstream-set-invalid",
            "workstream_release_milestones must contain exactly W00, B01-B13, and W14",
            routing_path,
        )

    milestone_ids = _strings(routing.get("milestones"), non_empty=True)
    terminals = _mapping(routing.get("terminal_milestones"))
    terminal_stages = _mapping(routing.get("milestone_terminal_stages"))
    milestone_gates: dict[str, tuple[str, str]] = {}
    if milestone_ids is None or set(milestone_ids) != set(REQUIRED_MILESTONES):
        result.add(
            "requirement-routing-milestone-set-invalid",
            f"milestones must contain exactly {sorted(REQUIRED_MILESTONES)}",
            routing_path,
        )
    if terminals is None or terminal_stages is None:
        result.add(
            "requirement-routing-gates-invalid",
            "terminal_milestones and milestone_terminal_stages must be objects",
            routing_path,
        )
    else:
        for milestone_id in REQUIRED_MILESTONES:
            terminal = terminals.get(milestone_id)
            terminal_stage = terminal_stages.get(milestone_id)
            if not isinstance(terminal, str) or not isinstance(terminal_stage, str):
                result.add(
                    "requirement-routing-gates-invalid",
                    f"{milestone_id} requires terminal workstream and stage",
                    routing_path,
                )
                continue
            milestone_gates[milestone_id] = (terminal, terminal_stage)
            expected_gate = REQUIRED_MILESTONE_GATES[milestone_id]
            if milestone_gates[milestone_id] != expected_gate:
                result.add(
                    "requirement-routing-gate-drift",
                    f"{milestone_id} gate must be {expected_gate[0]}:{expected_gate[1]}",
                    routing_path,
                )
        if set(terminals) != set(REQUIRED_MILESTONES) or set(terminal_stages) != set(
            REQUIRED_MILESTONES
        ):
            result.add(
                "requirement-routing-milestone-set-invalid",
                "terminal milestone maps must contain exactly the required milestones",
                routing_path,
            )

    expected_b12_hard = tuple(f"B{number:02d}" for number in range(1, 11))
    if dependencies.get("B12") != expected_b12_hard or soft_dependencies.get("B12") != (
        "B11",
    ):
        result.add(
            "public-mvp-dependency-gate-invalid",
            "B12 must hard-depend on B01-B10 and soft-depend on B11; "
            "public_mvp cannot be hard-gated by post-MVP B11",
            routing_path,
        )
    if dependencies.get("B13") != ("B10", "B11", "B12"):
        result.add(
            "feature-freeze-dependency-gate-invalid",
            "B13 hard dependencies must be B10, B11, and B12",
            routing_path,
        )

    return RoutingRecord(
        path=routing_path,
        dependencies=dependencies,
        soft_dependencies=soft_dependencies,
        release_milestones=release_milestones,
        milestone_gates=milestone_gates,
    )


def _validate_requirement_matrix(
    root: Path,
    program_path: Path,
    matrix_value: object,
    expected_spec_version: str,
    expected_requirement_ids: frozenset[str],
    result: CheckResult,
) -> dict[str, RequirementAllocation]:
    matrix_path = _path(root, matrix_value)
    if matrix_path is None or not matrix_path.is_file():
        result.add(
            "requirement-matrix-missing",
            "program requirement_matrix must resolve to a file",
            program_path,
        )
        return {}
    try:
        matrix = load_json(matrix_path)
    except ValueError as exc:
        result.add("requirement-matrix-invalid", str(exc), matrix_path)
        return {}
    if matrix.get("schema_version") != 1:
        result.add(
            "requirement-matrix-schema-invalid",
            "requirement matrix requires schema_version=1",
            matrix_path,
        )
    if matrix.get("spec_version") != expected_spec_version:
        result.add(
            "requirement-matrix-version-drift",
            f"expected spec_version {expected_spec_version}",
            matrix_path,
        )
    raw_allocations = _sequence(matrix.get("requirements"))
    if raw_allocations is None:
        result.add(
            "requirement-matrix-invalid",
            "requirements must be a list",
            matrix_path,
        )
        return {}
    allocations: dict[str, dict[str, object]] = {}
    for raw_allocation in raw_allocations:
        allocation = _mapping(raw_allocation)
        requirement_id = allocation.get("requirement_id") if allocation is not None else None
        if allocation is None or not isinstance(requirement_id, str) or not requirement_id:
            result.add(
                "requirement-allocation-invalid",
                "every requirement allocation needs requirement_id",
                matrix_path,
            )
            continue
        if requirement_id in allocations:
            result.add(
                "requirement-allocation-duplicate",
                f"duplicate allocation for {requirement_id}",
                matrix_path,
            )
            continue
        allocations[requirement_id] = allocation
    actual_ids = frozenset(allocations)
    missing = sorted(expected_requirement_ids - actual_ids)
    unknown = sorted(actual_ids - expected_requirement_ids)
    if missing:
        result.add(
            "requirement-matrix-incomplete",
            f"unallocated requirement IDs: {', '.join(missing)}",
            matrix_path,
        )
    if unknown:
        result.add(
            "requirement-matrix-unknown-id",
            f"unknown requirement IDs: {', '.join(unknown)}",
            matrix_path,
        )
    known_workstreams = set(PROGRAM_WORKSTREAM_IDS)
    normalized_allocations: dict[str, RequirementAllocation] = {}
    for requirement_id, allocation in allocations.items():
        primary = allocation.get("primary_workstream")
        supporting = _strings(allocation.get("contributing_workstreams"))
        implementation_evidence = _strings(
            allocation.get("implementation_evidence"),
            non_empty=True,
        )
        acceptance_evidence = _strings(
            allocation.get("acceptance_evidence"),
            non_empty=True,
        )
        first_required_milestone = allocation.get("first_required_milestone")
        status = allocation.get("status")
        if status not in {
            "allocated",
            "open",
            "reference_only",
            "decision_required",
            "deferred",
            "non_goal",
        }:
            result.add(
                "requirement-allocation-status-invalid",
                f"{requirement_id} has invalid status {status!r}",
                matrix_path,
            )
        if not isinstance(primary, str) or primary not in known_workstreams:
            result.add(
                "requirement-primary-owner-invalid",
                f"{requirement_id} needs exactly one known primary_workstream",
                matrix_path,
            )
        if supporting is None or any(item not in known_workstreams for item in supporting):
            result.add(
                "requirement-supporting-owner-invalid",
                f"{requirement_id} supporting_workstreams must reference known IDs",
                matrix_path,
            )
        elif isinstance(primary, str) and primary in supporting:
            result.add(
                "requirement-owner-duplicate",
                f"{requirement_id} primary owner cannot also be supporting",
                matrix_path,
            )
        if implementation_evidence is None:
            result.add(
                "requirement-implementation-evidence-missing",
                f"{requirement_id} needs implementation_evidence",
                matrix_path,
            )
        if acceptance_evidence is None:
            result.add(
                "requirement-acceptance-evidence-missing",
                f"{requirement_id} needs acceptance_evidence",
                matrix_path,
            )
        if (
            not isinstance(first_required_milestone, str)
            or first_required_milestone not in REQUIRED_MILESTONES
        ):
            result.add(
                "requirement-first-milestone-invalid",
                f"{requirement_id} needs a known first_required_milestone",
                matrix_path,
            )
        normalized_allocations[requirement_id] = RequirementAllocation(
            primary_workstream=primary if isinstance(primary, str) else None,
            contributing_workstreams=supporting or (),
            first_required_milestone=(
                first_required_milestone
                if isinstance(first_required_milestone, str)
                else None
            ),
        )
    return normalized_allocations


def _validate_module_definition(
    path: Path,
    workstream_id: str,
    expected_spec_version: str,
    expected_requirement_ids: frozenset[str],
    result: CheckResult,
) -> None:
    parsed = _read_frontmatter(path, result, code="module-frontmatter-invalid")
    if parsed is None:
        return
    meta, _ = parsed
    _check_english(path, result, "module definitions")
    if (
        meta.get("artifact_kind") != "module_definition"
        or meta.get("staged_schema_version") != 1
    ):
        result.add(
            "module-schema-invalid",
            "module requires artifact_kind=module_definition and staged_schema_version=1",
            path,
        )
    if meta.get("workstream_id") != workstream_id:
        result.add(
            "module-workstream-id-drift",
            f"module workstream_id must be {workstream_id}",
            path,
        )
    if meta.get("product_spec_version") != expected_spec_version:
        result.add(
            "module-spec-version-drift",
            f"expected product_spec_version {expected_spec_version}",
            path,
        )
    requirement_ids = _strings(meta.get("requirement_ids"))
    if requirement_ids is None:
        result.add(
            "module-requirements-invalid",
            "module requirement_ids must be a list",
            path,
        )
        return
    if len(requirement_ids) != len(set(requirement_ids)):
        result.add(
            "module-requirements-duplicate",
            "module requirement_ids must not contain duplicates",
            path,
        )
    if set(requirement_ids) != set(expected_requirement_ids):
        missing = sorted(set(expected_requirement_ids) - set(requirement_ids))
        extra = sorted(set(requirement_ids) - set(expected_requirement_ids))
        result.add(
            "module-primary-requirements-drift",
            "module requirement_ids must equal the primary matrix allocation; "
            f"missing={missing}, extra={extra}",
            path,
        )


def _validate_program(
    root: Path,
    path: Path,
    expected_spec_version: str,
    expected_requirement_ids: frozenset[str],
    result: CheckResult,
) -> ProgramRecord | None:
    parsed = _read_frontmatter(path, result, code="program-frontmatter-invalid")
    if parsed is None:
        return None
    meta, _ = parsed
    _check_english(path, result, "program plans")
    if meta.get("artifact_kind") != "program_plan" or meta.get("staged_schema_version") != 1:
        result.add(
            "program-schema-invalid",
            "program plan requires artifact_kind=program_plan and staged_schema_version=1",
            path,
        )
    if meta.get("spec_version") != expected_spec_version:
        result.add(
            "program-spec-version-drift",
            f"expected spec_version {expected_spec_version}",
            path,
        )
    if not isinstance(meta.get("program_id"), str) or not meta.get("program_id"):
        result.add("program-id-invalid", "program_id is required", path)
    if meta.get("execution_mode") != CANONICAL_EXECUTION_MODE:
        result.add(
            "program-execution-mode-invalid",
            f"program execution_mode must be {CANONICAL_EXECUTION_MODE}",
            path,
        )
    routing = _validate_requirement_routing(
        root,
        path,
        meta.get("requirement_routing"),
        expected_spec_version,
        result,
    )

    raw_entries = _sequence(meta.get("workstreams"))
    entries: dict[str, dict[str, object]] = {}
    dependencies: dict[str, tuple[str, ...]] = {}
    soft_dependencies: dict[str, tuple[str, ...]] = {}
    seen_artifact_paths: dict[Path, str] = {}
    if raw_entries is None:
        result.add("program-workstreams-invalid", "workstreams must be a list", path)
        raw_entries = []
    for raw_entry in raw_entries:
        entry = _mapping(raw_entry)
        workstream_id = entry.get("workstream_id") if entry is not None else None
        if entry is None or not isinstance(workstream_id, str):
            result.add(
                "program-workstream-invalid",
                "every workstream must be an object with workstream_id",
                path,
            )
            continue
        if workstream_id in entries:
            result.add(
                "program-workstream-duplicate",
                f"duplicate workstream {workstream_id}",
                path,
            )
            continue
        entries[workstream_id] = entry
        hard = _strings(entry.get("hard_dependencies"))
        soft = _strings(entry.get("soft_dependencies"))
        if hard is None:
            result.add(
                "program-dependencies-invalid",
                f"{workstream_id} hard_dependencies must be a list of IDs",
                path,
            )
            hard = ()
        if soft is None:
            result.add(
                "program-dependencies-invalid",
                f"{workstream_id} soft_dependencies must be a list of IDs",
                path,
            )
            soft = ()
        dependencies[workstream_id] = hard
        soft_dependencies[workstream_id] = soft
        release_milestones = _strings(entry.get("release_milestones"), non_empty=True)
        if release_milestones is None:
            result.add(
                "program-workstream-milestones-invalid",
                f"{workstream_id} release_milestones must be a non-empty list",
                path,
            )
        elif any(milestone not in REQUIRED_MILESTONES for milestone in release_milestones):
            result.add(
                "program-workstream-milestones-invalid",
                f"{workstream_id} references an unknown release milestone",
                path,
            )
        expected_kind = (
            "foundation_baseline"
            if workstream_id == "W00"
            else "acceptance_bookend"
            if workstream_id == "W14"
            else "delivery"
        )
        if entry.get("kind") != expected_kind:
            result.add(
                "program-workstream-kind-invalid",
                f"{workstream_id} requires kind={expected_kind}",
                path,
            )
        if workstream_id in STAGED_WORKSTREAM_IDS:
            for key in TRIO_KEYS:
                artifact_path = _path(root, entry.get(key))
                if artifact_path is None:
                    result.add(
                        "program-workstream-link-invalid",
                        f"{workstream_id} has invalid {key}",
                        path,
                    )
                    continue
                resolved = artifact_path.resolve(strict=False)
                prior = seen_artifact_paths.get(resolved)
                if prior is not None:
                    result.add(
                        "program-workstream-path-duplicate",
                        f"{workstream_id} and {prior} share {key} {artifact_path}",
                        path,
                    )
                else:
                    seen_artifact_paths[resolved] = workstream_id
            if workstream_id in DELIVERY_WORKSTREAM_IDS:
                module_definition = _path(root, entry.get("module_definition"))
                if module_definition is None or not module_definition.is_file():
                    result.add(
                        "module-definition-missing",
                        f"{workstream_id} module_definition is missing",
                        path,
                    )

    actual_ids = set(entries)
    expected_ids = set(PROGRAM_WORKSTREAM_IDS)
    if actual_ids != expected_ids:
        result.add(
            "program-workstream-set-invalid",
            "program must contain exactly W00, B01-B13, and W14; "
            f"missing={sorted(expected_ids - actual_ids)}, extra={sorted(actual_ids - expected_ids)}",
            path,
        )
    for workstream_id, hard in dependencies.items():
        soft = soft_dependencies.get(workstream_id, ())
        if set(hard) & set(soft):
            result.add(
                "program-dependency-overlap",
                f"{workstream_id} repeats a dependency as hard and soft",
                path,
            )
        for dependency in (*hard, *soft):
            if dependency not in entries:
                result.add(
                    "program-dependency-unknown",
                    f"{workstream_id} depends on unknown {dependency}",
                    path,
                )
            if dependency == workstream_id:
                result.add(
                    "program-dependency-self",
                    f"{workstream_id} cannot depend on itself",
                    path,
                )
    cycle = _dependency_cycle(dependencies)
    if cycle is not None:
        result.add(
            "program-dependency-cycle",
            f"dependency cycle: {' -> '.join(cycle)}",
            path,
        )
    if routing is not None:
        for workstream_id in PROGRAM_WORKSTREAM_IDS:
            if dependencies.get(workstream_id) != routing.dependencies.get(workstream_id):
                result.add(
                    "program-routing-hard-dependency-drift",
                    f"{workstream_id} hard_dependencies differ from requirement routing",
                    path,
                )
            if soft_dependencies.get(workstream_id) != routing.soft_dependencies.get(
                workstream_id
            ):
                result.add(
                    "program-routing-soft-dependency-drift",
                    f"{workstream_id} soft_dependencies differ from requirement routing",
                    path,
                )
            entry = entries.get(workstream_id)
            direct_milestones = (
                _strings(entry.get("release_milestones"))
                if entry is not None
                else None
            )
            if direct_milestones != routing.release_milestones.get(workstream_id):
                result.add(
                    "program-routing-release-milestone-drift",
                    f"{workstream_id} release_milestones differ from requirement routing",
                    path,
                )

    raw_milestones = _sequence(meta.get("release_milestones"))
    milestones: dict[str, tuple[str, str]] = {}
    if raw_milestones is None:
        result.add("program-milestones-invalid", "release_milestones must be a list", path)
        raw_milestones = []
    for raw_milestone in raw_milestones:
        milestone = _mapping(raw_milestone)
        milestone_id = milestone.get("milestone_id") if milestone is not None else None
        terminal = milestone.get("terminal_workstream") if milestone is not None else None
        terminal_stage = milestone.get("terminal_stage") if milestone is not None else None
        if (
            not isinstance(milestone_id, str)
            or not isinstance(terminal, str)
            or not isinstance(terminal_stage, str)
        ):
            result.add(
                "program-milestone-invalid",
                "every milestone requires milestone_id, terminal_workstream, and terminal_stage",
                path,
            )
            continue
        if milestone_id in milestones:
            result.add(
                "program-milestone-duplicate",
                f"duplicate milestone {milestone_id}",
                path,
            )
            continue
        milestones[milestone_id] = (terminal, terminal_stage)
    if set(milestones) != set(REQUIRED_MILESTONES):
        result.add(
            "program-milestone-set-invalid",
            f"required milestones are {sorted(REQUIRED_MILESTONES)}",
            path,
        )
    milestone_closures: dict[str, frozenset[str]] = {}
    for milestone_id, expected_gate in REQUIRED_MILESTONE_GATES.items():
        actual_gate = milestones.get(milestone_id)
        if actual_gate != expected_gate:
            result.add(
                "program-milestone-terminal-drift",
                f"{milestone_id} terminal must be {expected_gate[0]}:{expected_gate[1]}",
                path,
            )
        if actual_gate is not None and actual_gate[0] not in entries:
            result.add(
                "program-milestone-workstream-unknown",
                f"{milestone_id} references unknown terminal {actual_gate[0]}",
                path,
            )
        if actual_gate is not None and actual_gate[0] in entries:
            terminal_workstream = actual_gate[0]
            milestone_closures[milestone_id] = frozenset(
                {
                    terminal_workstream,
                    *_transitive_dependencies(terminal_workstream, dependencies),
                }
            )
            terminal_entry = entries[terminal_workstream]
            terminal_direct_milestones = _strings(
                terminal_entry.get("release_milestones")
            )
            if (
                terminal_direct_milestones is None
                or milestone_id not in terminal_direct_milestones
            ):
                result.add(
                    "program-milestone-terminal-participation-missing",
                    f"{terminal_workstream} must directly declare {milestone_id}",
                    path,
                )
    if routing is not None and milestones != routing.milestone_gates:
        result.add(
            "program-routing-milestone-gate-drift",
            "program milestone gates differ from requirement routing",
            path,
        )

    requirement_allocations = _validate_requirement_matrix(
        root,
        path,
        meta.get("requirement_matrix"),
        expected_spec_version,
        expected_requirement_ids,
        result,
    )
    matrix_path = _path(root, meta.get("requirement_matrix")) or path
    for requirement_id, allocation in requirement_allocations.items():
        milestone = allocation.first_required_milestone
        if milestone is None:
            continue
        closure = milestone_closures.get(milestone)
        if (
            closure is not None
            and allocation.primary_workstream is not None
            and allocation.primary_workstream not in closure
        ):
            result.add(
                "requirement-primary-owner-outside-first-milestone",
                f"{requirement_id} primary owner {allocation.primary_workstream} "
                f"cannot satisfy first milestone {milestone}; "
                f"closure={sorted(closure)}",
                matrix_path,
            )
    for workstream_id in DELIVERY_WORKSTREAM_IDS:
        entry = entries.get(workstream_id)
        module_path = (
            _path(root, entry.get("module_definition"))
            if entry is not None
            else None
        )
        if module_path is None or not module_path.is_file():
            continue
        primary_requirement_ids = frozenset(
            requirement_id
            for requirement_id, allocation in requirement_allocations.items()
            if allocation.primary_workstream == workstream_id
        )
        _validate_module_definition(
            module_path,
            workstream_id,
            expected_spec_version,
            primary_requirement_ids,
            result,
        )
    return ProgramRecord(
        path=path,
        workstreams=entries,
        dependencies=dependencies,
        soft_dependencies=soft_dependencies,
        milestones=milestones,
        milestone_closures=milestone_closures,
        requirement_allocations=requirement_allocations,
        requirement_ids=expected_requirement_ids,
        spec_version=expected_spec_version,
    )


def _validate_evidence(
    root: Path,
    ledger_path: Path,
    stage_id: str,
    status: str,
    raw_evidence: object,
    result: CheckResult,
) -> tuple[Path, ...]:
    values = _strings(raw_evidence)
    if values is None:
        result.add(
            "ledger-stage-evidence-invalid",
            f"{stage_id} evidence must be a list of paths",
            ledger_path,
        )
        return ()
    evidence: list[Path] = []
    for value in values:
        evidence_path = _path(root, value)
        if evidence_path is None:
            result.add(
                "ledger-stage-evidence-invalid",
                f"{stage_id} evidence path is unsafe: {value}",
                ledger_path,
            )
            continue
        evidence.append(evidence_path)
    if status in {"accepted", "blocked", "skipped", "superseded"}:
        if not evidence:
            result.add(
                "ledger-stage-evidence-missing",
                f"{stage_id} status {status} requires evidence",
                ledger_path,
            )
        for evidence_path in evidence:
            if not evidence_path.is_file():
                result.add(
                    "ledger-stage-evidence-missing",
                    f"{stage_id} evidence file is absent",
                    evidence_path,
                )
    return tuple(evidence)


def _validate_ledger(
    root: Path,
    path: Path,
    plan_path: Path,
    pack_path: Path,
    workstream_id: str,
    expected_spec_version: str,
    result: CheckResult,
) -> LedgerRecord | None:
    parsed = _read_frontmatter(path, result, code="ledger-frontmatter-invalid")
    if parsed is None:
        return None
    meta, _ = parsed
    _check_english(path, result, "stage ledgers and evidence")
    if meta.get("artifact_kind") != "stage_ledger" or meta.get("staged_schema_version") != 1:
        result.add(
            "ledger-schema-invalid",
            "ledger requires artifact_kind=stage_ledger and staged_schema_version=1",
            path,
        )
    if meta.get("workstream_id") != workstream_id:
        result.add(
            "ledger-workstream-id-drift",
            f"ledger workstream_id must be {workstream_id}",
            path,
        )
    expected_links = {
        "plan_doc": plan_path,
        "prompt_pack_dir": pack_path,
        "stage_ledger": path,
    }
    for key, expected in expected_links.items():
        if not _same_path(_path(root, meta.get(key)), expected):
            result.add(
                "staged-trio-link-mismatch",
                f"ledger {key} must equal the owning workstream link",
                path,
            )
    if meta.get("spec_version") != expected_spec_version:
        result.add(
            "ledger-spec-version-drift",
            f"expected spec_version {expected_spec_version}",
            path,
        )
    allowed = _strings(meta.get("allowed_stage_statuses"))
    if allowed is None or set(allowed) != ALLOWED_STAGE_STATUSES:
        result.add(
            "ledger-status-contract-invalid",
            "allowed_stage_statuses is not canonical",
            path,
        )
    ledger_status = meta.get("ledger_status")
    if ledger_status not in LEDGER_STATUSES:
        result.add(
            "ledger-status-invalid",
            f"ledger_status must be one of {sorted(LEDGER_STATUSES)}",
            path,
        )
        ledger_status = ""
    execution_mode = meta.get("execution_mode")
    if execution_mode != CANONICAL_EXECUTION_MODE:
        result.add(
            "ledger-execution-mode-invalid",
            f"execution_mode must be {CANONICAL_EXECUTION_MODE}",
            path,
        )
        execution_mode = ""
    current_value = meta.get("current_stage")
    current_stage = current_value if isinstance(current_value, str) else None
    if current_value is not None and current_stage not in STAGE_IDS:
        result.add(
            "ledger-current-stage-invalid",
            "current_stage must be S00-S06 or null",
            path,
        )

    raw_stages = _sequence(meta.get("stages"))
    stages: dict[str, StageRecord] = {}
    if raw_stages is None:
        result.add("ledger-stages-invalid", "stages must be a list", path)
        raw_stages = []
    for raw_stage in raw_stages:
        stage = _mapping(raw_stage)
        stage_id = stage.get("stage_id") if stage is not None else None
        if stage is None or not isinstance(stage_id, str):
            result.add(
                "ledger-stage-invalid",
                "every stage must be an object with stage_id",
                path,
            )
            continue
        if stage_id in stages:
            result.add(
                "ledger-stage-duplicate",
                f"duplicate stage {stage_id}",
                path,
            )
            continue
        status = stage.get("status")
        readiness = stage.get("prompt_readiness")
        next_allowed = stage.get("next_allowed")
        previous_gate = stage.get("previous_gate")
        requirement_ids = _strings(stage.get("requirement_ids"), non_empty=True)
        blocker = stage.get("blocker")
        supersedes = _strings(stage.get("supersedes"))
        prompt_path = _path(root, stage.get("prompt_path"))
        if status not in ALLOWED_STAGE_STATUSES:
            result.add(
                "ledger-stage-status-invalid",
                f"{stage_id} has invalid status {status!r}",
                path,
            )
            status = ""
        if readiness not in PROMPT_READINESS:
            result.add(
                "ledger-stage-readiness-invalid",
                f"{stage_id} prompt_readiness must be outline or executable",
                path,
            )
            readiness = ""
        if not isinstance(next_allowed, bool):
            result.add(
                "ledger-stage-next-allowed-invalid",
                f"{stage_id} next_allowed must be boolean",
                path,
            )
            next_allowed = False
        if previous_gate is not None and not isinstance(previous_gate, str):
            result.add(
                "ledger-stage-previous-gate-invalid",
                f"{stage_id} previous_gate must be a stage ID or null",
                path,
            )
            previous_gate = None
        if requirement_ids is None:
            result.add(
                "ledger-stage-requirements-invalid",
                f"{stage_id} requires non-empty requirement_ids",
                path,
            )
            requirement_ids = ()
        if blocker is not None and not isinstance(blocker, str):
            result.add(
                "ledger-stage-blocker-invalid",
                f"{stage_id} blocker must be a string or null",
                path,
            )
            blocker = None
        if supersedes is None:
            result.add(
                "ledger-stage-supersedes-invalid",
                f"{stage_id} supersedes must be a list",
                path,
            )
        if prompt_path is None:
            result.add(
                "ledger-stage-prompt-invalid",
                f"{stage_id} prompt_path is unsafe or unresolved",
                path,
            )
        elif prompt_path.parent.resolve(strict=False) != pack_path.resolve(strict=False):
            result.add(
                "ledger-stage-prompt-outside-pack",
                f"{stage_id} prompt must be inside the owning pack",
                path,
            )
        evidence = _validate_evidence(root, path, stage_id, str(status), stage.get("evidence"), result)
        stages[stage_id] = StageRecord(
            stage_id=stage_id,
            status=str(status),
            prompt_path=prompt_path,
            prompt_readiness=str(readiness),
            previous_gate=str(previous_gate) if previous_gate is not None else None,
            next_allowed=bool(next_allowed),
            requirement_ids=requirement_ids,
            evidence=evidence,
            blocker=str(blocker) if blocker is not None else None,
        )

    if set(stages) != set(STAGE_IDS):
        result.add(
            "ledger-stage-set-invalid",
            f"ledger requires exactly {', '.join(STAGE_IDS)}",
            path,
        )
    for index, stage_id in enumerate(STAGE_IDS):
        stage = stages.get(stage_id)
        if stage is None:
            continue
        expected_previous = STAGE_IDS[index - 1] if index else None
        if stage.previous_gate != expected_previous:
            result.add(
                "ledger-stage-previous-gate-invalid",
                f"{stage_id} previous_gate must be {expected_previous!r}",
                path,
            )
        for requirement_id in stage.requirement_ids:
            if requirement_id.startswith("<"):
                result.add(
                    "ledger-stage-requirements-invalid",
                    f"{stage_id} contains an unresolved requirement placeholder",
                    path,
                )

    if current_stage is not None and current_stage not in stages:
        result.add(
            "ledger-current-stage-missing",
            f"current stage {current_stage} is absent from stages",
            path,
        )
    allowed_stages = [stage.stage_id for stage in stages.values() if stage.next_allowed]
    if ledger_status == "dormant":
        if allowed_stages:
            result.add(
                "dormant-ledger-executable",
                "dormant ledger cannot allow a next stage",
                path,
            )
        if any(stage.status == "in_progress" for stage in stages.values()):
            result.add(
                "dormant-ledger-in-progress",
                "dormant ledger cannot have an in_progress stage",
                path,
            )
    elif ledger_status == "active":
        if current_stage is None or allowed_stages != [current_stage]:
            result.add(
                "active-ledger-gate-invalid",
                "active ledger must allow exactly its current stage",
                path,
            )
        current = stages.get(current_stage or "")
        if current is not None and current.status not in {"pending", "in_progress"}:
            result.add(
                "active-ledger-stage-status-invalid",
                "active current stage must be pending or in_progress",
                path,
            )
        if current is not None and current.prompt_readiness != "executable":
            result.add(
                "active-ledger-outline-forbidden",
                "active current stage must have an executable prompt",
                path,
            )
        if current is not None and current.previous_gate is not None:
            predecessor = stages.get(current.previous_gate)
            if predecessor is None or predecessor.status not in {"accepted", "superseded"}:
                result.add(
                    "active-ledger-predecessor-open",
                    "active current stage predecessor must be accepted or superseded",
                    path,
                )
    elif ledger_status == "blocked":
        if allowed_stages:
            result.add(
                "blocked-ledger-executable",
                "blocked ledger cannot allow a next stage",
                path,
            )
        current = stages.get(current_stage or "")
        if current is None or current.status != "blocked" or not current.blocker:
            result.add(
                "blocked-ledger-context-invalid",
                "blocked ledger current stage must be blocked with a blocker",
                path,
            )
    elif ledger_status == "completed":
        if current_value is not None or allowed_stages:
            result.add(
                "completed-ledger-current-stage-invalid",
                "completed ledger needs current_stage=null and no next_allowed stage",
                path,
            )
        if any(stage.status not in TERMINAL_STAGE_STATUSES for stage in stages.values()):
            result.add(
                "completed-ledger-open-stage",
                "completed ledger cannot contain open or blocked stages",
                path,
            )
    elif ledger_status == "superseded":
        if current_value is not None or allowed_stages:
            result.add(
                "superseded-ledger-current-stage-invalid",
                "superseded ledger needs current_stage=null and no next_allowed stage",
                path,
            )
        if not isinstance(meta.get("superseded_by"), str) or not meta.get("superseded_by"):
            result.add(
                "superseded-ledger-replacement-missing",
                "superseded ledger requires superseded_by",
                path,
            )
    if meta.get("goal_doc") is not None:
        result.add(
            "forbidden-coordination-source",
            "ledger links an unapproved goal_doc coordination source",
            path,
        )
    return LedgerRecord(
        path=path,
        status=str(ledger_status),
        current_stage=current_stage,
        execution_mode=str(execution_mode),
        stages=stages,
    )


def _validate_source_hashes(
    root: Path,
    prompt: Path,
    raw_hashes: object,
    *,
    verify_content: bool,
    require_non_empty: bool,
    result: CheckResult,
) -> None:
    hashes = _mapping(raw_hashes)
    if hashes is None:
        result.add(
            "source-hash-gate-missing",
            "required_source_hashes must be a mapping",
            prompt,
        )
        return
    if require_non_empty and not hashes:
        result.add(
            "source-hash-gate-empty",
            "the active executable current stage requires at least one pinned source hash",
            prompt,
        )
        return
    for source, digest in hashes.items():
        source_path = _path(root, source)
        if source_path is None or not isinstance(digest, str) or not SHA256.fullmatch(digest):
            result.add(
                "source-hash-gate-invalid",
                f"invalid source hash entry for {source}",
                prompt,
            )
            continue
        if verify_content:
            if not source_path.is_file():
                result.add(
                    "source-hash-input-missing",
                    f"required source is absent: {source}",
                    prompt,
                )
            elif f"sha256:{sha256_file(source_path)}" != digest:
                result.add(
                    "source-hash-mismatch",
                    f"required source changed: {source}",
                    prompt,
                )


def _validate_prompt(
    root: Path,
    prompt: Path,
    plan_path: Path,
    pack_path: Path,
    ledger: LedgerRecord,
    workstream_id: str,
    plan_requirement_ids: frozenset[str],
    expected_spec_version: str,
    stage: StageRecord,
    result: CheckResult,
) -> dict[str, object] | None:
    parsed = _read_frontmatter(prompt, result, code="prompt-frontmatter-invalid")
    if parsed is None:
        return None
    meta, body = parsed
    _check_english(prompt, result, "prompt-pack artifacts")
    match = STAGE_FILE.fullmatch(prompt.name)
    if match is None or match.group(1) != stage.stage_id:
        result.add(
            "prompt-stage-filename-invalid",
            f"prompt filename must start with {stage.stage_id}-",
            prompt,
        )
    if meta.get("spec_version") != expected_spec_version:
        result.add(
            "prompt-spec-version-drift",
            f"expected spec_version {expected_spec_version}",
            prompt,
        )
    requirement_ids = _strings(meta.get("requirement_ids"), non_empty=True)
    if requirement_ids is None:
        result.add(
            "prompt-requirements-invalid",
            "prompt requires non-empty requirement_ids",
            prompt,
        )
        requirement_ids = ()
    if tuple(requirement_ids) != stage.requirement_ids:
        result.add(
            "prompt-ledger-requirement-drift",
            "prompt requirement_ids must equal the ledger stage requirement_ids",
            prompt,
        )
    unknown_plan_ids = sorted(set(requirement_ids) - set(plan_requirement_ids))
    if unknown_plan_ids:
        result.add(
            "prompt-plan-requirement-drift",
            f"prompt requirement IDs are outside the plan: {', '.join(unknown_plan_ids)}",
            prompt,
        )

    execution = _mapping(meta.get("prompt_pack_execution"))
    if execution is None:
        result.add(
            "prompt-execution-schema-invalid",
            "prompt_pack_execution must be a mapping",
            prompt,
        )
        return None
    if execution.get("staged_schema_version") != 1:
        result.add(
            "prompt-execution-schema-invalid",
            "prompt execution requires staged_schema_version=1",
            prompt,
        )
    readiness = execution.get("readiness")
    enabled = execution.get("enabled")
    if readiness not in PROMPT_READINESS:
        result.add(
            "prompt-readiness-invalid",
            "readiness must be outline or executable",
            prompt,
        )
    expected_enabled = readiness == "executable"
    if not isinstance(enabled, bool) or enabled is not expected_enabled:
        result.add(
            "prompt-enabled-readiness-drift",
            "outline requires enabled=false and executable requires enabled=true",
            prompt,
        )
    if readiness != stage.prompt_readiness:
        result.add(
            "prompt-ledger-readiness-drift",
            "prompt readiness must equal ledger prompt_readiness",
            prompt,
        )
    if execution.get("workstream_id") != workstream_id:
        result.add(
            "prompt-workstream-id-drift",
            f"prompt workstream_id must be {workstream_id}",
            prompt,
        )
    if execution.get("stage_id") != stage.stage_id:
        result.add(
            "prompt-stage-id-drift",
            f"prompt stage_id must be {stage.stage_id}",
            prompt,
        )
    prompt_execution_mode = execution.get("execution_mode")
    if prompt_execution_mode != CANONICAL_EXECUTION_MODE:
        result.add(
            "prompt-execution-mode-invalid",
            f"prompt execution_mode must be {CANONICAL_EXECUTION_MODE}",
            prompt,
        )
    if prompt_execution_mode != ledger.execution_mode:
        result.add(
            "prompt-execution-mode-drift",
            "prompt execution_mode must equal ledger execution_mode",
            prompt,
        )
    expected_links = {
        "plan_doc": plan_path,
        "prompt_pack_dir": pack_path,
        "stage_ledger": ledger.path,
    }
    for key, expected in expected_links.items():
        if not _same_path(_path(root, execution.get(key)), expected):
            result.add(
                "staged-trio-link-mismatch",
                f"prompt {key} must equal the owning workstream link",
                prompt,
            )

    predecessor = _mapping(execution.get("predecessor_gate"))
    expected_previous = stage.previous_gate
    if predecessor is None:
        result.add(
            "prompt-predecessor-gate-invalid",
            "predecessor_gate must be a mapping",
            prompt,
        )
    else:
        if predecessor.get("stage_id") != expected_previous:
            result.add(
                "prompt-predecessor-gate-invalid",
                f"predecessor stage must be {expected_previous!r}",
                prompt,
            )
        allowed = _strings(predecessor.get("allowed_statuses"))
        expected_statuses = () if expected_previous is None else ("accepted", "superseded")
        if allowed != expected_statuses:
            result.add(
                "prompt-predecessor-gate-invalid",
                f"allowed predecessor statuses must be {list(expected_statuses)}",
                prompt,
            )
    if _sequence(execution.get("state_preconditions")) is None:
        result.add(
            "prompt-state-preconditions-invalid",
            "state_preconditions must be a list",
            prompt,
        )
    branch_policy = _mapping(execution.get("branch_policy"))
    if branch_policy is None or branch_policy.get("per_stage_branches") != "forbidden":
        result.add(
            "branch-policy-invalid",
            "per-stage branches must be forbidden",
            prompt,
        )
        branch_policy = None
    next_stage_rule = _mapping(execution.get("next_stage_rule"))
    if next_stage_rule is None:
        result.add(
            "prompt-next-stage-rule-invalid",
            "next_stage_rule must be a mapping",
            prompt,
        )
    else:
        index = STAGE_IDS.index(stage.stage_id) if stage.stage_id in STAGE_IDS else -1
        candidate = STAGE_IDS[index + 1] if 0 <= index < len(STAGE_IDS) - 1 else None
        if (
            next_stage_rule.get("candidate_stage") != candidate
            or next_stage_rule.get("unlock_on") != "accepted"
            or next_stage_rule.get("authority") != "stage_ledger"
        ):
            result.add(
                "prompt-next-stage-rule-invalid",
                "next_stage_rule must name the next canonical stage and ledger authority",
                prompt,
            )
    verify_hashes = (
        ledger.status == "active"
        and ledger.current_stage == stage.stage_id
        and stage.next_allowed
        and readiness == "executable"
    )
    _validate_source_hashes(
        root,
        prompt,
        execution.get("required_source_hashes"),
        verify_content=verify_hashes,
        require_non_empty=verify_hashes,
        result=result,
    )
    if readiness == "executable":
        missing_headings = [heading for heading in EXECUTABLE_HEADINGS if heading not in body]
        if missing_headings:
            result.add(
                "executable-prompt-sections-missing",
                f"missing sections: {', '.join(missing_headings)}",
                prompt,
            )
        if PLACEHOLDER.search(body):
            result.add(
                "executable-prompt-placeholder",
                "executable prompt contains an unresolved placeholder",
                prompt,
            )
    return branch_policy


def _validate_plan(
    root: Path,
    path: Path,
    program: ProgramRecord,
    entry: dict[str, object],
    expected_workstream_id: str,
    result: CheckResult,
) -> LedgerRecord | None:
    parsed = _read_frontmatter(path, result, code="plan-frontmatter-invalid")
    if parsed is None:
        return None
    meta, _ = parsed
    _check_english(path, result, "workstream plans")
    if meta.get("artifact_kind") != "workstream_plan" or meta.get("staged_schema_version") != 1:
        result.add(
            "plan-schema-invalid",
            "plan requires artifact_kind=workstream_plan and staged_schema_version=1",
            path,
        )
    workstream_id = meta.get("workstream_id")
    if workstream_id != expected_workstream_id:
        result.add(
            "plan-workstream-id-drift",
            f"plan workstream_id must be {expected_workstream_id}",
            path,
        )
    if meta.get("plan_maturity") not in {"initial", "detailed"}:
        result.add(
            "plan-maturity-invalid",
            "plan_maturity must be initial or detailed",
            path,
        )
    if meta.get("spec_version") != program.spec_version:
        result.add(
            "plan-spec-version-drift",
            f"expected spec_version {program.spec_version}",
            path,
        )
    if not _same_path(_path(root, meta.get("program_plan")), program.path):
        result.add(
            "plan-program-link-invalid",
            "program_plan must point to the canonical program plan",
            path,
        )
    if not _same_path(_path(root, meta.get("plan_doc")), path):
        result.add("plan-self-link-invalid", "plan_doc must point to the current plan", path)
    for key in TRIO_KEYS:
        if not _same_path(_path(root, meta.get(key)), _path(root, entry.get(key))):
            result.add(
                "program-plan-link-drift",
                f"plan {key} must equal the program workstream link",
                path,
            )
    if expected_workstream_id in DELIVERY_WORKSTREAM_IDS and not _same_path(
        _path(root, meta.get("module_definition")),
        _path(root, entry.get("module_definition")),
    ):
        result.add(
            "plan-module-link-drift",
            "module_definition must equal the program workstream link",
            path,
        )
    hard_dependencies = _strings(meta.get("hard_dependencies"))
    if hard_dependencies != program.dependencies.get(expected_workstream_id, ()):
        result.add(
            "plan-dependency-drift",
            "hard_dependencies must equal the program dependency map",
            path,
        )
    soft_dependencies = _strings(meta.get("soft_dependencies"))
    if soft_dependencies != program.soft_dependencies.get(expected_workstream_id, ()):
        result.add(
            "plan-soft-dependency-drift",
            "soft_dependencies must equal the program dependency map",
            path,
        )
    plan_milestones = _strings(meta.get("release_milestones"))
    expected_milestones = _strings(entry.get("release_milestones"))
    if plan_milestones is None or expected_milestones is None or plan_milestones != expected_milestones:
        result.add(
            "plan-milestone-drift",
            f"release_milestones must equal {list(expected_milestones or ())}",
            path,
        )
    stage_ids = _strings(meta.get("stage_ids"))
    if stage_ids != STAGE_IDS:
        result.add(
            "plan-stage-set-invalid",
            f"stage_ids must equal {list(STAGE_IDS)}",
            path,
        )
    requirement_ids = _strings(meta.get("requirement_ids"), non_empty=True)
    if requirement_ids is None:
        result.add(
            "plan-requirements-invalid",
            "plan requires non-empty requirement_ids",
            path,
        )
        requirement_ids = ()
    unknown_requirements = sorted(set(requirement_ids) - set(program.requirement_ids))
    if unknown_requirements:
        result.add(
            "plan-requirements-unknown",
            f"unknown requirement IDs: {', '.join(unknown_requirements)}",
            path,
        )
    requirement_set = set(requirement_ids)
    if expected_workstream_id in DELIVERY_WORKSTREAM_IDS:
        primary_requirements = {
            requirement_id
            for requirement_id, allocation in program.requirement_allocations.items()
            if allocation.primary_workstream == expected_workstream_id
        }
        missing_primary = sorted(primary_requirements - requirement_set)
        if missing_primary:
            result.add(
                "plan-primary-requirements-missing",
                f"missing primary requirement IDs: {', '.join(missing_primary)}",
                path,
            )
        invalid_supporting = sorted(
            requirement_id
            for requirement_id in requirement_set - primary_requirements
            if expected_workstream_id
            not in program.requirement_allocations.get(
                requirement_id,
                RequirementAllocation(None, ()),
            ).contributing_workstreams
        )
        if invalid_supporting:
            result.add(
                "plan-supporting-requirements-invalid",
                "non-primary requirement IDs must explicitly list the workstream "
                f"as a contributor: {', '.join(invalid_supporting)}",
                path,
            )
    elif expected_workstream_id == "W14":
        expected_acceptance = {
            requirement_id
            for requirement_id, allocation in program.requirement_allocations.items()
            if requirement_id.startswith(("AC-", "V1-AC-"))
            and "W14" in allocation.contributing_workstreams
        }
        if expected_acceptance and requirement_set != expected_acceptance:
            result.add(
                "w14-acceptance-requirements-drift",
                "W14 requirement_ids must equal AC-001..AC-040 plus "
                "V1-AC-001..V1-AC-019 from its contributor allocation",
                path,
            )
    execution_mode = meta.get("execution_mode")
    if execution_mode != CANONICAL_EXECUTION_MODE:
        result.add(
            "plan-execution-mode-invalid",
            f"execution_mode must be {CANONICAL_EXECUTION_MODE}",
            path,
        )

    pack_path = _path(root, meta.get("prompt_pack_dir"))
    ledger_path = _path(root, meta.get("stage_ledger"))
    if pack_path is None or not pack_path.is_dir():
        result.add("prompt-pack-missing", "linked prompt_pack_dir is absent", path)
        return None
    if ledger_path is None or not ledger_path.is_file():
        result.add("stage-ledger-missing", "linked stage_ledger is absent", path)
        return None
    ledger = _validate_ledger(
        root,
        ledger_path,
        path,
        pack_path,
        expected_workstream_id,
        program.spec_version,
        result,
    )
    if ledger is None:
        return None
    if ledger.execution_mode != execution_mode:
        result.add(
            "plan-ledger-execution-mode-drift",
            "ledger execution_mode must equal plan execution_mode",
            ledger_path,
        )
    stage_requirement_set = {
        requirement_id
        for stage in ledger.stages.values()
        for requirement_id in stage.requirement_ids
    }
    if stage_requirement_set != requirement_set:
        missing = sorted(requirement_set - stage_requirement_set)
        extra = sorted(stage_requirement_set - requirement_set)
        result.add(
            "plan-stage-requirement-coverage-drift",
            "the union of S00-S06 requirement_ids must equal the plan requirement set; "
            f"missing={missing}, extra={extra}",
            ledger_path,
        )

    expected_prompts = {
        stage.prompt_path.resolve(strict=False): stage
        for stage in ledger.stages.values()
        if stage.prompt_path is not None
    }
    actual_prompts = {
        prompt.resolve(strict=False): prompt
        for prompt in pack_path.glob("S[0-9][0-9]*-*.md")
        if prompt.is_file()
    }
    missing_prompts = sorted(str(path) for path in set(expected_prompts) - set(actual_prompts))
    extra_prompts = sorted(str(path) for path in set(actual_prompts) - set(expected_prompts))
    if missing_prompts:
        result.add(
            "prompt-pack-stage-missing",
            f"missing prompts: {', '.join(missing_prompts)}",
            pack_path,
        )
    if extra_prompts:
        result.add(
            "prompt-pack-stage-extra",
            f"unregistered prompts: {', '.join(extra_prompts)}",
            pack_path,
        )
    branch_policies: list[str] = []
    for resolved_prompt, stage in expected_prompts.items():
        prompt = actual_prompts.get(resolved_prompt)
        if prompt is None:
            continue
        policy = _validate_prompt(
            root,
            prompt,
            path,
            pack_path,
            ledger,
            expected_workstream_id,
            frozenset(requirement_ids),
            program.spec_version,
            stage,
            result,
        )
        if policy is not None and stage.prompt_readiness == "executable":
            branch_policies.append(json.dumps(policy, ensure_ascii=False, sort_keys=True))
    if len(set(branch_policies)) > 1:
        result.add(
            "prompt-pack-branch-policy-drift",
            "all executable prompts in a pack must share one branch policy",
            pack_path,
        )
    return ledger


def _validate_registry(
    root: Path,
    program: ProgramRecord,
    ledgers: dict[str, LedgerRecord],
    result: CheckResult,
) -> None:
    registry = root / ".codex/PLANS.md"
    parsed = _read_frontmatter(registry, result, code="plans-registry-frontmatter-invalid")
    if parsed is None:
        return
    meta, _ = parsed
    if meta.get("registry_schema_version") != 1:
        result.add(
            "plans-registry-schema-invalid",
            "PLANS registry requires registry_schema_version=1",
            registry,
        )
    if meta.get("execution_mode") != CANONICAL_EXECUTION_MODE:
        result.add(
            "plans-registry-execution-mode-invalid",
            f"PLANS execution_mode must be {CANONICAL_EXECUTION_MODE}",
            registry,
        )
    if not _same_path(_path(root, meta.get("program_plan")), program.path):
        result.add(
            "plans-registry-program-link-invalid",
            "PLANS program_plan must point to the canonical program plan",
            registry,
        )
    raw_active = _sequence(meta.get("active_workstreams"))
    active: dict[str, dict[str, object]] = {}
    if raw_active is None:
        result.add(
            "plans-registry-active-invalid",
            "active_workstreams must be a list",
            registry,
        )
        raw_active = []
    for raw_item in raw_active:
        item = _mapping(raw_item)
        workstream_id = item.get("workstream_id") if item is not None else None
        if item is None or not isinstance(workstream_id, str):
            result.add(
                "plans-registry-entry-invalid",
                "active workstream entry requires workstream_id",
                registry,
            )
            continue
        if workstream_id in active:
            result.add(
                "plans-registry-entry-duplicate",
                f"duplicate active workstream {workstream_id}",
                registry,
            )
            continue
        if "current_stage" in item:
            result.add(
                "plans-registry-current-stage-forbidden",
                "current_stage belongs only in the stage ledger",
                registry,
            )
        active[workstream_id] = item
    expected_active = {
        workstream_id
        for workstream_id, ledger in ledgers.items()
        if ledger.status in {"active", "blocked"}
    }
    if set(active) != expected_active:
        result.add(
            "plans-registry-active-drift",
            "active_workstreams must equal active/blocked ledgers; "
            f"expected={sorted(expected_active)}, actual={sorted(active)}",
            registry,
        )
    for workstream_id, item in active.items():
        entry = program.workstreams.get(workstream_id)
        if entry is None:
            result.add(
                "plans-registry-entry-unknown",
                f"unknown active workstream {workstream_id}",
                registry,
            )
            continue
        for key in TRIO_KEYS:
            if not _same_path(_path(root, item.get(key)), _path(root, entry.get(key))):
                result.add(
                    "plans-registry-link-drift",
                    f"{workstream_id} {key} must equal the program link",
                    registry,
                )


def _validate_orphan_packs(
    root: Path,
    known_packs: Iterable[Path],
    result: CheckResult,
) -> None:
    generated = root / ".codex/agents/generated"
    if not generated.is_dir():
        return
    known = {path.resolve(strict=False) for path in known_packs}
    for item in generated.iterdir():
        if item.is_dir() and item.resolve(strict=False) not in known:
            result.add("orphan-prompt-pack", "prompt pack has no linked plan", item)


def _validate_forbidden_coordination_files(root: Path, result: CheckResult) -> None:
    candidates = [root / "GOAL.md"]
    for coordination_root in (root / ".codex", root / "docs"):
        if coordination_root.is_dir():
            candidates.extend(coordination_root.rglob("GOAL.md"))
    for candidate in candidates:
        if candidate.is_file():
            result.add(
                "forbidden-coordination-source",
                "GOAL.md is forbidden; Codex Goal mode uses the staged trio only",
                candidate,
            )


def check(root: Path, plans: Iterable[Path] | None = None) -> CheckResult:
    result = CheckResult("validate_staged_workstream")
    template_paths = [
        root / ".codex/agents/plan_template.md",
        root / ".codex/agents/prompt_template.md",
        root / ".codex/agents/stage_execution_ledger_template.md",
        root / ".codex/agents/iteration_report_template.md",
    ]
    for path in template_paths:
        require_file(path, result, "staged-template-missing")
    _validate_forbidden_coordination_files(root, result)
    if result.findings:
        return result

    programs, discovered_plans = _discover_artifacts(root)
    explicitly_selected = [root / item for item in plans] if plans else []
    if len(programs) > 1:
        result.add(
            "program-plan-duplicate",
            "exactly one program plan is allowed",
            root / "docs/architecture",
        )
        return result
    if not programs:
        for plan in explicitly_selected:
            if not require_file(plan, result, "plan-missing"):
                continue
            result.add(
                "program-plan-missing",
                "schema-v1 workstream plans require one canonical program plan",
                plan,
            )
        if discovered_plans:
            result.add(
                "program-plan-missing",
                "workstream plans exist without a canonical program plan",
                discovered_plans[0],
            )
        _validate_orphan_packs(root, (), result)
        result.details.update(workstreams=0, program_plans=0)
        return result

    blueprint = _blueprint_contract(root, result)
    if blueprint is None:
        return result
    expected_spec_version, expected_requirement_ids = blueprint
    program = _validate_program(
        root,
        programs[0],
        expected_spec_version,
        expected_requirement_ids,
        result,
    )
    if program is None:
        return result

    discovered_by_id: dict[str, Path] = {}
    for plan in discovered_plans:
        parsed = _read_frontmatter(plan, result, code="plan-frontmatter-invalid")
        if parsed is None:
            continue
        meta, _ = parsed
        workstream_id = meta.get("workstream_id")
        if not isinstance(workstream_id, str):
            result.add("plan-workstream-id-invalid", "workstream_id is required", plan)
            continue
        if workstream_id in discovered_by_id:
            result.add(
                "plan-workstream-id-duplicate",
                f"duplicate plan for {workstream_id}",
                plan,
            )
            continue
        discovered_by_id[workstream_id] = plan

    ledgers: dict[str, LedgerRecord] = {}
    known_packs: list[Path] = []
    for workstream_id in STAGED_WORKSTREAM_IDS:
        entry = program.workstreams.get(workstream_id)
        if entry is None:
            continue
        expected_plan = _path(root, entry.get("plan_doc"))
        discovered_plan = discovered_by_id.get(workstream_id)
        if expected_plan is None or not expected_plan.is_file():
            result.add(
                "plan-missing",
                f"{workstream_id} plan_doc is absent",
                program.path,
            )
            continue
        if not _same_path(expected_plan, discovered_plan):
            result.add(
                "program-plan-discovery-drift",
                f"{workstream_id} program link does not identify its unique workstream plan",
                expected_plan,
            )
        pack = _path(root, entry.get("prompt_pack_dir"))
        if pack is not None:
            known_packs.append(pack)
        ledger = _validate_plan(
            root,
            expected_plan,
            program,
            entry,
            workstream_id,
            result,
        )
        if ledger is not None:
            ledgers[workstream_id] = ledger
    extra_plan_ids = sorted(set(discovered_by_id) - set(STAGED_WORKSTREAM_IDS))
    if extra_plan_ids:
        result.add(
            "plan-workstream-set-invalid",
            f"unexpected workstream plan IDs: {', '.join(extra_plan_ids)}",
            root / "docs/architecture",
        )
    _validate_orphan_packs(root, known_packs, result)
    _validate_registry(root, program, ledgers, result)
    result.details.update(
        program_plans=1,
        workstreams=len(ledgers),
        expected_workstreams=len(STAGED_WORKSTREAM_IDS),
        active_workstreams=sorted(
            workstream_id
            for workstream_id, ledger in ledgers.items()
            if ledger.status in {"active", "blocked"}
        ),
        milestone_closures={
            milestone_id: sorted(workstreams)
            for milestone_id, workstreams in program.milestone_closures.items()
        },
        requirement_allocations=len(expected_requirement_ids),
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the staged program, plans, prompt packs, ledgers, and registry"
    )
    add_common_arguments(parser)
    parser.add_argument("plans", type=Path, nargs="*")
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.plans or None), args.json)


if __name__ == "__main__":
    main_guard(cli)
