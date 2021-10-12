import base64
import os
from typing import Tuple

import hvac


def fix_base64(pairs: dict) -> dict:
    """Runs base64^-1(v) on every value in a dict."""
    return {k: base64.b64decode(v).decode() for k, v in pairs.items()}


def extract_secret(secret: dict, appname: str) -> Tuple[str, dict]:
    """Takes a Kubernetes secret object, returns analogous Vault path and the k:v secrets."""
    # TODO: Handle generateName? Though who would put generateName on a secret? Does that even work???
    path = (
        f"{secret['metadata'].get('namespace', appname)}/{secret['metadata']['name']}"
    )
    print(secret)
    return path, {**fix_base64(secret.get("data", {})), **secret.get("stringData", {})}


def convert_secret(secret: dict, context: dict, bootstrap: bool = False) -> dict:
    """Takes a Kubernetes secret object, pushes it to Vault (if not bootstrap), returns VaultSecret object."""
    if bootstrap:
        return secret

    client = hvac.Client("https://vault.ocf.berkeley.edu")
    client.token = os.getenv("VAULT_TOKEN")
    if not client.token:
        print(
            "I couldn't find your VAULT_TOKEN env variable, so I can't push secrets to Vault.",
        )
    assert client.is_authenticated()
    client.secrets.kv.v2.configure(mount_point="pwned")

    path, pairs = extract_secret(secret, context["appname"])
    try:
        client.secrets.kv.v2.create_or_update_secret(
            path=path,
            secret=pairs,
            cas=0,
            mount_point="pwned",
        )
    except hvac.exceptions.InvalidRequest:
        # TODO: Try to get the secret, see if there are any new fields. If there are, add those to Vault.
        # If there are extra fields, print an error so people looking at CI logs can see!
        print(f"'{path}' already created, not re-creating")

    return {
        "apiVersion": "ricoberger.de/v1alpha1",
        "kind": "VaultSecret",
        "metadata": secret["metadata"],
        # Explicitly puts the key names in the object, so you can tell if a secret changed from `git diff`.
        "spec": {
            "keys": [key for key in pairs],
            "path": f"pwned/{path}",
            "type": "Opaque",
        },
    }
