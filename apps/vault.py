import textwrap

from transpire import helm
from transpire.utils import get_versions

name = "vault"


def objects():
    yield {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {"name": "ocf-rootca"},
        "data": {
            "root.crt": textwrap.dedent(
                """
                -----BEGIN CERTIFICATE-----
                MIIC7jCCAk+gAwIBAgIUZPQZpVG1GfVIKkcvKb5vwky5RTAwCgYIKoZIzj0EAwQw
                gY8xCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMREwDwYDVQQHEwhC
                ZXJrZWxleTEgMB4GA1UEChMXT3BlbiBDb21wdXRpbmcgRmFjaWxpdHkxDDAKBgNV
                BAsTA0FsbDEoMCYGA1UEAxMfT3BlbiBDb21wdXRpbmcgRmFjaWxpdHkgUm9vdCBY
                MTAgFw0yMzAxMTYyMzM5MDBaGA8yMTIzMDExNjIzMzkwMFowgY8xCzAJBgNVBAYT
                AlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMREwDwYDVQQHEwhCZXJrZWxleTEgMB4G
                A1UEChMXT3BlbiBDb21wdXRpbmcgRmFjaWxpdHkxDDAKBgNVBAsTA0FsbDEoMCYG
                A1UEAxMfT3BlbiBDb21wdXRpbmcgRmFjaWxpdHkgUm9vdCBYMTCBmzAQBgcqhkjO
                PQIBBgUrgQQAIwOBhgAEAaXbYJW1MmFY27rALUopMUWDNC4DS+A4trLyTOqf8M+x
                OrIDDkaEZHjhD5ofAcsyCKQf4tMNGqsj4RKAYhOxJLLDAHJLcpV63S+EojFkUJpr
                PtH81lf9toed/yi16f+V159qQ+PF+cGSXkHSyzUHPcqhuVrbuH37/AJNohgDPGmN
                rKWDo0IwQDAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4E
                FgQUYk/x6J54THpb1Xv9lNNqZWvbEtMwCgYIKoZIzj0EAwQDgYwAMIGIAkIBzWa7
                +3IgvnGLPv5UaU1tQVOGfAfvW3LYtZSDZ543bAIFVNLxpdhozZAeAfjBuPzSY/yh
                T1O56toa7dMv4tILfGsCQgGSQ3VEVnuqwUTGnchcZYsHZtsRSQ/AglekXrphZCxa
                xqg2jrBElQrI7xM3NcqlerzdvSzMgVJA3XyqXQJ7uAC9ag==
                -----END CERTIFICATE-----
                """
            )
        },
    }

    yield from helm.build_chart_from_versions(
        name="vault",
        versions=get_versions(__file__),
        values={
            "global": {"enabled": True, "tlsDisable": False},
            "server": {
                "readinessProbe": {"enabled": False},
                "livenessProbe": {"enabled": False, "initialDelaySeconds": 60},
                "auditStorage": {"enabled": True, "storageClass": "rbd-nvme"},
                "dataStorage": {"storageClass": "rbd-nvme"},
                "image": {"tag": "1.12.2"},
                "ingress": {
                    "enabled": True,
                    "annotations": {
                        "cert-manager.io/cluster-issuer": "letsencrypt",
                        "ingress.kubernetes.io/force-ssl-redirect": "true",
                        "kubernetes.io/ingress.class": "contour",
                        "kubernetes.io/tls-acme": "true",
                    },
                    "hosts": [{"host": "vault.ocf.berkeley.edu", "paths": []}],
                    "tls": [
                        {
                            "hosts": ["vault.ocf.berkeley.edu"],
                            "secretName": "vault-ingress-tls",
                        },
                    ],
                },
                "volumes": [
                    {"name": "ocf-rootca", "configMap": {"name": "ocf-rootca"}}
                ],
                "volumeMounts": [
                    {
                        "mountPath": "/etc/ssl/certs/ocfroot.pem",
                        "name": "ocf-rootca",
                        "subPath": "ocfroot.pem",
                    }
                ],
                "standalone": {"enabled": False},
                "ha": {
                    "enabled": True,
                    "replicas": 3,
                    "raft": {
                        "enabled": True, 
                        "setNodeId": True, 
                        # for metrics, as recommended by the spec https://artifacthub.io/packages/helm/hashicorp/vault?modal=values&path=serverTelemetry.serviceMonitor
                        "config": 
                            r'listener "tcp" { "telemetry" { "unauthenticated_metrics_access" = "true"}}'
                    },
                    # for metrics, as recommended by the spec https://artifacthub.io/packages/helm/hashicorp/vault?modal=values&path=serverTelemetry.serviceMonitor
                    "config": 
                        r'"telemetry" { "prometheus_retention_time" = "30s", "disable_hostname" = "true"}'
                },
            },
            "ui": {"enabled": True},
            "injector": {"enabled": True},
            "serverTelemetry": {
                "serviceMonitor": {
                    "enabled": True,
                },
            },
        },
    )
