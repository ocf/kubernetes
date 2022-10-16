from transpire import emit, helm

from apps.versions import versions

name = "vault"
values = {
    "global": {"enabled": True, "tlsDisable": False},
    "server": {
        "readinessProbe": {"enabled": False},
        "livenessProbe": {"enabled": False, "initialDelaySeconds": 60},
        "auditStorage": {"enabled": True, "storageClass": "rook-ceph-block"},
        "dataStorage": {"storageClass": "rook-ceph-block"},
        "image": {"tag": "1.6.0"},
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
        "standalone": {"enabled": False},
        "ha": {
            "enabled": True,
            "replicas": 3,
            "raft": {"enabled": True, "setNodeId": True},
        },
    },
    "ui": {"enabled": True},
}


def objects() -> None:
    emit(
        helm.build_chart_from_versions(
            name="vault",
            versions=versions,
            values=values,
        )
    )
