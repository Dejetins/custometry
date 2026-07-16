from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .core import (
    CheckResult,
    JsonValue,
    add_common_arguments,
    flatten_json,
    load_json,
    main_guard,
    render_result,
    require_file,
)


def check(root: Path, english: Path, russian: Path) -> CheckResult:
    result = CheckResult("check_i18n_parity")
    en_path, ru_path = root / english, root / russian
    if en_path.is_dir() and ru_path.is_dir():
        en_files = {path.relative_to(en_path) for path in en_path.rglob("*.json")}
        ru_files = {path.relative_to(ru_path) for path in ru_path.rglob("*.json")}
        for path in sorted(en_files - ru_files):
            result.add("russian-catalog-missing", path.as_posix(), ru_path)
        for path in sorted(ru_files - en_files):
            result.add("english-catalog-missing", path.as_posix(), en_path)
        shared = sorted(en_files & ru_files)
        if not shared:
            result.observed = False
            result.add("catalogs-missing", "no paired JSON catalogs found")
            return result
        en: dict[str, JsonValue] = {}
        ru: dict[str, JsonValue] = {}
        try:
            for relative in shared:
                prefix = relative.with_suffix("").as_posix().replace("/", ".")
                en.update(flatten_json(load_json(en_path / relative), prefix))
                ru.update(flatten_json(load_json(ru_path / relative), prefix))
        except ValueError as exc:
            result.add("catalog-invalid", str(exc))
            return result
    else:
        if not require_file(en_path, result) or not require_file(ru_path, result):
            return result
        try:
            en = flatten_json(load_json(en_path))
            ru = flatten_json(load_json(ru_path))
        except ValueError as exc:
            result.add("catalog-invalid", str(exc))
            return result
    for key in sorted(en.keys() - ru.keys()):
        result.add("russian-key-missing", key, ru_path)
    for key in sorted(ru.keys() - en.keys()):
        result.add("english-key-missing", key, en_path)
    for locale, catalog, path in (("en", en, en_path), ("ru", ru, ru_path)):
        for key, value in sorted(catalog.items()):
            if not isinstance(value, str) or not value.strip():
                result.add("catalog-value-invalid", f"{locale}:{key} must be a non-empty string", path)
    result.details.update(english_keys=len(en), russian_keys=len(ru))
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate complete en/ru localization parity")
    add_common_arguments(parser)
    parser.add_argument("--english", type=Path, default=Path("packages/localization/locales/en"))
    parser.add_argument("--russian", type=Path, default=Path("packages/localization/locales/ru"))
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.english, args.russian), args.json)


if __name__ == "__main__":
    main_guard(cli)
