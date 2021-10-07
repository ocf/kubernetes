from typing import Tuple
import base64
import os
import hvac


def fix_base64(pairs: dict) -> dict:
    """Runs base64^-1(v) on every value in a dict."""
    {k: base64.b64decode(v) for k, v in pairs}


def extract_secret(secret: dict) -> Tuple[str, dict]:
    """Takes a Kubernetes secret object, returns analogous Vault path and the k:v secrets."""
    # TODO: Handle generateName? Though who would put generateName on a secret? Does that even work???
    path = (
        f"{secret['metadata'].get('namespace', 'default')}/{secret['metadata']['name']}"
    )
    return path, {**fix_base64(secret.get("data", {})), **secret.get("stringData", {})}


def convert_secret(secret: dict, bootstrap: bool = False) -> dict:
    """Takes a Kubernetes secret object, pushes it to Vault (if not bootstrap), returns VaultSecret object."""
    if bootstrap:
        return secret

    client = hvac.Client("https://vault.ocf.berkeley.edu")
    client.token = os.get("VAULT_TOKEN")
    if not client.token:
        print(
            "I couldn't find your VAULT_TOKEN env variable, so I can't push secrets to Vault."
        )
    assert client.is_authenticated()
    client.secrets.kv.v2.configure(mount_point="pwned")

    path, pairs = extract_secret(secret)
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
        "metadata": {"name": secret["metadata"]["name"]},
        # Explicitly puts the key names in the object, so you can tell if a secret changed from `git diff`.
        "spec": {"keys": [key for key in pairs], "path": f"pwned/{path}", "type": "Opaque"},
    }
