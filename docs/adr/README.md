# Architecture Decision Records

An ADR records an accepted architecture decision, its context, alternatives, consequences, and re-evaluation trigger. An ADR does not introduce a product requirement in place of the machine blueprint and does not report the current state of staged execution.

New records use the [ADR template](./adr-template.md); the template itself has `ship: false` and is not a decision.

## Index

| ADR | Status | Decision |
|---|---|---|
| [ADR-0001](./0001-foundation-operating-model.md) | accepted | Foundation operating model: public repository, protected main, UI-first slices, local-first runtime, documentation, and download-first installation |
| [ADR-0002](./0002-edge-ingress-network-segmentation.md) | accepted | Edge as an infrastructure ingress adapter; separate `edge_to_web` and `web_to_api` networks; production firewall/CNI hardening separate from Compose |
| [ADR-0003](./0003-agent-delivery-model.md) | accepted | Ticket-first agent delivery; optional coordination artifacts; static pack migration |
| [ADR-0004](./0004-ui-design-program-governance.md) | superseded | Historical Linear/Penpot reset and G-program route; current work uses the target pilot and ordinary implementation tickets |
| [ADR-0005](./0005-collaboration-measurement-and-compute-reuse.md) | accepted | Add collaboration/adoption and digital-measurement contexts plus content-addressed materialization/reuse inside the modular monolith |
| [ADR-0006](./0006-analytical-document-retail-product-and-time-aware-segmentation.md) | accepted | Add common analytical documents, time-aware segment snapshots, and retail product/category/inventory boundaries |
| [ADR-0007](./0007-responsive-web-frontend-platform.md) | accepted | Select the responsive-Web frontend platform and fix state, adapter, design-system, responsive, rollout, and proof ownership boundaries |

## Rules

- Numbers are monotonic; filenames use `NNNN-short-kebab-case.md`.
- Allowed statuses are `proposed`, `accepted`, `superseded`, and `deprecated`.
- A superseded ADR remains in Git and links to its replacement.
- A deviation from a blueprint `SHOULD` requires an ADR with a re-evaluation trigger.
- Decision owner and date are required; a runtime claim includes its proof boundary.
- Quality tooling validates links and the index.
