from __future__ import annotations

import textwrap
from typing import Any

import requests
import yaml

from ocfkube.lib import Ingress
from ocfkube.utils import versions

base_deployment = {
    "apiVersion": "argoproj.io/v1alpha1",
    "kind": "Application",
    "metadata": {"name": "bootstrap", "namespace": "argocd"},
    "spec": {
        "project": "default",
        "destination": {"server": "https://kubernetes.default.svc"},
        "source": {
            "repoURL": "https://github.com/ocf/kubernetes",
            "path": ".",
            "plugin": {"name": "python"},
        },
    },
}


def build() -> list[dict[str, Any]]:
    contents = requests.get(
        f"https://raw.githubusercontent.com/argoproj/argo-cd/v{versions['argocd']['version']}/manifests/ha/install.yaml",
    )
    contents.raise_for_status()
    base = list(yaml.safe_load_all(contents.text))
    ingress = Ingress.from_service_name("argocd-server", 80, "argo.ocf.berkeley.edu")
    return [customize(o) for o in base] + [ingress.data, base_deployment]


def customize(o: dict[str, Any]) -> dict[str, Any]:
    if o["kind"] == "ConfigMap" and o["metadata"]["name"] == "argocd-cm":
        o["data"] = {
            "url": "https://argocd.ocf.berkeley.edu",
            "resource.exclusions": textwrap.dedent(
                """
                    - apiGroups:
                      - "cilium*"
                      kinds:
                      - "CiliumIdentity"
                      clusters:
                      - "*"
                """,
            ),
            "repositories": "- url: https://github.com/ocf/kubernetes",
        }
    if o["kind"] == "ConfigMap" and o["metadata"]["name"] == "argocd-rbac-cm":
        o["data"] = {}
        o["data"]["policy.csv"] = "g, ocfroot, role:admin"

    return o
