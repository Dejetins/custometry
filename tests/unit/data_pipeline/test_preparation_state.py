from dataclasses import replace
import json
from pathlib import Path

import pytest

from apps.worker_data.prepare_retail_report import _prepare_locked
from packages.contracts.data_pipeline import DataPipelineFailure
from tools.custometry_quality import development_runtime as runtime


@pytest.mark.parametrize('defect', ['foreign_owner', 'wrong_profile', 'public_file', 'symlink'])
def test_preparation_rejects_unowned_or_unsafe_state_before_services(tmp_path: Path, defect: str) -> None:
    policy = runtime.load_policy(Path.cwd())
    paths = runtime.runtime_paths(tmp_path, policy)
    runtime.prepare_runtime(paths, policy)
    state = {'runtime_id': paths.project_name, 'profile': 'retail-report/v1'}
    if defect == 'foreign_owner':
        state['runtime_id'] = 'foreign-project'
    if defect == 'wrong_profile':
        state['profile'] = 'retail/v1'
    path = paths.secrets_dir / 'retail-report.json'
    path.write_text(json.dumps(state))
    path.chmod(0o644 if defect == 'public_file' else 0o600)
    if defect == 'symlink':
        foreign = tmp_path / 'foreign.json'
        path.rename(foreign)
        path.symlink_to(foreign)
    with pytest.raises(DataPipelineFailure, match='PREPARATION_(IDENTITY_CONFLICT|STATE_UNSAFE)'):
        _prepare_locked(paths, replace(policy))
    assert not (paths.secrets_dir / 'bootstrap_token').exists()
