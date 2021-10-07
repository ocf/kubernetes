from pkgutil import iter_modules
from pathlib import Path

import importlib
import yaml
import shutil

from ocfkube.utils.postprocessor import postprocess


def build_changed():
    # TODO: ask git what changed instead of building everything
    # TODO: get relative path
    manifest_dir = Path("manifests")
    manifest_dir.mkdir(exist_ok=True)
    for importer, mod_name, _ in iter_modules(["ocfkube/apps"]):
        app = importlib.import_module(f"ocfkube.apps.{mod_name}")
        write_manifests(app.build(), mod_name, manifest_dir)


def write_manifests(objects, appname: str, manifest_dir: Path):
    """Generates every possible Kubernetes manifest in this repository and writes it to {manifest_dir}"""
    appdir = manifest_dir / appname
    if appdir.exists():
        shutil.rmtree(appdir)
    appdir.mkdir()
    for obj in objects:
        if obj is None:
            # TODO: Log message with warning
            continue
        obj = postprocess(obj, dev=False)
        name = obj["metadata"].get("name", obj["metadata"].get("generateName", None))
        kind = obj["kind"]
        namespace = obj["metadata"].get("namespace", appname)
        with open(appdir / f"{name}_{kind}_{namespace}.yaml", "w") as f:
            yaml.safe_dump(obj, f)


def build(app_name: str) -> str:
    """Returns Kubernetes manifest(s) corresponding with app_name as a YAML string"""
    new_app_name = app_name.replace("-", "_")
    app = importlib.import_module(f"ocfkube.apps.{new_app_name}")
    return yaml.safe_dump_all([postprocess(x, dev=True) for x in app.build()])
