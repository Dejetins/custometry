# Report access request analysis

## Observed source behavior

- `apps/web/src/features/reports/ReportWorkspace.tsx`, `Protected`: one shared
  `report-actor` query calls `/api/identity/me`, with `refetchInterval:10000`.
- `report-api.ts`: query default `staleTime:0`; protected requests use the existing
  same-origin session, not password authentication. 401/403 clears protected
  caches; generation checks before and after JSON decoding reject late data.
- `workspace-api.ts`: result GETs are already deduplicated by immutable result ID.
- `apps/api/src/custometry_api/identity/http_auth.py` authenticates each protected
  endpoint and enforces origin/CSRF on writes. Application services still check
  object/data permissions; UI visibility is not authorization.
- `packages/identity_access/infrastructure/postgres.py`, `actor_for_access`:
  session/principal/membership/workspace validation, role lookup, then an
  unconditional activity UPDATE within a database transaction per session check.

## Correction and safe optimization candidates

The report-only company-calendar query was removed with its unused controls.
This removes that specific request and its authentication work; no latency or
throughput gain was measured. Browser observations provide actual request paths.

Separate focused work can reuse the actor context across navigation and coalesce
redundant refreshes while retaining a defined revocation detection mechanism.
Activity writes can be throttled or coalesced after checking their consumers and
expiry/audit semantics. Server authentication and per-object/data authorization
remain necessary on protected requests. A permission cache would additionally
need explicit invalidation for logout, account/membership/workspace changes and
role or data-policy changes; merely extending a TTL does not prove equivalent
security. No such cache, polling-policy change or backend rewrite is implemented
in correction 002. Preserve current idle revocation and late-body regression proof.

This is a bounded diagnosis and candidate optimization scope, not a benchmark,
new identity architecture, measured load claim or accepted cache policy.
