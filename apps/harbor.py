from transpire import helm, surgery

from apps.versions import versions

name = "harbor"

values = {
    "exposureType": "ingress",
    "ingress": {
        "core": {
            "ingressClassName": "cilium",
            "hostname": "harbor.ocf.berkeley.edu",
            "annotations": {
                "cert-manager.io/cluster-issuer": "letsencrypt",
                "ingress.kubernetes.io/force-ssl-redirect": "true",
                "kubernetes.io/tls-acme": "true",
            },
            "tls": True,
        },
        "notary": {
            "ingressClassName": "cilium",
            "hostname": "harbor-notary.ocf.berkeley.edu",
            "annotations": {
                "cert-manager.io/cluster-issuer": "letsencrypt",
                "ingress.kubernetes.io/force-ssl-redirect": "true",
                "kubernetes.io/tls-acme": "true",
            },
            "tls": True,
        },
    },
    "externalURL": "https://harbor.ocf.berkeley.edu",
    "forcePassword": True,

    # This helm chart is a little, well, uh... we just override this from Vault.
    "harborAdminPassword": "nice-try-this-isnt-it",
    "core": {"secretKey": "aaaaaaaaaaaaaaaa", "secret": "aaaaaaaaaaaaaaaa"},
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
                versions=versions,
                values=values,
            )
        ]
