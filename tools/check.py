"""Stable repository entrypoint: ``python -m tools.check --scope <scope>``."""

from tools.custometry_quality.check import cli
from tools.custometry_quality.core import main_guard


if __name__ == "__main__":
    main_guard(cli)
