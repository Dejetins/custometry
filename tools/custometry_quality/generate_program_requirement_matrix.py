from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path
from typing import Any, Sequence, cast

from .core import (
    CheckResult,
    add_common_arguments,
    canonical_json,
    json_object,
    load_json,
    main_guard,
    render_result,
    require_file,
    sha256_file,
    string_list,
    write_or_check,
)


RANGE_SELECTOR = re.compile(
    r"^(?P<prefix>[A-Z][A-Z0-9_-]*-)(?P<start>[0-9]{3})\.\."
    r"(?P=prefix)(?P<end>[0-9]{3})$"
)
EXACT_SELECTOR = re.compile(r"^[A-Z][A-Z0-9_-]*-[0-9]{3}$")
FAMILY_SELECTOR = re.compile(r"^(?P<prefix>[A-Z][A-Z0-9_-]*)-\*$")


def _selector_ids(selector: str, known_ids: set[str]) -> set[str]:
    family = FAMILY_SELECTOR.fullmatch(selector)
    if family:
        prefix = f"{family.group('prefix')}-"
        return {identifier for identifier in known_ids if identifier.startswith(prefix)}
    interval = RANGE_SELECTOR.fullmatch(selector)
    if interval:
        start = int(interval.group("start"))
        end = int(interval.group("end"))
        if end < start:
            raise ValueError(f"selector range is descending: {selector}")
        return {
            f"{interval.group('prefix')}{number:03d}" for number in range(start, end + 1)
        }
    if EXACT_SELECTOR.fullmatch(selector):
        return {selector}
    raise ValueError(f"unsupported selector: {selector}")


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _dependency_closure(
    workstream: str,
    dependencies: dict[str, tuple[str, ...]],
    *,
    visiting: tuple[str, ...] = (),
) -> set[str]:
    if workstream in visiting:
        cycle = " -> ".join((*visiting, workstream))
        raise ValueError(f"workstream dependency cycle: {cycle}")
    closure = {workstream}
    for dependency in dependencies.get(workstream, ()):
        closure.update(
            _dependency_closure(
                dependency,
                dependencies,
                visiting=(*visiting, workstream),
            )
        )
    return closure


def build_matrix(index: dict[str, Any], routing: dict[str, Any]) -> dict[str, Any]:
    requirements_raw = index.get("requirements")
    if not isinstance(requirements_raw, list):
        raise ValueError("requirement index requirements must be a list")
    requirements: list[dict[str, Any]] = []
    for position, item_value in enumerate(cast(list[object], requirements_raw)):
        if not isinstance(item_value, dict):
            raise ValueError(f"requirement index item {position} must be an object")
        item = cast(dict[str, Any], item_value)
        identifier = _string(item.get("id"), f"requirements[{position}].id")
        family = _string(item.get("family"), f"requirements[{position}].family")
        requirements.append({**item, "id": identifier, "family": family})
    identifiers = [item["id"] for item in requirements]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("requirement index contains duplicate IDs")
    known_ids = set(identifiers)

    workstreams = json_object(routing.get("workstreams"), "workstreams")
    milestones = set(string_list(routing.get("milestones"), "milestones", non_empty=True))
    terminal_milestones = json_object(
        routing.get("terminal_milestones"), "terminal_milestones"
    )
    if set(terminal_milestones) != milestones:
        missing_terminals = sorted(milestones - set(terminal_milestones))
        extra_terminals = sorted(set(terminal_milestones) - milestones)
        details: list[str] = []
        if missing_terminals:
            details.append(f"missing: {', '.join(missing_terminals)}")
        if extra_terminals:
            details.append(f"extra: {', '.join(extra_terminals)}")
        raise ValueError(
            "terminal milestones must cover the milestone catalog exactly; "
            + "; ".join(details)
        )
    unknown_terminal_workstreams = sorted(
        {
            _string(value, f"terminal_milestones.{milestone}")
            for milestone, value in terminal_milestones.items()
        }
        - set(workstreams)
    )
    if unknown_terminal_workstreams:
        raise ValueError(
            "terminal milestones reference unknown workstreams: "
            + ", ".join(unknown_terminal_workstreams)
        )
    milestone_terminal_stages = json_object(
        routing.get("milestone_terminal_stages"), "milestone_terminal_stages"
    )
    if set(milestone_terminal_stages) != milestones:
        missing_terminal_stages = sorted(milestones - set(milestone_terminal_stages))
        extra_terminal_stages = sorted(set(milestone_terminal_stages) - milestones)
        details: list[str] = []
        if missing_terminal_stages:
            details.append(f"missing: {', '.join(missing_terminal_stages)}")
        if extra_terminal_stages:
            details.append(f"extra: {', '.join(extra_terminal_stages)}")
        raise ValueError(
            "milestone terminal stages must cover the milestone catalog exactly; "
            + "; ".join(details)
        )
    allowed_terminal_stages = {"foundation_proof"} | {
        f"S{number:02d}" for number in range(7)
    }
    invalid_terminal_stages = sorted(
        {
            _string(value, f"milestone_terminal_stages.{milestone}")
            for milestone, value in milestone_terminal_stages.items()
        }
        - allowed_terminal_stages
    )
    if invalid_terminal_stages:
        raise ValueError(
            "milestone terminal stages are invalid: "
            + ", ".join(invalid_terminal_stages)
        )
    workstream_release_milestones = json_object(
        routing.get("workstream_release_milestones"),
        "workstream_release_milestones",
    )
    if set(workstream_release_milestones) != set(workstreams):
        missing_workstreams = sorted(set(workstreams) - set(workstream_release_milestones))
        extra_workstreams = sorted(set(workstream_release_milestones) - set(workstreams))
        details: list[str] = []
        if missing_workstreams:
            details.append(f"missing: {', '.join(missing_workstreams)}")
        if extra_workstreams:
            details.append(f"extra: {', '.join(extra_workstreams)}")
        raise ValueError(
            "workstream release milestones must cover the workstream catalog exactly; "
            + "; ".join(details)
        )
    for workstream, raw_milestones in workstream_release_milestones.items():
        release_milestones = string_list(
            raw_milestones,
            f"workstream_release_milestones.{workstream}",
            non_empty=True,
        )
        unknown_milestones = sorted(set(release_milestones) - milestones)
        if unknown_milestones:
            raise ValueError(
                f"workstream {workstream} references unknown release milestones: "
                + ", ".join(unknown_milestones)
            )
    workstream_dependencies = json_object(
        routing.get("workstream_dependencies"), "workstream_dependencies"
    )
    if set(workstream_dependencies) != set(workstreams):
        missing_workstreams = sorted(set(workstreams) - set(workstream_dependencies))
        extra_workstreams = sorted(set(workstream_dependencies) - set(workstreams))
        details: list[str] = []
        if missing_workstreams:
            details.append(f"missing: {', '.join(missing_workstreams)}")
        if extra_workstreams:
            details.append(f"extra: {', '.join(extra_workstreams)}")
        raise ValueError(
            "workstream dependencies must cover the workstream catalog exactly; "
            + "; ".join(details)
        )
    hard_dependencies_by_workstream: dict[str, tuple[str, ...]] = {}
    for workstream, raw_dependencies in workstream_dependencies.items():
        dependencies = json_object(
            raw_dependencies, f"workstream_dependencies.{workstream}"
        )
        hard = string_list(
            dependencies.get("hard", []),
            f"workstream_dependencies.{workstream}.hard",
        )
        soft = string_list(
            dependencies.get("soft", []),
            f"workstream_dependencies.{workstream}.soft",
        )
        if len(hard) != len(set(hard)) or len(soft) != len(set(soft)):
            raise ValueError(f"workstream {workstream} has duplicate dependencies")
        invalid_dependencies = sorted(
            (set(hard) | set(soft)) - set(workstreams)
        )
        if invalid_dependencies:
            raise ValueError(
                f"workstream {workstream} references unknown dependencies: "
                + ", ".join(invalid_dependencies)
            )
        if workstream in hard or workstream in soft or set(hard) & set(soft):
            raise ValueError(f"workstream {workstream} has an invalid dependency set")
        hard_dependencies_by_workstream[workstream] = tuple(hard)
    milestone_closures = {
        milestone: _dependency_closure(
            _string(
                terminal_milestones.get(milestone),
                f"terminal_milestones.{milestone}",
            ),
            hard_dependencies_by_workstream,
        )
        for milestone in milestones
    }
    release_scopes = set(
        string_list(routing.get("release_scopes"), "release_scopes", non_empty=True)
    )
    evidence_types = set(
        string_list(routing.get("evidence_types"), "evidence_types", non_empty=True)
    )
    profiles = json_object(routing.get("profiles"), "profiles")
    rules_raw = routing.get("rules")
    if not isinstance(rules_raw, list) or not rules_raw:
        raise ValueError("routing rules must be a non-empty list")

    assignments: dict[str, dict[str, Any]] = {}
    selector_coverage: Counter[str] = Counter()
    for rule_number, raw_rule in enumerate(cast(list[object], rules_raw), 1):
        rule = json_object(raw_rule, f"rules[{rule_number}]")
        selectors = string_list(
            rule.get("selectors"), f"rules[{rule_number}].selectors", non_empty=True
        )
        profile_name = _string(rule.get("profile"), f"rules[{rule_number}].profile")
        profile = json_object(profiles.get(profile_name), f"profiles.{profile_name}")
        primary = _string(
            rule.get("primary_workstream"), f"rules[{rule_number}].primary_workstream"
        )
        if primary not in workstreams:
            raise ValueError(f"unknown primary workstream {primary} in rule {rule_number}")
        contributors = string_list(
            rule.get("contributing_workstreams", []),
            f"rules[{rule_number}].contributing_workstreams",
        )
        if primary in contributors or len(contributors) != len(set(contributors)):
            raise ValueError(f"invalid contributor set in rule {rule_number}")
        unknown_contributors = sorted(set(contributors) - set(workstreams))
        if unknown_contributors:
            raise ValueError(
                f"unknown contributors in rule {rule_number}: {', '.join(unknown_contributors)}"
            )
        milestone = _string(
            rule.get("first_required_milestone"),
            f"rules[{rule_number}].first_required_milestone",
        )
        if milestone not in milestones:
            raise ValueError(f"unknown milestone {milestone} in rule {rule_number}")
        if primary not in milestone_closures[milestone]:
            raise ValueError(
                f"primary workstream {primary} in rule {rule_number} cannot satisfy "
                f"first milestone {milestone}; "
                f"closure={sorted(milestone_closures[milestone])}"
            )
        release_scope = _string(
            rule.get("release_scope"), f"rules[{rule_number}].release_scope"
        )
        if release_scope not in release_scopes:
            raise ValueError(f"unknown release scope {release_scope} in rule {rule_number}")

        implementation_evidence = string_list(
            profile.get("implementation_evidence"),
            f"profiles.{profile_name}.implementation_evidence",
            non_empty=True,
        )
        acceptance_evidence = string_list(
            profile.get("acceptance_evidence"),
            f"profiles.{profile_name}.acceptance_evidence",
            non_empty=True,
        )
        unknown_evidence = sorted(
            (set(implementation_evidence) | set(acceptance_evidence)) - evidence_types
        )
        if unknown_evidence:
            raise ValueError(
                f"profile {profile_name} uses unknown evidence: {', '.join(unknown_evidence)}"
            )
        route = {
            "requirement_kind": _string(
                profile.get("requirement_kind"),
                f"profiles.{profile_name}.requirement_kind",
            ),
            "primary_workstream": primary,
            "contributing_workstreams": contributors,
            "first_required_milestone": milestone,
            "release_scope": release_scope,
            "implementation_evidence": implementation_evidence,
            "acceptance_evidence": acceptance_evidence,
            "decision_gate": rule.get("decision_gate"),
            "status": _string(rule.get("status", "allocated"), f"rules[{rule_number}].status"),
            "notes": _string(rule.get("notes", "Canonical primary allocation."), "notes"),
        }
        selected: set[str] = set()
        for selector in selectors:
            expanded = _selector_ids(selector, known_ids)
            unknown = expanded - known_ids
            if unknown:
                raise ValueError(
                    f"selector {selector} references unknown IDs: {', '.join(sorted(unknown))}"
                )
            if not expanded:
                raise ValueError(f"selector {selector} matched no requirement IDs")
            selected.update(expanded)
            selector_coverage[selector] += len(expanded)
        for identifier in sorted(selected):
            if identifier in assignments:
                raise ValueError(f"requirement {identifier} is routed more than once")
            assignments[identifier] = route

    missing = sorted(known_ids - assignments.keys())
    extra = sorted(assignments.keys() - known_ids)
    if missing or extra:
        messages: list[str] = []
        if missing:
            messages.append(f"missing: {', '.join(missing)}")
        if extra:
            messages.append(f"extra: {', '.join(extra)}")
        raise ValueError("routing coverage is not exact; " + "; ".join(messages))

    rows: list[dict[str, Any]] = []
    for item in requirements:
        route = assignments[item["id"]]
        occurrences = item.get("machine_occurrences")
        source_line = item.get("definition_line")
        if source_line is None and isinstance(occurrences, list) and occurrences:
            source_line = cast(list[Any], occurrences)[0]
        rows.append(
            {
                "requirement_id": item["id"],
                "family": item["family"],
                "requirement_kind": route["requirement_kind"],
                "source_document": index.get("source"),
                "source_line": source_line,
                "primary_workstream": route["primary_workstream"],
                "contributing_workstreams": route["contributing_workstreams"],
                "first_required_milestone": route["first_required_milestone"],
                "release_scope": route["release_scope"],
                "implementation_evidence": route["implementation_evidence"],
                "acceptance_evidence": route["acceptance_evidence"],
                "decision_gate": route["decision_gate"],
                "status": route["status"],
                "notes": route["notes"],
            }
        )
    owner_counts = Counter(row["primary_workstream"] for row in rows)
    return {
        "schema_version": 1,
        "document_family_id": index.get("document_family_id"),
        "spec_version": index.get("spec_version"),
        "requirement_index_source": "docs/generated/requirement-index.json",
        "routing_source": "docs/architecture/program/requirement-routing.json",
        "terminal_milestones": terminal_milestones,
        "milestone_terminal_stages": milestone_terminal_stages,
        "workstream_release_milestones": workstream_release_milestones,
        "workstream_dependencies": workstream_dependencies,
        "requirement_count": len(rows),
        "unique_requirement_count": len({row["requirement_id"] for row in rows}),
        "workstream_counts": dict(sorted(owner_counts.items())),
        "requirements": rows,
        "selector_coverage": dict(sorted(selector_coverage.items())),
    }


def check(
    root: Path,
    *,
    index_path: Path,
    routing_path: Path,
    output_path: Path,
    check_mode: bool,
) -> CheckResult:
    result = CheckResult("generate_program_requirement_matrix")
    index_file = root / index_path
    routing_file = root / routing_path
    output_file = root / output_path
    if not require_file(index_file, result) or not require_file(routing_file, result):
        return result
    try:
        index = load_json(index_file)
        routing = load_json(routing_file)
        matrix = build_matrix(index, routing)
    except ValueError as exc:
        result.add("program-requirement-routing-invalid", str(exc))
        return result
    matrix["requirement_index_sha256"] = sha256_file(index_file)
    matrix["routing_source_sha256"] = sha256_file(routing_file)
    write_or_check(output_file, canonical_json(matrix), check_mode, result)
    result.details["requirements"] = matrix["requirement_count"]
    result.details["unique_requirements"] = matrix["unique_requirement_count"]
    result.details["workstreams"] = len(matrix["workstream_counts"])
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate and validate the canonical program requirement matrix"
    )
    add_common_arguments(parser)
    parser.add_argument(
        "--index",
        type=Path,
        default=Path("docs/generated/requirement-index.json"),
    )
    parser.add_argument(
        "--routing",
        type=Path,
        default=Path("docs/architecture/program/requirement-routing.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/architecture/program/requirement-matrix.json"),
    )
    parser.add_argument("--check", action="store_true", help="fail when output is absent or stale")
    return parser


def cli(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = check(
        args.root.resolve(),
        index_path=args.index,
        routing_path=args.routing,
        output_path=args.output,
        check_mode=args.check,
    )
    return render_result(result, args.json)


if __name__ == "__main__":
    main_guard(cli)
