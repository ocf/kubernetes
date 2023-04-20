import secrets

from transpire import helm, surgery
from transpire.utils import get_versions

name = "harbor"

harbor_registry_password = secrets.token_urlsafe(16)
values = {
    "exposureType": "ingress",
    "ingress": {
        "core": {
            "ingressClassName": "contour",
            "hostname": "harbor.ocf.berkeley.edu",
            "annotations": {
                "cert-manager.io/cluster-issuer": "letsencrypt",
                "kubernetes.io/tls-acme": "true",
            },
            "tls": True,
            # Default is ImplementationSpecific, which does regex match for Cilium.
            # Regex match does not work because it takes the path as a literal regex,
            # and the regex `/foo` does not match `/`.
            "pathType": "Prefix",
        },
        "notary": {
            "ingressClassName": "contour",
            "hostname": "harbor-notary.ocf.berkeley.edu",
            "annotations": {
                "cert-manager.io/cluster-issuer": "letsencrypt",
                "kubernetes.io/tls-acme": "true",
            },
            "tls": True,
            # See above.
            "pathType": "Prefix",
        },
    },
    "externalURL": "https://harbor.ocf.berkeley.edu",
    "forcePassword": True,
    # This helm chart has default passwords like "not-secure-database-password" and "registry_password" so...
    # I am pretty sure most harbor instances in the wild are vulnerable as a result, which is great and fantastic.
    "harborAdminPassword": secrets.token_urlsafe(24),
    # "core": {"secretKey": "aaaaaaaaaaaaaaaa", "secret": "aaaaaaaaaaaaaaaa"},
    "registry": {
        "credentials": {
            "username": "harbor_registry_user",
            "password": harbor_registry_password,
            # TODO: This doesn't work, you need to bcrypt.hashpw(password=b'password', salt=bcrypt.gensalt())
            # ... but we can't depend on bcrypt because it's not in stdlib, so it has to be added to transpire!
            "htpasswd": f"harbor_registry_user:{harbor_registry_password}",
        },
    },
    "postgresql": {"auth": {"postgresPassword": secrets.token_urlsafe(24)}},
    "metrics": {
        "enabled": True,
        "serviceMonitor": {
            "enabled": True,
        },
    }
}


def strip_secret_checksum(m):
    """
    Bludgeon all checksum annotations for secrets since they are managed in
    vault, and the chart autogenerates certificates which change each run
    """
    # spec.template.metadata.annotations['checksum/secret*']
    annotations = surgery.delve(m, ("spec", "template", "metadata", "annotations"))
    if annotations is not None:
        for key, value in list(annotations.items()):
            if key.startswith("checksum/secret"):
                del annotations[key]
    return m


def objects():
    yield from [
        strip_secret_checksum(m)
        for m in helm.build_chart_from_versions(
            name="harbor",
            versions=get_versions(__file__),
            values=values,
        )
    ]
