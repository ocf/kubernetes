from transpire import helm
from transpire.resources import Secret
from transpire.utils import get_versions

name = "cert-manager"


def objects():
    # Secret to allow cert-manager to create DNS01 entries in BIND.
    tsig_secret = "ocf-tsig"
    tsig_key = "key"
    yield Secret.simple(
        name="ocf-tsig",
        string_data={
            tsig_key: "",
        },
    )

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
                                        "key": tsig_key,
                                        "name": tsig_secret,
                                    },
                                },
                            }
                        }
                    ],
                }
            },
        }

    yield from helm.build_chart_from_versions(
        name="cert-manager",
        versions=get_versions(__file__),
        values={
            "installCRDs": True,
        },
    )

    yield make_le_issuer(
        "letsencrypt", "https://acme-v02.api.letsencrypt.org/directory"
    )

    yield make_le_issuer(
        "letsencrypt-staging", "https://acme-staging-v02.api.letsencrypt.org/directory"
    )
