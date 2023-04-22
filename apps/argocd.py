import yaml
from transpire import helm
from transpire.utils import get_versions

name = "argocd"


def objects():
    yield from helm.build_chart_from_versions(
        name="argocd",
        versions=get_versions(__file__),
        values={
            "redis-ha": {"enabled": True},
            "controller": {
                "replicas": 1,
                "metrics": {
                    "enabled": True,
                    "serviceMonitor": {
                        "enabled": True,
                    },
                },
            },
            "server": {
                "replicas": 2,
                "ingress": {
                    "enabled": True,
                    "ingressClassName": "contour",
                    "hosts": ["argo.ocf.berkeley.edu"],
                    "tls": [
                        {
                            "secretName": "argocd-server-tls",
                            "hosts": ["argo.ocf.berkeley.edu"],
                        },
                    ],
                },
            },
            "repoServer": {"replicas": 2},
            "applicationSet": {"replicaCount": 2},
            "configs": {
                "cm": {
                    "url": "https://argo.ocf.berkeley.edu",
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
                },
                "params": {
                    "server.insecure": True,
                },
                "repositories": {
                    "cluster": {
                        "url": "https://github.com/ocf/cluster",
                    },
                },
                "rbac": {"policy.csv": "g, ocfroot, role:admin"},
            },
        },
    )

    yield {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Application",
        "metadata": {"name": "bootstrap", "namespace": "argocd"},
        "spec": {
            "project": "default",
            "destination": {"server": "https://kubernetes.default.svc"},
            "source": {
                "repoURL": "https://github.com/ocf/cluster",
                "path": "base",
            },
        },
    }
