# MS-022 authoring error and scoped recovery

Preparation accidentally read /tmp/ms019-body.txt instead of /tmp/ms022-body.txt.
Plan metadata and sequence stage contract were new, but the plan body described the
old correlated-authoring unit. Structural preflight/claim did not validate prose.
The executor noticed immediately after claim; no product implementation occurred.
This is an unusable contradictory execution source, not a provider/user blocker.

Preserve S01, its prompt, claim and journal history. Block this instance through the
exclusive CLI. Reconcile under the same existing exclusive updater mechanism: retain
original plan bytes as historical0.1.0, publish corrected intended sequence plan0.1.1,
append unique S01-R1 replacement with repair evidence and historical-plan binding.
Do not overwrite S01 prompt or claim, reset the journal, infer acceptance or weaken
checks. New preflight/claim must validate the corrected sources before implementation.

Authority is WS-004 whole-workstream technical decomposition/repair delegation;
no new owner decision is required. Existing updater/validator already support scoped
reconciliation, historical plans and unique blocked-stage replacements. Use their
actual lock, source hashes, Pack validation and atomic replacement, not a new updater.
