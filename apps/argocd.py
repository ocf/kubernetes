import json

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
            "global": {
                "domain": "dev-argo.ocf.berkeley.edu",
            },
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
                    "hosts": ["dev-argo.ocf.berkeley.edu"],
                    "annotations": {
                        "cert-manager.io/cluster-issuer": "letsencrypt",
                        "projectcontour.io/websocket-routes": "/",
                        "ingress.kubernetes.io/force-ssl-redirect": "true",
                        "kubernetes.io/tls-acme": "true",
                    },
                    "tls": [
                        {
                            "secretName": "argocd-server-tls",
                            "hosts": ["dev-argo.ocf.berkeley.edu"],
                        },
                    ],
                },
            },
            "repoServer": {"replicas": 2},
            "applicationSet": {"replicaCount": 2},
            "configs": {
                "cm": {
                    "url": "https://dev-argo.ocf.berkeley.edu",
                    "oidc.config": yaml.dump(
                        {
                            "name": "Keycloak",
                            "issuer": "https://idm.ocf.berkeley.edu/realms/ocf",
                            "clientID": "dev-argocd",
                            "clientSecret": "$oidc.keycloak.clientSecret",
                            "requestedScopes": [
                                "openid",
                                "profile",
                                "email",
                                "groups",
                            ],
                        }
                    ),
                    "resource.customizations.ignoreDifferences.admissionregistration.k8s.io_MutatingWebhookConfiguration": json.dumps(
                        {
                            "jqPathExpressions": [
                                ".webhooks[]?.clientConfig.caBundle",
                            ]
                        }
                    ),
                    "resource.customizations.ignoreDifferences.apiextensions.k8s.io_CustomResourceDefinition": json.dumps(
                        {
                            "jqPathExpressions": [
                                ".spec.conversion.webhook.clientConfig.caBundle",
                            ]
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
                "ref": "dev",
            },
        },
    }
