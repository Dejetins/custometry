"""Structural scope resolution. Provider authorization and store evaluation are separate.

Ancestry is document/chapter/page/outer-to-inner section/block. Explicit linked
expressions are appended in binding-ID order, intersected once, and never replace
ancestry constraints. Links broadcast their own expression, not an implicit copy
of a source block's full context, and do not propagate through other links.
"""

from __future__ import annotations
from collections import deque
import hashlib
import json
from typing import Any, Literal
from uuid import UUID
from packages.contracts.presentation.composer import ComposerDefinitionV1
from packages.contracts.presentation.scopes import (
    ComposerScopesV1,
    ComposerScopes,
    ReceiptScopeBinding,
    scope_filter_bindings,
    FilterScopeBinding,
    ScopeTarget,
    ScopeOrigin,
    ResolvedComposerScope,
    ContextField,
)
from packages.contracts.analytics.workspace import WorkspaceRunRequest
from packages.contracts.analytics.receipt_selection import ReceiptSelection
from packages.presentation.domain.receipt_scopes import (
    canonical_filter, replacement_field, compatible_replacement, combine_filters,
)
from packages.contracts.semantic.store_filters import semantic_expression


def hierarchy(d: ComposerDefinitionV1) -> tuple[dict[UUID, ScopeTarget], dict[UUID, UUID | None]]:
    targets = {d.document_id: ScopeTarget(kind="document", id=d.document_id)}
    parents: dict[UUID, UUID | None] = {d.document_id: None}
    for kind, values, key in (
        ("chapter", d.chapters, "chapter_id"),
        ("page", d.pages, "page_id"),
        ("section", d.sections, "section_id"),
        ("block", d.blocks, "block_id"),
    ):
        for value in values:
            identifier: UUID = getattr(value, key)
            targets[identifier] = ScopeTarget.model_validate({"kind": kind, "id": identifier})
            parents[identifier] = (
                getattr(value, "section_id")
                if kind == "block"
                else getattr(value, "parent_section_id") or getattr(value, "page_id")
                if kind == "section"
                else getattr(value, "chapter_id") or d.document_id
                if kind == "page"
                else d.document_id
            )
    return targets, parents


def path_to(identifier: UUID, parents: dict[UUID, UUID | None]) -> list[UUID]:
    result: list[UUID] = []
    current: UUID | None = identifier
    while current is not None:
        result.append(current)
        current = parents[current]
    return result[::-1]


def validate_scope_graph(d: ComposerDefinitionV1, scopes: ComposerScopes) -> None:
    targets, parents = hierarchy(d)
    edges: dict[UUID, set[UUID]] = {key: set() for key in targets}
    for child, parent in parents.items():
        if parent is not None:
            edges[parent].add(child)
    filters = {f.binding_id: f for f in scope_filter_bindings(scopes)}
    for binding in [*scope_filter_bindings(scopes), *scopes.contexts]:
        if targets.get(binding.target.id) != binding.target:
            raise ValueError("COMPOSER_UNKNOWN_SCOPE_TARGET")
        if binding.binding_id in targets or binding.binding_id in {
            s.definition_id for s in d.definitions
        }:
            raise ValueError("COMPOSER_SCOPE_ID_COLLISION")
        if not isinstance(binding, (FilterScopeBinding, ReceiptScopeBinding)):
            continue
        ancestor_ids = set(path_to(binding.target.id, parents)[:-1])
        for replaced in binding.replaces:
            previous = filters.get(replaced)
            if previous is None or previous.target.id not in ancestor_ids:
                raise ValueError("COMPOSER_REPLACEMENT_REQUIRES_ANCESTOR")
            if previous.locked or not previous.replaceable:
                raise ValueError("COMPOSER_SCOPE_LOCKED")
            if isinstance(binding, ReceiptScopeBinding):
                fields = replacement_field(binding.filter)
                if (
                    not isinstance(previous, ReceiptScopeBinding)
                    or binding.semantic_dataset_version_id != previous.semantic_dataset_version_id
                    or not compatible_replacement(binding.filter, previous.filter)
                    or len(fields) != 1
                    or fields != replacement_field(previous.filter)
                ):
                    raise ValueError("COMPOSER_REPLACEMENT_FIELD_MISMATCH")
            elif isinstance(previous, ReceiptScopeBinding):
                raise ValueError("COMPOSER_REPLACEMENT_FIELD_MISMATCH")
        for target in binding.linked_target_block_ids:
            if targets.get(target) != ScopeTarget(kind="block", id=target):
                raise ValueError("COMPOSER_UNKNOWN_LINK_TARGET")
            edges[binding.target.id].add(target)
    indegree = dict.fromkeys(targets, 0)
    for children in edges.values():
        for child in children:
            indegree[child] += 1
    queue = deque(key for key, degree in indegree.items() if degree == 0)
    visited = 0
    while queue:
        current = queue.popleft()
        visited += 1
        for child in edges[current]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if visited != len(targets):
        raise ValueError("COMPOSER_SCOPE_LINK_CYCLE")


def resolve_scope(
    d: ComposerDefinitionV1, scopes: ComposerScopes, block_id: UUID
) -> ResolvedComposerScope:
    validate_scope_graph(d, scopes)
    targets, parents = hierarchy(d)
    if targets.get(block_id) != ScopeTarget(kind="block", id=block_id):
        raise ValueError("COMPOSER_UNKNOWN_BLOCK")
    ancestry = path_to(block_id, parents)
    block = next(b for b in d.blocks if b.block_id == block_id)
    if block.source is None:
        raise ValueError("COMPOSER_NOT_DATA_BLOCK")
    base = next(s.query for s in d.definitions if s.definition_id == block.source.definition_id)
    local = None if base.local_store_ids is None else set(base.local_store_ids)
    for control in (b.control for b in d.blocks if b.control is not None):
        if block_id in control.target_block_ids and control.store_ids is not None:
            local = set(control.store_ids) if local is None else local.intersection(control.store_ids)
    if local is not None:
        base = base.model_copy(update={"local_store_ids": sorted(local)})
    query = base.model_dump(mode="json")
    origins: list[ScopeOrigin] = []
    context = {b.target.id: b for b in scopes.contexts}
    previous_context: dict[ContextField, int] = {}
    fields: tuple[ContextField, ...] = (
        "period",
        "grain",
        "calendar_ref",
        "calendar_basis",
        "alignment",
        "time_comparison",
    )
    context_dependencies: dict[ContextField, dict[str, Any]] = {}
    for identifier in ancestry:
        binding = context.get(identifier)
        if binding is None:
            continue
        for field in fields:
            value = getattr(binding.context, field)
            if value is None:
                continue
            if field in ("alignment", "time_comparison"):
                other: ContextField = "time_comparison" if field == "alignment" else "alignment"
                if other in previous_context:
                    index = previous_context.pop(other)
                    if origins[index].state == "locked":
                        raise ValueError("COMPOSER_CONTEXT_LOCKED")
                    origins[index] = origins[index].model_copy(
                        update={"state": "overridden", "overridden_by": binding.binding_id})
                    context_dependencies.pop(other, None)
                if field == "alignment":
                    query.pop("time_comparison", None)
                else:
                    query["alignment"] = "none"
            if field in previous_context:
                index = previous_context[field]
                if origins[index].state == "locked":
                    # An explicit repeated value is still an attempted override of a lock.
                    raise ValueError("COMPOSER_CONTEXT_LOCKED")
                origins[index] = origins[index].model_copy(
                    update={"state": "overridden", "overridden_by": binding.binding_id}
                )
            raw = binding.context.model_dump(mode="json")[field]
            if field == "period":
                query["common"].update(raw)
            else:
                query[field] = raw
            previous_context[field] = len(origins)
            origins.append(
                ScopeOrigin(
                    binding_id=binding.binding_id,
                    target=binding.target,
                    field=field,
                    state="locked" if field in binding.locked_fields else "applied",
                )
            )
            context_dependencies[field] = {
                "binding_id": str(binding.binding_id),
                "target": binding.target.model_dump(mode="json"),
                "value": raw,
                "locked": field in binding.locked_fields,
            }
    by_target: dict[UUID, list[FilterScopeBinding | ReceiptScopeBinding]] = {}
    for f in scope_filter_bindings(scopes):
        by_target.setdefault(f.target.id, []).append(f)
    ordered = [
        f for target in ancestry for f in sorted(by_target.get(target, []), key=lambda f: f.order)
    ]
    own_ids = {f.binding_id for f in ordered}
    linked = sorted(
        (
            f
            for f in scope_filter_bindings(scopes)
            if block_id in f.linked_target_block_ids and f.binding_id not in own_ids
        ),
        key=lambda f: str(f.binding_id),
    )
    active: dict[UUID, FilterScopeBinding | ReceiptScopeBinding] = {}
    positions: dict[UUID, int] = {}
    for f in [*ordered, *linked]:
        for replaced in f.replaces:
            if replaced not in active:
                raise ValueError("COMPOSER_REPLACEMENT_NOT_ACTIVE")
            del active[replaced]
            at = positions[replaced]
            origins[at] = origins[at].model_copy(
                update={"state": "overridden", "overridden_by": f.binding_id}
            )
        active[f.binding_id] = f
        positions[f.binding_id] = len(origins)
        origins.append(
            ScopeOrigin(
                binding_id=f.binding_id,
                target=f.target,
                field="Receipt" if isinstance(f, ReceiptScopeBinding) else "Store.store_id",
                state="locked" if f.locked else "linked" if f in linked else "applied",
            )
        )
    if any(
        (
            f.semantic_dataset_version_id
            if isinstance(f, ReceiptScopeBinding)
            else f.filter.semantic_dataset_version_id
        )
        != base.semantic_dataset_version_id
        for f in active.values()
    ):
        raise ValueError("COMPOSER_FILTER_DATASET_MISMATCH")
    dependencies = {
        "schema_version": "composer-scopes/v1",
        "contexts": context_dependencies,
        "filters": [
            {
                "binding_id": str(f.binding_id),
                "target": f.target.model_dump(mode="json"),
                "expression": semantic_expression(f.filter.expression),
                "rule": f.filter.semantic_rule,
                "schema_version": f.filter.schema_version,
                "semantic_dataset_version_id": str(f.filter.semantic_dataset_version_id),
                "locked": f.locked,
            }
            for f in sorted(active.values(), key=lambda f: str(f.binding_id))
            if isinstance(f, FilterScopeBinding)
        ],
    }
    receipts = [f for f in active.values() if isinstance(f, ReceiptScopeBinding)]
    if receipts:
        inputs: list[tuple[UUID | Literal["block-base"], ReceiptSelection]] = [
            (f.binding_id, f.filter) for f in receipts
        ]
        if base.receipt_filter is not None:
            inputs.append(("block-base", base.receipt_filter))
        query["receipt_filter"] = combine_filters(inputs).model_dump(mode="json")
        dependencies["receipt_filters"] = [
            {
                "binding_id": str(f.binding_id),
                "target": f.target.model_dump(mode="json"),
                **canonical_filter(f.filter),
                "semantic_dataset_version_id": str(f.semantic_dataset_version_id),
                "locked": f.locked,
            }
            for f in sorted(receipts, key=lambda f: str(f.binding_id))
        ]
    digest = (
        hashlib.sha256(
            json.dumps(
                dependencies, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            ).encode()
        ).hexdigest()
        if active or context_dependencies
        else None
    )
    return ResolvedComposerScope(
        block_id=block_id,
        query=WorkspaceRunRequest.model_validate(query),
        filters=[f.filter for f in active.values() if isinstance(f, FilterScopeBinding)],
        origins=origins,
        dependency_hash=digest,
    )


def preserve_scope_locks(previous: ComposerDefinitionV1, following: ComposerDefinitionV1) -> None:
    """Persisted user locks cannot be removed, retargeted or escaped by moving a block."""
    if previous.scopes is None:
        return
    before = previous.scopes
    after = following.scopes or ComposerScopesV1()
    filters = {f.binding_id: f for f in scope_filter_bindings(after)}
    contexts = {c.binding_id: c for c in after.contexts}
    locked = False
    for original in scope_filter_bindings(before):
        if original.locked:
            locked = True
            if filters.get(original.binding_id) != original:
                raise ValueError("COMPOSER_SCOPE_LOCKED")
    for original in before.contexts:
        if original.locked_fields:
            locked = True
            current = contexts.get(original.binding_id)
            if current is None or current.target != original.target:
                raise ValueError("COMPOSER_CONTEXT_LOCKED")
            for field in original.locked_fields:
                if field not in current.locked_fields or getattr(current.context, field) != getattr(
                    original.context, field
                ):
                    raise ValueError("COMPOSER_CONTEXT_LOCKED")
    if not locked:
        return

    def inherited_locks(
        d: ComposerDefinitionV1, scopes: ComposerScopes, block_id: UUID
    ) -> set[tuple[UUID, str]]:
        # Lock inheritance is structural: resolving unrelated analytical inputs here
        # would couple a selected block to semantic errors elsewhere in the draft.
        _, parents = hierarchy(d)
        ancestry = set(path_to(block_id, parents))
        result = {
            (f.binding_id, "filter")
            for f in scope_filter_bindings(scopes)
            if f.locked and (f.target.id in ancestry or block_id in f.linked_target_block_ids)
        }
        result.update(
            (c.binding_id, field)
            for c in scopes.contexts
            if c.target.id in ancestry
            for field in c.locked_fields
        )
        return result

    remaining = {b.block_id for b in following.blocks}
    for block in previous.blocks:
        if block.block_id not in remaining:
            continue
        old_locks = inherited_locks(previous, before, block.block_id)
        new_locks = inherited_locks(following, after, block.block_id)
        if not old_locks <= new_locks:
            raise ValueError("COMPOSER_SCOPE_LOCKED")
