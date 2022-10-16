from __future__ import annotations

import requests
import yaml
from transpire import emit

from apps.versions import versions


name = "argoci"

def objects() -> None:
    # TODO: Create argo-events namespace.

    argo_workflows = requests.get(
        f"https://github.com/argoproj/argo-workflows/releases/download/v{versions['argo-workflows']['version']}/namespace-install.yaml",
    )
    argo_workflows.raise_for_status()
    emit(yaml.safe_load_all(argo_workflows.text))

    argo_events = requests.get(
        f"https://raw.githubusercontent.com/argoproj/argo-events/v{versions['argo-events']['version']}/manifests/install.yaml",
    )
    argo_events.raise_for_status()
    emit(yaml.safe_load_all(argo_events.text))
