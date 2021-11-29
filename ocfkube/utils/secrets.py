import base64
import subprocess
import os
from typing import Tuple


def fix_base64(pairs: dict) -> dict:
    """Runs base64^-1(v) on every value in a dict."""
    return {k: base64.b64decode(v).decode() for k, v in pairs.items()}


def extract_secret(secret: dict) -> Tuple[str, dict]:
    """Takes a Kubernetes secret object, returns analogous Vault path and the k:v secrets."""
    # TODO: Handle generateName? Though who would put generateName on a secret? Does that even work???
    return {**fix_base64(secret.get("data", {})), **secret.get("stringData", {})}


def encrypt_value(key: str, value: str) -> str:
    """Encrypt a secret with the public key of the cluster."""
    return subprocess.run(
        ["arcanum-cli", "encrypt", str(value)],
        env={"ARCANUM_PUB_KEY": key, "PATH": os.getenv("PATH")},
        capture_output=True,
    ).stdout


def convert_secret(secret: dict, context: dict, bootstrap: bool = False) -> dict:
    """Takes a Kubernetes secret object, pushes it to Vault (if not bootstrap), returns VaultSecret object."""
    pub_key = "08TiLEIqvq2yDWSx1yGNwI5ICtld+ZyMzuvxqXxkA8M="

    return {
        "apiVersion": "njha.dev/v1",
        "kind": "SyncedSecret",
        "metadata": secret["metadata"],
        # Explicitly puts the key names in the object, so you can tell if a secret changed from `git diff`.
        "spec": {
            "data": {
                key: str(encrypt_value(pub_key, value).decode('utf-8')).strip() for (key, value) in extract_secret(secret).items()
            },
            "pub_key": pub_key,
        },
    }
