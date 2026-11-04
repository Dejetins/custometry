# Independent review — MS-021

Existing read-only qa_engineer Dewey reviewed contracts/provider/access, scopes and
aggregate rebasing, persistence dispatch, current rights/identity and editor behavior.
Initial P2: a publication containing current-day receipts used next-midnight coverage
beyond exact publication cutoff, disabling the whole v3 catalog. Independently
reproduced with2026-10-01…07 receipts and2026-10-07T15:24:39.123456Z publication.

Two executor regressions failed before the fix. Coverage now ends at the last closed
UTC-day boundary while exact observation/knowledge cutoffs remain unchanged. Only
publication-day data returns no count definitions, retains fields/relations and never
invents past/future coverage; API distinguishes this from empty search and UI explains
it without creating a node. Future/reversed metadata still rejects. Historical output
and incomplete-history policy remain unchanged.

Final narrow verdict cleared; no new actionable findings. Reviewer independently
ran initial6 Semantic +2 v3 scope +6 old scope cases and final8 Semantic checks plus
historical boundary/UTC normalization/relation-preservation checks. All pass.
Previous DTOs, executor/calculation and main scope resolver match the baseline.
API/UI follow-up was inspected by source/tests. Genuine provider/browser/full suites
were not independently repeated. No files changed or recursive review delegated.

A second source-only review cleared the narrow functional harness adjustment: explicit
60s capture/response and saved-table deadlines in three filter specs. HTTP200, values,
identity, unknown, locks and persistence assertions remain. One route.fetch per request;
installed Playwright maxRetries defaults to0 and suite retries stays0. UI action timeout
and global configuration are unchanged. No unsafe write replay or error swallowing.
This does not establish performance or attribute the observed delay; C10 remains open.
