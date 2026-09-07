#!/usr/bin/env python3
"""Repository snapshot of Prompt Manager's prompt-pack/v1 structural validator.

Source: prompt-manager/scripts/validate_pack.py, SHA-256:
bcb7ee44d67e0568bec7b26683d180c32b68766ba6eaf20df8271d951ffb1077
Adaptations: typed interface; in-memory candidate validation for atomic updates;
accepted plan/hash binding. Lifecycle and receipt schema remain prompt-pack/v1.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast


def field(value: Any, key: str, default: Any = None) -> Any:
    return value.get(key, default)


def is_object(value: Any) -> bool:
    return isinstance(value, dict)


def is_array(value: Any) -> bool:
    return isinstance(value, list)


class Invalid(ValueError):
    pass


class Unavailable(Exception):
    pass


def need(condition: object, message: str) -> None:
    if not condition:
        raise Invalid(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(text: str) -> dict[str, Any]:
    def bad_constant(value: str) -> None:
        raise Invalid(f"Non-JSON constant: {value}")

    try:
        result = json.loads(text, object_pairs_hook=unique_object, parse_constant=bad_constant)
    except json.JSONDecodeError as exc:
        raise Invalid(f"Invalid JSON at line {exc.lineno}, column {exc.colno}") from exc
    need(is_object(result), "Expected a JSON object")
    return result


def document(path: Path, marker: str = "", frontmatter: bool = False) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if frontmatter:
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
        need(match is not None, f"Missing JSON front matter: {path.name}")
        assert match is not None
        return parse_json(match.group(1))
    need(text.count(marker) == 1, f"Expected one {marker} marker in {path.name}")
    tail = text.split(marker, 1)[1]
    match = re.match(r"\s*```json\r?\n(.*?)\r?\n```(?:\r?\n|$)", tail, re.S)
    need(match is not None, f"Missing marked JSON block: {path.name}")
    assert match is not None
    return parse_json(match.group(1))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contract_digest(contract: dict[str, Any]) -> str:
    raw = json.dumps(contract, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    return hashlib.sha256(raw).hexdigest()


class Pack:
    def __init__(self, root: Path | str, ledger: Path | str, data: dict[str, Any] | None = None):
        self.root = Path(root).resolve(strict=True)
        need(self.root.is_dir(), "Root must be a directory")
        self.ledger = Path(ledger).resolve(strict=True)
        need(self.ledger.is_relative_to(self.root), "Ledger escapes declared root")
        self.base = self.ledger.parent
        self.data = (
            document(self.ledger, "<!-- prompt-pack-ledger:v1 -->") if data is None else data
        )
        if field(self.data, "schema_version") != "prompt-pack-ledger/v1":
            raise Unavailable("Unsupported ledger schema; resolve the selected profile")
        triad = field(self.data, "prompt_pack_execution")
        need(
            is_object(triad) and set(triad) == {"plan_doc", "prompt_pack_dir", "stage_ledger"},
            "Triad must have exactly three paths",
        )
        self.triad: dict[str, Path] = {key: self.path(value) for key, value in triad.items()}
        need(self.triad["stage_ledger"] == self.ledger, "Ledger self-link mismatch")
        need(self.triad["plan_doc"].is_file(), "Accepted plan is missing")
        need(self.triad["prompt_pack_dir"].is_dir(), "Prompt directory is missing")
        need(
            field(self.data, "execution_mode") in {"manual_sequential", "goal_driven"},
            "Invalid execution_mode",
        )
        need("current_stage" in self.data, "Missing current_stage field")
        need(
            field(self.data, "ledger_status")
            in {
                "draft",
                "active",
                "awaiting_input",
                "blocked",
                "completed",
                "archived",
                "superseded",
            },
            "Invalid ledger_status",
        )
        rows = field(self.data, "stages")
        need(is_array(rows) and bool(rows), "Stages must be a nonempty list")
        plan = document(self.triad["plan_doc"], frontmatter=True)
        need(field(plan, "planning_status") == "accepted", "Plan is not accepted")
        binding = field(self.data, "plan_binding")
        need(
            is_object(binding)
            and field(binding, "version") == field(plan, "version")
            and field(binding, "sha256") == digest(self.triad["plan_doc"]),
            "Stale ledger plan binding",
        )
        self.rows: dict[str, Any] = {}
        prompt_paths: set[Path] = set()
        for row in rows:
            need(is_object(row), "Stage row must be an object")
            c = field(row, "contract")
            need(is_object(c), "Missing stage contract")
            for key in (
                "id",
                "title",
                "prompt_path",
                "report_path",
                "proof_boundary",
                "receipt_dir",
            ):
                need(nonempty(field(c, key)), f"Missing stage contract field: {key}")
            sid = c["id"]
            need(sid not in self.rows, "Duplicate stage ID")
            self.rows[sid] = row
            for key in ("depends_on", "expected_touches", "acceptance_criteria"):
                values = field(c, key)
                need(is_array(values) and all(nonempty(x) for x in values), f"Invalid {key}: {sid}")
                need(len(values) == len(set(values)), f"Duplicate {key}: {sid}")
            for touch in c["expected_touches"]:
                if touch.startswith("zone:"):
                    zone = touch[5:].strip()
                    need(
                        nonempty(zone) and "/" not in zone and "\\" not in zone,
                        f"Named touch zone must not contain a path: {sid}",
                    )
                else:
                    self.path(touch)
            need(bool(c["acceptance_criteria"]), f"No acceptance criteria: {sid}")
            v = field(c, "validation")
            need(
                is_object(v) and nonempty(field(v, "profile")), f"Missing validation profile: {sid}"
            )
            need(
                isinstance(field(v, "checks"), list)
                and bool(v["checks"])
                and all(nonempty(x) for x in v["checks"]),
                f"Missing validation checks: {sid}",
            )
            need(
                type(field(v, "requires_user_acceptance")) is bool,
                f"Invalid acceptance flag: {sid}",
            )
            inputs = field(c, "entry_inputs")
            need(is_array(inputs), f"Missing entry_inputs: {sid}")
            for item in inputs:
                need(
                    is_object(item) and set(item) == {"path", "producer_stage"},
                    f"Invalid entry input: {sid}",
                )
                self.path(item["path"])
                need(
                    item["producer_stage"] is None or nonempty(item["producer_stage"]),
                    f"Invalid producer_stage: {sid}",
                )
            prompt = self.path(c["prompt_path"])
            need(
                prompt.is_relative_to(self.triad["prompt_pack_dir"]) and prompt.suffix == ".md",
                f"Prompt outside pack or not Markdown: {sid}",
            )
            need(prompt not in prompt_paths, "Two stages share one prompt")
            prompt_paths.add(prompt)
            self.path(c["report_path"])
            self.path(c["receipt_dir"])
            front = document(prompt, frontmatter=True)
            need(
                field(front, "schema_version") == "stage-prompt/v1",
                f"Unsupported prompt schema: {sid}",
            )
            pt = field(front, "prompt_pack_execution")
            need(is_object(pt) and set(pt) == set(triad), f"Prompt triad missing: {sid}")
            need(nonempty(pt["stage_ledger"]), f"Missing bootstrap ledger path: {sid}")
            resolved_triad = {
                key: self.path(value) for key, value in pt.items() if key != "stage_ledger"
            }
            resolved_triad["stage_ledger"] = (prompt.parent / pt["stage_ledger"]).resolve()
            need(resolved_triad == self.triad, f"Prompt triad mismatch: {sid}")
            need(field(front, "plan_binding") == binding, f"Stale prompt plan binding: {sid}")
            need(field(front, "stage_contract") == c, f"Prompt/ledger contract mismatch: {sid}")
            need(
                field(row, "status")
                in {
                    "pending",
                    "in_progress",
                    "needs_input",
                    "accepted",
                    "blocked",
                    "skipped",
                    "superseded",
                },
                f"Invalid row status: {sid}",
            )
            for key in ("execution_allowed", "current_authority"):
                need(type(field(row, key)) is bool, f"Invalid {key}: {sid}")
            for key in ("executor_claim", "claimed_at", "transition_receipt", "decision_packet"):
                need(key in row, f"Missing row field {key}: {sid}")
            packet = row["decision_packet"]
            if packet is not None:
                need(
                    is_object(packet)
                    and nonempty(field(packet, "question"))
                    and nonempty(field(packet, "resume_condition"))
                    and "resolution_evidence" in packet,
                    f"Invalid decision packet: {sid}",
                )
                if packet["resolution_evidence"] is not None:
                    need(
                        self.path(packet["resolution_evidence"]).is_file(),
                        f"Decision resolution evidence missing: {sid}",
                    )
                else:
                    need(
                        not row["execution_allowed"],
                        f"Unresolved decision marked executable: {sid}",
                    )
            if row["status"] == "pending":
                need(
                    row["executor_claim"] is None and row["claimed_at"] is None,
                    f"Pending row already claimed: {sid}",
                )
            if row["status"] in {"in_progress", "needs_input"}:
                need(
                    nonempty(row["executor_claim"]) and nonempty(row["claimed_at"]),
                    f"Executing row lacks claim: {sid}",
                )
            if row["status"] == "needs_input":
                need(packet is not None, f"needs_input lacks decision packet: {sid}")
        artifacts = [
            self.ledger,
            self.triad["plan_doc"],
            *prompt_paths,
            *(self.path(row["contract"]["report_path"]) for row in self.rows.values()),
        ]
        need(len(set(artifacts)) == len(artifacts), "Report or triad artifact paths collide")
        for i, first in enumerate(artifacts):
            for second in artifacts[i + 1 :]:
                need(
                    not first.is_relative_to(second) and not second.is_relative_to(first),
                    "A file artifact is also used as an artifact directory",
                )
        receipt_dirs = [self.path(row["contract"]["receipt_dir"]) for row in self.rows.values()]
        for i, directory in enumerate(receipt_dirs):
            for artifact in artifacts:
                need(
                    not artifact.is_relative_to(directory)
                    and not directory.is_relative_to(artifact),
                    "Receipt directory overlaps a protected artifact",
                )
            for other in receipt_dirs[i + 1 :]:
                need(
                    not directory.is_relative_to(other) and not other.is_relative_to(directory),
                    "Stage receipt directories must be disjoint",
                )
        for sid in self.rows:
            self.ancestors(sid)
            for item in self.rows[sid]["contract"]["entry_inputs"]:
                producer = item["producer_stage"]
                need(
                    producer is None or producer in self.ancestors(sid),
                    f"Input producer is not a dependency: {sid}",
                )
        status = self.data["ledger_status"]
        current = field(self.data, "current_stage")
        if status == "draft":
            need(current is None, "Draft must have current_stage=null")
            for sid, row in self.rows.items():
                need(
                    row["status"] == "pending"
                    and row["transition_receipt"] is None
                    and row["current_authority"],
                    f"Draft contains execution state: {sid}",
                )
                need(
                    not row["execution_allowed"] or not row["contract"]["depends_on"],
                    f"Draft enables a dependent stage: {sid}",
                )
            need(
                sum(row["execution_allowed"] for row in self.rows.values()) <= 1,
                "Draft has multiple enabled roots",
            )
        if status in {"active", "awaiting_input", "blocked"}:
            need(current in self.rows, "Ledger current_stage is missing")
        live = [
            sid for sid, row in self.rows.items() if row["status"] in {"in_progress", "needs_input"}
        ]
        need(len(live) <= 1 and (not live or live[0] == current), "Inconsistent current claim")
        if status == "awaiting_input":
            need(self.rows[current]["status"] == "needs_input", "awaiting_input row mismatch")
        if status == "active":
            need(
                not any(row["status"] == "needs_input" for row in self.rows.values()),
                "Active ledger contains needs_input",
            )
            need(
                self.rows[current]["status"] != "blocked",
                "Active ledger has a blocked current stage",
            )
        if status == "blocked":
            need(
                self.rows[current]["status"] == "blocked" and not live,
                "Blocked ledger row mismatch",
            )
        if status in {"completed", "archived", "superseded"}:
            need(not live, "Terminal ledger contains an executing row")
        if status == "completed":
            need(
                all(self.satisfied(sid) for sid in self.rows),
                "Completed ledger has an unsatisfied obligation",
            )

    def path(self, value: str) -> Path:
        need(nonempty(value), "Expected nonempty path")
        path = (self.base / value).resolve()
        need(path.is_relative_to(self.root), "Artifact path escapes declared root")
        return path

    def ancestors(self, sid: str, visiting: set[str] | None = None) -> set[str]:
        visiting = set() if visiting is None else visiting
        need(sid in self.rows, f"Unknown dependency: {sid}")
        need(sid not in visiting, "Dependency cycle")
        result: set[str] = set()
        for dep in self.rows[sid]["contract"]["depends_on"]:
            result.add(dep)
            result.update(self.ancestors(dep, visiting | {sid}))
        return result

    def replacement(
        self, sid: str, pending: bool = False, projected: frozenset[str] = frozenset()
    ) -> str:
        original = self.rows[sid]
        statuses = {"pending"} if pending else {"accepted", "superseded", "blocked"}
        named = field(original, "replacement_stage")
        candidates = [
            key
            for key, row in self.rows.items()
            if field(row, "replaces_stage") == sid
            and row["current_authority"]
            and (row["status"] in statuses or key in projected)
        ]
        if named is not None:
            need(named in self.rows and named != sid, f"Invalid named replacement: {sid}")
            need(not candidates or candidates == [named], f"Ambiguous replacement: {sid}")
            target = named
        else:
            need(len(candidates) == 1, f"No unique replacement: {sid}")
            target = candidates[0]
        replacement = self.rows[target]
        need(
            replacement["status"] in statuses or target in projected,
            f"Replacement is not an accepted path: {sid}",
        )
        if original["status"] == "blocked":
            need(
                field(replacement, "replaces_stage") == sid,
                f"Replacement does not name blocked row: {sid}",
            )
            evidence = field(replacement, "repair_evidence_ref")
            need(
                nonempty(evidence) and self.path(evidence).is_file(),
                f"Missing repair evidence: {sid}",
            )
        return target

    def accepted_replacement(
        self, sid: str, seen: frozenset[str] = frozenset(), projected: frozenset[str] = frozenset()
    ) -> bool:
        need(sid not in seen, "Replacement cycle")
        target = self.replacement(sid, projected=projected)
        row = self.rows[target]
        if target in projected:
            return row["current_authority"]
        if row["status"] == "accepted" and row["current_authority"]:
            return self.satisfied(target, seen=seen | {sid})
        if row["status"] in {"superseded", "blocked"} or (
            row["status"] == "accepted" and not row["current_authority"]
        ):
            return self.accepted_replacement(target, seen | {sid}, projected)
        return False

    def satisfied(
        self, sid: str, projected: frozenset[str] = frozenset(), seen: frozenset[str] = frozenset()
    ) -> bool:
        need(sid not in seen, "Replacement cycle")
        row = self.rows[sid]
        if sid in projected:
            return True
        if row["status"] == "accepted" and row["current_authority"]:
            ref = field(row, "transition_receipt")
            need(nonempty(ref), f"Accepted dependency lacks receipt: {sid}")
            self.receipt(self.path(ref), successor=False, expected_stage=sid)
            return True
        if row["status"] == "skipped":
            ref = field(row, "waiver_evidence")
            return row["current_authority"] and nonempty(ref) and self.path(ref).is_file()
        if row["status"] in {"superseded", "blocked"} or (
            row["status"] == "accepted" and not row["current_authority"]
        ):
            return self.accepted_replacement(sid, seen, projected)
        return False

    def entry(
        self,
        sid: str,
        projected: frozenset[str] = frozenset(),
        require_allowed: bool = True,
        executor: str | None = None,
    ) -> None:
        need(sid in self.rows, "Unknown entry stage")
        capability = field(self.data, "claim_capability")
        need(
            is_object(capability)
            and set(capability) == {"mechanism", "evidence"}
            and nonempty(field(capability, "mechanism")),
            "Entry lacks a resolved claim capability; keep the draft non-runnable",
        )
        self.binding(capability["evidence"])
        row = self.rows[sid]
        ledger_status = self.data["ledger_status"]
        current = self.data["current_stage"]
        need(row["current_authority"], "Entry is not current authority")
        packet = row["decision_packet"]
        need(
            packet is None or packet["resolution_evidence"] is not None, "Entry awaits owner input"
        )
        if row["status"] in {"needs_input", "in_progress"}:
            required_state = "awaiting_input" if row["status"] == "needs_input" else "active"
            need(ledger_status == required_state and current == sid, "Resume ledger/row mismatch")
            need(
                nonempty(executor) and executor == row["executor_claim"],
                "Resume requires --executor matching the existing claim; reconcile foreign/stale claims",
            )
        else:
            need(row["status"] == "pending", "Entry is not pending or resumable work")
            need(not require_allowed or row["execution_allowed"], "Entry is not allowed")
            if ledger_status == "draft":
                enabled = [key for key, value in self.rows.items() if value["execution_allowed"]]
                need(
                    enabled == [sid] and not row["contract"]["depends_on"],
                    "No unique initial entry",
                )
            elif ledger_status == "blocked":
                need(
                    self.replacement(current, pending=True) == sid,
                    "Entry is not the permitted repair replacement",
                )
            else:
                need(ledger_status == "active", "Ledger is not entry-eligible")
                live = [
                    key
                    for key, value in self.rows.items()
                    if value["status"] in {"in_progress", "needs_input"}
                ]
                need(
                    not live or all(key in projected for key in live),
                    "Another stage still owns the active claim",
                )
        for dep in row["contract"]["depends_on"]:
            need(self.satisfied(dep, projected), f"Unsatisfied dependency: {dep}")
        for item in row["contract"]["entry_inputs"]:
            need(self.path(item["path"]).is_file(), f"Missing live entry input: {sid}")

    def binding(self, ref: Any, expected: Path | None = None) -> None:
        need(is_object(ref) and set(ref) == {"path", "sha256"}, "Invalid file binding")
        path = self.path(ref["path"])
        need(expected is None or path == expected, "Receipt artifact identity mismatch")
        value = ref["sha256"]
        need(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value), "Invalid SHA-256")
        need(
            path.is_file() and digest(path) == value, "Receipt references missing or changed bytes"
        )

    def receipt(
        self, path: Path, successor: bool = True, expected_stage: str | None = None
    ) -> dict[str, Any]:
        data = document(path, "<!-- prompt-pack-receipt:v1 -->")
        need(
            field(data, "schema_version") == "prompt-pack-receipt/v1", "Unsupported receipt schema"
        )
        sid = field(data, "stage_id")
        need(
            sid in self.rows and (expected_stage is None or sid == expected_stage),
            "Receipt stage mismatch",
        )
        row = self.rows[sid]
        c = row["contract"]
        need(
            row["status"] in {"in_progress", "needs_input", "accepted"},
            "Receipt lacks executing/accepted row",
        )
        need(row["current_authority"], "Receipt stage is not current authority")
        for dep in c["depends_on"]:
            need(self.satisfied(dep), f"Receipt has an unsatisfied dependency: {dep}")
        need(
            path.resolve().is_relative_to(self.path(c["receipt_dir"])),
            "Receipt outside stage receipt_dir",
        )
        if row["status"] == "accepted":
            need(
                nonempty(row["transition_receipt"])
                and self.path(row["transition_receipt"]) == path.resolve(),
                "Receipt is not the accepted row's recorded receipt",
            )
        need(field(data, "stage_contract_sha256") == contract_digest(c), "Receipt contract changed")
        stamp = field(data, "created_at")
        need(nonempty(stamp) and stamp.endswith("Z"), "Receipt timestamp must be UTC")
        try:
            datetime.fromisoformat(stamp[:-1] + "+00:00")
        except ValueError as exc:
            raise Invalid("Invalid receipt timestamp") from exc
        for key, expected in (
            ("plan", self.triad["plan_doc"]),
            ("prompt", self.path(c["prompt_path"])),
            ("report", self.path(c["report_path"])),
        ):
            self.binding(field(data, key), expected)
        validation = field(data, "validation")
        need(
            is_object(validation)
            and field(validation, "result") == "pass"
            and field(validation, "profile") == c["validation"]["profile"],
            "Receipt validation profile/result mismatch",
        )
        evidence = field(validation, "evidence")
        need(is_array(evidence) and bool(evidence), "Receipt has no validation evidence")
        for item in evidence:
            self.binding(item)
        need("user_acceptance" in data, "Missing user_acceptance field")
        acceptance = data["user_acceptance"]
        if acceptance is not None:
            self.binding(acceptance)
        state = field(data, "status")
        need(state in {"ready", "review_ready"}, "Invalid receipt readiness status")
        if row["status"] == "accepted":
            need(state == "ready", "Accepted row must record ready evidence")
        required = c["validation"]["requires_user_acceptance"]
        if state == "ready":
            need(not required or acceptance is not None, "Required user acceptance missing")
        else:
            need(
                required and acceptance is None, "review_ready requires outstanding user acceptance"
            )
        need(type(field(data, "next_stage_allowed")) is bool, "Invalid next-stage allowance")
        need(nonempty(field(data, "handoff_reason")), "Missing handoff reason")
        need("next_stage" in data, "Missing next_stage field")
        nxt = data["next_stage"]
        if nxt is not None:
            need(
                is_object(nxt) and field(nxt, "id") in self.rows and nxt["id"] != sid,
                "Invalid next stage",
            )
            nc = self.rows[nxt["id"]]["contract"]
            self.binding(field(nxt, "prompt"), self.path(nc["prompt_path"]))
            need(
                field(nxt, "stage_contract_sha256") == contract_digest(nc),
                "Next-stage contract changed",
            )
        if data["next_stage_allowed"]:
            need(state == "ready" and nxt is not None, "Cannot allow absent/unready successor")
            if successor:
                assert nxt is not None
                self.entry(nxt["id"], projected=frozenset({sid}), require_allowed=False)
        if not successor:
            need(state == "ready", "Accepted dependency only has review_ready evidence")
        return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", required=True, help="Explicit common root of approved local artifact paths"
    )
    parser.add_argument("--ledger", required=True, help="Absolute ledger Markdown path")
    parser.add_argument("--check", choices=("draft", "entry", "receipt"), required=True)
    parser.add_argument("--stage")
    parser.add_argument("--receipt")
    parser.add_argument(
        "--executor",
        help="Existing claim ID for read-only resume preflight; never acquires a claim",
    )
    args = parser.parse_args(argv)
    try:
        need(
            args.check == "entry" or (args.stage is None and args.executor is None),
            "--stage and --executor are only valid for entry checks",
        )
        need(
            args.check == "receipt" or args.receipt is None,
            "--receipt is only valid for receipt checks",
        )
        pack = Pack(args.root, args.ledger)
        if args.check == "draft":
            need(
                pack.data["ledger_status"] == "draft",
                "Draft check cannot reclassify an activated ledger",
            )
        elif args.check == "entry":
            need(nonempty(args.stage), "Entry check requires --stage")
            pack.entry(cast(str, args.stage), executor=args.executor)
        else:
            need(nonempty(args.receipt), "Receipt check requires --receipt")
            pack.receipt(pack.path(cast(str, args.receipt)))
        result, exit_code, errors = "pass", 0, []
    except Invalid as exc:
        result, exit_code, errors = "fail", 1, [str(exc)]
    except (TypeError, KeyError, RecursionError):
        result, exit_code, errors = (
            "fail",
            1,
            ["Malformed field types, missing fields or excessive nesting"],
        )
    except (OSError, UnicodeError, Unavailable) as exc:
        result, exit_code, errors = "unavailable", 2, [str(exc)]
    print(
        json.dumps(
            {
                "status": result,
                "check": args.check,
                "errors": errors,
                "proof_boundary": "artifact-structure-and-file-binding",
            },
            ensure_ascii=False,
        )
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
