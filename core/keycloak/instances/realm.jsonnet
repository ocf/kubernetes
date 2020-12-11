// https://github.com/keycloak/keycloak-operator/blob/master/deploy/crds/keycloak.org_keycloakrealms_crd.yaml

{
  "apiVersion": "keycloak.org/v1alpha1",
  "kind": "KeycloakRealm",
  "metadata": {
    "name": "example-keycloakrealm",
    "labels": {
      "app": "sso"
    }
  },
  "spec": {
    "realm": {
      "id": "basic",
      "realm": "basic",
      "enabled": true,
      "displayName": "Basic Realm"
    },
    "instanceSelector": {
      "matchLabels": {
        "app": "sso"
      }
    }
  }
}