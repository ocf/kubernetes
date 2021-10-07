import hvac


def get_path_from_secret(secret: dict):
    pass


def get_value_from_secret(secret: dict):
    pass


def get_key_from_secret(secret: dict):
    pass


def process_secret(secret: dict, token: str, bootstrap: bool = False) -> dict:
    """Takes a Kubernetes secret object, pushes it to Vault (if not bootstrap), returns VaultSecret object."""
    if bootstrap:
        return secret
    path = get_path_from_secret(secret)
    key = get_key_from_secret(secret)
    client = hvac.Client("https://vault.ocf.berkeley.edu")
    client.token = token
    assert client.is_authenticated()
    client.secrets.kv.v2.configure(mount_point='pwned')
    try:
        data = client.secrets.kv.v2.read_secret_version(path=path, mount_point='pwned')
        value = data["data"]["data"][key]
    except hvac.exceptions.InvalidPath:
        value = get_value_from_secret(secret)
        client.secrets.kv.v2.create_or_update_secret(
            path=path, secret={key: value}, cas=0, mount_point='pwned',
        )
