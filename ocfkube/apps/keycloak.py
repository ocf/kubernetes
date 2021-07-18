import requests
import yaml

base_url = (
    "https://raw.githubusercontent.com/keycloak/keycloak-operator/11.0.3/deploy/{}"
)
paths = [
    "crds/keycloak.org_keycloakbackups_crd.yaml",
    "crds/keycloak.org_keycloakclients_crd.yaml",
    "crds/keycloak.org_keycloakrealms_crd.yaml",
    "crds/keycloak.org_keycloaks_crd.yaml",
    "crds/keycloak.org_keycloakusers_crd.yaml",
    "role.yaml",
    "role_binding.yaml",
    "service_account.yaml",
    "operator.yaml",
]
settings = {
    "apiVersion": "keycloak.org/v1alpha1",
    "kind": "Keycloak",
    "metadata": {"name": "keycloak", "labels": {"app": "sso"}},
    "spec": {
        "instances": 1,
        "extensions": [
            "https://github.com/aerogear/keycloak-metrics-spi/releases/download/1.0.4/keycloak-metrics-spi-1.0.4.jar"
        ],
        "externalAccess": {"enabled": False},
    },
}


def build() -> object:
    yamls = []
    for path in paths:
        yamls += list(yaml.safe_load_all(requests.get(base_url.format(path)).text))
    return yamls + settings
