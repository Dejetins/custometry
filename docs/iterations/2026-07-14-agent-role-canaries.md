# Custometry — positive and negative profile spawn canaries

## Status and scope

- status: `validation and cold review complete`;
- date: `2026-07-14`, `Europe/Moscow`;
- runtime: `codex-cli 0.144.2`, app-server protocol;
- validated files: `.codex/AGENTS.md` and nine `.codex/agents/*.toml` profiles;
- applicable machine-blueprint IDs: `DOC-RULE-001`, `DOC-RULE-002`, `DOC-RULE-003`, `DOC-RULE-007`, `DOC-RULE-010`;
- product implementation, API, PostgreSQL, browser, deployment, and performance are outside the proof boundary.

## Method

Two separate spawns were run for each role:

1. positive — the role accepts only the read-only classification of its task, selects the applicable mode and skill route, and returns `complete` for that classification;
2. negative — the role does not perform adjacent work, returns `blocked`, and names exactly one `next_owner`.

The harness checked the following fail-closed conditions:

- exactly one child and the exact `thread.agentRole` from runtime metadata rather than the model's self-description;
- the correct `parentThreadId` and an ephemeral root;
- the child policy actually injected at runtime: filesystem `read-only`, outbound network restricted, and approval policy `never`;
- no file-change, MCP, web-search, or image-generation actions;
- no reading of the role's own `.codex/agents/<role>.toml`, so the profile is proven by runtime injection;
- required `role_fit`, `mode`, authoritative inputs, primary skill route, ownership, proof boundary, status, stop reason, exactly one `next_owner`, empty `files_changed`, and `write_attempted=false`;
- the repository content hash matched before and after every accepted canary.

A positive `complete` means only that the read-only classification was completed. It does not mean that the hypothetical product task was implemented.

## Results

| Role | Positive route | Negative stop / handoff | Accepted child IDs | Result |
|---|---|---|---|---|
| `architect` | `inspect` → `architecture-design` | FastAPI implementation → `backend_engineer` | `019f6278-04dc-7bf3-8a27-045952a3d222` / `019f6278-0497-7df2-a987-6072fbbc4420` | `2/2 pass` |
| `backend_engineer` | `inspect` → `contract-impact-analysis` | React/browser work → `frontend_engineer` | `019f6279-9dad-7501-a7a3-5f67b9ea48e3` / `019f6282-aeb6-7680-bfa9-c97589c0a589` | `2/2 pass` |
| `data_engineer` | `inspect` → `contract-impact-analysis` | Forecast champion/training → `ml_engineer` | `019f6282-b134-7042-8c4f-28dd2940465a` / `019f6282-d6d1-74e3-a17b-f307f07c4802` | `2/2 pass` |
| `devops_engineer` | `inspect` → `pre-ship-gate` | Read-only `contract-impact-analysis`, DDL ownership → `backend_engineer` | `019f6283-c8e1-75c1-ab76-c0c058c9d7ba` / `019f6283-c827-7971-9564-ce73167b55e1` | `2/2 pass` |
| `frontend_engineer` | `inspect` → `ui-ux-pro-max` | Product scope/acceptance → `product_agent` | `019f627b-eef2-7c80-8d71-0782555dfffd` / `019f627c-0778-7ed2-a26f-6ecedc54f5e1` | `2/2 pass` |
| `ml_engineer` | `inspect` → `data-analytics-methodology` | Ingestion/artifact/watermark → `data_engineer` | `019f629c-7797-77d2-8aa3-53dddde9299f` / `019f629c-71ff-74e3-ac43-16d9c223c667` | `2/2 pass` |
| `qa_engineer` | `gate` → `backend-quality-gates` | Diagnose-only `root-cause-debugging`, fix → `backend_engineer` | `019f627c-f892-77f2-ba6d-84e224f836b1` / `019f6284-c593-7a30-90d9-f7da87ae8b09` | `2/2 pass` |
| `product_agent` | `inspect`: `product-design:index` → `product-design:audit` | React implementation → `frontend_engineer` | `019f6287-a6bf-7b73-9190-58357c9ede68` / `019f627d-fa10-7b40-80a4-5b055764d944` | `2/2 pass` |
| `prompt_manager` | `audit` → `prompt-manager` | Pack execution → `staged-plan-runner` | `019f628d-11b3-7713-b823-57348d34aa84` / `019f628f-4ed8-7be1-b68b-c9a80c4cf2e3` | `2/2 pass` |

Result: `18/18 pass`; nine positive classifications completed with `complete`, and nine negative classifications returned `blocked` with the expected handoff.

## Observations during harness stabilization

- An early `thread/read` sometimes encountered an empty rollout. Bounded retry/backoff eliminated the transport race; the profile had already been created with the correct `agentRole`.
- Four external PNG files appeared and then disappeared from the worktree during the first batch attempt. They were not created by the canaries, but correctly changed the content hash. The affected checks were repeated against a stable baseline, and the preliminary results were rejected.
- Negative DevOps and QA can use a read-only cross-cutting skill for classification and must still stop before adjacent implementation. The canary therefore checks for the absence of workflow takeover, not the absence of every skill.
- Product Design uses a two-step route: the mandatory `product-design:index` selects `product-design:audit`; the actual audit workflow may be reported as primary.
- The canary exposed an ambiguous compound `next_owner`. The shared contract was corrected so that the field contains exactly one role or executor ID, with subsequent owners described separately.

## Runtime limitation

In Codex 0.144.2, a custom-role child with a non-empty TOML profile does not inherit `ephemeral=true` after role reload, and neither `spawn_agent` nor the role TOML supports an `ephemeral` field. Accepted child metadata was therefore retained in the local `~/.codex/state_5.sqlite` and `~/.codex/sessions`.

This did not weaken the canary sandbox: child rollout and state metadata independently confirmed filesystem `read-only`, outbound network restricted, and approval policy `never`; all 18 accepted content hashes matched. No raw rollout or transcript was stored in the repository. The limitation concerns the local persistence of Codex metadata, not the product or Git.

Official sources: [Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md), [Codex App Server](https://learn.chatgpt.com/docs/app-server.md), [spawn arguments in Codex 0.144.2](https://github.com/openai/codex/blob/rust-v0.144.2/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs#L178-L188), and [role reload](https://github.com/openai/codex/blob/rust-v0.144.2/codex-rs/core/src/agent/role.rs#L56-L81).

## Cold review receipt

- mode: independent terminal read-only review;
- reviewer: `/root/cold_role_routing_review`;
- scope: `.codex/AGENTS.md`, nine role TOML profiles, both blueprints, the architecture document, this canary report, skill routes, `codex doctor`, and accepted canary metadata;
- reviewer verdict: `Release after fixes`;
- Blocker/High: none;
- Medium: `ml_engineer.design` did not define its local mutation boundary explicitly enough;
- author fix: `design` is now read-only by default and may change only explicitly named forecast-domain contract or methodology artifacts under separate design authority; implementation code is excluded;
- fixed blockers: none;
- fixed findings: `1 Medium`;
- local follow-up: TOML/structural validation passed, `codex doctor` passed, and repeated ML positive/negative canaries passed `2/2` with the exact role and policy, the correct route and handoff, and an unchanged content hash;
- second review: not performed in accordance with the terminal reviewer contract;
- residual risk: upstream persistence of custom-role children in Codex 0.144.2; the verdict does not mean Git publication or product ship readiness.

## Contract impact

| Surface | Classification | Rationale |
|---|---|---|
| Codex agent config | `compatible-change` | Unsupported fields were removed; previously ignored malformed profiles became loadable |
| Role selection / routing | `compatible-change` | Role names were preserved; selection, ownership, stop, and handoff behavior became more deterministic |
| Skill contracts | `none` | No skill changed; the TOML profiles contain conditional routes only |
| Product/API/DTO/persistence/browser contracts | `none` | Product implementation and the product blueprint did not change |
| Local Codex session persistence | `unknown` outside the repository | Depends on an upstream fix for custom-child ephemeral inheritance |

## File manifest and next step

- created: `docs/iterations/2026-07-14-agent-role-canaries.md`;
- modified by the role-contract correction: `.codex/AGENTS.md`, `.codex/agents/*.toml`, `docs/architecture/repository-layout.md`;
- deleted: none;
- foreign/excluded: external PNG files that appeared briefly and were not modified by the agent;
- next step: publication is not authorized; commit and push require a separate user request.
