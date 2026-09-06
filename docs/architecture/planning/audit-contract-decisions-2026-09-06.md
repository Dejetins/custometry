---
doc_id: ARCH-AUDIT-CONTRACT-DECISIONS-2026-09-06
title: Remaining documentation audit contract proposals
doc_version: 2
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [DOC-RULE-001, DOC-RULE-002, DOC-RULE-006, GOAL-005, GOAL-007, GOAL-015, NON-GOAL-002, NON-GOAL-009, NON-GOAL-015, ARCH-PRINCIPLE-001, ARCH-PRINCIPLE-002, ARCH-PRINCIPLE-003, ARCH-PRINCIPLE-004, ARCH-PRINCIPLE-005, ARCH-PRINCIPLE-007, ARCH-PRINCIPLE-008, ARCH-PRINCIPLE-010, ARCH-PRINCIPLE-011, ARCH-PRINCIPLE-014, PVM-001, PVM-002, PVM-003, PVM-004, PVM-005, PVM-006, MATERIALIZE-002, MATERIALIZE-003, MATERIALIZE-010, MATERIALIZE-011, MATERIALIZE-013, MATERIALIZE-017, EXEC-STATE-001, EXEC-STATE-002, EXEC-STATE-006, EXEC-CANCEL-004, EXEC-CANCEL-005, NOTIFY-003, NOTIFY-004, NOTIFY-006, NOTIFY-008, NOTIFY-009, NOTIFY-010, NOTIFY-011, NOTIFY-012, NOTIFY-015, SEC-001, SEC-006, SEC-007, SEC-016, SEC-017, SEC-018]
status: proposed
proof_boundary:
  label: source-traceable-contract-proposals-and-exact-arithmetic-example
  exclusions: [implementation, database-concurrency, provider-delivery, runtime-tls, browser, performance, recovery, release]
---

# Remaining documentation audit contract proposals

## Status and authority

PVM, shared cancellation and notification revocation remain `proposed`. The owner accepted only the TLS exception in section 4 on 2026-09-06 through WS-001 1.0.0; the artifact retains proposed status for the other three decisions.
The three pending selections cover PVM algebra, shared compute cancellation and
notification endpoint revocation. Those policies must be accepted before changing
dependent behavior; they do not block unrelated
accepted documentation repairs. Implementation belongs to the respective
context owners and its independent verification boundary.

[W31](../../../.codex/delivery/tickets/W31-RECONCILE-DOCUMENTATION-AUDITS.md) and the [accepted
reconciliation](./documentation-audit-reconciliation-2026-09-06.md) authorize concrete proposals,
not silent adoption of new runtime policy. These recommendations preserve the modular monolith,
PostgreSQL control-plane truth, immutable artifacts, owner ports, workspace isolation, transactional
outbox, and the release stages in the [machine
blueprint](../../../custometry-technical-blueprint-ru.md). Its [human
mirror](../../../custometry-technical-blueprint-human-ru.md) explains the same obligations.
`DOC-RULE-001/002` retain their existing force; `DOC-RULE-006` supplies reproducibility, not
acceptance of this proposal. PVM and external Notifications target `v1_target`; no first external
release, forecast work, threshold, SLA, credential, or deployment target is selected.

| Kind | Evidence and consequence |
|---|---|
| Fact | Machine §12.13 names PVM order and reconciliation without algebra; §9.7/9.11 require coalescing and cancellation without consumer ownership rules. |
| Historical baseline | NOTIFY-012 applied revocation only to new delivery; SEC-001 proxy TLS conflicted with the former SEC-016 secretless Edge. The TLS conflict is resolved by the owner adoption in section 4; notification revocation remains pending. |
| Fact | Publication-base source inspection at `d5ecbd33c1fd582058ec3514e2084820c8a3f1c2` finds implemented execution-control and Notifications modules; `packages/analytics_sales` remains a placeholder, while implemented analytics lives in `packages/analytics_core`. Presence of analytics code alone does not establish PVM support. The earlier local-audit placeholder observation does not describe this publication base. [Edge configuration](../../../deploy/edge/nginx.conf) still listens on HTTP port 8080 with one Web upstream. Source presence is not runtime or external-consumer evidence. |
| Fact | Existing execution cancellation is scoped to a Run: `packages/execution/application/service.py` delegates `run.cancel`, and `infrastructure/control_postgres.py` serializes revision/idempotency, transitions to CANCELLING and fences outstanding attempts with cancel outbox records. Migration `0008` already persists runs, attempts, history, outbox and idempotency. No durable shared-consumer-interest graph was found in the bounded owner paths. The proposal extends this existing lifecycle. |
| Fact | Existing Notifications implements in-app inbox delivery and read/update operations, with source-event, inbox, event-history, idempotency and audit-outbox persistence in migration `0009`. No external endpoint/version/security-revoke or external retry implementation was found in the bounded Notifications/API/contracts search. The endpoint proposal concerns the future v1 external-delivery extension. |
| Assumption | Existing execution, notification and artifact records/consumers must be inventoried before adopting the proposed contracts. Their absence cannot be assumed; no proposal authorizes rewriting existing records. |
| Proposal | Three primary options remain proposals; only the TLS option is an accepted amendment to the blueprint. |
| Unknown | Acceptance of the economic attribution convention, last-consumer policy and security-revoke semantics; the actual deployment/provider/consumer matrix and TLS runtime proof remain future qualification inputs. |

Ownership and dependency direction follow the accepted [context map](../bounded-context-map.md).
Apps compose inbound adapters; application/domain contracts own their ports; infrastructure
implements them. No new service or direct access to another context's private tables is proposed.

## 1. PVM: fixed portfolio, volume then mix then price

**Primary recommendation:** register the following exact interpretation of
`portfolio_laspeyres_price_last_v1`, satisfying `PVM-001` through `PVM-006`. Base prices value
volume/mix changes; the final price step uses comparison quantities. The name does not imply a
Laspeyres price index. A symmetric/Shapley alternative can be a separately registered method; it
changes attribution and needs its own identity and validation. Keeping only the name leaves output
underdetermined and does not close the audit.

Analytics owns `PvmCalculationPort` and `PvmResultProjection` (proposed public names). Semantic
Model supplies pinned metric, product/UOM, grain and policy projections; Analytics emits immutable
results through Artifact Lifecycle. Presentation consumes effects and trust evidence without
recomputing them.

### Input, reference portfolio and algebra

For one pinned authorized root filter scope and one commensurate quantity-unit portfolio, atom `i`
is a unique product × allowed disjoint dimension cell. Pin the atomic grain, root scope hash,
product identity mapping, UOM conversion, period alignment, returns/cancellation, currency/FX,
taxes, all metric versions, and `calculation_order=[volume,mix,price]` in the spec/result identity.
Different non-convertible UOM portfolios calculate separately; only currency effects sum across
portfolios. No aggregation of kilograms and units into a common `Q`.

Let `q_ti`, `p_ti`, `r_ti` be the pinned quantity, unit price and recognized revenue at `t=0,1`.
Define disjoint comparable `C`, new `N`, discontinued `D`, and unattributed `U` sets with a recorded
reason per atom. Determine new/discontinued product identity over the entire root scope, not from
absence in one child cell; cell-only turnover of an otherwise present product belongs to explicit
`U` policy. Proposed strict eligibility for `C`: positive quantities in both periods, comparable
product/UOM and known prices/revenues. A valid zero price stays zero. A missing observation is never
proof of zero activity. Confirmed absent-side activity may be zero for `N`/`D`; absent prices on
their zero-activity side need no imputation. Negative/zero-net quantities, changed packs and unknown
prices require the explicit pinned policy: validated normalization/separate portfolio, block, or
`separate_unattributed`. The template does not silently net returns or choose a returns policy.
Unknown revenue prevents reconciliation to observed revenue and blocks trusted publication for that
claimed population.

For nonempty `C`, with `Q0=sum_C(q_0i)>0`, `Q1=sum_C(q_1i)>0`:

```text
s_0i = q_0i / Q0                       s_1i = q_1i / Q1
V_i  = (Q1 - Q0) * s_0i * p_0i
M_i  = Q1 * (s_1i - s_0i) * p_0i
P_i  = q_1i * (p_1i - p_0i)
E_i  = (r_1i - q_1i*p_1i) - (r_0i - q_0i*p_0i)
V_i + M_i + P_i + E_i = r_1i - r_0i
A_i  = r_1i for i in N; -r_0i for i in D; 0 otherwise
E_i  = r_1i-r_0i for i in U; other non-applicable effects are zero
Delta_R = sum(V_i + M_i + P_i + A_i + E_i)
```

`E` explicitly separates revenue-versus-price×quantity discrepancy and unattributed coverage. It is
not a balancing number inserted after calculation. With no comparable atoms, `V=M=P=0` with
`no_comparable_portfolio` disclosure; known assortment/unattributed deltas still reconcile. A
declared absolute tolerance applies to `abs(Delta_R_observed - sum_effects)` before display
rounding; its value comes from the pinned spec, not this proposal. Residual coverage remains visible
even when the arithmetic reconciliation error is zero.

For `separate_assortment_effect`, the observed delta covers all root atoms. For the existing
`comparable_only` option, it covers `C` only, with `A=0`; also disclose the full filtered delta and
excluded `N/D/U` delta so that `full_delta = comparable_delta + excluded_delta`. Do not present the
smaller population as whole-portfolio revenue change.

Drilldown sums the stored atomic `V/M/P/A/E` computed using the parent's `Q0/Q1` and shares. Each
atom maps once to a child, including explicit unknown buckets. Child sums equal the parent.
Recalculating shares within a child is a separate analysis with a new reference-scope identity, not
the parent's contribution. Overlapping groups cannot be added; versioned exclusive allocation is
needed before offering an additive view. Presentation rounding cannot alter stored effects; disclose
any display rounding difference separately.

### Exact arithmetic example and observed evidence

One unit portfolio, no FX conversion, `C={A,B}`, `N={C}`, `D={D}`:

| Atom | q0 / q1 | p0 / p1 | r0 / r1 | V | M | P | A | E | Delta |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| A | 10 / 18 | 2 / 3 | 20 / 55 | 10 | 6 | 18 | 0 | 1 | 35 |
| B | 10 / 12 | 4 / 5 | 40 / 60 | 20 | -12 | 12 | 0 | 0 | 20 |
| C | 0 / 3 | absent / 7 | 0 / 21 | 0 | 0 | 0 | 21 | 0 | 21 |
| D | 2 / 0 | 5 / absent | 10 / 0 | 0 | 0 | 0 | -10 | 0 | -10 |
| Total | — | — | 70 / 136 | 30 | -6 | 30 | 11 | 1 | 66 |

`Q0=20`, `Q1=30`; the A/B base shares are both `1/2`, comparison shares `3/5` and `2/5`. On
2026-09-06, local `.venv/bin/python` with `fractions.Fraction` evaluated the equations and asserted
each comparable row equality, totals `(30,-6,30,1)`, and `30-6+30+11+1 == 136-70 == 66`: PASS. This
checks the example and additive allocation, not implementation or empirical economic validity. The
equations derive the telescoping identity; they do not assert a causal decomposition or
external-standard certification.

**Selection still needed:** accept this attribution convention, especially root-preserving drilldown
and comparable-only disclosure. Method scope is otherwise specified; actual source/policy readiness
belongs to later tickets.

## 2. Shared computation: cancel participation separately from compute

**Primary recommendation:** an ordinary cancel detaches that consumer's durable interest; a
separately authorized operator command cancels shared compute. When no durable consumer or
materialization/schedule interest remains, cancel the compute. Browser disconnect alone never
detaches interest. The alternative is completing abandoned work for cache under an explicit resource
policy; it can improve reopen latency but spends resources without a waiting consumer. No grace
interval, lease duration, or compute budget is invented here.

Execution Control owns proposed `ComputeParticipationPort`, `ComputeCancellationPort` and its
PostgreSQL command/participation/compute records. Identity supplies authorization decisions;
Artifact Lifecycle owns commit fencing and lineage references; consumers use owner projections.
`MATERIALIZE-002/003/010/011/013/017`, `EXEC-STATE-001/002/006` and `EXEC-CANCEL-004/005` remain the
constraints.

- Proposed durable identities: `compute_id`, `reuse_key`, `generation`,
  `fencing_token`, `revision`; participation has `consumer_id`, owning request/
  run/node reference, policy version, `state=attached|fulfilled|cancelled` and
  `revision`. A schedule/materialization has an explicit service-owned interest.
- Commands `CancelParticipationV1` and `CancelComputeV1` carry `command_id`,
  workspace, target identity, expected revision, actor and reason code. A unique
  command identity makes retries return the persisted receipt plus current
  authorized state; reuse of that identity with different payload is rejected.
  Revision conflict is explicit. Ordinary callers cancel their authorized
  interests; operator cancellation checks existing operational authority and
  scope, without granting access to result data or other consumer identities.
- In one owner transaction, detach interest, evaluate remaining durable
  interests and record state history/outbox. Global or last-interest cancel
  fences the compute and moves it to `CANCELLING` atomically before dispatching
  cooperative stop. Worker checks the epoch before commit; the same owner
  serialization orders result commit, cancellation, and consumer fulfillment.
- Fulfillment winning first remains terminal and cancellation returns that
  state. Cancellation winning first prevents later result binding to that
  participation. Other attached consumers still receive a successful shared
  result. Cancelling a run detaches all its interests; run/node aggregation
  accounts for that detachment before claiming terminal cancellation.
- Operator cancellation prevents new joins to that generation and detaches its
  remaining interests with a safe shared-cancel reason. `CANCELLING` persists
  until attempts stop or are fenced and cleanup policy completes. Existing
  committed outputs become orphan candidates only as applicable to the stopped
  attempt; valid references from other/published consumers remain protected.
  Declared partial policy continues to govern publishable successful branches.
- Reconnect queries the persisted participation after fresh authorization;
  it does not create a second consumer. Explicitly cancelled participation is
  immutable; retry/reopen creates a new interest and may reuse an authorized
  committed artifact or join a later generation. Reconciler resumes command
  delivery and cleanup from PostgreSQL, never from Valkey subscriber counts.

**Selection still needed:** approve last-interest cancellation versus bounded completion-for-cache.
Per-consumer versus operator semantics are the proposed shared API meaning; no new permission grant
is selected.

## 3. Endpoint rotation, security revoke and uncertain external outcomes

**Primary recommendation:** ordinary rotation affects new deliveries and lets already pinned
deliveries drain while their version remains valid; security revoke additionally blocks new dispatch
admissions and retries for affected versions. Keeping all old deliveries active matches current
`NOTIFY-012` but cannot stop a compromised destination. Silent rebinding to a new endpoint changes a
previously authorized destination and is excluded from both options.

Notifications owns proposed `EndpointLifecyclePort`, `NotificationDispatchPort` and
delivery/reconciliation projections; its adapter alone resolves destination and signing-secret
references. Report Delivery remains separate. Identity supplies authorization; Audit consumes
redacted owner events. Existing `NOTIFY-003/004/006/008/009/010/011/015`, `SEC-006/007` still apply.

- Rotation creates an immutable version for new deliveries. Preserve pinned
  payload/version hashes and access checks on queued/retried work; keep old
  credential references usable only for its permitted drain. No available
  credential means a stable failure, not fallback to another destination.
- `RevokeEndpointV1(command_id, endpoint_id, affected_version_ids,
  expected_revision, reason_code)` records an append-only revocation overlay
  and monotonic `dispatch_epoch` in the owner transaction with audit/outbox.
  Current destination details and historical snapshots remain immutable.
  Admission checks active authorization, endpoint verification and revocation
  epoch under the same serialization boundary used by revoke.
- Pending/retry work without dispatch admission ends as `failed` with
  `endpoint_revoked`; it consumes no provider attempt. Attempts already admitted
  may have sent bytes: stop locally where possible and recheck before I/O, but
  do not promise that revocation can retract remote acceptance. The admission
  transaction is the precise cutoff; a DB transaction cannot atomically commit
  an external send. Record `dispatch_epoch` and admission time per attempt.
- Known provider success stays `delivered`, including completion after revoke;
  retain an auditable revoke/in-flight overlap. A lost response after possible
  acceptance becomes proposed attempt/delivery `outcome_unknown`, not an
  ordinary retryable failure. Reconcile using a provider receipt/status port or
  a supported receiver deduplication contract before any resend. Event ID stays
  stable across permitted retries; exactly-once external delivery is not claimed.
- If outcome cannot be reconciled, retain the unknown state with an operator
  action and safe code; do not retry against a revoked version. A later audited
  user-approved replacement is a new delivery linked to the prior one, with an
  explicit duplicate-risk disclosure. Revocation never erases attempt history.
  Logs/audit exclude destinations, secret values, response bodies and raw PII.

**Selection still needed:** accept security revocation overriding queued/retry delivery validity and
the honest admission/in-flight cutoff. Unknown outcome handling is fully specified above; provider
feasibility still needs evidence.

## 4. Production TLS: a credential-only Edge exception

**Accepted selection (2026-09-06):** the owner adopted the narrow exception in WS-001 1.0.0, now reflected in SEC-016, §24.1, ADR-0002 doc_version 2 and runtime contract doc_version 8. Allow only installation TLS private
keys/certificate chains in Edge, preserving the ban on business, workspace, source, database, mail,
API and master-key credentials. Edge remains an infrastructure adapter with one immutable Web
upstream and no domain state. The alternative is an explicitly trusted external TLS terminator
before Edge; it requires an accepted boundary for certificate custody, protected forwarding, trusted
headers and network exposure. Plain HTTP is not production TLS proof.

DevOps owns a proposed `IngressTlsConfigurationV1` configuration boundary with mode, approved public
origin, certificate/key file references, public certificate fingerprint, revision and rotation
policy reference. No private key belongs in environment values, images, Git, logs, diagnostics or
this document. Installer preflight verifies the installation-owned secret directory, file access by
the non-root Edge process, key/certificate match, trust/name/validity, and immutable configuration.
Read-only file mounts/root filesystem and bounded temporary storage preserve the existing runtime
constraints. Edge receives no secret-management API or certificate-acquisition Internet access.

Renewal/issuance stays outside Edge under installation custody. Rotation stages and validates a
complete key/chain pair, atomically selects a configuration revision, reloads/restarts through a
supported mechanism, and verifies a new handshake/public fingerprint. Failed validation keeps the
last valid revision; failed activation restores it only if still valid and uncompromised. Expired or
compromised keys are not rollback candidates; fail closed and forward-repair. Certificate health
signals use public metadata and the chosen expiry policy; no renewal schedule or numeric warning
threshold is selected. `SEC-001/007/017/018` and [network/install
policy](../runtime-network-installation.md) still constrain headers, secrets, adjacency and
target-specific egress proof.

**Selection resolved:** the narrow credential exception is accepted; external termination is not a required boundary for WS-001. Exact origin, certificate authority, custody/renewal mechanism, supported runtime and
exposure are qualification inputs, not values needed to write this design. No deployment is
authorized by this choice.

## Compatibility, rollout, proof and synchronization

Actual product API/persistence/config behavior is unchanged by this document. The table classifies
the proposed transition against the current documented guarantees; unsupported external/dynamic
consumers remain `unknown` until found.

| Boundary: before → proposed after | Impact and recovery |
|---|---|
| PVM named order → exact allocation and scope identity | `unknown` for any preexisting result consumers; same-name method semantics can change values. Version spec/result schema and algorithm identity before publication; never reinterpret stored results. Disable new computation on rollback and preserve old readers/results. |
| One cancel/run state → separate durable consumer/global commands | `breaking-change` if ordinary cancel currently stops shared work; version APIs and projections. New commands are `compatible-change` only for consumers explicitly adopting them. Preserve old terminal history; drain/fence work before reverting readers and never revive cancelled interests. |
| New-delivery-only endpoint revoke → dispatch barrier and unknown outcomes | `breaking-change` to pending/retry guarantees and exhaustive state readers. Expand readers/schema first, then switch dispatch under one epoch-aware writer; no old dispatcher may bypass revocation. Rollback pauses external sends and retains revocation/unknown records. |
| Secretless Edge → TLS-only key custody | `breaking-change` to security/config policy; fixed routing/network boundaries remain. Acceptance is recorded above; introduce the coordinated TLS mode only through its implementation milestone. Rollback may use a valid uncompromised prior certificate, never HTTP or revoked material. |

Logical phases: (1) accept the bounded choices and synchronize normative contracts; (2) inventory
actual consumers and introduce versioned owner ports, schemas/readers with migration proof; (3)
enable each capability after its boundary evidence, preserving terminal history and rollback
readers. External delivery cannot be undone; retain evidence and reconcile instead of promising
rollback. Existing supported versions require a compatibility window or explicit downtime under
machine §24.3. No numeric scale target is added.

| Contract | Required evidence before dependent acceptance | Exact documentation synchronization upon acceptance |
|---|---|---|
| PVM | Golden/property tests for equations, UOM partitioning, absent/zero/negative/missing cases, residual reasons, both assortment policies, `vs LY`, disjoint/overlapping dimensions and full parent/child reconciliation; manifest/reader compatibility and trust/export disclosure. | Machine §12.13 spec, method prose and `PVM-001`–`PVM-006`; matching human clauses; ADR-0006 PVM decision, system-design PVM flow, owner result/API contract and UI trust/drilldown description. |
| Cancellation | Real PostgreSQL races for two consumers, last-interest detach versus join, operator cancel versus commit, lost/repeated commands, crash/reconnect, expired leases, stale fencing and artifact retention; API/browser consumer semantics. | Machine §9.5–9.7/9.11 DTO/state/cancel contract and corresponding human clauses; ADR-0005 reuse policy, context-map reuse section, execution/API and progress/UI contracts. Preserve `EXEC-CANCEL-004` orphan semantics. |
| Revocation | Owner DB/adapter tests for queued/retry/admitted work, rotation drain, revoked credential access, partial send/lost response, duplicate event, restart/reconciliation and authorization changes; real supported provider/receiver proof for dedup/status claims. | Machine §15.7 `NOTIFY-012`, endpoint/attempt/delivery schemas and matching human clauses; Notifications owner ports, dispatch/runbook policy, channel UI states and generated API readers. |
| TLS | Selected target handshake/headers, wrong/missing/expired/mismatched credentials, file/mount isolation, rotation/failure/restart, no secret leakage; positive ingress and negative direct/outbound probes under `SEC-018`. | Machine `SEC-016`, §17.1 SVC-PROXY and §24.1–24.2; matching human entries; system-design ingress, runtime-network-installation, accepted ingress ADR/config contract and release runbook. |

All runtime/DB/provider/browser/performance/recovery/release proof above remains unverified.
Engineering follows accepted choices and scoped tickets; the Forecasting hold remains in force.


## Partial adoption record — 2026-09-06

[WS-001](directions/DIR-006/workstreams/WS-001.md) `1.0.0` accepts section 4 only.
The former conflict is historical evidence of the proposal baseline, resolved in
product specification `0.11.0-draft`. PVM, shared-consumer cancellation and
notification-revocation proposals are unchanged and require their own decisions.
Runtime TLS, recovery and production proof are still unobserved here.
