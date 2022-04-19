import importlib.resources as pkg_resources
import tomlkit
import apps

from typing import Dict, cast

versions = cast(
    Dict[str, Dict[str, str]],
    tomlkit.parse(pkg_resources.read_text(apps, "versions.toml")),
)
