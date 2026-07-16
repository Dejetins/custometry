from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Sequence

from .core import (
    CheckResult,
    JsonObject,
    JsonValue,
    add_common_arguments,
    json_list,
    json_object,
    json_string,
    load_json,
    main_guard,
    render_result,
    require_file,
    sha256_paths,
    string_list,
    write_or_check,
)


GENERATOR = "custometry-foundation-openapi-ts"
GENERATOR_VERSION = "1"
TS_IDENTIFIER = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*$")
HTTP_METHODS = ("delete", "get", "patch", "post", "put")


def _relative_path(value: object, label: str) -> Path:
    raw = json_string(value, label)
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} must be a repository-relative path without `..`")
    return path


def _contract(data: JsonObject) -> tuple[Path, list[Path], dict[Path, str], Path]:
    if data.get("schema_version") != 1:
        raise ValueError("drift manifest requires schema_version=1")
    openapi = _relative_path(data.get("openapi"), "openapi")
    schemas = [
        _relative_path(value, f"json_schemas[{index}]")
        for index, value in enumerate(
            string_list(data.get("json_schemas"), "json_schemas", non_empty=True)
        )
    ]
    bindings_raw = json_object(
        data.get("openapi_schema_bindings") or {}, "openapi_schema_bindings"
    )
    bindings: dict[Path, str] = {}
    schema_set = set(schemas)
    for raw_path, raw_component in bindings_raw.items():
        bound_path = _relative_path(raw_path, "openapi_schema_bindings key")
        if bound_path not in schema_set:
            raise ValueError(
                f"openapi_schema_bindings path is not listed in json_schemas: {bound_path}"
            )
        component = json_string(
            raw_component, f"openapi_schema_bindings[{raw_path!r}]"
        )
        if not TS_IDENTIFIER.fullmatch(component):
            raise ValueError(f"invalid OpenAPI component name in binding: {component}")
        bindings[bound_path] = component
    client = json_object(data.get("typescript_client"), "typescript_client")
    path = _relative_path(client.get("path"), "typescript_client.path")
    if path.suffix != ".ts":
        raise ValueError("typescript_client.path must identify one generated .ts file")
    if client.get("generator") != GENERATOR or str(client.get("generator_version")) != GENERATOR_VERSION:
        raise ValueError(
            f"typescript_client must pin generator={GENERATOR!r}, generator_version={GENERATOR_VERSION!r}"
        )
    return openapi, schemas, bindings, path


def _json_type(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    raise ValueError(f"unsupported JSON value type: {type(value).__name__}")


def _semantic_schema(value: JsonValue, label: str) -> JsonValue:
    """Normalize the payload-validation subset shared by JSON Schema and OpenAPI 3.1."""

    schema = json_object(value, label)
    union = schema.get("anyOf") or schema.get("oneOf")
    if union is not None:
        variants = [
            _semantic_schema(item, f"{label}.union[{index}]")
            for index, item in enumerate(json_list(union, f"{label}.union"))
        ]
        return {"union": sorted(variants, key=lambda item: json.dumps(item, sort_keys=True))}

    raw_types = schema.get("type")
    types: list[str]
    if isinstance(raw_types, str):
        types = [raw_types]
    elif isinstance(raw_types, list):
        types = sorted(string_list(raw_types, f"{label}.type", non_empty=True))
    elif "const" in schema:
        types = [_json_type(schema["const"])]
    elif isinstance(schema.get("enum"), list) and schema["enum"]:
        enum_values = json_list(schema["enum"], f"{label}.enum")
        types = sorted({_json_type(item) for item in enum_values})
    elif isinstance(schema.get("properties"), dict):
        types = ["object"]
    else:
        types = []

    if len(types) > 1:
        variants: list[JsonValue] = []
        for schema_type in types:
            narrowed = dict(schema)
            narrowed["type"] = schema_type
            variants.append(_semantic_schema(narrowed, label))
        return {"union": sorted(variants, key=lambda item: json.dumps(item, sort_keys=True))}

    normalized: JsonObject = {}
    if types:
        normalized["type"] = types[0]
    if "const" in schema:
        normalized["const"] = schema["const"]
    if isinstance(schema.get("enum"), list):
        normalized["enum"] = sorted(
            json_list(schema["enum"], f"{label}.enum"),
            key=lambda item: json.dumps(item, sort_keys=True),
        )
    for keyword in (
        "format",
        "maxLength",
        "maximum",
        "minLength",
        "minimum",
        "multipleOf",
        "pattern",
    ):
        if keyword in schema:
            normalized[keyword] = schema[keyword]

    if normalized.get("type") == "object" or isinstance(schema.get("properties"), dict):
        properties = json_object(schema.get("properties") or {}, f"{label}.properties")
        normalized["type"] = "object"
        normalized["additionalProperties"] = schema.get("additionalProperties", True)
        required_values: list[JsonValue] = []
        required_values.extend(
            sorted(string_list(schema.get("required") or [], f"{label}.required"))
        )
        normalized["required"] = required_values
        normalized["properties"] = {
            name: _semantic_schema(item, f"{label}.properties.{name}")
            for name, item in sorted(properties.items())
        }
    elif normalized.get("type") == "array":
        normalized["items"] = _semantic_schema(schema.get("items"), f"{label}.items")
    return normalized


def _validate_schema_bindings(
    openapi: JsonObject,
    schema_documents: dict[Path, JsonObject],
    bindings: dict[Path, str],
) -> list[str]:
    components = json_object(openapi.get("components") or {}, "components")
    openapi_schemas = json_object(components.get("schemas") or {}, "components.schemas")
    mismatches: list[str] = []
    for path, component in sorted(bindings.items(), key=lambda item: str(item[0])):
        raw_component = openapi_schemas.get(component)
        if raw_component is None:
            raise ValueError(f"bound OpenAPI component does not exist: {component}")
        external = _semantic_schema(schema_documents[path], f"JSON Schema {path}")
        provider = _semantic_schema(raw_component, f"OpenAPI component {component}")
        if external != provider:
            mismatches.append(f"{path} != components.schemas.{component}")
    return mismatches


def _ts_property(name: str) -> str:
    return name if TS_IDENTIFIER.fullmatch(name) else json.dumps(name, ensure_ascii=False)


def _ts_type(value: JsonValue) -> str:
    schema = json_object(value, "OpenAPI schema")
    if "const" in schema:
        return json.dumps(schema["const"], ensure_ascii=False)
    for combinator in ("anyOf", "oneOf"):
        combined = schema.get(combinator)
        if combined is not None:
            variants = json_list(combined, f"schema.{combinator}")
            if not variants:
                raise ValueError(f"schema.{combinator} cannot be empty")
            return " | ".join(_ts_type(item) for item in variants)
    combined = schema.get("allOf")
    if combined is not None:
        variants = json_list(combined, "schema.allOf")
        if not variants:
            raise ValueError("schema.allOf cannot be empty")
        return " & ".join(_ts_type(item) for item in variants)
    reference = schema.get("$ref")
    if isinstance(reference, str):
        prefix = "#/components/schemas/"
        name = reference.removeprefix(prefix)
        if not reference.startswith(prefix) or not TS_IDENTIFIER.fullmatch(name):
            raise ValueError(f"unsupported OpenAPI schema reference: {reference}")
        return name
    enum = schema.get("enum")
    if isinstance(enum, list) and enum:
        literals = [json.dumps(item, ensure_ascii=False) for item in enum]
        return " | ".join(literals)
    schema_type = schema.get("type")
    if schema_type == "string":
        return "string"
    if schema_type in {"integer", "number"}:
        return "number"
    if schema_type == "boolean":
        return "boolean"
    if schema_type == "null":
        return "null"
    if schema_type == "array":
        return f"ReadonlyArray<{_ts_type(schema.get('items'))}>"
    if schema_type == "object" or isinstance(schema.get("properties"), dict):
        properties = json_object(schema.get("properties") or {}, "schema.properties")
        required_raw = schema.get("required")
        required: set[str] = (
            set(string_list(required_raw, "schema.required")) if required_raw is not None else set()
        )
        fields = [
            f"readonly {_ts_property(name)}{'?' if name not in required else ''}: {_ts_type(item)};"
            for name, item in sorted(properties.items())
        ]
        return "{ " + " ".join(fields) + " }" if fields else "Record<string, unknown>"
    if not schema:
        return "unknown"
    raise ValueError(f"unsupported OpenAPI schema shape: {sorted(schema)}")


def _response_type(operation: JsonObject) -> str:
    responses = json_object(operation.get("responses"), "operation.responses")
    success = next((responses[key] for key in sorted(responses) if str(key).startswith("2")), None)
    if success is None:
        raise ValueError("operation requires a 2xx response")
    response = json_object(success, "success response")
    content_raw = response.get("content")
    if content_raw is None:
        return "void"
    content = json_object(content_raw, "response.content")
    media = content.get("application/json")
    if media is None:
        raise ValueError("Foundation generator supports application/json responses only")
    return _ts_type(json_object(media, "application/json").get("schema"))


def render_typescript(openapi: JsonObject, *, source_digest: str, schema_ids: list[str]) -> bytes:
    if not isinstance(openapi.get("openapi"), str):
        raise ValueError("OpenAPI document requires an openapi version")
    paths = json_object(openapi.get("paths"), "paths")
    components_raw = openapi.get("components")
    components = json_object(components_raw, "components") if components_raw is not None else {}
    schemas_raw = components.get("schemas")
    schemas = json_object(schemas_raw, "components.schemas") if schemas_raw is not None else {}
    lines = [
        "// Generated by custometry-foundation-openapi-ts v1. Do not edit.",
        f'export const contractSourceDigest = "{source_digest}" as const;',
        "export const externalJsonSchemaIds = "
        + json.dumps(sorted(schema_ids), ensure_ascii=False, separators=(",", ":"))
        + " as const;",
        "",
    ]
    for name, schema in sorted(schemas.items()):
        if not TS_IDENTIFIER.fullmatch(name):
            raise ValueError(f"component schema name is not a TypeScript identifier: {name}")
        normalized = json_object(schema, f"components.schemas.{name}")
        if normalized.get("type") == "object" or isinstance(normalized.get("properties"), dict):
            required_raw = normalized.get("required")
            required: set[str] = (
                set(string_list(required_raw, f"components.schemas.{name}.required"))
                if required_raw is not None
                else set()
            )
            properties = json_object(
                normalized.get("properties") or {}, f"components.schemas.{name}.properties"
            )
            lines.append(f"export interface {name} {{")
            for property_name, value in sorted(properties.items()):
                optional = "" if property_name in required else "?"
                lines.append(
                    f"  readonly {_ts_property(property_name)}{optional}: {_ts_type(value)};"
                )
            lines.extend(("}", ""))
        else:
            lines.extend((f"export type {name} = {_ts_type(normalized)};", ""))

    operations: list[tuple[str, str, str, str]] = []
    seen_operations: set[str] = set()
    for route, path_value in sorted(paths.items()):
        path_item = json_object(path_value, f"paths.{route}")
        for method in HTTP_METHODS:
            raw_operation = path_item.get(method)
            if raw_operation is None:
                continue
            operation = json_object(raw_operation, f"paths.{route}.{method}")
            operation_id = json_string(operation.get("operationId"), "operationId")
            if not TS_IDENTIFIER.fullmatch(operation_id):
                raise ValueError(f"operationId is not a TypeScript identifier: {operation_id}")
            if operation_id in seen_operations:
                raise ValueError(f"duplicate operationId: {operation_id}")
            seen_operations.add(operation_id)
            if operation.get("parameters") or operation.get("requestBody"):
                raise ValueError(
                    f"operation {operation_id} exceeds the Foundation no-input generator subset"
                )
            operations.append((operation_id, method.upper(), route, _response_type(operation)))

    lines.extend(
        (
            "export class FoundationApiClient {",
            "  public constructor(",
            "    private readonly baseUrl: string,",
            "    private readonly fetcher: typeof fetch = globalThis.fetch.bind(globalThis),",
            "  ) {}",
            "",
        )
    )
    for operation_id, method, route, response_type in sorted(operations):
        lines.append(f"  public async {operation_id}(): Promise<{response_type}> {{")
        lines.append(
            f"    const response = await this.fetcher(`${{this.baseUrl}}{route}`, "
            f"{{ method: {json.dumps(method)} }});"
        )
        lines.append(
            f"    if (!response.ok) throw new Error({json.dumps(operation_id + ' failed')});"
        )
        if response_type == "void":
            lines.append("    return;")
        else:
            lines.append(f"    return (await response.json()) as {response_type};")
        lines.extend(("  }", ""))
    lines.extend(("}", ""))
    return "\n".join(lines).encode("utf-8")


def check(
    root: Path,
    manifest: Path = Path("docs/contracts/contract-drift.json"),
    *,
    write_client: bool = False,
) -> CheckResult:
    result = CheckResult("check_contract_drift")
    manifest_path = root / manifest
    if not require_file(manifest_path, result):
        return result
    try:
        openapi_relative, schema_relatives, bindings, client_relative = _contract(
            load_json(manifest_path)
        )
    except ValueError as exc:
        result.add("contract-manifest-invalid", str(exc), manifest_path)
        return result
    sources = [root / openapi_relative, *(root / item for item in schema_relatives)]
    for source in sources:
        require_file(source, result, "contract-source-missing")
    if result.findings:
        return result
    try:
        openapi = load_json(sources[0])
        schema_documents = [load_json(path) for path in sources[1:]]
        schema_documents_by_path = {
            relative: document
            for relative, document in zip(schema_relatives, schema_documents, strict=True)
        }
        schema_ids: list[str] = []
        for path, value in zip(sources[1:], schema_documents, strict=True):
            if "$schema" not in value:
                raise ValueError(f"JSON Schema lacks $schema: {path}")
            raw_id = value.get("$id")
            schema_ids.append(raw_id if isinstance(raw_id, str) and raw_id else path.name)
        semantic_mismatches = _validate_schema_bindings(
            openapi, schema_documents_by_path, bindings
        )
        for mismatch in semantic_mismatches:
            result.add(
                "json-schema-openapi-drift",
                f"bound schemas have different payload-validation semantics: {mismatch}",
            )
        if result.findings:
            return result
        digest = sha256_paths(sources, root)
        expected = render_typescript(openapi, source_digest=digest, schema_ids=schema_ids)
    except ValueError as exc:
        result.add("contract-source-invalid", str(exc))
        return result
    client_path = root / client_relative
    if write_client:
        write_or_check(client_path, expected, False, result)
    elif not require_file(client_path, result, "generated-client-missing"):
        return result
    elif client_path.read_bytes() != expected:
        result.add(
            "generated-client-drift",
            "generated TypeScript client does not byte-match the pinned deterministic generator",
            client_path,
        )
    result.details.update(
        mode=result.details.get("mode", "check"),
        source_digest=digest,
        sources=len(sources),
        schema_bindings=len(bindings),
        generated_client=str(client_path),
        generator=f"{GENERATOR}@{GENERATOR_VERSION}",
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministically generate or verify the Foundation OpenAPI TypeScript client"
    )
    add_common_arguments(parser)
    parser.add_argument("--manifest", type=Path, default=Path("docs/contracts/contract-drift.json"))
    parser.add_argument("--write-client", action="store_true")
    args = parser.parse_args(argv)
    return render_result(
        check(args.root.resolve(), args.manifest, write_client=args.write_client), args.json
    )


if __name__ == "__main__":
    main_guard(cli)
