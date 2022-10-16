import importlib.resources as pkg_resources
from typing import Dict, cast

import tomlkit

import apps

versions = cast(
    Dict[str, Dict[str, str]],
    tomlkit.parse(pkg_resources.read_text(apps, "versions.toml")),
)
