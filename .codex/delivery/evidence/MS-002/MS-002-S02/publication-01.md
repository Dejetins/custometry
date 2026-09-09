# S02 publication follow-up

The owner explicitly requested publication to main through a technical branch,
followed by synchronization and branch deletion. [PR #65](https://github.com/Dejetins/custometry/pull/65)
uses `codex/ms002-s02-publish`, based on origin/main. The accepted S02 receipt and
its evidence remain unchanged; this follow-up records publication compatibility.

The full pytest run exposed a frozen-inventory test tied to live source bytes
(1 failed, 387 passed, 16 skipped). The test now checks the exact Git revision that
introduced the retained inventory, including its Dockerfile mappings. Missing
history or a missing/mismatched mapped source still fails. It neither rewrites
MS-001 inventory nor claims that old images contain S02. CI already fetches full
history. An initial implementation incorrectly treated an absent alternative
mapping as fatal; it now requires exactly one matching existing recorded source.

The canonical disposable/development Compose API had no artifact directory while
S02 readiness now requires a real writable root. A bounded 64 MiB tmpfs with
UID/GID 10001 and 0700 mode provides that prerequisite; installed persistent bind
storage and HTTP route identities remain unchanged. Runtime contract revision 23
records its ephemeral boundary. CI runtime verifies this configuration.

Validation and final publication outcome are available in the PR's check runs.
No milestone permission or completed receipt is rewritten by this follow-up.
