import importlib
from pkgutil import iter_modules


def build() -> object:
    return [
        importlib.import_module(f"ocfkube.apps.{module.name}").ci()  # type: ignore
        for module in iter_modules(__import__("ocfkube").apps.__path__)
        if hasattr(importlib.import_module(f"ocfkube.apps.{module.name}"), "ci")
    ]
