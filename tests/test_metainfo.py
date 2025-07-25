from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

from aiohttp_things import __version__


def test_version() -> None:
    with Path("./pyproject.toml").open("rb") as f:
        pyproject = tomllib.load(f)
        version = pyproject["project"]["version"]
        assert __version__ == version
