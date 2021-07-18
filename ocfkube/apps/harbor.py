from ocfkube.utils import helm
from ocfkube.utils import versions

values = {
    "service": {
        "type": "Ingress",
        "tls": {
            "enabled": True,
            "existingSecret": "harbor-tls",
            "notaryExistingSecret": "harbor-notary-tls",
        },
    },
    "ingress": {
        "enabled": True,
        "hosts": {
            "core": "harbor.ocf.berkeley.edu",
            "notary": "harbor-notary.ocf.berkeley.edu",
        },
        "annotations": {
            "cert-manager.io/cluster-issuer": "letsencrypt",
            "ingress.kubernetes.io/force-ssl-redirect": "true",
            "kubernetes.io/tls-acme": "true",
        },
    },
    "externalURL": "https://harbor.ocf.berkeley.edu",
    "forcePassword": True,
    "harborAdminPassword": "nice-try-this-isnt-it",
    "core": {"secretKey": "aaaaaaaaaaaaaaaa", "secret": "aaaaaaaaaaaaaaaa"},
}


def build() -> object:
    return helm.build_chart_from_versions(
        name="harbor",
        versions=versions,
        values=values,
    )
