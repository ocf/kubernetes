from __future__ import annotations

from typing import Generator

import requests
import yaml

from apps.versions import versions

name = "buildkit"


def objects() -> Generator[dict, None, None]:
    contents = requests.get(
        f"https://raw.githubusercontent.com/moby/buildkit/{versions['buildkit']['version']}/examples/kubernetes/statefulset.rootless.yaml",
    )
    contents.raise_for_status()

    yield yaml.safe_load(contents.text)
