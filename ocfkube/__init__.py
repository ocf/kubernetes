import importlib
import yaml

import os


def argocd_build():
    # See https://argoproj.github.io/argo-cd/user-guide/build-environment/
    ARGOCD_APP_NAME = os.environ["ARGOCD_APP_NAME"]
    print(build(ARGOCD_APP_NAME))


def build(app_name: str) -> str:
    # avoid casing on application name, just try to import the right file
    new_app_name = app_name.replace("-", "_")
    app = importlib.import_module(f"ocfkube.apps.{new_app_name}")
    return yaml.safe_dump_all(app.build())
