import importlib.resources as pkg_resources
import sys
import types
from collections import UserDict

import tomlkit

import ocfkube.apps


class ModuleDict(types.ModuleType, UserDict):
    data = tomlkit.parse(pkg_resources.read_text(ocfkube.apps, "versions.toml"))


sys.modules[__name__] = ModuleDict(__name__)
