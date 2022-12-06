from transpire import helm

from apps.versions import versions

values = {
    "installCRDs": True,
}


def make_le_issuer(name: str, endpoint: str) -> dict:
    return {
        "apiVersion": "cert-manager.io/v1",
        "kind": "ClusterIssuer",
        "metadata": {
            "name": name,
        },
        "spec": {
            "acme": {
                "email": "root@ocf.berkeley.edu",
                "server": endpoint,
                "privateKeySecretRef": {
                    "name": name,
                },
                "solvers": [
                    {
                        "dns01": {
                            "cnameStrategy": "Follow",
                            "rfc2136": {
                                "nameserver": "169.229.226.22",
                                "tsigAlgorithm": "HMACSHA512",
                                "tsigKeyName": "letsencrypt.ocf.io",
                                "tsigSecretSecretRef": {
                                    "key": "key",
                                    "name": "ocf-tsig",
                                },
                            },
                        }
                    }
                ],
            }
        },
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
            "solvers": [{"http01": {"ingress": {"class": "cilium"}}}],
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

    yield make_le_issuer(
        "letsencrypt", "https://acme-v02.api.letsencrypt.org/directory"
    )
    yield make_le_issuer(
        "letsencrypt-staging", "https://acme-staging-v02.api.letsencrypt.org/directory"
    )
    yield {
        "apiVersion": "ricoberger.de/v1alpha1",
        "kind": "VaultSecret",
        "metadata": {"name": "ocf-tsig"},
        "spec": {
            "keys": ["key"],
            "path": "kvv2/cert-manager/ocf-tsig",
            "type": "Opaque",
        },
    }
