from pkgutil import iter_modules
import importlib


def build() -> object:
    return [
        importlib.import_module(f"ocfkube.apps.{module.name}").ci()
        for module in iter_modules(__import__("ocfkube").apps.__path__)
        if hasattr(importlib.import_module(f"ocfkube.apps.{module.name}"), "ci")
    ]
