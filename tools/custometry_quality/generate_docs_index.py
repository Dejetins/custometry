from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Sequence, cast

from .core import (
    CheckResult,
    JsonObject,
    add_common_arguments,
    canonical_json,
    main_guard,
    parse_frontmatter,
    render_result,
    require_dir,
    require_file,
    stable_ids,
    write_or_check,
)


HEADING = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
CYRILLIC = re.compile(r"[\u0400-\u04FF]")
DOC_ID = re.compile(r"[a-z0-9][a-z0-9-]*")
OWNER = re.compile(r"[a-z][a-z0-9-]*")
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
AUDIENCES = {"installer", "user", "operator", "administrator", "developer"}
STATUSES = {"draft", "active", "deprecated"}
VISIBILITIES = {"public", "authenticated", "internal"}
REQUIRED_SHIPPED_FIELDS = {
    "doc_id",
    "title",
    "doc_version",
    "product_spec_version",
    "locale",
    "visibility",
    "ship",
    "audiences",
    "route",
    "status",
    "owner",
    "requirement_ids",
    "proof_boundary",
    "reviewed_at",
}


@dataclass(frozen=True, slots=True)
class ProductContract:
    spec_version: str
    requirement_ids: frozenset[str]


@dataclass(frozen=True, slots=True)
class Document:
    path: Path
    title: str
    visibility: str | None = None
    locale: str | None = None
    identifier: str | None = None
    route: str | None = None


def load_product_contract(root: Path, result: CheckResult) -> ProductContract | None:
    blueprint = root / "custometry-technical-blueprint-ru.md"
    if not require_file(blueprint, result, "shipped-doc-blueprint-missing"):
        return None
    try:
        meta, body = parse_frontmatter(blueprint)
    except ValueError as exc:
        result.add("shipped-doc-blueprint-invalid", str(exc), blueprint)
        return None
    spec_version = meta.get("spec_version")
    requirement_ids = stable_ids(body)
    if not isinstance(spec_version, str) or not spec_version or not requirement_ids:
        result.add(
            "shipped-doc-blueprint-invalid",
            "machine blueprint requires a non-empty spec_version and stable requirement IDs",
            blueprint,
        )
        return None
    return ProductContract(spec_version, frozenset(requirement_ids))


def _string_list(value: object, allowed: set[str] | None = None) -> list[str] | None:
    if not isinstance(value, list) or not value:
        return None
    raw_items = cast(list[object], value)
    if not all(isinstance(item, str) and item for item in raw_items):
        return None
    items = cast(list[str], raw_items)
    if len(items) != len(set(items)) or (allowed is not None and not set(items) <= allowed):
        return None
    return items


def _valid_proof_boundary(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    proof = cast(JsonObject, value)
    return (
        isinstance(proof.get("label"), str)
        and bool(proof["label"])
        and _string_list(proof.get("exclusions")) is not None
    )


def _valid_review_date(value: object) -> bool:
    if not isinstance(value, str) or not ISO_DATE.fullmatch(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def discover(
    docs_root: Path,
    output: Path,
    result: CheckResult,
) -> list[Document]:
    documents: list[Document] = []
    for path in docs_root.rglob("*.md"):
        if path.resolve() == output.resolve():
            continue
        source = path.read_text(encoding="utf-8")
        if CYRILLIC.search(source):
            result.add(
                "contributor-doc-language-invalid",
                "repository-authored contributor documentation must be written in English",
                path,
            )
        match = HEADING.search(source)
        if not match:
            continue
        documents.append(Document(path.relative_to(docs_root), match.group(1).strip()))
    return sorted(documents, key=lambda item: item.path.as_posix())


def discover_shipped(
    docs_root: Path,
    output: Path,
    result: CheckResult,
    product: ProductContract,
) -> list[Document]:
    if not docs_root.is_dir():
        result.observed = False
        result.add("shipped-docs-root-missing", "shipped documentation root is required", docs_root)
        return []
    documents: list[Document] = []
    identities: set[tuple[str, str]] = set()
    routes: set[str] = set()
    for path in sorted(docs_root.rglob("*.md")):
        if path.resolve() == output.resolve():
            continue
        try:
            meta, body = parse_frontmatter(path)
        except ValueError as exc:
            result.add("shipped-doc-metadata-missing", str(exc), path)
            continue
        missing = sorted(REQUIRED_SHIPPED_FIELDS - meta.keys())
        if missing:
            result.add(
                "shipped-doc-metadata-invalid",
                f"missing required frontmatter fields: {', '.join(missing)}",
                path,
            )
            continue
        identifier = meta.get("doc_id")
        title = meta.get("title")
        doc_version = meta.get("doc_version")
        product_spec_version = meta.get("product_spec_version")
        locale = meta.get("locale")
        visibility = meta.get("visibility")
        ship = meta.get("ship")
        audiences = _string_list(meta.get("audiences"), AUDIENCES)
        route = meta.get("route")
        status = meta.get("status")
        owner = meta.get("owner")
        requirement_ids = _string_list(meta.get("requirement_ids"))
        proof_boundary = meta.get("proof_boundary")
        reviewed_at = meta.get("reviewed_at")
        if (
            not isinstance(identifier, str)
            or not DOC_ID.fullmatch(identifier)
            or not isinstance(title, str)
            or not title.strip()
            or isinstance(doc_version, bool)
            or not isinstance(doc_version, int)
            or doc_version < 1
            or not isinstance(product_spec_version, str)
            or not product_spec_version
            or locale not in {"en", "ru"}
            or visibility not in VISIBILITIES
            or not isinstance(ship, bool)
            or audiences is None
            or not isinstance(route, str)
            or not route.startswith("/docs/")
            or not route.endswith("/")
            or ".." in route.split("/")
            or "?" in route
            or "#" in route
            or status not in STATUSES
            or not isinstance(owner, str)
            or not OWNER.fullmatch(owner)
            or requirement_ids is None
            or not _valid_proof_boundary(proof_boundary)
            or not _valid_review_date(reviewed_at)
        ):
            result.add(
                "shipped-doc-metadata-invalid",
                "frontmatter must satisfy the normative shipped-document metadata contract",
                path,
            )
            continue
        if product_spec_version != product.spec_version:
            result.add(
                "shipped-doc-spec-version-drift",
                f"product_spec_version must equal current blueprint {product.spec_version!r}",
                path,
            )
            continue
        unknown_requirement_ids = sorted(set(requirement_ids) - product.requirement_ids)
        if unknown_requirement_ids:
            result.add(
                "shipped-doc-requirement-unknown",
                f"unknown requirement IDs: {', '.join(unknown_requirement_ids)}",
                path,
            )
            continue
        if ship and status == "draft":
            result.add(
                "draft-doc-shipping-forbidden",
                "draft documentation cannot set ship=true",
                path,
            )
            continue
        relative = path.relative_to(docs_root)
        route_parts = relative.with_suffix("").parts
        expected_route = (
            "/docs/"
            if route_parts == ("index",)
            else "/docs/"
            + "/".join(route_parts[:-1] if route_parts[-1] == "index" else route_parts)
            + "/"
        )
        if route != expected_route:
            result.add(
                "shipped-doc-route-drift",
                f"route {route!r} does not match source path route {expected_route!r}",
                path,
            )
            continue
        identity = (identifier, locale)
        if identity in identities:
            result.add(
                "shipped-doc-identity-duplicate",
                f"duplicate documentation identity {identifier}/{locale}",
                path,
            )
            continue
        identities.add(identity)
        if route in routes:
            result.add("shipped-doc-route-duplicate", f"duplicate route {route}", path)
            continue
        routes.add(route)
        match = HEADING.search(body)
        if not match:
            result.add("shipped-doc-title-missing", "documentation source requires an H1", path)
            continue
        if match.group(1).strip() != title.strip():
            result.add(
                "shipped-doc-title-drift",
                "frontmatter title must equal the H1 title",
                path,
            )
            continue
        if not ship:
            continue
        if visibility != "public":
            result.add(
                "non-public-doc-shipping-forbidden",
                "the current public shipped artifact accepts only visibility=public",
                path,
            )
            continue
        documents.append(
            Document(
                path=path.relative_to(docs_root.parent),
                title=title.strip(),
                visibility=visibility,
                locale=locale,
                identifier=identifier,
                route=route,
            )
        )
    return documents


def render(documents: list[Document]) -> bytes:
    lines = [
        "# Documentation Index",
        "",
        "<!-- Generated by tools.custometry_quality.generate_docs_index; do not edit. -->",
        "",
    ]
    groups: dict[str, list[Document]] = {}
    for document in documents:
        group = document.path.parts[0] if len(document.path.parts) > 1 else "root"
        groups.setdefault(group, []).append(document)
    for group in sorted(groups):
        lines.extend((f"## {group}", ""))
        for document in groups[group]:
            link = document.path.as_posix().replace(" ", "%20")
            lines.append(f"- [{document.title}]({link})")
        lines.append("")
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def check(
    root: Path,
    docs: Path,
    output: Path,
    check_mode: bool,
    audience: str = "contributor",
) -> CheckResult:
    result = CheckResult("generate_docs_index")
    docs_root = root / docs
    output_path = root / output
    if not require_dir(docs_root, result):
        return result
    if audience == "contributor":
        documents = discover(docs_root, output_path, result)
        payload = render(documents)
    elif audience == "shipped":
        product = load_product_contract(root, result)
        if product is None:
            return result
        documents = discover_shipped(docs_root, output_path, result, product)
        payload = canonical_json(
            {
                "schema_version": 1,
                "source_root": docs.as_posix(),
                "documents": [
                    {
                        "path": document.path.as_posix(),
                        "id": document.identifier,
                        "title": document.title,
                        "visibility": document.visibility,
                        "locale": document.locale,
                        "route": document.route,
                    }
                    for document in documents
                ],
            }
        )
        result.details["product_spec_version"] = product.spec_version
    else:
        result.add("docs-audience-invalid", f"unsupported audience {audience}")
        return result
    if not documents:
        result.add("no-documents", "no Markdown documents with H1 headings were found", docs_root)
        return result
    if result.findings:
        return result
    write_or_check(output_path, payload, check_mode, result)
    result.details.update(documents=len(documents), audience=audience)
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic documentation index")
    add_common_arguments(parser)
    parser.add_argument("--docs", type=Path)
    parser.add_argument("--audience", choices=("contributor", "shipped"), default="contributor")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    docs = args.docs or (Path("docs") if args.audience == "contributor" else Path("docs-site/docs"))
    output = args.output or (
        Path("docs/README.md")
        if args.audience == "contributor"
        else Path("apps/web/public/help-index.json")
    )
    return render_result(
        check(args.root.resolve(), docs, output, args.check, args.audience), args.json
    )


if __name__ == "__main__":
    main_guard(cli)
