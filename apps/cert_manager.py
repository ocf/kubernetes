from transpire import helm

from apps.versions import versions

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

name = "cert-manager"

def objects():
    yield from helm.build_chart_from_versions(
        name="cert-manager",
        versions=versions,
        values=values,
    )
    yield cluster_issuer

