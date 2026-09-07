"""Read-only repository gate for canonical milestone journals and prompt bindings."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .core import CheckResult, add_common_arguments, main_guard, render_result
from .prompt_pack_validation import Invalid, Pack, Unavailable
from .stage_ledger import verify_capability, verify_receipt_history


def check(root: Path) -> CheckResult:
    result = CheckResult("validate_prompt_packs")
    ledgers = sorted((root / ".codex/delivery/ledgers").glob("*.md"))
    result.details["journals"] = len(ledgers)
    for ledger in ledgers:
        try:
            pack = Pack(root, ledger)
            if pack.data.get("claim_capability"):
                verify_capability(pack)
                verify_receipt_history(pack)
            for sid, row in pack.rows.items():
                if pack.data["ledger_status"] == "draft" and row["execution_allowed"]:
                    pack.entry(sid)
                if row["status"] == "accepted":
                    pack.satisfied(sid)
        except (Invalid, Unavailable, OSError, TypeError, ValueError, KeyError) as exc:
            result.add("prompt-pack-invalid", str(exc), ledger.relative_to(root))
    result.details["proof_boundary"] = (
        "artifact-structure-and-file-binding; no claims or stage execution"
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser)
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve()), args.json)


if __name__ == "__main__":
    main_guard(cli)
