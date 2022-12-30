from transpire import helm
from transpire.surgery import edit_manifests

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
    yield from edit_manifests(
        {
            (("policy/v1beta1", "PodSecurityPolicy"), "teleport"):
            # PSPs no longer exist in kubernetes (deprecated in 1.21), so remove
            # the generated one
            # TODO: add back the securityContext settings applied by this PSP
            lambda _: None,
            # Associated RBAC for PSP
            (("rbac.authorization.k8s.io/v1", "Role"), "teleport-psp"): lambda _: None,
            (
                ("rbac.authorization.k8s.io/v1", "RoleBinding"),
                "teleport-psp",
            ): lambda _: None,
        },
        helm.build_chart_from_versions(
            name="teleport",
            versions=versions,
            values=values,
        ),
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
