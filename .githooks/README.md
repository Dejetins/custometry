# Repository Git hooks

These hooks are deliberately thin wrappers around the canonical quality profiles.
They do not duplicate validator rules.

Enable them once in this checkout:

```bash
git config core.hooksPath .githooks
```

- `pre-commit` activates the exact repository Node, pnpm, and uv pins, then
  runs `tools.check --scope pre-commit` with the locked Python environment.
- `pre-push` rejects any direct update to `refs/heads/main`, then runs
  the same pin activation and `tools.check --scope pre-push` for other refs.

Both hooks delegate tool activation to `scripts/run-hook-profile.sh`. This
prevents Git launched from a GUI or an older shell from silently running gates
with ambient Node or pnpm versions.

Git hooks are a local fast-feedback layer, not an authorization boundary. GitHub
branch protection and required checks remain authoritative.
