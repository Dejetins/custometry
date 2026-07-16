## Outcome

<!-- State the observable outcome and the requirement IDs addressed. -->

## Scope

- owned paths:
- foreign changes intentionally excluded:
- non-goals:

## Contract impact

<!-- Classify applicable surfaces: none, compatible-change, breaking-change, or unknown. -->

- API / ports / DTOs:
- persistence / migrations:
- configuration / defaults / identity:
- retry / idempotency / external effects:
- logs / audit / alerts / runbooks:
- browser-visible behavior:
- rollout / rollback:

## Verification

- [ ] `uv run python -m tools.check --scope local`
- [ ] focused tests for changed behavior
- [ ] nearest required real-boundary evidence recorded
- [ ] docs and generated indexes updated with no drift
- [ ] no secret, PII, generated runtime state, or large data dump added

## Proof boundary

<!-- State exactly what the evidence proves and what it does not prove. -->
