import importlib
import yaml

import os

def argocd_build():
    # See https://argoproj.github.io/argo-cd/user-guide/build-environment/
    ARGOCD_APP_NAME = os.environ["ARGOCD_APP_NAME"]
    print(build(ARGOCD_APP_NAME))


def build(application_name: str) -> str:
    # avoid casing on application name, just try to import the right file
    app = importlib.import_module(f"ocfkube.apps.{application_name}")
    return yaml.safe_dump_all(app.build())
