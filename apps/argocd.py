import requests
import yaml
from transpire import emit, surgery
from transpire.resources.ingress import Ingress

from apps.versions import versions

name = "argocd"

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


def objects() -> None:
    contents = requests.get(
        f"https://raw.githubusercontent.com/argoproj/argo-cd/v{versions['argocd']['version']}/manifests/ha/install.yaml",
    )
    contents.raise_for_status()
    emit(
        surgery.edit_manifests(
            {
                ("ConfigMap", "argocd-cm"): lambda m: surgery.shelve(
                    m,
                    ("data",),
                    {
                        "url": "https://argo.ocf.berkeley.edu",
                        "resource.exclusions": yaml.dump(
                            [
                                {
                                    "apiGroups": ["cilium*"],
                                    "kinds": ["CiliumIdentity"],
                                    "clusters": ["*"],
                                }
                            ]
                        ),
                        "oidc.config": yaml.dump(
                            {
                                "name": "Keycloak",
                                "issuer": "https://auth.ocf.berkeley.edu/auth/realms/ocf",
                                "clientID": "argocd",
                                "clientSecret": "$oidc.keycloak.clientSecret",
                                "requestedScopes": [
                                    "openid",
                                    "profile",
                                    "email",
                                    "groups",
                                ],
                            }
                        ),
                        "repositories": "- url: https://github.com/ocf/kubernetes",
                    },
                ),
                ("ConfigMap", "argocd-rbac-cm"): lambda m: surgery.shelve(
                    m, ("data",), {"policy.csv": "g, ocfroot, role:admin"}
                ),
                ("Service", "argocd-server"): lambda m: surgery.shelve(
                    m,
                    (
                        "metadata",
                        "annotations",
                        "projectcontour.io/upstream-protocol.tls",
                    ),
                    "https",
                    create_parents=True,
                ),
                ("Deployment", "argocd-redis-ha-haproxy"): surgery.make_edit_manifest(
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
            yaml.safe_load_all(contents.text),
        )
    )

    ingress = Ingress.simple(
        "argo.ocf.berkeley.edu", "argocd-server", "https", "argocd-server"
    )
    emit(ingress)
