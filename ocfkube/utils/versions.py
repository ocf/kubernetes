from collections import UserDict
import ocfkube.apps
import importlib.resources as pkg_resources
import sys
import tomlkit
import types


class ModuleDict(types.ModuleType, UserDict):
    data = tomlkit.parse(pkg_resources.read_text(ocfkube.apps, "versions.toml"))


sys.modules[__name__] = ModuleDict(__name__)
