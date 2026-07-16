from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, Sequence

from .core import (
    CheckResult,
    add_common_arguments,
    json_object,
    main_guard,
    parse_frontmatter,
    render_result,
    require_file,
    string_list,
)


TRIO_KEYS = ("plan_doc", "prompt_pack_dir", "stage_ledger")
ALLOWED_STATUSES = {"pending", "in_progress", "accepted", "blocked", "skipped", "superseded"}
CYRILLIC = re.compile(r"[\u0400-\u04FF]")


def _path(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value.strip() or "<" in value:
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    return root / relative


def _validate_ledger(root: Path, ledger: Path, result: CheckResult) -> None:
    try:
        meta, body = parse_frontmatter(ledger)
    except ValueError as exc:
        result.add("ledger-frontmatter-invalid", str(exc), ledger)
        return
    if CYRILLIC.search(ledger.read_text(encoding="utf-8")):
        result.add(
            "staged-artifact-language-invalid",
            "stage ledgers and evidence must be written in English",
            ledger,
        )
    for key in TRIO_KEYS:
        target = _path(root, meta.get(key))
        if target is None or not target.exists():
            result.add("staged-trio-broken", f"{key} is missing or unresolved", ledger)
    try:
        allowed = string_list(meta.get("allowed_stage_statuses"), "allowed_stage_statuses")
    except ValueError:
        allowed = []
    if set(allowed) != ALLOWED_STATUSES:
        result.add(
            "ledger-status-contract-invalid", "allowed_stage_statuses is not canonical", ledger
        )
    current = str(meta.get("current_stage", ""))
    if not re.fullmatch(r"[0-9]{2}[A-Z]?", current):
        result.add(
            "ledger-current-stage-invalid", "current_stage must be a stable stage ID", ledger
        )
    if "GOAL.md" in body:
        result.add("forbidden-coordination-source", "ledger references forbidden GOAL.md", ledger)


def _validate_prompt(root: Path, prompt: Path, result: CheckResult) -> None:
    try:
        meta, _ = parse_frontmatter(prompt)
    except ValueError as exc:
        result.add("prompt-frontmatter-invalid", str(exc), prompt)
        return
    if CYRILLIC.search(prompt.read_text(encoding="utf-8")):
        result.add(
            "staged-artifact-language-invalid",
            "prompt-pack artifacts must be written in English",
            prompt,
        )
    try:
        execution = json_object(meta.get("prompt_pack_execution"), "prompt_pack_execution")
    except ValueError:
        execution = {}
    if execution.get("enabled") is not True:
        result.add(
            "staged-prompt-disabled", "staged prompt must enable prompt_pack_execution", prompt
        )
        return
    for key in TRIO_KEYS:
        target = _path(root, execution.get(key))
        if target is None or not target.exists():
            result.add("staged-trio-broken", f"prompt {key} is missing or unresolved", prompt)
    try:
        json_object(execution.get("required_source_hashes"), "required_source_hashes")
    except ValueError:
        result.add("source-hash-gate-missing", "required_source_hashes must be a mapping", prompt)
    try:
        policy = json_object(execution.get("branch_policy"), "branch_policy")
    except ValueError:
        policy = {}
    if policy.get("per_stage_branches") != "forbidden":
        result.add("branch-policy-invalid", "per-stage branches must be forbidden", prompt)


def check(root: Path, plans: Iterable[Path] | None = None) -> CheckResult:
    result = CheckResult("validate_staged_workstream")
    template_paths = [
        root / ".codex/agents/prompt_template.md",
        root / ".codex/agents/stage_execution_ledger_template.md",
        root / ".codex/agents/iteration_report_template.md",
    ]
    for path in template_paths:
        require_file(path, result, "staged-template-missing")
    if result.findings:
        return result
    selected = [root / item for item in plans] if plans else []
    if not selected:
        for path in (root / "docs/architecture").rglob("*.md"):
            try:
                meta, _ = parse_frontmatter(path)
            except ValueError:
                continue
            if all(key in meta for key in TRIO_KEYS):
                selected.append(path)
    validated = 0
    for plan in selected:
        if not require_file(plan, result, "plan-missing"):
            continue
        try:
            meta, _ = parse_frontmatter(plan)
        except ValueError as exc:
            result.add("plan-frontmatter-invalid", str(exc), plan)
            continue
        validated += 1
        targets = {key: _path(root, meta.get(key)) for key in TRIO_KEYS}
        if targets["plan_doc"] is None or targets["plan_doc"].resolve() != plan.resolve():
            result.add("plan-self-link-invalid", "plan_doc must point to the current plan", plan)
        pack = targets["prompt_pack_dir"]
        ledger = targets["stage_ledger"]
        if pack is None or not pack.is_dir():
            result.add("prompt-pack-missing", "linked prompt_pack_dir is absent", plan)
        else:
            prompts = sorted(pack.glob("[0-9][0-9]*-*.md"))
            if not prompts:
                result.add("prompt-pack-empty", "prompt pack has no stage prompts", pack)
            for prompt in prompts:
                _validate_prompt(root, prompt, result)
        if ledger is None or not ledger.is_file():
            result.add("stage-ledger-missing", "linked stage_ledger is absent", plan)
        else:
            _validate_ledger(root, ledger, result)
    generated = root / ".codex/agents/generated"
    if generated.is_dir():
        known_packs: set[Path] = set()
        for plan in selected:
            if not plan.is_file():
                continue
            try:
                meta, _ = parse_frontmatter(plan)
            except ValueError:
                continue
            pack = _path(root, meta.get("prompt_pack_dir"))
            if pack is not None:
                known_packs.add(pack.resolve())
        for item in generated.iterdir():
            if item.is_dir() and item.resolve() not in known_packs:
                result.add("orphan-prompt-pack", "prompt pack has no linked plan", item)
    result.details["workstreams"] = validated
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate plan + prompt pack + stage ledger triads"
    )
    add_common_arguments(parser)
    parser.add_argument("plans", type=Path, nargs="*")
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.plans or None), args.json)


if __name__ == "__main__":
    main_guard(cli)
