from apps.versions import versions
from transpire.dsl import emit
from transpire.dsl import helm

values = {
    "installCRDs": True,
}

cluster_issuer = {
    "apiVersion": "cert-manager.io/v1",
    "kind": "ClusterIssuer",
    "metadata": {"name": "letsencrypt", "namespace": "cert-manager"},
    "spec": {
        "acme": {
            "email": "root@ocf.berkeley.edu",
            "privateKeySecretRef": {"name": "letsencrypt"},
            "server": "https://acme-v02.api.letsencrypt.org/directory",
            "solvers": [{"http01": {"ingress": {"class": "contour"}}}],
        }
    },
}


def build() -> None:
    helm_contents = helm.build_chart_from_versions(
        name="cert-manager",
        versions=versions,
        values=values,
    )
    emit(helm_contents)
    emit(cluster_issuer)
