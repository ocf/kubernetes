from transpire import helm

from apps.versions import versions

values = {
    "clusterName": "tele.ocf.io",
    "kubeClusterName": "dna.ocf.io",
    "enterprise": True,
    # "acme": False,
    "highAvailability": {
        # "replicaCount": 2,
        # "podDisruptionBudget": {
            # "enabled": True,
            # "minAvailable": 1,
        # },
        "certManager": {
            "enabled": True,
            "issuerName": "letsencrypt",
            "issuerKind": "ClusterIssuer",
        }
    },
    "service": {
        "spec": {
            "loadBalancerIP": "169.229.226.82",
        },
    },
}

name = "teleport"

def objects():
    yield from helm.build_chart_from_versions(
        name="teleport",
        versions=versions,
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
 
