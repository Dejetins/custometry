# HTML-first UI contracts

This directory owns portable repository contracts for the Custometry UI
foundation. The current delivery chain is:

1. product, route, and surface contracts;
2. a product-owner-accepted responsive HTML source and browser evidence;
3. semantic CSS token and registered Lucide icon identities;
4. typed public component identities, props, states, accessibility metadata,
   and DOM provenance rules;
5. screen manifests that reference registered component IDs without embedding
   visible markup;
6. an inspectable browser component catalog and deterministic screen renders;
7. structural and same-viewport visual browser receipts.

The existing `*.v1.json` pilot artifacts predate this HTML-first contract and
remain historical evidence until W29 replaces or versions their external-node
identity fields. They are not current generation inputs and must not be used by
W22. W29 owns the compatible-or-breaking classification, schema versioning,
migration checks, and normalized browser receipts for their replacement.

These contracts prove repository identity, reproducible composition, and
browser-observed reuse only. They do not prove backend integration,
authorization, persistence, measured performance, release, or deployment.
