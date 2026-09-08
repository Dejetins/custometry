#!/usr/bin/env python3
"""Bounded structural reader for the delivery v1 schema, never an installer.

The deliberately finite JSON Schema vocabulary is checked before use. S02/S04
own cross-record, archive, signature and runtime validation; this CLI reports
structural validity only. No third-party runtime or remote schema is loaded.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, cast

MAX_BYTES = 1048576
MAX_DEPTH = 32
KEYWORDS = {
    "$schema", "$defs", "$ref", "title", "type", "const", "enum", "anyOf",
    "properties", "required", "additionalProperties", "items", "minItems",
    "maxItems", "uniqueItems", "minimum", "maximum", "minLength", "maxLength", "pattern",
}


class InvalidDelivery(ValueError):
    """A stable, non-payload-bearing structural failure."""


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InvalidDelivery("DELIVERY_JSON_DUPLICATE")
        result[key] = value
    return result


def _depth(value: Any, level: int = 0) -> None:
    if level > MAX_DEPTH:
        raise InvalidDelivery("DELIVERY_LIMIT")
    if isinstance(value, dict):
        for key, child in cast(dict[str, Any], value).items():
            _depth(key, level + 1)
            _depth(child, level + 1)
    elif isinstance(value, list):
        for child in cast(list[Any], value):
            _depth(child, level + 1)
    elif isinstance(value, str) and (not value.isascii() or any(ord(c) < 32 for c in value)):
        raise InvalidDelivery("DELIVERY_JSON_STRING")
    elif isinstance(value, float):
        raise InvalidDelivery("DELIVERY_JSON_NUMBER")


def parse_json(raw: bytes, max_bytes: int = MAX_BYTES) -> Any:
    if len(raw) > max_bytes:
        raise InvalidDelivery("DELIVERY_LIMIT")
    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=_pairs)
        _depth(value)
        return value
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InvalidDelivery("DELIVERY_JSON_INVALID") from exc


def canonical_bytes(value: Any) -> bytes:
    _depth(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def check_schema(node: dict[str, Any], root: dict[str, Any]) -> None:
    if set(node) - KEYWORDS:
        raise InvalidDelivery("DELIVERY_SCHEMA_KEYWORD")
    if "$ref" in node:
        name = node["$ref"]
        if not isinstance(name, str) or not name.startswith("#/$defs/"):
            raise InvalidDelivery("DELIVERY_SCHEMA_REFERENCE")
        if name.removeprefix("#/$defs/") not in root.get("$defs", {}):
            raise InvalidDelivery("DELIVERY_SCHEMA_REFERENCE")
    if node.get("type") == "object":
        if node.get("additionalProperties") is not False:
            raise InvalidDelivery("DELIVERY_SCHEMA_OPEN_OBJECT")
        if set(node.get("required", [])) != set(node.get("properties", {})):
            raise InvalidDelivery("DELIVERY_SCHEMA_REQUIRED")
    for key in ("properties", "$defs"):
        for child in node.get(key, {}).values():
            check_schema(child, root)
    if "items" in node:
        check_schema(node["items"], root)
    for child in node.get("anyOf", []):
        check_schema(child, root)
    if "pattern" in node:
        re.compile(node["pattern"])


def validate(value: Any, node: dict[str, Any], root: dict[str, Any]) -> None:
    if "$ref" in node:
        validate(value, root["$defs"][node["$ref"].removeprefix("#/$defs/")], root)
        return
    if "const" in node and canonical_bytes(value) != canonical_bytes(node["const"]):
        raise InvalidDelivery("DELIVERY_SCHEMA_VALUE")
    if "enum" in node and canonical_bytes(value) not in [canonical_bytes(v) for v in node["enum"]]:
        raise InvalidDelivery("DELIVERY_SCHEMA_VALUE")
    if "anyOf" in node:
        for option in node["anyOf"]:
            try:
                validate(value, option, root)
                return
            except InvalidDelivery:
                pass
        raise InvalidDelivery("DELIVERY_SCHEMA_VALUE")
    kind = node.get("type")
    expected = {"object": dict, "array": list, "string": str, "integer": int,
                "boolean": bool, "null": type(None)}
    if kind is not None and type(value) is not expected[kind]:
        raise InvalidDelivery("DELIVERY_SCHEMA_TYPE")
    if kind == "object":
        value = cast(dict[str, Any], value)
        if set(value) != set(node["required"]):
            raise InvalidDelivery("DELIVERY_SCHEMA_FIELDS")
        for key, child in cast(dict[str, Any], value).items():
            validate(child, node["properties"][key], root)
    elif kind == "array":
        value = cast(list[Any], value)
        if not node["minItems"] <= len(value) <= node["maxItems"]:
            raise InvalidDelivery("DELIVERY_LIMIT")
        if node.get("uniqueItems") and len({canonical_bytes(v) for v in value}) != len(value):
            raise InvalidDelivery("DELIVERY_SCHEMA_DUPLICATE")
        for child in cast(list[Any], value):
            validate(child, node["items"], root)
    elif kind == "string":
        value = cast(str, value)
        if not node["minLength"] <= len(value) <= node["maxLength"]:
            raise InvalidDelivery("DELIVERY_LIMIT")
        if "pattern" in node and re.fullmatch(node["pattern"], value) is None:
            raise InvalidDelivery("DELIVERY_SCHEMA_VALUE")
    elif kind == "integer" and not node["minimum"] <= value <= node["maximum"]:
        raise InvalidDelivery("DELIVERY_LIMIT")


def read_contract(path: Path, *, policy: bool = False, reader_major: int = 1) -> Any:
    with path.open("rb") as stream:
        limit = 65536 if policy else MAX_BYTES
        value = parse_json(stream.read(limit + 1), limit)
    if not isinstance(value, dict):
        raise InvalidDelivery("DELIVERY_READER_UNSUPPORTED")
    record = cast(dict[str, Any], value)
    version = record.get("manifest_schema" if policy else "schema_version")
    if not isinstance(version, str) or version not in {"custometry-delivery/v1", "custometry-delivery/v2"}:
        raise InvalidDelivery("DELIVERY_READER_UNSUPPORTED")
    if reader_major not in (1, 2) or (version.endswith("/v2") and reader_major < 2):
        raise InvalidDelivery("DELIVERY_READER_UNSUPPORTED")
    name = "delivery-manifest.v2.schema.json" if version.endswith("/v2") else "delivery-manifest.schema.json"
    schema = parse_json(Path(__file__).with_name(name).read_bytes())
    check_schema(schema, schema)
    validate(record, schema["$defs"]["verificationPolicy"] if policy else schema, schema)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--policy", action="store_true")
    parser.add_argument("--reader-major", type=int, choices=(1, 2), default=1)
    args = parser.parse_args()
    try:
        read_contract(args.path, policy=args.policy, reader_major=args.reader_major)
    except (InvalidDelivery, OSError, ValueError, KeyError, TypeError) as error:
        code = str(error) if isinstance(error, InvalidDelivery) else "DELIVERY_INPUT_INVALID"
        print(json.dumps({"result": "fail", "code": code,
                          "next_action": "Obtain supported intact input; do not execute it."}))
        return 2
    print(json.dumps({"result": "pass", "code": "DELIVERY_STRUCTURE_VALID",
                      "next_action": "Complete independent authenticity and closure verification."}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
