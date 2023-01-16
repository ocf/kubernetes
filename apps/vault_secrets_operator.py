from transpire import helm
from transpire.utils import get_versions

name = "vault-secrets-operator"
values = {
    "vault": {
        "authMethod": "kubernetes",
        "address": "http://vault.vault.svc.cluster.local:8200",
    },
}


def objects():
    yield from helm.build_chart_from_versions(
        name="vault-secrets-operator",
        versions=get_versions(__file__),
        values=values,
    )
