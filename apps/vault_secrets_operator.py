from transpire import helm

from apps.versions import versions

name = "vault-secrets-operator"
values = {
    "vault": {
        "authMethod": "kubernetes",
        "address": "http://ocf-vault.vault:8200",
    },
}

def objects():
    yield from helm.build_chart_from_versions(
        name="vault-secrets-operator",
        versions=versions,
        values=values,
    )
