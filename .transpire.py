from importlib import import_module
from pkgutil import iter_modules


def build() -> None:
    for _, mod_name, _ in iter_modules(["apps"]):
        app = import_module(f"apps.{mod_name}")
        if hasattr(app, "build"):
            app.build()
