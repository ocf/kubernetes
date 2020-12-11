{
  "apiVersion": "keycloak.org/v1alpha1",
  "kind": "KeycloakClient",
  "metadata": {
    "name": "harbor",
    "labels": {
      "app": "sso"
    },
  },
  "spec": {
    "realmSelector": {
      "matchLabels": {
        "app": "sso"
      }
    },
    "client": {
      "clientId": "harbor",
      "secret": "client-secret",
      "clientAuthenticatorType": "client-secret",
      "protocol": "openid-connect"
    }
  }
}
