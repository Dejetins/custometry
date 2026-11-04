# WS-004 continuation and dependency authority addendum — 2026-10-07

The current task was explicitly dispatched by the owner through source chat
`01a111ea-1459-7eb1-9209-94c7004145f5`. The relayed owner instruction is:
“агент сделал до MS-008 включительно, какие там подтверждения от меня нужны?
я разрешил все чтобы сделать работу. отправь остальные задачи в новый codex чат,
проконтролируй чтобы агент начал работу а не просил подтверждения, далее останови
наблюдение”. The dispatch explicitly authorizes necessary project dependencies,
including DuckDB, changes to `apps/api/pyproject.toml` and `uv.lock`, and installation
in the servicing checkout's `.venv`.

This supplements and supersedes only the dependency exclusion in the
[earlier continuation authority](owner-continuation-2026-10-07.md) and resolves the
[provider dependency decision](C04-provider-dependency-decision.md). Those historical
files and accepted MS-005–MS-008 journals/receipts remain unchanged. Their old
pending-dependency statements describe the previous authority, not a current gate.

Scope: complete the accepted WS-004 C01–C11 plan sequentially after bounded MS-008;
prepare bounded milestone plans/packs; implement, test actual user scenarios, repair
in-scope failures and accept technical stages on evidence through the existing
exclusive journal updater. Repeated owner acceptance of technical plans, stages,
milestones or routine implementation choices is unnecessary. Necessary local
rebuilds/restarts and disposable API/browser fixtures are authorized. Preserve all
existing user data and foreign checkout changes.

Work only in `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`. Do not substitute
the saved project checkout. PostgreSQL remains the control database. DuckDB is a
typed isolated columnar execution adapter; no user SQL or row-wise fallback.

This does not authorize Goal mode, parallel implementation agents, publication,
deployment, production migrations, destructive reset, external messages or removal
of existing product holds such as Forecasting. Required independent review remains
applicable. Missing provider proof still prevents the affected completion claim;
continue independent authorized work. MS-004 is not accepted retroactively.

Initial observation: retained runtime `http://localhost:41746` returned HTTP 200;
this establishes reachability only. MS-008 journal is `completed` with S01/S02
`accepted`; full C04 and C05–C11 are still incomplete.

## Explicit DuckDB confirmation

The source chat subsequently relayed the owner's direct confirmation:
“ок отлично, пускай будет DuckDB”. This confirms the same scope above and does
not change PostgreSQL ownership, preservation obligations or validation gates.
