from transpire import helm
from transpire.surgery import edit_manifests
from transpire.utils import get_versions

values = {
    "clusterName": "dev-tele.ocf.io",
    "kubeClusterName": "gravitywell.ocf.io",
    "enterprise": True,
    "highAvailability": {
        "replicaCount": 1,
        "certManager": {
            "enabled": True,
            "issuerName": "letsencrypt",
            "issuerKind": "ClusterIssuer",
        },
    },
    "proxy": {
        "highAvailability": {
            "replicaCount": 1,
        },
    },
    "service": {
        "spec": {
            "loadBalancerIP": "169.229.226.106",
        },
    },
}

name = "teleport"


def objects():
    yield from helm.build_chart_from_versions(
        name="teleport",
        versions=get_versions(__file__),
        values=values,
    )

    yield {
        "apiVersion": "ricoberger.de/v1alpha1",
        "kind": "VaultSecret",
        "metadata": {"name": "license"},
        "spec": {
            "keys": ["license.pem"],
            "path": "kvv2/teleport/license",
            "type": "Opaque",
        },
    }
