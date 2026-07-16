from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def write(path: Path, text: str, *, executable: bool = False) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if executable:
        path.chmod(0o755)
    return path


def test_hook_runner_activates_pinned_versions_before_profile(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    scripts = repository / "scripts"
    runner = write(
        scripts / "run-hook-profile.sh",
        (REPOSITORY_ROOT / "scripts/run-hook-profile.sh").read_text(encoding="utf-8"),
        executable=True,
    )
    write(
        scripts / "activate-toolchain.sh",
        (REPOSITORY_ROOT / "scripts/activate-toolchain.sh").read_text(encoding="utf-8"),
        executable=True,
    )
    write(repository / ".node-version", "24.18.0\n")
    write(repository / ".uv-version", "0.9.26\n")
    write(
        repository / "package.json",
        '{\n  "packageManager": "pnpm@11.13.0"\n}\n',
    )

    home = tmp_path / "home"
    pinned_bin = tmp_path / "pinned-bin"
    ambient_bin = tmp_path / "ambient-bin"
    log_path = tmp_path / "uv-command.log"

    write(
        home / ".nvm/nvm.sh",
        """nvm() {
  if [ "${1:-}" = "use" ]; then
    export PATH="${CUSTOMETRY_TEST_PINNED_BIN}:${PATH}"
    return 0
  fi
  return 1
}
""",
    )
    write(
        pinned_bin / "node",
        "#!/bin/sh\nprintf 'v24.18.0\\n'\n",
        executable=True,
    )
    write(
        pinned_bin / "corepack",
        """#!/bin/sh
if [ "${1:-}" = "pnpm" ] && [ "${2:-}" = "--version" ]; then
  printf '11.13.0\n'
  exit 0
fi
exit 9
""",
        executable=True,
    )
    write(
        ambient_bin / "node",
        "#!/bin/sh\nprintf 'v22.22.2\\n'\n",
        executable=True,
    )
    write(
        ambient_bin / "corepack",
        "#!/bin/sh\nprintf '11.9.0\\n'\n",
        executable=True,
    )
    write(
        ambient_bin / "uv",
        """#!/bin/sh
if [ "${1:-}" = "--version" ]; then
  printf 'uv 0.9.26\n'
  exit 0
fi
printf '%s\n' "$*" >"${CUSTOMETRY_TEST_UV_LOG}"
""",
        executable=True,
    )

    environment = os.environ.copy()
    environment.update(
        {
            "CUSTOMETRY_TEST_PINNED_BIN": str(pinned_bin),
            "CUSTOMETRY_TEST_UV_LOG": str(log_path),
            "HOME": str(home),
            "NVM_DIR": str(home / ".nvm"),
            "PATH": f"{ambient_bin}:/usr/bin:/bin",
        }
    )
    completed = subprocess.run(
        [str(runner), "pre-push"],
        cwd=repository,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "Node 24.18.0, pnpm 11.13.0, uv 0.9.26" in completed.stdout
    assert log_path.read_text(encoding="utf-8").strip() == (
        "run --locked python -m tools.check --scope pre-push"
    )


def test_git_hooks_delegate_to_pinned_toolchain_runner() -> None:
    pre_commit = (REPOSITORY_ROOT / ".githooks/pre-commit").read_text(encoding="utf-8")
    pre_push = (REPOSITORY_ROOT / ".githooks/pre-push").read_text(encoding="utf-8")

    assert 'scripts/run-hook-profile.sh" pre-commit' in pre_commit
    assert 'scripts/run-hook-profile.sh" pre-push' in pre_push
    assert "exec uv run" not in pre_commit
    assert "exec uv run" not in pre_push
