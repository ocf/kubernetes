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

    if o["kind"] == "Deployment" and o["metadata"]["name"] == "argocd-repo-server":
        pod_spec = o["spec"]["template"]["spec"]
        volume_mounts = [
            {"mountPath": "/usr/local/sbin", "name": "usr-local-bin"},
            {"mountPath": "/usr/local/include", "name": "usr-local-include"},
            {"mountPath": "/usr/local/lib", "name": "usr-local-lib"},
        ]

        pod_spec["containers"][0]["volumeMounts"] += volume_mounts
        pod_spec["containers"][0]["env"] = pod_spec["containers"][0].get("env", [])
        pod_spec["containers"][0]["env"].append(
            {"name": "LD_LIBRARY_PATH", "value": "/usr/local/lib"},
        )
        volumes = [
            {
                "name": "usr-local-lib",
                "emptyDir": {},
            },
            {
                "name": "usr-local-include",
                "emptyDir": {},
            },
            {
                "name": "usr-local-bin",
                "emptyDir": {},
            },
        ]
        pod_spec["volumes"] += volumes
        init_containers = yaml.safe_load(
            textwrap.dedent(
                """
                    - name: python
                      image: python:3.9-buster
                      command: ["sh", "-c"]
                      args:
                      - cp -r /usr/local/bin/. /mnt/usr/local/bin/ &&
                        cp -r /usr/local/include/. /mnt/usr/local/include/ &&
                        cp -r /usr/local/lib/. /mnt/usr/local/lib/
                      volumeMounts:
                      - mountPath: /mnt/usr/local/bin
                        name: usr-local-bin
                      - mountPath: /mnt/usr/local/include
                        name: usr-local-include
                      - mountPath: /mnt/usr/local/lib
                        name: usr-local-lib
                """,
            ),
        )
        pod_spec["initContainers"] = init_containers

    if o["kind"] == "Deployment" and o["metadata"]["name"] == "argocd-server":
        o["spec"]["template"]["spec"]["containers"][0]["command"] = [
            "argocd-server",
            "--staticassets",
            "/shared/app",
            "--redis",
            "argocd-redis-ha-haproxy:6379",
            "--insecure",
        ]
    return o
