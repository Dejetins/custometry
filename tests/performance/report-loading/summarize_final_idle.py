"""Summarize only a completed, source-bound thirty-minute idle observation."""

from datetime import datetime
import hashlib
import json
from pathlib import Path

root = Path(".codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY")
data = json.loads((root / "final-profile-idle.json").read_text())
assert data.get("completed") and data["elapsedMs"] >= 1_800_000
comment_only_drift = []
for file in data["sourceFiles"]:
    source = Path(file["path"]).read_bytes()
    if hashlib.sha256(source).hexdigest() == file["sha256"]:
        continue
    # The final static-only correction is permitted only when removing its exact
    # comment reproduces the original measured bytes, not merely similar code.
    assert file["path"] == "apps/api/src/custometry_api/identity/router.py"
    original = source.replace(b"  # pyright: ignore[reportUnusedFunction] -- registered by FastAPI", b"")
    assert hashlib.sha256(original).hexdigest() == file["sha256"]
    comment_only_drift.append(file["path"])
first, last = data["samples"][0], data["samples"][-1]
columns = ("insert", "update", "delete", "dead_tuples", "relation_bytes", "index_bytes")


def tables(sample):
    return {row[0]: dict(zip(columns, row[1:])) for row in sample["tables"]}


before, after = tables(first), tables(last)


def heaps(samples):
    return [
        next(m["value"] for m in sample["metrics"] if m["name"] == "JSHeapUsedSize")
        for sample in samples
    ]


a, b = heaps(data["heapBefore"]), heaps(data["heapAfter"])
value = dict(
    completed=True,
    elapsed_ms=data["elapsedMs"],
    sample_span_seconds=(
        datetime.fromisoformat(last["at"]) - datetime.fromisoformat(first["at"])
    ).total_seconds(),
    samples=len(data["samples"]),
    users=50,
    ready_graphs_final=last["readyGraphs"],
    ready_graphs_min_sampled=min(s["readyGraphs"] for s in data["samples"]),
    activity_changed=max(s["cohort_activity_changed"] for s in data["samples"]),
    cohort_sessions=last["cohort_sessions"],
    cohort_principals=last["cohort_principals"],
    rotation_history=last["cohort_history"],
    cohort_security_events=last["cohort_audit"],
    global_counts_before=first["counts"],
    global_counts_after=last["counts"],
    tables_before=before,
    tables_after=after,
    table_deltas={name: {c: after[name][c] - before[name][c] for c in columns} for name in before},
    wal_bytes_delta=int(last["wal"][1]) - int(first["wal"][1]),
    artifact_bytes_before=first["artifact_bytes"],
    artifact_bytes_after=last["artifact_bytes"],
    api_rss_mib=dict(
        first=first["api_rss_kib"] / 1024,
        last=last["api_rss_kib"] / 1024,
        minimum=min(s["api_rss_kib"] for s in data["samples"]) / 1024,
        maximum=max(s["api_rss_kib"] for s in data["samples"]) / 1024,
    ),
    browser_heap_bytes=dict(
        before_sum=sum(a), after_sum=sum(b), before_max=max(a), after_max=max(b)
    ),
    cache_payload_bytes_max=max(s["cache"]["bytes"] for s in data["heapAfter"] if s.get("cache")),
    cache_entries_max=max(s["cache"]["entries"] for s in data["heapAfter"] if s.get("cache")),
    forced_gc=False,
    requests=data["requests"],
    page_errors=data["errors"],
    source_hashes_still_match=not comment_only_drift,
    comment_only_source_drift=comment_only_drift,
    runtime_source_equivalent=True,
    limitations=[
        "Owned local selected profile; not release/production evidence.",
        "An early wrong-target QA login/logout caused one global invalidation/reconciliation on this fixture database; no idle-cohort activity updates. Subsequent QA used separate databases.",
        "RSS/SQL sampled about every 30 seconds; transient peaks may occur between samples.",
        "Global table/WAL deltas include the disclosed early diagnostic login/logout and database maintenance; cohort security events attribute token renewals separately.",
        "No forced browser/API collection in this idle observation.",
    ],
    harness_files=[
        dict(path=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest())
        for p in [
            "tests/performance/report-loading/idle-final.mjs",
            "tests/performance/report-loading/idle_snapshot.py",
            "tests/performance/report-loading/summarize_final_idle.py",
        ]
    ],
)
(root / "final-profile-idle-summary.json").write_text(json.dumps(value, indent=2) + "\n")
assert (
    value["ready_graphs_final"] == 50
    and value["activity_changed"] == 0
    and value["cohort_sessions"] == 50
    and value["cohort_principals"] == 50
)
assert value["artifact_bytes_after"] == value["artifact_bytes_before"] and not value["page_errors"]
print(
    json.dumps(
        {
            k: v
            for k, v in value.items()
            if k
            in [
                "elapsed_ms",
                "activity_changed",
                "rotation_history",
                "cohort_security_events",
                "api_rss_mib",
                "browser_heap_bytes",
                "wal_bytes_delta",
            ]
        }
    )
)
