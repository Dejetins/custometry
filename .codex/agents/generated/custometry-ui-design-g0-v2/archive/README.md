# Historical prompt archive

This directory owns the regular-file copies of superseded and otherwise
non-current-authority UI design program prompts. Current-authority prompts stay
as regular files in the parent prompt-pack directory.

The original historical paths in the parent directory are relative symbolic
links into this directory. Those links preserve immutable ledger and transition
receipt references without reviving historical prompts as execution authority.

## Checkout requirement

Inspection and validation of this archive require a symlink-capable checkout
(macOS, Linux, or WSL with Git symlinks enabled). A checkout that uses
`core.symlinks=false` is not a supported execution or historical-inspection
surface for this prompt pack because Git would materialize link targets as
plain text files.

## Preflight

Run this check after checkout and before validating or inspecting historical
prompt rows:

```bash
python3 - <<'PY'
from pathlib import Path

pack = Path('.codex/agents/generated/custometry-ui-design-g0-v2')
archive = pack / 'archive'
links = sorted(path for path in pack.glob('*.md') if path.is_symlink())
files = sorted(path for path in archive.glob('*.md') if path.name != 'README.md')

assert len(links) == len(files) == 110
assert {path.name for path in links} == {path.name for path in files}
assert all(not Path(path.readlink()).is_absolute() for path in links)
assert all(path.resolve().parent == archive.resolve() for path in links)
assert all(path.read_bytes() == (archive / path.name).read_bytes() for path in links)
print('PASS prompt archive compatibility: 110/110')
PY
```

Then run the semantic ledger validator:

```bash
python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_stage_ledger.py \
  --project-root . \
  .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md
```
