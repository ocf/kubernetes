import importlib
import shutil
from pathlib import Path
from pkgutil import iter_modules

import yaml

from ocfkube.utils.postprocessor import postprocess


def build_changed() -> None:
    # TODO: ask git what changed instead of building everything
    # TODO: get relative path
    manifest_dir = Path("manifests")
    manifest_dir.mkdir(exist_ok=True)
    for importer, mod_name, _ in iter_modules(["ocfkube/apps"]):
        app = importlib.import_module(f"ocfkube.apps.{mod_name}")
        if hasattr(app, "build"):
            write_manifests(app.build(), mod_name, manifest_dir)  # type: ignore # https://github.com/python/mypy/issues/1424
        else:
            raise RuntimeError(f"Module {mod_name} has no build() function.")


def write_manifests(objects, appname: str, manifest_dir: Path):
    """Generates every possible Kubernetes manifest in this repository and writes it to {manifest_dir}"""
    appdir = manifest_dir / appname
    if appdir.exists():
        for p in set(appdir.glob("*")) - set(appdir.glob("*_SyncedSecret_*")):
            p.unlink()
    appdir.mkdir(exist_ok=True)
    for obj in objects:
        if obj is None:
            # TODO: Log message with warning
            continue
        obj = postprocess(obj, context={"appname": appname}, dev=False)
        name = obj["metadata"].get("name", obj["metadata"].get("generateName", None))
        kind = obj["kind"]
        namespace = obj["metadata"].get("namespace", appname)
        if obj["kind"] == "SyncedSecret" and (appdir / f"{name}_{kind}_{namespace}.yaml").exists():
            continue
        with open(appdir / f"{name}_{kind}_{namespace}.yaml", "w") as f:
            yaml.safe_dump(obj, f)


def build(app_name: str) -> str:
    """Returns Kubernetes manifest(s) corresponding with app_name as a YAML string"""
    new_app_name = app_name.replace("-", "_")
    app = importlib.import_module(f"ocfkube.apps.{new_app_name}")
    if hasattr(app, "build"):
        return yaml.safe_dump_all(
            [
                postprocess(x, context={"appname": new_app_name}, dev=True)
                for x in app.build()  # type: ignore # https://github.com/python/mypy/issues/1424
            ],
        )
    else:
        raise RuntimeError(f"Module {new_app_name} has no build() function.")
