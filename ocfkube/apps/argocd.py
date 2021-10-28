from __future__ import annotations

from typing import Any

import requests
import yaml

from ocfkube.lib import Ingress
from ocfkube.lib.surgery import edit_manifests, make_edit_manifest
from ocfkube.utils.json import shelve
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
            "path": "manifests/bootstrap",
        },
    },
}


def build() -> list[dict[str, Any]]:
    contents = requests.get(
        f"https://raw.githubusercontent.com/argoproj/argo-cd/v{versions['argocd']['version']}/manifests/ha/install.yaml",
    )
    contents.raise_for_status()
    base = list(yaml.safe_load_all(contents.text))
    ingress = Ingress.from_service_name(
        "argocd-server", "https", "argo.ocf.berkeley.edu"
    )
    return (
        edit_manifests(
            {
                ("ConfigMap", "argocd-cm"): lambda m: shelve(
                    m,
                    ("data",),
                    {
                        "url": "https://argocd.ocf.berkeley.edu",
                        "resource.exclusions": yaml.dump(
                            [
                                {
                                    "apiGroups": ["cilium*"],
                                    "kinds": ["CiliumIdentity"],
                                    "clusters": ["*"],
                                }
                            ]
                        ),
                        "repositories": "- url: https://github.com/ocf/kubernetes",
                    },
                ),
                ("ConfigMap", "argocd-rbac-cm"): lambda m: shelve(
                    m, ("data",), {"policy.csv": "g, ocfroot, role:admin"}
                ),
                ("Service", "argocd-server"): lambda m: shelve(
                    m,
                    (
                        "metadata",
                        "annotations",
                        "projectcontour.io/upstream-protocol.tls",
                    ),
                    "https",
                    create_parents=True,
                ),
                ("Deployment", "argocd-redis-ha-haproxy"): make_edit_manifest(
                    {
                        # Run 3 replicas...
                        ("spec", "replicas"): 3,
                        # ...but make sure we never surge above 3 because we only
                        # have 3 nodes (otherwise we would be unable to progress
                        # the deployment because of the node antiaffinity)
                        ("spec", "strategy", "rollingUpdate", "maxSurge"): 0,
                        ("spec", "strategy", "rollingUpdate", "maxUnavailable"): 1,
                    },
                    create_parents=True,
                ),
            },
            base,
        )
        + [ingress.data, base_deployment]
    )
